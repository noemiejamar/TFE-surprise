###################################################################################################################
#
#   OBJECTIF: Réalisation d'un journal par quadrimestre d'entreprise simulant de manière chronologique 
#               l'obtention la valeur moyenne des estimés  des analystes financiers tout en regroupant ces données 
#               avec les valeurs finales publiées pour ce quadrimestre. 
#   PARAMETRISATION: adapter la fonction path 
#                  : adapter les dates de coupures des fichiers de train et test (datecoupurestart,datecoupureend)
#                  : adapter les dateDebutJournalEbit='01-01-2017' et dateFinJournalEBIT='01-03-2022' 
#   INPUTS:   .../fichierDeRefinitiv/Company.xlxs  : liste des Entreprises
#             .../fichierDeRefinitiv/RevActual.xlxs : liste des chiffres d'affaires  (Actual revenue) publiés par quadrimestre et par entreprise
#             .../fichierDeRefinitiv/RevEstimate.xlsx : liste des prévision de chiffre d'affaires (Mean) par entreprise et quadrimestre
#             .../fichierDeRefinitiv/RevSurprise.xlsx : liste des Surprise de revenus lors de la publication par entreprise et quadrimestre
#             .../fichierDeRefinitiv/EBIT-Actual.xlxs : liste des resultats d'exploitation (EBIT) publiés par entreprise et quadrimestre
#             .../fichierDeRefinitiv/EBITMean.xlxs : liste des porévision de résultat d'exploitation par entreprise et quadrimestre
#             .../fichierDeRefinitiv/classif.xlsx : Classification des ebtreprises en nombre d'employés et de secteur d'activités
#             .../fichierDeRefinitiv/classifESG.xlsx : liste de Resultat annuel ESG par entrepris
#   CONTROLES:.../etapePreparation/output1.xlsx
#             .../etapePreparation/output2.xlsx
#             .../controlPreparation/extract.xlsx
#             .../controlPreparation/extract1.xlsx
#             .../controlPreparation/extract2.xlsx
#             .../controlPreparation/extract3.xlsx
#             .../controlPreparation/verif2.xlsx
#              .../etapePreparation/CleanedRevActual.xlsx
#              .../controlPreparation/verif.xlsx
#              .../etapePreparation/CleanedRevEstimate.xlsx
#              .../controlPreparation/verif1.xlsx
#              .../etapePreparation/actualoutput.xlsx
#              .../etapePreparation/classifESG0.xlsx
#              .../etapePreparation/journal_surprise.xlsx
#              .../etapePreparation/journal_previous_surprise.xlsx
#              .../etapePreparation/EBITMean0.xlsx
#
#   OUTPUTS:   .../etapePreparation/output.xlsx : journal final
#              .../fichiersApprentissage/train.xlsx : extrait du journal selon les découpages temporels
#              .../fichiersApprentissage/test.xlsx : extrait du journal selon les découpages temporels
###################################################################################################################
import pandas as pd
import numpy as np
from numpy  import *
import matplotlib
from matplotlib import pyplot as plt
from scipy.stats.mstats import winsorize
###################################################################################################################
#
# Import des fichiers provenant de Refinitive
# Generation Excell -RevActual.xlsx  
#                      ['cpy', 'Period End Date','Date','Revenue Actual']
#                   -RevEstimate.xlsx
#                      ['cpy', 'Period End Date','Date','Revenue - Mean']
#                   -RevSurprise.xlsx
#                     ["cpy",	"RRevenue - Actual Surprise",	"Date",	"Period End Date"}
#
#  Step1 : Nettoyage du fichier Revenu Actual (RevActual.xlsx)
#           - pas de na/NULL sur 'Revenue -Actual') 
#          - Rename "Date" de RevActual en "FilingData" 
#          Calcul d'une colonne  PreviousSeasonQuarter dans RevActual
#          Calcul d'une colonne PreviousQuarter dans RevActual
#          Calcul d'une colonne DayGap dans RevEstimate (distance en jours avant la fin de period end date)
#          
###################################################################################################################
sheet_name = 0 
header = 0 # The header is the first row

def path(file):
    return "/Users/isabelledebry/Documents/TFENOEMIE/"+file
dateDebutJournalEbit='01-01-2017'
dateFinJournalEBIT='01-03-2022'

arf = pd.read_excel(path("fichierDeRefinitiv/RevActual.xlsx"), sheet_name = sheet_name, header = header)
actualRevenue_frame=arf[['cpy', 'Period End Date','Date','Revenue - Actual']]
actualRevenue_frame['Date']= pd.to_datetime(actualRevenue_frame['Date'])
actualRevenue_frame['Period End Date']= pd.to_datetime(actualRevenue_frame['Period End Date'])
actualRevenue_frame.rename(columns = { 'Date': 'FilingDate'}, inplace = True)
result=len(actualRevenue_frame)
actualRevenue_frame= actualRevenue_frame[actualRevenue_frame['Revenue - Actual'].notna()] 
actualRevenue_frame= actualRevenue_frame[actualRevenue_frame['Revenue - Actual']>0] 
print("nettoyage revenu ACTUAL %d",result-len(actualRevenue_frame))
###################################################################################################################
#
#   Step2:  Nettoyage du fichier EBIT Actual (EBIT-Actual.xlsx)
#               - pas de na/NULL sur 'EBIT-Actual','Date'
#           rename column 'EBIT Filing Date' au lieu de Date
###################################################################################################################
ebit= pd.read_excel(path("fichierDeRefinitiv/EBIT-Actual.xlsx"), sheet_name = sheet_name, header = header)
ebit=ebit[['cpy',	'Date',	'EBIT-Actual', 'Period End Date']]
result=len(ebit)
ebit=ebit[ebit['Date'].notna()]
print("nettoyage EBIT ACTUAL %d",result-len(ebit))
ebit['Date']= pd.to_datetime(ebit['Date'])
ebit['Period End Date']= pd.to_datetime(ebit['Period End Date'])
ebit.rename(columns = { 'Date': 'EBIT Filing Date'}, inplace = True)
###################################################################################################################
#
#   Step3: merge EBIT & REVENUE ACTUAL in CleanedRevActual.xlsx
#
###################################################################################################################

