
# include libraries.

from bs4 import BeautifulSoup
import csv
import datetime
import urllib.request
import pandas as pd
import os

# In command line, you will get a name of state. ex: AL
strInputState = input('Input your state\n')

# as you can see, this is some urls of data-page.
html_doc = ''
url1 = 'https://www.aoml.noaa.gov/hrd/hurdat/UShurrs_detailed.html'
url2 = 'https://www.aoml.noaa.gov/hrd/hurdat/uststorms.html'

###---------the processing for first url----------------------
try:
    request = urllib.request.Request(url1) # make a request(get) for fetching html page.
    response = urllib.request.urlopen(request) # get a handle of html page by using the request.
    html_doc = response.read()  # read a page in style of text, 
except Exception as ee: # if some exception is occured
    print(ee)
    print("Request Error.")
    input('Press Enter to exit.')
    exit()

def handleCellStr(_strCell, _bDelBar = True):   # a function for processing a cell of table.
    strCell = _strCell.replace('\t', '')
    strCell = strCell.replace('\n', '')
    if _bDelBar == True:
        strCell = strCell.replace('-', '')
    strCell = strCell.replace(' ', '')
    return strCell

title = ['Name of Storm', 'No', 'Type', 'Estimated Landfall', 'Estimated Max Winds', 'Severity']    # columns in a table

export_date = datetime.datetime.now()   # get a date and time

    # produce a name of excel file.
export_xlsfname = export_date.strftime('%m') + '.' + \
               export_date.strftime('%d') + '.' + \
               export_date.strftime('%Y') + '_' + strInputState + '.xlsx'  
if os.path.exists(export_xlsfname): # if the file of same name is exist already
    try:
        os.rename(export_xlsfname, export_xlsfname + '_')
        os.rename(export_xlsfname + '_', export_xlsfname)
    except OSError as e:    # in this case, file is opening,
        print("CSV file opened. After close, and then Try.")
        exit()

results = []
    # html page have to be converted into lxml
bs_soup = BeautifulSoup(html_doc, "lxml")
tag_lines = None
try:    # look for a part for analysation.
    tag_lines = bs_soup.find('td', {'id': 'tdcontent'}).find('div').find('font').find('table').findAll('tr')
except Exception as ee:
    print(ee)
    print("No lines.")
    input('Press Enter to exit.')
    exit()

    # if data is null,
if tag_lines == None or len(tag_lines) == 0:
    print("No Content")
    input('Press Enter to exit.')
    exit()

    # get real values from data
tag_lines = tag_lines[2:]
for tr_line in tag_lines:
    line_cells = tr_line.find_all('td')
    if line_cells == None or len(line_cells) != 12:
        continue
    strDate = line_cells[0].text
    strTime = line_cells[1].text
    strLatitude = line_cells[2].text
    strLongitude = line_cells[3].text
    strMaxWinds = line_cells[4].text
    strSSHWS = line_cells[5].text
    strRMWnm = line_cells[6].text
    strCentralPressure = line_cells[7].text
    strOCI = line_cells[8].text
    strSize = line_cells[9].text
    strStates = line_cells[10].text
    strStormNames = line_cells[11].text

    strDate = handleCellStr(strDate, False)
    strTime = handleCellStr(strTime)
    strLatitude = handleCellStr(strLatitude)
    strLongitude = handleCellStr(strLongitude)
    strMaxWinds = handleCellStr(strMaxWinds)
    strSSHWS = handleCellStr(strSSHWS)
    strRMWnm = handleCellStr(strRMWnm)
    strCentralPressure = handleCellStr(strCentralPressure)
    strOCI = handleCellStr(strOCI)
    strSize = handleCellStr(strSize)
    strStates = handleCellStr(strStates)
    strStormNames = handleCellStr(strStormNames)
        
        # For the changing of date style
    while True:
        try:
            temp = strDate[len(strDate) - 1:]
            nTemp = int(temp)
            break
        except Exception as e:
            strDate = strDate[:len(strDate) - 1]
        
    strNoFront = format(int(strDate.split('-')[0]), '02d')
    strNo = strDate[len(strDate) - 2:] + '-' + strNoFront
    strModifedDate = strDate.split('-')[1]
        
        # look for data that is stable for given state.
    bState = False
    strStateLast = ''
    strSeverity = ''
    if strStates.find(',') > -1:
        nList = [0]
        strStateItems = strStates.split(',')
        for strStateOne in strStateItems:
            if strStateOne.find(strInputState) > -1:
                strSeverity = strStateOne
                bState = True
                nList.append(int(strStateOne[len(strStateOne) - 1:]))
        strStateLast = str(max(nList))
    else:
        strSeverity = strStates
        if strStates.find(strInputState) > -1:
            bState = True
        strStateLast = strStates[len(strStates) - 1:]
        
    if bState == False:
        continue
        
    # from the severity number, get some characters such as H(Hurricanes), and MH(Major Hurricanes).

    strType = ''
    if strStateLast == '1':
        strType = 'H'
    elif strStateLast == '2':
        strType = 'H'
    elif strStateLast == '3':
        strType = 'MH'
    elif strStateLast == '4':
        strType = 'MH'
    elif strStateLast == '5':
        strType = 'MH'
        
    # for exporting to file, produce a line in the style of table column.
    line = [strStormNames, strNo, strType, strModifedDate, strMaxWinds, strSeverity]

    # collect the lines 
    results.append(line)



