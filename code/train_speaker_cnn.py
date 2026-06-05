import random
from pathlib import Path
import librosa
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

#** IMPORTANT NOTE **
#this original folder is not in our final repository! its in the .gitignore due to size 
#if you need to rerun our training script, please download & extract the dataset from the link in the README!
DATA_ROOT = Path(__file__).resolve().parent / "data"

#path to save model checkpoint
MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "speaker_cnn.pt"
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

#audio/model hyperparameters
SAMPLE_RATE = 16000
N_MELS = 40
MAX_FRAMES = 80
BATCH_SIZE = 16
EPOCHS = 10
LR = 1e-3

#dataset class
#loads audio, turns into mel-spectrograms, pads into fixed size, returns (features, label)
class SpeakerDataset(Dataset):
    def __init__(self, root, file_label_pairs):
        self.root = Path(root)
        self.file_label_pairs = file_label_pairs

    def __len__(self):
        return len(self.file_label_pairs)

    def __getitem__(self, idx):
        rel_path, label = self.file_label_pairs[idx]
        wav_path = self.root / rel_path
        
        #load audio @ fixed sample rate
        y, sr = librosa.load(wav_path, sr=SAMPLE_RATE, mono=True)
        #make mel-spectrogram
        mel = librosa.feature.melspectrogram(
            y=y,
            sr=SAMPLE_RATE,
            n_mels=N_MELS
        )
        mel_db = librosa.power_to_db(mel, ref=np.max)
        #normalize per audio clip so volume isnt a factor
        mel_db = (mel_db - mel_db.mean()) / (mel_db.std() + 1e-9)

        #pad or cut to fixed size
        if mel_db.shape[1] < MAX_FRAMES:
            pad_width = MAX_FRAMES - mel_db.shape[1]
            mel_db = np.pad(mel_db, ((0, 0), (0, pad_width)), mode="constant")
        else:
            mel_db = mel_db[:, :MAX_FRAMES]

        #return tensor of shape (1, n_mels, max_frames)
        feat = torch.tensor(mel_db, dtype=torch.float32).unsqueeze(0)
        return feat, torch.tensor(label, dtype=torch.long)

#small CNN for speaker classification
class SimpleCNN(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        #define layers (conv, pool, fc, dropout)
        #3 conv layers + pooling
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.dropout = nn.Dropout(0.3)
        #fully connected layers
        self.fc1 = nn.Linear(64 * 5 * 10, 128)
        self.fc2 = nn.Linear(128, num_classes)
        
    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        b, c, h, w = x.shape
        x = x.view(b, -1)
        x = self.dropout(F.relu(self.fc1(x)))
        x = self.fc2(x)
        return x

#build list of (relative file path, label) pairs
#also maps each speaker label to ID
def build_file_list(root):
    root = Path(root)
    speakers = sorted([d for d in root.iterdir() if d.is_dir()])
    label_to_speaker = {}
    file_label_pairs = []

    for label, spk_dir in enumerate(speakers):
        spk_id = spk_dir.name
        label_to_speaker[label] = spk_id
        wavs = sorted(spk_dir.glob("*.wav"))
        for w in wavs:
            rel = w.relative_to(root)
            file_label_pairs.append((rel, label))

    return file_label_pairs, label_to_speaker

#split data so each speaker has both train & val samples
#randomize per speaker so we dont accidently put all of one speaker's samples in either set
def split_train_val(file_label_pairs, val_fraction=0.3):
    by_label = {}
    for rel, lab in file_label_pairs:
        by_label.setdefault(lab, []).append(rel)

    train_pairs = []
    val_pairs = []

    for lab, files in by_label.items():
        files = list(files)
        random.shuffle(files)
        #70/30 split
        split_idx = max(1, int(len(files) * (1 - val_fraction)))
        train_files = files[:split_idx]
        val_files = files[split_idx:]

        for f in train_files:
            train_pairs.append((f, lab))
        for f in val_files:
            val_pairs.append((f, lab))

    random.shuffle(train_pairs)
    random.shuffle(val_pairs)
    return train_pairs, val_pairs

#main training loop
#train for fixed num of epochs, save best model by val accuracy
def main():
    device = "cpu"
    random.seed(42)

    file_label_pairs, label_to_speaker = build_file_list(DATA_ROOT)
    num_classes = len(label_to_speaker)
    print(f"found {num_classes} speakers")
    print(f"total {len(file_label_pairs)} files")

    train_pairs, val_pairs = split_train_val(file_label_pairs, val_fraction=0.3)
    print(f"train files: {len(train_pairs)}")
    print(f"val files: {len(val_pairs)}")

    train_ds = SpeakerDataset(DATA_ROOT, train_pairs)
    val_ds = SpeakerDataset(DATA_ROOT, val_pairs)

    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False)

    model = SimpleCNN(num_classes=num_classes).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LR)

    best_val_acc = 0.0

    for epoch in range(1, EPOCHS + 1):
        #TRAINING
        model.train()
        train_loss = 0.0
        correct_train = 0
        total_train = 0

        for feats, labels in train_loader:
            feats = feats.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()
            outputs = model(feats)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            train_loss += loss.item() * feats.size(0)
            _, preds = torch.max(outputs, 1)
            correct_train += (preds == labels).sum().item()
            total_train += labels.size(0)

        train_loss /= total_train
        train_acc = correct_train / total_train
        
        #VALIDATION
        model.eval()
        val_loss = 0.0
        correct_val = 0
        total_val = 0

        with torch.no_grad():
            for feats, labels in val_loader:
                feats = feats.to(device)
                labels = labels.to(device)
                outputs = model(feats)
                loss = criterion(outputs, labels)

                val_loss += loss.item() * feats.size(0)
                _, preds = torch.max(outputs, 1)
                correct_val += (preds == labels).sum().item()
                total_val += labels.size(0)

        val_loss /= total_val
        val_acc = correct_val / total_val

        print(
            f"epoch {epoch}/{EPOCHS} | "
            f"train loss {train_loss:.4f} & acc {train_acc*100:.2f}% | "
            f"val loss {val_loss:.4f} & acc {val_acc*100:.2f}%"
        )

        #save best model
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(
                {
                    "model_state": model.state_dict(),
                    "label_to_speaker": label_to_speaker,
                    "n_mels": N_MELS,
                    "sample_rate": SAMPLE_RATE,
                    "max_frames": MAX_FRAMES,
                },
                MODEL_PATH,
            )
            print(f"saved best model to {MODEL_PATH} (acc={val_acc*100:.2f}%)")

    #print results
    print("training done :)")
    print(f"best val acc: {best_val_acc*100:.2f}%")
    print(f"final model saved at: {MODEL_PATH}")

if __name__ == "__main__":
    main()