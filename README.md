# Giraffe AI Hybrid
🦒 Welcome to Giraffe AI Hybrid! 🦒
I’m your trusty digital giraffe here to assist you with precision and accuracy. 
As a RAG system, I rely on our local database to provide spot-on answers to your queries. Whether it’s facts, trivia, or practical advice, I’ve got it covered!
Let’s explore the vast savanna of knowledge together! 🌟🦒<br>
<p>
  RAM: 1.3 GB
</p>
## Installation Guide
### 1. Build environment
#### 1.1 Download and install Anaconda from https://www.anaconda.com/
#### 1.2 Create and activate python (version 3.10.0) virtual environment
```
conda create -n GiraffeAI python=3.10.0
conda activate GiraffeAI
```
### 2. Setup Giraffe AI
#### 2.1 Install all required libraries from requirements.txt
```
pip install -r requirements.txt
```
#### 2.2 LLM API 
Create a .txt file in the current directory with your OpenAI API Key, rename the file to *openAI_API.txt*
#### 2.3 Embeddings
1. Create a new folder and rename it to "model"
2. Download bge-large-en-v1.5 to the *model* folder using following command:
```
git clone https://huggingface.co/BAAI/bge-large-en-v1.5
```
### 3. Launch Giraffe AI
Run Giraffe_AI_launcher.py in your virtual environment
```
python Giraffe_AI_launcher.py
```
## Development Log
### Version 1.0 (3/22/2024)
#### 1.0.0: initial release (3/22/2024)
- Databse: Chroma
- Record management: document upload and replacement
- Source document format: .pdf/.txt
- Embeddings: bge-large-en-v1.5
- LLM: OpenAI GPT3.5-turbo
#### 1.0.1: minor updates (3/23/2024)
- Add directory checker
- Import OpenAI API Key from a file
- DB builder will skip unsupported files
- Once source file is loaded, it will be removed from the source folder and moves to the archive folder