actualRevenue_frame=pd.merge(actualRevenue_frame,ebit,how='left',on=["cpy",'Period End Date'])
result=len(actualRevenue_frame)
actualRevenue_frame=actualRevenue_frame[actualRevenue_frame['EBIT-Actual'].notna()]
print("nettoyage revenu ACTUAL with no EBIT %d",result-len(actualRevenue_frame))
actualRevenue_frame.to_excel(path("etapePreparation/CleanedRevActual.xlsx"))
print('creation de Cleaned Rev Actual')
###################################################################################################################
#
#   Step4: deduce previous Period-End_Date and previous Y2Y Period-End-Date from current Period-End-Date
#
###################################################################################################################
actualRevenue_frame.assign(PreviousQuarter=actualRevenue_frame['Period End Date'])
actualRevenue_frame.assign(PreviousSeasonQuarter=actualRevenue_frame['Period End Date'])
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/12/15', 'PreviousQuarter']	='30/09/15'	
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/12/15','PreviousSeasonQuarter']= '31/12/14'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/01/16','PreviousQuarter']	=	'31/10/15'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/01/16','PreviousSeasonQuarter']='31/01/15'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '29/02/16','PreviousQuarter']	=	'30/11/15'	
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '29/02/16','PreviousSeasonQuarter']	=	'28/02/15'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/03/16','PreviousQuarter']	=	'31/12/15'	
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/03/16','PreviousSeasonQuarter']	=	'31/03/15'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/06/16','PreviousQuarter']	=	'31/03/16'	
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/06/16','PreviousSeasonQuarter']	=	'30/06/15'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/09/16','PreviousQuarter']	=	'30/06/16'	
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/09/16','PreviousSeasonQuarter']	=	'30/09/15'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/12/16','PreviousQuarter']	=	'30/09/16'	
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/12/16','PreviousSeasonQuarter']	=	'31/12/15'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/01/17','PreviousQuarter']	=	'31/10/16'	
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/01/17','PreviousSeasonQuarter']	=	'31/01/16'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '28/02/17','PreviousQuarter']	=	'30/11/16'	
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '28/02/17','PreviousSeasonQuarter']	=	'29/02/16'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/03/17','PreviousQuarter']	=	'31/12/16'	
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/03/17','PreviousSeasonQuarter']	=	'31/03/16'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/04/17','PreviousQuarter']	=	'31/01/17'	
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/04/17','PreviousSeasonQuarter']	=	'30/04/16'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/05/17','PreviousQuarter']	=	'28/02/17'	
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/05/17','PreviousSeasonQuarter']	=	'31/05/16'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/06/17','PreviousQuarter']	=	'31/03/17'	
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/06/17','PreviousSeasonQuarter']	=	'30/06/16'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/07/17','PreviousQuarter']	=	'30/04/17'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/07/17','PreviousSeasonQuarter']	=	'31/07/16'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/08/17','PreviousQuarter']	=	'31/05/17'	
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/08/17','PreviousSeasonQuarter']	=	'31/08/16'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/09/17','PreviousQuarter']	=	'30/06/17' 
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/09/17','PreviousSeasonQuarter']	=		'30/09/16'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/10/17','PreviousQuarter']	=	'31/07/17'	
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/10/17','PreviousSeasonQuarter']	=	'31/10/16'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/11/17','PreviousQuarter']	=	'31/08/17' 
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/11/17','PreviousSeasonQuarter']	=		'30/11/16'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/12/17','PreviousQuarter']	=	'30/09/17'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/12/17','PreviousSeasonQuarter']	=		'31/12/16'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/01/18','PreviousQuarter']	=	'31/10/17' 
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/01/18','PreviousSeasonQuarter']	=		'31/01/17'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '28/02/18','PreviousQuarter']	=	'30/11/17' 
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '28/02/18','PreviousSeasonQuarter']	=		'28/02/17'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/03/18','PreviousQuarter']	=	'31/12/17' 
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/03/18','PreviousSeasonQuarter']	=		'31/03/17'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/04/18','PreviousQuarter']	=	'31/01/18'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/04/18','PreviousSeasonQuarter']	=		'30/04/17'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/05/18','PreviousQuarter']	=	'28/02/18'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/05/18','PreviousSeasonQuarter']	=		'31/05/17'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/06/18','PreviousQuarter']	=	'31/03/18'	
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/06/18','PreviousSeasonQuarter']	=	'30/06/17'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/07/18','PreviousQuarter']	=	'30/04/18' 
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/07/18','PreviousSeasonQuarter']	=		'31/07/17'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/08/18','PreviousQuarter']	=	'31/05/18'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/08/18','PreviousSeasonQuarter']	=		'31/08/17'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/09/18','PreviousQuarter']	=	'30/06/18'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/09/18','PreviousSeasonQuarter']	=		'30/09/17'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/10/18','PreviousQuarter']	=	'31/07/18'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/10/18','PreviousSeasonQuarter']	=		'31/10/17'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/11/18','PreviousQuarter']	=	'31/08/18'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/11/18','PreviousSeasonQuarter']	=		'30/11/17'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/12/18','PreviousQuarter']	=	'30/09/18'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/12/18','PreviousSeasonQuarter']	=		'31/12/17'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/01/19','PreviousQuarter']	=	'31/10/18' 
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/01/19','PreviousSeasonQuarter']	=			'31/01/18'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '28/02/19','PreviousQuarter']	=	'30/11/18' 
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '28/02/19','PreviousSeasonQuarter']	=		'28/02/18'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/03/19','PreviousQuarter']	=	'31/12/18'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/03/19','PreviousSeasonQuarter']	=		'31/03/18'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/04/19','PreviousQuarter']	=	'31/01/19'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/04/19','PreviousSeasonQuarter']	=		'30/04/18'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/05/19','PreviousQuarter']	=	'28/02/19'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/05/19','PreviousSeasonQuarter']	=		'31/05/18'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/06/19','PreviousQuarter']	=	'31/03/19'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/06/19','PreviousSeasonQuarter']	=		'30/06/18'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/07/19','PreviousQuarter']	=	'30/04/19'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/07/19','PreviousSeasonQuarter']	=		'31/07/18'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/08/19','PreviousQuarter']	=	'31/05/19'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/08/19','PreviousSeasonQuarter']	=		'31/08/18'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/09/19','PreviousQuarter']	=	'30/06/19'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/09/19','PreviousSeasonQuarter']	=		'30/09/18'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/10/19','PreviousQuarter']	=	'31/07/19'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/10/19','PreviousSeasonQuarter']	=		'31/10/18'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/11/19','PreviousQuarter']	=	'31/08/19'	
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/11/19','PreviousSeasonQuarter']	=	    '30/11/18'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/12/19','PreviousQuarter']	=	'30/09/19'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/12/19','PreviousSeasonQuarter']	=		'31/12/18'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/01/20','PreviousQuarter']	=	'31/10/19'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/01/20','PreviousSeasonQuarter']	=		'31/01/19'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '29/02/20','PreviousQuarter']	=	'30/11/19'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '29/02/20','PreviousSeasonQuarter']	=		'28/02/19'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/03/20','PreviousQuarter']	=	'31/12/19'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/03/20','PreviousSeasonQuarter']	=		'31/03/19'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/04/20','PreviousQuarter']	=	'31/01/20'	
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/04/20','PreviousSeasonQuarter']	=	    '30/04/19'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/05/20','PreviousQuarter']	=	'29/02/20'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/05/20','PreviousSeasonQuarter']	=		'31/05/19'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/06/20','PreviousQuarter']	=	'31/03/20'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/06/20','PreviousSeasonQuarter']	=		'30/06/19'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/07/20','PreviousQuarter']	=	'30/04/20'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/07/20','PreviousSeasonQuarter']	=		'31/07/19'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/08/20','PreviousQuarter']	=	'31/05/20'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/08/20','PreviousSeasonQuarter']	=		'31/08/19'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/09/20','PreviousQuarter']	=		'30/06/20'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/09/20','PreviousSeasonQuarter']	=		'30/09/19'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/10/20','PreviousQuarter']	=		'31/07/20'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/10/20','PreviousSeasonQuarter']	=		'31/10/19'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/11/20','PreviousQuarter']	=		'31/08/20'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/11/20','PreviousSeasonQuarter']	=		'30/11/19'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/12/20','PreviousQuarter']	=		'30/09/20'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/12/20','PreviousSeasonQuarter']	=		'31/12/19'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/01/21','PreviousQuarter']	=		'31/10/20'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/01/21','PreviousSeasonQuarter']	=		'31/01/20'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '28/02/21','PreviousQuarter']	=		'30/11/20'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '28/02/21','PreviousSeasonQuarter']	=		'29/02/20'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/03/21','PreviousQuarter']	=		'31/12/20'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/03/21','PreviousSeasonQuarter']	=		'31/03/20'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/04/21','PreviousQuarter']	=		'31/01/21'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/04/21','PreviousSeasonQuarter']	=		'30/04/20'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/05/21','PreviousQuarter']	=		'28/02/21'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/05/21','PreviousSeasonQuarter']	=		'31/05/20'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/06/21','PreviousQuarter']	=		'31/03/21'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/06/21','PreviousSeasonQuarter']	=		'30/06/20'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/07/21','PreviousQuarter']	=		'30/04/21'	
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/07/21','PreviousSeasonQuarter']	=	'31/07/20'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/08/21','PreviousQuarter']	=		'31/05/21'	
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/08/21','PreviousSeasonQuarter']	=	'31/08/20'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/09/21','PreviousQuarter']	=		'30/06/21'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/09/21','PreviousSeasonQuarter']	=		'30/09/20'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/10/21','PreviousQuarter']	=		'31/07/21'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/10/21','PreviousSeasonQuarter']	=		'31/10/20'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/11/21','PreviousQuarter']	=		'31/08/21'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/11/21','PreviousSeasonQuarter']	=		'30/11/20'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/12/21','PreviousQuarter']	=		'30/09/21'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/12/21','PreviousSeasonQuarter']	=		'31/12/20'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/01/22','PreviousQuarter']	=		'31/10/21'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/01/22','PreviousSeasonQuarter']	=		'31/01/21'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '28/02/22','PreviousQuarter']	=		'30/11/21'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '28/02/22','PreviousSeasonQuarter']	=		'28/02/21'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/03/22','PreviousQuarter']	=		'31/12/21'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '31/03/22','PreviousSeasonQuarter']	=		'31/03/21'
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/04/22','PreviousQuarter']	=		'31/01/22'	
actualRevenue_frame.loc[actualRevenue_frame['Period End Date'] == '30/04/22','PreviousSeasonQuarter']	=	'30/04/21'
actualRevenue_frame['PreviousSeasonQuarter']= pd.to_datetime(actualRevenue_frame['PreviousSeasonQuarter'])
actualRevenue_frame['PreviousQuarter']= pd.to_datetime(actualRevenue_frame['PreviousQuarter'])
actualRevenue_frame.to_excel(path("/controlPreparation/verif.xlsx"))
print('creation de verif Rev Actual')
###################################################################################################################
#
#
#   Step5: Nettoyage fichier Revenue-Estimate (RevEstimate.xlsx)
#           - Revenue-Mean notna
#          Création DayGap : différence en jours entre la date d'estimation et la period-end-date 
# 
###################################################################################################################
erf = pd.read_excel(path("fichierDeRefinitiv/RevEstimate.xlsx"), sheet_name = sheet_name, header = header)
estimateRevenue_frame=erf[['cpy', 'Period End Date','Date','Revenue - Mean']]
result=len(estimateRevenue_frame)
estimateRevenue_frame= estimateRevenue_frame[estimateRevenue_frame['Revenue - Mean'].notna()] 
print("nettoyage revenu estimate %d",result-len(estimateRevenue_frame))
estimateRevenue_frame['Period End Date']= pd.to_datetime(estimateRevenue_frame['Period End Date']) 
estimateRevenue_frame['Date']= pd.to_datetime(estimateRevenue_frame['Date'])
estimateRevenue_frame['DayGap']= estimateRevenue_frame['Period End Date']-estimateRevenue_frame['Date']
estimateRevenue_frame.to_excel(path("etapePreparation/CleanedRevEstimate.xlsx"))
print('chargement des estimates')
print('creation CleanedRevEstimate')
###################################################################################################################
# 
#
#  Step6 :
#  link "previous Quarter" and "Previous season Quarter" informations to Revenue Actual row 
###################################################################################################################
sheet_name = 0 
header = 0 # The header is the first row
arf1 = pd.read_excel(path("etapePreparation/CleanedRevActual.xlsx"), sheet_name = sheet_name, header = header)
previousSeasonRevenue_frame=arf1[['cpy', 'Period End Date','FilingDate','Revenue - Actual','EBIT-Actual']]
previousSeasonRevenue_frame.rename(columns = {'cpy':'cpy','Period End Date' : 'PreviousSeasonQuarter', 'FilingDate' : 'Previous season FilingDate','Revenue - Actual' : 'previous season Revenue Actual','EBIT-Actual': 'previous season EBIT'}, inplace = True)

