###################################################################################################################
#
#   OBJECTIF:  Regression linéaire sur un jeu d'apprentissage qui est scalé selon soit le principe MinMax soit le 
#              principe robustScaler. Présentation des coefficients de régression, de l'intercept, de la mesure r2,
#              de la mesure MSE et des graphiques de distribution de probabilité des variables cibles et prédites 
#              du jeu de test. Sauvegarde de la prédiction dans le fichier test_predicted_by_train_scaled.
#   PARAMETRISATION: adapter la fonction path 
#   INPUT:   ../fichiersApprentissage/train.xlsx
#            ../fichiersApprentissage/test.xlsx
#   OUTPUTS:   affichage des différentes métriques et graphiques 
#              ../fichierwithPredorHit/test_predicted_by_train_scaled.xlsx
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
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import RobustScaler
from sklearn.linear_model import Ridge
import tensorflow as tf
# use keras API
from tensorflow import keras
from tensorflow.keras import layers
import seaborn as sns
from scipy.stats.mstats import winsorize

def regression_results(y_true, y_pred):
    # Regression metrics
    explained_variance=metrics.explained_variance_score(y_true, y_pred)
    mean_absolute_error=metrics.mean_absolute_error(y_true, y_pred) 
    mse=metrics.mean_squared_error(y_true, y_pred) 
    #mean_squared_log_error=metrics.mean_squared_log_error(y_true, y_pred)
    median_absolute_error=metrics.median_absolute_error(y_true, y_pred)
    r2=metrics.r2_score(y_true, y_pred)
    print('explained_variance: ', round(explained_variance,4))    
    #print('mean_squared_log_error: ', round(mean_squared_log_error,4))
    print('r2: ', round(r2,4))
    print('MAE: ', round(mean_absolute_error,4))
    print('MSE: ', round(mse,4))
    print('RMSE: ', round(np.sqrt(mse),4))


def path(file):
    return "/Users/isabelledebry/Documents/TFENOEMIE/"+file


sheet_name = 0 
header = 0 # The header is the first row

train = pd.read_excel(path("fichiersApprentissage/train.xlsx"), sheet_name = sheet_name, header = header)
test = pd.read_excel(path("fichiersApprentissage/te#st.xlsx"), sheet_name = sheet_name, header = header)

#print ("SCALING minMaxScaler")
#scaler = MinMaxScaler()
print ("SCALING RobustScaler")
scaler = RobustScaler(with_centering=True, with_scaling=True, quantile_range=(25, 75))
#
# REGRESSION REVENUE ACTUAL by Revenue-Mean, growthEstimate, EBIT-Mean
# 
X_train=train[['DayGap','Revenue - Mean','growthSeasonalityEstimate','Year-EBIT-Mean', 'PreviousSeasonSurprise' ]]

y_train=train[['Revenue - Actual']]
X_test=test[['DayGap','Revenue - Mean','growthSeasonalityEstimate','Year-EBIT-Mean', 'PreviousSeasonSurprise' ]]

y_test=test[['Revenue - Actual']]

print('start regression')
clf = LinearRegression(fit_intercept=True)
X_train_scaled= scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
clf.fit(X_train_scaled, y_train)
print("LinearRegression: Revenue - Actual ")
print(clf.coef_)
print(clf.intercept_)
y_test_predicted_RA=clf.predict(X_test_scaled)
print(clf.score(X_test_scaled, y_test))
regression_results(y_test, y_test_predicted_RA)

fig, ax = plt.subplots()
plt.hist(y_test_predicted_RA, alpha=0.3, color='g',label='data test year:21 : Predicted Revenue' )
plt.hist(y_test, alpha=0.3,  color='r',label='data test year:21 : Actual Revenue')
plt.title('Comparaison Revenue Actual-Predicted')
ax.set_xlim(-1,200000000000)
plt.legend()
plt.show()
plt.figure()




# REGRESSION SURPRISE by  Revenue-Mean, growthEstimate, EBIT estimate
#y_train=train[['Surprise']]
y_train=train[['capComputedSurprise']]
y_test=test[['ComputedSurprise']]
clf = LinearRegression(fit_intercept=True)
scaler = MinMaxScaler()
X_train_scaled= scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
clf.fit(X_train_scaled, y_train)
print("LinearRegression: ComputedSurprise ")
print(clf.coef_)
print(clf.intercept_)
y_test_predicted_S=clf.predict(X_test_scaled)
print(clf.score(X_test_scaled, y_test))
regression_results(y_test, y_test_predicted_S)

plt.hist(y_test_predicted_S, alpha=0.3, color='g',label='data:test year:21 : Predicted Surprise' )
plt.hist(y_test,  color='r',alpha=0.3,label='data:test year:21 : Surprise ')
plt.title('Comparaison Surprise Computed-Predicted')
plt.legend()
plt.show()
plt.figure()

# REGRESSION growthSeasonalityActual by Time, Revenue-Mean, growthEstimate, cpy 
y_train=train[['growthSeasonalityActual']]
y_test=test[['growthSeasonalityActual']]
clf = LinearRegression(fit_intercept=True)
scaler = MinMaxScaler()
X_train_scaled= scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
clf.fit(X_train_scaled, y_train)
print("LinearRegression: growthSeasonalityActual ")
print(clf.coef_)
print(clf.intercept_)
y_test_predicted_G=clf.predict(X_test_scaled)
print(clf.score(X_test_scaled, y_test))
regression_results(y_test, y_test_predicted_G)


plt.hist(y_test_predicted_G, alpha=0.3, color='g',label='data:test(2021) : predict growthSeasonalityActual' )
plt.hist(y_test,  color='r',alpha=0.3,label='data:test(2021) : growthSeasonalityActual ')
plt.title('Comparaison Y2Y_growth: Actual-Predicted')
plt.legend()
plt.show()
plt.figure()

test.insert(0,'Surprise predicted',y_test_predicted_S)
test.insert(0,'Revenue Actual predicted',y_test_predicted_RA)
test.insert(0,'seasonal growth predicted',y_test_predicted_G)


test.to_excel(path("fichierwithPredorHit/test_predicted_by_train_scaled.xlsx"))

features = ['ComputedSurprise',  'Surprise predicted']
sns.set(rc={'figure.figsize': (16, 5)})
sns.boxplot(data=test[features].select_dtypes(include='number')).set(title='Boxplots Surprise')
plt.show()
fig, ax = plt.subplots()
sns.histplot(test[features],stat='density',ax=ax).set(title='Surprise Density')
ax.set_xlim(-5,5)
plt.show()

features = ['growthSeasonalityActual', 'seasonal growth predicted' ]
sns.set(rc={'figure.figsize': (16, 5)})
sns.boxplot(data=test[features].select_dtypes(include='number')).set(title='Boxplots S_growth')
plt.show()
fig, ax = plt.subplots()
sns.histplot(test[features],stat='density').set(title='S_Growth Density')
ax.set_xlim(-1,1)
plt.show()




