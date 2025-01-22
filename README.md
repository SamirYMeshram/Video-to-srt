# Video-to-srt
A Python tool for automatically generating subtitles (SRT format) from video files using speech recognition (Vosk). It includes features like audio enhancement (FFmpeg), punctuation restoration (Transformers), and subtitle segmentation optimization for better readability.


---

# **Advanced Video to SRT Subtitle Generator**

This Python-based tool enables automatic subtitle generation from video files in the **SRT** (SubRip Subtitle) format. It combines **Vosk** for accurate speech-to-text transcription, **FFmpeg** for high-quality audio enhancement, and **Hugging Face's Transformers** for punctuation restoration. The tool optimizes subtitle segments to fit readability criteria like duration, character count, and line count. 

Whether you're generating subtitles for personal use or adding captions to videos for accessibility, this tool is designed for high-quality, customizable subtitle creation.

---

## **Key Features**
- **Speech Recognition**: Converts audio from video files into accurate text using the **Vosk** ASR (Automatic Speech Recognition) system.
- **Audio Enhancement**: Improves audio quality by applying noise reduction, normalization, and compression filters using **FFmpeg**.
- **Punctuation Restoration**: Enhances raw transcriptions by automatically restoring punctuation using the **Hugging Face** **Transformers** pipeline.
- **Subtitle Segmentation**: Automatically segments subtitles based on maximum duration, character count, and line count.
- **Debug Mode**: Provides detailed logging for easy troubleshooting and debugging.
- **Speaker Diarization**: Placeholder for future support to identify different speakers (currently not implemented).
- **Cross-platform Support**: Works on Windows, Linux, and macOS.

---

