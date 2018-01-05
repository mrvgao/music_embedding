import numpy as np
from functools import lru_cache
from utilities import search_nearest
from scipy.io import wavfile as wav
from collections import Counter
from multiprocessing import Pool
import multiprocessing
from functools import reduce
from itertools import repeat
from utilities import chunks


wav_max = 25000
wav_min = -wav_max
linespace = np.linspace(start=wav_min, stop=wav_max, num=3000)


@lru_cache(maxsize=1024*16)
def get_music_notation(value):
    return search_nearest(value, linespace)


v_func = np.vectorize(get_music_notation)


def change_file_batches(file_batches, token_file_path, test_mode=False):
    vocabulary = Counter()
    sample_num = 200
    for f in file_batches:
        vocabulary += change_wav_to_sampling_discrete(f, token_file_path, sample_num, test_mode)
    return vocabulary


def change_wav_to_sampling_discrete(wav_file, tokens_file_path, sampling_num=1, test_mode=False):
    original_file_name = wav_file
    rate, data = wav.read(original_file_name)
    datas = np.array_split(data, sampling_num)

    vocabulary_counter = Counter()

    for i in range(sampling_num):
        print('processing --- {} -- {}/{}'.format(wav_file, i+1, sampling_num))
        if test_mode and i >= 2: break

        discrete_data = v_func(datas[i])
        discrete_data = discrete_data.astype(np.int32)
        # file_name = 'dataset/discretes/' + ''.join(wav_file.split('.')[:-1]).replace('dataset/', '') + '_sample_{}'.format(i) + '.wav'
        # wav.write(data=discrete_data, rate=rate, filename=file_name)

        discrete_data = list(map(tuple, list(discrete_data)))
        with open(tokens_file_path, 'a') as f:
            f.write('\n')
            for data in discrete_data:
                f.write(str(data).replace(' ', '') + ' ')

        vocabulary_counter.update(discrete_data)

    return vocabulary_counter


def reduce_merge_result(v1, v2):
    return v1 + v2



def run_multiply_process(files, tokens_path, test_mode=False, cpu_number=None):
    if cpu_number is None:
        cpu_number = multiprocessing.cpu_count()

    results = Pool(processes=cpu_number).starmap(change_file_batches, zip(chunks(files, cpu_number), repeat(tokens_path), repeat(test_mode)))
    result = reduce(reduce_merge_result, results, Counter())

    return result


def get_discrete_data(files, token_path, test_mode=False, multiply_process_num=None):
    result = run_multiply_process(files, token_path, test_mode, multiply_process_num)
    return result


if __name__ == '__main__':
    # change_wav_to_sampling_discrete('Richard Clayderman - 水边的阿狄丽娜.wav', sampling_num=5)

    # Pool.map(change_file_batches, )

    files = ['dataset/DDBY - 近く远い斜め色の空.wav', 'dataset/Richard Clayderman - 水边的阿狄丽娜.wav']
    # files = glob.glob('/Users/Minchiuan/Music/网易云音乐/*')
    # files = glob('Vladimir Ashkenazy - Frédéric Chopin： Mazurka No.41 in C sharp minor Op.63 No.3.mp3')
    result = change_file_batches(files)

    # results = Pool(processes=cpu_count).map(change_file_batches, chunks(files, cpu_count))
    # result = reduce(reduce_merge_result, results, Counter())

    print(len(result))

