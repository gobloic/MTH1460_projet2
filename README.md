
# MTH1460_projet2

 - **Dinosaure.py** : mécaniques de déplacement
 - **Thescelosaurus.py** : hérite de Dinosaure.py, spécialise stratégies de fuite et paramètres physiques (rayon min, vitesse max)
 - **Velociraptor.py** : hérite de Dinosaure.py, spécialise stratégies de poursuite et paramètres physiques
 - **Course.py** : boucle principale, où vivent les objets proie (Thescelosaurus) et prédateurs (1 ou 2 Velociraptor) pendant 15s. Au cours des 15s, à chaque pas de temps, 
            les positions sont mises à jour et les destinations de chacun sont adaptées.
