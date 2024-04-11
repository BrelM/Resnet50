# Facial and Fingerprint Recognition Application

## Overview

This Flutter project aims to develop a facial recognition application with the added feature of fingerprint recognition for enhanced security. The application utilizes a PyTorch model (`facial_recognition_by_me.pth`) to perform facial recognition, allowing users to capture images and predict the person's name along with their associated information. Additionally, the application will incorporate fingerprint recognition as an additional layer of authentication to ensure recognition accuracy.

## Features

- Facial Recognition:
    - Capture images of individuals.
    - Utilize the pre-trained PyTorch model for facial recognition.
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

4. The application will use the pre-trained PyTorch model to predict the person's name and associated information.

5. Optionally, enable the fingerprint recognition feature for enhanced security.

6. Capture the individual's fingerprint using the device's fingerprint sensor.

7. The application will authenticate the user based on both facial and fingerprint recognition.

## Contributing

Contributions to this project are welcome and encouraged. If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any inquiries or support, feel free to contact [Juns Sashu] at [junssashu@gmail.com].
