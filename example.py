import os
import warnings
import ujson as ujson
from pywave import PyWave
from pywave.recognize import FileRecognizer, MicrophoneRecognizer
from pywave.config import Config
warnings.filterwarnings("ignore")

if __name__ == '__main__':

    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    if os.path.exists(config_path):
        with open(config_path) as c:
            loaded_config = Config(ujson.loads(c.read()))
            Config.current = loaded_config
    else:
        raise Exception('Please create the config file at: {}'.format(config_path))

    # create a Dejavu instance
    djv = PyWave(loaded_config)

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
