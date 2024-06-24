import STT as stt
import TTS as tts
import speech_recognition as sr
import Speaker_Recognition
import re

def recognize_speech(timeout):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(sample_rate=22050)  # Adjust sample rate as needed
    print('start')

    with microphone as source:
        audio_data = recognizer.listen(source, timeout=timeout)
    print('finish')
    return audio_data

if __name__ == '__main__':
    tts = tts.TTS()
    stt = stt.STT()
    sp_r=Speaker_Recognition.Speaker_Recognition()

    credit_card_number = input("הכנס את כרטיס האשראי שלך:")

    tts.RequestForIdentification()
    max_attempts = 3
    attempts = 1
    is_recognize = False
    is_operation_succeeded = False

    while attempts <= max_attempts and not is_recognize:
        is_recognize = sp_r.recognize_speaker(credit_card_number)
        if not is_recognize and attempts!=max_attempts:
            tts.AuthenticationFailed()
        attempts += 1

    if is_recognize:
        tts.AuthenticationSuccess()
        tts.AskForAmount()
        attempts=1
        while attempts <= max_attempts:
            audio_data = recognize_speech(10.0)
            string = stt.recognize(audio_data)
            numbers_only = re.sub(r'\D', '', string)

            try:
                number = int(numbers_only)
                tts.ValidteAmount(numbers_only)
                audio_data=recognize_speech(5.0)
                string = stt.recognize(audio_data)
                if 'כן' in string or 'מאשר' in string and 'לא' not in string:
                    is_operation_succeeded = True
                    break
                else:
                    tts.doesNotConfirmTheAmount()
            except ValueError:
                tts.failedRecognizeAmount()
            tts.AskForAmountAgain()
            attempts += 1

    if is_operation_succeeded:
        tts.OperationSuccessMessage()
    else:
        tts.transferredToHumanService()