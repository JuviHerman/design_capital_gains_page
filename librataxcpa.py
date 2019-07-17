import pandas as pd
import dateutil
from tkinter.filedialog import askopenfilename
import tkinter as tk
from datetime import datetime
import numpy as np
import os


def OpenFile():
    desktop_location = os.path.expanduser("~\Desktop")
    root = tk.Tk()
    root.withdraw()
    name = askopenfilename(initialdir=desktop_location,filetypes =(("Trade Files", "*.csv *.xlsx *.xls"),("All Files","*.*")),title = "Choose a file")
    return name

BitcoinTaxFile_title_identifiers = ['Volume','Symbol','Date Acquired', 'Date Sold', 'Proceeds']
BloxTaxFile_title_identifiers =['רווח\הפסד שקלים (נומינלי)', 'רווח\הפסד שקלים (ריאלי)']
Bittrex_identify = ['OrderUuid', 'Exchange', 'Type', 'Quantity', 'Limit', 'CommissionPaid', 'Price', 'Opened', 'Closed']

formats = {'BitcoinTax':BitcoinTaxFile_title_identifiers,'BloxTax':BloxTaxFile_title_identifiers,'Bittrex':Bittrex_identify}

#choose file window:
path = OpenFile()

#terminate window midway:
if path is '':
    print('Terminated')
    exit()

#check columns in order to classify origin:
try:
    file = pd.read_excel(path,index_col=False)
    titles = list(file.head(0))
except:
    file = pd.read_csv(path,index_col=False)
    titles = list(file.head(0))

#which exchange is the file from
format = None
for key,values in formats.items():
    if all(elem in titles for elem in values):
        format = key
        break
print(format)


#parse the data to objects - for bittrex file origin
#file.pop('OrderUuid')
dates = file['Closed'].dt.date()

dates.sort_values(ascending=True)
#dates = dates.loc(dates['Closed'].'{}'.format(int(datetime.year)) > 2017)
print(dates.astype(datetime))


