from pydub import AudioSegment


def change_ext(file_name, new_ext):
    return ''.join(file_name.split('.')[:-1]) + '.' + new_ext


def change_file_to_wav(file_path):
    sound = AudioSegment.from_mp3(file_path)

    new_file_name = change_ext(file_path, 'wav')
    print('converting {} ==> {}'.format(file_path, new_file_name))

    sound.export(new_file_name, format='wav')

    return new_file_name


assert change_ext('file.txt', 'wav') == 'file.wav'

if __name__ == '__main__':
    files = ['dataset/王迟 - 葫芦金刚.mp3', 'dataset/Nick Cave - To Be By Your Side.mp3']

    wav_files = []
    for f in files:
        wav_f = change_file_to_wav(f)
        wav_files.append(wav_f)

    print(wav_files)
