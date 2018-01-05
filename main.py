import glob
from change_mp3_to_wav import change_file_to_wav
from random_sampling_wav import change_file_batches
import pickle

mp3_src_pattern = "/Users/Minchiuan/PycharmProjects/MusicEmbedding/dataset/mini_test/*.mp3" # xxx/xxx/*.mp3

token_file_path = ""

mp3_files = glob.glob(mp3_src_pattern)

wav_files = map(change_file_to_wav, mp3_files)

result = change_file_batches(wav_files)

with open('music_vocabulary.pickle', 'wb') as f:
    pickle.dump(result, f)

print('length of vocabulary is {}'.format(len(result)))

print('pickle finish!')




