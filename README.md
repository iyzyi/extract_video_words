# 视频语音转文字小工具

将目标视频分割成58秒一段的PCM格式的音频，然后借助百度API实现音频转文字。

（我妈居然对照视频逐一打字记录，好麻烦的，简单做了这个小工具，让她体验一下科技的力量o.O）

## 环境

```
pip install baidu-aip
pip install chardet
pip install ffmpy
pip install pydub
```

## 使用

1. 将`extract_video_words.py`中的`APP_ID`, `APP_KEY`, `SECRET_KEY`修改成你的（不知道这是啥的可以访问https://cloud.baidu.com/doc/SPEECH/s/Jlbxdezuf 查阅并创建）
2. 运行`run_me.bat`或`extract_video_words.py`
3. 识别结果保存到目标视频所在目录下。

## 费用

百度的这个短音频转文字的API有免费额度，半年且不超过15万次调用，对于普通人来说完全够用了。