actualRevenue_frame=pd.merge(actualRevenue_frame,previousSeasonRevenue_frame,how='left',on=["cpy","PreviousSeasonQuarter"])
actualRevenue_frame.to_excel(path("controlPreparation/verif1.xlsx"))
#
previousRevenue_frame=previousSeasonRevenue_frame
previousRevenue_frame.rename(columns = {'cpy':'cpy','PreviousSeasonQuarter' : 'PreviousQuarter',  'Previous season FilingDate':'Previous FilingDate' ,'previous season Revenue Actual': 'previous Revenue Actual','previous season EBIT':'previous EBIT'}, inplace = True)
actualRevenue_frame=pd.merge(actualRevenue_frame,previousRevenue_frame,how='left',on=["cpy","PreviousQuarter"])
actualRevenue_frame.to_excel(path("controlPreparation/verif2.xlsx"))
print('Enrichissement de Actual Revenu avec les revenus précédents:  creation verif2')
###################################################################################################################
# 
#
#  Step7 : Nettoyage de actualRevenue_frame
#               -Previous season FilingDate notna (control extract1.xlsx)
#               -Previous FilingDate notna (control extract2.xlsx)
#               -FilingDate notna (control extract3.xlsx)
#
###################################################################################################################
extract1=actualRevenue_frame[actualRevenue_frame['Previous season FilingDate'].isna()]
extract1.to_excel(path("controlPreparation/extract1.xlsx"))
extract2=actualRevenue_frame[actualRevenue_frame['Previous FilingDate'].isna()]
extract2.to_excel(path("controlPreparation/extract2.xlsx"))
extract3=actualRevenue_frame[actualRevenue_frame['FilingDate'].isna()]
extract3.to_excel(path("controlPreparation/extract3.xlsx"))
print('Elimination des Revenus vides: extract1, extract2, extract3')
result=len(actualRevenue_frame)
actualRevenue_frame=actualRevenue_frame[actualRevenue_frame['Previous season FilingDate'].notna()] 
print("nettoyage revenuactual with no previous season filingdate %d",result-len(actualRevenue_frame))
result=len(actualRevenue_frame)
actualRevenue_frame=actualRevenue_frame[actualRevenue_frame['Previous FilingDate'].notna()] 
print("nettoyage revenuactual with no previous filingdate %d",result-len(actualRevenue_frame))
result=len(actualRevenue_frame)
actualRevenue_frame=actualRevenue_frame[actualRevenue_frame['FilingDate'].notna()] #
print("nettoyage revenuactual with no filingdate %d",result-len(actualRevenue_frame))
###################################################################################################################
#
#     
#   Step7:          compute      
#                           'growth Seasonality Actual' = Revenue Actual - (previous season quater Revenue Actual)/(previous season quater Revenue Actual)
#                            "growth Actual" =Revenue Actual - (previous quater Revenue actual)/(previous quater Revenue actual)
###################################################################################################################
actualRevenue_frame=actualRevenue_frame.assign(growthSeasonalityActual=(actualRevenue_frame['Revenue - Actual']-actualRevenue_frame['previous season Revenue Actual'])/actualRevenue_frame['previous season Revenue Actual'])
actualRevenue_frame=actualRevenue_frame.assign(growthActual=(actualRevenue_frame['Revenue - Actual']-actualRevenue_frame['previous Revenue Actual'])/actualRevenue_frame['previous Revenue Actual'])
actualRevenue_frame.to_excel(path("etapePreparation/actualoutput.xlsx"))
###################################################################################################################
#
#  Step8 :  Nettoyage classification ESG (classifESG.xslx)
#               - préparation d'une colonne Year
###################################################################################################################
c = pd.read_excel(path("fichierDeRefinitiv/classifESG.xlsx"), sheet_name = sheet_name, header = header)
classifESG=c[['cpy', 'Date','ESG Score']]
classifESG['Date']= pd.to_datetime(classifESG['Date'])
classifESG=classifESG.assign(Year=classifESG['Date'].dt.to_period('Y'))
classifESG=classifESG[['cpy','ESG Score','Year']]
classifESG.to_excel(path("etapePreparation/classifESG0.xlsx"))
print("creation de classif ESG")
###################################################################################################################
#
#   Step10:     creation du journal des estimés connus par jour pour une cpy+Quater
#        Construct a journal of days : key= 'Date'+'cpy'+'PeriodEndDate' : 
#                           period elligible for estimates
#                           first date = FilingDate du quarter précédent
#                           last date =  FilingDate (de ce quater)
####################################################################################################################
print('creation du journal par jour')
journal=pd.DataFrame(columns=['Date','cpy', 'Period End Date','FilingDate',"Revenue - Actual",'growthActual','growthSeasonalityActual','previous season Revenue Actual', 'previous Revenue Actual',"Revenue - Mean","DayGap","EBIT-Actual","previous season EBIT",'PreviousSeasonQuarter','PreviousQuarter'])
for i in actualRevenue_frame.index:
    print(i)
    startdate= pd.to_datetime(actualRevenue_frame['Previous FilingDate'][i]) #last issue date previous quarter
    print(startdate)
    enddate= pd.to_datetime(actualRevenue_frame['FilingDate'][i]) 
    print(enddate)
    list = pd.bdate_range(startdate, enddate) 
    calendar=pd.DataFrame(list,columns=['Date'])
    print(calendar.size)
    calendar['key']=1
    tab=np.array([[actualRevenue_frame['cpy'][i],actualRevenue_frame['Period End Date'][i],actualRevenue_frame['FilingDate'][i],actualRevenue_frame['Revenue - Actual'][i],actualRevenue_frame['growthSeasonalityActual'][i],actualRevenue_frame['growthActual'][i] ,actualRevenue_frame['previous season Revenue Actual'][i],actualRevenue_frame['previous Revenue Actual'][i],actualRevenue_frame['EBIT-Actual'][i],actualRevenue_frame['previous season EBIT'][i],actualRevenue_frame['PreviousSeasonQuarter'][i],actualRevenue_frame['PreviousQuarter'][i] ]])
    create=pd.DataFrame(tab,columns=['cpy', 'Period End Date','FilingDate','Revenue - Actual','growthActual','growthSeasonalityActual','previous season Revenue Actual','previous Revenue Actual','EBIT-Actual','previous season EBIT','PreviousSeasonQuarter','PreviousQuarter'])
    create['key']=1
    result=pd.merge(calendar,create,how='left', on = 'key')
    result=result.drop(columns='key')
