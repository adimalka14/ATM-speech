import pveagle
from pvrecorder import PvRecorder
import pickle
import time

class Speaker_Recognition():
        def __init__(self):
            self.DEFAULT_DEVICE_INDEX = -1
            with open(r"C:\Users\ASUS\PycharmProjects\ATMSpeech\pico_voice_key.txt", "r") as file:
                self.access_key = file.read().strip()
            self.save_path = r"C:\Users\ASUS\PycharmProjects\ATMSpeech\speakers profilers\profiles_data.pkl"

        def recognize_speaker(self, credit_card_number) :
            # Load user data from PKL
            with open(self.save_path, 'rb') as f:
                loaded_data = pickle.load(f)

            speaker_profile_b = loaded_data[credit_card_number]

            try:
                speaker_profile_p = pveagle.EagleProfile.from_bytes(speaker_profile_b)

            except pveagle.EagleError as e:
                print(f"Error creating profiler: {e}")
                #print(speaker_profile_p)

            try:
                eagle = pveagle.create_recognizer(
                        access_key=self.access_key,
                        speaker_profiles=[speaker_profile_p])
            except pveagle.EagleError as e:
                print(f"Error creating recognizer: {e}")
                return

            recognizer_recorder = PvRecorder(
                        device_index=self.DEFAULT_DEVICE_INDEX,
                        frame_length=eagle.frame_length)

            recognizer_recorder.start()

            desired_duration = 10
            start_time = time.time()
            print("start recognition")
            scores_list = []

            while time.time() - start_time < desired_duration:
                audio_frame = recognizer_recorder.read()
                scores_list.append(eagle.process(audio_frame))

            print("stop recognition")
            scores_list = [score for scores in scores_list for score in scores if score > 0]
            print(scores_list)
            if scores_list:
                max_score = max(scores_list)
                average_score = sum(scores_list) / len(scores_list)
                sum_scores=sum(i > 0.8 for i in scores_list)
                print(f"Sum scores that bigger than 0.8 : {sum_scores}")
                print(f"Max Score: {max_score}")
                print(f"Average Score: {average_score}")
                is_recognize=average_score>0.7 and sum_scores>70
            else:
                print("No detection during the specified duration.")
                is_recognize = False
            recognizer_recorder.stop()
            recognizer_recorder.delete()
            eagle.delete()
            return is_recognize