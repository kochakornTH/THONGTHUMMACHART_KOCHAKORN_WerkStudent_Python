import os
import sys

import json
import pandas as pd

from cleanInfo import  dateFormatAdj, defineDateMonthFormat, find_m_match, create_date_from_string , clean_text , find_currency_match , clean_AMT , clean_date_string , currencySigntoCode, invoiceAMTConvert
from directoryManagement import _mkdir,_rmdir,pdfFileList
from extractInfo import  extractInvNo,  extractText, findCompanyFn,  extractValuefromDict, extractCompanyName
from ocr import  ocrFieldInfoValues
from pdfManagement import measurePDFSize, pdfToImage,adjCoordiateforPDF,PNGtoSplit,splittedPDFtoImage
from statusControl import  pdfFileReadChecking, _checkNumericalField, _updateFirstValidation, _checkSecondValidation, _updateSecondValidation, summaryFileStatus


def _exportResult(Result_main_df, sts_main_df, outputDir):
    try: 
        batchName = sts_main_df.batchName[0]
        filesSummary = sts_main_df[['fileName','overall_status']].rename(columns={'fileName': 'File_Name','overall_status': 'File_Status'})
    
        df_result = Result_main_df[['fileName','result_InvoiceDTX','result_InvoiceAMT_EUR']]
        df_result= df_result.rename(columns={'fileName': 'fileName','result_InvoiceDTX': 'Invoice_Date','result_InvoiceAMT_EUR': 'Total_Amount_EUR'})
        
        pivot = df_result.pivot_table(index =['Invoice_Date','fileName'],
                               values =['Total_Amount_EUR'],
                               aggfunc ='sum')
        
        excelOutputFileName  = 'BatchSummary_'+batchName+'.xlsx'
        excelOutputDirectory = os.path.join(outputDir,excelOutputFileName)


        csvOutputFileName = 'BatchSummary_'+batchName+'.csv'
        csvOutputDirectory = os.path.join(outputDir,csvOutputFileName)
        df_result.to_csv(csvOutputDirectory,sep=';', index=False)
        
        
        with pd.ExcelWriter(excelOutputDirectory) as writer:
            # use to_excel function and specify the sheet_name and index 
            # to store the dataframe in specified sheet
            df_result.to_excel(writer, sheet_name="sheet1", index=False)
            pivot.to_excel(writer, sheet_name="sheet2", index=True)
            filesSummary.to_excel(writer, sheet_name="fileStatusSummary", index=False)
        print('Exported Summary file Successful! : '+excelOutputFileName)
    except (IndexError, KeyError):
    # Handle potential errors (e.g., invalid date format)
        print('Error, ',IndexError, KeyError)