###################################################################################################################
#  Step 11: 
#    merge avec le dataframe des estimés émis (Revenue et EBIT) et forwardfill pour les dates suivantes
#    merge également avec la classification ESG pour l'année en cours. 
###################################################################################################################

    result=pd.merge(result,estimateRevenue_frame,how='left',on=["Date","cpy","Period End Date"])
###################################################################################################################
# Step 11(b):
# forwardfill after merge of estimates
# the produced estimate is valid until a new one is produced
#
###################################################################################################################
    result=result.ffill(axis = 0)
    result=result.assign(Year=result['Date'].dt.to_period('Y'))
    result=pd.merge(result,classifESG,how='left', on = ['cpy','Year'])
    result.drop(columns='Year')
    print(len(result))
    journal=pd.concat([journal,result],ignore_index=True)
###################################################################################################################
#
# Step12:
#   Journal complet des estimés journalier 
#
###################################################################################################################
journal.to_excel(path("etapePreparation/output0.xlsx")) 
print('taille du journal des estimes')
print(len(journal))
journal= journal[journal['Revenue - Mean'].notna()] #estimé vide on enleve souvent en début de période élligible
print('taille du journal des estimes apres retrait des estimés vides')
print(len(journal))
print('taille du journal des estimes apres retrait des cas de previous season revenu =0')
journal= journal[journal['previous season Revenue Actual']!=0] # AMCR.K revenue=0 2019 march  to be excluded 
print(len(journal))#
###################################################################################################################
# Step 13:
#   COMPUTE GROWTH and SURPRISE ( based on estimate)
#
###################################################################################################################
journal=journal.assign(growthSeasonalityEstimate=(journal['Revenue - Mean']-journal['previous season Revenue Actual'])/journal['previous season Revenue Actual'])
journal=journal.assign(growthEstimate=(journal['Revenue - Mean']-journal['previous Revenue Actual'])/journal['previous Revenue Actual'])
journal=journal.assign(SeasonalityGrowthSurprise=journal['growthSeasonalityEstimate']-journal['growthSeasonalityActual'])
journal=journal.assign(ComputedSurprise=(100*(journal['Revenue - Actual']-journal['Revenue - Mean'])/journal['Revenue - Actual']))
journal=journal.assign(capComputedSurprise=winsorize(journal["ComputedSurprise"], limits=[0.02, 0.02])) #on cape
journal.to_excel(path("etapePreparation/output2.xlsx"))
###################################################################################################################
#
# Step14:
#        link avec la surprise Y2Y précédente 
#              et journal : journal des estimés
#           création du journal_surprise : la surprise du dernier estimé de la périod end date
#
###################################################################################################################
last_cpy=' '
last_ped='1900 1 1 '
last_date='1900 1 1 '
last_FilingDate='1900 1 1'
last_Supr=0
last_ps_ped='1900 1 1 '
journal_surprise=pd.DataFrame(columns=['Date','cpy', 'Period End Date','FilingDate',"Surprise","PreviousSeasonQuarter"])
for i in journal.index:
    print(i)
    cpy=journal['cpy'][i]
    ped=journal['Period End Date'][i]
    date=journal['Date'][i]
    Supr=journal['ComputedSurprise'][i]
    FilingDate=journal['FilingDate'][i]
    PS_Ped=journal['PreviousSeasonQuarter'][i]
    if (ped !=last_ped) or (cpy!=last_cpy):
    #capture la dernière surprise pour une key cpy+PED
        tab=np.array([[last_date,last_cpy,last_ped,last_FilingDate,last_Supr,last_ps_ped]])
        tab_frame=pd.DataFrame(tab,columns=['Date','cpy', 'Period End Date','FilingDate',"Surprise","PreviousSeasonQuarter"])
        journal_surprise=pd.concat([journal_surprise,tab_frame],ignore_index=True)
    last_cpy=cpy
    last_ped=ped
    last_date=date
    last_FilingDate=FilingDate
    last_Supr=Supr
    last_ps_ped=PS_Ped
