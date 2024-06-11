from django.core.management.base import BaseCommand
from ...models import Nom

class Command(BaseCommand):
    help = 'Importe les noms depuis un fichier'

    def handle(self, *args, **options):
        with open('noms.txt', 'r') as file:
            for line in file:
                Nom.objects.create(nom=line.strip())
        self.stdout.write(self.style.SUCCESS('Importation des noms terminée.'))