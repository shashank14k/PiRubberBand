import ctypes
import os
from typing import Optional
import numpy as np
import soundfile as sf
from pirubberband.rubberband import _rubberband
from pirubberband.options import set_finer_engine


class PRubberBand:
    def __init__(self, sample_rate: int, channels: int, tempo: float, pitch: float, options: Optional[int] = None, max_process_size: Optional[float] = None):
        self.sample_rate = sample_rate
        self.channels = channels
        self._tempo = tempo
        self._pitch = pitch
        self.options = options if options is not None else set_finer_engine()
        self.state = _rubberband.rubberband_new(self.sample_rate, self.channels, self.options, self._tempo, self._pitch)
        if max_process_size is None:
            self._process_size = self.max_process_size
        else:
            self._process_size = max_process_size
        self.out = np.zeros((self.channels, 1), dtype=np.float32)

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

    def study(self, buffer: np.ndarray):
        ptr = 0
        final = False
        while not final:
            cur_size = min(self.process_size, buffer.shape[1] - ptr)
            batch_buffer = buffer[:, ptr:ptr+cur_size]
            buffer_ptr = (ctypes.POINTER(ctypes.c_float) * self.channels)()
            for i in range(self.channels):
                buffer_ptr[i] = batch_buffer[i].ctypes.data_as(ctypes.POINTER(ctypes.c_float))
            final = ptr + cur_size >= buffer.shape[1]
            _rubberband.rubberband_study(self.state, buffer_ptr, cur_size, final)
            ptr += cur_size


    def process(self, buffer: np.ndarray):
        ptr = 0
        final = False
        tot = 0
        while not final:
            cur_size = min(self.process_size, buffer.shape[1] - ptr)
            batch_buffer = buffer[:, ptr:ptr + cur_size].copy()
            buffer_ptr = (ctypes.POINTER(ctypes.c_float) * self.channels)()
            for i in range(self.channels):
                buffer_ptr[i] = batch_buffer[i].ctypes.data_as(ctypes.POINTER(ctypes.c_float))
            final = ptr + cur_size >= buffer.shape[1]
            _rubberband.rubberband_process(self.state, buffer_ptr, cur_size, final)
            ptr += cur_size
            while 1:
                avail = self.available()
                avail = min(avail, cur_size)
                if avail <= 0:
                    break
                av = _rubberband.rubberband_retrieve(self.state, buffer_ptr, avail)
                tot += av
                batch_buffer = batch_buffer[:, :avail]
                self.out = np.concatenate([self.out, batch_buffer], axis=-1)
def pitch_shift_audio_file(filepath: os.path, scale: float, save_path: os.path):
    assert os.path.exists(filepath), "Invalid file-path {}".format(filepath)
    data, samplerate = sf.read(filepath)
    data = data.astype(np.float32).T #(channel, samples)
    options = set_finer_engine()
    obj = PRubberBand(samplerate, data.shape[0], 1.0, 1.0, options, 1024)
    obj.pitch = scale
    obj.study(data)
    obj.process(data)
    sf.write(save_path, obj.out.T, samplerate)

def time_stretch_audio_file(filepath: os.path, rate: float, save_path: os.path):
    assert os.path.exists(filepath), "Invalid file-path {}".format(filepath)
    data, samplerate = sf.read(filepath)
    data = data.astype(np.float32).T #(channel, samples)
    options = set_finer_engine()
    obj = PRubberBand(samplerate, data.shape[0], 1.0, 1.0, options, 1024)
    obj.tempo = rate
    obj.study(data)
    obj.process(data)
    sf.write(save_path, obj.out.T, samplerate)




