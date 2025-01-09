import os
import shutil
from pathlib import Path

import pdf2image
from PyPDF2 import PdfWriter, PdfReader, PdfMerger

import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from PIL import Image

import pandas as pd

def pdfFileList(filePath):
    BatchDir = os.path.join(filePath)
    TargetDir = os.listdir(BatchDir)
    data = []
    for i in TargetDir:
        data.append({
            "filePath": BatchDir,
            "fileName": i,
            "fileType": Path(i).suffix
                    })
    df = pd.DataFrame(data) 
    return BatchDir, df

def pdfFileReadChecking(filePath, fileName,fileType):
    fileName_Dir = os.path.join(filePath, fileName)
    if fileType == (".pdf"):
        try:
            x = extractText(filePath,fileName, 0 )
            return "00 - Readable PDF"
        except Exception as e:
            return "02 - Unreadable PDF"
    else:
        return "01 - Not PDF"

def _mkdir(directory_name):
    try:
        shutil.rmtree(directory_name)  # Remove directory and its contents
        try:
            os.mkdir(directory_name)
            return '00 - Able to Create Directory'
        except OSError as e:
            return '01 - Unable to Create Directory'
    except OSError as e:
        try:
            os.mkdir(directory_name)
            return '00 - Able to Create Directory'
        except OSError as e:
            return '01 - Unable to Create Directory'

def extractText(filePath, fileName, pageNum):
    filePath = os.path.join(filePath, fileName) 
    text = ''
    with open(filePath, 'rb') as file:
        reader = PdfReader(file)
        text = reader.pages[pageNum].extract_text()
    return text



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


def measurePDFSize(filePath,fileName):
    XBatchDir = os.path.join(filePath,fileName)
    try:
        reader = PdfReader(XBatchDir)
        noPage = len(reader.pages)
        page = reader.pages[0]
        text = page.extract_text()
        pdfPageSize = reader.pages[0].mediabox
        pdf_x_size = pdfPageSize[2]
        pdf_y_size = pdfPageSize[3]
        return '00 - Able to Measure PDF', pdf_x_size, pdf_y_size, noPage
    except OSError as e:
        return '01 - Unable to Measure PDF', 0, 0, 0

def transformGrayScale(imgName,outputPath,inputPath):
    try:
        # Open the image
        # print(imgName)
        # print(type(imgName))
        fileList = []
        for i in imgName:
            imageName = os.path.join(inputPath,i)
            
            image = Image.open(imageName).convert('L')  # Convert to grayscale
            
            
            image_width, image_height = image.size
            
            # Desired DPI for the figure
            my_dpi = 300.
            
            # Create the figure with adjusted dimensions based on image size and DPI
            fig, ax = plt.subplots(figsize=(float(image.size[0]) / my_dpi, float(image.size[1]) / my_dpi), dpi=my_dpi)
            
            # Invert the Y-axis to move (0, 0) to the bottom left corner
            ax.set_ylim(bottom=0, top=image.size[1])
            
            # Remove whitespace from around the image
            fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
            
            # Set major and minor gridding intervals
            major_interval = 100.
            minor_interval = 25  # Adjust this value to control the minor grid spacing
            
            # Create locators for major and minor ticks
            major_locator = plticker.MultipleLocator(base=major_interval)
            minor_locator = plticker.MultipleLocator(base=minor_interval)
            
            # Set major and minor tick locators for both axes
            ax.xaxis.set_major_locator(major_locator)
            ax.xaxis.set_minor_locator(minor_locator)
            ax.yaxis.set_major_locator(major_locator)
            ax.yaxis.set_minor_locator(minor_locator)
            
            # Add major and minor grid lines with different linestyles
            ax.grid(which='major', axis='both', linestyle='-', linewidth=1)  # Major grid
            ax.grid(which='minor', axis='both', linestyle='--', linewidth=0.5, alpha=0.7)  # Minor grid, adjust alpha for transparency
            
            # Add the grayscale image (without displaying it)
            ax.imshow(image, extent=(0, image.size[0], 0, image.size[1]), alpha=1, cmap='gray')  # Use 'gray' colormap
            
            # Adjust limits to match image size (no scaling)
            ax.set_xlim(0, image.size[0])
            ax.set_ylim(0, image.size[1])
            
            # Save the figure as PNG (without the image data)
            grayImage = os.path.join(outputPath,i[:-4]+'grid_Grey.png')
            fig.savefig(grayImage, dpi=my_dpi, transparent=True)
            GrayfileName = i[:-4]+'grid_Grey.png'
            fileList.append(GrayfileName)
            
        return '00 - Able to Transform to GrayScale' , fileList
    except OSError as e:
        return '01 - Unable to Transform to GrayScale' , []
