import os
import argparse
import csv
from pathlib import Path
import librosa
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

#** IMPORTANT NOTE **
#this evaluation script is designed to work w train_speaker_cnn.py
#to run -> "python code/eval_speaker_cnn.py --root code/(dataset ex. "data_demo") --out results/(whatever file name you want it saved as ex. demo_eval.csv)
#but if you want to test on the FULL dataset or any transformed data like we did to get our results, please download & extract it from the link in the README!
#python3 code/eval_speaker_cnn.py --root pitch_form/ --out results/pitch_form_eval.csv
#same CNN as in train_speaker_cnn.py
class SimpleCNN(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.dropout = nn.Dropout(0.3)
        self.fc1 = nn.Linear(64 * 5 * 10, 128)
        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        b, c, h, w = x.size()
        x = x.view(b, -1)
        x = self.dropout(F.relu(self.fc1(x)))
        x = self.fc2(x)
        return x

#extract features from audio file
def extract_features(path: Path, sample_rate: int, n_mels: int, max_frames: int) -> torch.Tensor:
    #load audio @ same sample rate as training
    y, _ = librosa.load(path, sr=sample_rate, mono=True)

    #make mel-spectrogram
    mel = librosa.feature.melspectrogram(
        y=y,
        sr=sample_rate,
        n_mels=n_mels
    )
    mel_db = librosa.power_to_db(mel, ref=np.max)
    #normalize per audio clip so volume isnt a factor
    mel_db = (mel_db - mel_db.mean()) / (mel_db.std() + 1e-9)
    
    #pad or cut to fixed size
    if mel_db.shape[1] < max_frames:
        pad = max_frames - mel_db.shape[1]
        mel_db = np.pad(mel_db, ((0, 0), (0, pad)), mode="constant")
    else:
        mel_db = mel_db[:, :max_frames]
    
    #return tesnor of shape (1, n_mels, max_frames)
    return torch.tensor(mel_db).unsqueeze(0).float()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--out", default="results/eval_results.csv")
    args = parser.parse_args()
    
    root = Path(args.root)
    if not root.exists():
        raise FileNotFoundError(f"folder not found: {root}")

    device = "cpu"
    #load checkpoint
    MODEL_PATH = Path("code/models/speaker_cnn.pt")
    ckpt = torch.load(MODEL_PATH, map_location=device)
    label_to_speaker = ckpt["label_to_speaker"]
    num_classes = len(label_to_speaker)

    sr = ckpt["sample_rate"]
    n_mels = ckpt["n_mels"]
    max_frames = ckpt["max_frames"]
    #rebuild model & load weights
    model = SimpleCNN(num_classes)
    model.load_state_dict(ckpt["model_state"])
    model.to(device)
    model.eval()

    results = []
    audio_exts = {".wav"}
    file_count = 0

    #walk thru root & all subfolders
    for dirpath, _, filenames in os.walk(root):
        dirpath = Path(dirpath)

        for fn in filenames:
            if Path(fn).suffix.lower() not in audio_exts:
                continue

            file_count += 1
            filepath = dirpath / fn
            true_spk = filepath.parent.name  #ex. spk001
            #extract features & send thru model
            feat = extract_features(filepath, sr, n_mels, max_frames).unsqueeze(0).to(device)

            with torch.no_grad():
                logits = model(feat)
                probs = torch.softmax(logits, dim=1)
                pred_idx = int(torch.argmax(probs, dim=1))
                pred_spk = label_to_speaker[pred_idx]
                conf = float(probs[0, pred_idx])

            correct = int(pred_spk == true_spk)
            results.append([str(filepath), true_spk, pred_spk, conf, correct])

    print(f"found {file_count} files")
    if file_count == 0:
        print("file count=0, check folder path")
        return

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    
    #save results to CSV
    with out.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["file", "true_speaker", "pred_speaker", "confidence", "correct"])
        writer.writerows(results)
    
    #print results
    acc = sum(r[4] for r in results) / len(results)
    print(f"acc: {acc*100:.2f}%")
    print(f"results saved at: {out.resolve()}")

if __name__ == "__main__":
    main()