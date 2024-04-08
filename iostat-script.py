import subprocess
import csv
import time
from datetime import datetime


INTERVAL = 2
SAMPLES = 10

# Obtenir la date et l'heure actuelles
current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Nom du fichier de sortie avec la date et l'heure actuelles
output_file = f"iostat_output_{current_datetime}.csv"

# Ouvrir un fichier CSV pour écrire les données
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Écrire l'en-tête du CSV
    writer.writerow(['Device', 'tps', 'kB_read/s', 'kB_wrtn/s', 'kB_read', 'kB_wrtn'])
    
    # Boucle pour effectuer les échantillonnages à intervalle régulier
    for sample in range(SAMPLES):
        # Exécuter la commande iostat pour obtenir les données
        process = subprocess.Popen(['iostat', '-d', str(INTERVAL), '1'], stdout=subprocess.PIPE)
        # Lire et décoder la sortie de la commande
        iostat_output = process.communicate()[0].decode('utf-8')
        # Diviser la sortie en sections basées sur le séparateur de double espace
        sections = iostat_output.strip().split('\n\n')
        
        # Parcourir chaque section
        for section in sections:
            # Diviser chaque section en lignes
            lines = section.strip().split('\n')
            # Ignorer la première ligne qui contient l'en-tête
            for line in lines[1:]:
                # Diviser chaque ligne en colonnes
                columns = line.split()
                # Écrire les données dans le fichier CSV
                writer.writerow(columns)
        
        # Afficher un message indiquant l'intervalle
        print(f"Échantillonnage {sample+1}/{SAMPLES} effectué. Attente de {INTERVAL} secondes avant le prochain échantillonnage...")
        
        # Attendre l'intervalle spécifié avant le prochain échantillonnage
        time.sleep(INTERVAL)

print(f"Données iostat enregistrées dans {output_file}")