## **Table of Contents**
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Install Dependencies](#install-dependencies)
  - [Download Vosk Model](#download-vosk-model)
- [Usage](#usage)
  - [CLI Usage](#cli-usage)
  - [Configuration Options](#configuration-options)
  - [Example Usage](#example-usage)
- [How It Works](#how-it-works)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## **Installation**

### **Prerequisites**
Before running the tool, make sure you have the following installed:

1. **Python 3.7+**  
   You can download Python from [here](https://www.python.org/downloads/).

2. **FFmpeg**  
   FFmpeg is required for audio extraction and enhancement. Install FFmpeg according to your operating system:

   - **Windows**: Download from [FFmpeg.org](https://ffmpeg.org/download.html).
   - **macOS**: Install via Homebrew:
     ```bash
     brew install ffmpeg
     ```
   - **Linux**: Install using your package manager (e.g., `apt` for Ubuntu):
     ```bash
     sudo apt-get install ffmpeg
     ```

3. **Vosk Model**  
   You need to download a pre-trained ASR model from Vosk to perform speech-to-text. The smallest and fastest model for English is `vosk-model-small-en-us-0.15`, but there are other models for multiple languages available.

   - Download Vosk models from [here](https://alphacephei.com/vosk/models).

   **Note**: Download and extract the model to a directory on your system. You'll need to specify the model's path in the next steps.

---

### **Install Dependencies**
After ensuring Python 3.7+ and FFmpeg are installed, clone this repository and install the required Python dependencies.

1. Clone the repository:
   ```bash
   git clone https://github.com/SamirYMeshram/advanced-video-to-srt-generator.git
   cd advanced-video-to-srt-generator
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use 'venv\Scripts\activate'
   ```

3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Install **FFmpeg** if you haven't already. Refer to the instructions above to install it.

---

### **Download Vosk Model**
1. Visit the [Vosk Model page](https://alphacephei.com/vosk/models) and download the desired language model (e.g., `vosk-model-small-en-us-0.15`).
2. Extract the model to a folder, e.g., `/path/to/vosk-model`.
3. Make a note of the path, as you'll need to reference it in the next steps.

---

## **Usage**

### **CLI Usage**
The tool can be run from the command line to process video files or directories containing video files. Here’s how to run it:

```bash
python generate_subtitles.py --model /path/to/vosk/model --output-dir /path/to/output [video_files_or_directories]
```

#### **Configuration Options**
- **`--model`**: (Required) Path to the Vosk ASR model directory (e.g., `/path/to/vosk-model`).
- **`--output-dir`**: (Optional) Directory where the generated subtitle (SRT) files will be saved. Default is `output`.
- **`--max-duration`**: (Optional) Maximum duration (in seconds) of each subtitle segment. Default is `8.0`.
- **`--max-chars`**: (Optional) Maximum number of characters per subtitle line. Default is `45`.
- **`--max-lines`**: (Optional) Maximum number of lines per subtitle segment. Default is `2`.
- **`--punctuation`**: (Optional) If specified, restores punctuation in transcriptions using a Hugging Face punctuation model.
- **`--speakers`**: (Optional) Enable speaker diarization (currently a placeholder).
- **`--debug`**: (Optional) Enables detailed logging for debugging purposes.

#### **Example Usage**
```bash
python generate_subtitles.py --model /path/to/vosk/model --output-dir ./subtitles --punctuation --max-duration 10.0 --debug video1.mp4 video2.mkv
```
This command will:
- Process `video1.mp4` and `video2.mkv`.
- Restore punctuation in transcriptions.
- Ensure each subtitle segment is no longer than 10 seconds.
- Save subtitles to the `./subtitles` directory.

---

## **How It Works**

### **Step-by-Step Process**:

1. **Audio Extraction and Enhancement**:
   The tool uses **FFmpeg** to extract the audio from the video. It then applies filters like:
   - **Noise Reduction**: Removes background noise.
   - **Volume Normalization**: Adjusts audio levels to be consistent.
   - **Compression**: Adjusts dynamic range for better clarity.

2. **Speech-to-Text Transcription**:
   The extracted audio is processed by **Vosk** ASR to convert speech to text. The model segments the audio and produces a raw transcript.

3. **Punctuation Restoration**:
   If enabled, the raw transcription (without punctuation) is processed using **Hugging Face Transformers** to add proper punctuation (e.g., periods, commas, question marks).

4. **Subtitle Optimization**:
   Transcribed text is divided into subtitle segments, ensuring that each subtitle meets:
   - Maximum duration (`max_duration`).
   - Maximum characters per line (`max_chars`).
   - Maximum lines per subtitle (`max_lines`).

5. **SRT Generation**:
   Finally, the subtitle segments are written into an **SRT** file with accurate timestamps and properly formatted text.

---

## **Customization**

You can modify the behavior of the tool by changing the following configurations in the script or by passing different command-line arguments:
- **Punctuation Model**: You can replace the `oliverguhr/fullstop-punctuation-multilang-large` model with any custom punctuation model from Hugging Face.
- **Audio Filters**: Modify the audio enhancement filters in the `_enhance_audio` method to change how the audio is processed (e.g., applying different noise reduction techniques).

---

## **Troubleshooting**

### Common Issues:

1. **FFmpeg Not Found**:
   - Ensure that **FFmpeg** is installed and added to your system’s PATH.
   - Run `ffmpeg -version` in the terminal to confirm it’s properly installed.

2. **Model Not Found**:
   - Ensure that the path to the **Vosk ASR model** is correct.
   - Download the model from [Vosk Models](https://alphacephei.com/vosk/models).

3. **Audio Quality Issues**:
   - If the transcription is unclear or inaccurate, try using a higher-quality audio source or adjusting the **FFmpeg** filters for better noise reduction.

4. **Punctuation Issues**:
   - If punctuation restoration is not performing as expected, consider using a different Hugging Face model or adjusting parameters such as `num_beams`.

---

## **Contributing**

Contributions are welcome! If you have suggestions or improvements, feel free to:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

---

## **License**

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## **Author**

**Samir Y. Meshram**  
GitHub: [SamirYMeshram](https://github.com/SamirYMeshram)  
Email: [sameerYmeshram@gmail.com](mailto:sameerYmeshram@gmail.com)

---
