###################################################################################################################
#
#   OBJECTIF:  Construction des surprises (prédites directement, construites à partir de la prédiction de revenue 
#               ou de seasonal revenue growth)
#              Construction des métriques hit et anchored_hit sur base des signes des surprises (prédites ou 
#               calculées à partir d'une prédiction versus la surprise calculée sur base de la publication
# 
#   PARAMETRISATION: adapter la fonction path 
#   INPUT:   ../fichierwithPredOrHit/test_predicted.xlsx
#            
#   OUTPUTS:   affichage des différentes métriques et graphiques 
#              ../fichierwithPredOrHit/test_hit_rate.xlsx
###################################################################################################################

import pandas as pd
import numpy as np
from numpy  import *
import datetime as dt

from sklearn.linear_model   import LinearRegression
import sklearn.metrics as metrics
import matplotlib
from matplotlib import pyplot as plt
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
import tensorflow as tf
# use keras API
from tensorflow import keras
from tensorflow.keras import layers
import seaborn as sns


def path(file):
    return "/Users/isabelledebry/Documents/TFENOEMIE/"+file

sheet_name = 0 
header = 0 # The header is the first row

test = pd.read_excel(path("fichierwithPredOrHit/test_predicted_by_train_scaled.xlsx"), sheet_name = sheet_name, header = header)

test=test.assign(Surprise_DEDUCED_BY_RA_Pred=(100*(test['Revenue Actual predicted']-test['Revenue - Mean'])/test['Revenue Actual predicted']))
test=test.assign(RA_DEDUCED_BY_G_Pred=(test['previous season Revenue Actual']+(test['seasonal growth predicted']*test['previous season Revenue Actual'])))
test=test.assign(Surprise_DEDUCED_BY_G_Pred=(100*( test['RA_DEDUCED_BY_G_Pred']-test['Revenue - Mean'] )/test['RA_DEDUCED_BY_G_Pred']))



r=test['Surprise_DEDUCED_BY_RA_Pred'].describe()
print(r)
r=test['Surprise_DEDUCED_BY_G_Pred'].describe()
print(r)
r=test['Surprise predicted'].describe()
print(r)
r=test['ComputedSurprise'].describe()
print(r)

r=test['PreviousSeasonSurprise'].describe()
print(r)
r=test['Surprise'].describe()
print(r)

fig, ax = plt.subplots()
features = ['ComputedSurprise', 'PreviousSeasonSurprise']
sns.histplot(test[features],stat='density')
ax.set_xlim(-10,10)
plt.show()
sns.set(rc={'figure.figsize': (10, 5)})
sns.boxplot(data=test[features].select_dtypes(include='number'),)
ax.set_xlim(-1,1)
plt.show()
features = ['ComputedSurprise', 'Surprise predicted']
fig, ax = plt.subplots()
sns.histplot(test[features],stat='density')
ax.set_xlim(-10,10)
plt.show()
sns.set(rc={'figure.figsize': (10, 5)})
sns.boxplot(data=test[features].select_dtypes(include='number'))
plt.show()

fig, ax = plt.subplots()
features = ['ComputedSurprise','Surprise_DEDUCED_BY_G_Pred']
sns.histplot(test[features],stat='density')
ax.set_xlim(-10,10)
plt.show()
sns.set(rc={'figure.figsize': (10, 5)})
sns.boxplot(data=test[features].select_dtypes(include='number'))
plt.show()

fig, ax = plt.subplots()
features = ['ComputedSurprise','Surprise_DEDUCED_BY_RA_Pred']
sns.histplot(test[features],stat='density')
ax.set_xlim(-10,10)
plt.show()
sns.set(rc={'figure.figsize': (10, 5)})
sns.boxplot(data=test[features].select_dtypes(include='number'))
plt.show()


fig, ax = plt.subplots()
features = ['ComputedSurprise','Surprise']
sns.histplot(test[features],stat='density')
ax.set_xlim(-10,10)
plt.show()
sns.set(rc={'figure.figsize': (10, 5)})
sns.boxplot(data=test[features].select_dtypes(include='number'))
plt.show()


# calcul anchored Season Surprise (substract by median)
# 
anchored_Surprise = test['ComputedSurprise']-test['ComputedSurprise'].median()
test.insert(0,'anchored_Surprise',anchored_Surprise)
#
anchored_PreviousSeasonSurprise= test['PreviousSeasonSurprise']-test['PreviousSeasonSurprise'].median()
test.insert(0,'anchored_PreviousSeasonSurprise',anchored_PreviousSeasonSurprise)
#
anchored_Surprise_predicted = test['Surprise predicted']-test['Surprise predicted'].median()
test.insert(0,'anchored_Surprise_predicted',anchored_Surprise_predicted)
#
#
anchored_Surprise_by_RA = test['Surprise_DEDUCED_BY_RA_Pred']-test['Surprise_DEDUCED_BY_RA_Pred'].median()
test.insert(0,'anchored_Surprise_by_RA',anchored_Surprise_by_RA)
#
anchored_Surprise_by_G= test['Surprise_DEDUCED_BY_G_Pred']-test['Surprise_DEDUCED_BY_G_Pred'].median()
test.insert(0,'anchored_Surprise_by_G',anchored_Surprise_by_G)
#



