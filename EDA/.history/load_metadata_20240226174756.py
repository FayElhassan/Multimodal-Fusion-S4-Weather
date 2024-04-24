#################### IMPORTS ####################
# ALL
import os
import re

# AS
import pandas as pd

#################### FUNCTIONS ####################

# This function will validate filename to ensure it is a valid dataset filename
def validate_filename(filename):
    """
    Validate filename to ensure it is a valid dataset filename.
    """
    # general pattern to include and . file
    # pattern = re.compile('\w+$.\w+$') #TODO: Change patterns to match other file formats

    csv_file_pattern = r'.+\.csv$'
    image_file_pattern = r'.+\.(jpg|jpeg|png|gif)$'

    pattern = re.compile(f'{csv_file_pattern}|{image_file_pattern}')

    return bool(pattern.match(filename))

# This function will get info from filename
def get_info_from_filename(filename):
    """
    Extract file_name and file_format from filename
    """
    csv_file_pattern = r'.+\.csv$'
    image_file_pattern = r'.+\.(jpg|jpeg|png|gif)$'#TODO: Change patterns to match other file formats

    pattern = re.compile(f'{csv_file_pattern}|{image_file_pattern}')
    match = pattern.match(filename)
    file_name = match.group(1)
    file_format = match.group(2)

    return file_name, file_format

# This function will extract file format
def extract_file_format(file_name):
    """
    Extracts the file format from a file name.
    
    Parameters:
    file_name (str): The name of the file including its extension.
    
    Returns:
    str: The file format (extension) of the file.
    """
    # Split the file name by '.' and get the last part as the file format
    file_format = file_name.split('.')[-1]
    return file_format

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
    file_names, file_formats = [], []

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
            
                        # check to see if the file is a valid filename
                        if not validate_filename(original_file_1):
                            # Combine file and folder to one name a
                            raise ValueError(f'Invalid filename: {file}')
                        else:
                            file = original_file_1

                        file_name, file_format = get_info_from_filename(file)
                        # print(file_format)
                            
                        if file_format != 'csv' or file_format != 'jpg' or file_format != 'jpeg' or file_format != 'png' :
                            continue

                        paths.append(os.path.join(dataset_path, folder, original_file, data_folder, original_file_1))
                        labels.append(folder)
                        file_names.append(file)
                        file_formats.append(file_format)
            else:

                # check to see if the file is a valid filename
                if not validate_filename(original_file):
                    raise ValueError(f'Invalid filename: {file}')
                else:
                    file = original_file

                file_name, file_format = get_info_from_filename(file)
    
                paths.append(os.path.join(dataset_path, folder, original_file))
                labels.append(folder)
                file_names.append(file_name)
                file_formats.append(file_format)

    ref_df = pd.DataFrame({
        'path': paths,
        'label': labels,
        'file_name': file_names,
        'file_format': file_formats
    })

    ref_df = ref_df.astype({
        'path': 'string',
        'label': 'string',
        'file_name': 'string',
        'file_format': 'string'
    })

    return ref_df