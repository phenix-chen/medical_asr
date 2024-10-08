import os
import sys
from typing import Optional

from funasr import AutoModel
from xpinyin import Pinyin

from medical_asr.download import check_or_download_models


class HotwordCorrect:
    def __init__(self, hotword_file: str) -> None:
        self.parser = Pinyin()
        self.std_hotwords = self.read_hotword_file(hotword_file)
        self.std_pinyins = [self.parser.get_pinyin(hw) for hw in self.std_hotwords]

    def read_hotword_file(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            hotwords = f.readlines()
        hotwords = [hw.strip() for hw in hotwords]
        return hotwords

    def correct(self, input_string: str):
        chars = list(input_string)
        pinyin = self.parser.get_pinyin(input_string)
        result = ""
        for std_pinyin, std_hotword in zip(self.std_pinyins, self.std_hotwords):
            if std_pinyin in pinyin:
                idx = pinyin.index(std_pinyin)
                front_pinyin = pinyin[:idx]
                len_front_chars = len(front_pinyin.split("-")[:-1])
                len_word = len(std_hotword)
                change_idx = len_front_chars
                chars[change_idx: change_idx + len_word] = list(std_hotword)
                result = "".join(chars)
        if result != "":
            return result
        else:
            return input_string


class SeacoASRModel:
    def __init__(self, hotword_file: Optional[str] = None, model_dir: Optional[str] = None) -> None:
        print("hotword_file: ", hotword_file)
        self.hotword_str = ""
        if sys.platform == "win32":
            with open(hotword_file, "r", encoding="utf-8") as f:
                content = f.readlines()
                self.hotword_str = " ".join(line.strip() for line in content)

        if model_dir is None:
            home = os.path.expanduser("~")
            model_dir = os.path.join(home, ".cache/modelscope/hub")

        model, vad = check_or_download_models(model_dir)
        self.asr_model = AutoModel(
            disable_pbar=True,
            model=model,
            model_revision="v2.0.4",
        )
        self.vad_model = AutoModel(model=vad, model_revision="v2.0.4", max_end_silence_time=800, speech_noise_thres=0.9)
        self.chunk_size = 60
        self.frames = []
        self.cache = {}
        self.start_chunk_num = 0
        self.pre_chunk_num = 60

        self.hotword_corrector = HotwordCorrect(hotword_file) if hotword_file else None

    def vad(self, audio_in: bytes, is_final=False):

        res = self.vad_model.generate(
            input=audio_in,
            disable_pbar=True,
            disable_log=True,
            cache=self.cache,
            is_final=is_final,
            chunk_size=self.chunk_size,
        )
        if len(res[0]["value"]):
            return res[0]["value"][0]
        else:
            return 0, 0

    def asr(self, audio_in) -> str:
        rec_result = self.asr_model.generate(
            audio_in,
            hotword=self.hotword_str,
        )
        return rec_result[0]

    def recognize(self, message: bytes) -> str:
        self.frames.append(message)
        start, end = self.vad(message)

        if start > self.pre_chunk_num:
            self.start_chunk_num = int((start - self.pre_chunk_num) * 16000 / 1000 * 2)

        if end > 0:
            audio_in = b"".join(self.frames)
            end_chunk_num = int(end * 16000 / 1000 * 2)
            speech_chunk = audio_in[self.start_chunk_num:end_chunk_num]

            result = self.asr(speech_chunk)
            self.cache = {}
            self.frames = []
            text = "".join(result["text"].split())

            if self.hotword_corrector:
                text = self.hotword_corrector.correct(text)

            self.start_chunk_num = 0
            return text
        return ""
