import streamlit as st
import tempfile
import whisper
import ffmpeg
import pysrt
from moviepy.editor import VideoFileClip

@st.cache_resource
def load_whisper_model():
    model = whisper.load_model("small")
    return model

def extract_audio(video_path, audio_path):
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path, codec='pcm_s16le')

def transcribe_audio(audio_path):
    model = load_whisper_model()
    result = model.transcribe(audio_path, task="translate")
    return result["text"], result["segments"]

def generate_srt(segments, srt_path):
    subs = pysrt.SubRipFile()
    for i, seg in enumerate(segments):
        subs.append(pysrt.SubRipItem(
            index=i+1,
            start=pysrt.SubRipTime(seconds=seg["start"]),
            end=pysrt.SubRipTime(seconds=seg["end"]),
            text=seg["text"]
        ))
    subs.save(srt_path)

def add_subtitles_with_ffmpeg(video_path, srt_path, output_video_path):
    (
        ffmpeg
        .input(video_path)
        .output(
            output_video_path,
            vf=f"subtitles={srt_path}",
            acodec="copy"
        )
        .global_args('-loglevel', 'error')
        .run(cmd="ffmpeg")
    )

def main():
    st.title("AI Video Subtitle Editor")
    uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])

    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
            temp_video.write(uploaded_file.read())
            video_path = temp_video.name

        audio_path = video_path.replace(".mp4", ".wav")
        srt_path = video_path.replace(".mp4", ".srt")
        output_video_path = video_path.replace(".mp4", "_subtitled.mp4")

        st.write("Extracting audio...")
        extract_audio(video_path, audio_path)
        
        st.write("Transcribing...")
        text, segments = transcribe_audio(audio_path)
        
        st.write("Generating SRT...")
        generate_srt(segments, srt_path)

        with open(srt_path, "r", encoding="utf-8") as f:
            srt_content = f.read()

        edited_srt_content = st.text_area("Edit Subtitles", srt_content, height=300)

        if st.button("Save and Preview"):
            with open(srt_path, "w", encoding="utf-8") as f:
                f.write(edited_srt_content)

            try:
                add_subtitles_with_ffmpeg(video_path, srt_path, output_video_path)
                st.video(output_video_path)
                with open(output_video_path, "rb") as f:
                    st.download_button("Download", f, "subtitled.mp4")
            except Exception as e:
                st.error(f"Error processing video: {str(e)}")

if __name__ == "__main__":
    main()