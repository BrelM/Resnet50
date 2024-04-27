from django.shortcuts import render, HttpResponse




def index(request):
    return render(HttpResponse("Vous êtes à l'accueil", "recongnition/index.html"))



def recognize(request):

    if request.method == "POST":
        image = request.FILES.get['image']

        # Handle the file