tab=np.array([[last_date,last_cpy,last_ped,last_FilingDate,last_Supr,last_ps_ped]])
tab_frame=pd.DataFrame(tab,columns=['Date','cpy', 'Period End Date','FilingDate',"Surprise","PreviousSeasonQuarter"])
journal_surprise=pd.concat([journal_surprise,tab_frame],ignore_index=True)
#enleve le 1ier record car pris en erreur
journal_surprise = journal_surprise.iloc[1:]
journal_surprise.to_excel(path("etapePreparation/journal_surprise.xlsx")) 
print('taille du journal des surprise')
print(len(journal_surprise))
###################################################################################################################
#
#  Step 15 : ajout dans journal de la dernière Surprise par cpy+PED 'Surprise'
#
###################################################################################################################
#journal=pd.read_excel("/Users/isabelledebry/Documents/TFENOEMIE/output2.xlsx", sheet_name = sheet_name, header = header)


journal_surprise= pd.read_excel(path("etapePreparation/journal_surprise.xlsx"), sheet_name = sheet_name, header = header)
previous_surprise = pd.read_excel(path("etapePreparation/journal_surprise.xlsx"), sheet_name = sheet_name, header = header)
previous_surprise.rename(columns={'PreviousSeasonQuarter':'notused'},inplace=True)
previous_surprise.rename(columns = { "Period End Date": 'PreviousSeasonQuarter'}, inplace = True)
previous_surprise.rename(columns = { "Surprise": 'PreviousSeasonSurprise'}, inplace = True)
previous_surprise.rename(columns = { "FilingDate": 'PreviousFilingDate'}, inplace = True)
previous_surprise.rename(columns = { "Date": 'PreviousDate'}, inplace = True)
previous_surprise['PreviousSeasonQuarter']= pd.to_datetime(previous_surprise['PreviousSeasonQuarter'])
journal_surprise['PreviousSeasonQuarter']= pd.to_datetime(journal_surprise['PreviousSeasonQuarter'])

journal_surprise=pd.merge(journal_surprise[["FilingDate","cpy","Period End Date","Surprise",'PreviousSeasonQuarter']],previous_surprise[["PreviousFilingDate","cpy",'PreviousSeasonQuarter','PreviousSeasonSurprise']],how='left', on = ["cpy","PreviousSeasonQuarter"])
print('taille du journal des surprises')
print(len(journal_surprise))
journal_surprise=journal_surprise[journal_surprise['PreviousSeasonSurprise'].notna()] 
print('taille du journal des surprises après nettoyage des surprises previous Y2Y vide')
print(len(journal_surprise))
journal_surprise.to_excel(path("etapePreparation/journal_previous_surprise.xlsx")) 
print('creation de journal_previous_surprise')

