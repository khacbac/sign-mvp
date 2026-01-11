import streamlit as st
import sys
from pathlib import Path
import time

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from pipeline.process_audio import process_audio_to_avatar, process_text_to_avatar
from avatar_engines.stick.renderer import render_avatar_streamlit
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(page_title="Sign Language Translator", page_icon="🤟", layout="wide")

# Title
st.title("🤟 Sign Language Translation System")
st.markdown("Transform speech into American Sign Language (ASL) gestures")

# Avatar engine selection
st.sidebar.header("Avatar Settings")
avatar_engine = st.sidebar.selectbox(
    "Choose Avatar Engine:",
    options=["stick", "skeleton", "human_video"],
    format_func=lambda x: x.replace("_", " ").title(),
    help="Select the avatar rendering engine",
)

# Store in session state
st.session_state.avatar_engine = avatar_engine


# Show engine-specific messages
def get_engine_description(engine):
    """Get description for the selected engine"""
    if engine == "stick":
        return {
            "title": "✅ Stick Figure Avatar",
            "message": "2D stick figure animation with smooth interpolation and gesture labels.",
        }
    elif engine == "skeleton":
        return {
            "title": "✅ Skeleton Avatar (FastAPI)",
            "message": "3D skeleton pose files generated via text-to-skeleton service. Requires FastAPI server on localhost:8000. Pose files saved to text-to-skeleton/output/poses/sample.pose",
        }
    elif engine == "human_video":
        return {
            "title": "🎬 Human Video Avatar (NEW!)",
            "message": "Real sign language videos from WLASL dataset. Videos are downloaded and composited on-demand.",
        }
    return None


def is_engine_available(engine):
    """Check if an engine is available/implemented"""
    return engine in ["stick", "human_video", "skeleton"]


# Show engine description
desc = get_engine_description(avatar_engine)
if desc:
    st.sidebar.info(f"**{desc['title']}**\n\n{desc['message']}")

# Input method selection
input_method = st.radio(
    "Choose your input method:",
    ("Local Audio Test", "Upload Audio File", "Microphone Input", "Type Text"),
)


