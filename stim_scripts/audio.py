"""
Code for automatically presenting the audio in the passive listening task.
Uses the same melodies as in the training, which are stored in the wav folder. 
The program loops through the melodies in order (see readme for updated order).

"""

import pygame
import time
import mido
import sys
import os
from pathlib import Path

#setting wav path
folder_path = Path('./wav_bal/')

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 1480
screen_height = 850
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Melody training")




# Welcome screen text
welcome_text_lines = [
    "Welcome!",
    "You will listen to a series of melodies.",
    "Try to stay as still as possible.",
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
prompt_text = font.render("Listen to the melody. If you can, imagine yourself playing them.", True, (255, 255, 255))
prompt_rect = prompt_text.get_rect(center=(screen_width // 2, screen_height // 2))


# Initialize variables for trial
trial_number = 1
notes_vector = []

num_cycles = 1
curr_cycle = 0

paused = False

clock = pygame.time.Clock()

while curr_cycle < num_cycles:

    for file_name in sorted(os.listdir(folder_path)):
        file_path = os.path.join(folder_path, file_name)
        print(file_path)

        try:
            # Load the sound file
            sound = pygame.mixer.Sound(file_path)

            # Play the sound file
            sound.play()

            # Clear the screen
            screen.fill((0, 0, 0))

            # Draw the "Now try to imitate" text
            screen.blit(prompt_text, prompt_rect)

            # Update the display
            pygame.display.flip()

            # Wait for the sound to finish playing
            while pygame.mixer.get_busy():
                # Handle events during playback
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        # Allow the user to pause or skip to the next sound by pressing space
                        pygame.mixer.stop()
                        time.sleep(0.5)  # Optional delay for better user experience

                # Cap the frame rate to avoid high CPU usage
                clock.tick(30)

        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    curr_cycle += 1

# Quit Pygame
pygame.quit()
