# _*_ coding:utf-8 _*_
'''
Created on 2021-May-29
@author: Raisul Islam
'''
from bdshare import get_last_trade_price_data

df = get_last_trade_price_data()
print(df.to_string())