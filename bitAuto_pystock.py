import pyupbit
import time
import datetime

access = "X3lCoKLLqoNYFouOXRPOahtX9pAKSeK7qW10VEfu"
secret = "xG14t7seRTnSg3XFQ1dt0XrB82jEAqGsIZayl4rP"

### 목표가 계산 ###
def cal_target
    df = pyupbit.get_ohlcv("KRW-BTC", "day")
    yesterday = df.iloc[-2]  # 어제 data - iloc - 행을 가져옴
    today = df.iloc[-1]  # 오늘 data
    yesterday_range = yesterday["high"]-yesterday["low"]
    target = today['open'] + yesterday_range * 0.5  # k=0.5, 금일 변동성 돌파 목표가
    print(target)

while True:
    now = datetime.datetime.now()                  # 현재 시간을 얻음 (9시에 시가 계산)
    price = pyupbit.get_current_price("KRW-BTC")
    print(now, price)

    time.sleep(1)