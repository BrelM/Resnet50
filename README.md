# Facial and Fingerprint Recognition Application

## Overview

This Flutter project aims to develop a facial recognition application with the added feature of fingerprint recognition for enhanced security. The application utilizes a PyTorch model (`model.pth`), specifically the ResNet50 architecture, to perform facial recognition, allowing users to capture images and predict the person's name along with their associated information. Additionally, the application will incorporate fingerprint recognition as an additional layer of authentication to ensure recognition accuracy.

## ResNet50 Architecture

The ResNet50 architecture is a convolutional neural network (CNN) that consists of 50 layers. It employs residual connections, which help alleviate the vanishing gradient problem and enable training of very deep networks. Here's a brief overview of each component of the ResNet50 architecture:

- **Convolutional Layers**: The network begins with a series of convolutional layers that extract features from the input images.

- **Residual Blocks**: These blocks contain multiple convolutional layers with shortcut connections (skip connections). The skip connections allow gradients to flow more easily during training, enabling the network to learn deeper representations.

- **Global Average Pooling**: After the convolutional layers, the network employs global average pooling to reduce the spatial dimensions of the features.

- **Fully Connected Layer**: The output of the global average pooling layer is fed into a fully connected layer, which produces the final predictions.

## Training Dataset

The ResNet50 model used in this application was trained on a personal dataset consisting of data science students in the computer science department of the University of Yaounde I. The dataset is located at the following Google Drive address: [Google Drive Address](https://drive.google.com/your_dataset).

## Features

- Facial Recognition:
    - Capture images of individuals.
    - Utilize the pre-trained PyTorch model (ResNet50) for facial recognition.
    - Predict the person's name and associated information.

- Fingerprint Recognition:
    - Integrate fingerprint recognition as an additional authentication method.
    - Enhance recognition accuracy and security.

## Installation

1. Clone the repository to your local machine:

    ```
    git clone https://github.com/BrelM/Resnet50.git
    ```

2. Ensure you have Flutter installed on your machine. If not, follow the official [Flutter installation guide](https://flutter.dev/docs/get-started/install).

3. Navigate to the project directory:

    ```
    cd resnet50
    ```

4. Install dependencies:

    ```
    flutter pub get
    ```

5. Run the application:

    ```
    flutter run
    ```

## Usage

1. Open the application on your device.

2. Navigate to the facial recognition feature.

3. Capture an image of the individual whose identity you want to verify.

4. The application will use the pre-trained PyTorch model (ResNet50) to predict the person's name and associated information.

5. Optionally, enable the fingerprint recognition feature for enhanced security.

6. Capture the individual's fingerprint using the device's fingerprint sensor.

7. The application will authenticate the user based on both facial and fingerprint recognition.

## Contributing

Contributions to this project are welcome and encouraged. If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any inquiries or support, feel free to contact [Juns Sashu] at [junssashu@gmail.com].
