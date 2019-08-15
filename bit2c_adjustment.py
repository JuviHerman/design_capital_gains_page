import pandas as pd
pd.options.mode.chained_assignment = None
from functions import OpenFile
from xlwt import Workbook


def openfile():
    #choose file
    path = OpenFile()
    #terminate window midway:
    if path is '':
        print('Terminated')
        exit()
    file = pd.read_excel(path)
    return(path,file)

def transfer_transaction(file):
    condition_deposit = file['Action'] == 'Deposit'
    condition_withdrawal = file['Action'] == 'Withdrawal'
    transfers = file[condition_deposit | condition_withdrawal]
    if transfers.empty:
        print('No transfers are on this file')
        return None
    return transfers

def fees(file):
    # figure out how many fees are in file who weren't added to assets cost
    withdrawal_fees = file['Action'] == "FeeWithdrawal"
    other_fees = file['Action'] == 'Fee'
    fees_file = file[withdrawal_fees | other_fees]
    if fees_file.empty:
        print('No Fees are on this file')
        return None
    return fees_file

def trade_transaction(file):
    #filter the file in order to retain the actual trades that had occured(buy and sell)
    condition_buy = file['Action'] == "Buy"
    condition_sell = file['Action'] == "Sell"
    condition_debit = file['Action'] == 'Debit'
    condition_credit = file['Action'] == 'Credit'

    file = file[condition_buy | condition_sell]
    if file.empty:
        print('No sales or purchases on this file')
        return None
    return file

def save_file(data,path,added_name):
    where_to_save = path[:-4] + " " + added_name
    writer = pd.ExcelWriter(where_to_save, engine='xlsxwriter')
    data.to_excel(writer, index=False, encoding='UTF-8')
    writer.save()

def set_original(original):
    # delete unnecessary columns and add a few corrections
    original = original.rename(
        columns={'created': 'Date', 'accountAction': 'Action', 'firstCoin': 'Symbol', 'secondCoin': 'Currency',
                 'firstAmount': 'Volume', 'feeAmount': 'Fee', 'fee': 'FeeCurrency'})
    original.loc[original['Volume'] < 0, 'Volume'] = original['Volume'] * -1
    original['Total'] = original.apply(lambda row: (row['price'] * row['Volume']), axis=1)
    original.drop(columns=['id', 'secondAmount', 'ref'], axis=1, inplace=True)
    original['Currency'] = 'ILS'
    original.loc[original['Symbol'] == 'NIS', 'Symbol'] = 'ILS'
    original['FeeCurrency'] = 'ILS'
    original['Source'] = 'Bit2C'
    original = original[
        ['Date', 'Action', 'Symbol', 'Volume', 'price', 'Currency', 'Total', 'Fee', 'FeeCurrency', 'Source']]
    original.sort_values(by='Date', ascending=True, inplace=True, axis=0)
    return original


if __name__ == '__main__':

    path,original = openfile()
    modified_original = set_original(original)

    #1. save trades to excel file
    trades = trade_transaction(modified_original)
    if trades is not None:
        save_file(trades,path," Bitcoin_tax_ready.xlsx")

    #2. save all transaction (fiat and crypto)
    transfers = transfer_transaction(modified_original)
    if transfers is not None:
        save_file(transfers, path, 'All transfers.xlsx')

    #3. save crypto transaction to excel file
    condition_noFiat = transfers['Symbol'] != 'ILS'
    crypto_transfers = transfers[condition_noFiat]
    if crypto_transfers is not None:
        save_file(crypto_transfers, path, 'Crypto transfers.xlsx')

    #4. save fees collected to excel file
    fees = fees(modified_original)
    if fees is not None:
        save_file(fees,path,'Unaccounted_for_fees.xlsx')





