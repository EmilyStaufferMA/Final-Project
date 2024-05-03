from PIL import Image
import os

def get_dominant_color(image):
    # Resize the image to speed up color extraction
    small_image = image.resize((100, 100))
    # Get the dominant color
    dominant_color = small_image.getpixel((0, 0))
    return dominant_color

def find_watermark_location(image, watermark):
    width, height = image.size
    watermark_width, watermark_height = watermark.size
    
    # Calculate the size of the watermark as 1/5th of the input image size
    scaled_width = width // 5
    scaled_height = watermark_height * scaled_width // watermark_width
    scaled_watermark = watermark.resize((scaled_width, scaled_height))
    
    watermark_color = get_dominant_color(scaled_watermark)
    
    target_color = image.getpixel((0, 0))

    # Add spacing between the watermark and the edge of the image
    spacing = 10

    for x in range(spacing, width - scaled_width - spacing, 10):
        for y in range(spacing, height - scaled_height - spacing, 10):
            region = image.crop((x, y, x + scaled_width, y + scaled_height))
            colors = region.getcolors(scaled_width * scaled_height)
            dominant_color = max(colors, key=lambda c: c[0])[1]

            color_diff = sum(abs(c1 - c2) for c1, c2 in zip(dominant_color, target_color))

            watermark_diff = sum(abs(c1 - c2) for c1, c2 in zip(dominant_color, watermark_color))

            if color_diff < 100 and watermark_diff > 100:
                return x, y, scaled_width, scaled_height

    # If no suitable location is found, return default location with spacing
    return spacing, height - scaled_height - spacing, scaled_width, scaled_height

def add_watermark(input_folder, output_folder, watermark_path):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    watermark = Image.open(watermark_path)

    for filename in os.listdir(input_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_WM{os.path.splitext(filename)[1]}")

            image = Image.open(image_path)

            x, y, width, height = find_watermark_location(image, watermark)

            image_with_watermark = image.copy()
            image_with_watermark.paste(watermark, (x, y), watermark)

            image_with_watermark.save(output_path)
            print(f"Watermark added to {filename}. Saved as {output_path}")

if __name__ == "__main__":
    input_folder = input("Enter the input folder path: ")
    output_folder = input("Enter the output folder name: ")
    watermark_path = "watermark.png"  # Assuming watermark is in the same directory as the script

    add_watermark(input_folder, output_folder, watermark_path)
