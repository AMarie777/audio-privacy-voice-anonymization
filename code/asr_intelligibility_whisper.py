import argparse
import csv
from pathlib import Path
import whisper

def load_transcripts(path):
    mapping = {}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames or []
        if "utt_id" not in fields or "text" not in fields:
            raise RuntimeError(
                f"Transcript file {path} must have columns 'utt_id' and 'text', "
                f"but has: {fields}"
            )
        for row in reader:
            utt_id = row["utt_id"].strip()
            text = row["text"].strip()
            if utt_id:
                mapping[utt_id] = text
    return mapping

#simple WER (levenshtein distance over words)
def compute_wer(ref, hyp):
    #split into words
    r = ref.split()
    h = hyp.split()

    #initialize distance matrix
    dp = [[0] * (len(h) + 1) for _ in range(len(r) + 1)]
    for i in range(len(r) + 1):
        dp[i][0] = i
    for j in range(len(h) + 1):
        dp[0][j] = j
    #compute distances
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            if r[i - 1] == h[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                substitute = dp[i - 1][j - 1] + 1
                insert = dp[i][j - 1] + 1
                delete = dp[i - 1][j] + 1
                dp[i][j] = min(substitute, insert, delete)
    #return WER
    if len(r) == 0:
        #if both ref & hyp are empty WER=0
        return float(len(h))
    return dp[len(r)][len(h)] / len(r)

def main():
    #parse args for running in terminal
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio-root", required=True)
    parser.add_argument("--transcripts", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    
    #load transcripts
    audio_root = Path(args.audio_root)
    transcripts = load_transcripts(args.transcripts)
    all_wavs = sorted(audio_root.rglob("*.wav"))

    #only keep files whose stem (utt_id) exists in transcripts
    pairs = []
    for wav in all_wavs:
        stem = wav.stem  #ex.'1116-137572-0000_form' or '1116-137572-0000'
        base_id = stem.split("_")[0]  #remove any suffix after '_' to match transcript utt_id
        if base_id in transcripts:
            pairs.append((wav, base_id))
    if not pairs:
        print("no wav files matched any utt_id in the transcripts CSV.")
        return
    
    print("loading Whisper model (tiny)...")
    model = whisper.load_model("tiny")
    rows = []
    wers = []

    #transcribe each file & compute WER
    for i, (wav, utt_id) in enumerate(pairs, start=1):
        print(f"[{i}/{len(pairs)}] Transcribing: {wav}")
        result = model.transcribe(str(wav), fp16=False, language="en")
        hyp = result["text"].strip()
        ref = transcripts[utt_id].strip()

        #normalize
        ref_norm = ref.lower()
        hyp_norm = hyp.lower()
        #compute WER
        w = compute_wer(ref_norm, hyp_norm)
        wers.append(w)
        #store results
        rows.append({
            "file": str(wav),
            "utt_id": utt_id,
            "ref": ref,
            "hyp": hyp,
            "wer": w,
        })
    #avg WER
    avg_wer = sum(wers) / len(wers)
    print(f"Average WER over {len(wers)} files: {avg_wer:.3f}")

    #write results to CSV
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"Writing results to {out_path} ...")
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["file", "utt_id", "ref", "hyp", "wer"],
        )
        writer.writeheader()
        writer.writerows(rows)

    print("Done.")

if __name__ == "__main__":
    main()