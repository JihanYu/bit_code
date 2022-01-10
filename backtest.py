import pyupbit
import numpy as np

df = pyupbit.get_ohlcv("KRW-BTC", count=7)  # 7일 동안 원화부분의 BTC

# 변동성 돌파 기준 범위 계산
# 변동폭 * k 계산, (고가 - 저가) * k값
k = 0.5
df['range'] = (df['high'] - df['low']) * k

# target(매수가), range 컬럼을 한칸씩 밑으로 내림 (.shift(1))
df['target'] = df['open'] + df['range'].shift(1)  # range는 전날이 것이므로 한칸씩 내려야 오늘 data 와 계산 가능

fee = 0.0000   # 수수료 우선 없는 것으로 계산함
## np.where(조건문, 참일 때 값, 거짓일때 값)
# ror(수익률)
df['ror'] = np.where(df['high'] > df['target'],         # 오늘 고가가 target 보다 높으면 매수를 진행했을 것임
                     df['close'] / df['target'] - fee,  # 종가/매수가(target)가 수익률임
                     1)                                 # 매수를 진행하지 않았으므로 그대로임

# 누적 곱 계산(cumprod) => 누적수익률
df['hpr'] = df['ror'].cumprod()

# draw down 계산 (누적 최대 값과 현재 hpr 차이 / 누적 최대값 * 100)
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100

# MDD 계산 (max draw down)
print("MDD(%): ", df['dd'].max())
print("HPR : ", df['hpr'][-1])
df.to_excel("dd.xlsx")