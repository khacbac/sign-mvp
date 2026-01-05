import streamlit as st
import sys
from pathlib import Path
import time

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from pipeline.process_audio import process_audio_to_avatar
from avatar_engines.stick.renderer import render_avatar_streamlit
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Sign Language Translator",
    page_icon="🤟",
    layout="wide"
)

# Title
st.title("🤟 Sign Language Translation System")
st.markdown("Transform speech into American Sign Language (ASL) gestures")

# Avatar engine selection
st.sidebar.header("Avatar Settings")
avatar_engine = st.sidebar.selectbox(
    "Choose Avatar Engine:",
    options=["stick", "skeleton", "human_video"],
    format_func=lambda x: x.replace("_", " ").title(),
    help="Select the avatar rendering engine"
)

# Store in session state
st.session_state.avatar_engine = avatar_engine

# Show coming soon messages for unimplemented engines
def get_engine_alert_message(engine):
    """Get the alert message for unimplemented engines"""
    if engine == "skeleton":
        return {
            "title": "🚧 Skeleton Avatar Coming Soon!",
            "message": "The 3D skeleton avatar is currently under development. Stay tuned for realistic bone-based animations with advanced kinematics!"
        }
    elif engine == "human_video":
        return {
            "title": "🚧 Human Video Avatar Coming Soon!",
            "message": "Photorealistic human video synthesis is in development. This will feature lifelike sign language rendering with natural expressions!"
        }
    return None

def is_engine_available(engine):
    """Check if an engine is available/implemented"""
    return engine == "stick"

if avatar_engine == "skeleton":
    st.sidebar.info("🚧 Skeleton avatar is coming soon! Currently using stick figure.")
elif avatar_engine == "human_video":
    st.sidebar.info("🚧 Human video avatar is coming soon! Currently using stick figure.")

# Input method selection
input_method = st.radio(
    "Choose your input method:",
    ("Local Audio Test", "Upload Audio File", "Microphone Input")
)