test=test.assign(hit_by_Previous_S_S=0)
test=test.assign(hit_by_S_pred=0)
test=test.assign(hit_by_RA_pred =0)
test=test.assign(hit_by_G_pred =0)
test=test.assign(anchored_hit_rate_by_previous =0)
test=test.assign(anchored_hit_rate =0)
test=test.assign(anchored_hit_by_RA_pred =0)
test=test.assign(anchored_hit_by_G_pred =0)





for i in test.index: 

    if (test['PreviousSeasonSurprise'][i] ==0 and test['ComputedSurprise'][i]==0):
        test['hit_by_Previous_S_S'][i] =1
    else:
        if (test['PreviousSeasonSurprise'][i] ==0 or test['ComputedSurprise'][i]==0):
            test['hit_by_Previous_S_S'][i] =0 
        else:
           if (test['PreviousSeasonSurprise'][i]*test['ComputedSurprise'][i]>0):
               test['hit_by_Previous_S_S'][i] = 1 
           else:
                test['hit_by_Previous_S_S'][i] = 0



    if (test['Surprise predicted'][i] ==0 and test['ComputedSurprise'][i]==0):
        test['hit_by_S_pred'][i] =1
    else:
        if (test['Surprise predicted'][i] ==0 or test['ComputedSurprise'][i]==0):
            test['hit_by_S_pred'][i] =0 
        else:
            if (test['Surprise predicted'][i]*test['ComputedSurprise'][i]>0):
                test['hit_by_S_pred'][i] = 1
            else:
                test['hit_by_S_pred'][i] = 0
    

    if (test['Surprise_DEDUCED_BY_RA_Pred'][i] ==0 and test['ComputedSurprise'][i]==0):
        test['hit_by_RA_pred'][i]  =1
    else:
        if (test['Surprise_DEDUCED_BY_RA_Pred'][i] ==0 or test['ComputedSurprise'][i]==0):
            test['hit_by_RA_pred'][i]  =0 
        else:
            if (test['Surprise_DEDUCED_BY_RA_Pred'][i]*test['ComputedSurprise'][i]>0):
                test['hit_by_RA_pred'][i]= 1
            else:
                test['hit_by_RA_pred'][i]= 0


    if (test['Surprise_DEDUCED_BY_G_Pred'][i] ==0 and test['ComputedSurprise'][i]==0):
        test['hit_by_G_pred'][i]  =1
    else:
        if (test['Surprise_DEDUCED_BY_G_Pred'][i] ==0 or test['ComputedSurprise'][i]==0):
            test['hit_by_G_pred'][i]  =0 
        else:
            if (test['Surprise_DEDUCED_BY_G_Pred'][i]*test['ComputedSurprise'][i]>0):
                test['hit_by_G_pred'][i] = 1
            else:
                test['hit_by_G_pred'][i] = 0
  
    if (test['anchored_Surprise_predicted'][i] ==0 and test['anchored_Surprise'][i]==0):
        test['anchored_hit_rate'][i]   =1
    else:
        if (test['anchored_Surprise_predicted'][i] ==0 or test['anchored_Surprise'][i]==0):
            test['anchored_hit_rate'][i]  =0  
        else:
            if (test['anchored_Surprise_predicted'][i]*test['anchored_Surprise'][i]>0):
                test['anchored_hit_rate'][i] = 1
            else:
                test['anchored_hit_rate'][i] = 0

    #
    #
    if (test['anchored_PreviousSeasonSurprise'][i] ==0 and test['anchored_Surprise'][i]==0):
        test['anchored_hit_rate_by_previous'][i]   =1
    else:
        if (test['anchored_PreviousSeasonSurprise'][i] ==0 or test['anchored_Surprise'][i]==0):
           test['anchored_hit_rate_by_previous'][i]  =0  
        else:
            if (test['anchored_PreviousSeasonSurprise'][i]*test['anchored_Surprise'][i]>0):
                test['anchored_hit_rate_by_previous'][i] = 1
            else:
                 test['anchored_hit_rate_by_previous'][i] = 0

    if (test['anchored_Surprise_by_RA'][i] ==0 and test['anchored_Surprise'][i]==0):
        test['anchored_hit_by_RA_pred'][i]   =1
    else:
        if (test['anchored_Surprise_by_RA'][i] ==0 or test['anchored_Surprise'][i]==0):
            test['anchored_hit_by_RA_pred'][i]   =0 
        else:
            if (test['anchored_Surprise_by_RA'][i]*test['anchored_Surprise'][i]>0):
                test['anchored_hit_by_RA_pred'][i] = 1
            else:
                test['anchored_hit_by_RA_pred'][i] = 0

    if (test['anchored_Surprise_by_G'][i] ==0 and test['anchored_Surprise'][i]==0):
        test['anchored_hit_by_G_pred'][i]   =1
    else:
        if (test['anchored_Surprise_by_G'][i] ==0 or test['anchored_Surprise'][i]==0):
            test['anchored_hit_by_G_pred'][i]   =0 
        else:
            if (test['anchored_Surprise_by_G'][i]*test['anchored_Surprise'][i]>0):
                test['anchored_hit_by_G_pred'][i] = 1
            else:
                test['anchored_hit_by_G_pred'][i] = 0




