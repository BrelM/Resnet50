# User manual for the voting system app
### For a local setup


## Hardware requirements:
1. Ubuntu 20.X LTS or above / Windows 10 or above
2. At least 4GB of RAM
3. 1 GB of storage
4. Internet access for web application style sheets loading
5. A computer with a webcam and installed compatible drivers

## Software requirements
1. A back-end that consists of a processing server running the model. 
* Python 3.10 (due building wheel compatibility with Tensorflow 2.10) 
* Conda/miniconda environment 
* Tensorflow version 2.10.0 
* Pillow 
* Opencv-python 
* Flask 
* Flask_json 
* Numpy 
2. A web application in a MVC architecture. For now, this should be set up on the same environment as the back. 
* Python 3.12 
* Pillow 
* Django

## Launching the components
1. The back: python server3.0.py  # using the 3.10 python version of course 
2. The front: py Recon/manage.py runserver (web app can be accessed via http:127.0.0.1:8000)

## Enrolment
1. On the top left corner, click on  'Register and individual'
For the following steps, make sure to be in a correctly lighted place and Authorize the web application to use your webcam.

2. In the page that displays, click 'Capture' or load 