def _mainExtractValfromPDF(filePath,_mainPath,folderName):
    inputDirName = folderName
    impageDirName = inputDirName+'_PNG'
    splittedDirName = inputDirName+'_Splitted'
    splittedImgDirName = inputDirName+'_SplittedImg'
    
    df_RUL = pd.read_json(os.path.join(_mainPath,'File_x_Company_CheckingRules.json') , lines=True)
    companyList = list(df_RUL['companyName'])
    
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
    with open(os.path.join(_mainPath,'CurrencyRate.json')) as f:
        CurrencyRate = json.load(f)
    
    
    BatchDir, main_df = pdfFileList(filePath,folderName)
    main_df['readStatus'] = main_df.apply(lambda row: pdfFileReadChecking(row['filePath'], row['fileName'], row['fileType']), axis=1)
    main_df[['CompanyStatus','companyName']] = main_df.apply(lambda row: findCompanyFn(row['readStatus'], row['filePath'], row['fileName'],companyList), axis=1)

    pdf_main_df = main_df[main_df['CompanyStatus'] == '01 - Can find company name'].reset_index()
    pdf_main_df[['pdfMeasure_sts', 'pdf_x_size','pdf_y_size','numPage']] = pdf_main_df.apply(lambda row: measurePDFSize(row['filePath'], row['fileName']), axis='columns', result_type='expand')
    
    pdf_main_df_merged = pd.merge(pdf_main_df,df_RUL, on='companyName', how='left')
    
    # First Validation
    pdf_main_df_merged[['pdf_x_size_sts','pdf_y_size_sts','numPage_sts']] = pdf_main_df_merged.apply(lambda row: _checkNumericalField(row['pdf_x_size_x'], row['pdf_x_size_y'], row['pdf_y_size_x'], row['pdf_y_size_y'], row['numPage_x'], row['numPage_y']), axis='columns', result_type='expand')
    pdf_main_df_merged['firstValidate_sts'] = pdf_main_df_merged.apply(lambda row: _updateFirstValidation(row['pdf_x_size_sts'],row['pdf_y_size_sts'],row['numPage_sts']),axis=1)
    
    # Define '01 - Pass 1st Validation' df
    Extractpdf_main_df = pdf_main_df_merged[pdf_main_df_merged['firstValidate_sts'] == '01 - Pass 1st Validation'].reset_index()
    Extractpdf_main_df['batchCD'] = folderName
    
    _mkdir(os.path.join(filePath,folderName,impageDirName))
    _mkdir(os.path.join(filePath,folderName,splittedDirName))
    _mkdir(os.path.join(filePath,folderName,splittedImgDirName))
    
    # PDF to PNG
    Extractpdf_main_df['logExportFileSplittedImgx'] = Extractpdf_main_df.apply(lambda row: pdfToImage(row['filePath'],row['fileName'],os.path.join(filePath,folderName,impageDirName)),axis=1)
    
    # Split PDF to small PDF
    Extractpdf_main_df['logExportFilePDF'] = Extractpdf_main_df.apply(lambda row: PNGtoSplit(row['filePath'],row['fileName'],row['result_fieldCoordinate'],row['logExportFileSplittedImgx'],row['pdf_x_size_x'],row['pdf_y_size_x'],impageDirName,splittedDirName),axis=1)
    
    # Turn small PDF to PNG
    Extractpdf_main_df['logExportFileSplittedImg'] = Extractpdf_main_df.apply(lambda row: splittedPDFtoImage(row['filePath'],splittedDirName,splittedImgDirName,row['logExportFilePDF']),axis=1)
    
    # OCR PNG
    Extractpdf_main_df['FieldInfoValues'] = Extractpdf_main_df.apply(lambda row: ocrFieldInfoValues(row['logExportFileSplittedImg'],row['filePath'],row['fileName'],splittedImgDirName),axis=1)
    
    # Extract 2nd Validation Info
    Extractpdf_main_df['field_companyAdress_x'] = Extractpdf_main_df.apply(lambda row: extractValuefromDict(row['FieldInfoValues'],'companyAdress'),axis=1)
    Extractpdf_main_df['field_TableLeft_x'] = Extractpdf_main_df.apply(lambda row: extractValuefromDict(row['FieldInfoValues'],'TableLeft'),axis=1)
    Extractpdf_main_df['field_topVerify_x'] = Extractpdf_main_df.apply(lambda row: extractValuefromDict(row['FieldInfoValues'],'topVerify'),axis=1)
    Extractpdf_main_df['field_botVerify_x'] = Extractpdf_main_df.apply(lambda row: extractValuefromDict(row['FieldInfoValues'],'botVerify'),axis=1)
    
    # Second Validation
    Extractpdf_main_df[['TableLeft_sts','topVerify_sts','botVerify_sts','companyAdress_sts']] = Extractpdf_main_df.apply(lambda row: _checkSecondValidation(row['field_TableLeft'],row['field_TableLeft_x']  ,row['field_topVerify'],row['field_topVerify_x']  ,row['field_botVerify'],row['field_botVerify_x'] ,row['companyAdress'],row['field_companyAdress_x']), axis='columns', result_type='expand')
    Extractpdf_main_df['secondValidate_sts'] = Extractpdf_main_df.apply(lambda row: _updateSecondValidation(row['TableLeft_sts'],row['topVerify_sts'],row['botVerify_sts'],row['companyAdress_sts']),axis=1)
    
    # Define '01 - Pass 2st Validation' df
    Final_main_df = Extractpdf_main_df[Extractpdf_main_df.secondValidate_sts == '01 - Pass 2nd Validation']
    Final_main_df['_jsonDateMatching'] = Final_main_df.apply(lambda row: dateFormatAdj(row['companyCD'],ReciptDateFormat),axis=1)
    
    # Extract Necessary Info
    Final_main_df['result_CompanyName'] = Final_main_df.apply(lambda row: extractCompanyName(row['FieldInfoValues'],row['companyCD'],CompanyNameFormat),axis=1)
    Final_main_df['field_InvoiceDT'] = Final_main_df.apply(lambda row: extractValuefromDict(row['FieldInfoValues'],'invoiceDate'),axis=1)
    Final_main_df['field_grossAMT'] = Final_main_df.apply(lambda row: extractValuefromDict(row['FieldInfoValues'],'grossAMT'),axis=1)
    Final_main_df['field_invoiceNumber'] = Final_main_df.apply(lambda row: extractValuefromDict(row['FieldInfoValues'],'invoiceNumber'),axis=1)
    
    Final_main_df['result_InvoiceNUM'] = Final_main_df.apply(lambda row: extractInvNo(row['field_invoiceNumber'],row['companyCD'],ReciptInvNoFormat),axis=1)
    Final_main_df['result_CurrencyX'] = Final_main_df.apply(lambda row: find_currency_match(row['field_grossAMT']),axis=1)
    Final_main_df['result_Currency'] = Final_main_df.apply(lambda row: currencySigntoCode(row['result_CurrencyX'],currencyIndexDict),axis=1)
    Final_main_df['result_InvoiceAMT'] = Final_main_df.apply(lambda row: clean_AMT(row['field_grossAMT'],row['companyCD'],ReciptAmtFormat),axis=1)
    Final_main_df['result_InvoiceDTX'] = Final_main_df.apply(lambda row: clean_date_string(row['field_InvoiceDT'],row['_jsonDateMatching'],dateMonthFormat),axis=1)
    
    
    Result_main_df = Final_main_df[['fileName','result_CompanyName','result_InvoiceNUM','result_Currency','result_InvoiceAMT','result_InvoiceDTX']]
    Result_main_df['result_InvoiceAMT_EUR'] = Result_main_df.apply(lambda row: invoiceAMTConvert(row['result_Currency'],row['result_InvoiceAMT'],CurrencyRate),axis=1)
    Result_main_df['result_InvoiceCUR_EUR'] = 'eur'
    
    sts_main_df = main_df[['fileName','readStatus']]
    sts_main_readable_df = pdf_main_df_merged[['fileName','pdfMeasure_sts','firstValidate_sts']]
    sts_main_extractd_df = Extractpdf_main_df[['fileName','secondValidate_sts']]
    
    sts_main_df = pd.merge(sts_main_df,sts_main_readable_df, on='fileName', how='left')
    sts_main_df = pd.merge(sts_main_df,sts_main_extractd_df, on='fileName', how='left')
    sts_main_df['overall_status'] = sts_main_df.apply(lambda row: summaryFileStatus(row['secondValidate_sts'],row['firstValidate_sts'],row['pdfMeasure_sts'],row['readStatus']),axis=1)
    sts_main_df = sts_main_df.sort_values(by=['overall_status','fileName'])
    sts_main_df['batchName'] = folderName

    _rmdir(os.path.join(filePath,folderName,impageDirName))
    _rmdir(os.path.join(filePath,folderName,splittedDirName))
    _rmdir(os.path.join(filePath,folderName,splittedImgDirName))
    
    return Result_main_df, sts_main_df

if __name__== "__main__":
    filePath   = sys.argv[1]
    _mainPath  = os.path.join(sys.argv[2],'_pdfOCRScript_PRD')
    folderName = sys.argv[3]
    # hello(int(sys.argv[1]), int(sys.argv[2]))
    Result_main_df, sts_main_df = _mainExtractValfromPDF(filePath,_mainPath,folderName)
    _exportResult(Result_main_df, sts_main_df, os.path.join(filePath,folderName))