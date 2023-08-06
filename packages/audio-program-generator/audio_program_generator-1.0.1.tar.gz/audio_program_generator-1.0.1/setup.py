# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['audio_program_generator']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0',
 'gTTS>=2.2.2,<3.0.0',
 'pydub>=0.25.1,<0.26.0',
 'tqdm>=4.61.0,<5.0.0']

setup_kwargs = {
    'name': 'audio-program-generator',
    'version': '1.0.1',
    'description': 'Create an audio program from a text file containing English sentences',
    'long_description': '# apg (audio_program_generator)\nGenerates an audio program from a text file containing English sentences\n\n# Prerequisites\n* Some relatively recent version of Python (3.7+)\n* FFMPEG with at least the ability to read mp3s and wavs, and write mp3s\n\n# Description:\napg.py:\nGenerate audio program of spoken phrases, with optional background\nsound file mixed in.\n\nUser populates a semicolon-separated text file with plain-text phrases,\neach followed by an inter-phrase duration. Each line of the file is\ncomprised of:\n  - one phrase to be spoken\n  - a semicolon\n  - a silence duration (specified in seconds)\n\nThe script generates and saves a single MP3 file. The base name of the MP3\nfile is the same as the specified input file. So, for example, if the\nscript is given input file "phrases.txt", the output file will be\n"phrases.mp3".\n\nThe "mix" command is used to mix in background sounds. This command takes\nan extra parameter, the path/filename of a sound file to be mixed in with\nthe speech file generated from the phrase file. If the sound file is shorter\nin duration than the generated speech file, it will be looped. If it is\nlonger, it will be truncated. The resulting background sound (looped or\nnot) will be faded in and out to ensure a smooth transition. Currently,\nonly .wav files are supported as inputs.\n\n# Usage:\n    apg [options] <phrase_file>\n    apg [options] mix <phrase_file> <sound_file>\n    apg -V --version\n    apg -h --help\n\n# Options:\n    -a --attenuation LEVEL  Set attenuation level of background file (non-\n                            negative number, indicating dB attenuation).\n    -d --debug              Print debug statements to console.\n    -V --version            Show version.\n    -h --help               Show this screen.\n\n# Commands:\n    mix                     Mix files\n\n# Arguments:\n    phrase_file             Name of semicolon-separated text file containing\n                            phrases and silence durations. Do not include\n                            commas in this file.\n    sound_file              A file to be mixed into the generated program\n                            file. Useful for background music/sounds. Must\n                            be in .wav format.\n\n# Example <phrase_file> format:\n    Phrase One;2\n    Phrase Two;5\n    Phrase Three;0\n\n# Author:\nJeff Wright <jeff.washcloth@gmail.com>\n\n',
    'author': 'Jeff Wright',
    'author_email': 'jeff.washcloth@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jeffwright13/audio_program_generator/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