###################################################################################################################
#
#  Step 16 : ajout dans output de PreviousSeasonSurprise
#
###################################################################################################################
journal=pd.merge(journal,journal_surprise[["cpy",'Period End Date','Surprise','PreviousSeasonSurprise']],how='left', on = ["cpy","Period End Date"])
journal.to_excel(path("etapePreparation/output1.xlsx"))

# Step 17 : ajout du nb d'employé et secteurs d'activité
classif= pd.read_excel(path("fichierDeRefinitiv/classif.xlsx"), sheet_name = sheet_name, header = header)
classif=classif[['cpy','Business Sector','Number of Employees']]
journal=pd.merge(journal,classif,how='left',on=["cpy"])
###################################################################################################################

# step 18: creation d'un journal de publication d'estimé EBIT Mean
###################################################################################################################
EBITMean = pd.read_excel(path("fichierDeRefinitiv/EBITMean.xlsx"), sheet_name = sheet_name, header = header)
EBITMean= EBITMean[EBITMean['Date'].notna()] 
EBITMean['Date']= pd.to_datetime(EBITMean['Date'])
Cpy=pd.read_excel(path("fichierDeRefinitiv/company.xlsx"), sheet_name = sheet_name, header = header)
journalEBIT=pd.DataFrame(columns=['Date','cpy', 'Period End Date','Year-EBIT-Mean'])
for i in Cpy.index:
    list = pd.bdate_range(dateDebutJournalEbit, dateFinJournalEBIT)
    calendar=pd.DataFrame(list,columns=['Date'])
    calendar['key']=1
    tab=np.array([[Cpy['cpy'][i]]])
    create=pd.DataFrame(tab,columns=['cpy'])
    create['key']=1
    result=pd.merge(calendar,create,how='left', on = 'key')
    result=result.drop(columns='key')
    result=pd.merge(result,EBITMean,how='left',on=["Date","cpy"])
    result=result.ffill(axis = 0)
    journalEBIT=pd.concat([journalEBIT,result],ignore_index=True)
journalEBIT= journalEBIT[journalEBIT['Year-EBIT-Mean'].notna()] 
journalEBIT.to_excel(path("etapePreparation/EBITMean0.xlsx")) 
print("creation journal des estimes EBITMean0")

#journalEBIT=pd.read_excel(path("etapePreparation/EBITMean0.xlsx")) 
#journal= pd.read_excel(path("etapePreparation/output1.xlsx"))

journalEBIT.rename(columns = { 'Period End Date': 'Annual Period End Date'}, inplace = True)
journal=pd.merge(journal,journalEBIT,how='left', on = ["Date","cpy"])


#journal= pd.read_excel(path("etapePreparation/output.xlsx"))

###################################################################################################################

#  Step 19: verification des données EBIT, surprise et creation capsurprise
###################################################################################################################
print('avant retrait des na')
print(len(journal))
journal= journal[journal['Year-EBIT-Mean'].notna()]
journal= journal[journal['Year-EBIT-Mean'].notnull()]
journal= journal[journal['Surprise'].notna()]
journal=journal.assign(capSurprise=winsorize(journal["Surprise"], limits=[0.005, 0.005])) 
journal.rename(columns = { 'EstimateSurprise': 'ComputedSurprise'}, inplace = True)
print('après retrait des na')
print(len(journal))

###################################################################################################################
 # Step 20: ajout des données quasi-statiques 
 ###################################################################################################################

def classifier_emp(row):
    if row["Number of Employees"] < 1000:
            return "small"
    elif row["Number of Employees"] <10000 :
        return "medium"
    elif row["Number of Employees"] <100000 :
        return "big"        
    else:
        return "huge"