###---------the processing for second url----------------------



try:
    request = urllib.request.Request(url2)
    response = urllib.request.urlopen(request)
    html_doc = response.read()
except Exception as ee:
    print(ee)
    print("Request Error.")
    input('Press Enter to exit.')
    exit()

def handleCellStr(_strCell, _bDelBar = True):
    strCell = _strCell.replace('\t', '')
    strCell = strCell.replace('\n', '')
    if _bDelBar == True:
        strCell = strCell.replace('-', '')
    strCell = strCell.replace(' ', '')
    return strCell

export_date = datetime.datetime.now()
export_xlsfname = export_date.strftime('%m') + '.' + \
               export_date.strftime('%d') + '.' + \
               export_date.strftime('%Y') + '_0_' + strInputState + '.xlsx'
if os.path.exists(export_xlsfname):
    try:
        os.rename(export_xlsfname, export_xlsfname + '_')
        os.rename(export_xlsfname + '_', export_xlsfname)
    except OSError as e:
        print("Excel file opened. After close, and then Try.")
        exit()
# html_file = open("response.txt", "r")
# html_doc = html_file.read()
# bs_soup = BeautifulSoup(html_doc, "html.parser")
bs_soup = BeautifulSoup(html_doc, "lxml")
tag_lines = None
try:
    tag_lines = bs_soup.find('td', {'id': 'tdcontent'}).find('div').find('center').find('table').findAll('tr')
    
    # tag_lines = bs_soup.find('td', {'id': 'tdcontent'}).find_all('tr')
except Exception as ee:
    print(ee)
    print("No lines.")
    input('Press Enter to exit.')
    exit()

if tag_lines == None or len(tag_lines) == 0:
    print("No Content")
    input('Press Enter to exit.')
    exit()

tag_lines = tag_lines[2:]
idx = 0
for tr_line in tag_lines:
    idx += 1
    line_cells = tr_line.find_all('td')
    if len(line_cells) != 7 and len(line_cells) != 8:
        continue
    #print(line_cells)
    strStorm = line_cells[0].text
    strDate = line_cells[1].text
    strTime = line_cells[2].text
    strLatitude = line_cells[3].text
    strLongitude = line_cells[4].text
    strMaxWinds = line_cells[5].text
    strStates = line_cells[6].text
    strStormNames = ""
    if len(line_cells) > 7:
        strStormNames = line_cells[7].text

    strStrom = handleCellStr(strStorm)
    strDate = handleCellStr(strDate, False)
    strTime = handleCellStr(strTime)
    strLatitude = handleCellStr(strLatitude)
    strLongitude = handleCellStr(strLongitude)
    strMaxWinds = handleCellStr(strMaxWinds)
    strStates = handleCellStr(strStates)
    strStormNames = handleCellStr(strStormNames)

        
    while True:
        try:
            temp = strDate[len(strDate) - 1:]
            nTemp = int(temp)
            break
        except Exception as e:
            strDate = strDate[:len(strDate) - 1]
        
    strNoFront = format(int(strStorm), '02d')
    strNo = strDate[len(strDate) - 2:] + '-' + strNoFront
        
    bState = False
    strStateLast = ''
    strSeverity = ''

    if strStates.find('/') > -1:
        nList = [0]
        strStateItems = strStates.split('/')
        for strStateOne in strStateItems:
            if strStateOne.find(strInputState) > -1:
                strSeverity = strStateOne
                bState = True
        strStateLast = str(max(nList))
    else:
        strSeverity = strStates
        if strStates.find(strInputState) > -1:
            bState = True
        strStateLast = strStates[len(strStates) - 1:]
        
    if bState == False:
        continue
        
    strType = 'TS'
    line = [ strStormNames, strNo, strType, strDate,  strMaxWinds, strSeverity]

    results.append(line)

    # conclude columns and results to export to excel.

df = pd.DataFrame(results, columns=title)
    # export the data into excel, filename, sheet->hurricane.
df.to_excel(export_xlsfname, sheet_name='hurricane', index=False)

    # if it is completed, print the text as follows.
input('Press Enter to exit.')