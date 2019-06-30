import pandas as pd
from functions import OpenFile,prepare_capital_gains_file_for_print,Inflation_Adjusted_Cost_Basis,Convert_to_ILS_Figures,divide_to_different_coins,set_bloxtaxfile
import os
import win32com.client

#known columns for csv loaded to project:
BitcoinTaxFile_title_identifiers = ['Volume','Symbol','Date Acquired', 'Date Sold', 'Proceeds']
BloxTaxFile_title_identifiers =['רווח\הפסד שקלים (נומינלי)', 'רווח\הפסד שקלים (ריאלי)']

#choose file window:
path = OpenFile()
print(path)

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
del file

#send to the relevant handling
isbloxtax =  all(elem in titles for elem in BloxTaxFile_title_identifiers)
isbitcointax = all(elem in titles for elem in BitcoinTaxFile_title_identifiers)

capital_gains = pd.DataFrame
if isbitcointax:
    capital_gains = pd.read_csv(path, index_col=None, usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8])
elif isbloxtax:
    capital_gains = set_bloxtaxfile(path)
else:
    print('Sorry, your file didnt match any known file we can use')
    exit()

#groupby the page
df1 = prepare_capital_gains_file_for_print(capital_gains)

#if necessary, convert USD to ILS
if 'USD' in df1.values:
    print('Original was a USD file')
    df2 =Convert_to_ILS_Figures(df1)
else:
    print('Original was an ILS file')
    df2 = df1

#adjust for inflation:
df3 = Inflation_Adjusted_Cost_Basis(df2) #all capital gains are presented in a singel excel sheet and adjusted to inflation.

#save to regular excel file
where_to_save = path[:-4] + " edited.xlsx"
writer = pd.ExcelWriter(where_to_save, engine='xlsxwriter')
df3.to_excel(writer, index=False, encoding='UTF-8')


#Save macro on a macro enabled excel file (xlsm)
where_to_save_the_macro = where_to_save[:-1] + str('m')
workbook = writer.book
workbook.filename = where_to_save_the_macro
workbook.add_vba_project('vbaProject.bin')
writer.save()

#Activate the macro on the xlsm file and save
if os.path.exists(where_to_save_the_macro):
    xl = win32com.client.Dispatch('Excel.Application')
    xl.Workbooks.Open(Filename = where_to_save_the_macro, ReadOnly=0)
    xl.Application.Run("Macro1")
    xl.Application.Quit()
    del xl

#remove regular excel file
workbook.close()
try:
   os.remove(where_to_save)
except:
    pass



