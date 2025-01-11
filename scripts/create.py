import json
import os
import random
from os import makedirs, listdir
from os.path import dirname, isfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from ovos_plugin_manager.tts import load_tts_plugin

WW_CFGS = f"{dirname(dirname(__file__))}/ww_configs"
VOICES_BASE = f"{dirname(dirname(__file__))}/tts_voices"
OUTPUT_BASE = f"{dirname(dirname(__file__))}/synth_data"

engines = {}


def process_voice(WW, voice, LANG, OUTPUT_FOLDER, VOICES_FOLDER):
    voice_cfg = f"{VOICES_FOLDER}/{voice}"
    if not isfile(voice_cfg):
        return
    with open(voice_cfg) as f:
        voice_data = json.load(f)

    m = voice_data.pop("module")
    if m in engines:
        engine = engines[m]
    else:
        clazz = load_tts_plugin(m)
        if clazz is None:
            print(f"Plugin not installed: {m}")
            return
        try:
            engine = engines[m] = clazz(config=voice_data)
        except Exception as e:
            print(f"Failed to load plugin {m}: {e}")
            return

    wav_file = f"{OUTPUT_FOLDER}/{voice.replace('.json', f'.{engine.audio_ext}')}"
    if isfile(wav_file) or isfile(wav_file + ".wav"):  # Handle converted MP3 files
        return

    print(wav_file)
    kwargs = {"lang": LANG}
    if "speaker" in voice_data:
        kwargs["speaker"] = voice_data["speaker"]
    if "voice" in voice_data:
        kwargs["voice"] = voice_data["voice"]

    if not os.path.isfile(wav_file):
        try:
            engine.get_tts(WW, wav_file, **kwargs)
        except Exception as e:
            print(f"Synthesis failed for {wav_file}: {e}")


def process_config(cfg_file):
    with open(cfg_file) as f:
        CONF = json.load(f)

    LANG = CONF.get("lang", "en")
    WW = CONF["name"]
    VOICE_IDS = CONF.get("tts_voices") or []

    VOICES_FOLDER = f"{VOICES_BASE}/{LANG}"
    OUTPUT_FOLDER = f"{OUTPUT_BASE}/{WW.lower().replace(' ', '_')}"
    makedirs(OUTPUT_FOLDER, exist_ok=True)

    with ThreadPoolExecutor(max_workers=os.cpu_count() // 2) as voice_executor:
        voice_futures = [
            voice_executor.submit(process_voice, WW, voice, LANG, OUTPUT_FOLDER, VOICES_FOLDER)
            for voice in VOICE_IDS
        ]
        for future in as_completed(voice_futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error processing voice: {e}")


def main():
    wws = listdir(WW_CFGS)
    random.shuffle(wws)
    cfg_files = [f"{WW_CFGS}/{cfg}" for cfg in wws if cfg.endswith(".json")]

    with ThreadPoolExecutor(max_workers=os.cpu_count() // 2) as cfg_executor:
        cfg_futures = {cfg_executor.submit(process_config, cfg_file): cfg_file for cfg_file in cfg_files}
        for future in as_completed(cfg_futures):
            cfg_file = cfg_futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error processing {cfg_file}: {e}")


if __name__ == "__main__":
    main()
