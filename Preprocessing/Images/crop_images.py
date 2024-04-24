import os
import sys
from PIL import Image, UnidentifiedImageError

Image.LOAD_TRUNCATED_IMAGES = True

root_dir = sys.argv[1]
images_path = root_dir + '/images'
cropped_images_path = root_dir + '/cropped_images'

# if cropped_images directory doesn't exist, create it
if not os.path.exists(cropped_images_path):
    os.makedirs(cropped_images_path)

def crop_center(image_path, image):
    try:
        with Image.open(image_path) as im:
            width, height = im.size   # Get dimensions
            new_width = 256
            new_height = 256

            left = (width - new_width)/2
            top = (height - new_height)/2
            right = (width + new_width)/2
            bottom = (height + new_height)/2


            try:
                # Crop the center of the image
                im = im.crop((left, top, right, bottom))
                path_to_cropped = os.path.join(cropped_images_path, image)
                im.save(path_to_cropped)
            except OSError:
                print(f"Truncated file read: {image_path}")
    
    except UnidentifiedImageError:
        print(f"Cannot identify image file: {image_path}")
    except (OSError, SyntaxError):
        print(f"Broken or truncated file: {image_path}")
        


def main():
    all_images = os.listdir(images_path)
    for image in all_images:
        print(image)
        path_to_image = os.path.join(images_path, image)
        crop_center(path_to_image, image)


if __name__ == "__main__":
    main()
