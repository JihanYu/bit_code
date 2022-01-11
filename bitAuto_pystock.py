import pyupbit
import time
import datetime

### 객체설정 ###
f = open("upbit_API.txt")
lines = f.readlines()
access = lines[0].strip()
secret = lines[1].strip()
f.close()

upbit = pyupbit.Upbit(access, secret)

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

### 변수 설정 ###
target = cal_target("KRW-BTC", 0.5)
op_mode = False     # 매수기능 추가 (프로그램 처음 시작한 날은 매수되지 않도록 처리)
                    # op_mode = False 이면 매수하지 않음 / True 이면 매수 가능
hold = False        # hold = False : 현재 보유하고 있는지 아닌지를 판단

while True:
    ### 목표가 갱신 ###
    now = datetime.datetime.now()                  # 현재 시간을 얻음 (9시에 시가 계산)

    ### 매도 기능 ###
    # 08:59:00에 보유하고 있으면 전량 매도 (보통 9시에 매도 많이 하므로 좀 당김)
    # 08:59:50 - 09:00:00 사이에 매도
    if now.hour == 8 and now.minute == 59 and (50 <= now.second <= 59):
        if op_mode is True and hold is True:
            btc_balance = upbit.get_balance("KRW-BTC")
            upbit.sell_market_order("KRW-BTC", btc_balance)
            hold = False

        # 새로운 거래일에서 목표가 갱신될 때까지 거래가 되지 않도록
        op_mode = False     # 팔았으면 더 이상 거래하지 않도록 변경
        time.sleep(10)      # 10초간은 거래하지 않도록 (08:59:50 - 09:00:00 에 매도하므로)
                            # 새로운 목표가 갱신 까지 거래 하지 않도록 쉼

    # 09:00:00 목표가 갱신
    # 9시 0분 20초 - 30초 사이  (매일 아침 9시 목표가 새로 계산)
    # 당일 시가는 9시에 거래가 있어야 설정 가능 / 20-30초 정도면 거래 설정될 것으로 판단
    if now.hour == 9 and now.minute == 0 and (20 <= now.second <= 30):
        target = cal_target("KRW-BTC", 0.5)
        time.sleep(10)      # 09:00:20 - 31 목표가 갱신하면 10초 동안 더 이상 갱신하지 않음
        op_mode = True      # 다음날 시가 결정되면 매수 가능으로 변경

    price = pyupbit.get_current_price("KRW-BTC")

    ### 매수 시도 ###
    # 매초마다 조건 확인 후 매수 시도
    # 동작상태(op_mode) True 이고 현재 보유하고 있지 않고(hold=False) 현재가가 목표 이상이면
    # 잔고 조회 후 시장가 매수
    # price : 예외처리 - API 호출 시 error 발생할 수 있는데 이를 예외처리함.
    if op_mode is True and price is not None and hold is False and price >= target:
        krw_balane = upbit.get_balance("KRW")           # 현재 보유 중인 원화 잔고 조회
        upbit.buy_market_order("KRW-BTC", krw_balance)  # 원화 만큼 시장가로 주문을 넣음 (시장가 주문체결)
                        # 10% 만 사고 잎으면 krw_balance * 0.1 로 변경
        hold = True     # 현재 보유 하고 있음으로 변경

    ### 상태 출력 ###
    # 현재 시간, 목표가, 현재가, 보유상태, 동작상태 #
    print(f"current time : {now},  target : {target},  current price : {price},  hold : {hold},  op : {op_mode}")

    time.sleep(1)