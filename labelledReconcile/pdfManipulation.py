import os
import shutil
from pathlib import Path

import pdf2image
from PyPDF2 import PdfWriter, PdfReader, PdfMerger

import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from PIL import Image

import pandas as pd
import ast
from cvDetection import detect_rectangle

def adjCoordiateforPDF(rectangle_coords,pdf_x_size,pdf_y_size):
    areaTopL = rectangle_coords[0]
    areaBotR = rectangle_coords[1]
    min_origin = rectangle_coords[2]
    max_origin = rectangle_coords[3]
    
    LL = rectangle_coords[0][0],rectangle_coords[1][1]
    UR = rectangle_coords[1][0],rectangle_coords[0][1]
    MAX_X = rectangle_coords[3][0]
    MAX_Y = rectangle_coords[3][1]
    LL_inv = rectangle_coords[0][0],MAX_Y - rectangle_coords[1][1]
    UR_inv = rectangle_coords[1][0],MAX_Y - rectangle_coords[0][1]
    x_prf_ratio = (pdf_x_size/MAX_X)
    y_prf_ratio = (pdf_y_size/MAX_Y)
    # ___
    adj_LL = float(LL_inv[0]*x_prf_ratio),float(LL_inv[1]*y_prf_ratio)
    adj_UR = float(UR_inv[0]*x_prf_ratio),float(UR_inv[1]*y_prf_ratio)

    return adj_LL, adj_UR

def splitFunctionByCoor(FieldInfoDictCoor,filePath,fieldList,colorInfoDict,image_path,labelledFileName,pdf_x_size,pdf_y_size,BatchName,fileName,splittedDirName):
    logExportFile = []
    for i in fieldList:
        color_to_detect = colorInfoDict[i]
        rectangle_coords = detect_rectangle(image_path, color_to_detect) 
        if rectangle_coords:  # Check if rectangle was actually detected
            adj_LL, adj_UR = adjCoordiateforPDF(rectangle_coords,pdf_x_size,pdf_y_size)
            fileName_DirPDF = os.path.join(filePath,BatchName ,fileName )
            reader = PdfReader(fileName_DirPDF)
            page = reader.pages[0]
            page.mediabox.lower_left = adj_LL
            page.mediabox.upper_right = adj_UR

            exportFileName = os.path.join(filePath,splittedDirName,fileName.replace('.pdf','')+'_'+i+'_.pdf')
            exportFileNameForLoging = fileName.replace('.pdf','')+'_'+i+'_.pdf'
            with open(exportFileName,'wb') as fp:
                writer = PdfWriter()
                writer.add_page(page)
                writer.write(fp)
            FieldInfoDictCoor[i] = [adj_LL, adj_UR]
            logExportFile.append(exportFileNameForLoging)
        else:
            1== 1
            FieldInfoDictCoor[i] = []
    outputdict = {'labelledFileName':[labelledFileName],'FieldInfoDictCoor':[FieldInfoDictCoor]}
    return outputdict, logExportFile

def splitByColor(pdfBucket,BatchName,fileName,filePath,labelledDirName,FieldInfoDictCoor,fieldList,colorInfoDict,pdf_x_size,pdf_y_size,splittedDirName):
    results = []
    logExportFilePDF = []
    for k in pdfBucket:
        image_path = os.path.join(filePath,labelledDirName,k)
        outputdict, logExportFile = splitFunctionByCoor(FieldInfoDictCoor,filePath,fieldList,colorInfoDict,image_path,k,pdf_x_size,pdf_y_size,BatchName,fileName,splittedDirName)
        results.append(str(outputdict))
        logExportFilePDF.append(logExportFile)
    return results,logExportFilePDF

def findLabelledPage(numPage,splitResult):
    labelledPage = 0
    labelledIndexPage = []
    xDict = dict()
    for i in range(0,numPage):
        x = splitResult[i]
        y = ast.literal_eval(x)
        labelsFileName = y['labelledFileName']
        labelsCoordinate = y['FieldInfoDictCoor'][0]

        xDict['page_'+str(i)] = labelsCoordinate
        
        if len(labelsCoordinate['invoiceNumber']) == 0 :
            labelledPage = labelledPage + 0
        else:
            labelledPage = labelledPage + 1    
            labelledIndexPage.append(i)
    return labelledPage, labelledIndexPage,xDict

def pdfToImage(filePath, fileName, outputPath):
    XBatchDir = os.path.join(filePath,fileName)
    exportDir = outputPath
    try:
        images = pdf2image.convert_from_path(XBatchDir)
        imgName = fileName[:-4]
        kxk = []
        for i in range(len(images)):
            imageNameX = imgName+'_'+str(i+1)+"_image.png"
            images[i].save(os.path.join(exportDir,imageNameX), 'PNG')            
            kxk.append(imageNameX)
        return '00 - Transformable to Image', kxk
    except OSError as e:
        return '01 - Untransformable to Image', []

def splittedPDFtoImage(filePath,splittedDirName,splittedImgDirName,logExportFilePDF):
    xinPath = os.path.join(filePath,splittedDirName)
    xotPath = os.path.join(filePath,splittedImgDirName)
    splittedPicLog = []
    for i in logExportFilePDF[0]:
        exportFile_sts,exportFileName = pdfToImage(xinPath, i, xotPath)
        splittedPicLog.append(exportFileName[0])
    return splittedPicLog

