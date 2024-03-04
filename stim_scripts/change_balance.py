from pydub import AudioSegment
import os

def change_stereo_balance(input_folder, output_folder, balance_factor):
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through each file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".wav"):
            # Load the audio file
            audio_path = os.path.join(input_folder, filename)
            sound = AudioSegment.from_wav(audio_path)

            # Adjust stereo balance
            sound = sound.pan(balance_factor)

            # Save the adjusted audio to the output folder
            output_path = os.path.join(output_folder, filename)
            sound.export(output_path, format="wav")

if __name__ == "__main__":
    input_folder = "raw_training_files"
    output_folder = "wav_bal"
    balance_factor = 0.9  # Adjust this value between -1 (full left) and 1 (full right)

    change_stereo_balance(input_folder, output_folder, balance_factor)
