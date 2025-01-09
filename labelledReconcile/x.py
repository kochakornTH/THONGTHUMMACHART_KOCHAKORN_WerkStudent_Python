# def _mkdir(directory_name):
#     try:
#         shutil.rmtree(directory_name)  # Remove directory and its contents
#         try:
#             os.mkdir(directory_name)
#             return '00 - Able to Create Directory'
#         except OSError as e:
#             return '01 - Unable to Create Directory'
#     except OSError as e:
#         try:
#             os.mkdir(directory_name)
#             return '00 - Able to Create Directory'
#         except OSError as e:
#             return '01 - Unable to Create Directory'




# #Status
# def controlFileChecking(filePath,folderName,controlDirName):
#     PDFControlJSON = ''
#     overallControlJSON = ''
#     for i in os.listdir(os.path.join(filePath,controlDirName)):
#     # for i in ['xxx']:
#         if ("PDF" in i):
#             PDFControlJSON = i
#         elif "Overall" in i   :
#             overallControlJSON = i
#         elif "Rules" in i   :
#             RulesJSON = i
    
#     if (PDFControlJSON == '')|(overallControlJSON == ''):
#         controlJSON_sts = '01 - Unable to Find JSON file'
#     else:
#         controlJSON_sts = '00 - Able to Find JSON file'
    
#     return controlJSON_sts, PDFControlJSON, overallControlJSON

# # Detection
# def detect_rectangle(image_path, color):
#     """
#     Detects the boundaries of a rectangle of a given color in an image.

#     Args:
#         image_path: Path to the image file.
#         color: Color to detect ('red', 'blue', 'green', 'yellow', 'purple')

#     Returns:
#         A tuple containing the coordinates of the top-left corner (x1, y1) 
#         and the bottom-right corner (x2, y2) of the rectangle, 
#         or None if no rectangle of the specified color is found.
#     """

#     # Load the image
#     img = cv2.imread(image_path)

#     # Check if image was loaded successfully
#     if img is None:
#         print(f"Error: Could not load image from {image_path}")
#         return None

#     # Convert to HSV color space
#     hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#     # Define color bounds in HSV
#     if color == 'red':
#         lower = np.array([0, 50, 50])
#         upper = np.array([10, 255, 255])
#         lower2 = np.array([170, 50, 50])
#         upper2 = np.array([180, 255, 255])
#     elif color == 'blue':
#         lower = np.array([90, 50, 50])
#         upper = np.array([130, 255, 255])
#     elif color == 'orange':
#         lower = np.array([10, 50, 50])  
#         upper = np.array([25, 255, 255])
#     elif color == 'cyan':
#         lower = np.array([80, 50, 50])
#         upper = np.array([100, 255, 255])
#     elif color == 'green':
#         lower = np.array([40, 50, 50])
#         upper = np.array([80, 255, 255])
#     elif color == 'purple':
#         lower = np.array([130, 50, 50])
#         upper = np.array([160, 255, 255])
#     elif color == 'yellow':
#         lower = np.array([20, 50, 50])
#         upper = np.array([40, 255, 255])
#     elif color == 'brown':
#         lower = np.array([10, 50, 50]) 
#         upper = np.array([30, 255, 150]) 
#     else:
#         print(f"Invalid color: {color}. Supported colors: 'red', 'blue', 'green', 'yellow', 'purple','orange','cyan','pink'")
#         return None

#     # Create a mask for the specified color
#     if color == 'red':
#         mask1 = cv2.inRange(hsv, lower, upper)
#         mask2 = cv2.inRange(hsv, lower2, upper2)
#         mask = cv2.bitwise_or(mask1, mask2)
#     else:
#         mask = cv2.inRange(hsv, lower, upper)

#     # Find contours in the masked image
#     contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     # Find the contour with the most area (assuming it's the rectangle)
#     if len(contours) > 0:
#         largest_contour = max(contours, key=cv2.contourArea)

#         # Find the bounding rectangle of the contour
#         x, y, w, h = cv2.boundingRect(largest_contour)

#         # Calculate coordinates of top-left and bottom-right corners
#         x1, y1 = x, y
#         x2, y2 = x + w, y + h

#         # Get image dimensions
#         height, width, _ = img.shape

#         return (x1, y1), (x2, y2), (0, 0), (width, height) 

#     else:
#         return None

