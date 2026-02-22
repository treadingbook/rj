import streamlit as st
import yt_dlp
import os

# পেজ সেটআপ
st.set_page_config(page_title="Cyber Video Downloader", page_icon="📟", layout="wide")

# হ্যাকার টাইপ স্টাইল (CSS) - শুধুমাত্র স্টাইল পরিবর্তন করা হয়েছে
st.markdown("""
    <style>
    /* ডার্ক এবং হ্যাকার ব্যাকগ্রাউন্ড */
    .stApp {
        background-color: #000000;
        background-image: linear-gradient(rgba(0, 255, 65, 0.05) 1px, transparent 1px), 
                          linear-gradient(90deg, rgba(0, 255, 65, 0.05) 1px, transparent 1px);
        background-size: 30px 30px;
        color: #00FF41 !important;
        font-family: 'Courier New', Courier, monospace;
    }

    /* মেইন কন্টেইনার বক্স */
    .main-box {
        background-color: rgba(0, 0, 0, 0.85);
        padding: 35px;
        border-radius: 10px;
        border: 1px solid #00FF41;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.4);
        backdrop-filter: blur(5px);
    }

    /* টাইটেল এবং সব টেক্সট কালার গ্রিন */
    h1, h2, h3, p, label, .stMarkdown {
        color: #00FF41 !important;
        text-shadow: 0 0 5px #00FF41;
    }

    /* ইনপুট বক্স স্টাইল */
    .stTextInput>div>div>input {
        background-color: #050505 !important;
        color: #00FF41 !important;
        border: 1px solid #00FF41 !important;
        font-family: 'Courier New', monospace;
    }

    /* রেডিও বাটন */
    .stRadio>div {
        color: #00FF41 !important;
    }

    /* হ্যাকার টাইপ বাটন */
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3.5em;
        background: transparent !important;
        color: #00FF41 !important;
        font-weight: bold;
        border: 1px solid #00FF41 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: #00FF41 !important;
        color: black !important;
        box-shadow: 0 0 20px #00FF41;
        cursor: crosshair;
    }

    /* ফুটার সেকশন */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(0, 0, 0, 0.9);
        color: #00FF41;
        text-align: center;
        padding: 8px;
        border-top: 1px solid #00FF41;
        font-size: 14px;
    }

    /* টেক্সট এরিয়া ও এক্সপ্যান্ডার */
    .stTextArea textarea, .streamlit-expanderHeader {
        background-color: #000 !important;
        color: #00FF41 !important;
        border: 1px solid #00FF41 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-box">', unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>📟 CYBER VIDEO TERMINAL</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>[ ACCESSING SECURE DATA EXTRACTION PROTOCOL ]</p>", unsafe_allow_html=True)
st.markdown("---")

url = st.text_input("> ENTER VIDEO SOURCE URL:", placeholder="Paste link here...")

if url:
    try:
        with st.spinner('📡 EXTRACTING METADATA... PLEASE WAIT...'):
            ydl_opts_info = {'format': 'best'}
            with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
                info = ydl.extract_info(url, download=False)
                video_url = info.get('url') 
                video_title = info.get('title')
                video_description = info.get('description')
                uploader = info.get('uploader')
                view_count = info.get('view_count')

            st.subheader(f"🎬 TARGET: {video_title}")
            st.video(video_url)
            
            with st.expander("📝 VIEW RAW METADATA"):
                st.write(f"**UPLOADER:** {uploader}")
                st.write(f"**VIEWS:** {view_count}")
                st.markdown("---")
                st.text(video_description) 

            st.success("SUCCESS: DATA PACKETS READY FOR DOWNLOAD.")
    except Exception as e:
        st.error("ERROR: SYSTEM COULD NOT RETRIEVE DATA.")

st.markdown("---")
format_choice = st.radio("> SELECT EXPORT FORMAT:", ("ভিডিও (MP4)", "অডিও (MP3)"), horizontal=True)

if st.button("EXECUTE DOWNLOAD"):
    if url:
        try:
            with st.spinner('⚡ DOWNLOADING...'):
                if format_choice == "অডিও (MP3)":
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                        'outtmpl': 'downloaded_audio.%(ext)s',
                    }
                else:
                    ydl_opts = {
                        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                        'outtmpl': 'downloaded_video.mp4',
                        'merge_output_format': 'mp4',
                    }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_data = ydl.extract_info(url, download=True)
                    actual_filename = ydl.prepare_filename(info_data)
                    
                    if format_choice == "অডিও (MP3)":
                        actual_filename = actual_filename.replace('.webm', '.mp3').replace('.m4a', '.mp3')

                with open(actual_filename, "rb") as file:
                    st.download_button(
                        label=f"💾 SAVE {format_choice} TO DISK",
                        data=file,
                        file_name=os.path.basename(actual_filename),
                        mime="video/mp4" if "video" in actual_filename else "audio/mp3"
                    )
                st.balloons()
        except Exception as e:
            st.error(f"FATAL ERROR: {e}")
st.markdown('</div>', unsafe_allow_html=True)

# --- ক্রেডিট সেকশন ---
st.markdown("""
    <div class="footer">
        <p>Developed with 🖥️ by <a href="https://www.facebook.com/md.rashed.miah.977782" style="color: #00FF41; text-decoration: none; font-weight: bold;">MD RASHED MIAH</a> | SYSTEM_VERSION_1.0</p>
    </div>
    """, unsafe_allow_html=True)
