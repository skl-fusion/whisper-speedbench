# Whisper Speedbench

This Python script utilizes ffmpeg and OpenAI's Whisper API to benchmark the transcription accuracy of audio files at various playback speeds. It speeds up audio files, transcribes them, and calculates the Word Error Rate (WER) from 1.1x to 4x speed increments. The normal 1.0x transcript serves as the baseline for accuracy comparison.

## Setup

1. **Environment Setup**:
   - Copy `example.env` to `.env` in the root directory and update it with your OpenAI API key:
     ```
     cp example.env .env
     # Open .env and replace your_openai_api_key_here with your actual OpenAI API key
     ```
   - Ensure the `.env` file is not tracked by Git (included in `.gitignore`).

2. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```

## Usage
   - Execute the script by running:
     ```
     python benchmark.py path_to_your_audio_file
     ```
   - Optionally, specify the language code if the audio is not in English:
     ```
     python benchmark.py path_to_your_audio_file --language es
     ```

This script converts the specified audio file to MP3 format, processes it at speeds ranging from 1.1x to 4x, transcribes the audio using the Whisper API, computes the WER for each speed, and outputs the results to a CSV file named `benchmark_results.csv`.

## License

This project is licensed under the MIT License and is open-source.