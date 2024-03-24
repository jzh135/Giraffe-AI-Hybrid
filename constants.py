import os

# Import OpenAI API Key from a file
def read_api_key_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            api_key = file.read().strip()  # Read the content and remove leading/trailing spaces
            return api_key
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None

# Document Directory
SOURCE_DIRECTORY = os.path.join(os.path.dirname(__file__), 'source')
ARCHIVE_DIRECTORY = os.path.join(os.path.dirname(__file__), 'archive')
METADATA_DIRECTORY = os.path.join(ARCHIVE_DIRECTORY, 'metadata')
ARCHIVE_SOURCE_DIRECTORY = os.path.join(ARCHIVE_DIRECTORY, 'source files')
# Audio Directory
AUDIO_ROOT = os.path.join(os.path.dirname(__file__), 'audio_docs')
AUDIO_SOURCE = os.path.join(AUDIO_ROOT, 'audio_source')
TRANSCRIPTION = os.path.join(AUDIO_ROOT, 'transcription')
# Database Directory
DB_DIRECTORY = os.path.join(os.path.dirname(__file__), 'db_en')

# Embeddings Directory
MODEL_ROOT = os.path.join(os.path.dirname(__file__), 'model')
BEG_EN = os.path.join(MODEL_ROOT,'bge-large-en-v1.5')

# OpenAI API Key 
API_KEY_FILE = os.path.join(os.path.dirname(__file__), 'openAI_API.txt')
API_KEY = read_api_key_from_file(API_KEY_FILE)

# Check if essential directories exist
for folder_path in [SOURCE_DIRECTORY, ARCHIVE_DIRECTORY, METADATA_DIRECTORY, ARCHIVE_SOURCE_DIRECTORY, AUDIO_ROOT, AUDIO_SOURCE, TRANSCRIPTION, DB_DIRECTORY, MODEL_ROOT]:
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    else:
        pass