def classifier_business(row):
    if (row["Business Sector"] =='Banks' or row["Business Sector"] =='Investment Banks'):
            return "Finance"
    elif (row["Business Sector"] =='Other Financial'or row["Business Sector"] =='Other Insurance') :
        return "Finance" 
    elif (row["Business Sector"] =='Asset Management & Custody Banks'or row["Business Sector"] =='Asset Managers') :
        return "Finance" 
    elif (row["Business Sector"] =='Consumer Finance'or row["Business Sector"] =='Financial Exchanges & Data') :
        return "Finance" 
    elif (row["Business Sector"] =='Insurance - Non-Life'or row["Business Sector"] =='Insurance Brokers') :
        return "Finance" 
    elif (row["Business Sector"] =='Investment Entities (ineligible for indices inclusion)'or row["Business Sector"] =='Life Assurance') :
        return "Finance" 
    elif (row["Business Sector"] =='Re-insurance'or row["Business Sector"] =='Real Estate Holding & Development') :
        return "Finance"     
    elif (row["Business Sector"] =='Real Estate Services'or row["Business Sector"] =='Regional Banks') :
        return "Finance" 
    elif (row["Business Sector"] =='Building & Construction Materials'	or row["Business Sector"] =='Building Products') :
        return "Real Estate" 
    elif (row["Business Sector"] =='Construction Materials'	or row["Business Sector"] =='Furnishings & Floor Coverings') :
        return "Real Estate"
    elif (row["Business Sector"] =='House Building'	or row["Business Sector"] =='Household Appliances & Housewares') :
        return "Real Estate"    
    elif (row["Business Sector"] =='Household Products'	or row["Business Sector"] =='Other Construction') :
        return "Real Estate"
    elif (row["Business Sector"] ==  'Clothing & Footwear') :
        return 'Real Estate'
    elif (row["Business Sector"] =='Aerospace & Defense'	or row["Business Sector"] =='Defence') :
        return 'Defense'	
    elif (row["Business Sector"] ==  'Beverages - Brewers'	or row["Business Sector"] =='Packaged Foods & Meats') :
        return 'Utilities'
    elif (row["Business Sector"] =='Beverages - Distillers & Vintners'	or row["Business Sector"] =='Food Processors') :
        return 'Utilities'
    elif (row["Business Sector"] =='Soft Drinks'	or row["Business Sector"] =='Water') :
        return 'Utilities'	
    elif (row["Business Sector"] =='Casinos & Gaming'	or row["Business Sector"] =='Gambling') :
        return 'Utilities'	
    elif (row["Business Sector"] =='Health Care Equipment'	or row["Business Sector"] =='Health Care Facilities') :
        return 'Healthcare' 		
    elif (row["Business Sector"] =='Health Care Services'	or row["Business Sector"] =='Health Maintenance Organisations') :
        return 'Healthcare' 
    elif (row["Business Sector"] =='Hospital Management & Long Term Care'	or row["Business Sector"] =='Managed Health Care') :
        return 'Healthcare' 
    elif (row["Business Sector"] =='Medical Equipment & Supplies'	or row["Business Sector"] =='Other Health Care') :
        return 'Healthcare' 
    elif (row["Business Sector"] =='Pharmaceuticals'	) :
        return 'Healthcare'        
    elif (row["Business Sector"] =='Hotels'	or row["Business Sector"] =='Hotels, Resorts & Cruise Lines') :
        return 'Utilities'
    elif (row["Business Sector"] =='Restaurants'	or row["Business Sector"] =='Restaurants and Pubs') :
        return 'Utilities'	
    elif (row["Business Sector"] =='Chemicals - Advanced Materials'	or row["Business Sector"] =='Chemicals - Commodity') :
        return 'Industry'	    
    elif (row["Business Sector"] =='Chemicals - Speciality'	or row["Business Sector"] =='Commodity Chemicals') :
        return 'Industry'	
    elif (row["Business Sector"] =='Diversified Industrials'	or row["Business Sector"] =='Electric Utilities') :
        return 'Industry'
    elif (row["Business Sector"] =='Electrical Components & Equipment'	or row["Business Sector"] =='Electrical Equipment') :
        return 'Industry'
    elif (row["Business Sector"] =='Electricity'	or row["Business Sector"] =='Electronic Equipment') :
        return 'Industry'	
    elif (row["Business Sector"] =='Electronic Equipment & Instruments'	or row["Business Sector"] =='Electronic Manufacturing Services') :
        return 'Industry'
    elif (row["Business Sector"] =='Engineering - Fabricators'	or row["Business Sector"] =='Engineering - General') :
        return 'Industry'
    elif (row["Business Sector"] =='Environment Control'	or row["Business Sector"] =='Fertilizers & Agricultural Chemicals') :
        return 'Industry'	
    elif (row["Business Sector"] =='Gas Distribution'or row["Business Sector"] =='Industrial Gases') :
        return 'Industry'
    elif (row["Business Sector"] =='Industrial Machinery'	or row["Business Sector"] =='Oil - Integrated') :
        return 'Industry'
    elif (row["Business Sector"] =='Oil - Services'	or row["Business Sector"] =='Oil & Gas - Exploration & Production') :
        return 'Industry'	
    elif (row["Business Sector"] =='Oil & Gas Equipment & Services'or row["Business Sector"] =='Oil & Gas Exploration & Production') :
        return 'Industry'
    elif (row["Business Sector"] =='Oil & Gas Refining & Marketing'	or row["Business Sector"] =='Oil & Gas Storage & Transportation') :
        return 'Industry'
    elif (row["Business Sector"] =='Other Textiles & Leather Goods'	or row["Business Sector"] =='Paper') :
        return 'Industry'
    elif (row["Business Sector"] =='Paper Packaging'	or row["Business Sector"] =='Semiconductor Equipment') :
        return 'Industry'	
    elif (row["Business Sector"] =='Semiconductors'or row["Business Sector"] =='Specialty Chemicals') :
        return 'Industry'
    elif (row["Business Sector"] =='Steel'or row["Business Sector"] =='Biotechnology') :
        return 'Industry'
    elif (row["Business Sector"] =='Application Software'	or row["Business Sector"] =='Computer Hardware') :
        return 'IT'	
    elif (row["Business Sector"] =='Computer Services'or row["Business Sector"] =='Consumer Electronics') :
        return 'IT'
    elif (row["Business Sector"] =='Data Processing & Outsourced Services'	or row["Business Sector"] =='IT Consulting & Other Services') :
        return 'IT'	
    elif (row["Business Sector"] =='Software'or row["Business Sector"] =='Systems Software') :
        return 'IT'	
    elif (row["Business Sector"] =='Technology Hardware, Storage & Peripherals') :
        return 'IT'	
    elif (row["Business Sector"] =='Leisure Equipment'	or row["Business Sector"] =='Leisure Facilities') :
        return 'Utilities'	
    elif (row["Business Sector"] =='Movies & Entertainment'or row["Business Sector"] =='Subscription Entertainment Networks') :
        return 'Utilities'
    elif (row["Business Sector"] =='Movies & Entertainment'or row["Business Sector"] =='Subscription Entertainment Networks') :
        return 'Utilities'	
    elif (row["Business Sector"] =='Tobacco') :
        return 'Utilities'
    elif (row["Business Sector"] =='Apparel, Accessories & Luxury Goods') :
        return 'Utilities'
    elif (row["Business Sector"] =='Miscellaneous') :
        return 'Miscellaneous'
    elif (row["Business Sector"] =='Gold Mining'or row["Business Sector"] =='Other Mineral Extractors & Mines') :
        return 'Materials' 
    elif (row["Business Sector"] =='Discount & Super Stores and Warehouses'or row["Business Sector"] =='Drug Retail') :
        return 'Retail'
    elif (row["Business Sector"] =='Food & Drug Retailers'or row["Business Sector"] =='Retail REITs') :
        return 'Retail'	    
    elif (row["Business Sector"] =='Retailers - Hardlines'or row["Business Sector"] =='Retailers - Multi Department') :
        return 'Retail'	    
    elif (row["Business Sector"] =='Retailers - Soft Goods'or row["Business Sector"] =='Retailers e-commerce') :
        return 'Retail'	   
    elif (row["Business Sector"] =='Specialized REITs'or row["Business Sector"] =='Specialty Stores') :
        return 'Retail'	

    elif (row["Business Sector"] =='Business Support Services'	or row["Business Sector"] =='Delivery Services') :
        return 'Services'	   
    elif (row["Business Sector"] =='Education, Business Training & Employment Agencies'or row["Business Sector"] =='Life Sciences Tools & Services') :
        return 'Services'	
    elif (row["Business Sector"] =='Multi - Utilities'	or row["Business Sector"] =='Personal Products') :
        return 'Services'	   
    elif (row["Business Sector"] =='Publishing'or row["Business Sector"] =='Publishing & Printing') :
        return 'Services'
    elif (row["Business Sector"] =='Research & Consulting Services'or row["Business Sector"] =='Transaction and Payroll Services') :
        return 'Services' 
    elif (row["Business Sector"] =='Broadcasting'or row["Business Sector"] =='Cable & Satellite') :
        return 'Telecom'
    elif (row["Business Sector"] =='Communications Equipment'or row["Business Sector"] =='Fixed-Line Telecommunication Services') :
        return 'Telecom'
    elif (row["Business Sector"] =='Internet & Direct Marketing Retail'or row["Business Sector"] =='Media Agencies') :
        return 'Telecom'
    elif (row["Business Sector"] =='Telecommunications Equipment'or row["Business Sector"] =='Television, Radio and Filmed Entertainment') :
        return 'Telecom'	
    elif (row["Business Sector"] =='Wireless Telecommunication Services') :
        return 'Telecom'
    elif (row["Business Sector"] =='Aerospace'	or row["Business Sector"] =='Airlines & Airports') :
        return 'Transport'
    elif (row["Business Sector"] =='Auto Parts'	or row["Business Sector"] =='Auto Parts & Equipment') :
        return 'Transport'
    elif (row["Business Sector"] =='Automobile Manufacturers'	or row["Business Sector"] =='Automobiles') :
        return 'Transport'
    elif (row["Business Sector"] =='Commercial Vehicles & Trucks'	or row["Business Sector"] =='Rail, Road & Freight') :
        return 'Transport'
    elif (row["Business Sector"] =='Vehicle Distribution') :
        return 'Transport'	
    else:
        return "others"

