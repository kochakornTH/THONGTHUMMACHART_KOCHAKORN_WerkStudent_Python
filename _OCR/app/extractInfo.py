import os
import pandas as pd

import nltk
from PyPDF2 import PdfWriter, PdfReader, PdfMerger
from cleanInfo import clean_text

# To extract company name from FieldInfoValues which extract by OCR
def extractCompanyName(FieldInfoValues,companyCD,CompanyNameFormat):
    companySplitList = clean_text(FieldInfoValues['companyAdress']).split()
    companyPOSList =  CompanyNameFormat[companyCD]['CompanyNamePosition']
    
    resultCompanyName = ''
    for i in companyPOSList:
        resultCompanyName = resultCompanyName + ' ' + companySplitList[i]
    resultCompanyName = resultCompanyName[1:]
    return resultCompanyName

# To get value from dict
def extractValuefromDict(FieldInfoValues,fieldDictName):
    result = FieldInfoValues[fieldDictName]
    return result

# To Find company name by skimming from pdf and match with companyList
## NEED THE IMPROVEMENT!!!!
def findCompanyFn(readStatus,filePath,fileName,companyList):
    fileName_DirPDF = os.path.join(filePath, fileName)
    if readStatus == 'Readable':
        text = extractText(filePath,fileName, 0 )
        tokens = nltk.word_tokenize(text)
        
        numMatch = 0
        companyMatch = []
        for j in companyList:
            countx = 0
            for i in tokens:
                if i.lower() == j.lower() :
                    countx = countx + 1
                else :
                    countx = countx + 0
            if countx == 1 :
                numMatch = numMatch+1
                companyMatch.append(j)
            else: 
                numMatch = numMatch+0
        
        if numMatch == 1:
            return pd.Series(['01 - Can find company name', companyMatch[0]])
        else:
            return pd.Series(['02 - CANNOT find company name', companyMatch])
    else:
        return pd.Series(['02 - CANNOT find company name', [] ])
    
# Basic extract text from PDF to check error of the PDF too    
def extractText(filePath, fileName, pageNum):
    filePath = os.path.join(filePath, fileName) 
    text = ''
    try:
        with open(filePath, 'rb') as file:
            reader = PdfReader(file)
            text = reader.pages[pageNum].extract_text()
    except Exception as e:
        print(f"Error extracting text from {filePath}: {e}")
    return text

# Extract Invoice no. from OCR extracted field
def extractInvNo(field_invoiceNumber,companyCD,ReciptInvNoFormat):
    listText = clean_text(field_invoiceNumber).split()
    invposition = ReciptInvNoFormat[companyCD]['InvNoPosition']
    result_invNo = listText[invposition]
    return result_invNo

# # Find company from 
# def findCompanyFn(readStatus,filePath,fileName,companyList):
#     fileName_DirPDF = os.path.join(filePath, fileName)
#     if readStatus == 'Readable':
#         text = extractText(filePath,fileName, 0 )
#         tokens = nltk.word_tokenize(text)
        
#         numMatch = 0
#         companyMatch = []
#         for j in companyList:
#             countx = 0
#             for i in tokens:
#                 if i.lower() == j.lower() :
#                     countx = countx + 1
#                 else :
#                     countx = countx + 0
#             if countx == 1 :
#                 numMatch = numMatch+1
#                 companyMatch.append(j)
#             else: 
#                 numMatch = numMatch+0
        
#         if numMatch == 1:
#             return pd.Series(['01 - Can find company name', companyMatch[0]])
#         else:
#             return pd.Series(['02 - CANNOT find company name', companyMatch])
#     else:
#         return pd.Series(['02 - CANNOT find company name', [] ])