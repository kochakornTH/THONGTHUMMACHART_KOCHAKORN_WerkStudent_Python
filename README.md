## 01. app
<ins>Input</ins>
1. A directory which contains production batch folder. 
2. Production paremeter directory.
3. Batch Name : same as target production batch folder name.

<ins>Output</ins>
1. Excel file: File Name : ’BatchSummary\_\<Batch Name\>.xlsx’
    - with 2 sheets: 
        - ‘sheet1’:Summary of invoice info 
        - ‘sheet2’: pivot table of invoice info
2. CSV file : File Name : ’BatchSummary\_\<Batch Name\>.csv’

<ins>Execution step</ins>
1. Copy all pdf into a folder
2. Name to folder as batch name as batch folder 
    - (suggest: ‘INV\_\<YYYYMMDD\_HHMM\>')
3. Copy ‘\_OCR’ folder into working folder (it SHOULD NOT in the batch folder).
4. Open command line
5. Change directory to ‘app’ folder in the working folder
6. Compile python script with
```
python _main.py <PATH which contains production batch folder > \<PATH of _OCR\> <Batch Name> 
```

## Installation
### Prerequisites
1. poppler
3. tesseract
4. Necessary packages in requirements.txt
4. Python 3.11.7

### 01. To install ‘poppler’ 
(ref: https://github.com/Belval/pdf2image)
	
#### **Window**
Windows users will have to build or download poppler for Windows. The recommend version is  @oschwartz10612 version which is the most up-to-date. Then it has to add the bin/ folder to PATH or use poppler\_path = r"C:pathtopoppler-xxbin" as an argument in convert\_from\_path.

#### **Mac**
Mac users will have to install poppler. Installing using Brew:

	brew install poppler

#### **Linux**
Most distros ship with pdftoppm and pdftocairo. If they are not installed, refer to your package manager to install poppler-utils


### 02. To install tesseract
#### **Window**
Simple steps for tesseract installation in windows. (Ref: https://stackoverflow.com/questions/46140485/tesseract-installation-in-windows)
1. Download tesseract exe from https://github.com/UB-Mannheim/tesseract/wiki.
2. Install this exe in C:Program Files (x86)Tesseract-OCR
3. Open virtual machine command prompt in windows or anaconda prompt.
4. Run 
```	
    pip install pytesseract
```	

#### **Mac**
Mac users will have to install tesseract. Installing using Brew
```		    
    brew install tesseract
```	

#### **Linux**
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

