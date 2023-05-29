import numpy as np
np.random.seed(123)
import scaper
import os

# SCAPER SETTINGS
fg_folder = '/Users/dilipharish/Master-Thesis/scaper-master/datasets/soundbanks/train/foreground'
bg_folder = '/Users/dilipharish/Master-Thesis/scaper-master/datasets/soundbanks/train/background/'

n_soundscapes = 50
ref_db = -20
duration = 10.0

min_events = 1
max_events = 3

event_time_dist = 'truncnorm'
event_time_mean = 5.0
event_time_std = 2.0
event_time_min = 0.0
event_time_max = 10.0

source_time_dist = 'const'
source_time = 0.0

event_duration_dist = 'truncnorm'
event_duration_mean = 3.0
event_duration_std = 2.0
event_duration_min = 0.5
event_duration_max = 3.0

snr_dist = 'uniform'
snr_min = 0
snr_max = 1

pitch_dist = 'uniform'
pitch_min = -1.0
pitch_max = 1.0

time_stretch_dist = 'uniform'
time_stretch_min = 0.8
time_stretch_max = 1.2


# FILE SETTINGS
outfolder = os.path.join('/Users/dilipharish/Master-Thesis/scaper-master/audio/soundscapes/train/unimodal2')
if not os.path.isdir(outfolder):
    os.mkdir(outfolder)


# Generate 2000 soundscapes using a UNIFORM distribution of start times

for n in range(n_soundscapes):
    
    print('Generating soundscape: {:d}/{:d}'.format(n+1, n_soundscapes))
    
    # create a scaper
    sc = scaper.Scaper(duration, fg_folder, bg_folder)
    sc.protected_labels = []
    sc.ref_db = ref_db
    
    # add background
    sc.add_background(label=('const', 'car_horn'), 
                      source_file=('choose', []), 
                      source_time=('const', 0))

    # add random foreground events
    n_events = np.random.randint(min_events, max_events+1)
    for _ in range(n_events):
        sc.add_event(label=('choose', []), 
                     source_file=('choose', []), 
                     source_time=(source_time_dist, source_time), 
                     event_time=(event_time_dist, event_time_mean, event_time_std, event_time_min, event_time_max), 
                     event_duration=(event_duration_dist, event_duration_mean, event_duration_std,event_duration_min, event_duration_max), 
                     snr=(snr_dist, snr_min, snr_max),
                     pitch_shift=(pitch_dist, pitch_min, pitch_max),
                     time_stretch=(time_stretch_dist, time_stretch_min, time_stretch_max))
    
    # generate
    audiofile = os.path.join(outfolder, "soundscape_train_unimodal{:d}.wav".format(n))
    jamsfile = os.path.join(outfolder, "soundscape_train_unimodal{:d}.jams".format(n))
    txtfile = os.path.join(outfolder, "soundscape_train_unimodal{:d}.txt".format(n))
    
    sc.generate(audiofile, jamsfile,
                allow_repeated_label=True,
                allow_repeated_source=False,
                reverb=0.1,
                disable_sox_warnings=True,
                no_audio=False,
                txt_path=txtfile)