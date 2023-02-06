# Hannah Johnston – Feb 6, 2023
# Put all of your custom .wav files in the the same directory as your project (.lms) file
# TO DO: project/folder names more dynamic

import os
import hashlib
import json
import zipfile
import wave

# Define the directory where the LEGO MINDSTORMS project lives
root_dir = ''
sound_dir = 'sounds'

# Open the .lms file and extract the .sb3 file
with zipfile.ZipFile(os.path.join(root_dir, 'project.lms'), 'r') as lms:
    lms.extractall(root_dir)
with zipfile.ZipFile(os.path.join(root_dir, 'scratch.sb3'), 'r') as sb3:
    sb3.extractall(root_dir)

# Get all .wav files in the sounds folder
sounds = [f for f in os.listdir(sound_dir) if f.endswith('.wav')]

for sound in sounds:
    og_name = sound 
        
    # Get the md5 hash of the sound file
    hash = hashlib.md5()
    with open(os.path.join(sound_dir, sound), 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash.update(chunk)
    sound_hash = hash.hexdigest()

    # Get the number of samples and sample rate from the .wav file
    with wave.open(os.path.join(sound_dir, sound), 'rb') as wav_file:
        num_samples = wav_file.getnframes()
        sample_rate = wav_file.getframerate()

    # Rename the sound file to its hash value
    os.rename(os.path.join(sound_dir, sound), os.path.join(f"{sound_hash}.wav"))
    
    with open('project.json', 'r') as json_file:
        # Load the .json file into a dictionary
        data = json.load(json_file)

        # Add a new sound to the dictionary
        new_sound = {
            "assetId": sound_hash,
            "name": og_name,
            "dataFormat": "wav",
            "rate": sample_rate,
            "sampleCount": num_samples,
            "md5ext": f"{sound_hash}.wav"
        }
        data["targets"][1]["sounds"].append(new_sound)

        # Write the updated dictionary back to the .json file
        with open('project.json', 'w') as json_file:
            json.dump(data, json_file)

# Get all .wav, .svg, and .json files
files = [f for f in os.listdir() if f.endswith('.wav') or f.endswith('.svg') or f.endswith('.json')]

exclude = ['icon.svg', 'manifest.json']

# Create a list of files to include in the zip
include = [f for f in files if f not in exclude]

# Create the .sb3 file
with zipfile.ZipFile('scratch.sb3', 'w') as scratch:
    # Add included files to the zip file
    for f in include:
        scratch.write(f)
        os.remove(f)

# Zip the .lms file to recreate the original project file
with zipfile.ZipFile('project.lms', 'w') as proj:
    proj.write('icon.svg')
    proj.write('manifest.json')
    proj.write('scratch.sb3', compress_type=zipfile.ZIP_DEFLATED)
    os.remove('icon.svg')
    os.remove('manifest.json')
    os.remove('scratch.sb3')