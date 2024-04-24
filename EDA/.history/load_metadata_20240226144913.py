#################### IMPORTS ####################
# ALL
import os
import re

# AS
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import nibabel as nib  # For neuroimaging data
import plotly.express as px

# FROM
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from PIL import Image
from scipy.stats import skew
from tqdm import tqdm

#################### FUNCTIONS ####################

# This function will validate filename to ensure it is a valid OASIS Alzheimer's dataset filename
def validate_filename(filename):
    """
    Validate filename to ensure it is a valid OASIS Alzheimer's dataset filename.
    """
    # general pattern to include and . file
    pattern = re.compile('OAS\d+_\d+_MR\d+_mpr-\d+_\d+\.\w+$') #TODO: Change patterns to match other file formats

    return bool(pattern.match(filename))

# This function will get info from filename
def change_filename(folder, filename, layer_id=0):
    """
    Extract patient_id and layer_id from filename
    """
    if validate_filename(filename):
        return filename
    
    # if mpr-1 is followed by . then remove .nifti from name # Pattern to match '.nifti' or '.4dfp' right before the file extension
    pattern = re.compile(r'(\.nifti|\.4dfp)(?=\.\w+$)') #TODO: Change patterns to match other file formats

    # Replace '.nifti' or '.4dfp' with '_0' if it's right before the file extension
    filename = re.sub(pattern, f'_{layer_id}', filename)

    # Combine file and folder to one name a
    filename = folder + '_' + filename

    return filename

# This function will get info from filename
def get_info_from_filename(filename):
    """
    Extract patient_id and layer_id from filename
    """
    pattern = re.compile('OAS(\d+)_(\d+)_MR(\d+)_mpr-(\d+)_(\d+).(\w+$)')  #TODO: Change patterns to match other file formats
    match = pattern.match(filename)
    oasis_dataset_number = match.group(1)
    patient_id = match.group(2)
    mr_id = match.group(3)
    scan_id = match.group(4)
    layer_id = match.group(5)
    file_format = match.group(6)

    return oasis_dataset_number, patient_id, mr_id, scan_id, layer_id, file_format

# This function will create a reference dataframe
def create_ref_df(dataset_path):
    """
    Create a reference dataframe with the following columns:
    - path: path to the image
    - label: label of the image
    - patient_id: patient id
    - mr_id: session number of the mr
    - scan_id: id of scan in the corresponding mr session
    - layer_id: layer id of the image -> [100, 160]
    """
    paths, labels = [], []
    oasis_dataset_numbers, patient_ids, mr_ids, scan_ids, layer_ids, file_formats = [], [], [], [], [], []

    for folder in os.listdir(dataset_path):
        # Skip .DS_Store file or any file that is not a folder
        if folder == '.DS_Store' or not os.path.isdir(os.path.join(dataset_path, folder)):
            continue

        for original_file in os.listdir(os.path.join(dataset_path, folder)):
            # Skip .DS_Store file or any file that is not a folder
            if original_file == '.DS_Store' or not os.path.isdir(os.path.join(dataset_path, folder)):
                continue
            # Check to see if the folder contains other folders
            if os.path.isdir(os.path.join(dataset_path, folder, original_file)):
                for data_folder in os.listdir(os.path.join(dataset_path, folder, original_file)):

                    # Skip .DS_Store file or any file that is not a folder
                    if data_folder == '.DS_Store' or not os.path.isdir(os.path.join(dataset_path, folder)):
                        continue

                    for original_file_1 in os.listdir(os.path.join(dataset_path, folder, original_file, data_folder)):
                        # if file ends with 4dfp.img.rec file, skip
                        if original_file_1.endswith('4dfp.img.rec'):
                            continue

                        # check to see if the file is a valid filename
                        if not validate_filename(original_file_1):
                            # Combine file and folder to one name a
                            file = change_filename(folder, original_file_1)
                            
                            if not validate_filename(file):
                                raise ValueError(f'Invalid filename: {file}')
                        else:
                            file = original_file_1

                        oasis_dataset_number, patient_id, mr_id, scan_id, layer_id, file_format = get_info_from_filename(file)
                        # print(file_format)
                            
                        if file_format == 'hdr' or file_format == 'ifh' or file_format == "4dfp.img.rec":
                            continue

                        paths.append(os.path.join(dataset_path, folder, original_file, data_folder, original_file_1))
                        labels.append(folder)
                        oasis_dataset_numbers.append(oasis_dataset_number)
                        patient_ids.append(patient_id)
                        mr_ids.append(mr_id)
                        scan_ids.append(scan_id)
                        layer_ids.append(layer_id)
                        file_formats.append(file_format)
            else:

                # check to see if the file is a valid filename
                if not validate_filename(original_file):
                    # Combine file and folder to one name a
                    file = change_filename(folder, original_file)
                    
                    if not validate_filename(file):
                        raise ValueError(f'Invalid filename: {file}')
                else:
                    file = original_file

                oasis_dataset_number, patient_id, mr_id, scan_id, layer_id, file_format = get_info_from_filename(file)
                    
                if file_format == 'hdr':
                    continue

                paths.append(os.path.join(dataset_path, folder, original_file))
                labels.append(folder)
                oasis_dataset_numbers.append(oasis_dataset_number)
                patient_ids.append(patient_id)
                mr_ids.append(mr_id)
                scan_ids.append(scan_id)
                layer_ids.append(layer_id)
                file_formats.append(file_format)

    ref_df = pd.DataFrame({
        'path': paths,
        'label': labels,
        'oasis_dataset_number': oasis_dataset_numbers, # 'oasis_dataset_number' is the 'OAS' number in the filename
        'patient_id': patient_ids,
        'mr_id': mr_ids,
        'scan_id': scan_ids,
        'layer_id': layer_ids,
        'file_format': file_formats
    })

    ref_df = ref_df.astype({
        'path': 'string',
        'label': 'string',
        'oasis_dataset_number': 'int64',
        'patient_id': 'int64',
        'mr_id': 'int64',
        'scan_id': 'int64',
        'layer_id': 'int64',
        'file_format': 'string'
    })

    return ref_df