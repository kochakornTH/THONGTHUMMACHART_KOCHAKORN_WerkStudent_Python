import os 
import sys


from pdfManipulation import  pdfFileList, _mkdir, pdfFileReadChecking, measurePDFSize , pdfToImage , transformGrayScale 

def _mainpdfToGrayPNG(filePath,folderName):
    try:
        
        inputDirName = folderName
        outputDirName = inputDirName+'_Lebeling'
        controlDirName = inputDirName+'_Control'
        
        outputDirNamePath = os.path.join(filePath, outputDirName)
        controlDirNamePath = os.path.join(outputDirNamePath, controlDirName)
        pictureDirName = os.path.join(outputDirNamePath,  outputDirName+'_picture')
        grayScaleDirName = os.path.join(outputDirNamePath, outputDirName+'_gray')
        
        mkdir_output_sts = _mkdir(outputDirNamePath)
        mkdir_contrl_sts = _mkdir(controlDirNamePath)
        mkdir_pic_sts = _mkdir(pictureDirName)
        mkdir_gry_sts = _mkdir(grayScaleDirName)
        
        BatchDir, fileDF = pdfFileList(os.path.join(filePath,inputDirName))
        print('fileDF',fileDF.T)
        fileDF['outputDirName'] = outputDirName
        fileDF['pictureDirName'] = pictureDirName
        fileDF['grayScaleDirName'] = grayScaleDirName
        fileDF['readStatus'] = fileDF.apply(lambda row: pdfFileReadChecking(row['filePath'], row['fileName'], row['fileType']), axis=1)
        readablePDFFile = fileDF[fileDF.readStatus == '00 - Readable PDF']
        readablePDFFile[['pdfMeasure_sts', 'pdf_x_size','pdf_y_size','numPage']] = readablePDFFile.apply(lambda row: measurePDFSize(row['filePath'], row['fileName']), axis='columns', result_type='expand')
        readablePDFFile[['pdftoImage_sts', 'imgName']] = readablePDFFile.apply(lambda row: pdfToImage(row['filePath'], row['fileName'], row['pictureDirName']), axis='columns', result_type='expand')
        readablePDFFile[['grayTransfrom_sts', 'grayImageName']] = readablePDFFile.apply(lambda row: transformGrayScale(row['imgName'], row['grayScaleDirName'],row['pictureDirName']), axis='columns', result_type='expand')
        fileDF.to_json(os.path.join(controlDirNamePath,'Batch_'+folderName+'_Overall.json'), orient='records', lines=True)
        readablePDFFile.to_json(os.path.join(controlDirNamePath,'Batch_'+folderName+'_PDF.json'), orient='records', lines=True)
        return '00 - Able to Transform to GrayScale' 
    except OSError as e:
        return '01 - Unable to Transform to GrayScale'
    

if __name__== "__main__":
    filePath   = sys.argv[1]
    folderName = sys.argv[2]
    result = _mainpdfToGrayPNG(filePath,folderName)
    print(result)