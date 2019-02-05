import pandas as pd
import dateutil
from tkinter.filedialog import askopenfilename
import tkinter as tk


def divide_to_different_coins(pd1):
    coins = pd1['מטבע'].unique()
    pd_list = []
    for i in coins:
        condition = (pd1['מטבע']== i)
        df2 = pd1[condition]
        df2.reset_index( drop=True, inplace = True)
        pd_list.append((i,df2))
    return pd_list

def Convert_to_ILS_Figures(file : pd.DataFrame):
    # convert from USD to ILS
    Dollar_ILS_Rates = pd.read_excel('dollar values.xlsx',index_col=None)
    file.columns = ["Symbol","Volume","Date Acquired","Date Sold","Currency","Proceeds","Nominal_Cost_Basis","Gain"]

    #change caption of currency to ILS
    file['Currency'] = 'ILS'

    #left merge for purchasings USD rate
    file.rename(columns={'Date Acquired': 'Date'}, inplace=True)
    result = file.merge(Dollar_ILS_Rates,on = 'Date',how = 'left')

    #update ILS value for cost_base, delete "Dollar_ILS_Rates" column, rename 'Date' to 'Date Acquired'
    result['Nominal_Cost_Basis'] *= result['USD/ILS']
    result['Nominal_Cost_Basis'] = round(result['Nominal_Cost_Basis'],2)
    del result['USD/ILS']
    result.rename(columns = {'Date' : 'Date Acquired'}, inplace= True)

    #left merge for sells USD rate
    result.rename(columns={'Date Sold': 'Date'}, inplace=True)
    result2 = result.merge(Dollar_ILS_Rates,on = 'Date',how = 'left')

    #update ILS value for Proceeds, delete "Dollar_ILS_Rates" column, rename 'Date' to 'Date Sold'
    result2['Proceeds'] *= result2['USD/ILS']
    result2['Proceeds'] = round(result2['Proceeds'],2)
    del result2['USD/ILS']
    result2.rename(columns = {'Date' : 'Date Sold'}, inplace= True)

    #update gains column
    result2['Gain'] = result2['Proceeds'] - result2['Nominal_Cost_Basis']

    return result2

def Inflation_Adjusted_Cost_Basis(file: pd.DataFrame):
    #Pandas object for Israeli rates thougout the years - until 11/2018
    Israeli_Rates = pd.read_excel('C:\\Users\\yuval\\PycharmProjects\\delay_capital_gains\\‏‏rates.xlsx',index_col=None)

    test_file = file
    test_file.columns = ["Symbol","Volume","Date Acquired","Date Sold","Currency","Proceeds","Nominal_Cost_Basis","Gain"]

    #add Purchased YearMonth value to the list
    test_file['YearMonth'] = test_file['Date Acquired'].map(lambda x: 100*x.year + x.month)

    results=test_file.merge(Israeli_Rates,on='YearMonth',how = 'left')
    results.rename(columns = {'Rate':'Purchasing_rate'}, inplace = True)
    del results['YearMonth']

    #add Sale YearMonth value to the list
    results['YearMonth'] = results['Date Sold'].map(lambda x: 100*x.year + x.month)
    results2=results.merge(Israeli_Rates,on='YearMonth',how = 'left')
    results2.rename(columns = {'Rate':'Sale_rate'}, inplace = True)
    del results2['YearMonth']

    #add inflation percentage
    results2['Periodical_Inflation_In_percent'] = round(((results2['Sale_rate']/results2['Purchasing_rate'])-1)*100,3)

    #add inflation adjustment
    results2.loc[results2.Periodical_Inflation_In_percent > 0, 'Inflation_Adjusted_Cost_Basis'] =  results2.Nominal_Cost_Basis * (1+(results2.Periodical_Inflation_In_percent/100))
    results2.loc[results2.Periodical_Inflation_In_percent <= 0, 'Inflation_Adjusted_Cost_Basis'] =  results2.Nominal_Cost_Basis

    #recalculate correct gains/losses
    results2['Gain'] = results['Proceeds'] - results2['Inflation_Adjusted_Cost_Basis']
    cols = ['Symbol'] + ['Volume'] + ['Date Acquired'] + ['Purchasing_rate'] +['Date Sold'] + ['Sale_rate'] + ['Currency'] + ['Proceeds'] + ['Nominal_Cost_Basis'] + ['Periodical_Inflation_In_percent'] + ['Inflation_Adjusted_Cost_Basis'] + ['Gain']
    results2 = results2[cols]
    results2['Periodical_Inflation_In_percent'] = results2['Periodical_Inflation_In_percent'].astype(str) + '%'

    #fix date variable to look better
    results2['Date Acquired'] = results2['Date Acquired'].dt.date
    results2['Date Sold'] = results2['Date Sold'].dt.date

    #give hebrew titles
    results2.columns = ["מטבע","כמות","תאריך רכישה","מדד רכישה","תאריך מכירה","מדד מכירה","מטבע הצגה","תמורה","עלות מקורית נומינאלית","שיעור שינוי אינפלציוני בתקופה","עלות מקורית מתואמת","רווח/הפסד"]

    return results2

def prepare_capital_gains_file_for_print(df1):

    ## in case "Date Sold" and "Date Acquired" is with chars such as "-" between parameters, these two lines of code will fix
    try:
        df1['Date Sold'] = df1['Date Sold'].apply(dateutil.parser.parse, dayfirst=True)
        df1['Date Acquired'] = df1['Date Acquired'].apply(dateutil.parser.parse, dayfirst=True)
    except:
        pass

    #delete unmatched coloumn if exists
    if 'Unmatched' in list(df1.head(0)):
        df1.drop(['Unmatched'],axis =1 ,inplace = True)

    #groupby rows by condition
    x = df1.groupby(['Date Sold','Symbol','Date Acquired','Currency'], as_index=False).sum()
    cols = ['Symbol'] + ['Volume'] + ['Date Acquired'] + [col for col in x if col != 'Volume' and col != 'Symbol' and col != 'Date Acquired']
    x = x[cols]
    x.sort_values(by='Date Sold')
    x.columns = ["מטבע","כמות","תאריך רכישה","תאריך מכירה","מטבע הצגה","תמורה","עלות מקורית","רווח/הפסד"]

    return x

def prepare_capital_gains_file_for_work(df1):
    try:
        df1['Date Sold'] = df1['Date Sold'].apply(dateutil.parser.parse, dayfirst=True)
        df1['Date Acquired'] = df1['Date Acquired'].apply(dateutil.parser.parse, dayfirst=True)
    except:
        pass

        # delete unmatched coloumn if exists
    if 'Unmatched' in list(df1.head(0)):
        df1.drop(['Unmatched'], axis=1, inplace=True)


    x = df1.groupby(['Date Sold','Symbol','Date Acquired','Currency'], as_index=False).sum()
    cols = ['Symbol'] + ['Volume'] + ['Date Acquired'] + [col for col in x if col != 'Volume' and col != 'Symbol' and col != 'Date Acquired']
    x = x[cols]
    x.sort_values(by='Date Sold')
    return x

def OpenFile():
    root = tk.Tk()
    root.withdraw()
    name = askopenfilename(initialdir="C:\\Users\\yuval\\Desktop\\",filetypes =(("Csv File", "*.csv"),("All Files","*.*")),title = "Choose a file")
    return name

