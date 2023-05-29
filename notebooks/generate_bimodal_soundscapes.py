import numpy as np
np.random.seed(123)
import scaper
import os

# SCAPER SETTINGS
fg_folder = '/Users/dilipharish/Master-Thesis/scaper-master/datasets/soundbanks/train/foreground'
bg_folder = '/Users/dilipharish/Master-Thesis/scaper-master/datasets/soundbanks/train/background/'


n_soundscapes = 5
ref_db = -50
duration = 10.0 

min_events = 1
max_events = 2

event_time_dist = 'truncnorm'
event_time_mean1 = 3.0
event_time_mean2 = 7.0
event_time_std = 2.0
event_time_min = 0.0
event_time_max = 10.0

source_time_dist = 'const'
source_time = 0.0

event_duration_dist = 'uniform'
event_duration_min = 0.5
event_duration_max = 4.0

snr_dist = 'uniform'
snr_min = 6
snr_max = 30

pitch_dist = 'uniform'
pitch_min = -3.0
pitch_max = 3.0

time_stretch_dist = 'uniform'
time_stretch_min = 0.8
time_stretch_max = 1.2


# FILE SETTINGS
outfolder = os.path.join('/Users/dilipharish/Master-Thesis/scaper-master/audio/soundscapes/train/bimodal2')
if not os.path.isdir(outfolder):
    os.mkdir(outfolder)


# Generate 20 soundscapes using a BIMODAL distribution of start times

for n in range(n_soundscapes):
    
    print('Generating soundscape: {:d}/{:d}'.format(n+1, n_soundscapes))
    
    # create a scaper
    sc = scaper.Scaper(duration, fg_folder, bg_folder)
    sc.protected_labels = []
    sc.ref_db = ref_db
    
    # add background
    sc.add_background(label=('choose', []), 
                      source_file=('choose', []), 
                      source_time=('const', 0))

    # add random foreground events
    n_events = np.random.randint(min_events, max_events+1)
    for _ in range(n_events):
        
        coin = np.random.randint(0, 2)
        if coin==0:
            mu = event_time_mean1
        else:
            mu = event_time_mean2
            
        sc.add_event(label=('choose', []), 
                     source_file=('choose', []), 
                     source_time=(source_time_dist, source_time), 
                     event_time=(event_time_dist, mu, event_time_std, event_time_min, event_time_max), 
                     event_duration=(event_duration_dist, event_duration_min, event_duration_max), 
                     snr=(snr_dist, snr_min, snr_max),
                     pitch_shift=(pitch_dist, pitch_min, pitch_max),
                     time_stretch=(time_stretch_dist, time_stretch_min, time_stretch_max))
    
    # generate
    audiofile = os.path.join(outfolder, "soundscape_train_bimodal{:d}.wav".format(n))
    jamsfile = os.path.join(outfolder, "soundscape_train_bimodal{:d}.jams".format(n))
    txtfile = os.path.join(outfolder, "soundscape_train_bimodal{:d}.txt".format(n))
    
    sc.generate(audiofile, jamsfile,
                allow_repeated_label=True,
                allow_repeated_source=False,
                reverb=0.1,
                disable_sox_warnings=True,
                no_audio=False,
                txt_path=txtfile)