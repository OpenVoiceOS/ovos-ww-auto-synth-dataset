import subprocess
from os import listdir, makedirs, walk, rename
from os.path import join, isdir, isfile, dirname
import json

WW_CFGS = f"auto_synth/ww_configs"
SAMPLES_BASE = f"auto_synth/synth_data"
OUTPUT_BASE = f"auto_synth/synth_data_converted"


# this will convert all files to the correct format
def convert_dir(SOURCE_DIR, DEST_DIR, overwrite=False):
    if not isdir(DEST_DIR):
        makedirs(DEST_DIR)

    exts = ["mp3", "wav", "mp4"]
    for wav in listdir(SOURCE_DIR):
        if wav.split(".")[-1] not in exts:
            # non audio file, skip
            if isdir(join(SOURCE_DIR, wav)):
                # TODO recursive
                print("skipping directory", wav)
            else:
                print("unrecognized format, skipping", wav)
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
    ww = cfg.replace(".json", ".wav")
    src = f"{SAMPLES_BASE}/{ww}"
    if not isfile(src):
        continue
    dst = f"{OUTPUT_BASE}/{ww}"

    for root, dirs, files in walk(src, topdown=False):
        path = root
        dest = path.replace(src, dst)
        convert_dir(root, dest)
