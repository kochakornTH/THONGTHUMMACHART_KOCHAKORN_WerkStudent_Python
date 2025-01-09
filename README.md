# PDF Information Extraction with \OCR\app

## 01. Program Overview

### <ins>Prerequisites</ins>
1. poppler
3. tesseract
3. Python 3.11.7
4. Necessary Python packages in 'requirements.txt'

### <ins>Input</ins>
1. Working space PATH which is a directory that contains 'Production Batch Folder'. 
    - 'Production Batch Folder' is the folder that contain PDF files.
2. PATH of 'Production Paremeter Directory'.
    - 'Production Paremeter Directory' is the folder that contain prior paratmeter for pdf classification and OCR.
3. Batch Name : A string that represent 'Production Batch Number'
    -  'Batch Name' HAVE TO be the same word with 'Production Batch Folder' name. (suggest: ‘INV\_\<YYYYMMDD\_HHMM\>')

### <ins>Output</ins>
1. Excel file: File Name : ’BatchSummary\_\<Batch Name\>.xlsx’
    - with 2 sheets: 
        - ‘sheet1’:Summary of invoice info 
        - ‘sheet2’: pivot table of invoice info
2. CSV file : File Name : ’BatchSummary\_\<Batch Name\>.csv’

### <ins>Execution step</ins>
1. Copy all pdf into a folder
2. Name to folder as batch name as batch folder 
3. Copy ‘\_OCR’ folder into working folder (it SHOULD NOT in the batch folder).
4. Complie via command line
    (a) Open Command line program 
    (b) Change directory to ‘app’ folder in the working folder
    (c) Compile python script with
```
python _main.py <PATH_which_contains_production_batch_folder> <PATH_of-_OCR> <Batch_Name> 
```

Example of Working Directory

```
├── ...
├── Work_Space                           # Working Directory
│   ├── Production_Batch_Folder          # Folder that contains Production PDF files for infomation extraction
│   └── _OCR                             # Folder that contains Programs for infomation extraction
│                              
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
1. Install pip (Ref: https://pip.pypa.io/en/stable/installation/)
2. Install virtualenv  (Ref: https://virtualenv.pypa.io/en/latest/)
3. Active the virtualenv
4. Install python package with
```	
    pip install -r requirements.txt
```

## 03. Program Overview


