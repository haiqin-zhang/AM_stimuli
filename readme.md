## Code for generating and running experimental stimuli in the audiomotor piano project.

The stimulus presentation scripts are run in the psychopie environment (see psychopie.yml). 


**These scripts only take care stimulus presentation and logging MIDI keystrokes.
You need to have the MIDI keyboard plugged in and the Ableton file "TRAINING_AUDIO.als" running in another window for sound synthesis.**


.wav files were recorded manually at 60 bpm in Ableton Live 11. The 'wurli' and 'classic' folders use different instruments and slightly different melodies. Classic was used to pilot the program, wurli was used in EEG experiments.

Each set of melodies uses a certain combination of pitches. The order of sets used in the training is:
cd  
cde  
ef  
def  
fg  
efg  
cdef  
cdefg  

The training phase loops through all files twice in the same order and takes approx 30 mins to complete.