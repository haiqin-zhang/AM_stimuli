"""
Records the keystrokes during a trial and saves the time and keystroke to a CSV file. 
Backup recording for the motor imagery part of the experiment, 
but all the info recorded here should be recorded in double on Ableton for audio synthesis.

How to use: python MI.py [root name of csv, usually name of subject]

ABLETON MUST BE ACTIVE IN THE BACKGROUND TO PRODUCE SOUND (has nothing to do with the python stuff though)
Requires a midi keyboard to be plugged into the computer (the one I'm using is called V49 Out)

"""

import pygame
import time
import mido
import csv
from pathlib import Path
import sys
import os


# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 1480
screen_height = 850
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame MIDI Recorder")

# Set up font and text
font = pygame.font.Font(None, 36)
prompt_text = font.render("Play one note per metronome beat. Four notes on, four notes rest.", True, (255, 255, 255))
prompt_rect = prompt_text.get_rect(center=(screen_width // 2, screen_height // 2))

# Set up MIDI recording
midi_input = mido.open_input("V49 Out", callback=None)  # Replace with the actual MIDI device name

# Create a CSV file for recording
#csv_filename = "midi_record.csv"
csv_filename = "MI_" + sys.argv[1]+".csv"
csv_file = open(csv_filename, "w", newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["time", "note"])


# Record start time
start_time = time.time()


# Clear the screen
screen.fill((0, 0, 0))

# Draw the "Now try to imitate" text
screen.blit(prompt_text, prompt_rect)

# Update the display
pygame.display.flip()

# Record MIDI events
while time.time() - start_time < 300:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    for msg in midi_input.iter_pending():
        if msg.type == "note_on":
            note = msg.note

        # Save notes_vector to CSV and reset for the next trial
        csv_writer.writerow([time.time()-start_time, note])


# Close the MIDI file and CSV file
midi_input.close()
csv_file.close()

# Quit Pygame
pygame.quit()
sys.exit()