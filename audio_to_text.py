import os
import time
import datetime
import json

import whisper

from constants import AUDIO_SOURCE, TRANSCRIPTION

model = whisper.load_model("base").to(device="cuda")

def transcribe(source_directory, transcription_directory):
    for root, _, files in os.walk(source_directory):
        for file in files:
            file_name = os.path.splitext(file)[0]
            source_file_path = os.path.join(root, file)
            transcription = model.transcribe(source_file_path)
            print(transcription)
            current_date = datetime.date.today()

            trans_file_path = os.path.join(transcription_directory,file_name+".txt")
            with open(trans_file_path, "w", encoding="utf-8") as file:
                file.write(transcription["text"])

# Test code
#transcribe(source_directory=AUDIO_SOURCE,transcription_directory=TRANSCRIPTION)