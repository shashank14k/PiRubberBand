import ctypes
import os
from typing import Optional
import numpy as np
import soundfile as sf
from rubberband import _rubberband
from options import set_finer_engine


class PRubberBand:
    def __init__(self, sample_rate: int, channels: int, options: int, tempo: float, pitch: float, max_process_size: Optional[float] = None):
        self.sample_rate = sample_rate
        self.channels = channels
        self._tempo = tempo
        self._pitch = pitch
        self.options = options
        self.state = _rubberband.rubberband_new(self.sample_rate, self.channels, self.options, self._tempo, self._pitch)
        if max_process_size is None:
            self._process_size = self.max_process_size
        else:
            self._process_size = max_process_size
        self.out = np.zeros((2, 1), dtype=np.float32)

    @property
    def tempo(self):
        return _rubberband.rubberband_get_time_ratio(self.state)

    @property
    def pitch(self):
        return _rubberband.rubberband_get_pitch_scale(self.state)
    @property
    def max_process_size(self):
        return _rubberband.rubberband_get_process_size_limit(self.state)

    @property
    def process_size(self):
        return self._process_size

    @tempo.setter
    def tempo(self, val: float):
        _rubberband.rubberband_set_time_ratio(self.state, val)
        self._tempo = val

    @pitch.setter
    def pitch(self, val: float):
        _rubberband.rubberband_set_pitch_scale(self.state, val)
        self._pitch = val

    @process_size.setter
    def process_size(self, val: float):
        self._process_size = min(self.max_process_size, val)
        _rubberband.rubberband_set_max_process_size(self.state, self._process_size)

    def reset(self):
        _rubberband.rubberband_reset(self.state)

    def available(self):
        return _rubberband.rubberband_available(self.state)

    def __del__(self):
        _rubberband.rubberband_delete(self.state)

    def process(self, buffer: np.ndarray, last_buffer: int):
        """

        :param buffer: of shape (channel, num_samples) where channel = 1 for mono and 2 for stereo
        :param last_buffer:
        :return:
        """
        buffer_ptr = (ctypes.POINTER(ctypes.c_float) * self.channels)()
        for i in range(self.channels):
            buffer_ptr[i] = buffer[i].ctypes.data_as(ctypes.POINTER(ctypes.c_float))
        _rubberband.rubberband_study(self.state, buffer_ptr, buffer.shape[1], last_buffer)
        _rubberband.rubberband_process(self.state, buffer_ptr, buffer.shape[1], last_buffer)
        av = _rubberband.rubberband_retrieve(self.state, buffer_ptr, buffer.shape[1])
        while av != 0:
            av = _rubberband.rubberband_retrieve(self.state, buffer_ptr, buffer.shape[1])





