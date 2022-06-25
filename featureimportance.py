###################################################################################################################
#
#   OBJECTIF:  Regression selon GradientBoosting sur un jeu d'apprentissage . 
#               Présentation de l'importance des variables prédictives caractéristiques,  de la mesure r2 ,
#              de la mesure MSE et des graphiques de distribution de probabilité des variables cibles et prédites 
#              du jeu de test. Sauvegarde de la prédiction dans le fichier test_predicted_By_GBoosting.
#   PARAMETRISATION: adapter la fonction path 
#   INPUT:   ../fichiersApprentissage/train.xlsx
#            ../fichiersApprentissage/test.xlsx
#   OUTPUTS:   affichage des différentes métriques et graphiques 
#              ../fichierwithPredorHit/test_predicted_By_GBoosting.xlsx
###################################################################################################################

import pandas as pd
import numpy as np
from numpy  import *
import datetime as dt


from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model   import LinearRegression
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.inspection import permutation_importance
from sklearn.metrics import mean_squared_error
from sklearn import preprocessing
from sklearn import utils




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

train = pd.read_excel(path("fichiersApprentissage/train_19.xlsx"), sheet_name = sheet_name, header = header)
test = pd.read_excel(path("fichiersApprentissage/test_20.xlsx"), sheet_name = sheet_name, header = header)



#train=train[train['Business']=="Bank&Insurance"]
#test=test[test['Business']=="Bank&Insurance"]

print(len(train))
print(len(test))

#
# REGRESSION REVENUE ACTUAL by Revenue-Mean, growthEstimate, EBIT-Mean
# 
X_train=train[['DayGap','Revenue - Mean','growthSeasonalityEstimate','Year-EBIT-Mean', 'PreviousSeasonSurprise' ]]
y_train=ravel(train[['Revenue - Actual']])
X_test=test[['DayGap','Revenue - Mean','growthSeasonalityEstimate','Year-EBIT-Mean', 'PreviousSeasonSurprise' ]]
y_test=ravel(test[['Revenue - Actual']])
feature_names = ['DayGap','Revenue - Mean','growthSeasonalityEstimate','Year-EBIT-Mean', 'PreviousSeasonSurprise' ]

forest = GradientBoostingClassifier(n_estimators=20, learning_rate=0.1,max_depth=4, random_state=0,verbose=1).fit(X_train, y_train)
mse = mean_squared_error(y_test, forest.predict(X_test))
print("The mean squared error (MSE) on test set: {:.4f}".format(mse))
feature_importance = forest.feature_importances_
sorted_idx = np.argsort(feature_importance)
pos = np.arange(sorted_idx.shape[0]) + 0.5
fig = plt.figure(figsize=(12, 6))
plt.barh(pos, feature_importance[sorted_idx], align="center")
plt.yticks(pos, np.array(feature_names)[sorted_idx])
plt.title("Feature Importance (MDI)")

fig.suptitle('GradientBoosting regression for RA train_19 test_20')
fig.tight_layout()
plt.show()


y_test_predicted_RA=forest.predict(X_test)
print(forest.score(X_test, y_test))
regression_results(y_test, y_test_predicted_RA)


test.insert(0,'Revenue Actual predicted',y_test_predicted_RA)
test.to_excel(path("fichierwithPredOrHit/test_predicted_By_GBoosting.xlsx"))


# REGRESSION SURPRISE by  Revenue-Mean, growthEstimate, EBIT estimate
#y_train=train[['Surprise']]
y_train=ravel(train[['capComputedSurprise']])
y_test=ravel(test[['ComputedSurprise']])

#convert y values to categorical values 
lab = preprocessing.LabelEncoder()
y_train_transformed = lab.fit_transform(y_train)
y_test_transformed = lab.fit_transform(y_test)

forest = GradientBoostingClassifier(n_estimators=5, learning_rate=0.1,max_depth=4, random_state=0,verbose=1).fit(X_train, y_train_transformed)
mse = mean_squared_error(y_test_transformed, forest.predict(X_test))
print("The mean squared error (MSE) on test set: {:.4f}".format(mse))
feature_importance = forest.feature_importances_
sorted_idx = np.argsort(feature_importance)
pos = np.arange(sorted_idx.shape[0]) + 0.5
fig = plt.figure(figsize=(12, 6))
plt.barh(pos, feature_importance[sorted_idx], align="center")
plt.yticks(pos, np.array(feature_names)[sorted_idx])
plt.title("Feature Importance (MDI)")
fig.suptitle('GradientBoosting regression for Surprise train_19 test_20')
fig.tight_layout()
plt.show()

y_test_predicted_S=forest.predict(X_test)
print(forest.score(X_test, y_test_transformed))
regression_results(y_test_transformed, y_test_predicted_S)

# REGRESSION growthSeasonalityActual by Time, Revenue-Mean, growthEstimate, cpy 
y_train=ravel(train[['growthSeasonalityActual']])
y_test=ravel(test[['growthSeasonalityActual']])

#convert y values to categorical values
lab = preprocessing.LabelEncoder()
y_train_transformed = lab.fit_transform(y_train)
y_test_transformed = lab.fit_transform(y_test)

forest = GradientBoostingClassifier(n_estimators=5, learning_rate=0.1,max_depth=4, random_state=0,verbose=1).fit(X_train, y_train_transformed)
mse = mean_squared_error(y_test_transformed, forest.predict(X_test))
print("The mean squared error (MSE) on test set: {:.4f}".format(mse))
feature_importance = forest.feature_importances_
sorted_idx = np.argsort(feature_importance)
pos = np.arange(sorted_idx.shape[0]) + 0.5
fig = plt.figure(figsize=(12, 6))
plt.barh(pos, feature_importance[sorted_idx], align="center")
plt.yticks(pos, np.array(feature_names)[sorted_idx])
plt.title("Feature Importance (MDI)")

fig.suptitle('GradientBoosting regression for G train_19 test_2')
fig.tight_layout()
plt.show()

y_test_predicted_G=forest.predict(X_test)
print(forest.score(X_test, y_test_transformed))
regression_results(y_test_transformed, y_test_predicted_G)

test.insert(0,'Surprise predicted',y_test_predicted_S)
test.insert(0,'Revenue Actual predicted',y_test_predicted_RA)
test.insert(0,'seasonal growth predicted',y_test_predicted_G)

test.to_excel(path("fichierwithPredOrHit/test_predicted_By_GBoosting.xlsx"))