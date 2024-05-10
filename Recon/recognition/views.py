from django.shortcuts import render, HttpResponse, HttpResponse,redirect
from .models import *
from .forms import *
#from django.db.models import Q

from django.conf import settings
#from django.conf.urls.static import static

import requests
import os
import base64
import io
from PIL import Image



if not os.getcwd().lower().endswith('recon'):
    os.chdir(os.path.join(os.getcwd(), "Recon"))


'''def index(request):
    return render(request, "recognition/index.html")
'''

def index(request):
    return render(request, 'recognition/home.html')


def select_image(request):
    form = ProfileForm()
    if request.method == 'POST':
        return redirect('recognize')
        form = ProfileForm(request.POST,request.FILES)
        if form.is_valid():
            profile_image = Images.objects.create(
                image = form.cleaned_data.get("image"),
                updated = form.cleaned_data.get("updated")
            )
            profile_image.save()
            recognize(profile_image.image.name)

            return redirect('recognize')
    context={'form':form}
    return render(request,'recognition/select_image.html',context)



def recognize(request):

    if request.method == "POST":
        image = request.FILES.get('image')

        file_path = os.path.join(os.getcwd(), "recognition\static\images", image.name)
        with open(file_path, "wb+") as file:    
            file.write(image.read())

        # Handle the file
        response = None
        file = open(file_path, "rb")
        files = {
            'image': (image.name, file.read())
        }

        file.close()
        r = requests.post(url="http://127.0.0.1:8080", files=files)
        response = r.json()
        
        label = response.get('label')
        size = response.get('size')

        byte_image = base64.b64decode(response.get('image'))

        final_image = Image.frombytes("RGB", (size[1], size[0]), byte_image, "raw")
        # final_image = Image.open(io.BytesIO(byte_image))
        
        final_image.save(file_path)
            
        print(settings.MEDIA_ROOT, file_path)
        return render(request, "recognition/recognition.html", {"label": label, "src": "images/" + image.name})
    
    else:
            return render(request,'recognition/select_image.html')


