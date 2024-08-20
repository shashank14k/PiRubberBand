import ctypes
import os
import numpy as np
import soundfile as sf
from rubberband import _rubberband
from options import set_finer_engine


class PRubberBand:
    def __init__(self, sample_rate: int, channels: int, options: int, tempo: float, pitch: float):
        self.sample_rate = sample_rate
        self.channels = channels
        self._tempo = tempo
        self._pitch = pitch
        self.options = options
        print(self.options)
        self.state = _rubberband.rubberband_new(self.sample_rate, self.channels, self.options, self._tempo, self._pitch)

    @property
    def tempo(self):
        return _rubberband.rubberband_get_time_ratio(self.state)

    @property
    def pitch(self):
        return _rubberband.rubberband_get_pitch_scale(self.state)

    @tempo.setter
    def tempo(self, val: float):
        _rubberband.rubberband_set_time_ratio(self.state, val)
        self._tempo = val

    @pitch.setter
    def pitch(self, val: float):
        _rubberband.rubberband_set_pitch_scale(self.state, val)
        self._pitch = val

    def reset(self):
        _rubberband.rubberband_reset(self.state)

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





