import pandas as pd
import os
import numpy as np
from PIL import Image
from utils import sort_by_class, load_ground_truth, replace_special_characters
import random

# this file is used to do some simple preprocessing steps for the images as well as sorting them by class
sorting = False
loading = False
high_rotate = False
middle_rotate = False
replace_characters = True

# load data and create three lists with the postal codes sorted by class
if loading:
    ground_truth_path = 'D:/Formal/plz_einwohner.xls'
    high_list, middle_list, low_list = load_ground_truth(ground_truth_path)

# move the files into the corresponding folder depending on the class
    if sorting:
        path = 'D:/Formal/Maps'
        sort_by_class(path, high_list, middle_list, low_list)


# since this dataset is highly unbalanced, rotate random images by 90, 180 and 270 degrees
# from the High and Middle density class until the dataset is balanced

high_missing = len(os.listdir('D:/Formal/Maps/Low')) - len(os.listdir('D:/Formal/Maps/High'))
middle_missing = len(os.listdir('D:/Formal/Maps/Low')) - len(os.listdir('D:/Formal/Maps/Middle'))
print(len(os.listdir('D:/Formal/Maps/High')))
print(len(os.listdir('D:/Formal/Maps/Middle')))
print(len(os.listdir('D:/Formal/Maps/Low')))
print(high_missing)
print(middle_missing)

# High density class:
if high_rotate == True:
    high_path = 'D:/Formal/Maps/High'
    high_files = os.listdir(high_path)
    # all available files get rotated by 90 and by 180 degree respectively. Then 584 images are missing to have a
    # balanced dataset. Therefore, 584 randomly chosen images get rotated by 270 degrees as well
    random_sample_high = random.sample(high_files, 584)
    # rotate by 90 and 180 degree for all files
    for file in high_files:
        original = Image.open(os.path.join(high_path, file))
        rotated90 = original.rotate(90)
        rotated180 = original.rotate(180)
        to_add90 = 'rotated90'
        to_add180 = 'rotated180'
        new_filename90 = f'{high_path}/{to_add90}_{file}'
        new_filename180 = f'{high_path}/{to_add180}_{file}'
        rotated90.save(new_filename90, 'PNG')
        rotated180.save(new_filename180, 'PNG')
    # rotate by 270 degrees for 584 random files to balance the dataset
    for file in random_sample_high:
        random_original_high = Image.open(os.path.join(high_path, file))
        rotated270 = random_original_high.rotate(270)
        to_add270 = 'rotated270'
        new_filename270 = f'{high_path}/{to_add270}_{file}'
        rotated270.save(new_filename270, 'PNG')

# Middle density class:
if middle_rotate == True:
    middle_path = 'D:/Formal/Maps/Middle'
    middle_files = os.listdir(middle_path)
    # here fewer images are missing, therefore only 1989 randomly chosen images get rotated by 180 degrees
    random_sample_middle = random.sample(middle_files, 1989)
    # rotate 1989 random images by 180 degrees to balance the dataset
    for file in random_sample_middle:
        random_original_middle = Image.open(os.path.join(middle_path, file))
        rotated180_middle = random_original_middle.rotate(180)
        to_add180_middle = 'rotated180'
        new_filename180_middle = f'{middle_path}/{to_add180_middle}_{file}'
        rotated180_middle.save(new_filename180_middle, 'PNG')


if replace_characters:
    replace_special_characters('D:/Formal/Maps/Low')