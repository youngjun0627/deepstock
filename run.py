from tactics.v1 import func_version1
from utils import get_high_volume_tickers
import pyupbit

path = 'keys.json'

def main():
    EXCEPT_COINS = ['KRW-FLOW', 'KRW-ETH', 'KRW-ADA', 'KRW-MANA']
    
    
    func_version1(EXCEPT_COINS)

if __name__=='__main__':
    main()
