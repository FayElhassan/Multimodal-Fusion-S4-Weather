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


## Each class and functionality


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

### create_data_loaders Function

The `create_data_loaders` function is designed to automate the process of setting up PyTorch `DataLoader`s for training, validation, and testing. This function handles the splitting of image data into appropriate subsets and ensures that each subset is loaded with a specified batch size and optional transformations.

#### Function Signature: 
`create_data_loaders(data_dir, batch_size, train_val_test_split=(0.7, 0.2, 0.1), transform=None)`

#### Parameters:
- `data_dir`: String specifying the directory containing image files.
- `batch_size`: Integer defining the number of images per batch in the data loaders.
- `train_val_test_split`: Tuple indicating the proportion of data to be used for training, validation, and testing respectively.
- `transform`: Optional callable that applies transformations to the images (e.g., resizing, normalization).

#### Functionality:
- **Data Collection**:
  - Collects paths for all `.png` files located in the specified `data_dir`.
- **Data Splitting**:
  - Initially splits the image paths into training and combined validation/testing sets based on the training set size specified in `train_val_test_split[0]`.
  - Further splits the combined validation/testing set into validation and testing sets. The size of the validation set is determined by the relative proportions of validation and testing sizes provided in `train_val_test_split`.
- **Dataset Creation**:
  - Instantiates `PNGDataset` objects for training, validation, and testing datasets. Each dataset is initialized with its respective image paths and the provided transformation (if any).
- **DataLoader Setup**:
  - Initializes `DataLoader` objects for the training, validation, and testing datasets. The training loader is set to shuffle the data to ensure random distribution during training, while the validation and testing loaders do not shuffle data.

#### Return Value:
- Returns a tuple containing the training, validation, and testing `DataLoader`s.

This function streamlines the process of preparing data for machine learning models in PyTorch, ensuring that data is appropriately shuffled, batched, and transformed as required. It is especially useful for projects where data management and efficient loading are crucial for model performance and evaluation.

### train_model Function

The `train_model` function orchestrates the training process for a PyTorch model, utilizing both a training set and a validation set to evaluate model performance across epochs. This function is designed to handle gradient accumulation, a technique useful for effectively managing memory on hardware with limited capacity.

#### Function Signature: 
`train_model(model, train_loader, val_loader, criterion, optimizer, num_epochs, grad_accumulation_steps=1)`

#### Parameters:
- `model`: The PyTorch model to be trained.
- `train_loader`: DataLoader containing the training dataset.
- `val_loader`: DataLoader containing the validation dataset.
- `criterion`: The loss function used to evaluate a model's predictions against the true values.
- `optimizer`: The optimization algorithm used to update the model's weights.
- `num_epochs`: The number of times to iterate over the entire training dataset.
- `grad_accumulation_steps`: The number of forward/backward passes to accumulate gradients before performing a single optimization step. This parameter is crucial for handling large models or batches that would otherwise consume too much memory.

#### Functionality:
- **Device Setup**:
  - Determines the appropriate device (MPS, CUDA, or CPU) depending on availability, ensuring optimal model training performance.
- **Training Loop**:
  - Iterates over the number of epochs, each time passing through the entire training dataset.
  - For each batch of data:
    - Performs a forward pass to compute the loss.
    - Scales the loss according to the number of gradient accumulation steps.
    - Conducts a backward pass to compute gradients.
    - Updates the model weights conditionally after a specified number of accumulation steps, then resets gradients to zero.
  - Calculates and logs the training loss after each epoch.
- **Validation Phase**:
  - Evaluates the model on the validation dataset without updating model weights, which helps in monitoring overfitting during training.
  - Computes and logs the validation loss.

#### Return Value:
- Returns the trained model, allowing further analysis or additional training if necessary.

This function is key for implementing effective training routines in PyTorch, particularly when dealing with large datasets or models that require careful memory management. It ensures that the model learns effectively from the training data while monitoring its performance on unseen validation data.
