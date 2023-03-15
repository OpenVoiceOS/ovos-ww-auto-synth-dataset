import json
from os import makedirs, listdir
from os.path import dirname, isfile
from time import sleep
from ovos_plugin_manager.tts import load_tts_plugin

WW_CFGS = f"{dirname(dirname(__file__))}/ww_configs"
VOICES_BASE = f"{dirname(dirname(__file__))}/tts_voices"
OUTPUT_BASE = f"{dirname(dirname(__file__))}/synth_data"

engines = {}

for cfg in listdir(WW_CFGS):
    with open(f"{WW_CFGS}/{cfg}") as f:
        CONF = json.load(f)
    
    LANG = CONF.get("lang", "en-us")
    WW = CONF["name"]
    VOICE_IDS = CONF.get("tts_voices") or []

    VOICES_FOLDER = f"{VOICES_BASE}/{LANG}"
    OUTPUT_FOLDER = f"{OUTPUT_BASE}/{WW.lower().replace(' ', '_')}"
    makedirs(OUTPUT_FOLDER, exist_ok=True)

    for voice in VOICE_IDS:
        cfg = f"{VOICES_FOLDER}/{voice}"
        if not isfile(cfg):
            continue
        with open(cfg) as f:
            cfg = json.load(f)
        m = cfg.pop("module")

        if m in engines:
            engine = engines[m]
        else:
            engine = engines[m] = load_tts_plugin(m)(config=cfg)
        wav_file = f"{OUTPUT_FOLDER}/{voice.replace('.json', f'.{engine.audio_ext}')}"
        if isfile(wav_file) or isfile(wav_file + ".wav"):  # handle converted mp3 files
            continue
        print(wav_file)
        kwargs = {}
        if "speaker" in cfg:
            kwargs["speaker"] = cfg["speaker"]
        if "voice" in cfg:
            kwargs["voice"] = cfg["voice"]
        engine.get_tts(WW, wav_file, **kwargs)
        if "server" in voice:
            sleep(1)  # do not overload public servers