# Python Code Description

This script provides an extensive framework for deep learning tasks, focusing on image preprocessing, model training, and evaluation using PyTorch and associated libraries. It handles data loading, preprocessing, model training, evaluation, and saving results for different models including ResNet50, UNet, and ConvLSTM.

## Main Steps

### Imports
- Common libraries for handling arrays, dataframes, and visualization (e.g., `numpy`, `pandas`, `matplotlib`, `seaborn`).
- Deep learning and image processing libraries (e.g., `torch`, `torchvision`, `PIL`).
- Machine learning utilities from `sklearn` for data splitting and performance metrics.
- Custom modules for specific network architectures (e.g., `layers`, `unet_parts`).

### Environment Setup
- Configures PyTorch for optimal performance on available hardware (GPU or Apple's MPS).
- Defines transformations for image preprocessing.

### Data Preparation
- Functions to collect image paths and load datasets into PyTorch `DataLoader`s.
- Data is split into training, validation, and test sets, and loaded with specified transformations.

### Model Training
- Multiple models are prepared and trained:
  - **ResNet50** for basic image classification or regression tasks.
  - **UNet** tailored for image segmentation tasks.
  - **ConvLSTM** designed for sequential image data processing.
- Training function includes detailed logs and supports gradient accumulation for effective memory management.

### Evaluation and Reporting
- Functions to evaluate model performance using standard metrics such as accuracy, F1 score, precision, and recall.
- Additional evaluation for classification tasks includes ROC curves and confusion matrices.
- Results are saved both graphically and textually.

### Utility Functions
- Includes utilities for displaying images with predictions, generating detailed classification reports, and managing large datasets efficiently.

### Usage
This script is structured to be highly modular, suitable for various deep learning tasks involving image data. It facilitates easy switching between different models and tasks, making it ideal for experimental setups and research.

### Notes
- The script assumes the existence of certain directories and files, with paths defined at the beginning of the script.
- It heavily utilizes command-line arguments for configuration, making it flexible for batch processing and automation in research environments.


## Each class


### ForecastingDataset Class

The `ForecastingDataset` class is designed as a custom dataset handler for PyTorch, managing sequences of images for applications such as video frame prediction or time-series image analysis. This class inherits from PyTorch's `Dataset`, making it suitable for use with PyTorch utilities requiring a dataset object.

#### Constructor: `__init__(self, root_dir, transform=None, sequence_length=1, target_samples=None)`
- **Parameters:**
  - `root_dir`: String specifying the directory path containing the images.
  - `transform`: Optional callable that applies a transformation to each image in a sequence, useful for preprocessing images to fit neural network input requirements.
  - `sequence_length`: Integer indicating the number of images in each sequence, setting how many consecutive images are considered one sequence.
  - `target_samples`: Optional integer defining a target number of sequences to generate, useful for achieving balanced training when the data does not divide into the desired number of sequences naturally.

- **Functionality:**
  - Lists and sorts all non-hidden files in `root_dir` to ensure consistent sequence order.
  - Constructs full paths for these files.
  - Adjusts the sequence of images based on `target_samples`, using random sampling with or without replacement to meet the specified sequence count, thereby ensuring the generation of the required number of sequences.

#### Method: `__len__(self)`
- **Functionality:** Returns the total number of unique sequences available in the dataset, calculated as the total number of images minus the sequence length plus one. This ensures each sequence comprises exactly `sequence_length` images.

#### Method: `__getitem__(self, idx)`
- **Functionality:** Retrieves a specific sequence by its index (`idx`), which involves:
  - Selecting a subset of image paths to form the sequence.
  - Opening and optionally transforming each image in the sequence.
  - Returning the first image as `input_image` and the last image as `target_image`, typical for tasks predicting the next frame given previous frames.

#### Static Method: `adjust_sequence_distribution(image_paths, sequence_length, target_samples)`
- **Functionality:** Adjusts the distribution of sequences to meet a specific count (`target_samples`), either by oversampling (with replacement) or undersampling (without replacement), based on the availability of sequences relative to the target.

This class serves as a versatile tool for preparing datasets of image sequences for machine learning models in PyTorch, especially in scenarios where sequential data processing is crucial, such as video analysis or temporal image data prediction.