# pdfManipulate
# def adjCoordiateforPDF(rectangle_coords,pdf_x_size,pdf_y_size):
#     areaTopL = rectangle_coords[0]
#     areaBotR = rectangle_coords[1]
#     min_origin = rectangle_coords[2]
#     max_origin = rectangle_coords[3]
    
#     LL = rectangle_coords[0][0],rectangle_coords[1][1]
#     UR = rectangle_coords[1][0],rectangle_coords[0][1]
#     MAX_X = rectangle_coords[3][0]
#     MAX_Y = rectangle_coords[3][1]
#     LL_inv = rectangle_coords[0][0],MAX_Y - rectangle_coords[1][1]
#     UR_inv = rectangle_coords[1][0],MAX_Y - rectangle_coords[0][1]
#     x_prf_ratio = (pdf_x_size/MAX_X)
#     y_prf_ratio = (pdf_y_size/MAX_Y)
#     # ___
#     adj_LL = float(LL_inv[0]*x_prf_ratio),float(LL_inv[1]*y_prf_ratio)
#     adj_UR = float(UR_inv[0]*x_prf_ratio),float(UR_inv[1]*y_prf_ratio)

#     return adj_LL, adj_UR

# def splitFunctionByCoor(FieldInfoDictCoor,fieldList,colorInfoDict,image_path,labelledFileName,pdf_x_size,pdf_y_size,BatchName,fileName,splittedDirName):
#     logExportFile = []
#     for i in fieldList:
#         color_to_detect = colorInfoDict[i]
#         rectangle_coords = detect_rectangle(image_path, color_to_detect) 
#         print('rectangle_coords',rectangle_coords)
#         if rectangle_coords:  # Check if rectangle was actually detected
#             adj_LL, adj_UR = adjCoordiateforPDF(rectangle_coords,pdf_x_size,pdf_y_size)
#             fileName_DirPDF = os.path.join(filePath,BatchName ,fileName )
#             reader = PdfReader(fileName_DirPDF)
#             page = reader.pages[0]
#             page.mediabox.lower_left = adj_LL
#             page.mediabox.upper_right = adj_UR

#             exportFileName = os.path.join(filePath,splittedDirName,fileName.replace('.pdf','')+'_'+i+'_.pdf')
#             exportFileNameForLoging = fileName.replace('.pdf','')+'_'+i+'_.pdf'
#             with open(exportFileName,'wb') as fp:
#                 writer = PdfWriter()
#                 writer.add_page(page)
#                 writer.write(fp)
#             FieldInfoDictCoor[i] = [adj_LL, adj_UR]
#             logExportFile.append(exportFileNameForLoging)
#         else:
#             1== 1
#             FieldInfoDictCoor[i] = []
#     outputdict = {'labelledFileName':[labelledFileName],'FieldInfoDictCoor':[FieldInfoDictCoor]}
#     return outputdict, logExportFile

# def splitByColor(pdfBucket,BatchName,fileName,filePath,labelledDirName,FieldInfoDictCoor,fieldList,colorInfoDict,pdf_x_size,pdf_y_size,splittedDirName):
#     results = []
#     logExportFilePDF = []
#     for k in pdfBucket:
#         image_path = os.path.join(filePath,labelledDirName,k)
#         outputdict, logExportFile = splitFunctionByCoor(FieldInfoDictCoor,fieldList,colorInfoDict,image_path,k,pdf_x_size,pdf_y_size,BatchName,fileName,splittedDirName)
#         results.append(str(outputdict))
#         logExportFilePDF.append(logExportFile)
#     return results,logExportFilePDF

# def findLabelledPage(numPage,splitResult):
#     labelledPage = 0
#     labelledIndexPage = []
#     xDict = dict()
#     for i in range(0,numPage):
#         x = splitResult[i]
#         y = ast.literal_eval(x)
#         labelsFileName = y['labelledFileName']
#         labelsCoordinate = y['FieldInfoDictCoor'][0]

#         xDict['page_'+str(i)] = labelsCoordinate
        
#         if len(labelsCoordinate['invoiceNumber']) == 0 :
#             labelledPage = labelledPage + 0
#         else:
#             labelledPage = labelledPage + 1    
#             labelledIndexPage.append(i)
#     return labelledPage, labelledIndexPage,xDict

# def pdfToImage(filePath, fileName, outputPath):
#     XBatchDir = os.path.join(filePath,fileName)
#     exportDir = outputPath
#     try:
#         images = pdf2image.convert_from_path(XBatchDir)
#         imgName = fileName[:-4]
#         kxk = []
#         for i in range(len(images)):
#             imageNameX = imgName+'_'+str(i+1)+"_image.png"
#             images[i].save(os.path.join(exportDir,imageNameX), 'PNG')            
#             kxk.append(imageNameX)
#         return '00 - Transformable to Image', kxk
#     except OSError as e:
#         return '01 - Untransformable to Image', []

