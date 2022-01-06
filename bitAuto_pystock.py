import pyupbit
import time
import datetime

access = "X3lCoKLLqoNYFouOXRPOahtX9pAKSeK7qW10VEfu"
secret = "xG14t7seRTnSg3XFQ1dt0XrB82jEAqGsIZayl4rP"

### 목표가 계산 ###
# ticker와 k 를 받아서 target 을 return 함
def cal_target(ticker, k):
    df = pyupbit.get_ohlcv(ticker, "day")
    yesterday = df.iloc[-2]  # 어제 data - iloc - 행을 가져옴
    today = df.iloc[-1]      # 오늘 data (9시 이후 바로 거래가 일어나서 마지막이 오늘 시가로 판단)
                             # 거래 없을 수 있으므로 날짜 비교하는 것이 필요할 수도
    yesterday_range = yesterday["high"]-yesterday["low"]
    target = today['open'] + yesterday_range * k  # k=0.5, 금일 변동성 돌파 목표가
    return (target)

target = cal_target("KRW-BTC", 0.5)
print(target)

while True:
    now = datetime.datetime.now()                  # 현재 시간을 얻음 (9시에 시가 계산)

    # 9시 0분 20초 - 30초 사이  (매일 아침 9시 목표가 새로 계산)
    # 당일 시가는 9시에 거래가 있어야 설정 가능 / 20-30초 정도면 거래 설정될 것으로 판단
    if now.hour == 9 and now.minute == 0 and (20 <= now.second <= 30):
        target = cal_target("KRW-BTC", 0.5)

    price = pyupbit.get_current_price("KRW-BTC")
    print(now, price)
    time.sleep(1)