dataframe2 =pd.DataFrame(test['hit_by_Previous_S_S']).describe()
fig, ax = plt.subplots()
extract=test[['hit_by_Previous_S_S','Date']].groupby('Date').sum()
sns.histplot(extract[['hit_by_Previous_S_S']],stat='probability',ax=ax).set(title='sum of hit_by_Previous_Seasonal_Surprise by Date')
plt.show()
print("hit_by_Previous_S_S")
print(dataframe2)
#print(100*dataframe2.loc[["freq"]]/dataframe2.count)
dataframe2 =pd.DataFrame(test['hit_by_S_pred']).describe()
fig, ax = plt.subplots()
extract=test[['hit_by_S_pred','Date']].groupby('Date').sum()
sns.histplot(extract[['hit_by_S_pred']],stat='probability',ax=ax).set(title='sum hit_by_S_pred by Date')
plt.show()
print("hit_by_Surprise_pred")
print(dataframe2)
#print(100*dataframe2.loc[["freq"]]/dataframe2.count)
dataframe2 =pd.DataFrame(test['hit_by_RA_pred']).describe()
fig, ax = plt.subplots()
extract=test[['hit_by_RA_pred','Date']].groupby('Date').sum()
sns.histplot(extract[['hit_by_RA_pred']],stat='probability',ax=ax).set(title='sum hit_by_RA_prediction by Date')
plt.show()
print("hit_by_RA_pred")
print(dataframe2)
#print(100*dataframe2.loc[["freq"]]/dataframe2.count)
dataframe2 =pd.DataFrame(test['hit_by_G_pred']).describe()
fig, ax = plt.subplots()
extract=test[['hit_by_G_pred','Date']].groupby('Date').sum()
sns.histplot(extract[['hit_by_G_pred']],stat='probability',ax=ax).set(title='sum hit_by_G_prediction by Date')
plt.show()
print("hit_by_G_pred")
print(dataframe2)
#print(100*dataframe2.freq/dataframe2.count)



dataframe2 =pd.DataFrame(test['anchored_hit_rate_by_previous']).describe()
fig, ax = plt.subplots()
extract=test[['anchored_hit_rate_by_previous','Date']].groupby('Date').sum()
sns.histplot(extract[['anchored_hit_rate_by_previous']],stat='probability',ax=ax).set(title='sum anchored_hit_rate_by_previous by Date')
plt.show()
print("anchored_hit_rate_by_previous")
print(dataframe2)
#print(100*dataframe2.freq/dataframe2.count)
dataframe2 =pd.DataFrame(test['anchored_hit_rate']).describe()
fig, ax = plt.subplots()
extract=test[['anchored_hit_rate','Date']].groupby('Date').sum()
sns.histplot(extract['anchored_hit_rate'],stat='probability',ax=ax).set(title='sum anchored_hit_rate_by_surprise by Date')
plt.show()
print("anchored_hit_rate")
print(dataframe2)
#print(100*dataframe2.freq/dataframe2.count)
dataframe2 =pd.DataFrame(test['anchored_hit_by_RA_pred']).describe()
fig, ax = plt.subplots()
extract=test[['anchored_hit_by_RA_pred','Date']].groupby('Date').sum()
sns.histplot(extract['anchored_hit_by_RA_pred'],stat='probability',ax=ax).set(title='sum anchored_hit_by_RA_pred by Date')
plt.show()
print("anchored_hit_by_RA_pred")
print(dataframe2)
#print(100*dataframe2.freq/dataframe2.count)
dataframe2 =pd.DataFrame(test['anchored_hit_by_G_pred']).describe()
fig, ax = plt.subplots()
extract=test[['anchored_hit_by_G_pred','Date']].groupby('Date').sum()
sns.histplot(extract['anchored_hit_by_G_pred'],stat='probability',ax=ax).set(title='sum anchored_hit_by_G_pred by Date')
plt.show()
print("anchored_hit_by_G_pred")
print(dataframe2)
#print(100*dataframe2.freq/dataframe2.count)

"""
fig, ax = plt.subplots()
sns.histplot(test, x='ComputedSurprise', hue="Size",stat='density')
ax.set_xlim(-10,10)
plt.show()

fig, ax = plt.subplots()
sns.histplot(test, x='ComputedSurprise', hue="Business",stat='density')
ax.set_xlim(-10,10)
plt.show()
"""

test.to_excel(path("fichierwithPredOrHit/test_by_train_scaled_hit_rate.xlsx"))


