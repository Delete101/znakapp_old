import os
from PIL import Image, ImageDraw

mask_suffix = '_mask'

def create_mask_black(filename):
    dir_path, file_name = os.path.split(filename)
    file_name, file_ext = os.path.splitext(file_name)

    # Load the input image
    input_image = Image.open(filename)

    # Create a new blank image with the same resolution as the input image
    new_image = Image.new(mode='RGB', size=input_image.size, color='black')

    # Save the new image as a PNG file
    new_file_name = file_name + mask_suffix
    new_file_path = os.path.join(dir_path, new_file_name + file_ext)
    new_image.save(new_file_path)

    return new_file_path

def create_white_mask(filename):
    # Load the input image
    input_image = Image.open(filename)

    # Get the image size
    width, height = input_image.size

    # Set the size of the white rectangles and padding
    mask_width = 200
    mask_height = 100
    padding = 30
    id_mask_height = 50
    id_mask_width = 200

    # Create a new image with the same size as the input image
    output_image = Image.new(mode='RGBA', size=(width, height), color=(0, 0, 0, 0))

    # Draw the white rectangles in the corners with padding
    draw = ImageDraw.Draw(output_image)
    draw.rectangle((padding, padding, mask_width + padding, mask_height + padding), fill=(255, 255, 255, 255))
    draw.rectangle((padding, height - mask_height - padding, mask_width + padding, height - padding), fill=(255, 255, 255, 255))
    draw.rectangle((width - mask_width - padding, padding, width - padding, mask_height + padding), fill=(255, 255, 255, 255))
    draw.rectangle((width - mask_width - padding, height - mask_height - padding, width - padding, height - padding), fill=(255, 255, 255, 255))
    draw.rectangle(((width - id_mask_width)/2, (height - id_mask_height)/2, (width + id_mask_width)/2, (height + id_mask_height)/2), fill=(255, 255, 255, 255))

    # Merge the output image with the input image
    merged_image = Image.alpha_composite(input_image.convert('RGBA'), output_image)

    # Save the merged image as a PNG file
    merged_image.save(filename)

script_path = os.path.dirname(os.path.realpath(__file__))

# The path to the folder to enumerate
in_folder_path = '/Users/daniillavrentyev/PycharmProjects/znakapp3.8/znakapp_38/znakapp/znakapp/service/parser_znakapp/images/'

# Enumerate the files in the folder
for filename in os.listdir(in_folder_path):
    if os.path.isfile(os.path.join(in_folder_path, filename)):
        mask_file_name = create_mask_black(in_folder_path + filename)
        create_white_mask(mask_file_name)

