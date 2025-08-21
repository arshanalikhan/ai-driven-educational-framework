import speech_recognition as sr
from transformers import pipeline

class MultilingualVoiceInterface:
    """
    Voice interface supporting multiple languages for educational accessibility
    """
    def __init__(self, model_name="openai/whisper-base.en"):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.asr_pipeline = pipeline("automatic-speech-recognition",
                                     model=model_name)
    
    def listen_for_speech(self, timeout=5):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source, timeout=timeout)
            return audio
    
    def speech_to_text(self, audio_data):
        wav = audio_data.get_wav_data()
        result = self.asr_pipeline(wav)
        return result['text']
