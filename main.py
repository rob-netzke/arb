import numpy as np
import pandas as pd
from utils.conversions import find_best_conversion, find_first_conversion
from utils.reversals import find_best_reversal, find_first_reversal
from utils.boxes import find_best_box_spread


NIFTY_PRICE = 17_656.35 ## current NIFTY price
NIFTY_DATA= pd.read_csv("data/option_chain.csv")

NIFTY_DATA = NIFTY_DATA[['BID', 'ASK','STRIKE', 'BID.1','ASK.1']]
NIFTY_DATA.rename(columns={'BID': 'CALL_BID',
                           'ASK': 'CALL_ASK',
                           'STRIKE': 'STRIKE',
                           'BID.1': 'PUT_BID',
                           'ASK.1': 'PUT_ASK'}, inplace=True)
NIFTY_DATA.replace(',','', regex=True, inplace=True)
for col in NIFTY_DATA.columns:
    NIFTY_DATA[col] = NIFTY_DATA[col].astype(float)
NIFTY_DATA = NIFTY_DATA.to_dict('list')

print()
print('NIFTY data: ')
print('first reversal')
print(find_first_reversal(NIFTY_DATA, NIFTY_PRICE))
print('best reversal')
print(find_best_reversal(NIFTY_DATA, NIFTY_PRICE))
print('first conversion')
print(find_first_conversion(NIFTY_DATA, NIFTY_PRICE))
print('best conversion')
print(find_best_conversion(NIFTY_DATA, NIFTY_PRICE))
print()
print('==============================================================')
print()

S_0 = 100

data = pd.read_csv('data/fake_option_data.csv').rename(columns={'BID': 'CALL_BID',
                                                                'ASK': 'CALL_ASK',
                                                                'STRIKE': 'STRIKE',
                                                                'BID_P': 'PUT_BID',
                                                                'ASK_P': 'PUT_ASK'})

data = data.to_dict('list')

print('fake data: ')
print('best box spead')
print(find_best_box_spread(data, S_0))
