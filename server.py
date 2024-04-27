import os
from flask import Flask, request, send_from_directory

# create folder for uploaded data
FOLDER = '.'
os.makedirs(FOLDER, exist_ok=True)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'GET':
        return '''<form enctype="multipart/form-data" action="" method="POST">
    <input type="hidden" name="MAX_FILE_SIZE" value="8000000" />
    <input name="uploadedfile1" type="file" /><br />
    <input name="uploadedfile2" type="file" /><br />
    <input name="uploadedfile3" type="file" /><br />
    <input type="submit" value="Upload File" />
</form>'''
    
    if request.method == 'POST':
        
        for field, data in request.files.items():
            if data.filename:
                data.save(os.path.join(FOLDER, "input.mp4"))
                
                print("Processing the video...")
                os.system("start Tracks.exe")
                while(1):
                    with open("state", "r") as statefile:
                        status = statefile.read()
                        if status == "ready":	# Written by the .exe
                            break
                with open("state", 'w'):
                    pass


        return "http://192.168.8.101:8080/get-files/output.mp4"


@app.route('/get-output', methods = ['GET','POST'])
def get_output():

    try:
        return send_from_directory('', 'ouput.mp4', as_attachment=True)
    except FileNotFoundError:
        abort(404)


@app.route('/get-files/<path:path>',methods = ['GET','POST'])
def get_files(path):

    """Download a file."""
    try:
        return send_from_directory('', path, as_attachment=True)
    except FileNotFoundError:
        abort(404)




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)