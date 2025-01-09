import os
import pytesseract
from PIL import Image


def ocrFieldInfoValues(logExportFileSplittedImg,filePath,fileName,splittedImgDirName):
    xotPath= os.path.join(filePath,splittedImgDirName)
    splittedImgFileDir = logExportFileSplittedImg
    FieldInfoValues = {'invoiceNumber':[]
             , 'invoiceDate':[]
             , 'grossAMT':[]
             , 'companyAdress':[]
             , 'TableLeft':[]
             , 'topVerify':[]
             , 'botVerify':[]}
    fileNamex = fileName[:-4]
    for i in splittedImgFileDir:
        if ("invoiceNumber" in i) & (fileNamex in i): 
            FieldInfoValues['invoiceNumber'] = pytesseract.image_to_string(Image.open(os.path.join(xotPath, i)))
        elif ("invoiceDate" in i) & (fileNamex in i): 
            FieldInfoValues['invoiceDate'] = pytesseract.image_to_string(Image.open(os.path.join(xotPath, i)))
        elif ("grossAMT" in i) & (fileNamex in i): 
            FieldInfoValues['grossAMT'] = pytesseract.image_to_string(Image.open(os.path.join(xotPath, i)))
        elif ("TableLeft" in i) & (fileNamex in i): 
            FieldInfoValues['TableLeft'] = pytesseract.image_to_string(Image.open(os.path.join(xotPath, i)))
        elif ("companyAdress" in i) & (fileNamex in i): 
            FieldInfoValues['companyAdress'] = pytesseract.image_to_string(Image.open(os.path.join(xotPath, i)))
        elif ("topVerify" in i) & (fileNamex in i): 
            FieldInfoValues['topVerify'] = pytesseract.image_to_string(Image.open(os.path.join(xotPath, i)))
        elif("botVerify" in i) & (fileNamex in i): 
            FieldInfoValues['botVerify'] = pytesseract.image_to_string(Image.open(os.path.join(xotPath, i)))
        else:
            1==1
    return FieldInfoValues