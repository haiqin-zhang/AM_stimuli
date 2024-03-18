"""
A basic training module where melodies are played for you, and you have a few seconds to try to imitate the melodies on the keyboard.

The melodies are stored in the wav folder. The program loops through the melodies in order (see readme for updated order).

ABLETON MUST BE ACTIVE IN THE BACKGROUND TO SYNTHESIZE SOUND, otherwise you hear nothing (sound has nothing to do with the python stuff though)
Requires a midi keyboard to be plugged into the computer

In our lab the big MIDI keyboard is called V49 Out and the small keyboard is "Launchkey Mini MK3 MIDI Port"

"""

import pygame
import time
import mido
import csv
import sys
import os
from pathlib import Path

mode = 'wurli' #classic or wurli - determines which sample melodies are played. Defaults to wurli
MIDI_port = "Launchkey Mini MK3 MIDI Port" #"Launchkey Mini MK3 MIDI Port" (small keyboard) or "V49 Out"  (the big MIDI keyboard)



if len(sys.argv) < 3:
    print("Usage: python train.py <csv_subject>")

subj_name = sys.argv[1]

#setting wav path
if mode == 'classic':
    folder_path = Path('./wav_classic/')
elif mode == 'wurli':
    folder_path = Path('./wav_wurli/')
else:
    folder_path = Path('./wav_wurli/')

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 1480
screen_height = 850
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Melody training")


# Set up MIDI recording
#midi_input = mido.open_input("V49 Out", callback=None)  # Replace with the actual MIDI device name

def get_available_ports():
    return mido.get_input_names()

# Set up MIDI recording
available_ports = get_available_ports()

if MIDI_port in available_ports:
    midi_input = mido.open_input(MIDI_port, callback=None)
    print(f"Connected to MIDI port: {MIDI_port}")
else:
    print(f"The specified MIDI port '{MIDI_port}' is unavailable.")
    print("Available MIDI ports:", available_ports)
    sys.exit()


# Create a CSV file for recording
#csv_filename = "midi_record.csv"
csv_filename = "./train_analysis/train_responses_"+subj_name+".csv"
csv_file = open(csv_filename, "w", newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["trial_number", "notes_vector"])

# Welcome screen text
welcome_text_lines = [
    "Welcome! In this experiment you will hear melodies and try to imitate them on the keyboard.",
    "There will be 5 blocks with 8 sets of about 10 melodies per block.",
    "You will be able to take a break after each set.",
    "Each block should take you 10-12 minutes.",
    "",
    "Press the space bar to begin."
]

# Set up font and text for the intro screen
intro_font = pygame.font.Font(None, 30)

# List to store rendered text and rectangles for each line
text_surfaces = []
text_rects = []

# Render each line separately
for line in welcome_text_lines:
    text_surface = intro_font.render(line, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(screen_width // 2, len(text_surfaces) * 30 + screen_height // 4))
    text_surfaces.append(text_surface)
    text_rects.append(text_rect)

# Display the intro screen
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            running = False

    # Clear the screen
    screen.fill((0, 0, 0))

    # Blit each line onto the screen
    for text_surface, text_rect in zip(text_surfaces, text_rects):
        screen.blit(text_surface, text_rect)

    # Update the display
    pygame.display.flip()

# Wait for the user to press the space bar to start
waiting_for_space = True
while waiting_for_space:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            waiting_for_space = False

# Set up font and text for training
font = pygame.font.Font(None, 36)
prompt_text = font.render("Listen to the melody, then try to copy it!", True, (255, 255, 255))
prompt_rect = prompt_text.get_rect(center=(screen_width // 2, screen_height // 2))

# Initialize variables for trial
trial_number = 1
notes_vector = []

num_cycles = 2
curr_cycle = 0

paused = False

while curr_cycle < num_cycles:
    # Play the sound file 10 times
    set_num = 1

    for folder in sorted(folder_path.iterdir()):

        
        section_text = 'You may now take a short break if you wish. Press the space bar to continue.'
        block_text =  f'You are starting set {set_num}/8, block {curr_cycle+1}/{num_cycles}'

        # Set up font and text for the intro screen
        intro_font = pygame.font.Font(None, 36)
        intro_text = intro_font.render(section_text, True, (255, 255, 255))
        block_intro_text = intro_font.render(block_text, True, (255, 255, 255))
        block_intro_rect = block_intro_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
        intro_rect = intro_text.get_rect(center=(screen_width // 2, screen_height // 2))

        # Display the intro screen
        screen.fill((0, 0, 0))
        screen.blit(intro_text, intro_rect)
        screen.blit(block_intro_text, block_intro_rect)
        pygame.display.flip()

        # Wait for the user to press the space bar to start
        waiting_for_space = True
        while waiting_for_space:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting_for_space = False


        try: 
            folder_files = sorted(folder.iterdir())

            for file_path in folder_files:
                print(file_path)
                # Load the sound file
                pygame.mixer.init()
                pygame.mixer.music.load(file_path)

                # Play the sound file
                pygame.mixer.music.play()

                # Record start time
                start_time = time.time()

                # Record MIDI events for 5 seconds 
                while time.time() - start_time < 10:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                            # Toggle pause state
                            paused = not paused
                            if paused:
                                pygame.mixer.music.pause()
                            else:
                                pygame.mixer.music.unpause()

                    # Clear the screen
                    screen.fill((0, 0, 0))

                    # Draw the "Now try to imitate" text
                    screen.blit(prompt_text, prompt_rect)

                    # Update the display
                    pygame.display.flip()

                    # Record MIDI events
                    for msg in midi_input.iter_pending():
                        if msg.type == "note_on" and msg.velocity > 0: #the launchkey keyboard has a double of each note_on message where the velocity is 0
                            #print(msg)
                            notes_vector.append(msg.note)

                # Save notes_vector to CSV and reset for the next trial
                csv_writer.writerow([trial_number, notes_vector])
                trial_number += 1
                notes_vector = []

                # Wait for 1 second before playing the next sound file
                time.sleep(1)

            set_num += 1

        except Exception as e:
            print(f"Error processing {folder}: {e}") 
        
        
    curr_cycle +=1

# Close the MIDI file and CSV file
midi_input.close()
csv_file.close()

# Quit Pygame
pygame.quit()
