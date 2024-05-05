import ffmpeg
import argparse
import subprocess
from openai import OpenAI
from jiwer import wer
from dotenv import load_dotenv
import os
import csv

# Load environment variables
load_dotenv()

# Ensure the API key is loaded from .env
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in .env file")
else:
    client = OpenAI()


def speed_up_audio(input_audio_path, output_audio_path, speed_factor):
    """
    Speeds up the audio file by the given factor using ffmpeg-python.
    """
    stream = ffmpeg.input(input_audio_path)
    stream = ffmpeg.filter_(stream, 'atempo', speed_factor)
    stream = ffmpeg.output(stream, output_audio_path)
    ffmpeg.run(stream)

def transcribe_audio(audio_path, language='en'):
    """
    Transcribe the audio file using OpenAI's Whisper API with optional language support.
    """
    with open(audio_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language=language
        )
    return response.text

def calculate_wer(original_text, transcribed_text):
    """
    Calculate the Word Error Rate (WER) between the original and transcribed texts.
    """
    error = wer(original_text, transcribed_text)
    return error

def run_benchmark(audio_path, language='en'):

    # Transcribe the audio at normal speed to get the baseline transcript
    original_transcript = transcribe_audio(audio_path, language)
    print("Original Transcript (1x):", original_transcript)

    results = []
    # Speed factors range from 1.1x to 4x in 0.1x increments
    for speed_factor in [x * 0.1 for x in range(11, 41)]:
        sped_up_audio = f'output/sped_up_{speed_factor:.1f}_audio.mp3'
        speed_up_audio(audio_path, sped_up_audio, speed_factor)

        transcription = transcribe_audio(sped_up_audio, language)
        error_rate = calculate_wer(original_transcript, transcription)
        results.append((speed_factor, error_rate))

    for speed, error in results:
        print(f"Speed Factor: {speed:.1f}x - WER: {error:.2%}")

    # Output results to a CSV file
    with open('benchmark_results.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Speed Factor', 'Word Error Rate'])
        for speed, error in results:
            writer.writerow([f"{speed:.1f}x", f"{error:.2%}"])
    print("Results have been saved to benchmark_results.csv.")

def convert_to_mp3(input_file):
    output_file = 'output/test.mp3'
    """Convert an audio file to a mp3 file using ffmpeg."""
    command = ['ffmpeg', '-i', input_file, output_file]
    subprocess.run(command, check=True)

def main():
    parser = argparse.ArgumentParser(description="Convert audio files to MP3 and run benchmark.")
    parser.add_argument("input_file", type=str, help="The path to the input audio file.")
    parser.add_argument("--language", default="en", type=str, help="two letter Language code for the benchmark. (defaults to English)")
 
    args = parser.parse_args()

    convert_to_mp3(args.input_file)
    run_benchmark('output/test.mp3', language=args.language)

if __name__ == "__main__":
    main()
