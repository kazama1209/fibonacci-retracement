import os
from twelvedata import TDClient
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20, 10)


# ヒストリカルデータを取得
def get_historical_data(symbol, interval, outputsize, start_date, end_date):
    apikey = os.getenv('TWELVE_DATA_API_KEY')
    td = TDClient(apikey = apikey)
    
    res = td.time_series(symbol = symbol, interval = interval, outputsize = outputsize, start_date = start_date, end_date = end_date, timezone = 'Asia/Tokyo').as_json()
    
    df = pd.DataFrame(res).iloc[::-1].set_index('datetime').astype(float)
    df = df[df.index >= start_date]
    df.index = pd.to_datetime(df.index)

    return df

# フィボナッチ・リトレースメントを計算
def calc_fibonacci_retracement(df, trend_direction):
    top = df['close'].max()
    bottom = df['close'].min()
    diff = top - bottom

    if trend_direction == 'upward':
        first_level = top - diff * 0.236
        second_level = top - diff * 0.382
        third_level = top - diff * 0.5  
        fourth_level = top - diff * 0.618
    elif trend_direction == 'downward':
        first_level = bottom + diff * 0.236
        second_level = bottom + diff * 0.382
        third_level = bottom + diff * 0.5  
        fourth_level = bottom + diff * 0.618

    return top, bottom, first_level, second_level, third_level, fourth_level

symbol = 'USD/JPY' # 銘柄
interval = '1day' # 時間軸
outputsize = 5000 # 最大取得件数
start_date = '2021-02-23' # 取得開始日
end_date = '2021-05-03' # 取得終了日

# データフレームを作成
df = get_historical_data(symbol, interval, outputsize, start_date, end_date)

# フィボナッチ・リトレースメントを計算
top, bottom, first_level, second_level, third_level, fourth_level = calc_fibonacci_retracement(df, 'upward')

# 描画
plt.plot(df.index, df['close'])
plt.axhline(top, label = 'Top', linestyle = 'solid', alpha = 0.3, color = 'green')
plt.axhline(first_level, label = '23.6%', linestyle = 'dashed', alpha = 0.3, color = 'aqua')
plt.axhline(second_level, label = '38.2%', linestyle = 'dashed', alpha = 0.3, color = 'deeppink')
plt.axhline(third_level, label = '50.0%', linestyle = 'dashed', alpha = 0.3, color = 'orange')
plt.axhline(fourth_level, label = '61.8%', linestyle = 'dashed', alpha = 0.3, color = 'blue')
plt.axhline(bottom, label = 'Bottom', linestyle = 'solid', alpha = 0.3, color = 'red')
plt.legend(bbox_to_anchor=(1.05, 1), loc = 'upper left', borderaxespad = 0, fontsize = 18)
plt.ylabel('USD/JPY', fontsize = 18)
plt.show()
