from datetime import date
from datetime import datetime

import re

#Cleaning
def dateFormatAdj(companyCD,ReciptDateFormat):
    dateAdjInfo = ReciptDateFormat[companyCD]
    return dateAdjInfo

def find_m_match(target_list):
  """
  Finds the first occurrence of any element from the search_list in the target_list.

  Args:
    search_list: A list of strings to search for.
    target_list: A list of strings to search within.

  Returns:
    The first matching element from the search_list, or None if no match is found.
  """
  search_list = ['M', 'MM', 'MMM', 'MMMM']
  for item in search_list:
    if item in target_list:
      return item
  return None

def find_currency_match(target_list):
  """
  Finds the first occurrence of any element from the search_list in the target_list.

  Args:
    search_list: A list of strings to search for.
    target_list: A list of strings to search within.

  Returns:
    The first matching element from the search_list, or None if no match is found.
  """
  search_list = ['€', '$']
  for item in search_list:
    if item in target_list:
      return item
  return None
    
def defineDateMonthFormat(dateTypeX,dateLangX):
    dateTypeX_List = dateTypeX.split("-")   
    monthindex = find_m_match(dateTypeX_List)
    dateFormat = monthindex+'_'+dateLangX+'_DT'
    return dateFormat

def clean_text(text):
    """
    Cleans the given text by removing newlines and extra spaces.

    Args:
        text: The input text string.

    Returns:
        The cleaned text string.
    """
    text = text.strip()  # Remove leading/trailing whitespace
    text = re.sub(r'\n+', ' ', text)  # Replace multiple newlines with a single space
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = re.sub(r'\.', '', text)  # Remove full stops (periods)
    text = re.sub(r'\,', '', text)  # Remove full stops (periods)

    return text

def create_date_from_string(year, month, day):
  """
  Creates a datetime.date object from given year, month, and day strings.

  Args:
    year: String representing the year.
    month: String representing the month.
    day: String representing the day.

  Returns:
    A datetime.date object if the input is valid, otherwise None.
  """
  try:
    year = int(year)
    month = int(month)
    day = int(day)
    return date(year, month, day)
  except ValueError:
    return None

def clean_date_string(field_InvoiceDT,_jsonDateMatching,dateMonthFormat):
  """
  Cleans the given date string and converts it to the format "YYYY-MM-DD".

  Args:
    date_string: The input date string.

  Returns:
    The cleaned date string in the format "YYYY-MM-DD".
  """
  try:
    # Split the date string by spaces
    dateType = _jsonDateMatching['dateType']
    dateLang = _jsonDateMatching['dateLang']
    datePosition =  _jsonDateMatching['datePosition']

    monthFormat = defineDateMonthFormat(dateType,dateLang)

    DD_Position = datePosition['DD']
    MM_Position = datePosition['MM']
    YY_Position = datePosition['YY']
    
    parts = field_InvoiceDT.strip().split()

    # Extract month and year
    day_str = clean_text(parts[DD_Position].strip())
    month_str = parts[MM_Position].strip()
    year_str = parts[YY_Position].strip()
      
    # Convert month to numeric representation
    months = dateMonthFormat[monthFormat]
    month = months.get(month_str, "00")  # Default to "00" if month is not found
    return create_date_from_string(year_str, month, day_str)
  except (IndexError, KeyError):
    # Handle potential errors (e.g., invalid date format)
    return None

def clean_AMT(field_grossAMT,companyCD,ReciptAmtFormat):
    x = field_grossAMT
    x = re.sub(r'\n+', ' ', x)  # Replace multiple newlines with a single space
    x = re.sub(r'\s+', ' ', x)  # Replace multiple spaces with a single space
    xList = x.split(' ')
    
    result = []
    for i in xList:
        for j in re.split(r'(\$|€+)',i):
            result.append(j)
    
    AMTPosition = ReciptAmtFormat[companyCD]['AMTPosition']
    CURPosition = ReciptAmtFormat[companyCD]['CURPosition']
    
    resultAMT = result[AMTPosition]
    resultCUR = result[CURPosition]
    
    if resultCUR == '$':
        k = resultAMT.split('.')
        decimal = k[1]
        nonDecimal = k[0]
        nonDecimal = re.sub(r'\,', '', nonDecimal)  # Remove full stops (periods)
        
        resultAMT = float(nonDecimal+'.'+str(decimal))
        
    elif resultCUR == '€':
        k = resultAMT.split(',')
        decimal = k[1]
        nonDecimal = k[0]
        nonDecimal = re.sub(r'\.', '', nonDecimal)  # Remove full stops (periods)
    
        resultAMT = float(nonDecimal+'.'+str(decimal))
    else:
        resultAMT = 0
    
    return resultAMT

