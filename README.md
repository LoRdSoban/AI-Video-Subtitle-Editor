# AI Video Subtitle Editor

This project is an AI-powered video subtitle editor that uses OpenAI's Whisper model to transcribe and translate audio from video files, generate subtitles, and allow users to edit and preview the subtitles before downloading the final subtitled video.

## Features

- Extract audio from video files
- Transcribe and translate audio using Whisper model
- Generate SRT subtitle files
- Edit subtitles within the web interface
- Add subtitles to video using FFmpeg
- Download the final subtitled video

## Requirements

- Python 3.7+
- moviepy==2.0.0.dev2
- imageio==2.25.1
- ffmpeg-python
- streamlit
- whisper
- pysrt

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/AI-Video-Subtitle-Editor.git
    cd AI-Video-Subtitle-Editor
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Ensure FFmpeg is installed on your system. You can download it from [FFmpeg.org](https://ffmpeg.org/download.html).

4. Install ImageMagick:
    ```sh
    sudo apt install imagemagick
    ```

## Usage

1. Run the Streamlit app:
    ```sh
    streamlit run app.py
    ```

2. Open your web browser and go to `http://localhost:8501`.

3. Upload a video file, and the app will guide you through extracting audio, transcribing, generating subtitles, editing, and previewing the final subtitled video.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [OpenAI Whisper](https://github.com/openai/whisper)
- [Streamlit](https://streamlit.io/)
- [MoviePy](https://zulko.github.io/moviepy/)
- [FFmpeg](https://ffmpeg.org/)
- [pysrt](https://github.com/byroot/pysrt)
