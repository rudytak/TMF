from os import listdir
from os.path import isfile, join
from PIL import Image
Image.MAX_IMAGE_PIXELS = 1e9

onlyfiles = [f for f in listdir("./") if isfile(join("./", f)) and f.endswith(".png")]

targ_w = 500
for f in onlyfiles:
    img = Image.open(f)
    
    new_img = img.resize((targ_w, int(targ_w / img.width * img.height)))
    new_img.save(f"../imgsLR/{f}")