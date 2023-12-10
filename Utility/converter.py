import os
import shutil, librosa
from .utility import ROOTPATH

def remove():
    temp_path = f"{ROOTPATH}/temp_audio"
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)

def get_lenght(audio) -> int:
    return librosa.get_duration(path=audio)

def full_lenght():
    temp_path = f"{ROOTPATH}/temp_audio"
    dir_list = os.listdir(temp_path)
    durations = [get_lenght(f'{temp_path}/{i}') for i in dir_list]
    total_length = sum(durations)
    return durations, total_length, len(dir_list)