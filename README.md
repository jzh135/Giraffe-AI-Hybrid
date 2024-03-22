# Giraffe AI Hybrid
## Installation Guide
### 1. Build environment
#### 1.1 Download and install Anaconda from https://www.anaconda.com/
#### 1.2 Create and activate python (version 3.10.0) virtual environment
```
conda create -n GiraffeAI python=3.10.0
conda activate GiraffeAI
```
### 2. Setup Giraffe AI
#### 2.1 Install all required libraries from requirement.txt
```
pip install -r requirement.txt
```
#### 2.2 Constants 
Change "Your API KEY" to your OpenAI API Key
#### 2.3 Embeddings
1. Create a new folder and rename it to "model"
2. Download bge-large-en-v1.5 to the *model* folder using following command:
```
git clone https://huggingface.co/BAAI/bge-large-en-v1.5
```
### 3. Launch Giraffe AI
Run Giraffe_AI_launcher.py in your virtual environment

