import librosa
import soundfile as sf
import numpy as np
import pyworld as pw
from scipy.signal import resample
import os
import sys

#------------------------
def formant_shift(audio, sr, ratio=1.3):
    f0, sp, ap = pw.wav2world(audio.astype(np.float64), sr)
    new_bins = int(sp.shape[1] * ratio)

    sp_shifted = resample(sp, new_bins, axis=1)
    sp_shifted = sp_shifted[:, :sp.shape[1]] if new_bins > sp.shape[1] else np.pad(
        sp_shifted, ((0,0),(0, sp.shape[1]-new_bins)), mode="edge"
    )

    sp_shifted = np.ascontiguousarray(sp_shifted)
    shifted = pw.synthesize(f0, sp_shifted, ap, sr)
    return shifted / np.max(np.abs(shifted))

#------------------------
def main(input_file):
    y, sr = librosa.load(input_file, sr=None)
    base = os.path.splitext(os.path.basename(input_file))[0]
    speaker = os.path.basename(os.path.dirname(input_file))

    print(f"Processing: {input_file}")

    # funcs
    def do_pitch(x):
        return librosa.effects.pitch_shift(x, sr=sr, n_steps=-3)

    def do_form(x):
        return formant_shift(x, sr)

    def do_noise(x):
        s = librosa.effects.time_stretch(x, rate=1.0005)
        n = np.random.normal(0, 0.05, len(s))
        return s + n

    effects = {
        "pitch": do_pitch,
        "form": do_form,
        "noise": do_noise
    }

    # make the dirs + singles
    for name, fx in effects.items():
        out_dir = os.path.join(name, speaker)
        os.makedirs(out_dir, exist_ok=True)
        sf.write(f"{out_dir}/{base}_{name}.wav", fx(y), sr)

    # duos
    pairs = [
        ("pitch", "form"),
        ("pitch", "noise"),
        ("form", "noise"),
    ]
    for a, b in pairs:
        out = effects[b](effects[a](y))
        out_dir = os.path.join(f"{a}_{b}", speaker)
        os.makedirs(out_dir, exist_ok=True)
        sf.write(f"{out_dir}/{base}_{a}_{b}.wav", out, sr)

    # all 3
    a3 = ["pitch", "form", "noise"]
    x = y
    for step in a3:
        x = effects[step](x)
        
    out_dir = os.path.join("pitch_form_noise", speaker)
    os.makedirs(out_dir, exist_ok=True)
    sf.write(f"{out_dir}/{base}_pitch_form_noise.wav", x, sr)
        
if __name__ == "__main__":
    import sys
    target = sys.argv[1]# cause i keep forgetting 
    
    if os.path.isdir(target):
        for root, dirs, files in os.walk(target):
            for f in files:
                if f.lower().endswith(".wav"):
                    full = os.path.join(root, f)
                    main(full)
    else:
        main(target)
