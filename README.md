# Video-to-srt
A Python tool for automatically generating subtitles (SRT format) from video files using speech recognition (Vosk). It includes features like audio enhancement (FFmpeg), punctuation restoration (Transformers), and subtitle segmentation optimization for better readability.



---

# Advanced Video to SRT Subtitle Generator

This Python tool automates the process of generating subtitles (SRT format) from video files. It leverages **Vosk** for speech recognition, uses **FFmpeg** for audio enhancement, and integrates **Hugging Face's Transformers** for punctuation restoration. The tool optimizes subtitle segmentation based on duration, character limits, and line count, ensuring a smooth viewing experience.

### Features:
- **Speech Recognition**: Transcribes speech from video files using the Vosk ASR model.
- **Audio Enhancement**: Improves audio quality with noise reduction, normalization, and compression via FFmpeg.
- **Punctuation Restoration**: Restores punctuation to transcriptions using a pre-trained model from Hugging Face’s Transformers library.
- **Subtitle Optimization**: Automatically adjusts subtitle segments based on duration, character count, and line limits.
- **Debug Mode**: Enables verbose logging for troubleshooting.
- **Speaker Diarization**: Placeholder for future speaker recognition functionality.

---

## Installation

### Prerequisites:
1. **Python 3.x** (recommended version: 3.7+)
2. **FFmpeg** installed on your system.

   - [FFmpeg Installation Guide](https://ffmpeg.org/download.html)

### Install Dependencies:
Clone this repository and install the required Python packages using `pip`:

```bash
git clone https://github.com/SamirYMeshram/advanced-video-to-srt-generator.git
cd advanced-video-to-srt-generator
pip install -r requirements.txt
```

### Download Vosk Model:
Download the Vosk ASR model (you can use the `vosk-model-small-en-us-0.15` model or any other compatible model) and place it in your desired directory.

- [Vosk Models](https://alphacephei.com/vosk/models)

---

## Usage

### Command Line Interface (CLI)

The script can be executed from the command line to process video files or directories containing video files.

```bash
python generate_subtitles.py --model /path/to/vosk/model --output-dir /path/to/output [video_files_or_directories]
```

### Parameters:
- **`--model`**: Path to the Vosk ASR model directory (required).
- **`--output-dir`**: Directory to store generated SRT subtitle files (default: `output`).
- **`--max-duration`**: Maximum duration (in seconds) of each subtitle segment (default: `8.0`).
- **`--max-chars`**: Maximum number of characters per subtitle line (default: `45`).
- **`--max-lines`**: Maximum number of lines per subtitle segment (default: `2`).
- **`--punctuation`**: Enable punctuation restoration (default: disabled).
- **`--speakers`**: Enable speaker diarization (currently not implemented, placeholder).
- **`--debug`**: Enable debug logging for detailed error messages (default: disabled).

### Example:
```bash
python generate_subtitles.py --model /path/to/vosk/model --output-dir ./subtitles --punctuation --max-duration 10.0 --debug video1.mp4 video2.mkv
```

This command will:
1. Process `video1.mp4` and `video2.mkv`.
2. Restore punctuation in transcriptions.
3. Ensure each subtitle segment is no longer than 10 seconds.
4. Save subtitles to the `./subtitles` directory.

---

## How It Works

1. **Extract Audio**: The tool uses `FFmpeg` to extract and enhance the audio from the input video files. Filters like noise reduction, volume normalization, and compression are applied to improve the quality of the audio for better transcription accuracy.
   
2. **Speech Transcription**: The audio is transcribed using the **Vosk** ASR model. This model is capable of transcribing audio to text with high accuracy for multiple languages.

3. **Punctuation Restoration**: If enabled, the raw transcription (without punctuation) is processed through a punctuation restoration model provided by **Hugging Face's Transformers** library to enhance the readability of the output.

4. **Subtitle Optimization**: The transcribed text is divided into subtitle segments. Segments are optimized to ensure they fit within the character and line limits. The duration of each segment is also checked to ensure readability.

5. **SRT Generation**: Finally, the segments are written into a standard **SRT** subtitle file with accurate timestamps and formatted text.

---

## Configuration

You can adjust the behavior of the tool by modifying the configuration passed via command-line arguments or by editing the code in the `config` dictionary inside the script.

- **`max_duration`**: Controls the maximum duration for each subtitle segment (in seconds).
- **`max_chars`**: Defines the maximum number of characters per subtitle line.
- **`max_lines`**: Limits the maximum number of subtitle lines per segment.
- **`punctuation`**: Whether to restore punctuation to the transcriptions.
- **`speaker_diarization`**: Placeholder for enabling speaker identification in the future.
- **`debug`**: Enables detailed logging for debugging purposes.

---

## Troubleshooting

- **Missing FFmpeg**: Ensure FFmpeg is installed on your system and added to the system path.
- **Vosk Model Not Found**: Make sure the correct model path is specified and the model is downloaded and placed correctly.
- **Audio Quality**: If the transcription is unclear or inaccurate, check the audio enhancement filters or provide higher-quality audio sources.

---

## Author

**Samir Y. Meshram**  
GitHub: [SamirYMeshram](https://github.com/SamirYMeshram)  
Email: [sameerYmeshram@gmail.com](mailto:sameerYmeshram@gmail.com)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
