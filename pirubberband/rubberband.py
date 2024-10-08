import ctypes
import sys
import os
import logging

logger = logging.getLogger(__name__)
def load_rubberband_library():
# Determine the base directory for the installed package
    package_dir = os.path.abspath(os.path.dirname(__file__))
    lib_dir = os.path.join(package_dir, "rubberband_build")

    if sys.platform.startswith('win'):
        # Windows
        lib_file = os.path.join(lib_dir, 'librubberband-2.dll')
        win_mode = 0
    elif sys.platform.startswith('linux'):
        # Linux
        lib_file = os.path.join(lib_dir, 'librubberband.so')
        win_mode = None
    else:
        raise RuntimeError(f"Unsupported platform: {sys.platform}")

    if not os.path.exists(lib_file):
        raise RuntimeError(f"Rubberband library not found at {lib_file}")
    return str(lib_file), win_mode

# Usage
shared_obj_pth, w = load_rubberband_library()
_rubberband = ctypes.CDLL(shared_obj_pth, winmode=w)

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

# BufferLimits
_rubberband.rubberband_get_process_size_limit.argtypes = [opaque_state_alias]
_rubberband.rubberband_get_process_size_limit.restype = ctypes.c_uint
_rubberband.rubberband_set_max_process_size.argtypes = [opaque_state_alias, ctypes.c_uint]
_rubberband.rubberband_available.argtypes = [opaque_state_alias]
_rubberband.rubberband_available.restype = ctypes.c_int
_rubberband.rubberband_get_samples_required.argtypes = [opaque_state_alias]
_rubberband.rubberband_get_samples_required.restype = ctypes.c_uint