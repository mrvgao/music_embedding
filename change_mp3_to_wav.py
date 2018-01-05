from pydub import AudioSegment
from multiprocessing import Pool
from utilities import chunks
from functools import reduce


def change_ext(file_name, new_ext):
    return ''.join(file_name.split('.')[:-1]) + '.' + new_ext


def change_file_to_wav(file_paths):

    new_file_names = []

    for f in file_paths:
        sound = AudioSegment.from_mp3(f)
        new_f = change_ext(f, 'wav')
        print('converting {} ==> {}'.format(f, new_f))
        sound.export(new_f, format='wav')
        new_file_names.append(new_f)

    return new_file_names


def merge_results(r1, r2):
    return r1 + r2


def change_file_batches_to_wav(files, cpu_num):
    file_chunks = chunks(files, cpu_num)

    results = Pool(cpu_num).map(change_file_to_wav, file_chunks)

    result = reduce(merge_results, results, [])

    return result


assert change_ext('file.txt', 'wav') == 'file.wav'

if __name__ == '__main__':
    files = ['dataset/王迟 - 葫芦金刚.mp3', 'dataset/Nick Cave - To Be By Your Side.mp3']

    wav_files = []
    for f in files:
        wav_f = change_file_to_wav(f)
        wav_files.append(wav_f)

    print(wav_files)
