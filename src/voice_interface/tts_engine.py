import pyttsx3

class TextToSpeechEngine:
    """
    Text-to-speech engine for multilingual output
    """
    def __init__(self):
        self.engine = pyttsx3.init()
    
    def speak(self, text, rate=150, voice_id=None):
        self.engine.setProperty('rate', rate)
        if voice_id:
            self.engine.setProperty('voice', voice_id)
        self.engine.say(text)
        self.engine.runAndWait()
