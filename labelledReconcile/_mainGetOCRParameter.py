import os
import sys

import json
import re
from datetime import date
from datetime import datetime
import pandas as pd

from cleanInfo import dateFormatAdj,find_m_match,find_currency_match,defineDateMonthFormat,clean_text,create_date_from_string,clean_date_string,clean_AMT
from directoryManagement import _mkdir,_rmdir,pdfFileList
from extractInfo import extractValuefromDict, extractInvNo,extractCompanyName,field_X_Coordinate
from statusControl import controlFileChecking
from pdfManipulation import adjCoordiateforPDF, splitFunctionByCoor,splitByColor,findLabelledPage,pdfToImage,splittedPDFtoImage
from cvDetection import detect_rectangle
from ocr import  ocrFieldInfoValues


def prepCSVforJSONLabelling(field_InvoiceDT,field_invoiceNumber,companyAdress,field_grossAMT):
    field_InvoiceDT = field_InvoiceDT.replace('\n',' ').replace('$','$ ').replace('€','€ ').split(' ')
    field_invoiceNumber = field_invoiceNumber.replace('\n',' ').replace('$','$ ').replace('€','€ ').split(' ') 
    companyAdress = companyAdress.replace('\n',' ').replace('$','$ ').replace('€','€ ').split(' ')
    field_grossAMT = field_grossAMT.replace('\n',' ').replace('$','$ ').replace('€','€ ').split(' ')
    return field_InvoiceDT,field_invoiceNumber,companyAdress,field_grossAMT


