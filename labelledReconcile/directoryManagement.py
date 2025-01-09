import os
import shutil
import pandas as pd
from pathlib import Path

# Make folder
def _mkdir(directory_name):
    try:
        shutil.rmtree(directory_name)  # Remove directory and its contents
        try:
            os.mkdir(directory_name)
            return '00 - Able to Create Directory'
        except OSError as e:
            return '01 - Unable to Create Directory'
    except OSError as e:
        try:
            os.mkdir(directory_name)
            return '00 - Able to Create Directory'
        except OSError as e:
            return '01 - Unable to Create Directory'

# Delete folder       
def _rmdir(directory_name):
    try:
        shutil.rmtree(directory_name)  # Remove directory and its contents
        print('Removed Directory : '+directory_name)
    except OSError as e:
        print('Cannot remove the Directory')

# List file in the directory       
def pdfFileList(filePath,folderName):
    BatchDir = os.path.join(filePath, folderName)
    TargetDir = os.listdir(BatchDir)
    data = []
    for i in TargetDir:
        data.append({
            "filePath": BatchDir,
            "fileName": i,
            "fileType": Path(i).suffix
                    })
    df = pd.DataFrame(data) 
    return BatchDir, df