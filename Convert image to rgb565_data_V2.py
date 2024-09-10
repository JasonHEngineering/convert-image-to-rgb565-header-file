# -*- coding: utf-8 -*-
"""
Change variables "image_path", "header_filename" and "array_name" as needed

"""

from PIL import Image

# Example usage
image_path = "image2_60x60.png"      # Path to your PNG image
header_filename = "jason_h_engineering_logo_16bit.h"  # Output header file
array_name = "gImage_true_color"   # The array name in the header file

# Convert 24-bit RGB to 16-bit RGB565
def rgb888_to_rgb565(r, g, b):
    return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

# Load the PNG image and convert to 16-bit RGB565 format
def convert_image_to_header_16bit(image_path, header_filename, array_name):
    # Open the image
    img = Image.open(image_path)
    img = img.convert('RGB')  # Ensure the image is in RGB format

    # Get the image dimensions
    width, height = img.size

    # Prepare the image data
    image_data = []

    # Loop through all pixels in the image
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            rgb565 = rgb888_to_rgb565(r, g, b)
            image_data.append(rgb565)

    # Calculate the total size of the array (number of 16-bit values)
    array_size = len(image_data)

    # Write the data to a header file in 16-bit hex format
    with open(header_filename, 'w') as header_file:
        # Write array declaration with size
        header_file.write(f"const uint16_t {array_name}[{array_size}] = {{\n")

        # Add image dimensions as comments
        header_file.write(f"/* Image width: {width} pixels */\n")
        header_file.write(f"/* Image height: {height} pixels */\n")

        # Write the image data as 16-bit hex values
        for i, pixel in enumerate(image_data):
            if i % 8 == 0:
                header_file.write("\n  ")
            header_file.write(f"0x{pixel:04X}, ")

        # Close the array definition
        header_file.write("\n};\n")

    print(f"Header file '{header_filename}' created successfully with array '{array_name}' in 16-bit hex format.")

convert_image_to_header_16bit(image_path, header_filename, array_name)
