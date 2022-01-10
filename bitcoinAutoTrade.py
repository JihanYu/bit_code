import time
import pyupbit
import datetime

access = "X3lCoKLLqoNYFouOXRPOahtX9pAKSeK7qW10VEfu"
secret = "xG14t7seRTnSg3XFQ1dt0XrB82jEAqGsIZayl4rP"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)  # 2일 ohlcv 조회
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k  # 변동성돌파전략 사용
            # 전날 종가가 다음날 시가와 붙어 있으므로 df.iloc[0]['close']는 다음날 시가
            # (df.iloc[0]['high'] - df.iloc[0]['low'])은 전날 변동폭 <- 여기에 k를 곱하여 사용함
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)   # upbit에서 ohlcv 를 조회할 때 시간이 따라옴
    start_time = df.index[0]      # ohlcv 일봉(interval day) 조회하면 얻을 수 있는 df 의 첫번째 index 가 시작 시간임
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()           # 현재 시간을 받아옴
        start_time = get_start_time("KRW-BTC")  # 9:00 <- 시작 시간
        end_time = start_time + datetime.timedelta(days=1)  # 9:00 + 1day  <- 끝나는 시간

        if start_time < now < end_time - datetime.timedelta(seconds=10):  # 9:00 < 현재 <  8:59:50 (+1day)
                                                # 9시에서 다음날 9시에서 10초를 뺀 시간까지를 구함
            target_price = get_target_price("KRW-BTC", 0.5)     # 매수 목표가 계산, 전략에 맞게 변화 가능 (k 혹은 함수)
                                                                # 이평선 추가 가능 (with MA)
            current_price = get_current_price("KRW-BTC")
            if target_price < current_price:
                krw = get_balance("KRW")
                if krw > 5000:          # BTC 최소거래금액
                    upbit.buy_market_order("KRW-BTC", krw*0.9995)  # 수수료(0.05%) 고려
        else:       # 현재 시간이 8:59:50 - 9:00:00 일 때 당일 종가에 모두 매수
            btc = get_balance("BTC")  #
            if btc > 0.00008:  # 프로그램 작성 시 0.0008BTC 가 약 잔고 5000 이상 으로 판단했음 (최소 거래 금액)
                upbit.sell_market_order("KRW-BTC", btc*0.9995)   # 수수료 고려
            time.sleep(1)

    except Exception as e:
        print(e)
        time.sleep(1)