# app/utilities.py

import os
import dotenv
import cloudinary.uploader
from typing import Optional, Tuple, List
from PIL import Image
import extcolors

# Load environment variables
dotenv.load_dotenv()

cloudinary.config(
    cloud_name=os.environ['CLOUDINARY_NAME'],
    api_key=os.environ['CLOUDINARY_API_KEY'],
    api_secret=os.environ['CLOUDINARY_API_SECRET']
)

# def upload_image(image: bytes) -> Optional[str]:
#     try:
#         upload_result = cloudinary.uploader.upload(image)
#         return upload_result.get('secure_url', None)
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None

def upload_image(image: bytes) -> Optional[Tuple[str, List[str]]]:
    try:
        upload_result = cloudinary.uploader.upload(
            image,
            categorization="google_tagging",
            auto_tagging=0.6
        )
        
        image_url = upload_result.get('secure_url', None)
        auto_tags = upload_result.get('tags', [])
        
        return image_url, auto_tags
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# Extract colours


def hex_to_rgb(H):
    r = g = b = 0
    if len(H) == 4:
        r, g, b = [int(H[i]*2, 16) for i in (1, 2, 3)]
    elif len(H) == 7:
        r, g, b = [int(H[i:i+2], 16) for i in (1, 3, 5)]
    return r, g, b

def rgb_to_hsl(rgb):
    r, g, b = [x/255.0 for x in rgb]
    max_val, min_val = max(r, g, b), min(r, g, b)
    delta = max_val - min_val
    l = (max_val + min_val) / 2.0

    if delta == 0:
        h = s = 0
    else:
        s = delta / (2 - max_val - min_val) if l > 0.5 else delta / (max_val + min_val)
        h = {
            r: (g - b) / delta + (6 if g < b else 0),
            g: (b - r) / delta + 2,
            b: (r - g) / delta + 4,
        }[max_val]
        h /= 6

    h, s, l = [int(x*100) for x in [h, s, l]]  # Convert to percentage
    return h, s, l

def extract_colours(image_path, num_colors=3, resize_factor=0.1, tolerance=10):
    try:
        # Open and resize the image
        image = Image.open(image_path)
        image = image.resize((int(image.width * resize_factor), int(image.height * resize_factor)))

        # Extract colors from the resized image with custom tolerance
        colors, _ = extcolors.extract_from_image(image, tolerance=tolerance)

        # Sort the colors by pixel count and get the top N dominant colors
        top_colors = sorted(colors, key=lambda x: x[1], reverse=True)[:num_colors]

        # Convert the RGB values to HSL and format them
        hsl_values = ["hsl({}, {}%, {}%)".format(*rgb_to_hsl(color[0])) for color in top_colors]

        return hsl_values

    except Exception as e:
        return str(e)
    
# # Hex version
# def extract_colours(image_path, num_colors=5, resize_factor=0.1, tolerance=10):
#     try:
#         # Open and resize the image
#         image = Image.open(image_path)
#         image = image.resize((int(image.width * resize_factor), int(image.height * resize_factor)))
        
#         # Extract colors from the resized image with custom tolerance
#         colors, pixel_count = extcolors.extract_from_path(image_path, tolerance=tolerance)
        
#         # Sort the colors by pixel count
#         sorted_colors = sorted(colors, key=lambda x: x[1], reverse=True)
        
#         # Get the top N dominant colors (N = num_colors)
#         top_colors = sorted_colors[:num_colors]
        
#         # Extract the HEX values of the top colors and add the hash sign
#         hex_colors = ['#' + ''.join(f'{int(c):02X}' for c in color[0]) for color in top_colors]
        
#         return hex_colors
#     except Exception as e:
#         return str(e)

# # # Example usage:
# # image_path = '3.png'
# # num_colors = 5
# # resize_factor = 0.1  # Adjust the resize factor as needed
# # tolerance = 15       # Adjust the tolerance as needed
# # dominant_colors = extract_colour(image_path, num_colors, resize_factor, tolerance)