from django.shortcuts import render, HttpResponse, HttpResponse,get_object_or_404,redirect
from .models import *
from .forms import *
from .models import Nom

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

def voters(request):
    return render(request,'recognition/voters.html')




def select_image(request):
    form = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile_image = form.save()
            return redirect('recognize', image_name=profile_image.image.name)
    
    context = {'form': form}
    return render(request, 'recognition/select_image.html', context)



def nom_detail(request, nom_id):
    nom = get_object_or_404(Nom, id=nom_id)
    return render(request, 'nom/detail.html', {'nom': nom})


def recognize(request):
    show_vote_button = False

     # Traitement du vote
    '''nom = Nom.objects.get(nom=label)
    if request.POST.get('vote'):
        if not nom.a_vote:
            nom.a_vote = True
            nom.save()
            vote_message = "Votre vote a été enregistré."
        else:
            vote_message = "Désolé, vous avez déjà voté."
    else:
        show_vote_button = True

    '''

    vote_message = "Vous etes pas reconnu dans le systeme" 
    

    if request.GET.get('label'):
        label=request.GET.get('label')
        #nom = Nom.objects.get(nom=label)
        users=Nom.objects.all()
        nom = users.filter(nom = label)
      
        src = request.GET.get('src')

        if nom is not None and len(nom)>0:
            if not nom[0].a_vote:
                nom[0].a_vote = True
                nom[0].save()
                vote_message = "Votre vote a été enregistré."
            else:
                vote_message = "Désolé, vous avez déjà voté."

        return render(request, "recognition/select_image.html", {"label": label,"src": src, "vote_message": vote_message})


    if request.method == "POST":

        show_vote_button = True

        if 'image' in request.FILES:

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

            final_image = Image.frombytes("RGB", size, byte_image, "raw")
            # final_image = Image.open(io.BytesIO(byte_image))
            
            final_image.save(file_path)
            
            print(settings.MEDIA_ROOT, file_path)
            return render(request, "recognition/select_image.html", {"label": label, "src": "images/" + image.name,  "show_vote_button": show_vote_button})
        
        
        
        

        if 'image' in request.POST:
            

            image_data = request.POST['image']
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            img_data = base64.b64decode(imgstr)


            file_name = "captured_image." + ext
            file_path = os.path.join(os.getcwd(), "recognition\static\images", file_name)
            with open(file_path, "wb") as file:
                file.write(img_data)

            

            # Handle the file
            response = None
            file = open(file_path, "rb")
            files = {
                'image': (file_name, file.read())
            }

            file.close()
            r = requests.post(url="http://127.0.0.1:8080", files=files)
            response = r.json()
            
            label = response.get('label')
            size = response.get('size')

            byte_image = base64.b64decode(response.get('image'))

            final_image = Image.frombytes("RGB", size, byte_image, "raw")
            # final_image = Image.open(io.BytesIO(byte_image))
            
            final_image.save(file_path)
            
            print(settings.MEDIA_ROOT, file_path)
            return render(request, "recognition/select_image.html", {"label": label, "src": "images/" + file_name,  "show_vote_button": show_vote_button})
        
        
            

    return render(request, "recognition/select_image.html")


'''def voter(request, label):
     
    nom = Nom.objects.get(nom=label)
    image = request.session.get('image')
    
    # Vérifier si la personne a déjà voté
    if not nom.a_vote:
        nom.a_vote = True
        nom.save()
        
        # Définir un message pour indiquer que le vote a été enregistré
        vote_message = "Votre vote a été enregistré."
    else:
        vote_message = "Desolé, vous avez deja voté"
    
    #return redirect('liste_noms', extra_context={'vote_message': vote_message})
    return render(request, "recognition/select_image.html", { "label": label, "src": "images/" + image.name,  "show_vote_button": show_vote_button,"vote_message": vote_message})
  '''  
    