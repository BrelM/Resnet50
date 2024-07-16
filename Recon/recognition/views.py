from django.shortcuts import render, HttpResponse, HttpResponse,get_object_or_404,redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse

from .models import *
from .forms import *
from .models import Nom

#from django.conf.urls.static import static

import pickle
import requests
import os
import base64
from datetime import datetime
from PIL import Image
import json




THRESHOLD = 25
path_to_voters_file = "../voters.data"



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


@csrf_exempt
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

        # image = request.FILES.get('real-image')
        # file_name = image.name
        
        data = request.body.decode('utf-8')
        image_data = json.loads(data).get('image')

        # Removing the header of the base64 string
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]

        # Decode the base64 string
        img_data = base64.b64decode(imgstr)

        # Creating an unique file name
        file_name = f'snapshot_{datetime.now().strftime("%d%m%Y_%H%M%S")}.{ext}'

        # Storing the image
        file_path = os.path.join(os.getcwd(), "recognition/static/images", file_name)
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
        
        char = response.get('vector') # vector is actually a tensor of floats (characteristics vector)
        size = response.get('size')


        label = "No matches found."
        if not isinstance(char, str):
            char = char[0]
            features = char
            with open(path_to_voters_file, "rb") as voters_file:
                voters = pickle.Unpickler(voters_file).load()
                
                # Checking compatibility with stored individuals
                name, status, error = "", "", 1e36
                
                for nam, stat in voters.items():
                    # We simply evaluate the euclidian distance between stored voters' characteristics and the just-extracted ones.
                    temp_error = euclidian_dist(features, stat["features"])
                    if temp_error < error:
                        name, status, error = nam, stat["voted"], temp_error

                
                # If there's a match, procede to vote
                print(error)
                if error < THRESHOLD:
                    if not status:
                        voters[name]["voted"] = True
                        with open(path_to_voters_file, "wb") as voters_output:
                            pickle.Pickler(voters_output).dump(voters)

                        label = "The voter is recognized as {} with an error of {:2f}.\nStatus changed to 'Has voted'.".format(name, error)
        
                        # Unlock door for 3 seconds

                    else:
                        
                        # For testing purpose only
                        # voters[name]["voted"] = False
                        # with open(path_to_voters_file, "wb") as voters_output:
                        #     pickle.Pickler(voters_output).dump(voters)

                        label = "The voter is recognized as {} with an error of {:2f} and has already voted.".format(name, error)
        
                        # Keep the door locked

                
                else:
                    label = "No matches found."



        #     # Checking compatibility with stored individuals
        #     label, score = "", 1e3
            
        #     for elector in Nom.objects.all():
        #         # We simply evaluate the euclidian distance between stored voters' characteristics and the just-extracted ones.
        #         calc = euclidian_dist(json.loads(elector.char), char)
        #         if calc < score: # We store the most compatible voter 
        #             label, score = elector.nom, calc
        #     print(len(char))

        #     if score > THRESHOLD:
        #         label = "No matches found."


        # # If there's a match, procede to vote
        # if label != "No matches found.":
        #     elector = Nom.objects.get(nom=label)
            
        #     if not elector.a_vote:
        #         elector.a_vote = True
        #         elector.save()
        #         label = f"This individual is recognized as {label}. Status changed to 'already voted'.<br>Dissimilarity score: {score:.3f}"

        #         # Unlock door for 3 seconds

        #     else:
        #         label = f"This individual is recognized as {label} and has already voted.<br>Dissimilarity score: {score:.3f}"

        #         # Keep the door locked



        byte_image = base64.b64decode(response.get('image'))

        final_image = Image.frombytes("RGB", size, byte_image, "raw")
        # final_image = Image.open(io.BytesIO(byte_image))
        
        final_image.save(file_path)
        
        return JsonResponse({'status':'success', 'label': label})
        # return render(request, "recognition/select_image.html", {"label": label, "src": "images/" + file_name,  "show_vote_button": show_vote_button})
    
    return render(request, "recognition/select_image.html")




def register(request):
    if request.method == "GET":
        
        return render(request, "recognition/register_individual.html")
    
    else:
        
        # Recupération de l'image et du l'étiquette de l'individu
        image = request.FILES.get('image')
        
        if not image:
            image = request.POST.get('image_input')

            if not image:
                return render(request, "recognition/register_individual.html", {"message":"An image shall be provided!", "error":True})


            # Removing the header of the base64 string
            format, imgstr = image.split(';base64,')
            ext = format.split('/')[-1]

            # Decode the base64 string
            img_data = base64.b64decode(imgstr)

            # Creating an unique file name
            file_name = f'snapshot_{datetime.now().strftime("%d%m%Y_%H%M%S")}.{ext}'


        else:
            img_data = image.read()
            file_name = image.name


        name = request.POST.get('name')

        if not name:
            return render(request, "recognition/register_individual.html", {"message":"A name shall be provided!", "error":True})


        # Storing the image
        file_path = os.path.join(os.getcwd(), "recognition/static/images", file_name)
        with open(file_path, "wb") as file:
            file.write(img_data)


        # Handle the file
        response = None
        file = open(file_path, "rb")
        files = {
            'image': (name, file.read())
        }

        file.close()
        r = requests.post(url="http://127.0.0.1:8080", files=files)
        response = r.json()
        
        char = response.get('vector') # vector is actually a tensor of floats (characteristics vector)
        size = response.get('size')

        if not isinstance(char, str):
            char = char[0]

            # Sauvegarde du vecteur de caratéristiques
            # Nom.objects.create(nom=name, char=json.dumps(char))
            default_name = name
            features = char

            try:    # If the file exists

                with open(path_to_voters_file, "rb") as voters_file:
                    voters = pickle.Unpickler(voters_file).load()
                    voters[default_name] = {"features" : features, "voted" : False}

                    with open(path_to_voters_file, "wb") as voters_output:
                        pickle.Pickler(voters_output).dump(voters)

            except:     # If the file doesn't exist yet
                voters = {default_name : {"features" : features, "voted": False}}
                with open(path_to_voters_file, "wb") as voters_output:
                    pickle.Pickler(voters_output).dump(voters)

            return render(request, "recognition/register_individual.html", {"message":"Individual successfully registered", "error":False})
        
        return render(request, "recognition/register_individual.html", {"message":"Failed to register the individual.The face was not clear enough.", "error":True})
        




def euclidian_dist(vect1:list, vect2:list) -> float:
    '''
        Compute the euclidian distance over two vector of floats.
    '''

    if len(vect1) != len(vect2):
        raise ValueError(f"Lenght of the vectors should be the same. but vector 1 has lenght {len(vect1)} while vector 2 has lenght {len(vect2)}.")

    v = 0
    for _ in range(len(vect1)):
        v += (vect1[_] - vect2[_])**2

    return v ** 0.5







