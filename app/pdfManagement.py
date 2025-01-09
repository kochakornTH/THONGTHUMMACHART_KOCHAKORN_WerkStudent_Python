import os
from PyPDF2 import PdfWriter, PdfReader, PdfMerger
import pdf2image
import cv2

# Measure PDF page size
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
    
# Transfrom PDF to Image PNG
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

# Adjust coordinate for crop before OCR
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
    x_prf_ratio = (float(pdf_x_size)/float(MAX_X))
    y_prf_ratio = (float(pdf_y_size)/float(MAX_Y))
    # ___
    adj_LL = float(LL_inv[0]*x_prf_ratio),float(LL_inv[1]*y_prf_ratio)
    adj_UR = float(UR_inv[0]*x_prf_ratio),float(UR_inv[1]*y_prf_ratio)

    return adj_LL, adj_UR
    
# crop PDF to small PDF
def PNGtoSplit(filePath,fileName,result_fieldCoordinate,logExportFileSplittedImg,pdf_x_size_x,pdf_y_size_x,impageDirName,splittedDirName):
    listField = list(result_fieldCoordinate)
    imgPath = os.path.join(filePath,impageDirName)
    
    splittedPDFLog = []
    for i in listField:
        try: 
            rectangle_coords = result_fieldCoordinate[i]['coordinate']
            imgName = fileName[:-4]+'_'+str(int(result_fieldCoordinate[i]['pages'].split('_')[1])+1)+'_image.png'
            image_path = os.path.join(imgPath,imgName)
            pdf_path = os.path.join(filePath,fileName)
            img = cv2.imread(image_path)
            height, width, _ = img.shape

            adj_LL, adj_UR = rectangle_coords
            
            reader = PdfReader(pdf_path)
            page = reader.pages[0]
            page.mediabox.lower_left = adj_LL
            page.mediabox.upper_right = adj_UR

            exportFileName = os.path.join(filePath,splittedDirName,fileName.replace('.pdf','')+'_'+i+'.pdf')
            exportFileNameForLoging = fileName.replace('.pdf','')+'_'+i+'_.pdf'
            with open(exportFileName,'wb') as fp:
                writer = PdfWriter()
                writer.add_page(page)
                writer.write(fp)
            
            splittedPDFLog.append(fileName.replace('.pdf','')+'_'+i+'.pdf')
        except OSError as e:
            print('error')
    return [splittedPDFLog]

# Transform splitted PDF to Image PNG
def splittedPDFtoImage(filePath,splittedDirName,splittedImgDirName,logExportFilePDF):
    xinPath = os.path.join(filePath,splittedDirName)
    xotPath = os.path.join(filePath,splittedImgDirName)
    splittedPicLog = []
    for i in logExportFilePDF[0]:
        exportFile_sts,exportFileName = pdfToImage(xinPath, i, xotPath)
        splittedPicLog.append(exportFileName[0])
    return splittedPicLog