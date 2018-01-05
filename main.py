import glob
from change_mp3_to_wav import change_file_to_wav
from random_sampling_wav import change_file_batches
import pickle


def parse_config(conf_path):
    config = {}
    with open(conf_path, 'r', encoding='utf-8') as f:
        for line in f:
            splited = line.strip().split(':')
            if len(splited) >= 2:
                config[splited[0]] = splited[1].strip()
    return config


config = parse_config('main.conf')
mp3_src_pattern = config['map3_src']
token_file_path = config['token_path']
pickle_path = config['pickle_path']

mp3_files = glob.glob(mp3_src_pattern)
wav_files = map(change_file_to_wav, mp3_files)
result = change_file_batches(wav_files, token_file_path)

with open(pickle_path, 'wb') as f:
    pickle.dump(result, f)

print('length of vocabulary is {}'.format(len(result)))

print('pickle finish!')
