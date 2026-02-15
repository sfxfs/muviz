"""Frame generation module"""

import numpy as np
from typing import List
from PIL import Image

from muviz.audio.analyzer import AudioAnalyzer
from muviz.visualizer.base import BaseVisualizer
from muviz.config.settings import VisualizerConfig


class FrameGenerator:
    """Generates video frames from audio analysis and visualizer"""

    def __init__(
        self,
        analyzer: AudioAnalyzer,
        visualizer: BaseVisualizer,
        config: VisualizerConfig
    ):
        self.analyzer = analyzer
        self.visualizer = visualizer
        self.config = config

    def generate_frames(self) -> List[Image.Image]:
        """Generate all frames for the video

        Returns:
            List of PIL Image frames
        """
        fps = self.config.fps
        duration = self.analyzer.duration
        num_frames = int(duration * fps)

        frames = []
        for frame_idx in range(num_frames):
            # Get audio data for this frame
            audio_data = self._get_audio_data(frame_idx, fps)

            # Render frame
            frame = self.visualizer.render_frame(audio_data)
            frames.append(frame)

        return frames

    def _get_audio_data(self, frame_idx: int, fps: int) -> dict:
        """Get audio features for a specific frame

        Args:
            frame_idx: Frame index
            fps: Frames per second

        Returns:
            Dictionary of audio features
        """
        return {
            "rms": self.analyzer.get_rms_energy(frame_idx, fps),
            "spectrum": self.analyzer.get_spectrum(frame_idx, fps),
            "waveform": self.analyzer.get_waveform(frame_idx, fps),
            "frequency_bands": self.analyzer.get_frequency_bands(frame_idx, fps)
        }
