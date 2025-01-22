import argparse
import json
import os
import subprocess
import wave
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import numpy as np
from vosk import Model, KaldiRecognizer, SetLogLevel
from tqdm import tqdm
from transformers import pipeline

class AdvancedSubtitleGenerator:
    def __init__(self, config: Dict):
        self.config = self._validate_config(config)
        SetLogLevel(-1)
        self.punctuator = None
        self._init_logging()
        self._load_punctuation_model()
        
    def _init_logging(self):
        logging.basicConfig(
            level=logging.DEBUG if self.config['debug'] else logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def _load_punctuation_model(self):
        if self.config['punctuation']:
            self.punctuator = pipeline(
                "text2text-generation",
                model="oliverguhr/fullstop-punctuation-multilang-large",
                framework="pt",
                device=-1
            )
            
    def _validate_config(self, config: Dict) -> Dict:
        required_keys = ['video_paths', 'output_dir', 'model_path']
        for key in required_keys:
            if key not in config:
                raise KeyError(f"Missing required config key: {key}")
                
        if not Path(config['model_path']).exists():
            raise FileNotFoundError(f"Model path not found: {config['model_path']}")
            
        config.setdefault('batch_size', 1)
        config.setdefault('max_duration', 8.0)
        config.setdefault('max_chars', 45)
        config.setdefault('max_lines', 2)
        config.setdefault('audio_quality', 3)
        config.setdefault('debug', False)
        config.setdefault('target_languages', ['en'])
        config.setdefault('speaker_diarization', False)
        
        return config

    def _get_audio_duration(self, audio_path: str) -> float:
        with wave.open(audio_path, 'rb') as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            return frames / float(rate)

    def _enhance_audio(self, video_path: str, audio_path: str):
        filters = [
            "highpass=f=200",
            "lowpass=f=3000",
            "loudnorm=I=-16:TP=-1.5:LRA=11",
            "compand=attacks=0:decays=0.3:soft-knee=6:gain=-3"
        ]
        
        cmd = [
            'ffmpeg', '-y', '-i', video_path,
            '-ac', '1', '-ar', '16000',
            '-af', ','.join(filters),
            '-loglevel', 'error',
            audio_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"FFmpeg error: {e.stderr.decode()}")
            raise

    def _transcribe_audio(self, audio_path: str) -> List[Dict]:
        model = Model(self.config['model_path'])
        recognizer = KaldiRecognizer(model, 16000)
        recognizer.SetWords(True)
        
        duration = self._get_audio_duration(audio_path)
        progress = tqdm(total=duration, desc="Transcribing", unit="sec")
        
        results = []
        with wave.open(audio_path, 'rb') as wf:
            while True:
                data = wf.readframes(4000)
                if len(data) == 0: break
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    results.append(result)
                    progress.update(result['result'][-1]['end'] - progress.n if result['result'] else 0)
            results.append(json.loads(recognizer.FinalResult()))
            
        progress.close()
        return self._process_results(results)

    def _restore_punctuation(self, text: str) -> str:
        if self.punctuator:
            return self.punctuator(
                text,
                max_length=512,
                num_beams=5,
                repetition_penalty=2.0,
                clean_up_tokenization_spaces=True
            )[0]['generated_text']
        return text

    def _process_results(self, results: List[Dict]) -> List[Dict]:
        processed = []
        for res in results:
            if not res.get('result'): continue
            
            words = res['result']
            start = round(words[0]['start'], 2)
            end = round(words[-1]['end'], 2)
            raw_text = ' '.join([w['word'] for w in words])
            
            text = self._restore_punctuation(raw_text)
            if text and text[-1] not in {'.', '?', '!'}:
                text += '.'
                
            processed.append({
                'start': start,
                'end': end,
                'text': text.strip().capitalize(),
                'confidence': np.mean([w['conf'] for w in words]),
                'speaker': 'SPK1'  # Placeholder for diarization
            })
        return processed

    def _optimize_segmentation(self, items: List[Dict]) -> List[Dict]:
        optimized = []
        buffer = []
        
        for item in items:
            if not buffer:
                buffer.append(item)
                continue
                
            current_duration = item['end'] - buffer[0]['start']
            current_length = sum(len(i['text']) for i in buffer) + len(item['text'])
            
            if (current_duration <= self.config['max_duration'] and
                current_length <= self.config['max_chars'] * self.config['max_lines'] and
                len(buffer) < self.config['max_lines']):
                buffer.append(item)
            else:
                optimized.append(self._merge_segment(buffer))
                buffer = [item]
                
        if buffer:
            optimized.append(self._merge_segment(buffer))
            
        return optimized

    def _merge_segment(self, items: List[Dict]) -> Dict:
        merged = {
            'start': items[0]['start'],
            'end': items[-1]['end'],
            'text': '\n'.join([i['text'] for i in items]),
            'confidence': np.mean([i['confidence'] for i in items]),
            'speaker': items[0]['speaker']
        }
        return merged

    def _generate_srt(self, segments: List[Dict], output_path: str):
        srt_content = []
        for idx, seg in enumerate(segments, 1):
            start = self._format_time(seg['start'])
            end = self._format_time(seg['end'])
            speaker = f"[{seg['speaker']}] " if self.config['speaker_diarization'] else ""
            srt_content.append(f"{idx}\n{start} --> {end}\n{speaker}{seg['text']}\n")
            
        Path(output_path).write_text('\n'.join(srt_content))

    def _format_time(self, seconds: float) -> str:
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{seconds:06.3f}".replace('.', ',')

    def process_file(self, video_path: str):
        try:
            logging.info(f"Processing {video_path}")
            audio_path = f"temp_{datetime.now().timestamp()}.wav"
            
            self._enhance_audio(video_path, audio_path)
            segments = self._transcribe_audio(audio_path)
            optimized = self._optimize_segmentation(segments)
            
            output_path = Path(self.config['output_dir']) / f"{Path(video_path).stem}.srt"
            self._generate_srt(optimized, str(output_path))
            
            if not self.config['debug']:
                os.remove(audio_path)
                
            logging.info(f"Generated subtitles: {output_path}")
            
        except Exception as e:
            logging.error(f"Failed to process {video_path}: {str(e)}")
            raise

def main():
    parser = argparse.ArgumentParser(description="Advanced Video to SRT Generator")
    parser.add_argument('inputs', nargs='+', help="Input video files or directories")
    parser.add_argument('-m', '--model', required=True, help="Vosk model directory")
    parser.add_argument('-o', '--output-dir', default='output', help="Output directory")
    parser.add_argument('--max-duration', type=float, default=8.0, help="Max subtitle duration")
    parser.add_argument('--max-chars', type=int, default=45, help="Max characters per line")
    parser.add_argument('--max-lines', type=int, default=2, help="Max lines per subtitle")
    parser.add_argument('--punctuation', action='store_true', help="Enable punctuation restoration")
    parser.add_argument('--speakers', action='store_true', help="Enable speaker diarization")
    parser.add_argument('--debug', action='store_true', help="Enable debug mode")
    args = parser.parse_args()

    config = {
        'video_paths': [],
        'output_dir': args.output_dir,
        'model_path': args.model,
        'max_duration': args.max_duration,
        'max_chars': args.max_chars,
        'max_lines': args.max_lines,
        'punctuation': args.punctuation,
        'speaker_diarization': args.speakers,
        'debug': args.debug
    }

    for input_path in args.inputs:
        if os.path.isdir(input_path):
            for root, _, files in os.walk(input_path):
                for file in files:
                    if file.lower().endswith(('.mp4', '.mkv', '.avi', '.mov')):
                        config['video_paths'].append(os.path.join(root, file))
        else:
            config['video_paths'].append(input_path)

    Path(config['output_dir']).mkdir(exist_ok=True)
    generator = AdvancedSubtitleGenerator(config)
    
    for video_path in config['video_paths']:
        generator.process_file(video_path)

if __name__ == '__main__':
    main()
