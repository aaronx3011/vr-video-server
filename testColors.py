# Progress bar
from tqdm import tqdm

# Bash interactions
import shlex
import subprocess

# Time
from time import sleep

brightnessInitialValue=-0.10
contrastInitialValue=0.5
saturationInitialValue=1.0

for i in tqdm(range(10)):
    for j in tqdm(range(60)):
        for k in tqdm(range(160)):
            brightness= brightnessInitialValue + (k/100)
            contrast= contrastInitialValue + (j/100)
            saturation= saturationInitialValue + (i/100)
            print("\n\n\n\n\n")
            command= f"gst-launch-1.0 -e filesrc location=testColors.png ! pngdec ! glupload ! glcolorconvert ! video/x-raw(memory:GLMemory),format=RGBA ! glcolorbalance brightness={brightness} contrast={contrast} saturation={saturation} ! gldownload ! pngenc snapshot=True ! filesink location=testColors/brightness{brightness}_contrast{contrast}_saturation{saturation}.png"
            subprocess.check_call(shlex.split(command))
