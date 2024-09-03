from PIL import Image, ImageDraw, ImageFont
import numpy as np
import tkinter as tk
from tkinter import filedialog, simpledialog

# Grayscale-based ASCII character map
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

def resize_image(image, new_width=100):
    """Resizes the image while maintaining the aspect ratio."""
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)
    return image.resize((new_width, new_height))

def grayify(image):
    """Converts the image to grayscale."""
    return image.convert("L")

def pixels_to_ascii(image, detail_level=10):
    # Verify that the level of detail is valid
    if detail_level <= 0 or detail_level > len(ASCII_CHARS):
        raise ValueError("Level of detail must be between 1 and the length of the ASCII character map.")

    pixels = np.array(image)
    ascii_str = ""
    num_chars = len(ASCII_CHARS)
    
    # Sets the maximum value for the character index
    max_pixel_value = 255
    range_size = max_pixel_value // detail_level
    
    # Ensure range_size is never zero
    if range_size == 0:
        range_size = 1

    for pixel_row in pixels:
        for value in pixel_row:
            # Adjusts the division for the level of detail
            char_index = min(value // range_size, num_chars - 1)
            ascii_str += ASCII_CHARS[char_index]
        ascii_str += "\n"
    
    return ascii_str

def save_as_image(ascii_art, output_file="ascii_image.png"):
    """Saves ASCII art as a PNG image."""
    # Uses a monospace font (Courier) to ensure consistency
    font = ImageFont.truetype("cour.ttf", 10)
    
    # Creates a blank image large enough for the text
    lines = ascii_art.splitlines()
    max_width = max(len(line) for line in lines)
    max_height = len(lines)
    
    # Calculates text size and creates a proportional image
    char_width, char_height = font.getbbox("A")[2], font.getbbox("A")[3]
    img_width = char_width * max_width
    img_height = char_height * max_height
    
    image = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(image)
    
    # Draw text on image
    y = 0
    for line in lines:
        draw.text((0, y), line, fill="black", font=font)
        y += char_height
    
    # Save the image
    image.save(output_file)

def main(new_width=100):
    """Performs the image conversion process to ASCII art."""
    # Configures a window to select the image
    root = tk.Tk()
    root.withdraw()
    image_path = filedialog.askopenfilename(title="Select an image", 
                                            filetypes=[("Image files", "*.jpg *.png *.jpeg *.bmp *.gif")])

    if not image_path:
        print("No images selected.")
        return

    # Performs the image conversion process to ASCII art.
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Error opening image: {e}")
        return
    
    image = resize_image(image, new_width)
    image = grayify(image)
    
    # Asks the user for the level of detail
    detail_level = simpledialog.askinteger("Detail", "Choose the level of detail (1-10):", minvalue=1, maxvalue=10)
    ascii_art = pixels_to_ascii(image, detail_level)

    # Asks the user for the output format
    output_format = simpledialog.askstring("Format", "Choose output format (TXT or PNG):").lower()

    if output_format == "txt":
        with open("ascii_image.txt", "w") as f:
            f.write(ascii_art)
        print("ASCII art saved in ascii_image.txt")
    elif output_format == "png":
        save_as_image(ascii_art, "ascii_image.png")
        print("ASCII art saved in ascii_image.png")
    else:
        print("Unknown format. Saving as TXT by default.")
        with open("ascii_image.txt", "w") as f:
            f.write(ascii_art)

if __name__ == "__main__":
    main()
