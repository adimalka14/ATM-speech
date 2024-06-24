import pveagle
from pvrecorder import PvRecorder
import pickle
import os
import time

DEFAULT_DEVICE_INDEX = -1
save_path = r"C:\Users\ASUS\PycharmProjects\ATMSpeech\speakers profilers\profiles_data.pkl"
with open(r"C:\Users\ASUS\PycharmProjects\ATMSpeech\pico_voice_key.txt", "r") as file:
          access_key = file.read().strip()

def enroll_speaker(access_key, device_index=DEFAULT_DEVICE_INDEX):
    try:
        eagle_profiler = pveagle.create_profiler(access_key=access_key)
    except pveagle.EagleError as e:
        print(f"Error creating profiler: {e}")
        return

    enroll_recorder = PvRecorder(
        device_index=device_index,
        frame_length=eagle_profiler.min_enroll_samples)

    enroll_recorder.start()
    print("Start enrollment")


    enroll_percentage = 0.0
    while enroll_percentage < 100.0:
        print(enroll_percentage)
        audio_frame = enroll_recorder.read()
        enroll_percentage, feedback = eagle_profiler.enroll(audio_frame)

    print("Finish enrollment")
    enroll_recorder.stop()

    speaker_p=eagle_profiler.export()


    enroll_recorder.delete()
    eagle_profiler.delete()
    return speaker_p


if os.path.exists(save_path):
    with open(save_path, 'rb') as f:
        dict = pickle.load(f)
    # Rest of your code
else:
    print(f"The file {save_path} does not exist.")

cd_num = input("Enter your credit card number:")

# Uncomment the following lines to enroll and then recognize the speaker
speaker_p=enroll_speaker(access_key)
speaker_b=speaker_p.to_bytes()
dict[cd_num]=speaker_b

with open(save_path, 'wb') as f:
    pickle.dump(dict, f)