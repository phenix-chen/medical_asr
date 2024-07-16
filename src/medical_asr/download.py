import os.path
from typing import Tuple


def check_or_download_models(models_dir: str = "./models") -> Tuple[str, str]:
    asr_model = f"iic/speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch"
    vad_model = f"iic/speech_fsmn_vad_zh-cn-16k-common-pytorch"
    asr_path = f"{models_dir}/{asr_model}"
    vad_path = f"{models_dir}/{vad_model}"

    if not os.path.exists(asr_path):
        from modelscope.hub.snapshot_download import snapshot_download
        snapshot_download(asr_model, cache_dir=models_dir, revision='v2.0.4')
    if not os.path.exists(vad_path):
        from modelscope.hub.snapshot_download import snapshot_download
        snapshot_download(vad_model, cache_dir=models_dir, revision='v2.0.4')
    return asr_path, vad_path
