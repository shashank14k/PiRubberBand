import os
import configparser
import ctypes

config_path = os.path.join(os.path.dirname(__file__), "config.conf")
config = configparser.ConfigParser()
config.read(config_path)
shared_obj_pth = config.get('Rubberband', 'so_file')

assert os.path.exists(shared_obj_pth), "Failed to locate Rubberband build {}".format(shared_obj_pth)

_rubberband = ctypes.CDLL(shared_obj_pth)

# Init state function
_rubberband.rubberband_new.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_double, ctypes.c_double]
opaque_state_alias = ctypes.c_void_p
_rubberband.rubberband_new.restype = opaque_state_alias

# Reset
_rubberband.rubberband_reset.argtypes = [opaque_state_alias]

# Delete
_rubberband.rubberband_delete.argtypes = [opaque_state_alias]

# TimeRatio
_rubberband.rubberband_set_time_ratio.argtypes = [opaque_state_alias, ctypes.c_double]
_rubberband.rubberband_get_time_ratio.argtypes = [opaque_state_alias]
_rubberband.rubberband_get_time_ratio.restype = ctypes.c_double

# PitchScale
_rubberband.rubberband_set_pitch_scale.argtypes = [opaque_state_alias, ctypes.c_double]
_rubberband.rubberband_get_pitch_scale.argtypes = [opaque_state_alias]
_rubberband.rubberband_get_pitch_scale.restype = ctypes.c_double

# ProcessBuffer
_rubberband.rubberband_process.argtypes = [opaque_state_alias, ctypes.POINTER(ctypes.POINTER(ctypes.c_float)), ctypes.c_int, ctypes.c_int]

# StudyBuffer
_rubberband.rubberband_study.argtypes = [opaque_state_alias, ctypes.POINTER(ctypes.POINTER(ctypes.c_float)), ctypes.c_int, ctypes.c_int]

# Retrieve
_rubberband.rubberband_retrieve.argtypes = [opaque_state_alias, ctypes.POINTER(ctypes.POINTER(ctypes.c_float)), ctypes.c_uint]
_rubberband.rubberband_retrieve.restype = ctypes.c_uint