def classifier_ESG(row):
    if (row["ESG Score"] <25):
            return "to_improve"
    elif (row["ESG Score"] <50) :
        return "neutral"   
    elif (row["ESG Score"] <75) :
        return "good"      
    else:
        return "very good"



journal["Size"] = journal.apply(classifier_emp, axis=1)
journal["ESG"] = journal.apply(classifier_ESG, axis=1)
journal["Business"] = journal.apply(classifier_business, axis=1)

journal.to_excel("/Users/isabelledebry/Documents/TFENOEMIE/etapePreparation/output.xlsx")
print('creation de output.xlsx')

###################################################################################################################
#  Step 20: 
#   CREATION des fichiers d'apprentissage TRAIN TEST 
###################################################################################################################

def create_file (datecoupurestart,datecoupureend,nametrain,nametest,nameextract ):
    data=journal
    train=data[data['Date']<=pd.to_datetime(datecoupurestart) ]
    train=train[train['FilingDate']<pd.to_datetime(datecoupurestart)]
    train.to_excel(nametrain)
    print(len(train))
    test=data[data['Date']>pd.to_datetime(datecoupurestart) ]
    test=test[test['FilingDate']<pd.to_datetime(datecoupureend)]
    test=test[test['Period End Date']>pd.to_datetime(datecoupurestart)]
    extract4=test[test['PreviousSeasonSurprise'].isna()]
    extract4.to_excel(nameextract)
    print('taille du journal test des estimes')
    print(len(test))
    test= test[test['PreviousSeasonSurprise'].notna()] #PreviousSeasonSurprise vide on enleve souvent en début de période élligible
    print('taille du journal test des estimes apres retrait des PreviousSeasonSurprise vides')
    print(len(test))
    test.to_excel(nametest)


datecoupurestart= '2019 12 31'
datecoupureend='2020 12 31'
nametrain=path("fichiersApprentissage/train_20.xlsx")
data=journal
train=data[data['Date']<=pd.to_datetime(datecoupureend) ]
train=train[train['FilingDate']<pd.to_datetime(datecoupureend)]
train=train[train['Date']>pd.to_datetime(datecoupurestart) ]
train=train[train['FilingDate']>pd.to_datetime(datecoupurestart)]
train.to_excel(nametrain)

datecoupurestart= '2018 12 31'
datecoupureend='2019 12 31'
nametrain=path("fichiersApprentissage/train_19.xlsx")
data=journal
train=data[data['Date']<=pd.to_datetime(datecoupureend) ]
train=train[train['FilingDate']<pd.to_datetime(datecoupureend)]
train=train[train['Date']>pd.to_datetime(datecoupurestart) ]
train=train[train['FilingDate']>pd.to_datetime(datecoupurestart)]
train.to_excel(nametrain)

datecoupurestart= '2018 12 31'
datecoupureend='2020 12 31'
nametrain=path("fichiersApprentissage/train_19_20.xlsx")
data=journal
train=data[data['Date']<=pd.to_datetime(datecoupureend) ]
train=train[train['FilingDate']<pd.to_datetime(datecoupureend)]
train=train[train['Date']>pd.to_datetime(datecoupurestart) ]
train=train[train['FilingDate']>pd.to_datetime(datecoupurestart)]
train.to_excel(nametrain)


datecoupurestart= '2019 12 31'
datecoupureend='2020 12 31'
nametest=path("fichiersApprentissage/test_20.xlsx")
nameextract=path("controlPreparation/extract4_20.xlsx")
data=journal
test=data[data['Date']>pd.to_datetime(datecoupurestart) ]
test=test[test['FilingDate']>pd.to_datetime(datecoupurestart)]
test=test[test['Period End Date']>pd.to_datetime(datecoupurestart)]
test=test[test['FilingDate']<pd.to_datetime(datecoupureend)]
extract4=test[test['PreviousSeasonSurprise'].isna()]
extract4.to_excel(nameextract)
print('taille du journal test des estimes')
print(len(test))
test= test[test['PreviousSeasonSurprise'].notna()]
test.to_excel(nametest)

datecoupurestart= '2020 12 31'
datecoupureend='2021 12 31'
nametest=path("fichiersApprentissage/test_21.xlsx")
nameextract=path("controlPreparation/extract4_21.xlsx")
data=journal
test=data[data['Date']>pd.to_datetime(datecoupurestart) ]
test=test[test['FilingDate']>pd.to_datetime(datecoupurestart)]
test=test[test['Period End Date']>pd.to_datetime(datecoupurestart)]
test=test[test['FilingDate']<pd.to_datetime(datecoupureend)]
extract4=test[test['PreviousSeasonSurprise'].isna()]
extract4.to_excel(nameextract)
print('taille du journal test des estimes')
print(len(test))
test= test[test['PreviousSeasonSurprise'].notna()]
test.to_excel(nametest)


datecoupurestart= '2020 12 31'
datecoupureend='2021 12 31'
nametrain=path("fichiersApprentissage/train.xlsx")
nametest=path("fichiersApprentissage/test.xlsx")
nameextract=path("controlPreparation/extract4.xlsx")
create_file (datecoupurestart,datecoupureend,nametrain,nametest,nameextract )