# def splittedPDFtoImage(filePath,splittedDirName,splittedImgDirName,logExportFilePDF):
#     xinPath = os.path.join(filePath,splittedDirName)
#     xotPath = os.path.join(filePath,splittedImgDirName)
    
#     splittedPicLog = []
#     for i in logExportFilePDF[0]:
#         print('logExportFilePDF',i)
#         exportFile_sts,exportFileName = pdfToImage(xinPath, i, xotPath)
#         splittedPicLog.append(exportFileName[0])
#     return splittedPicLog

# OCRx
# def ocrFieldInfoValues(logExportFileSplittedImg,filePath,fileName,splittedImgDirName):
    xotPath= os.path.join(filePath,splittedImgDirName)
    splittedImgFileDir = logExportFileSplittedImg
    FieldInfoValues = {'invoiceNumber':[]
             , 'invoiceDate':[]
             , 'grossAMT':[]
             , 'companyAdress':[]
             , 'TableLeft':[]
             # , 'TableRight':[]
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
        # elif ("TableRight" in i) & (fileNamex in i): 
        #     FieldInfoValues['TableRight'] = pytesseract.image_to_string(Image.open(os.path.join(xotPath, i)))
        elif ("companyAdress" in i) & (fileNamex in i): 
            FieldInfoValues['companyAdress'] = pytesseract.image_to_string(Image.open(os.path.join(xotPath, i)))
        elif ("topVerify" in i) & (fileNamex in i): 
            FieldInfoValues['topVerify'] = pytesseract.image_to_string(Image.open(os.path.join(xotPath, i)))
        elif("botVerify" in i) & (fileNamex in i): 
            FieldInfoValues['botVerify'] = pytesseract.image_to_string(Image.open(os.path.join(xotPath, i)))
        else:
            1==1
    return FieldInfoValues


# #Cleaning
# def dateFormatAdj(companyCD,ReciptDateFormat):
#     dateAdjInfo = ReciptDateFormat[companyCD]
#     return dateAdjInfo

# def find_m_match(target_list):
#   """
#   Finds the first occurrence of any element from the search_list in the target_list.

#   Args:
#     search_list: A list of strings to search for.
#     target_list: A list of strings to search within.

#   Returns:
#     The first matching element from the search_list, or None if no match is found.
#   """
#   search_list = ['M', 'MM', 'MMM', 'MMMM']
#   for item in search_list:
#     if item in target_list:
#       return item
#   return None

# def find_currency_match(target_list):
#   """
#   Finds the first occurrence of any element from the search_list in the target_list.

#   Args:
#     search_list: A list of strings to search for.
#     target_list: A list of strings to search within.

#   Returns:
#     The first matching element from the search_list, or None if no match is found.
#   """
#   search_list = ['€', '$']
#   for item in search_list:
#     if item in target_list:
#       return item
#   return None
    
# def defineDateMonthFormat(dateTypeX,dateLangX):
#     dateTypeX_List = dateTypeX.split("-")   
#     monthindex = find_m_match(dateTypeX_List)
#     dateFormat = monthindex+'_'+dateLangX+'_DT'
#     return dateFormat

# def clean_text(text):
#     """
#     Cleans the given text by removing newlines and extra spaces.

#     Args:
#         text: The input text string.

#     Returns:
#         The cleaned text string.
#     """
#     text = text.strip()  # Remove leading/trailing whitespace
#     text = re.sub(r'\n+', ' ', text)  # Replace multiple newlines with a single space
#     text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
#     text = re.sub(r'\.', '', text)  # Remove full stops (periods)
#     text = re.sub(r'\,', '', text)  # Remove full stops (periods)

#     return text

# def create_date_from_string(year, month, day):
#   """
#   Creates a datetime.date object from given year, month, and day strings.

#   Args:
#     year: String representing the year.
#     month: String representing the month.
#     day: String representing the day.

#   Returns:
#     A datetime.date object if the input is valid, otherwise None.
#   """
#   try:
#     year = int(year)
#     month = int(month)
#     day = int(day)
#     return date(year, month, day)
#   except ValueError:
#     return None

# def clean_date_string(field_InvoiceDT,_jsonDateMatching,dateMonthFormat):
#   """
#   Cleans the given date string and converts it to the format "YYYY-MM-DD".

#   Args:
#     date_string: The input date string.

#   Returns:
#     The cleaned date string in the format "YYYY-MM-DD".
#   """
#   try:
#     # Split the date string by spaces
#     dateType = _jsonDateMatching['dateType']
#     dateLang = _jsonDateMatching['dateLang']
#     datePosition =  _jsonDateMatching['datePosition']

#     monthFormat = defineDateMonthFormat(dateType,dateLang)

#     DD_Position = datePosition['DD']
#     MM_Position = datePosition['MM']
#     YY_Position = datePosition['YY']
    
#     parts = field_InvoiceDT.strip().split()

#     # Extract month and year
#     day_str = clean_text(parts[DD_Position].strip())
#     month_str = parts[MM_Position].strip()
#     year_str = parts[YY_Position].strip()
      
#     # Convert month to numeric representation
#     months = dateMonthFormat[monthFormat]
#     month = months.get(month_str, "00")  # Default to "00" if month is not found
#     return create_date_from_string(year_str, month, day_str)
#   except (IndexError, KeyError):
#     # Handle potential errors (e.g., invalid date format)
#     return None

# def clean_AMT(field_grossAMT,companyCD,ReciptAmtFormat):
#     x = field_grossAMT
#     x = re.sub(r'\n+', ' ', x)  # Replace multiple newlines with a single space
#     x = re.sub(r'\s+', ' ', x)  # Replace multiple spaces with a single space
#     xList = x.split(' ')
    
#     result = []
#     for i in xList:
#         for j in re.split(r'(\$|€+)',i):
#             result.append(j)
    
#     AMTPosition = ReciptAmtFormat[companyCD]['AMTPosition']
#     CURPosition = ReciptAmtFormat[companyCD]['CURPosition']
    
#     resultAMT = result[AMTPosition]
#     resultCUR = result[CURPosition]
    
#     if resultCUR == '$':
#         k = resultAMT.split('.')
#         decimal = k[1]
#         nonDecimal = k[0]
#         nonDecimal = re.sub(r'\,', '', nonDecimal)  # Remove full stops (periods)
        
#         resultAMT = float(nonDecimal+'.'+str(decimal))
        
#     elif resultCUR == '€':
#         k = resultAMT.split(',')
#         decimal = k[1]
#         nonDecimal = k[0]
#         nonDecimal = re.sub(r'\.', '', nonDecimal)  # Remove full stops (periods)
    
#         resultAMT = float(nonDecimal+'.'+str(decimal))
#     else:
#         resultAMT = 0
    
#     return resultAMT


# Extract
# def extractValuefromDict(FieldInfoValues,fieldDictName):
#     result = FieldInfoValues[fieldDictName]
#     return result

# def extractInvNo(field_invoiceNumber,companyCD,ReciptInvNoFormat):
#     listText = clean_text(field_invoiceNumber).split()
#     invposition = ReciptInvNoFormat[companyCD]['InvNoPosition']
#     result_invNo = listText[invposition]
#     return result_invNo

# def extractCompanyName(FieldInfoValues,companyCD,CompanyNameFormat):
#     companySplitList = clean_text(FieldInfoValues['companyAdress']).split()
#     companyPOSList =  CompanyNameFormat[companyCD]['CompanyNamePosition']
    
#     resultCompanyName = ''
#     for i in companyPOSList:
#         resultCompanyName = resultCompanyName + ' ' + companySplitList[i]
#     resultCompanyName = resultCompanyName[1:]
#     return resultCompanyName

# def field_X_Coordinate(CoordinateForSplitting,):    
#     Dict_Field_x_Coor = {'invoiceNumber':dict()
#                      , 'invoiceDate':dict()
#                      , 'grossAMT':dict()
#                      , 'companyAdress':dict()
#                      , 'TableLeft':dict()
#                      # , 'TableRight':dict()
#                      , 'topVerify':dict()
#                      , 'botVerify':dict()}
#     xList = list(CoordinateForSplitting)
#     fieldList = list(Dict_Field_x_Coor)
#     for i in xList:
#         for j in fieldList:
#             if len(CoordinateForSplitting[i][j]) == 2:
#                 Dict_Field_x_Coor[j]['pages'] = i
#                 Dict_Field_x_Coor[j]['coordinate'] = CoordinateForSplitting[i][j]
                

#     return Dict_Field_x_Coor