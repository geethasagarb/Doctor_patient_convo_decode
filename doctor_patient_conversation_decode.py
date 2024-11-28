# -*- coding: utf-8 -*-
"""Doctor_Patient_conversation_decode.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1e5OvbwM1qImsucLhwnNNgNjEbJo8ULpT
"""

#!pip install git+https://github.com/openai/whisper.git
#!pip install groq

import whisper
import os
from groq import Groq

# Set up OpenAI API key
api_key= st.secrets["API_KEY"]
os.environ["OPENAI_API_KEY"] = api_key  # This line sets the environment variable
# Load the Whisper 'large' model for maximum accuracy
print("Loading Whisper model...")
whisper_model = whisper.load_model("base")

# Step 1: Transcribe the audio file
def transcribe_audio(audio_path):
    """
    Transcribes audio using Whisper and returns the text.
    Args:
        audio_path (str): Path to the audio file.
    Returns:
        str: Transcribed text from the audio.
    """
    print(f"Transcribing audio: {audio_path}")
    result = whisper_model.transcribe(audio_path, fp16=False)  # fp16=False for better accuracy
    transcription = result["text"]
    print("Transcription completed.")
    return transcription

# Step 2: Use GPT-4 for medical analysis
def analyze_transcription(transcription):
    """
    Sends the transcription to GPT-4 for medical analysis.
    Args:
        transcription (str): Text from the transcription.
    Returns:
        str: GPT-4's analysis.
    """
    prompt = f"""
    The following is a conversation between a doctor and a patient:
    {transcription}

    Based on this conversation, provide:
    1. A possible prognosis for the patient.
    2. A detailed diagnosis of the condition.
    3. Medication recommendations or treatments for the patient.
    """
    print("Sending transcription to GPT-4...")

    # Updated code to use the new OpenAI client interface
    client = Groq(
    api_key= st.secrets["API_KEY"]
     )
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a medical assistant AI with expertise in prognosis, diagnosis, and medication recommendations."},
            {"role": "user", "content": prompt}
        ]
    )

    analysis = response.choices[0].message.content  # Accessing the content
    print("GPT-4 analysis received.")
    return analysis

# Step 3: Main Workflow
def main(audio_path):
    """
    Main workflow to transcribe audio and analyze the transcription.
    Args:
        audio_path (str): Path to the audio file.
    """
    # Transcribe audio
    transcription = transcribe_audio(audio_path)

    # Save transcription to a file
    with open("transcription.txt", "w") as f:
        f.write(transcription)
        print("Transcription saved to 'transcription.txt'.")

    # Analyze transcription with GPT-4
    analysis = analyze_transcription(transcription)

    # Save analysis to a file
    with open("medical_analysis.txt", "w") as f:
        f.write(analysis)
        print("Medical analysis saved to 'medical_analysis.txt'.")

    # Print results
    print("\nTranscription:\n", transcription)
    print("\nMedical Analysis:\n", analysis)

# Run the main workflow with your audio file
main("doctor_patient_conversation.wav")  # Replace with your audio file path

# Give the initial info like age, name, etc.

# Dosage w.r.t the person or country (check in mg) -
# minimial suggestions should be given unless critical issue
# Age limitation suggestions
# sensitive info
# banned medication

#Doctor line of questioning
#Name
#Age
#GENDER
#SYMPTOMS