def _mainGetOCRParameter(filePath,_mainPath,folderName):
    try: 
        inputDirName = folderName
        outputDirName = inputDirName+'_Lebelled'
        controlDirName = inputDirName+'_Control'
        labelledDirName = inputDirName+'_Lebelled'
        splittedDirName = inputDirName+'_Splitted'
        splittedImgDirName = inputDirName+'_SplittedImg'
        
        
        mkdir_splitted_sts = _mkdir(os.path.join(filePath,splittedDirName))
        mkdir_splittedImg_sts = _mkdir(os.path.join(filePath,splittedImgDirName))
        
        
        fieldList = ['invoiceNumber'
                        ,'invoiceDate'
                        ,'grossAMT'
                        ,'companyAdress'
                        ,'TableLeft'
                        ,'topVerify'
                        ,'botVerify']
        
        colorInfoDict = {'invoiceNumber' :'red' 
                       , 'invoiceDate'   :'orange'  
                       , 'grossAMT'      :'yellow' 
                       , 'companyAdress' :'green'
                       , 'TableLeft'      :'purple'
                       , 'topVerify'     :'blue'
                       , 'botVerify'     :'cyan'}
        
        FieldInfoDictCoor = {'invoiceNumber':[]
                     , 'invoiceDate':[]
                     , 'grossAMT':[]
                     , 'companyAdress':[]
                     , 'TableLeft':[]
                     , 'topVerify':[]
                     , 'botVerify':[]}
        
        # Import Control JSON
        
        with open(os.path.join(_mainPath,'dateMonthFormat.json')) as f:
            dateMonthFormat = json.load(f)
            
        with open(os.path.join(_mainPath,'ReciptDateFormat.json')) as f:
            ReciptDateFormat = json.load(f)
        with open(os.path.join(_mainPath,'ReciptAmtFormat.json')) as f:
            ReciptAmtFormat = json.load(f)
        with open(os.path.join(_mainPath,'currencyIndexDict.json')) as f:
            currencyIndexDict = json.load(f)
        with open(os.path.join(_mainPath,'ReciptInvNoFormat.json')) as f:
            ReciptInvNoFormat = json.load(f)
        with open(os.path.join(_mainPath,'CompanyNameFormat.json')) as f:
            CompanyNameFormat = json.load(f)
        
        controlJSON_sts, PDFControlJSON, overallControlJSON = controlFileChecking(filePath,folderName,controlDirName)
        df_PDF = pd.read_json(os.path.join(filePath,controlDirName,PDFControlJSON) , lines=True)
        df_ALL = pd.read_json(os.path.join(filePath,controlDirName,overallControlJSON) , lines=True)
        
        # df_RUL = pd.read_json(os.path.join(_mainPath,'File_x_Company_CheckingRules.json') , lines=True)
        
        # Read Matching JSON
        df_Matching = pd.read_json(os.path.join(_mainPath,'Batch_'+folderName+'_companyMatching.json') , lines=True)
        
        # Manage info with DataFrame
        df_PDF[['splitResult','logExportFilePDF']] = df_PDF.apply(lambda row: splitByColor(row['grayImageName'],row['filePath'], row['fileName'], filePath, labelledDirName, FieldInfoDictCoor, fieldList, colorInfoDict,row['pdf_x_size'],row['pdf_y_size'],splittedDirName), axis='columns', result_type='expand')
        df_PDF[['numLabelledPage','labelledIndexPage','CoordinateForSplitting']] = df_PDF.apply(lambda row: findLabelledPage(row['numPage'],row['splitResult']), axis='columns', result_type='expand')
        
        # Find PDF which be labelled
        labelled_df = df_PDF[df_PDF.numLabelledPage >= 1]
        
        # Export splitted PDF as PNG
        labelled_df['logExportFileSplittedImg'] = labelled_df.apply(lambda row: splittedPDFtoImage(filePath,splittedDirName,splittedImgDirName,row['logExportFilePDF']),axis=1)
        

        # OCR
        labelled_df['FieldInfoValues'] = labelled_df.apply(lambda row: ocrFieldInfoValues(row['logExportFileSplittedImg'],filePath,row['fileName'],splittedImgDirName),axis=1)
        
        labelled_df_forJoin = labelled_df[['fileName','pdf_x_size','pdf_y_size','numPage','splitResult','FieldInfoValues','labelledIndexPage','CoordinateForSplitting']]
        merged_df = pd.merge(df_Matching,labelled_df_forJoin, on='fileName', how='left')
              
        merged_df['_jsonDateMatching'] = merged_df.apply(lambda row: dateFormatAdj(row['companyCD'],ReciptDateFormat),axis=1)
        merged_df['field_InvoiceDT'] = merged_df.apply(lambda row: extractValuefromDict(row['FieldInfoValues'],'invoiceDate'),axis=1)
        merged_df['field_grossAMT'] = merged_df.apply(lambda row: extractValuefromDict(row['FieldInfoValues'],'grossAMT'),axis=1)
        merged_df['field_invoiceNumber'] = merged_df.apply(lambda row: extractValuefromDict(row['FieldInfoValues'],'invoiceNumber'),axis=1)
        
        merged_df['field_TableLeft'] = merged_df.apply(lambda row: extractValuefromDict(row['FieldInfoValues'],'TableLeft'),axis=1)
        merged_df['field_topVerify'] = merged_df.apply(lambda row: extractValuefromDict(row['FieldInfoValues'],'topVerify'),axis=1)
        merged_df['field_botVerify'] = merged_df.apply(lambda row: extractValuefromDict(row['FieldInfoValues'],'botVerify'),axis=1)
        merged_df['companyAdress'] = merged_df.apply(lambda row: extractValuefromDict(row['FieldInfoValues'],'companyAdress'),axis=1)
        
        
        merged_df['result_InvoiceDTX'] = merged_df.apply(lambda row: clean_date_string(row['field_InvoiceDT'],row['_jsonDateMatching'],dateMonthFormat),axis=1)
        merged_df['result_CompanyName'] = merged_df.apply(lambda row: extractCompanyName(row['FieldInfoValues'],row['companyCD'],CompanyNameFormat),axis=1)
        
        merged_df['result_CurrencyX'] = merged_df.apply(lambda row: find_currency_match(row['field_grossAMT']),axis=1)
        merged_df['result_InvoiceAMT'] = merged_df.apply(lambda row: clean_AMT(row['field_grossAMT'],row['companyCD'],ReciptAmtFormat),axis=1)
        merged_df['result_InvoiceNUM'] = merged_df.apply(lambda row: extractInvNo(row['field_invoiceNumber'],row['companyCD'],ReciptInvNoFormat),axis=1)
        
        ruleCheck_df = merged_df[['companyCD','companyName','pdf_x_size','pdf_y_size','numPage','splitResult','labelledIndexPage','CoordinateForSplitting','field_TableLeft','field_topVerify','field_botVerify','companyAdress']]
        ruleCheck_df['result_fieldCoordinate'] = ruleCheck_df.apply(lambda row: field_X_Coordinate(row['CoordinateForSplitting']),axis=1)
        ruleCheck_df['rec_eff_dttm'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ruleCheck_df['rec_end_dttm'] = datetime(9999, 12, 31, 12, 0, 0).strftime("%Y-%m-%d %H:%M:%S")
        ruleCheck_df.to_json(os.path.join(_mainPath,folderName+'_CheckingRules.json'), orient='records', lines=True)

        merged_df[['listForRecieptDT','listForRecieptNo', 'listForCompanyName', 'listForAMT']] = merged_df.apply(lambda row: prepCSVforJSONLabelling(row['field_InvoiceDT'],row['field_invoiceNumber'],row['companyAdress'],row['field_grossAMT']), axis='columns', result_type='expand')

        merged_df[['companyCD','listForRecieptDT']].to_json(os.path.join(_mainPath,folderName+'_listForRecieptDT.json'), orient='records', lines=True)
        merged_df[['companyCD','listForRecieptNo']].to_json(os.path.join(_mainPath,folderName+'_listForRecieptNo.json'), orient='records', lines=True)
        merged_df[['companyCD','listForCompanyName']].to_json(os.path.join(_mainPath,folderName+'_listForCompanyName.json'), orient='records', lines=True)
        merged_df[['companyCD','listForAMT']].to_json(os.path.join(_mainPath,folderName+'_listForAMT.json'), orient='records', lines=True)

        print('Please find the Current OCR rules at '+ str(os.path.join(_mainPath,'Batch_'+folderName)))

        _rmdir(os.path.join(filePath,splittedDirName))
        _rmdir(os.path.join(filePath,splittedImgDirName))
        return  ruleCheck_df
    except (IndexError, KeyError):
        return print('Error')


if __name__== "__main__":
    filePath   = sys.argv[1]
    _mainPath  = sys.argv[2]
    folderName = sys.argv[3]
    ruleCheck_df = _mainGetOCRParameter(filePath,_mainPath,folderName)
