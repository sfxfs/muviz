"""Particle system visualization"""

import math
import random
import numpy as np
from PIL import Image, ImageDraw

from muviz.visualizer.base import BaseVisualizer


class Particle:
    """Single particle"""

    def __init__(self, x: float, y: float, vx: float, vy: float, color: tuple, size: int):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.life = 1.0


class ParticleVisualizer(BaseVisualizer):
    """Particle system that reacts to audio"""

    def __init__(self, config):
        super().__init__(config)
        self.particles = []
        self.max_particles = 200

    def render_frame(self, audio_data: dict) -> Image.Image:
        """Render particle visualization

        Args:
            audio_data: Dictionary with 'rms', 'frequency_bands', 'spectrum'

        Returns:
            PIL Image
        """
        # Create background
        img = Image.new("RGB", (self.config.width, self.config.height))
        draw = ImageDraw.Draw(img)

        # Fill background with slight trail effect
        bg = self.theme["background"]
        draw.rectangle([0, 0, self.config.width, self.config.height], fill=bg)

        # Get audio features
        rms = audio_data.get("rms", 0.0)
        low, mid, high = audio_data.get("frequency_bands", (0.5, 0.5, 0.5))

        # Spawn new particles based on audio
        self._spawn_particles(rms, low, mid, high)

        # Update and draw particles
        self._update_particles()
        self._draw_particles(draw)

        self.advance_frame()
        return img

    def _spawn_particles(self, rms: float, low: float, mid: float, high: float):
        """Spawn new particles"""
        # Number of particles to spawn based on audio energy
        num_to_spawn = int(rms * 10) + 2

        center_x = self.config.width // 2
        center_y = self.config.height // 2

        for _ in range(num_to_spawn):
            if len(self.particles) >= self.max_particles:
                break

            # Choose color based on frequency
            rand = random.random()
            if rand < 0.33:
                color = self.get_color("low", low)
            elif rand < 0.66:
                color = self.get_color("mid", mid)
            else:
                color = self.get_color("high", high)

            # Random velocity based on mid frequencies
            speed = (mid + 0.2) * 5
            angle = random.random() * 2 * math.pi
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed

            size = random.randint(2, 6 + int(rms * 6))

            # Spawn at center with some spread
            spread = 50
            x = center_x + random.uniform(-spread, spread)
            y = center_y + random.uniform(-spread, spread)

            self.particles.append(Particle(x, y, vx, vy, color, size))

    def _update_particles(self):
        """Update particle positions"""
        for p in self.particles:
            p.x += p.vx
            p.y += p.vy
            p.life -= 0.02

            # Slow down
            p.vx *= 0.98
            p.vy *= 0.98

        # Remove dead particles
        self.particles = [p for p in self.particles if p.life > 0]

    def _draw_particles(self, draw: ImageDraw):
        """Draw all particles"""
        for p in self.particles:
            if p.life > 0:
                # Scale size by life
                size = int(p.size * p.life)
                if size < 1:
                    size = 1

                x = int(p.x)
                y = int(p.y)

                # Draw particle
                color = tuple(int(c * p.life) for c in p.color)
                draw.ellipse(
                    [x - size, y - size, x + size, y + size],
                    fill=color
                )
