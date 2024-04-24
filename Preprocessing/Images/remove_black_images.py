################################ IMPORTS ################################
# ALL
import os
import shutil
import sys

# FROM
from PIL import Image, ImageFile, UnidentifiedImageError

# AS
import numpy as np
import pandas as pd

################################ FUNCTION ################################
ImageFile.LOAD_TRUNCATED_IMAGES = True

# Define the directory paths
root_dir = sys.argv[1]
original_images_dir = root_dir + '/images'
black_images_dir = root_dir + '/images_with_excess_black'

# Create a directory for images with excess black if it doesn't exist
if not os.path.exists(black_images_dir):
    os.makedirs(black_images_dir)

# Define the threshold value for black percentage
# Granice na slici imaju crni obrub i točno dva posto zauzimaju na slici
black_threshold = 2

# Function to calculate the percentage of black pixels in an image
def calculate_black_percentage(image_path):
    try:
        image = Image.open(image_path)
        gray_image = image.convert('L')
        image_array = np.array(gray_image)
        # Count black pixels(assuming black is represented as 0 in grayscale)
        black_pixels = np.sum(image_array == 0)
        total_pixels = image_array.size
        black_percentage = (black_pixels / total_pixels) * 100
        return black_percentage
    except UnidentifiedImageError:
        print(f"Cannot identify image file: {image_path}")
        return None
    except OSError:
        print(f"Truncated file read: {image_path}")
        return None

def main():
    # List to hold the paths of images that are moved
    # List to hold the paths of images that are moved
    moved_images = []
    images_list = []
    count = 0
    
    total_images = len(os.listdir(original_images_dir)) if os.path.exists(original_images_dir) else 0

    # Iterate over all files in the source directory
    for filename in os.listdir(original_images_dir):
        # Construct the full file path
        file_path = os.path.join(original_images_dir, filename)
        # Check if the file is an image based on its extension (simple check)
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            # Append the filename to the list
            images_list.append({'image_name': filename, 'black_percentage': calculate_black_percentage(file_path), 'black_iamge': file_path, 'moved': 'False'})
            
            # Calculate the black percentage
            print(filename)
            black_percentage = calculate_black_percentage(file_path)
            if black_percentage is None:
                continue

            # Move the image if the black percentage is greater than the threshold
            if black_percentage > black_threshold:
                shutil.move(file_path, os.path.join(black_images_dir, filename))
                moved_images.append(filename)
                
                images_list[-1]['moved'] = 'True'
                images_list[-1]['black_image'] = os.path.join(black_images_dir, filename)
                
            count += 1
            print(f"Processed {count}/{total_images} images")

    print(moved_images)

    # Save the dataframe to a CSV file
    images_df = pd.DataFrame(images_list)
    images_df.to_csv(root_dir + '/images_black_percentage.csv', index=False)


if __name__ == "__main__":
    main()
