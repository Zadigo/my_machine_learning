import os
from random import shuffle
import csv

PATH = 'C:\\Users\\Pende\\Pictures\\dataset'

def images(folder='faces'):
    return list(os.walk(os.path.join(PATH, folder)))[0][2]

def image_shuffler(folder='faces', dest_folder='shuffled_faces'):
    """A definition that shuffles the images in the folder and restitutes
    them to a destination folder"""
    images_in_folder = images()
    shuffle(images())

    for i, image in enumerate(images_in_folder):
        image_path = os.path.join(PATH, 'faces', image)
        dest_path = os.path.join(PATH, dest_folder, f'fw{i + 1}.jpg')
        os.replace(image_path, dest_path)
    print('Shuffled %s images' % len(images))

def score_file(folder='faces'):
    images_in_folder = images()
    with open(os.path.join(PATH, 'score_file.csv'), 'w', newline='', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['face_reference', 'image', 'score'])
        for i, image in enumerate(images_in_folder):
            csv_writer.writerow([f'fw{i + 1}', image, 0])
        print('Wrote %s images' % len(images_in_folder))

score_file()