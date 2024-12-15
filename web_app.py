import streamlit as st
import azure.cognitiveservices.speech as speechsdk
import wave
import os
import tempfile
from dotenv import load_dotenv

load_dotenv()

# Azure credentials (replace with your actual keys and region)
subscription_key = os.getenv("AZURE_SUB_KEY")
region = "East US"

# Function for Speech-to-Text using Azure ASR
def recognize_speech_from_microphone(region, subscription_key):
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    st.write("Say something...")

    # Start continuous recognition from the microphone
    result = speech_recognizer.recognize_once()
    
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return "No speech could be recognized"
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        return f"Speech Recognition canceled: {cancellation_details.reason}"

# Function for Text-to-Speech using Azure TTS
def text_to_speech(text, region, subscription_key):
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
    
    # No use_default_speaker argument needed here
    audio_config = speechsdk.audio.AudioConfig()  # Output to default speaker by default
    
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    synthesizer.speak_text_async(text)

def main():
    st.title("Live Speech-to-Text with Azure ASR and TTS")

    # Start live speech recognition when the button is clicked
    if st.button('Start Recording'):
        st.write("Listening...")
        
        # Recognize speech from the microphone
        text = recognize_speech_from_microphone(region, subscription_key)
        
        # Display the recognized text
        st.write("Your message (transcribed):")
        st.write(text)
        
        # Send the text to your chatbot here, and get the summary (mock response in this case)
        summary = f"Actionable Summary: {text}"  # Example summary
        
        # Convert the summary text to speech using Azure TTS
        st.write("Speaking the summary...")
        text_to_speech(summary, region, subscription_key)
        st.write("The summary has been spoken.")

if __name__ == "__main__":
    main()