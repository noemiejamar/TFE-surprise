###################################################################################################################
#
#   OBJECTIF:  Comparaison de la surprise calculée à la date de publication par rapport à 
#               la surprise publiée par Refinitiv
#              Analyse du coéfficient de corrélation de Pearson et Spearman 
#   PARAMETRISATION: adapter la fonction path 
#   INPUT:   ../etapePreparation/journal_surprise.xlsx
#            ../fichierDeRefinitiv/RevSurprise.xlsx
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
srf = pd.read_excel(path("etapePreparation/journal_surprise.xlsx"), sheet_name = sheet_name, header = header)
journal_surprise=srf[["cpy","Period End Date","Surprise"]]
srf = pd.read_excel(path("fichierDeRefinitiv/RevSurprise.xlsx"), sheet_name = sheet_name, header = header)
surpriseRevenue_frame=srf[['cpy', 'Period End Date','Date','Revenue - Actual Surprise']]
surpriseRevenue_frame.rename(columns = {'Revenue - Actual Surprise':'RefinitiveSurprise'}, inplace = True)



surpriseRevenue_frame['Date']= pd.to_datetime(surpriseRevenue_frame['Date'])
surpriseRevenue_frame=pd.merge(surpriseRevenue_frame,journal_surprise[["cpy","Period End Date","Surprise"]],how='left',on=["cpy","Period End Date"])
print('creation de SurpriseControle')

surpriseRevenue_frame=surpriseRevenue_frame[surpriseRevenue_frame['Surprise'].notna()]

sns.set()
sns.pairplot(surpriseRevenue_frame, vars=['RefinitiveSurprise',"Surprise"],kind='reg')
plt.show()
r=surpriseRevenue_frame['RefinitiveSurprise'].describe()
print(r)
r=surpriseRevenue_frame['Surprise'].describe()
print(r)

surpriseRevenue_frame=surpriseRevenue_frame.assign(capSurprise=winsorize(surpriseRevenue_frame["Surprise"], limits=[0.01, 0.01])) #on cape

sns.set()
sns.pairplot(surpriseRevenue_frame, vars=['RefinitiveSurprise',"capSurprise"],kind='reg')
plt.show()
r=surpriseRevenue_frame['capSurprise'].describe()
print(r)
surpriseRevenue_frame.to_excel("/Users/isabelledebry/Documents/TFENOEMIE/controlPreparation/SurpriseControl.xlsx")
print("Coef correlation Surprise Refinitive")
print (sc.stats.pearsonr(surpriseRevenue_frame['Surprise'], surpriseRevenue_frame['RefinitiveSurprise']))
print("Pearson Coef correlation capSurprise (0.005,0.005) Refinitive")
print (sc.stats.pearsonr(surpriseRevenue_frame['capSurprise'], surpriseRevenue_frame['RefinitiveSurprise']))
print("Spearman Coef correlation capSurprise (0.005,0.005) Refinitive")
print(sc.stats.spearmanr(surpriseRevenue_frame['capSurprise'], surpriseRevenue_frame['RefinitiveSurprise']))


