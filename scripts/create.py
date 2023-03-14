import json
from os import makedirs, listdir
from os.path import dirname, isfile
from time import sleep
from ovos_plugin_manager.tts import load_tts_plugin

WW_CFGS = f"auto_synth/ww_configs"
VOICES_BASE = f"auto_synth/tts_voices"
OUTPUT_BASE = f"auto_synth/synth_data"

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

        try:
            engine = load_tts_plugin(m)(config=cfg)
            wav_file = f"{OUTPUT_FOLDER}/{voice.replace('.json', f'.{engine.audio_ext}')}"
            if isfile(wav_file):
                continue
            engine.get_tts(WW, wav_file)
            if "server" in voice:
                sleep(1)  # do not overload public servers
        except:
            # bad plugin, oopsie
            continue