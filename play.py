import pandas as pd
from tkinter.filedialog import askopenfilename
import tkinter as tk
import os
import itertools

def Convert_to_ILS_Figures(file : pd.DataFrame):
    # convert from USD to ILS
    Dollar_ILS_Rates = pd.read_excel('dollar values.xlsx',index_col=None)

    for x, col in enumerate(file.columns):
        print ( x,':',col)


    column = file.columns[input('print a coloumn number to convert in to ILS figures:')]
    date_column = input('print the column representing the date:')

    #left merge for purchasings USD rate
    file.rename(columns={date_column: 'Date'}, inplace=True)
    result = file.merge(Dollar_ILS_Rates,on = 'Date',how = 'left')

    #update ILS value for cost_base, delete "Dollar_ILS_Rates" column, rename 'Date' to 'Date Acquired'
    result[column] *= result['USD/ILS']
    result[column] = round(result[column],2)
    del result['USD/ILS']
    result.rename(columns = {'Date' : date_column}, inplace= True)

    print(result[column])

    return result

def OpenFile():
    desktop_location = os.path.expanduser("~\Desktop")
    root = tk.Tk()
    root.withdraw()
    path = askopenfilename(initialdir=desktop_location,filetypes =(("Excel File", "*.xlsx"),("All Files","*.*")),title = "Choose a file")
    return path


if __name__ == '__main__':
    path = OpenFile()
    print(path)
    file_loaded = pd.read_excel(path, index_col=None, sheet ='ESPP')

    file_loaded.dropna(0)
    file = Convert_to_ILS_Figures(file_loaded)

    where_to_save = path[:-4] + " ESPP.xlsx"
    writer = pd.ExcelWriter(where_to_save, engine='xlsxwriter')
    file.to_excel(writer, index=False, encoding='UTF-8')
    writer.save()
