"""Audio analysis module"""

import numpy as np
import librosa
from typing import Tuple, Optional


class AudioAnalyzer:
    """Analyzes audio files and extracts features for visualization"""

    def __init__(self, sample_rate: int = 22050, hop_length: int = 512, n_fft: int = 2048):
        self.sample_rate = sample_rate
        self.hop_length = hop_length
        self.n_fft = n_fft
        self.audio = None
        self.duration = 0

    def load_audio(self, file_path: str, duration: Optional[float] = None) -> None:
        """Load audio file

        Args:
            file_path: Path to audio file
            duration: Optional duration limit in seconds
        """
        self.audio, sr = librosa.load(
            file_path,
            sr=self.sample_rate,
            duration=duration
        )
        self.duration = len(self.audio) / self.sample_rate

    def get_spectrum(self, frame_idx: int, fps: int) -> np.ndarray:
        """Get frequency spectrum for a specific frame

        Args:
            frame_idx: Frame index
            fps: Frames per second

        Returns:
            Frequency spectrum (magnitude)
        """
        if self.audio is None:
            return np.zeros(self.n_fft // 2 + 1)

        # Calculate sample position
        samples_per_frame = self.sample_rate / fps
        start_sample = int(frame_idx * samples_per_frame)
        end_sample = min(start_sample + int(samples_per_frame), len(self.audio))

        if start_sample >= len(self.audio):
            return np.zeros(self.n_fft // 2 + 1)

        # Extract frame and apply FFT
        frame = self.audio[start_sample:end_sample]
        if len(frame) < self.n_fft:
            frame = np.pad(frame, (0, self.n_fft - len(frame)))

        spectrum = np.fft.rfft(frame * np.hanning(self.n_fft))
        return np.abs(spectrum)

    def get_mel_spectrogram(self, n_mels: int = 128) -> np.ndarray:
        """Get mel spectrogram

        Args:
            n_mels: Number of mel bands

        Returns:
            Mel spectrogram matrix
        """
        if self.audio is None:
            return np.zeros((n_mels, 1))

        mel_spec = librosa.feature.melspectrogram(
            y=self.audio,
            sr=self.sample_rate,
            n_fft=self.n_fft,
            hop_length=self.hop_length,
            n_mels=n_mels
        )
        return librosa.power_to_db(mel_spec, ref=np.max)

    def get_waveform(self, frame_idx: int, fps: int, num_samples: int = 1024) -> np.ndarray:
        """Get waveform segment for a specific frame

        Args:
            frame_idx: Frame index
            fps: Frames per second
            num_samples: Number of samples to return

        Returns:
            Waveform segment
        """
        if self.audio is None:
            return np.zeros(num_samples)

        samples_per_frame = self.sample_rate / fps
        start_sample = int(frame_idx * samples_per_frame)
        end_sample = start_sample + num_samples

        if start_sample >= len(self.audio):
            return np.zeros(num_samples)

        waveform = self.audio[start_sample:min(end_sample, len(self.audio))]
        if len(waveform) < num_samples:
            waveform = np.pad(waveform, (0, num_samples - len(waveform)))

        return waveform

    def get_rms_energy(self, frame_idx: int, fps: int) -> float:
        """Get RMS energy for a specific frame

        Args:
            frame_idx: Frame index
            fps: Frames per second

        Returns:
            RMS energy value (0-1 normalized)
        """
        if self.audio is None:
            return 0.0

        samples_per_frame = self.sample_rate / fps
        start_sample = int(frame_idx * samples_per_frame)
        end_sample = min(start_sample + int(samples_per_frame), len(self.audio))

        if start_sample >= len(self.audio):
            return 0.0

        frame = self.audio[start_sample:end_sample]
        rms = np.sqrt(np.mean(frame ** 2))
        return min(rms * 5, 1.0)  # Scale and clamp

    def get_beat_positions(self) -> np.ndarray:
        """Detect beat positions in the audio

        Returns:
            Array of beat positions in frames (assuming 30fps)
        """
        if self.audio is None:
            return np.array([])

        # Use onset envelope for beat detection
        onset_env = librosa.onset.onset_detect(
            y=self.audio,
            sr=self.sample_rate,
            hop_length=self.hop_length,
            backtrack=True
        )

        # Convert to frame positions (assuming 30fps for visualization)
        fps = 30
        beats_per_sample = self.sample_rate / (self.hop_length * fps)
        beat_frames = (onset_env * beats_per_sample).astype(int)

        return np.unique(beat_frames)

    def get_frequency_bands(self, frame_idx: int, fps: int) -> Tuple[float, float, float]:
        """Get energy in low, mid, and high frequency bands

        Args:
            frame_idx: Frame index
            fps: Frames per second

        Returns:
            Tuple of (low, mid, high) energy values (0-1)
        """
        spectrum = self.get_spectrum(frame_idx, fps)
        n = len(spectrum)

        if n == 0:
            return (0.0, 0.0, 0.0)

        # Split into 3 bands
        low_end = n // 3
        mid_end = 2 * n // 3

        low = np.mean(spectrum[:low_end])
        mid = np.mean(spectrum[low_end:mid_end])
        high = np.mean(spectrum[mid_end:])

        # Normalize
        max_val = max(low, mid, high, 1e-10)
        return (low / max_val, mid / max_val, high / max_val)
