import os
import time
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

    # Recognize audio from a file
    song = djv.recognize(FileRecognizer, "mp3/Sean-Fournier--Falling-For-You.mp3")
    print(f"From file we recognized: {song}")

    # # Or use a recognizer without the shortcut, in anyway you would like
    # recognizer = FileRecognizer(djv)
    # song = recognizer.recognize_file("mp3/pruprupru.mp3")
    # print(f"No shortcut, we recognized: {song}")
