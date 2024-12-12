import os
from utils import load_ground_truth, sort_by_class, replace_special_characters
import random

# since the intuitive task also needs the exact same ground truth (population density divided by 3 classes), it is
# included in this project as well. This file loads it, does some preprocessing and sorts the images accordingly
ground_truth_path = 'D:/Formal/plz_einwohner.xls'
path = 'D:/Intuitive'
rename = False
sorting = False
loading = False
replace_characters = False
random_sample = False

# rename files:
if rename:
    dirs = os.listdir(path)
    extension = 'jpeg'

    for dirname in dirs:
        dir_path = os.path.join(path, dirname)
        file_list = os.listdir(dir_path)
        for count, file in enumerate(file_list):
            file_path_old = os.path.join(dir_path, file)
            file_path_new = f'{path}/{dirname}_{count}.{extension}'
            os.rename(file_path_old, file_path_new)
# replace special characters
if replace_characters:
    replace_special_characters('D:/Intuitive')

# sort images by class
if loading:
    high_list, middle_list, low_list = load_ground_truth(ground_truth_path)
    if sorting:
        sort_by_class(path, high_list, middle_list, low_list)

# to balance the dataset, take a random number of images equal to the number of images of the smaller class
# from the two bigger classes. This deletes 798 images in the low class, and 1406 images in the middle class
if random_sample:
    class_size = 5588
    path_low = 'D:/Intuitive/Low'
    path_middle = 'D:/Intuitive/Middle'
    path_low_random = 'D:/Intuitive/Low_random'
    path_middle_random = 'D:/Intuitive/Middle_random'

    filelist_low = os.listdir(path_low)
    filelist_middle = os.listdir(path_middle)
    random_low = random.sample(filelist_low, class_size)
    random_middle = random.sample(filelist_middle, class_size)
    for file in random_low:
        old_path_low = os.path.join(path_low, file)
        new_path_low = os.path.join(path_low_random, file)
        os.rename(old_path_low, new_path_low)
    for file in random_middle:
        old_path_middle = os.path.join(path_middle, file)
        new_path_middle = os.path.join(path_middle_random, file)
        os.rename(old_path_middle, new_path_middle)
