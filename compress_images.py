from dotenv import load_dotenv
from PIL import Image
from shutil import copy2
import os

load_dotenv()

upload_dir = os.getenv("UPLOAD_PATH")
storage_dir = os.getenv("STORAGE_PATH")
website_dir = os.getenv("WEB_PATH")

base = int(os.getenv("SIZE"))
quality = int(os.getenv("QUALITY"))

def resize_image(filename):
    basewidth = 300
    img = Image.open(upload_dir + filename)
    
    new_size = calculate_size(img.size, base)
    img = img.resize(new_size, Image.ANTIALIAS).convert('RGB')

    img.save(website_dir + create_new_filename(filename), quality=quality)

def create_new_filename(filename):
    name, ending = filename.rsplit('.',1)
    new_filename = name + ".jpg"

    return new_filename

def calculate_size(size, base):
    if size[0] < size[1]:
        wpercent = (base / float(size[0]))
        width = base
        height = int((float(size[1]) * float(wpercent)))
    else:
        hpercent = (base / float(size[1]))
        height = base
        width = int((float(size[0]) * float(hpercent)))
    
    return (width, height)

def use_fullsize(filename):
    copy2(upload_dir + filename, website_dir + filename)

def move_original(filename, failed=false):
    if failed:
        os.rename(upload_dir + filename, failed_dir + filename)
    else:
        os.rename(upload_dir + filename, storage_dir + filename)

def list_files(directory):
    files_and_folders = os.listdir(directory)
    return files_and_folders

def main():
    filenames = list_files(upload_dir)
    

    for filename in filenames:
        if os.path.isdir(upload_dir + filename):
            continue

        try:
            if filename.endswith("gif"):
                use_fullsize(filename)
            else:
                resize_image(filename)
        except:
            move_original(filename, failed=True)
        else:
            move_original(filename)

        

if __name__=="__main__":
    main()
    

