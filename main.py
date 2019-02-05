import pandas as pd
from functions import OpenFile,prepare_capital_gains_file_for_print,Inflation_Adjusted_Cost_Basis,Convert_to_ILS_Figures,divide_to_different_coins

###groupby sale events and capital gains for each actual transaction

path = OpenFile()
print(path)
capital_gains = pd.read_csv(path,index_col=None, usecols=[0,1,2,3,4,5,6,7,8])
df1 = prepare_capital_gains_file_for_print((capital_gains))
if 'USD' in df1.values:
    print('Original was a USD file')
    df2 =Convert_to_ILS_Figures(df1)
else:
    print('Original was an ILS file')
    df2 = df1
df3 = Inflation_Adjusted_Cost_Basis(df2) #all capital gains are presented in a singel excel sheet
dfs = divide_to_different_coins(df3) # capital gains for the sales of unique Coin in seperated in several excel sheets
where_to_save = path[:-4] + " edited.xlsx"

#which method of presentation is choosen, depending on the relevant Tax year
Tax_year = int(input('for which tax year? '))
if Tax_year > 2017:
    writer = pd.ExcelWriter(where_to_save, engine='xlsxwriter')
    for i in dfs:
        coin_name = i[0]
        i[1].to_excel(writer, index=False, encoding='UTF-8', sheet_name = coin_name)
    writer.save()
else:
    df3.to_excel(where_to_save, index=False, encoding='UTF-8')





