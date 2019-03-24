import pandas as pd
from functions import OpenFile,prepare_capital_gains_file_for_print,Inflation_Adjusted_Cost_Basis,Convert_to_ILS_Figures,divide_to_different_coins
import os
import win32com.client
###groupby sale events and capital gains for each actual transaction

path = OpenFile()
print(path)
capital_gains = pd.read_csv(path,index_col=None, usecols=[0,1,2,3,4,5,6,7,8])
print(capital_gains)
df1 = prepare_capital_gains_file_for_print(capital_gains)
if 'USD' in df1.values:
    print('Original was a USD file')
    df2 =Convert_to_ILS_Figures(df1)
else:
    print('Original was an ILS file')
    df2 = df1
df3 = Inflation_Adjusted_Cost_Basis(df2) #all capital gains are presented in a singel excel sheet and adjusted to inflation.


#save to file
where_to_save = path[:-4] + " edited.xlsx"
writer = pd.ExcelWriter(where_to_save, engine='xlsxwriter')
df3.to_excel(writer, index=False, encoding='UTF-8')


#Save macro to macro enabled file
where_to_save_the_macro = where_to_save[:-1] + str('m')
workbook = writer.book
workbook.filename = where_to_save_the_macro
workbook.add_vba_project('vbaProject.bin')
writer.save()

#Activate the macro on xlsm file
if os.path.exists(where_to_save_the_macro):
    xl = win32com.client.Dispatch('Excel.Application')
    xl.Workbooks.Open(Filename = where_to_save_the_macro, ReadOnly=1)
    xl.Application.Run("Macro1")
    xl.Application.Quit()
    del xl

#remove xlsx file
os.remove(where_to_save)



