from django.shortcuts import render, HttpResponse

import requests
import os

os.chdir(os.path.join(os.getcwd(), "Recon"))


def index(request):
    return render(request, "recognition/index.html")



def recognize(request):

    if request.method == "POST":
        image = request.FILES.get('image')

        file_path = os.path.join(os.getcwd(), "images", image.name)
        with open(file_path, "wb+") as file:
            file.write(image.read())

        # Handle the file
        response = None
        with open(file_path, "rb") as file:
            files = {
                'image': (image.name, file.read())
            }

            r = requests.post(url="http://127.0.0.1:8080", files=files)
            response = r.content.decode()
            print(response)
        return render(request, "recognition/recognition.html", {"label": response})