def show_results_dialog(transcription, gloss_sequence, all_keypoints, valid_glosses):
    """Show results in ultra-compact dialog popup"""
    @st.dialog("🤟", width="small")
    def results_modal():
        # Animation only - super compact
        animation_placeholder = st.empty()

        # Get the selected avatar engine
        engine = st.session_state.get('avatar_engine', 'stick')

        # Handle different engines
        if engine == 'stick':
            # Run animation in the dialog
            frames_per_gloss = len(all_keypoints) // len(valid_glosses) if valid_glosses else 0

            for i, pose in enumerate(all_keypoints):
                # Determine which gloss to show
                gloss_idx = min(i // frames_per_gloss, len(valid_glosses) - 1) if frames_per_gloss > 0 else 0
                current_gloss = valid_glosses[gloss_idx] if valid_glosses else ""

                render_avatar_streamlit(animation_placeholder, pose, text=current_gloss)
                time.sleep(0.03)

        elif engine == 'skeleton':
            animation_placeholder.markdown("""
            <div style='text-align: center; padding: 20px;'>
                <h3>🚧 Coming Soon!</h3>
                <p>3D skeleton avatar is under development.</p>
                <p>Currently showing stick figure preview:</p>
            </div>
            """, unsafe_allow_html=True)
            # For now, show stick figure as preview
            frames_per_gloss = len(all_keypoints) // len(valid_glosses) if valid_glosses else 0
            for i, pose in enumerate(all_keypoints[:30]):  # Show fewer frames for preview
                gloss_idx = min(i // frames_per_gloss, len(valid_glosses) - 1) if frames_per_gloss > 0 else 0
                current_gloss = valid_glosses[gloss_idx] if valid_glosses else ""
                render_avatar_streamlit(animation_placeholder, pose, text=current_gloss)
                time.sleep(0.05)

        elif engine == 'human_video':
            animation_placeholder.markdown("""
            <div style='text-align: center; padding: 20px;'>
                <h3>🚧 Coming Soon!</h3>
                <p>Human video avatar is under development.</p>
                <p>This will feature photorealistic sign language rendering.</p>
                <br>
                <p><em>Preview mode - stick figure:</em></p>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(2)
            # For now, show stick figure as preview
            frames_per_gloss = len(all_keypoints) // len(valid_glosses) if valid_glosses else 0
            for i, pose in enumerate(all_keypoints[:30]):  # Show fewer frames for preview
                gloss_idx = min(i // frames_per_gloss, len(valid_glosses) - 1) if frames_per_gloss > 0 else 0
                current_gloss = valid_glosses[gloss_idx] if valid_glosses else ""
                render_avatar_streamlit(animation_placeholder, pose, text=current_gloss)
                time.sleep(0.05)

    results_modal()

# Option 1: Local Audio Buttons
if input_method == "Local Audio Test":
    st.subheader("Quick Test - Play Local Audio Files")
    
    # Get list of audio files
    input_dir = Path("input")
    if not input_dir.exists():
        st.error("Input directory not found! Please create an 'input/' directory with audio files.")
    else:
        audio_files = list(input_dir.glob("*.wav")) + list(input_dir.glob("*.mp3"))
        
        if not audio_files:
            st.warning("No audio files found in input/ directory. Add some .wav or .mp3 files!")
        else:
            # Display each audio file with a translate button
            for i, audio_file in enumerate(audio_files):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.audio(str(audio_file))
                    st.caption(f"File: {audio_file.name}")
                
                with col2:
                    # Create a translate button for each audio file
                    engine_available = is_engine_available(st.session_state.avatar_engine)
                    button_help = "Select Stick Figure engine to enable translation" if not engine_available else "Translate this audio to sign language"

                    if st.button("Translate", key=f"btn_local_{i}", disabled=not engine_available, help=button_help):
                        with st.spinner(f"Processing {audio_file.name}..."):
                            try:
                                # Process the audio
                                transcription, gloss_sequence, all_keypoints, valid_glosses = process_audio_to_avatar(str(audio_file))

                                # Show results in popup
                                st.success("✅ Translation complete!")
                                show_results_dialog(transcription, gloss_sequence, all_keypoints, valid_glosses)

                            except Exception as e:
                                st.error(f"Error processing audio: {str(e)}")

# Option 2: Upload Audio
elif input_method == "Upload Audio File":
    st.subheader("Upload Your Audio File")
    
    uploaded_file = st.file_uploader(
        "Choose an audio file",
        type=['wav', 'mp3', 'm4a', 'ogg', 'flac'],
        help="Supported formats: WAV, MP3, M4A, OGG, FLAC"
    )
    
    if uploaded_file is not None:
        # Show audio player
        st.audio(uploaded_file)

        # Check if selected engine is available
        engine_available = is_engine_available(st.session_state.avatar_engine)
        if not engine_available:
            st.warning("🚧 Please select 'Stick Figure' engine in the sidebar to enable translation")
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
                    transcription, gloss_sequence, all_keypoints, valid_glosses = process_audio_to_avatar(str(temp_path))

                    # Show results in popup
                    st.success("✅ Translation complete!")
                    show_results_dialog(transcription, gloss_sequence, all_keypoints, valid_glosses)

                except Exception as e:
                    st.error(f"Error processing audio: {str(e)}")
                finally:
                    # Clean up temp file
                    if 'temp_path' in locals() and temp_path.exists():
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
            show_visualizer=True
        )
        
        if audio_bytes:
            # Convert AudioSegment to bytes
            audio_bytes_data = audio_bytes.export(format="wav").read()

            # Show audio player
            st.audio(audio_bytes_data)

            # Check if selected engine is available
            engine_available = is_engine_available(st.session_state.avatar_engine)
            if not engine_available:
                st.warning("🚧 Please select 'Stick Figure' engine in the sidebar to enable translation")
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
                        transcription, gloss_sequence, all_keypoints, valid_glosses = process_audio_to_avatar(str(temp_path))

                        # Show results in popup
                        st.success("✅ Translation complete!")
                        show_results_dialog(transcription, gloss_sequence, all_keypoints, valid_glosses)

                    except Exception as e:
                        st.error(f"Error processing audio: {str(e)}")
                    finally:
                        # Clean up temp file
                        if temp_path.exists():
                            temp_path.unlink()
    
    except ImportError:
        st.error("""
        ⚠️ **Missing Dependency: streamlit-audiorecorder**
        
        To use microphone input, please install the required package:
        
        ```bash
        pip install streamlit-audiorecorder
        ```
        
        Or add `streamlit-audiorecorder` to your environment.yml and update your environment.
        """)

# Add empty space at bottom
st.markdown("<br><br>", unsafe_allow_html=True)

# Footer
st.divider()
st.markdown("<div style='text-align: center; color: #666;'><p>🤟 Sign Language Translation System | ML4Sign Project</p><p>Powered by OpenAI Whisper and custom ASL gesture mapping</p></div>", unsafe_allow_html=True)
