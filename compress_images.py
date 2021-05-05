from dotenv import load_dotenv
from PIL import Image
from shutil import copy2
import os
import threading
import whatimage
import pyheif
import io
import secret

load_dotenv()

upload_dir = os.getenv("UPLOAD_PATH")
storage_dir = os.getenv("STORAGE_PATH")
website_dir = os.getenv("WEB_PATH")

base = int(os.getenv("SIZE"))
quality = int(os.getenv("QUALITY"))

interval = int(os.getenv("INTERVAL"))

def resize_image(filename):
    basewidth = 300

    filepath = upload_dir + filename

    with open(filepath, 'rb') as f:
        data = f.read()

    fmt = whatimage.identify_image(data)

    if fmt in ['heic', 'avif']:
        i = pyheif.read_heif(filepath)

        img = Image.frombytes(
            i.mode, 
            i.size, 
            i.data,
            "raw",
            i.mode,
            i.stride,)
    
    else:
        img = Image.open(filepath)

    new_size = calculate_size(img.size, base)
    img = img.resize(new_size, Image.ANTIALIAS).convert('RGB')

    img.save(website_dir + create_new_filename(filename), quality=quality)

def create_new_filename(filename):
    tok = secrets.token_urlsafe(32)
    name, ending = filename.rsplit('.',1)
    new_filename = name + tok + ".jpg"

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
    tok = secrets.token_urlsafe(32)
    copy2(upload_dir + filename, website_dir + filename.rsplit(".")[0] + tok + "." + filename.rsplit(".")[1])

def move_original(filename, failed=False):
    if failed:
        os.rename(upload_dir + filename, failed_dir + filename)
    else:
        os.rename(upload_dir + filename, storage_dir + filename)

def list_files(directory):
    files_and_folders = os.listdir(directory)
    return files_and_folders

def update_images():
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

def startTimer():
    threading.Timer(interval, startTimer).start()
    update_images()
    
def main():
    startTimer()

        

if __name__=="__main__":
    main()
    

