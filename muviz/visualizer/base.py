"""Base visualizer class"""

from abc import ABC, abstractmethod
import numpy as np
from PIL import Image

from muviz.config.settings import VisualizerConfig, get_theme_colors


class BaseVisualizer(ABC):
    """Base class for all visualizers"""

    def __init__(self, config: VisualizerConfig):
        self.config = config
        self.theme = get_theme_colors(config.theme)
        self.frame_idx = 0

    @abstractmethod
    def render_frame(self, audio_data: dict) -> Image.Image:
        """Render a single frame

        Args:
            audio_data: Dictionary containing audio features

        Returns:
            PIL Image
        """
        pass

    def create_background(self) -> np.ndarray:
        """Create background array

        Returns:
            Background array (height, width, 3)
        """
        bg = self.theme["background"]
        return np.full((self.config.height, self.config.width, 3), bg, dtype=np.uint8)

    def get_color(self, freq_band: str, intensity: float) -> tuple:
        """Get color based on frequency band and intensity

        Args:
            freq_band: 'low', 'mid', or 'high'
            intensity: 0-1 intensity value

        Returns:
            RGB color tuple
        """
        if freq_band == "low":
            base = self.theme["low_freq"]
        elif freq_band == "mid":
            base = self.theme["mid_freq"]
        else:
            base = self.theme["high_freq"]

        # Apply intensity
        return tuple(int(c * (0.3 + 0.7 * intensity)) for c in base)

    def advance_frame(self):
        """Advance to next frame"""
        self.frame_idx += 1
