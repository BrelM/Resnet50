# User manual for the voting system app
### For a local setup


## Hardware requirements:
* Windows 10 or above (the development was made on a Linux based environment but, the apps were designed to run on a user-friendly environment such as Windows)
* At least 4GB of RAM
* 1 GB of storage
* Internet access for web application style sheets loading
* A computer with a webcam and installed compatible drivers

## Software requirements
1. A back-end that consists of a processing server running the model.
* Miniconda3 environment 
* Tensorflow version 2.10.0 
* Pillow 
* Opencv-python 
* Flask 
* Flask_json 
* Numpy
* tensorflow-2.10.0-cp310-cp310-win_amd64.whl compiled distribution downloadable here: https://pypi.org/project/tensorflow/2.10.0/#files

2. A web application in a MVC architecture. For now, this should be set up on the same environment as the back. 
* Python 3.12
* Pillow 
* Django

### Launching the processing server and the web application

#### The back: 
1. Install Miniconda3 (and make sure to accept the 'Add to the PATH' option)
2. Open a terminal and execute the following commands:

conda create -n tf python=3.10
conda activate tf
python -m pip install path/to/tensorflow-2.10.0-cp310-cp310-win_amd64.whl
python -m pip install pillow opencv-python Flask Flask-JSON numpy

3. Type: python server3.0.py

#### The front: 
1. Install python 3.12 and check 'Add to the PATH' 
2. py install Django pillow
3. Navigate to the project directory and execute: py Recon/manage.py runserver
(The web app can be accessed via http:127.0.0.1:8000)


## Enrollment
1. On the top left corner, click on  'Register and individual'
For the following steps, make sure to be in a correctly lighted place and Authorize the web application to use your webcam.
You'll also have to stand right in front of the webcam in a straight position.

2. In the page that displays, click 'Capture' or 'Choose File' buttons to provide a capture of your face.
3. Enter your name in the text field below and then click 'Send'
4. If everything went well, you should see a message displaying below saying that your were registered successfully


## Authentication
1. Now when authenticating people, going from the home page, click on 'Start voting'
The voters should be in the same environmental situation as during the enrollment.
2.  A capture of the standing voter will be automatically taken and process every 3 seconds
3. Two cases arise:
* The voter is recognized: His/Her status changes to 'Already voted' and will always be recognized as so from now on. The room access is given the first time.
* The voter is not recognized: The room access isn't allowed





