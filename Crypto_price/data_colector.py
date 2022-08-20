import pandas as pd
import pandas_datareader
from os import path

MYDIR = path.dirname(__file__)
def write_crypto_data(cryptocurrency, exc_currency):
    '''
    This function will check crypto price on yahoofinance.com api
    and write data on csv file if thers any changes
    '''
    file_path = MYDIR+'/'+'/crypto/' + cryptocurrency + '_data.csv'
    # tring to conectng and faching data from server trying spacific times
    for i in range(19):
        try:
            data = pandas_datareader.get_data_yahoo(f'{cryptocurrency}-{exc_currency}')
            print('Conected')
            conected = True
            break
        except Exception as e:
            print('conection Faild\n',e)
            conected = False
            continue
    # if not succeed to connect returns False
    if not conected:
        print('conection issue check internet')
        return False

    # data have dates as index moving that to coulumn
    data.reset_index(inplace= True)

    # if csv file dont exit creating it and jest writein data collected return True
    if not path.exists(file_path):
        data.to_csv(file_path, sep=',', index=False)
        print('update')
        return True

    # reading data from exicxting file
    file_data = pd.read_csv(file_path)

    # compring index data from api and file
    eql_or_n = data.index.equals(file_data.index)

    # updating file if changes
    if not eql_or_n:
        data.to_csv(file_path, sep=',', index=False)
        print('updated')

    elif eql_or_n:
        print('no changes')
    
    return True

if __name__ == '__main__':
    with open(MYDIR+'/'+'settings//crypto.txt') as f:
        CRYPTOS = f.readline().split(',')
    CURRENCY = 'USD'
    for CRYPTO in CRYPTOS:
        suced = write_crypto_data(CRYPTO, CURRENCY)



