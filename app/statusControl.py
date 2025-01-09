import os
from extractInfo import extractText

# Checking readable status of PDF
def pdfFileReadChecking(filePath, fileName,fileType):
    fileName_Dir = os.path.join(filePath, fileName)
    if fileType == (".pdf"):
        try:
            extractText(filePath,fileName, 0 )
            return "Readable"
        except Exception as e:
            return str(e)  # Return the error message as a string
    else:
        return "Not PDF"

# First Vaidation : Checking PDF size and num of Page of PDF
def _checkNumericalField(pdf_x_size_x,pdf_x_size_y,pdf_y_size_x,pdf_y_size_y,numPage_x,numPage_y):
    if  float(pdf_x_size_x) == float(pdf_x_size_y) :
        pdf_x_size_sts = '01 - Pass'
    else:
        pdf_x_size_sts = '02 - Not Pass'
    if  float(pdf_y_size_x) == float(pdf_y_size_y) :
        pdf_y_size_sts = '01 - Pass'
    else:
        pdf_y_size_sts = '02 - Not Pass'
    if  float(numPage_x) == float(numPage_y) :
        numPage_sts = '01 - Pass'
    else:
        numPage_sts = '02 - Not Pass'
    return pdf_x_size_sts,pdf_y_size_sts,numPage_sts

# Update first validation to main dataframe
def _updateFirstValidation(pdf_x_size_sts,pdf_y_size_sts,numPage_sts):
    if (pdf_x_size_sts == '01 - Pass') & (pdf_y_size_sts == '01 - Pass') & (numPage_sts == '01 - Pass'):
        return '01 - Pass 1st Validation'
    else:
        return '02 - Not Pass 1st Validation - error in PDF Size'

# Second Validation : Checking Point that can make sure template matching between PDF file and previous parameter
def _checkSecondValidation(field_TableLeft,field_TableLeft_x  ,field_topVerify,field_topVerify_x  ,field_botVerify,field_botVerify_x ,companyAdress,field_companyAdress_x):
    if  str(field_TableLeft) == str(field_TableLeft_x) :
        TableLeft_sts = '01 - Pass'
    else:
        TableLeft_sts = '02 - Not Pass'
        
    if  str(field_topVerify) == str(field_topVerify_x) :
        topVerify_sts = '01 - Pass'
    else:
        topVerify_sts = '02 - Not Pass'
        
    if  str(field_botVerify) == str(field_botVerify_x) :
        botVerify_sts = '01 - Pass'
    else:
        botVerify_sts = '02 - Not Pass'
        
    if  str(companyAdress) == str(field_companyAdress_x) :
        companyAdress_sts = '01 - Pass'
    else:
        companyAdress_sts = '02 - Not Pass'
        
    return TableLeft_sts,topVerify_sts,botVerify_sts,companyAdress_sts

# Update Second validation to main dataframe
def _updateSecondValidation(TableLeft_sts,topVerify_sts,botVerify_sts,companyAdress_sts):
    if (TableLeft_sts == '01 - Pass') & (topVerify_sts == '01 - Pass') & (botVerify_sts == '01 - Pass') & (companyAdress_sts == '01 - Pass'):
        return '01 - Pass 2nd Validation'
    else:
        return '02 - Not Pass 2nd Validation - Dont Match Key Value'

# Summary Batch status 
def summaryFileStatus(secondValidate_sts,firstValidate_sts,pdfMeasure_sts,readStatus):
    if secondValidate_sts == '01 - Pass 2nd Validation':
        overall_status = '01 - Valid'
    elif (pdfMeasure_sts == '00 - Able to Measure PDF') & (firstValidate_sts == '02 - Not Pass 1st Validation - error in PDF Size') :
        overall_status = '02 - PDF error'
    elif (pdfMeasure_sts == '01 - Unable to Measure PDF'):
        overall_status = '02 - PDF error'
    elif (pdfMeasure_sts == '01 - Unable to Measure PDF') & (readStatus == 'Readable'):
        overall_status = '02 - PDF error'
    else:
        overall_status = '03 - Not PDF'
    return overall_status