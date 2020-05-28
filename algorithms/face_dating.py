#%%
# from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder
import numpy
import os

class Faces:
    def __init__(self, folder):
        path = 'C:\\Users\\Pende\\Downloads\\dataset'
        images = list(os.walk(os.path.join(path, folder)))[0][2]
        images_paths = [os.path.join(path, folder, image) for image in images]
        

    def extract_image_statistics(self, image):
        """Extracts the different color statistics 
        related to an image"""
        R, G, B = image.split()
        features = [numpy.mean(R), numpy.mean(G), numpy.mean(B),\
                        numpy.std(R), numpy.std(G), numpy.std(B)]
        return features

#%%
