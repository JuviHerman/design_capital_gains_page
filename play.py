from functions import OpenFile, prepare_capital_gains_file_for_work
import pandas as pd

def read_basic_files():
    ###get opening position
    path0 = OpenFile()
    opening_position = pd.read_csv(path0, index_col=None)

    ###get capital_gains
    path1 = OpenFile()
    file = pd.read_csv(path1, index_col=None)
    capital_gains = prepare_capital_gains_file_for_work(file)

    ###get all transactions
    path2 = OpenFile()
    all_transactions = pd.read_csv(path2,index_col=None)

    return [opening_position,capital_gains,all_transactions]

###save all Client's files to pickle-----> tuple(opening,gains,transaction)----->pickle

"""
client_name = input('enter the client name:')
tuple_of_all_basic_data = read_basic_files()
opening = tuple_of_all_basic_data[0]
gains = tuple_of_all_basic_data[1]
transactions = tuple_of_all_basic_data[2]

opening.to_pickle('opening_' + client_name)
gains.to_pickle('gains_' + client_name)
transactions.to_pickle('transactions_' + client_name)
"""


"""
opening = pd.read_pickle('opening_daniel')
gains = pd.read_pickle('gains_daniel')
transactions = pd.read_pickle('transactions_daniel')

print(opening)
print(gains)
print(transactions)

"""
