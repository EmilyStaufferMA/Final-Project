from PIL import Image

# TODO: Find an empty space and tell the program, to put a watermark there.
# Output to a folder with a custom imput name.
# Tag all the image names with WM.
def find():
    #default should be bottom right
    None

def watermark():
    with (Image.open('still_life_desk.png') as img,
          Image.open('NL_logo.png') as logo_img):
        padding = 50
        x = padding
        y = img.height - logo_img.height - padding
        img.paste(logo_img, (x, y))
        img.show()

# def save_to_disk(img_seq, filename):
#     foldername = input("What would you like to name this folder? ")
#     name, ext = os.path.splitext(filename)
#     try:
#         os.makedirs(foldername)
#     except FileExistsError:
#         pass
#     folder = name
#     watermark = watermark
#     for img in img_seq:
#         padded_filename = f"{name}.{watermark}{ext}"
#         path = os.path.join(folder, filename)
#         print(f"Saving to {path}...")
#         img.save(path)

def main():
    #find()
    watermark()
    #save_to_disk


if __name__ == "__main__":
    main()