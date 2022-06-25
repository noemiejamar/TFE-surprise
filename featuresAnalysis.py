###################################################################################################################
#
#   OBJECTIF:  Présenter les statistiques descriptives des variables prédictives caractéristiques potentielles:
#                   DayGap, 
#                   Revenue Mean, PreviousSeasonalSurprise, growthSeasonalityEstimate
#                   Year-EBIT-Mean, previous season Revenue Actual, previous season EBIT
#
#   PARAMETRISATION: adapter la fonction path 
#   INPUT:   ../etapePreparation/output
#            
#   OUTPUTS:   affichage des différentes métriques et graphiques 
#              
###################################################################################################################
import pandas as pd
import numpy as np
import scipy as sc
from numpy  import *
import matplotlib
from matplotlib import pyplot as plt
import seaborn as sns
from scipy.stats.mstats import winsorize
from scipy.stats import pearsonr,spearmanr

sheet_name = 0 
header = 0 # The header is the first row
def path(file):
    return "/Users/isabelledebry/Documents/TFENOEMIE/"+file

output = pd.read_excel(path("etapePreparation/output.xlsx"), sheet_name = sheet_name, header = header)
print(len(output))
output = output[output['Surprise'].notna()]
print(len(output))


r=output['Revenue - Mean'].describe()
print(r)
r=output['DayGap'].describe()
print(r)
r=output['growthSeasonalityEstimate'].describe()
print(r)
r=output['PreviousSeasonSurprise'].describe()
print(r)
r=output['Year-EBIT-Mean'].describe()
print(r)
r=output['previous season Revenue Actual'].describe()
print(r)
r=output['previous season EBIT'].describe()
print(r)


