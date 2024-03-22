import os

# Source Document Directory
SOURCE_DIRECTORY = os.path.join(os.path.dirname(__file__), 'source')
SINGLE_SOURCE = os.path.join(os.path.dirname(__file__), 'source', 'Severe mental illness across cultures.pdf') 

# Database Directory
DB_DIRECTORY = os.path.join(os.path.dirname(__file__), 'db_en')

# Embeddings Directory
BEG_EN = os.path.join(os.path.dirname(__file__), 'model','bge-large-en-v1.5')

# OpenAI API Key 
API_KEY = r"Your API Key"
