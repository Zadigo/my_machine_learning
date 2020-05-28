from PIL import Image
import numpy
from numpy import asarray
from matplotlib import image
from matplotlib import pyplot
import os
import csv

path = 'C:\\Users\\Pende\\Pictures\\dataset\\faces'

def get_images():
    images = os.walk(path)
    images = list(images)[0][2]
    return [os.path.join(path, image) for image in images]


def transform_to_greyscale():
    for image in get_images():
        opened_image = Image.open(image)
        greyscale_image = opened_image.convert('L')
        greyscale_image.save(image)
        
def images_statistics(write_to_file=False):
    all_statistics = []
    for image in get_images():
        opened_image = Image.open(image)
        # Get all the values for Red,
        # Green and Blue
        R, G, B = opened_image.split()
        # Transform images into a greyscale
        # format and get their statistics
        all_statistics.append([os.path.basename(image), numpy.mean(R), numpy.mean(G), numpy.mean(B)])

    if write_to_file:
        with open(os.path.join(path, 'images.csv'), 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'R', 'G', 'B'])
            for row in all_statistics:
                writer.writerow(row)
    return all_statistics

from sklearn.linear_model import Perceptron