def show_results_dialog(
    transcription, gloss_sequence, valid_glosses, all_keypoints=None, video_path=None
):
    """Show results in an expander (compatible alternative to dialog)"""
    # Get the selected avatar engine
    engine = st.session_state.get("avatar_engine", "stick")

    # Use expander as a compatible alternative to dialog
    with st.expander("🤟 Translation Results", expanded=True):
        if engine == "human_video" and video_path:
            # Show video player for human_video engine
            st.video(str(video_path))
            st.caption(f"Translation: {' '.join(valid_glosses)}")

            # Show download button
            with open(video_path, "rb") as f:
                st.download_button(
                    label="Download Video",
                    data=f,
                    file_name=f"{'_'.join(valid_glosses)}.mp4",
                    mime="video/mp4",
                )

        elif engine == "stick":
            # Show stick figure animation
            animation_placeholder = st.empty()

            # Run animation
            if all_keypoints and valid_glosses:
                frames_per_gloss = (
                    len(all_keypoints) // len(valid_glosses) if valid_glosses else 0
                )

                for i, pose in enumerate(all_keypoints):
                    # Determine which gloss to show
                    gloss_idx = (
                        min(i // frames_per_gloss, len(valid_glosses) - 1)
                        if frames_per_gloss > 0
                        else 0
                    )
                    current_gloss = valid_glosses[gloss_idx] if valid_glosses else ""

                    render_avatar_streamlit(
                        animation_placeholder, pose, text=current_gloss
                    )
                    time.sleep(0.03)
            else:
                st.info("No animation data available")

        elif engine == "skeleton":
            # Show success message for skeleton mode
            st.success("✅ Skeleton pose file generated successfully!")
            st.write(f"**Detected glosses (spaCy):** {', '.join(valid_glosses)}")
            st.info(
                "📁 **File location:** `text-to-skeleton/output/poses/safe_filename(transcription).pose`"
            )

            # Show helpful note
            with st.expander("ℹ️ How to access the pose file"):
                st.markdown(
                    """
                The `.pose` file has been generated at:
                ```
                text-to-skeleton/output/poses/safe_filename(transcription).pose
                ```

                You can use this file with pose visualization tools or scripts in the `text-to-skeleton/` directory.
                """
                )

        else:  # Other engines
            st.info("🚧 This avatar engine is not yet implemented.")
            st.write(f"Detected glosses: {', '.join(valid_glosses)}")


# Option 1: Local Audio Buttons
if input_method == "Local Audio Test":
    st.subheader("Quick Test - Play Local Audio Files")

    # Get list of audio files
    input_dir = Path("input")
    if not input_dir.exists():
        st.error(
            "Input directory not found! Please create an 'input/' directory with audio files."
        )
    else:
        audio_files = list(input_dir.glob("*.wav")) + list(input_dir.glob("*.mp3"))

        if not audio_files:
            st.warning(
                "No audio files found in input/ directory. Add some .wav or .mp3 files!"
            )
        else:
            # Display each audio file with a translate button
            for i, audio_file in enumerate(audio_files):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.audio(str(audio_file))
                    st.caption(f"File: {audio_file.name}")

                with col2:
                    # Create a translate button for each audio file
                    engine_available = is_engine_available(
                        st.session_state.avatar_engine
                    )
                    button_help = (
                        "Select Stick Figure engine to enable translation"
                        if not engine_available
                        else "Translate this audio to sign language"
                    )

                    if st.button(
                        "Translate",
                        key=f"btn_local_{i}",
                        disabled=not engine_available,
                        help=button_help,
                    ):
                        with st.spinner(f"Processing {audio_file.name}..."):
                            try:
                                # Get the selected engine
                                engine = st.session_state.get("avatar_engine", "stick")

                                # Process the audio
                                result = process_audio_to_avatar(
                                    str(audio_file), engine=engine
                                )
                                (
                                    transcription,
                                    gloss_sequence,
                                    result_data,
                                    valid_glosses,
                                ) = result

                                # Show results in popup
                                st.success("✅ Translation complete!")
                                if engine == "human_video":
                                    show_results_dialog(
                                        transcription,
                                        gloss_sequence,
                                        valid_glosses,
                                        video_path=result_data,
                                    )
                                elif engine == "skeleton":
                                    # For skeleton, result_data is None, but we still show the success message
                                    show_results_dialog(
                                        transcription, gloss_sequence, valid_glosses
                                    )
                                else:
                                    show_results_dialog(
                                        transcription,
                                        gloss_sequence,
                                        valid_glosses,
                                        all_keypoints=result_data,
                                    )

                            except Exception as e:
                                st.error(f"Error processing audio: {str(e)}")

# Option 2: Upload Audio
elif input_method == "Upload Audio File":
    st.subheader("Upload Your Audio File")

    uploaded_file = st.file_uploader(
        "Choose an audio file",
        type=["wav", "mp3", "m4a", "ogg", "flac"],
        help="Supported formats: WAV, MP3, M4A, OGG, FLAC",
    )

    if uploaded_file is not None:
        # Show audio player
        st.audio(uploaded_file)

        # Check if selected engine is available
        engine_available = is_engine_available(st.session_state.avatar_engine)
        if not engine_available:
            st.warning(
                "🚧 Please select 'Stick Figure' engine in the sidebar to enable translation"
            )
        else:
            # Auto-process when file is uploaded
            with st.spinner("Processing uploaded audio..."):
                try:
                    # Save uploaded file temporarily
                    temp_dir = Path("temp")
                    temp_dir.mkdir(exist_ok=True)
                    temp_path = temp_dir / uploaded_file.name

                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    # Process the audio
                    engine = st.session_state.get("avatar_engine", "stick")
                    result = process_audio_to_avatar(str(temp_path), engine=engine)
                    transcription, gloss_sequence, result_data, valid_glosses = result

                    # Show results in popup
                    st.success("✅ Translation complete!")
                    if engine == "human_video":
                        show_results_dialog(
                            transcription,
                            gloss_sequence,
                            valid_glosses,
                            video_path=result_data,
                        )
                    elif engine == "skeleton":
                        # For skeleton, result_data is None, but we still show the success message
                        show_results_dialog(
                            transcription, gloss_sequence, valid_glosses
                        )
                    else:
                        show_results_dialog(
                            transcription,
                            gloss_sequence,
                            valid_glosses,
                            all_keypoints=result_data,
                        )

                except Exception as e:
                    st.error(f"Error processing audio: {str(e)}")
                finally:
                    # Clean up temp file
                    if "temp_path" in locals() and temp_path.exists():
                        temp_path.unlink()

# Option 3: Microphone Input
elif input_method == "Microphone Input":
    st.subheader("Record with Your Microphone")

    # Check if audiorecorder is available
    try:
        from audiorecorder import audiorecorder

        # Record audio
        audio_bytes = audiorecorder(
            start_prompt="🎤 Click to Start Recording",
            stop_prompt="⏹️ Stop Recording",
            show_visualizer=True,
        )

        if audio_bytes:
            # Convert AudioSegment to bytes
            audio_bytes_data = audio_bytes.export(format="wav").read()

            # Show audio player
            st.audio(audio_bytes_data)

            # Check if selected engine is available
            engine_available = is_engine_available(st.session_state.avatar_engine)
            if not engine_available:
                st.warning(
                    "🚧 Please select 'Stick Figure' engine in the sidebar to enable translation"
                )
            else:
                # Auto-process when recording is done
                with st.spinner("Processing your recording..."):
                    try:
                        # Save recorded audio (AudioSegment has export method)
                        temp_dir = Path("temp")
                        temp_dir.mkdir(exist_ok=True)
                        temp_path = temp_dir / "recording.wav"

                        audio_bytes.export(temp_path, format="wav")

                        # Process the audio
                        engine = st.session_state.get("avatar_engine", "stick")
                        result = process_audio_to_avatar(str(temp_path), engine=engine)
                        transcription, gloss_sequence, result_data, valid_glosses = (
                            result
                        )

                        # Show results in popup
                        st.success("✅ Translation complete!")
                        if engine == "human_video":
                            show_results_dialog(
                                transcription,
                                gloss_sequence,
                                valid_glosses,
                                video_path=result_data,
                            )
                        elif engine == "skeleton":
                            # For skeleton, result_data is None, but we still show the success message
                            show_results_dialog(
                                transcription, gloss_sequence, valid_glosses
                            )
                        else:
                            show_results_dialog(
                                transcription,
                                gloss_sequence,
                                valid_glosses,
                                all_keypoints=result_data,
                            )

                    except Exception as e:
                        st.error(f"Error processing audio: {str(e)}")
                    finally:
                        # Clean up temp file
                        if temp_path.exists():
                            temp_path.unlink()

    except ImportError:
        st.error(
            """
        ⚠️ **Missing Dependency: streamlit-audiorecorder**

        To use microphone input, please install the required package:

        ```bash
        pip install streamlit-audiorecorder
        ```

        Or add `streamlit-audiorecorder` to your environment.yml and update your environment.
        """
        )

# Option 4: Type Text
elif input_method == "Type Text":
    st.subheader("Type Your Text")

    # Text input area
    user_text = st.text_area(
        "Enter text to translate to sign language:",
        placeholder="Type your message here... (e.g., 'Hello, how are you?')",
        height=100,
        help="Enter any text and it will be converted to sign language",
    )

    if user_text:
        # Check if selected engine is available
        engine_available = is_engine_available(st.session_state.avatar_engine)
        if not engine_available:
            st.warning(
                "🚧 Please select 'Stick Figure' or 'Human Video' engine in the sidebar to enable translation"
            )
        else:
            # Show translate button
            if st.button("Translate to Sign Language", type="primary"):
                with st.spinner("Translating your text..."):
                    try:
                        # Process the text
                        engine = st.session_state.get("avatar_engine", "stick")
                        result = process_text_to_avatar(user_text, engine=engine)
                        text, gloss_sequence, result_data, valid_glosses = result

                        # Show results in popup
                        st.success("✅ Translation complete!")
                        if engine == "human_video":
                            show_results_dialog(
                                text,
                                gloss_sequence,
                                valid_glosses,
                                video_path=result_data,
                            )
                        elif engine == "skeleton":
                            # For skeleton, result_data is None, but we still show the success message
                            show_results_dialog(text, gloss_sequence, valid_glosses)
                        else:
                            show_results_dialog(
                                text,
                                gloss_sequence,
                                valid_glosses,
                                all_keypoints=result_data,
                            )

                    except Exception as e:
                        st.error(f"Error processing text: {str(e)}")

# Add empty space at bottom
st.markdown("<br><br>", unsafe_allow_html=True)

# Footer
st.divider()
st.markdown(
    "<div style='text-align: center; color: #666;'><p>🤟 Sign Language Translation System | ML4Sign Project</p><p>Powered by OpenAI Whisper and custom ASL gesture mapping</p></div>",
    unsafe_allow_html=True,
)
