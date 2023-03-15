# WakeWord AutoSynth Dataset

submit a .json file to `ww_configs` -> get a dataset under `synth_data`

to add a new voice submit a OPM plugin config to `tts_voices`

this automated pipeline is built with github workflows and OPM

## Plugins

Only good quality plugins have been included by default

English currently outputs 180 unique samples for each wake word

- ovos-tts-plugin-mimic3
- ovos-tts-plugin-deepponies
- ovos-tts-plugin-privox
- ovos-tts-plugin-google-tx