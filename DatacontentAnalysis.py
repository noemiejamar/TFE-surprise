###################################################################################################################
#
#   OBJECTIF:  Donner les dimensions du contenu du journal et des fichiers d'apprentissages
#               nbr de lignes, nbr d'entreprises,nbr lignes par  entreprise,
#           	nbr de date du journal,	première date,	dernière date,	premier (test) / dernier (train) quadrimestre,
#           	nbr d'association entreprise - quadrimestre, nbr de jour par association entreprise - quadrimestre
#   PARAMETRISATION: adapter la fonction path 
#   INPUT:   .../etapePreparation/output.xlsx  : journal 
#
#   OUTPUTS:   affichage des différentes métriques
###################################################################################################################

import pandas as pd
import numpy as np
from numpy  import *
import datetime as dt


import matplotlib
from matplotlib import pyplot as plt
from sklearn.neural_network import MLPRegressor

import tensorflow as tf
# use keras API
from tensorflow import keras
from tensorflow.keras import layers
import seaborn as sns

def path(file):
    return "/Users/isabelledebry/Documents/TFENOEMIE/"+file

def print_infos(journal):
    print("nombre d element du journal:")
    print(len(journal))
    print("nombre de companies: ")
    print(journal.groupby(['cpy'])['cpy'].count())
    print(journal.groupby(['cpy'])['cpy'].count().mean())
    print("nbr Date")
    print(journal.groupby(['Date'])['Date'].count())
    print("periods")
    print(journal.groupby(['Period End Date'])['Period End Date'].count())
    print("periods par cpy")
    print(journal.groupby(['Period End Date','cpy']).size())
    print("nbr moyen de periods par cpy")
    print(journal.groupby(['Period End Date','cpy'])['Period End Date'].count().mean())


print("output")
journal= pd.read_excel(path("etapePreparation/output.xlsx"))
print_infos(journal)
print("train_19")
journal= pd.read_excel(path("fichiersApprentissage/train_19.xlsx"))
print_infos(journal)
print(journal[journal['Period End Date']=='2019-11-30'].groupby(['cpy'])['cpy'].count())

print("train_20")
journal= pd.read_excel(path("fichiersApprentissage/train_20.xlsx"))
print_infos(journal)
print(journal[journal['Period End Date']=='2020-11-30'].groupby(['cpy'])['cpy'].count())
print("train_19_20")
journal= pd.read_excel(path("fichiersApprentissage/train_19_20.xlsx"))
print_infos(journal)
print("test_20")
journal= pd.read_excel(path("fichiersApprentissage/test_20.xlsx"))
print(journal[journal['Period End Date']=='2019-11-30'].groupby(['cpy'])['cpy'].count())
print_infos(journal)
print("test_21")
journal= pd.read_excel(path("fichiersApprentissage/test_21.xlsx"))
print_infos(journal)
print(journal[journal['Period End Date']=='2020-11-30'].groupby(['cpy'])['cpy'].count())


print("train")
journal= pd.read_excel(path("fichiersApprentissage/train.xlsx"))
print_infos(journal)
print(journal[journal['Period End Date']=='2019-11-30'].groupby(['cpy'])['cpy'].count())
print("test")
journal= pd.read_excel(path("fichiersApprentissage/test.xlsx"))
print_infos(journal)
