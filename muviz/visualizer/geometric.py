"""Geometric visualization"""

import math
import numpy as np
from PIL import Image, ImageDraw

from muviz.visualizer.base import BaseVisualizer


class GeometricVisualizer(BaseVisualizer):
    """Geometric shapes that react to audio"""

    def __init__(self, config):
        super().__init__(config)
        self.center_x = config.width // 2
        self.center_y = config.height // 2
        self.max_radius = min(config.width, config.height) // 3

    def render_frame(self, audio_data: dict) -> Image.Image:
        """Render geometric visualization

        Args:
            audio_data: Dictionary with 'rms', 'frequency_bands', 'spectrum'

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

        # Draw concentric circles based on frequency bands
        self._draw_circles(draw, low, mid, high, rms)

        # Draw polygon in center
        self._draw_polygon(draw, mid, rms)

        # Draw radiating lines
        self._draw_radiating_lines(draw, high, rms)

        self.advance_frame()
        return img

    def _draw_circles(self, draw: ImageDraw, low: float, mid: float, high: float, rms: float):
        """Draw concentric circles"""
        colors = [
            self.get_color("low", low),
            self.get_color("mid", mid),
            self.get_color("high", high)
        ]

        radii = [
            self.max_radius * (0.3 + 0.4 * low),
            self.max_radius * (0.4 + 0.3 * mid),
            self.max_radius * (0.5 + 0.3 * high)
        ]

        for radius, color in zip(radii, colors):
            if radius > 10:
                width = max(1, int(rms * 8))
                draw.ellipse(
                    [
                        self.center_x - radius,
                        self.center_y - radius,
                        self.center_x + radius,
                        self.center_y + radius
                    ],
                    outline=color,
                    width=width
                )

    def _draw_polygon(self, draw: ImageDraw, mid: float, rms: float):
        """Draw rotating polygon in center"""
        sides = 6
        rotation = self.frame_idx * 0.02
        base_radius = 50 + rms * 100

        points = []
        for i in range(sides):
            angle = (2 * math.pi * i / sides) + rotation
            x = self.center_x + base_radius * math.cos(angle)
            y = self.center_y + base_radius * math.sin(angle)
            points.append((x, y))

        color = self.get_color("mid", mid)
        draw.polygon(points, outline=color, width=3)

    def _draw_radiating_lines(self, draw: ImageDraw, high: float, rms: float):
        """Draw lines radiating from center"""
        num_lines = 12
        inner_radius = self.max_radius * 0.6
        outer_radius = self.max_radius * (0.8 + high * 0.4)

        for i in range(num_lines):
            angle = (2 * math.pi * i / num_lines) + self.frame_idx * 0.01

            x1 = self.center_x + inner_radius * math.cos(angle)
            y1 = self.center_y + inner_radius * math.sin(angle)
            x2 = self.center_x + outer_radius * math.cos(angle)
            y2 = self.center_y + outer_radius * math.sin(angle)

            color = self.get_color("high", high)
            width = max(1, int(high * 4))
            draw.line([x1, y1, x2, y2], fill=color, width=width)
