# Yap Scribe

This is a project where I attempt to replicate the functionality of Wispr flow,
with the benefit being that the entire application runs locally.

## Setup and Instructions

### Ollama

For this project to work, you must download Ollama, as well as Qwen3_4b-q4-K-M model.
Link: <https://ollama.com/> for download. Once installed, start the Ollama application and go to your terminal, where you should then run:

```bash
ollama run Qwen3_4b-q4-K-M
```

### Rest of Project

After setting up Ollama, you can now get started on setting up the rest of the application. 

Start by setting up the python virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Then install all of the required packages from the requirements.txt file:

```bash
pip install -r requirements.txt
```

Now you give your coding IDE access to the microphone and computer control so that it is able to type for you.

Then you will be able to run the main script:

```bash
python main.py
```

The application should take a moment to start up, but when you see

```bash
Waiting for left alt/option key press
```

the script is running, press and hold left alt/option to start transcription, once transcription and text cleanup is finished, the script will type your transcribed text into the focused text area. Qwen will take a few extra seconds to startup on the first transcription.

Enjoy!

Made by - Jayden Plytas
