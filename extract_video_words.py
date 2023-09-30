from aip import AipSpeech               # pip install baidu-aip     # pip install chardet
import ffmpy
from pydub import AudioSegment as pd
import os, math, shutil


def time2str(time_len):
    time_len = math.ceil(time_len)
    hours = time_len // 3600 
    time_len %= 3600
    mins = time_len // 60     
    time_len %= 60
    seconds = time_len        

    def int2str(x):
        return '0' + str(x) if x < 10 else str(x)
    return '{}:{}:{}'.format(int2str(hours), int2str(mins), int2str(seconds))


def call_api(APP_ID, API_KEY, SECRET_KEY, audio_path, output_file):
    # https://cloud.baidu.com/doc/SPEECH/s/Jlbxdezuf
    # 调用百度aip 实现语音识别，对音频文件的要求如下：
    # 1、支持音频格式：pcm、wav、amr、m4a
    # 2、音频编码要求：采样率 16000、8000，16 bit 位深，单声道
    # 3、音频时长不超过 60 秒

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    with open(audio_path, 'rb') as fp:
        audio = fp.read()

    # pcm格式，16000采样频率，1537表示普通话。
    res = client.asr(audio, 'pcm', 16000, {'dev_pid': 1537})

    if res['err_no'] != 0:
        print('接口错误:', res)
        output_file.write('接口错误: %s\n\n' % str(res))
    else:
        result = ''.join(res['result'])
        print('识别结果: ', result)
        output_file.write(result)
        output_file.write('\n\n')


def extract_video_words(APP_ID, API_KEY, SECRET_KEY, video_path):
    if not os.path.exists(video_path):
        print('文件 %s 不存在')
        return False

    dir_path = os.path.dirname(video_path)
    temp_dir_path = os.path.join(dir_path, '__temp')
    if not os.path.exists(temp_dir_path):
        os.makedirs(temp_dir_path)
    file_prefix = os.path.splitext(os.path.basename(video_path))[0]
    output_path = os.path.join(dir_path, file_prefix + '.txt')
    output_file = open(output_path, 'w')

    segments = pd.from_file(video_path)
    time_len = len(segments) / 1000             # seconds
    
    print('Input Vedio:     %s' % video_path)
    print('Time Len:        %s' % time2str(time_len))

    split_len = 58
    for i in range(0, math.ceil(time_len), split_len):
        s = time2str(i)
        t = str(split_len)          # 是len，而非end (-to选项对应的是end)

        temp_audio_path = os.path.join(temp_dir_path,  file_prefix + '__%d.pcm' % (i / split_len))

        # demo: ffmpeg -y -i input.mp4 -acodec pcm_s16le -f s16le -ac 1 -ar 16000 -ss 00:00:00 -t 00:00:59 output.pcm
        ff = ffmpy.FFmpeg(
            inputs = {video_path: [
                '-ss',          s,
                '-t',           t,
                '-accurate_seek',
            ]},
            outputs = {temp_audio_path : [
                '-loglevel',    'quiet',
                '-y',
                '-acodec',      'pcm_s16le',
                '-f',           's16le',
                '-ac',          '1',
                '-ar',          '16000',
            ]}
        )
        ff.run()
        #print(ff.cmd)

        if os.path.exists(temp_audio_path) and os.path.getsize(temp_audio_path) > 0:
            print('Split Audio:     %s' % temp_audio_path)
            call_api(APP_ID, API_KEY, SECRET_KEY, temp_audio_path, output_file)

    shutil.rmtree(temp_dir_path)
    print('Delete Temp:     %s' % temp_dir_path)

    output_file.close()
    print('提取完成，导出文件: %s' % output_path)
    print('自动打开识别结果......')
    os.system(output_path)



if __name__ == '__main__':
    APP_ID = ''
    API_KEY = ''
    SECRET_KEY = ''

    if APP_ID == '' or API_KEY == '' or SECRET_KEY == '':
        raise Exception("Error API Key!")

    #video_path = r'D:\桌面\4bdd54a7f8cec13c3dc47d468b4a3b27.mp4'
    video_path = input('视频语音转文字小工具\n请输入视频路径: ')
    if video_path[0] == '"' and video_path[-1] == '"':
        video_path = video_path[1:-1]
    extract_video_words(APP_ID, API_KEY, SECRET_KEY, video_path)