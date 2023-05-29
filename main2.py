import scaper
import numpy as np
import os

# OUTPUT FOLDER
outfolder = '/Users/dilipharish/Master-Thesis/scaper-master/outputfiles/'

path_to_audio = os.path.expanduser('~/Master-Thesis/scaper-master/tests/data/audio')

# soundscape_duration = 10.0
# seed = 123
fg_folder = os.path.join(path_to_audio, 'foreground')
bg_folder = os.path.join(path_to_audio, 'background')
# SCAPER SETTINGS
# fg_folder = 'audio/soundbank/foreground/'
# bg_folder = 'audio/soundbank/background/'

n_soundscapes = 2
ref_db = -50
duration = 10.0

min_events = 1
max_events = 9

event_time_dist = 'truncnorm'
event_time_mean = 5.0
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

# generate a random seed for this Scaper object
seed = 123

# create a scaper that will be used below
sc = scaper.Scaper(duration, fg_folder, bg_folder, random_state=seed)
sc.protected_labels = []
sc.ref_db = ref_db

# Generate 1000 soundscapes using a truncated normal distribution of start times

for n in range(n_soundscapes):

    print('Generating soundscape: {:d}/{:d}'.format(n+1, n_soundscapes))

    # reset the event specifications for foreground and background at the
    # beginning of each loop to clear all previously added events
    # sc.reset_bg_spec()
    # sc.reset_fg_spec()

    # add background
    sc.add_background(label=('const', 'street'),
                      source_file=('choose', []),
                      source_time=('const', 0))
    
    sc.add_background(label=('const', 'park'),
                  source_file=('choose', []),
                  source_time=('const', 0))

    # add random number of foreground events
    n_events = np.random.randint(min_events, max_events+1)
    for _ in range(n_events):
        sc.add_event(label=('choose', ['siren']),
                    source_file=('choose', []),
                     source_time=(source_time_dist, source_time),
                     event_time=(event_time_dist, event_time_mean, event_time_std, event_time_min, event_time_max),
                     event_duration=(event_duration_dist, event_duration_min, event_duration_max),
                     snr=(snr_dist, snr_min, snr_max),
                     pitch_shift=(pitch_dist, pitch_min, pitch_max),
                     time_stretch=(time_stretch_dist, time_stretch_min, time_stretch_max))
    


    # generate
    audiofile = '/Users/dilipharish/Master-Thesis/scaper-master/outputfiles/mysoundscape'+str(n)+'.wav'
    jamsfile = '/Users/dilipharish/Master-Thesis/scaper-master/outputfiles/mysoundscape'+str(n)+'.jams'
    txtfile = '/Users/dilipharish/Master-Thesis/scaper-master/outputfiles/mysoundscape'+str(n)+'.text'

    sc.generate(audiofile, jamsfile,
                allow_repeated_label=True,
                allow_repeated_source=True,
                reverb=0.1,
                disable_sox_warnings=True,
                no_audio=False,
                txt_path=txtfile)