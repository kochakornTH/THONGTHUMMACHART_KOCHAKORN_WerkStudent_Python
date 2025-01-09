import os
import pandas as pd

import nltk
from PyPDF2 import PdfWriter, PdfReader, PdfMerger
from cleanInfo import clean_text


def extractValuefromDict(FieldInfoValues,fieldDictName):
    result = FieldInfoValues[fieldDictName]
    return result

def extractInvNo(field_invoiceNumber,companyCD,ReciptInvNoFormat):
    listText = clean_text(field_invoiceNumber).split()
    invposition = ReciptInvNoFormat[companyCD]['InvNoPosition']
    result_invNo = listText[invposition]
    return result_invNo

def extractCompanyName(FieldInfoValues,companyCD,CompanyNameFormat):
    companySplitList = clean_text(FieldInfoValues['companyAdress']).split()
    companyPOSList =  CompanyNameFormat[companyCD]['CompanyNamePosition']
    
    resultCompanyName = ''
    for i in companyPOSList:
        resultCompanyName = resultCompanyName + ' ' + companySplitList[i]
    resultCompanyName = resultCompanyName[1:]
    return resultCompanyName

def field_X_Coordinate(CoordinateForSplitting,):    
    Dict_Field_x_Coor = {'invoiceNumber':dict()
                     , 'invoiceDate':dict()
                     , 'grossAMT':dict()
                     , 'companyAdress':dict()
                     , 'TableLeft':dict()
                     # , 'TableRight':dict()
                     , 'topVerify':dict()
                     , 'botVerify':dict()}
    xList = list(CoordinateForSplitting)
    fieldList = list(Dict_Field_x_Coor)
    for i in xList:
        for j in fieldList:
            if len(CoordinateForSplitting[i][j]) == 2:
                Dict_Field_x_Coor[j]['pages'] = i
                Dict_Field_x_Coor[j]['coordinate'] = CoordinateForSplitting[i][j]
                

    return Dict_Field_x_Coor