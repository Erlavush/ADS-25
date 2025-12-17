import streamlit as st
import streamlit.components.v1 as components
import base64
import os

def waveform_player(audio_path, height=100, wave_color="#a1a1aa", progress_color="#6366f1", key=None):
    """
    Renders an interactive Waveform Player using Wavesurfer.js.
    """
    if not os.path.exists(audio_path):
        st.error(f"Audio file not found: {audio_path}")
        return

    # Read Audio and Encode to Base64
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()
        b64_audio = base64.b64encode(audio_bytes).decode()
    
    # Unique ID for the container
    # Using python hash of path + key to ensure uniqueness
    element_id = f"waveform_{hash(audio_path + str(key))}".replace("-", "_")

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://unpkg.com/wavesurfer.js@7/dist/wavesurfer.min.js"></script>
        <style>
            body {{
                background-color: #18181b; /* Zinc 900 - Matches Card Background */
                display: flex;
                flex-direction: row;
                align-items: center;
                margin: 0;
                padding: 0 10px;
                font-family: 'Figtree', sans-serif;
                color: #FAFAFA;
                overflow: hidden;
            }}
            #controls {{
                display: flex;
                align-items: center;
                margin-right: 15px;
            }}
            button {{
                background: none;
                border: none;
                cursor: pointer;
                color: #FAFAFA;
                font-size: 24px;
                transition: transform 0.1s;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            button:active {{
                transform: scale(0.9);
            }}
            #waveform {{
                flex-grow: 1;
                position: relative;
            }}
            /* Customizing the scrollbar if needed, but overflow hidden mostly */
        </style>
    </head>
    <body>
        <div id="controls">
            <button id="playBtn" onclick="togglePlay()">
                <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M8 5v14l11-7z" name="play"/>
                    <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z" name="pause" style="display:none"/>
                </svg>
            </button>
        </div>
        <div id="waveform"></div>

        <script>
            // Initialize Wavesurfer
            const wavesurfer = WaveSurfer.create({{
                container: '#waveform',
                waveColor: '{wave_color}',
                progressColor: '{progress_color}',
                cursorColor: '#FAFAFA',
                barWidth: 2,
                barRadius: 2,
                cursorWidth: 1,
                height: {height - 20}, // Adjust for padding
                barGap: 2,
                normalize: true,
                url: 'data:audio/mp3;base64,{b64_audio}'
            }});

            // Play/Pause Logic
            const btn = document.getElementById('playBtn');
            const playIcon = btn.querySelector('path[name="play"]');
            const pauseIcon = btn.querySelector('path[name="pause"]');

            function togglePlay() {{
                wavesurfer.playPause();
            }}

            wavesurfer.on('play', () => {{
                playIcon.style.display = 'none';
                pauseIcon.style.display = 'block';
            }});

            wavesurfer.on('pause', () => {{
                playIcon.style.display = 'block';
                pauseIcon.style.display = 'none';
            }});
            
            wavesurfer.on('finish', () => {{
                playIcon.style.display = 'block';
                pauseIcon.style.display = 'none';
            }});
        </script>
    </body>
    </html>
    """
    
    # Render component
    components.html(html_code, height=height, scrolling=False)
