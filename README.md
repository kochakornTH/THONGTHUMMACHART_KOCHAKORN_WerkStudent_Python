# PDF Information Extraction 
## 00. Case Limitation, Scope and Solution Selection
### Case Limitation
Due to the small number of sample files, the developer assumes the following possible cases:
1. Encountering both image-based and text-based PDF files.
2. The target folder may contain non-PDF files. 
3. Some PDFs might be password-protected.
4. Some PDFs may be cropped by programs (like PyPDF2 in Python). While the displayed PDF appears cropped, the underlying information might be complete. (Reference: [https://stackoverflow.com/questions/72804653/cropped-pdf-still-contains-the-original-text](https://stackoverflow.com/questions/72804653/cropped-pdf-still-contains-the-original-text))
5. Some invoices may come from the same company but have variations in their templates.

### Solution Scope
1. Only text-based PDF files are eligible to be processed. (OCR for entire pages on image-based PDFs is not ideal.) 
2. Before processing, all PDFs need to be labeled (see 'Labelling Preparation') and their necessary parameters logged in JSON (see 'Labelled Reconcile'). 
3.  To minimize risks during information extraction, two validation steps are implemented. Any PDF template must pass these two validation rules before information extraction:
	1. First Validation: The PDF must have the same page number and size as specified in the corresponding JSON file.
	2. Second Validation: After extracting information by OCR, the program will match necessary fields with the information logged in the corresponding JSON file (see 'Labelling Preparation' for details on necessary fields).

### Solution Selection
1. Extract simple text from the PDF to find the company name.
2. Use the company name to select the corresponding JSON file containing crop coordinates for OCR and interpretation parameters.
3. Perform the two-step validation. 
4. Crop the PDF into small PNG files for specific needed fields and extract information from the images.
	1. Invoice Date 
	2. Invoice Amount
	3. Invoice Number
	4. Company Name
5. Return Excel and CSV files.


## 01. Information Extraction Program Overview

### <ins>Prerequisites</ins> (* Installation Guide Below)
1. poppler
3. tesseract
3. Python 3.11.7
4. Necessary Python packages in 'requirements.txt'

 
### <ins>Program Info</ins> 

#### <ins>Input</ins>
1. Working space PATH which is a directory that contains 'Production Batch Folder'. 
    - 'Production Batch Folder' is the folder that contain PDF files.
2. PATH of 'Production Paremeter Directory'.
    - 'Production Paremeter Directory' is the folder that contain prior paratmeter for pdf classification and OCR.
3. Batch Name : A string that represent 'Production Batch Number'
    -  'Batch Name' HAVE TO be the same word with 'Production Batch Folder' name. (suggest: ‘INV\_\<YYYYMMDD\_HHMM\>')

#### <ins>Output</ins>
1. Excel file: File Name : ’BatchSummary\_\<Batch Name\>.xlsx’
    - with 2 sheets: 
        - ‘sheet1’:Summary of invoice info 
        - ‘sheet2’: pivot table of invoice info
        - ‘fileStatusSummary’: to show status of PDF in the folder

2. CSV file : File Name : ’BatchSummary\_\<Batch Name\>.csv’

#### <ins>Execution step</ins>
1. Copy all pdf into a folder
2. Name to folder as batch name as batch folder 
3. Copy ‘\_OCR’ folder into working folder (it SHOULD NOT in the batch folder).
4. Compile via command line
    - (a) Open Command line program 
    - (b) Change directory to ‘app’ folder in the working folder
    - (c) Compile python script with
```
python _main.py <PATH_which_contains_production_batch_folder> <PATH_of-_OCR> <Batch_Name> 
```

Example of Working Directory

```
├── ...
├── Work_Space                           # Working Directory
│   ├── Production_Batch_Folder             # Folder that contains Production PDF files for infomation extraction
│   └── _OCR                                # Folder that contains Programs for infomation extraction 
│    └── app                                   # Folder that contains '_main.py' for information extraction
│       └── _main.py                             # Script for information extraction                       
└── ...
```
Example of python script

```
python _main.py './Work_Space' './Work_Space/_OCR' 'INV_20250109_2355' 

```

## 02. Installation

### 01. To install ‘poppler’ 
(Reference: https://github.com/Belval/pdf2image)
	
#### <ins>Window</ins>
Windows users will have to build or download poppler for Windows. The recommend version is  @oschwartz10612 version which is the most up-to-date. Then it has to add the bin/ folder to PATH or use poppler\_path = r"C:pathtopoppler-xxbin" as an argument in convert\_from\_path.

#### <ins>Mac</ins>
Mac users will have to install poppler. Installing using Brew:

	brew install poppler

#### <ins>Linux</ins>
Most distros ship with pdftoppm and pdftocairo. If they are not installed, refer to your package manager to install poppler-utils


### 02. To install tesseract
#### <ins>Window</ins>
Simple steps for tesseract installation in windows. 
(Reference: https://stackoverflow.com/questions/46140485/tesseract-installation-in-windows)
1. Download tesseract exe from https://github.com/UB-Mannheim/tesseract/wiki.
2. Install this exe in C:Program Files (x86)Tesseract-OCR
3. Open virtual machine command prompt in windows or anaconda prompt.
4. Run 
```	
    pip install pytesseract
```	

#### <ins>Mac</ins>
Mac users will have to install tesseract. Installing using Brew
```		    
    brew install tesseract
```	

#### <ins>Linux</ins>
Linux users will have to install tesseract. Installing using apt-get
```		
    apt-get install tesseract-ocr
```	

### 03. To install necessary python packages
1. Install pip (Reference: https://pip.pypa.io/en/stable/installation/)
2. Install virtualenv  (Reference: https://virtualenv.pypa.io/en/latest/)
3. Active the virtualenv
4. Install python package with
```	
    pip install -r requirements.txt
```

## 03. Labelling Preparation

#### <ins>Input</ins>
1. Working space PATH which is a directory that contains 'Production Batch Folder'. 
	- 'Production Batch Folder' is the folder that contain PDF files.
2. Batch Name : A string that represent 'Production Batch Number'
	-  'Batch Name' HAVE TO be the same word with 'Production Batch Folder' name. (suggest: ‘INV\_\<YYYYMMDD\_HHMM\>')

#### <ins>Output</ins>
The program will return 2 folders: 
1. Folder ‘<Batch Name>\_Labelling’
	 In this folder, there are 2 folders:
	1. ‘_gray’ ; contains gray PNG files (files that be transformed from PDF)
	2. ‘_picture’ contains color PNG files (files that be transformed from PDF)

2. Folder ‘<Batch Name>\_Control’
	In this folder, there are 2 files:
	1.  ‘<Batch Name>\_Overall.json’ ; Contains basic info of the files in developing batch folder.
	2. ‘<Batch Name>\_PDF.json’ ; contains basic info of the ONLY pdf in developing batch folder.

#### <ins>Execution step</ins>
1. Copy all pdf into a folder
2. Name to folder as batch name as batch folder 
3. Copy ‘\_OCR’ folder into working folder (it SHOULD NOT in the batch folder).
4. Compile via command line
	- (a) Open Command line program 
	- (b) Change directory to ‘\_OCR\labellingPrep’ folder in the working folder
	- (c) Compile python script with
```
	python _mainpdfToGrayPNG.py <PATH_which_contains_production_batch_folder> <Batch_Name> 
```
Example of Working Directory

```
├── ...
├── Work_Space                                      # Working Directory
│   ├── Production_Batch_Folder                      # Folder that contains Production PDF files for infomation extraction.
│   ├── _OCR                                         # Folder that contains Programs for infomation extraction.
│   │    └── labellingPrep                              # Folder that contains '_mainpdfToGrayPNG.py' for preparation PDF before Labelling.         
│   |        └── _mainpdfToGrayPNG.py                             # Script for information extraction                  
│   | 
│   ├── Production_Batch_Folder_Control              # Output Folder that contains JSON output.      
|   |    ├──  Production_Batch_Folder_Overall.json     # JSON file that contains preparation result of All files.      
|   |    └──  Production_Batch_Folder_Overall.json     # JSON file that contains preparation result of Only PDF files.            
│   └── Production_Batch_Folder_Labelling            # Output Folder that contains images for Lebelling.
|   |    ├──  _gray                                    # Folder that contains Gray PNG files.      
|   |    └──  _picture                                 # Folder that contains Color PNG files.     
└── ...
```
Example of python script

```
python _mainpdfToGrayPNG.py './Work_Space' 'INV_20250109_2355' 

```

## 04.Labelled Reconcile
### Labelling Manual
1. Copy folder '_gray' to Work_Space folder
2. Change '_gray' folder name to 'Production_Batch_Folder_Labelled'
3. Enter into the folder and start labelling with the manual below
![screenshot](/ImageDocument/PDF_Lebelling_Guideline_image.png)

### Labelled Reconcile Process
#### <ins>Input</ins>
1. Working space PATH which is a directory that contains 'Production Batch Folder'. 
	- 'Production Batch Folder' is the folder that contain PDF files.
2. PATH of ‘Development Parameter Directory'.
	- 'Development Parameter Directory' is the folder that contain prior Parameter for pdf classification and OCR.
3. Batch Name : A string that represent 'Production Batch Number'
	-  'Batch Name' HAVE TO be the same word with 'Production Batch Folder' name. (suggest: ‘INV\_\<YYYYMMDD\_HHMM\>')

#### <ins>Output</ins>
The program will return 2 folders: 
1. Folder ‘<Batch Name>\_Labelling’
	 In this folder, there are 2 folders:
	1. ‘\_gray’ ; contains gray PNG files (files that be transformed from PDF)
	2. ‘\_picture’ contains color PNG files (files that be transformed from PDF)

2. Folder ‘<Batch Name>\_Control’
	In this folder, there are 5 JSON files:
	1.  ‘Batch_<Batch Name>_listForRecieptDT.json’
		JSON file that contains basic info for manual labelling of date format.
	2.  ‘Batch_<Batch Name>_listForRecieptNo.json’
		JSON file that contains basic info for manual labelling of invoice number format.
	3. ‘Batch_<Batch Name>_listForCompanyName.json’
		JSON file that contains basic info for manual labelling of company name format.
	4. ‘Batch_<Batch Name>_listForAMT.json’
		JSON file that contains basic info for manual labelling of invoice gross amount format.
	5. ‘Batch_<Batch Name>_CheckingRules.json’
		JSON file that contains rules of 2-Step Validation rule and coordinate of PDF for cropping.

#### <ins>Execution step</ins>
1. After Labelled copy file 'Batch_companyMatching.json' and rename as 'Batch_<Batch_Name>_companyMatching.json'. then open the JSON file and log Company number, company Name, and match file name.
![screenshot](/ImageDocument/_ManualCompanyMatching.png)

2. Compile via command line
	- (a) Open Command line program 
	- (b) Change directory to ‘\_OCRlabellingPrep’ folder in the working folder
	- (c) Compile python script with
```
python _mainGetOCRParameter.py <PATH_which_contains_production_batch_folder> <PATH_of-_OCR> <Batch_Name> 

```
3. Go to Folder ‘<Batch Name>\_Control’ find files {‘Batch_<Batch Name>_listForRecieptDT.json’,‘Batch_<Batch Name>_listForRecieptNo.json’,‘Batch_<Batch Name>_listForCompanyName.json’,‘Batch_<Batch Name>_listForAMT.json’}
4. Go to Folder ‘_OCR\_pdfOCRSCRIPT_DEV’ find files {'ReciptDateFormat.json','ReciptInvNoFormat.json','CompanyNameFormat.json’,'ReciptAmtFormat.json’}
5. Manually edit 4 files in ‘_OCR\_pdfOCRSCRIPT_DEV’ with the guideline below
- Guideline for ReciptDateFormat.json: ![screenshot](/ImageDocument/_ManualReciptDateFormatJSON.png)
- Guideline for ReciptInvNoFormat.json: ![screenshot](/ImageDocument/_ManualReciptlnvNoFormatJSON.png)
- Guideline for CompanyNameFormat.json: ![screenshot](/ImageDocument/_ManualCompanyNameFormatJSON.png)
- Guideline for ReciptAmtFormat.json: ![screenshot](/ImageDocument/_ManualReciptAmtFormatJSON.png)
5. Compile _mainGetOCRParameter.py again.
6. Get result file ‘Batch_<Batch Name>_CheckingRules.json’ 
7. if you would like to applied new company from Development Environment to Production you should update '_OCR\_pdfOCRSCRIPT_PRD\Programm_RulesCurrent.json' with JSON in ‘Batch_<Batch Name>_CheckingRules.json’ 

