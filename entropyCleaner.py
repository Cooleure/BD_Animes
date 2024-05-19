import numpy as np
from PIL import Image
from scipy.stats import entropy
import os

#how "uniform" the histogram, thus the image is
def calculate_entropy(image_path):
    image = Image.open(image_path).convert('L')
    histogram = np.histogram(image, bins=256, range=(0, 255))[0]
    histogram = histogram / np.sum(histogram)
    return entropy(histogram, base=2)

def filter_low_entropy_images(image_folder, entropy_threshold):
    low_entropy_images = []
    entropy_score = []
    for filename in os.listdir(image_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(image_folder, filename)
            ent = calculate_entropy(image_path)
            if ent < entropy_threshold:
                low_entropy_images.append(filename)
            entropy_score.append((filename, ent))
    return low_entropy_images, entropy_score

image_folder = "./"
garbage_folder = "Garbage/"
entropy_threshold = 3.4 #found empirically
# low_entropy_images, score = filter_low_entropy_images(image_folder, entropy_threshold)
# print("Low entropy images:", low_entropy_images)

#we iterate through each subfolder etc till finding a leaf folder
for root, dirs, files in os.walk(image_folder):
    for dir in dirs:
        if ("Output" in dir):
            print(root+"/"+dir)
            realDir = root+"/"+dir
            low_entropy_images, score = filter_low_entropy_images(realDir, entropy_threshold)    
            for image in low_entropy_images:
                os.rename(realDir+"/"+image, garbage_folder+image)