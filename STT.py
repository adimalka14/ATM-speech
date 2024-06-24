import os
from google.cloud import speech

credential_path = "C:\\Users\\ASUS\\PycharmProjects\\ATMSpeech\\TTS_And_STT_API.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

class STT():
    def __init__(self):
        self.config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=22050,
            language_code="iw-IL",
            #language_code="en-US",
        )
        self.client = speech.SpeechClient()

    def recognize(self, audio_data):
        audio_content = audio_data.frame_data
        audio = speech.RecognitionAudio(content=audio_content)
        response_text = ''

        try:
            response = self.client.recognize(config=self.config, audio=audio)
            for result in response.results:
                response_text += result.alternatives[0].transcript
        except Exception as e:
            print('Something wrong with recognition:', e)

        return response_text