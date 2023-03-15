import subprocess
from os import listdir, makedirs, walk, rename
from os.path import join, isdir, isfile, dirname
import json

WW_CFGS = f"{dirname(dirname(__file__))}/ww_configs"
SAMPLES_BASE = f"{dirname(dirname(__file__))}/synth_data"
OUTPUT_BASE = SAMPLES_BASE


exts = ["mp3", "mp4"]


# this will convert all files to the correct format
def convert_dir(SOURCE_DIR, DEST_DIR=None, overwrite=True):
    DEST_DIR = DEST_DIR or SOURCE_DIR
    if not isdir(DEST_DIR):
        makedirs(DEST_DIR)

    for wav in listdir(SOURCE_DIR):
        if wav.split(".")[-1] not in exts:
            continue
        print("converting ", wav)
        if wav.endswith(".wav"):
            converted = join(DEST_DIR, wav)
        else:
            converted = join(DEST_DIR, wav + ".wav")
        wav = join(SOURCE_DIR, wav)
        if isfile(converted) and not overwrite:
            print("converted file already exists, skipping")
        else:
            cmd = ["ffmpeg", "-i", wav, "-acodec", "pcm_s16le", "-ar",
                   "16000", "-ac", "1", "-f", "wav", converted, "-y"]

            subprocess.call(cmd)


for cfg in listdir(WW_CFGS):
    with open(f"{WW_CFGS}/{cfg}") as f:
        CONF = json.load(f)
    ww = cfg.replace(".json", "")
    src = f"{SAMPLES_BASE}/{ww}"
    if not isdir(src):
        continue
    convert_dir(src)
