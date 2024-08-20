from typing import Literal, Dict

# Process Options
ProcessOpt = {
    "Offline": 0x00000000,
    "RealTime": 0x00000001
}
ProcessOptType = Literal["Offline", "RealTime"]

# Transients Options
TransientsOpt = {
    "Crisp": 0x00000000,
    "Mixed": 0x00000100,
    "Smooth": 0x00000200
}
TransientsOptType = Literal["Crisp", "Mixed", "Smooth"]

# Detector Options
DetectorOpt = {
    "Compound": 0x00000000,
    "Percussive": 0x00000400,
    "Soft": 0x00000800
}
DetectorOptType = Literal["Compound", "Percussive", "Soft"]

# Phase Options
PhaseOpt = {
    "Laminar": 0x00000000,
    "Independent": 0x00002000
}
PhaseOptType = Literal["Laminar", "Independent"]

# Threading Options
ThreadingOpt = {
    "Auto": 0x00000000,
    "Never": 0x00010000,
    "Always": 0x00020000
}
ThreadingOptType = Literal["Auto", "Never", "Always"]

# Window Options
WindowOpt = {
    "Standard": 0x00000000,
    "Short": 0x00100000,
    "Long": 0x00200000
}
WindowOptType = Literal["Standard", "Short", "Long"]

# Smoothing Options
SmoothingOpt = {
    "Off": 0x00000000,
    "On": 0x00800000
}
SmoothingOptType = Literal["Off", "On"]

# Formant Options
FormantOpt = {
    "Shifted": 0x00000000,
    "Preserved": 0x01000000
}
FormantOptType = Literal["Shifted", "Preserved"]

# Pitch Options
PitchOpt = {
    "HighSpeed": 0x00000000,
    "HighQuality": 0x02000000,
    "HighConsistency": 0x04000000
}
PitchOptType = Literal["HighSpeed", "HighQuality", "HighConsistency"]

# Channels Options
ChannelsOpt = {
    "Apart": 0x00000000,
    "Together": 0x10000000
}
ChannelsOptType = Literal["Apart", "Together"]

# Engine Options
EngineOpt = {
    "Faster": 0x00000000,
    "Finer": 0x20000000
}
EngineOptType = Literal["Faster", "Finer"]


def set_finer_engine(window_opt: WindowOptType = "Standard", pitch_opt: PitchOptType = "HighQuality",
                      formant_opt: FormantOptType = "Preserved"):
    faster = EngineOpt["Finer"]
    faster |= WindowOpt[window_opt]
    faster |= PitchOpt[pitch_opt]
    faster |= FormantOpt[formant_opt]
    return faster

def set_faster_engine():
    pass
