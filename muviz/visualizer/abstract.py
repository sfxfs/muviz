"""Abstract art visualization"""

import math
import random
import numpy as np
from PIL import Image, ImageDraw

from muviz.visualizer.base import BaseVisualizer


class AbstractVisualizer(BaseVisualizer):
    """Abstract art patterns that react to audio"""

    def __init__(self, config):
        super().__init__(config)
        self.waveform_history = []
        self.max_history = 100

    def render_frame(self, audio_data: dict) -> Image.Image:
        """Render abstract visualization

        Args:
            audio_data: Dictionary with 'rms', 'frequency_bands', 'spectrum', 'waveform'

        Returns:
            PIL Image
        """
        # Create background
        img = Image.new("RGB", (self.config.width, self.config.height))
        draw = ImageDraw.Draw(img)

        # Fill background
        bg = self.theme["background"]
        draw.rectangle([0, 0, self.config.width, self.config.height], fill=bg)

        # Get audio features
        rms = audio_data.get("rms", 0.0)
        low, mid, high = audio_data.get("frequency_bands", (0.5, 0.5, 0.5))
        waveform = audio_data.get("waveform", np.zeros(1024))

        # Draw flowing waveform
        self._draw_flowing_waveform(draw, waveform, rms)

        # Draw frequency bars
        self._draw_frequency_bars(draw, audio_data.get("spectrum", np.zeros(1024)), mid)

        # Draw circular aura
        self._draw_circular_aura(draw, low, mid, high)

        self.advance_frame()
        return img

    def _draw_flowing_waveform(self, draw: ImageDraw, waveform: np.ndarray, rms: float):
        """Draw flowing waveform across screen"""
        if len(waveform) < 2:
            return

        # Store waveform in history
        self.waveform_history.append(waveform.copy())
        if len(self.waveform_history) > self.max_history:
            self.waveform_history.pop(0)

        # Draw multiple waveforms from history
        for i, wf in enumerate(self.waveform_history):
            alpha = (i + 1) / len(self.waveform_history)
            y_offset = self.config.height // 2
            scale = self.config.height // 4

            points = []
            step = len(wf) // self.config.width
            if step < 1:
                step = 1

            for x in range(0, min(len(wf), self.config.width), step):
                idx = x * len(wf) // self.config.width
                y = y_offset + int(wf[idx] * scale * (0.5 + rms))
                points.append((x, y))

            if len(points) > 1:
                color = self.get_color("mid", alpha * rms)
                color = tuple(int(c * alpha) for c in color)
                draw.line(points, fill=color, width=2)

    def _draw_frequency_bars(self, draw: ImageDraw, spectrum: np.ndarray, intensity: float):
        """Draw vertical frequency bars"""
        if len(spectrum) < 2:
            return

        num_bars = 32
        bar_width = self.config.width // num_bars
        bar_spacing = 2

        # Get relevant portion of spectrum
        spectrum_slice = spectrum[:len(spectrum) // 4]  # Use low frequencies
        step = len(spectrum_slice) // num_bars
        if step < 1:
            step = 1

        for i in range(num_bars):
            idx = i * step
            if idx >= len(spectrum_slice):
                break

            # Normalize height
            height = int((spectrum_slice[idx] / 255) * self.config.height * 0.7)
            height = max(5, min(height, self.config.height * 9 // 10))

            x = i * bar_width
            y_top = self.config.height - height

            # Color based on position
            if i < num_bars // 3:
                color = self.get_color("low", intensity)
            elif i < 2 * num_bars // 3:
                color = self.get_color("mid", intensity)
            else:
                color = self.get_color("high", intensity)

            draw.rectangle(
                [x + bar_spacing, y_top, x + bar_width - bar_spacing, self.config.height],
                fill=color
            )

    def _draw_circular_aura(self, draw: ImageDraw, low: float, mid: float, high: float):
        """Draw circular aura in center"""
        center_x = self.config.width // 2
        center_y = self.config.height // 2

        # Multiple concentric rings
        for i in range(5):
            radius = 50 + i * 40 + int(mid * 30)
            color = self.get_color("mid", mid * (1 - i * 0.15))

            # Pulsing effect
            pulse = int(math.sin(self.frame_idx * 0.1 + i) * 5 * low)
            radius += pulse

            draw.ellipse(
                [
                    center_x - radius,
                    center_y - radius,
                    center_x + radius,
                    center_y + radius
                ],
                outline=color,
                width=2
            )

        # Inner glow
        radius = 30 + int(high * 40)
        color = self.get_color("high", high)
        draw.ellipse(
            [
                center_x - radius,
                center_y - radius,
                center_x + radius,
                center_y + radius
            ],
            fill=color
        )
