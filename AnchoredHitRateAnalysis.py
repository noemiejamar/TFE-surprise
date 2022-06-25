###################################################################################################################
#
#   OBJECTIF: Analyse des anchored Hit rates par des regroupements
#              par date : histogramme du nombre de cpy avec anchored hit rate positif par date
#              par cpy  : histogramme du nombre de date avec anchored hit rate positif par cpy
#   PARAMETRISATION: adapter la fonction path 
#   INPUT:   ../fichierwithPredOrHit/test_hit_rate.xlsx
#            
#   OUTPUTS:   affichage des différentes métriques et graphiques 
#              
###################################################################################################################

import pandas as pd
import numpy as np
from numpy  import *
import datetime as dt


import sklearn.metrics as metrics
import matplotlib
from matplotlib import pyplot as plt
import seaborn as sns


def path(file):
    return "/Users/isabelledebry/Documents/TFENOEMIE/"+file

sheet_name = 0 
header = 0 # The header is the first row

test = pd.read_excel(path("fichierwithPredOrHit/test_21_hit_rate.xlsx"), sheet_name = sheet_name, header = header)





dataframe2 =pd.DataFrame(test['anchored_hit_rate_by_previous']).describe()
fig, ax = plt.subplots()
extract=test[['anchored_hit_rate_by_previous','cpy']].groupby('cpy').sum()
sns.histplot(extract[['anchored_hit_rate_by_previous']],stat='probability',ax=ax).set(title='sum positive anchored_hit_rate_by_previous by cpy')
plt.show()
print("anchored_hit_rate_by_previous")
print(dataframe2)
#print(100*dataframe2.freq/dataframe2.count)
dataframe2 =pd.DataFrame(test['anchored_hit_rate']).describe()
fig, ax = plt.subplots()
extract=test[['anchored_hit_rate','cpy']].groupby('cpy').sum()
sns.histplot(extract['anchored_hit_rate'],stat='probability',ax=ax).set(title='sum positive anchored_hit_rate_by_surprise by cpy')
plt.show()
print("anchored_hit_rate")
print(dataframe2)
#print(100*dataframe2.freq/dataframe2.count)
dataframe2 =pd.DataFrame(test['anchored_hit_by_RA_pred']).describe()
fig, ax = plt.subplots()
extract=test[['anchored_hit_by_RA_pred','cpy']].groupby('cpy').sum()
sns.histplot(extract['anchored_hit_by_RA_pred'],stat='probability',ax=ax).set(title='sum anchored_hit_by_RA_pred by cpy')
plt.show()
print("anchored_hit_by_RA_pred")
print(dataframe2)
#print(100*dataframe2.freq/dataframe2.count)
dataframe2 =pd.DataFrame(test['anchored_hit_by_G_pred']).describe()
fig, ax = plt.subplots()
extract=test[['anchored_hit_by_G_pred','cpy']].groupby('cpy').sum()
sns.histplot(extract['anchored_hit_by_G_pred'],stat='probability',ax=ax).set(title='sum anchored_hit_by_G_pred by cpy')
plt.show()
print("anchored_hit_by_G_pred")
print(dataframe2)
#print(100*dataframe2.freq/dataframe2.count)


