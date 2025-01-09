import os


#Status
def controlFileChecking(filePath,folderName,controlDirName):
    PDFControlJSON = ''
    overallControlJSON = ''
    for i in os.listdir(os.path.join(filePath,controlDirName)):
    # for i in ['xxx']:
        if ("PDF" in i):
            PDFControlJSON = i
        elif "Overall" in i   :
            overallControlJSON = i
        elif "Rules" in i   :
            RulesJSON = i
    
    if (PDFControlJSON == '')|(overallControlJSON == ''):
        controlJSON_sts = '01 - Unable to Find JSON file'
    else:
        controlJSON_sts = '00 - Able to Find JSON file'
    
    return controlJSON_sts, PDFControlJSON, overallControlJSON
