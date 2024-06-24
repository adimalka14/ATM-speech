import os
# Imports the Google Cloud client library
from google.cloud import texttospeech
import  sounddevice as sd
import  numpy as np

credential_path = "C:\\Users\\ASUS\\PycharmProjects\\ATMSpeech\\TTS_And_STT_API.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

class TTS():

    def __init__(self):
        self.config =''
        self.client = texttospeech.TextToSpeechClient() # Instantiates a client

    def AskForAmount(self):
        str = 'בבקשה אמור את סכום הכסף אותו הינחה מעוניין למשוך'
        print('בבקשה אמור את סכום הכסף אותו הינך מעוניין למשוך')
        self.tts_request(str)

    def AskForAmountAgain(self):
        str = 'בבקשה אמור שוב את סכום הכסף אותו הינחה מעוניין למשוך'
        print('בבקשה אמור שוב את סכום הכסף אותו הינך מעוניין למשוך')
        self.tts_request(str)

    def ValidteAmount(self,amount):
        str =(f' המערכת זיהתה כי ביקשת למשוך סכום של { amount } שקלים '
              f'האם אתה מאשר את ביצוע הפעולה? ')
        print(str)
        self.tts_request(str)

    def failedRecognizeAmount(self):
        str =('לא הצלחנו לזההות את הסכום המבוקש')
        print(str)
        self.tts_request(str)

    def RequestForIdentification(self):
        str = 'בבקשה אמור את שימחה המלא ולאחר מכן את מספר תעודת הזהות שלחה'
        print('בבקשה אמור את שמך המלא ולאחר מכן את מספר תעודת הזהות שלך')
        self.tts_request(str)

    def OperationSuccessMessage(self):
        str = 'הפעולה התבצעה בהצלחה,הוצא בבקשה את הכרטיס והכסף מייד יגיע אליך!'
        print('הפעולה התבצעה בהצלחה,הוצא בבקשה את הכרטיס והכסף מייד יגיע אלייך!')
        self.tts_request(str)

    def AuthenticationFailed(self):
        str = 'לא הצלחנו לאמת את זהותך, בבקשה אמור שוב את שימחה המלא ולאחר מכן את מספר תעודת הזהות שלחה'
        print('לא הצלחנו לאמת את זהותך, בבקשה אמור שוב את שמך המלא ולאחר מכן את מספר תעודת הזהות שלך')
        self.tts_request(str)

    def AuthenticationSuccess(self):
        str = 'האימות עבר בהצלחה'
        print(str)
        self.tts_request(str)

    def transferredToHumanService(self):
        str = 'הפעולה נכשלה, הינחה מועבר כעת לנציג תמיכה אנושי.'
        print('הפעולה נכשלה, הנך מועבר כעת לנציג תמיכה אנושי')
        self.tts_request(str)

    def doesNotConfirmTheAmount(self):
        str = 'המערכת זיהתה שלא אישרת את הסכום שנקלט'
        print(str)
        self.tts_request(str)

    def tts_request(self, textstring):
        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=textstring)

        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        voice = texttospeech.VoiceSelectionParams(
            language_code="iw-IL",
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
        )

        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        audio_array = np.frombuffer(response.audio_content, dtype=np.int16)

        # Play the audio using sounddevice
        sd.play(audio_array, samplerate=22500)  # Adjust samplerate as needed
        sd.wait()