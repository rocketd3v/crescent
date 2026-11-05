# for the 3x3 characters (yes this script is ai)
from PIL import Image
import os

# Open the original sprite sheet
elliot_character_sheet = Image.open(
    "assets/characters/mara_sheet.png" # change 3x3 character file location here
).convert("RGBA")

# Find the area containing visible pixels
alpha = elliot_character_sheet.getchannel("A")
left_edge, top_edge, right_edge, bottom_edge = alpha.getbbox()

# Calculate the dimensions of each frame
sheet_width = right_edge - left_edge
sheet_height = bottom_edge - top_edge

frame_width = sheet_width / 3
frame_height = sheet_height / 3

# Create a folder for the individual frames
output_folder = "assets/characters/elliot_frames"
os.makedirs(output_folder, exist_ok=True)

# Names for each row of the sprite sheet
directions = ["down", "side", "up"]

# Slice the sprite sheet into 9 frames
for row in range(3):
    for column in range(3):

        # Calculate the boundaries of the frame
        x1 = round(left_edge + column * frame_width)
        y1 = round(top_edge + row * frame_height)

        x2 = round(left_edge + (column + 1) * frame_width)
        y2 = round(top_edge + (row + 1) * frame_height)

        # Crop the frame
        frame = elliot_character_sheet.crop((x1, y1, x2, y2))

        # Give the frame a filename
        direction = directions[row]
        filename = f"{direction}_{column + 1}.png"

        # Save the frame
        frame.save(os.path.join(output_folder, filename))

        print(f"Saved: {filename}")

print("Finished slicing Elliot's sprite sheet!")
