#################### IMPORTS ####################
# AS
import numpy as np
import pandas as pd

# FROM
from scipy.stats import skew
from tqdm import tqdm

#################### FUNCTIONS ####################

# This function will get image stats: mean, std, width, height, skewness
'''
The following statistics were extracted:

* **mean:** Mean pixel value of each image.
* **std:** Standard deviation of pixel values in each image.
* **width:** Width of each image.
* **height:** Height of each image.
* **skew:** Skewness of the histogram of pixel values in each image.
'''
def get_image_stats(images, labels, paths):
    means, stds, widths, heights = [], [], [], []
    skewnesses = []
    
    for image in tqdm(images):
        means.append(np.mean(image))
        stds.append(np.std(image))
        widths.append(image.shape[0])
        heights.append(image.shape[1])
        image_hist = np.histogram(image.flatten())[0]
        skewnesses.append(skew(image_hist))
    
    image_stats = pd.DataFrame({
        'mean': means,
        'std': stds,
        'width': widths,
        'height': heights,
        'skew': skewnesses
    })
    
    image_stats['label'] = labels
    image_stats['path'] = paths
    return image_stats

def get_csv_stats(df):
    
    # Initialize lists to store stats
    means, stds, mins, maxs, skews = [], [], [], [], []
    
    # Calculate stats for each column
    for column in df.columns:
        means.append(df[column].mean())
        stds.append(df[column].std())
        mins.append(df[column].min())
        maxs.append(df[column].max())
        skews.append(skew(df[column]))
    
    # Create a DataFrame to store the stats
    csv_stats = pd.DataFrame({
        'mean': means,
        'std': stds,
        'min': mins,
        'max': maxs,
        'skew': skews
    }, index=df.columns)  # Use the column names of the original DataFrame as the index
    
    return csv_stats