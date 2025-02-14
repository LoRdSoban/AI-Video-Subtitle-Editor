import streamlit as st
import whisper
import ffmpeg
import pysrt
from moviepy.editor import VideoFileClip
import tempfile

# Load the Whisper model
@st.cache_resource
def load_whisper_model(model_size):
    model = whisper.load_model(model_size)  # Use "small", "medium", "large" for better accuracy
    return model

def extract_audio(video_path, audio_path):
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path, codec='pcm_s16le')  # Use a lossless codec

def transcribe_audio(audio_path, model_size):
    model = load_whisper_model(model_size)
    result = model.transcribe(audio_path, task="translate")
    return result["text"], result["segments"]

def generate_srt(segments, srt_path):
    subs = pysrt.SubRipFile()
    for i, seg in enumerate(segments):
        start_time = seg["start"]
        end_time = seg["end"]
        subs.append(pysrt.SubRipItem(
            index=i + 1,
            start=pysrt.SubRipTime(seconds=start_time),
            end=pysrt.SubRipTime(seconds=end_time),
            text=seg["text"]
        ))
    subs.save(srt_path)

def time_to_seconds(time_obj):
    return time_obj.hours * 3600 + time_obj.minutes * 60 + time_obj.seconds + time_obj.milliseconds / 1000.0

def add_subtitles_with_ffmpeg(video_path, srt_path, output_video_path, font_size, color, position):
    position_filter = "subtitles={}:force_style='FontSize={},PrimaryColour=&H{}&'".format(
        srt_path, font_size, color.lstrip('#')  # Adding alpha channel
    )
    if position == "top":
        position_filter += ":force_style='Alignment=6'"  # Top alignment

    (
        ffmpeg
        .input(video_path)
        .output(
            output_video_path,
            vf=position_filter,
            acodec="copy"
        )
        .global_args('-loglevel', 'error')
        .run(cmd="ffmpeg")
    )

def main():
    st.set_page_config(page_title="AI Video Subtitle Editor", layout="wide")
    st.title("🎬 AI Video Subtitle Editor")
    
    
    st.markdown("### 📤 Upload Video")
    uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])

    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
            temp_video.write(uploaded_file.read())
            video_path = temp_video.name

        audio_path = video_path.replace(".mp4", ".wav")
        srt_path = video_path.replace(".mp4", ".srt")
        output_video_path = video_path.replace(".mp4", "_ffmpeg_subtitled.mp4")

        st.write("### Step 1: 🎧 Extracting audio...")
        extract_audio(video_path, audio_path)
        
        st.write("### Step 2: 📝 Transcribing audio...")
        text, segments = transcribe_audio(audio_path, model_size)
        
        st.write("### Step 3: 🗒️ Generating subtitles...")
        generate_srt(segments, srt_path)

        with open(srt_path, "r", encoding="utf-8") as f:
            srt_content = f.read()

        st.write("### Step 4: ✏️ Edit subtitles below:")
        edited_srt_content = st.text_area("SRT Content", srt_content, height=300)

        st.sidebar.title("⚙️ Settings")
    
        # This was causing the streamlit app to crash, because the community edition of streamlit could not support heavy models
        #model_size = st.sidebar.selectbox("Select Whisper model size", ["base", "small", "medium", "large"])
        st.sidebar.markdown("**Note:** Using 'base' Whisper model due to limitations of community cloud.")
        model_size = "base"
        
        subtitle_font_size = st.sidebar.slider("Subtitle Font Size", min_value=10, max_value=50, value=18)
        subtitle_color = st.sidebar.color_picker("Subtitle Color", "#FFFFFF")
        subtitle_position = st.sidebar.selectbox("Subtitle Position", ["bottom", "top"])
        
        if st.button("Save and Preview Subtitles"):
            with open(srt_path, "w", encoding="utf-8") as f:
                f.write(edited_srt_content)

            st.write("### Step 5: 🎥 Adding subtitles to video for preview...")
            add_subtitles_with_ffmpeg(
                video_path=video_path, 
                srt_path=srt_path, 
                output_video_path=output_video_path,
                font_size=subtitle_font_size,
                color=subtitle_color,
                position=subtitle_position
            )

            st.success("Preview ready! ✅")
            st.video(output_video_path)

            with open(output_video_path, "rb") as f:
                st.download_button("Download Subtitled Video", f, file_name="subtitled_video.mp4")

if __name__ == "__main__":
    main()
