# Audio Privacy Through Voice Anonymization

Can editing audio distort someone's voice enough to make it effectively anonymous, and how do we model the trade-off between privacy and intelligibility in anonymized speech data?

## Overview

Nowadays, most of us interact with voice assistants every day. Whether it's Siri, Alexa, Google Assistant, or another speech-based system, our voices are constantly being recorded, processed, and stored. While companies often claim that this data is anonymous, voice recordings themselves are highly identifiable biometric information.

This project explores whether voice recordings can be manipulated enough to protect a speaker's identity while still preserving the meaning of what is being said. We wanted to investigate the balance between privacy and usability:

- How much can a voice be altered before it becomes unrecognizable?
- Can speech remain understandable after anonymization?
- Is voice anonymity actually achievable?

## Research Question

Can editing audio distort someone's voice enough to make it effectively anonymous, and how do we model the trade-off between privacy and intelligibility in anonymized speech data?

## Motivation

One of the biggest concerns surrounding modern voice assistants is how voice recordings are collected, stored, and used. Unlike passwords, voices cannot easily be changed or revoked once compromised. Even when recordings are disconnected from a user's account information, the voice itself may still reveal the speaker's identity.

We wanted to explore whether simple audio transformations could reduce the ability of machine learning models to identify speakers while still allowing speech recognition systems to understand what was said.

## Dataset

Originally, we planned to collect and record our own dataset. After realizing that data collection would become a bottleneck, we pivoted to using the LibriSpeech ASR corpus from OpenSLR.

The dataset contains English speech recordings from multiple speakers and is distributed under the Creative Commons Attribution 4.0 license, allowing it to be used and modified for research purposes.

For our experiments:

- 20 speakers were selected
- Each speaker contributed 15+ audio clips
- Thousands of transformed audio samples were generated
- Approximately 2.5 GB of transformed audio data was produced

The original dataset is not included in this repository.

## Methodology

### Audio Transformations

Using Python audio processing libraries, we created several anonymized versions of each audio sample.

The transformations included:

- Pitch shifting
- Formant shifting
- Noise injection

We also evaluated every combination of these techniques, resulting in seven total transformation groups.

The goal was to determine which transformations best reduced speaker identifiability while preserving intelligibility.

### Speaker Recognition Model

To simulate an attacker attempting to identify speakers, we trained a Convolutional Neural Network (CNN) using unmodified speech recordings.

The model:

1. Converts audio clips into mel-spectrograms
2. Extracts acoustic features using convolutional layers
3. Classifies the speaker associated with each clip

The model achieved approximately:

- 98% training accuracy
- 96% evaluation accuracy

on unmodified speech recordings.

We then evaluated the transformed audio using the same model to measure how effectively each transformation anonymized the speaker.

### Intelligibility Analysis

Privacy alone is not useful if the transformed audio becomes impossible to understand.

To evaluate intelligibility, we used OpenAI Whisper to automatically transcribe transformed audio clips and compared those transcripts against the original text using Word Error Rate (WER).

Lower speaker recognition accuracy indicates better privacy.

Lower WER indicates better intelligibility.

Together, these metrics allowed us to evaluate the trade-off between anonymity and usability.

## Results

| Transformation | Speaker Accuracy | Average WER |
|---------------|-----------------|-------------|
| Original | 96.0% | 0.19 |
| Formant | 23.0% | 0.26 |
| Pitch | 40.64% | 0.60 |
| Noise | 34.10% | 0.62 |
| Pitch + Formant | 67.30% | 0.79 |
| Formant + Noise | 12.98% | 0.65 |
| Pitch + Noise | 29.18% | 1.017 |
| Pitch + Noise + Formant | 23.34% | 0.97 |

### Key Findings

- Formant shifting significantly reduced speaker identification accuracy while maintaining relatively strong intelligibility.
- Formant + Noise achieved the lowest speaker recognition accuracy of all transformations.
- Pitch and formant shifting partially canceled each other out, making the Pitch + Formant combination less effective than expected.
- Heavy combinations of pitch shifting and noise often produced audio that became difficult for Whisper to transcribe accurately.

While many of the transformed clips sounded like completely different people to human listeners, the project also raised an important question: how difficult would it be to reverse these transformations if an attacker knew how they were generated?

## Challenges

One of the biggest challenges was processing time.

Generating transformed datasets, training speaker recognition models, and running Whisper transcription required processing thousands of audio samples. Some experiments took over 30 minutes to complete, and moving or compressing large collections of audio files often became a bottleneck.

We also encountered dependency issues while developing across Windows and macOS environments.

## Future Work

Potential improvements include:

- Additional audio transformation techniques
- Larger speaker populations
- More advanced speaker recognition models
- Evaluating reversible vs. irreversible transformations
- Testing against commercial voice assistant systems

## Technologies Used

- Python
- PyTorch
- Librosa
- NumPy
- PyWorld
- OpenAI Whisper
- Machine Learning
- Audio Signal Processing

## Repository Structure

```
code/
results/
docs/
README.md
```

## Documentation

Additional project documentation can be found in:

- docs/final-report.pdf
- docs/proposal.pdf

## Contributors

Alexa McKee  
Gabriela Diaz