"""Video writing module"""

import numpy as np
from typing import List
from PIL import Image

try:
    from moviepy import ImageSequenceClip, AudioFileClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

from muviz.config.settings import VisualizerConfig


class VideoWriter:
    """Writes video files from frames"""

    def __init__(self, config: VisualizerConfig):
        self.config = config

    def write_video(self, frames: List[Image.Image], audio: np.ndarray, output_path: str):
        """Write frames to video file with audio

        Args:
            frames: List of PIL Image frames
            audio: Audio array
            output_path: Output video file path
        """
        if not frames:
            raise ValueError("No frames to write")

        if MOVIEPY_AVAILABLE:
            self._write_with_moviepy(frames, audio, output_path)
        elif CV2_AVAILABLE:
            self._write_with_cv2(frames, output_path)
        else:
            raise RuntimeError("Neither moviepy nor opencv-python available")

    def _write_with_moviepy(
        self,
        frames: List[Image.Image],
        audio: np.ndarray,
        output_path: str
    ):
        """Write video using MoviePy"""
        # Convert frames to numpy arrays
        frame_arrays = [np.array(frame) for frame in frames]

        # Convert RGB to BGR for moviepy
        frame_arrays = [frame[:, :, ::-1] for frame in frame_arrays]

        # Create video clip
        clip = ImageSequenceClip(frame_arrays, fps=self.config.fps)

        # Add audio if available
        import tempfile
        import soundfile as sf

        if len(audio) > 0:
            # Save audio to temp file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp_path = tmp.name

            sf.write(tmp_path, audio, self.config.sample_rate)
            audio_clip = AudioFileClip(tmp_path)
            clip = clip.with_audio(audio_clip)

        # Write video
        clip.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            logger=None
        )

    def _write_with_cv2(self, frames: List[Image.Image], output_path: str):
        """Write video using OpenCV"""
        # Get video writer
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(
            output_path,
            fourcc,
            self.config.fps,
            (self.config.width, self.config.height)
        )

        if not writer.isOpened():
            raise RuntimeError("Failed to open video writer")

        try:
            for frame in frames:
                # Convert RGB to BGR
                frame_bgr = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
                writer.write(frame_bgr)
        finally:
            writer.release()

        # Note: Audio not supported with OpenCV alone
        if len(frames) > 0:
            print("Warning: Audio not included (moviepy not available)")
