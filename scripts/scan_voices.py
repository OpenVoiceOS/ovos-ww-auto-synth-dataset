import json
from os import makedirs
from os.path import dirname
from pprint import pprint

from ovos_plugin_manager.tts import get_tts_lang_configs

LANGS = ["en-us", "es-es", "de-de", "fr-fr", "it-it", "pt-pt"]
for LANG in LANGS:
    VOICES_FOLDER = f"{dirname(dirname(__file__))}/tts_voices/{LANG}"
    makedirs(VOICES_FOLDER, exist_ok=True)

    voice_ids = []

    for plug, voices in get_tts_lang_configs(LANG, include_dialects=True).items():
        for voice in voices:
            spkr = voice.get("speaker") or voice.get("lang") or "default"
            name = voice.get("voice") or voice.get("model") or voice.get("gender") or LANG
            voiceid = f"{plug}_{name}_{spkr}.json".replace("/", "_")
            voice_ids.append(voiceid)
            noise = ["meta", "priority", "display_name", "offline", "gender"]
            for k in noise:
                if k in voice:
                    voice.pop(k)
            voice["module"] = plug
            with open(f"{VOICES_FOLDER}/{voiceid}", "w") as f:
                json.dump(voice, f, indent=4)

    pprint(voice_ids)
