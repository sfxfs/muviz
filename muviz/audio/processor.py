"""Audio preprocessing module"""

import numpy as np
import librosa


class AudioProcessor:
    """Preprocesses audio for visualization"""

    @staticmethod
    def normalize(audio: np.ndarray) -> np.ndarray:
        """Normalize audio to -1 to 1 range

        Args:
            audio: Audio array

        Returns:
            Normalized audio
        """
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            return audio / max_val
        return audio

    @staticmethod
    def apply_fade(audio: np.ndarray, sample_rate: int, fade_duration: float = 0.5) -> np.ndarray:
        """Apply fade in/out to audio

        Args:
            audio: Audio array
            sample_rate: Sample rate
            fade_duration: Fade duration in seconds

        Returns:
            Audio with fade applied
        """
        fade_samples = int(fade_duration * sample_rate)
        fade_samples = min(fade_samples, len(audio) // 4)

        # Fade in
        fade_in = np.linspace(0, 1, fade_samples)
        audio[:fade_samples] *= fade_in

        # Fade out
        fade_out = np.linspace(1, 0, fade_samples)
        audio[-fade_samples:] *= fade_out

        return audio

    @staticmethod
    def resample(audio: np.ndarray, orig_sr: int, target_sr: int) -> np.ndarray:
        """Resample audio to target sample rate

        Args:
            audio: Audio array
            orig_sr: Original sample rate
            target_sr: Target sample rate

        Returns:
            Resampled audio
        """
        if orig_sr == target_sr:
            return audio

        return librosa.resample(audio, orig_sr=orig_sr, target_sr=target_sr)

    @staticmethod
    def extract_channels(audio: np.ndarray) -> np.ndarray:
        """Convert stereo to mono if needed

        Args:
            audio: Audio array (can be mono or stereo)

        Returns:
            Mono audio array
        """
        if audio.ndim > 1:
            return np.mean(audio, axis=1)
        return audio
