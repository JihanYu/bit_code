import pyupbit
import numpy as np

df = pyupbit.get_ohlcv("KRW-BTC", count=7)  # 7일 동안 원화부분의 BTC

# 변동폭 * k 계산, (고가 - 저가) * k값
k = 0.5
df['range'] = (df['high'] - df['low']) * k

# target(매수가), range 컬럼을 한칸씩 밑으로 내림 (.shift(1))
df['target'] = df['open'] + df['range'].shift(1)

fee = 0.0000   # 수수료
# np.where(조건문, 참일 때 값, 거짓일때 값)
df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'] - fee,
                     1)

# 누적 곱 계산(cumprod) => 누적수익률
df['hpr'] = df['ror'].cumprod()

# draw down 계산 (누적 최대 값과 현재 hpr 차이 / 누적 최대값 * 100)
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100

# MDD 계산
print("MDD(%): ", df['dd'].max())
df.to_excel("dd.xlsx")