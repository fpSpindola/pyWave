from pywave import PyWave
from pywave.recognize import FileRecognizer, MicrophoneRecognizer
import warnings
import json
warnings.filterwarnings("ignore")

# load config from a JSON file (or anything outputting a python dictionary)
with open("pywave.cnf.SAMPLE") as f:
    config = json.load(f)

if __name__ == '__main__':

    # create a Dejavu instance
    djv = PyWave(config)

    # Fingerprint all the mp3's in the directory we give it
    djv.fingerprint_directory("mp3", [".mp3"])

    # Recognize audio from a file
    song = djv.recognize(FileRecognizer, "mp3/Sean-Fournier--Falling-For-You.mp3")
    print(f"From file we recognized: {song}")

    # Or recognize audio from your microphone for `secs` seconds
    secs = 5
    song = djv.recognize(MicrophoneRecognizer, seconds=secs)
    if song is None:
        print("Nothing recognized -- did you play the song out loud so your mic could hear it? :)")
    else:
        print(f"From mic with {secs} seconds we recognized: {song}")

    # Or use a recognizer without the shortcut, in anyway you would like
    recognizer = FileRecognizer(djv)
    song = recognizer.recognize_file("mp3/Josh-Woodward--I-Want-To-Destroy-Something-Beautiful.mp3")
    print(f"No shortcut, we recognized: {song}")