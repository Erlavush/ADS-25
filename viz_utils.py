import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_spectrogram(audio_path, title="Spectrogram"):
    """
    Generates a high-quality Mel-Spectrogram using Librosa and Matplotlib.
    Returns the matplotlib figure.
    """
    y, sr = librosa.load(audio_path)
    
    # Compute Mel Spectrogram
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
    S_dB = librosa.power_to_db(S, ref=np.max)

    # Plot
    fig, ax = plt.subplots(figsize=(10, 4))
    img = librosa.display.specshow(S_dB, x_axis='time', y_axis='mel', sr=sr, fmax=8000, ax=ax, cmap='magma')
    fig.colorbar(img, ax=ax, format='%+2.0f dB')
    ax.set_title(title, fontsize=14, color='white')
    
    # Style for Dark Mode
    fig.patch.set_facecolor('#09090b') # Zinc-950
    ax.set_facecolor('#09090b')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.yaxis.label.set_color('white')
    ax.xaxis.label.set_color('white')
    
    plt.tight_layout()
    return fig

def plot_before_after_psd(orig_path, stem_path, stem_name):
    """
    Plots the Power Spectral Density (PSD) comparison.
    Shows how much energy was removed/retained at each frequency.
    """
    y_orig, sr = librosa.load(orig_path)
    y_stem, _ = librosa.load(stem_path)
    
    # Ensure same length
    min_len = min(len(y_orig), len(y_stem))
    y_orig = y_orig[:min_len]
    y_stem = y_stem[:min_len]

    # Compute FFT
    fft_orig = np.abs(np.fft.rfft(y_orig))
    fft_stem = np.abs(np.fft.rfft(y_stem))
    freqs = np.fft.rfftfreq(min_len, 1/sr)

    # Plotly Interactive Figure
    fig = go.Figure()
    
    # Original (Faded)
    fig.add_trace(go.Scatter(
        x=freqs, y=20*np.log10(fft_orig + 1e-6),
        mode='lines', name='Original Mix',
        line=dict(color='gray', width=1),
        opacity=0.5
    ))
    
    # Stem (Pop color)
    color_map = {'Vocals': '#3b82f6', 'Drums': '#ef4444', 'Bass': '#eab308', 'Other': '#22c55e'}
    fig.add_trace(go.Scatter(
        x=freqs, y=20*np.log10(fft_stem + 1e-6),
        mode='lines', name=f'Isolated {stem_name}',
        line=dict(color=color_map.get(stem_name, 'white'), width=2)
    ))

    fig.update_layout(
        title=f"Spectral Analysis: {stem_name} Isolation",
        xaxis_title="Frequency (Hz)",
        yaxis_title="Power (dB)",
        xaxis_type="log",
        template="plotly_dark",
        plot_bgcolor='#09090b',
        paper_bgcolor='#09090b',
        font=dict(family="Figtree, sans-serif")
    )
    return fig
