#################### IMPORTS ####################
# AS
import numpy as np
import pandas as pd

# FROM
from PIL import Image
from scipy.stats import skew
from tqdm import tqdm

# FROM FILE
from load_metadata import *

#################### FUNCTIONS ####################

# This function will read a CSV file
def read_csv(file_path):
    return pd.read_csv(file_path)

# This function will read multiple CSV files
def read_multiple_csv(file_paths):
    dfs = []
    for file_path in file_paths:
        dfs.append(pd.read_csv(file_path))
    return dfs

# This function will load an image
def load_image(file_path):
    return np.array(Image.open(file_path).convert('L'))

# This function will load multiple images
def load_multiple_images(ref_df):
    labels = []
    images = []
    paths = []

    # to only load a subset of images
    # ref_df = ref_df.sample(n=100)
    for idx, row in tqdm(ref_df.iterrows(), total=ref_df.shape[0]):
        images.append(np.array(Image.open(row['path']).convert('L')))
        labels.append(row['label'])
        paths.append(row['path'])
    
    return images, labels, paths

# This function will load the data
def load_data(ref_df, numbers='single'):

    if numbers == 'multi':
        file_format = ref_df['file_format']
        if (file_format == 'jpg').all() or (file_format == 'png').all() or (file_format == 'jpeg').all():
            images, labels, paths = load_multiple_images(ref_df)
        elif (file_format == 'csv').all():
            images, labels, paths = read_multiple_csv(ref_df)
        else:
            return 'Invalid file format'
    else:
        # extract the file format from str as last 3 characters
        file_format = extract_file_format(ref_df)
        if (file_format == 'jpg').all() or (file_format == 'png').all() or (file_format == 'jpeg').all():
            images, labels, paths = load_image(ref_df)
        elif (file_format == 'csv').all():
            images, labels, paths = read_csv(ref_df)
        else:
            return 'Invalid file format'
        
    return images, labels, paths