# TFE-surprise
# comparaison des résultats de prédiction de surprise de revenu
#
# description des répertoires:
#
#   controlPreparation : contient les fichiers intermédiaires 
#                     établis lors des controles  du traitement 
#                     data_preparation
#   etapepreparation : contient les fichiers intermédiaires du   
#                    traitement data_preparation
#   fichierDeRefinitiv : contient les fichiers extraits de 
#                     Refinitiv
#   fichiersApprentissage : contient les fichiers train et test 
#   fichierwithPredOrHit : contient les fichiers tests avec les 
#                     prédictions et les calculs de hit et 
#                     de anchored hit. 
#                     Les fichiers test contenant le sigle 21bis #                     sont issus de l'apprentissage avec le 
#                     fichier  train_19_20. 
#                     Les fichiers avec le sigle 21 sont issus de #                     l'apprentissage via train_20. 
#
#
#  description des traitements:
#
#1) Data preparation.py
#L'objectif est la réalisation d'un journal par quadrimestre #d'entreprise simulant de manière chronologique l'obtention la #valeur moyenne des estimés  des analystes financiers tout en #regroupant ces données avec les valeurs finales publiées pour ce #quadrimestre.
#
#Les données extraites de Refinitiv sont utilisées comme input #par le programme. 
#Les fichiers résultats sont le fichier journal output.xlsx dans #le répertoire étapePréparation et les fichiers train.xlsx et #test.xlsx dans le répertoire fichiersApprentissage.
#
#Les paramètres de ce programme à adapter sont le chemin de #répertoires et les variables de temps  pour couper le journal et #créer des fichiers d'apprentissage spécifiques.


#2) DatacontentAnalysis.py
#L'objectif est de donner les dimensions du contenu du journal et #des fichiers d'apprentissages (
#nombre de lignes, nombre d'entreprises,nombre lignes par  #entreprise,nombre de date du journal,	première date,	dernière #date,	premier (test) / dernier (train) quadrimestre,nombre #d'association entreprise - quadrimestre, nombre de jour par #association entreprise - quadrimestre). Le chemin des #répertoires utiles est à paramétrer dans le programme (fonction #path()) 

#3) SurpriseAnalysis.py
#Comparaison de la surprise calculée à la date de publication par #rapport à la surprise publiée par Refinitiv et Analyse du #coefficient de corrélation de Pearson et Spearman. 
#Les fichiers input sont etapePreparation/journal\_surprise.xlsx #et fichierDeRefinitiv/RevSurprise.xlsx. 


#4) cibleAnalysis.py
#L'objectif est de présenter à partir du fichier journal #(etapePreparation/output), les statistiques descriptives des #variables cibles potentielles: Revenue Actual, Surprise #(computedSurprise à la publication), ComputedSurprise #(journalière), growthSeasonalityActual mais aussi d'analyser #leur corrélation avec leurs variables estimateurs Revenue Mean, #PreviousSeasonalSurprise, growthSeasonalityEstimate. 

#5) featuresAnalysis.py
#L'objectif est de présenter à partir du fichier journal #(etapePreparation/output), les statistiques descriptives des #variables prédictives caractéristiques potentielles:
#DayGap, Revenue Mean, PreviousSeasonalSurprise, #growthSeasonalityEstimate, Year-EBIT-Mean, previous season #Revenue Actual, previous season EBIT. 

#6) featureimportance.py
#Régression selon GradientBoosting sur un jeu d'apprentissage. #Les trois cibles sont Revenue Actual, ComputedSurprise, #GrowthSeasonalActual à partir des 5 variables prédictives: #DayGap, Revenue - Mean, growthSeasonalityEstimate, #Year-EBIT-Mean, PreviousSeasonSurprise. Présentation de #l'importance des variables prédictives caractéristiques,  de la #mesure r2 , de la mesure MSE et des graphiques de distribution #de probabilité des variables cibles et prédites du jeu de test. #Sauvegarde de la prédiction dans le fichier #\est_predicted_By_GBoosting}.

#7) scaling.py
#Regression linéaire sur un jeu d'apprentissage (train, test) #dont les variables prédictives sont scalées selon soit le #principe MinMax soit le principe robustScaler. Les trois cibles #sont Revenue Actual, ComputedSurprise, GrowthSeasonalActual à #partir des 5 variables prédictives: DayGap, Revenue - Mean, #growthSeasonalityEstimate, Year-EBIT-Mean, #PreviousSeasonSurprise. 
#Présentation des coefficients de régression, de l'intercept, de #la mesure r2, de la mesure MSE et des graphiques de distribution #de probabilité des variables cibles et prédites du jeu de test. 
#Sauvegarde de la prédiction dans le fichier #"../fichierwithPredorHit/test_predicted_by_train_scaled.xlsx"
           

#8) targets prediction.py

#Regression linéaire multi-variée sur un jeu d'apprentissage pour #les trois cibles Revenue Actual, ComputedSurprise, #GrowthSeasonalActual à partir des 5 variables prédictives: #DayGap, Revenue - Mean,\\ growthSeasonalityEstimate, #Year-EBIT-Mean, PreviousSeasonSurprise. Présentation des #coefficients de régression, de l'intercept, de la mesure r2, de #la mesure MSE et des graphiques de distribution de probabilité #des variables cibles et prédites du jeu de test. Sauvegarde de #la prédiction dans le fichier test_predicted.


#9) hit_Analysis.py
#Construction des surprises prédites directement ou construites à #partir de la prédiction de revenue ou de seasonal revenue #growth. Construction des métriques hit et anchored_hit sur base #des signes des surprises (prédites ou calculées à partir d'une #prédiction versus la surprise calculée sur base de la #publication. 
#   INPUT:   ../fichierwithPredOrHit/test_predicted.xlsx
#   OUTPUTS: ../fichierwithPredOrHit/test_hit\_rate.xlsx


#10) AnchoredHitRateAnalysis.py
#Analyse des anchored Hit rates par des regroupements soit par #date (histogramme du nombre de cpy avec anchored hit rate #positif par date), soit par entreprise (histogramme du nombre de #date avec anchored hit rate positif par entreprise). 


