###################################################################################################################
#
#   OBJECTIF:  Présenter les statistiques descriptives des variables cibles potentielles:
#                   Revenue Actual, Surprise(computedSurprise à la publication), ComputedSurprise, RevenueSeasonalitygrowthActual
#              Analyser leur corrélation avec leur estimateurs 
#                   Revenue Mean, PreviousSeasonalSurprise, RevenueSeasonalitygrowthEstimate
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

def path(file):
    return "/Users/isabelledebry/Documents/TFENOEMIE/"+file

sheet_name = 0 
header = 0 # The header is the first row


output = pd.read_excel(path("etapePreparation/output.xlsx"), sheet_name = sheet_name, header = header)
print(len(output))
output = output[output['Surprise'].notna()]
print(len(output))
"""
sns.set()
sns.pairplot(output, vars=['Revenue - Actual','Revenue - Mean'],kind='reg')
plt.show()
r=output['Revenue - Actual'].describe()
print(r)
r=output['Revenue - Mean'].describe()
print(r)
print("Coef correlation Revenue Actual- Revenue Mean")
print (sc.stats.pearsonr(output['Revenue - Actual'], output['Revenue - Mean']))
print("Spearman Coef correlation ")
print(sc.stats.spearmanr(output['Revenue - Actual'], output['Revenue - Mean']))
fig, ax = plt.subplots()
sns.histplot(output, x='Revenue - Actual', stat='probability').set(title='Revenue (Actual) Probability')
plt.show()

sns.pairplot(output, vars=['ComputedSurprise','PreviousSeasonSurprise'],kind='reg')
plt.show()
r=output['ComputedSurprise'].describe()
print(r)
r=output['PreviousSeasonSurprise'].describe()
print(r)
print("Coef correlation ComputedSurprise - PreviousSeasonSurprise")
print (sc.stats.pearsonr(output['ComputedSurprise'], output['PreviousSeasonSurprise']))
print("Spearman Coef correlation ")
print(sc.stats.spearmanr(output['ComputedSurprise'], output['PreviousSeasonSurprise']))
fig, ax = plt.subplots()
sns.histplot(output, x='ComputedSurprise', stat='probability').set(title='computedSurprise Probability')
"""
sns.pairplot(output, vars=['capComputedSurprise','PreviousSeasonSurprise'],kind='reg')
plt.show()
r=output['capComputedSurprise'].describe()
print(r)
r=output['PreviousSeasonSurprise'].describe()
print(r)
print("Coef correlation capComputedSurprise - PreviousSeasonSurprise")
print (sc.stats.pearsonr(output['capComputedSurprise'], output['PreviousSeasonSurprise']))
print("Spearman Coef correlation ")
print(sc.stats.spearmanr(output['capComputedSurprise'], output['PreviousSeasonSurprise']))
fig, ax = plt.subplots()
sns.histplot(output, x='capComputedSurprise', stat='probability').set(title='Surprise Probability')


plt.show()
"""
sns.pairplot(output, vars=['growthSeasonalityActual','growthSeasonalityEstimate'],kind='reg')
plt.show()
r=output['growthSeasonalityActual'].describe()
print(r)
r=output['growthSeasonalityEstimate'].describe()
print(r)
print("Coef correlation growthSeasonalityActual")
print (sc.stats.pearsonr(output['growthSeasonalityActual'], output['growthSeasonalityEstimate']))
print("Spearman Coef correlation ")
print(sc.stats.spearmanr(output['growthSeasonalityActual'], output['growthSeasonalityEstimate']))
fig, ax = plt.subplots()
sns.histplot(output, x='growthSeasonalityActual', stat='probability').set(title='Seasonal Revenue growth (actual) Probability')
plt.show()

sns.pairplot(output, vars=['growthSeasonalityActual','Revenue - Mean'],kind='reg')
plt.show()
r=output['growthSeasonalityActual'].describe()
print(r)
r=output['Revenue - Mean'].describe()
print(r)
print("Coef correlation growthSeasonalityActual")
print (sc.stats.pearsonr(output['growthSeasonalityActual'], output['Revenue - Mean']))
print("Spearman Coef correlation ")
print(sc.stats.spearmanr(output['growthSeasonalityActual'], output['Revenue - Mean']))
fig, ax = plt.subplots()
sns.histplot(output, x='growthSeasonalityActual', stat='probability').set(title='Seasonal Revenue growth (actual) Probability')
plt.show()
"""