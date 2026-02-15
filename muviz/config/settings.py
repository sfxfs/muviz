"""Configuration settings for muviz"""

from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class VisualizerConfig:
    """Configuration for visualization"""
    width: int = 1920
    height: int = 1080
    fps: int = 30
    style: str = "geometric"  # geometric, particle, abstract
    theme: str = "cosmic"  # cosmic, neon, pastel
    sample_rate: int = 22050


@dataclass
class AudioConfig:
    """Configuration for audio processing"""
    sample_rate: int = 22050
    hop_length: int = 512
    n_fft: int = 2048
    n_mels: int = 128


# Color themes
THEMES = {
    "cosmic": {
        "background": (10, 10, 30),
        "low_freq": (255, 100, 50),    # Warm orange
        "mid_freq": (150, 50, 200),    # Purple
        "high_freq": (50, 150, 255),   # Cool blue
    },
    "neon": {
        "background": (0, 0, 0),
        "low_freq": (255, 0, 128),     # Hot pink
        "mid_freq": (0, 255, 128),    # Neon green
        "high_freq": (0, 128, 255),   # Electric blue
    },
    "pastel": {
        "background": (250, 245, 240),
        "low_freq": (255, 182, 193),   # Light pink
        "mid_freq": (173, 216, 230),   # Light blue
        "high_freq": (144, 238, 144),  # Light green
    },
}


def get_theme_colors(theme_name: str) -> dict:
    """Get color palette for a theme"""
    return THEMES.get(theme_name, THEMES["cosmic"])
