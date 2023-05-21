import pandas as pd
import numpy as np
from fbprophet import Prophet

# 各等級の時間帯別当選数データ
np.random.seed(0)
date_range = pd.date_range(start='2023-01-01', end='2023-01-31', freq='H')
data = {
    'ds': date_range,  
    'prize1_counts': np.random.randint(1, 10, size=len(date_range)), 
    'prize2_counts': np.random.randint(10, 20, size=len(date_range)), 
    'prize3_counts': np.random.randint(20, 30, size=len(date_range)), 
}
df = pd.DataFrame(data)

# 各等級の時間帯別当選割合データを作成
total_winnings = df[['prize1_counts', 'prize2_counts', 'prize3_counts']].sum(axis=1)
df['prize1_ratio'] = df['prize1_counts'] / total_winnings
df['prize2_ratio'] = df['prize2_counts'] / total_winnings
df['prize3_ratio'] = df['prize3_counts'] / total_winnings

df.head()

# 各等級ごとのProphetモデルを訓練
models = {}
for prize in ['prize1_ratio', 'prize2_ratio', 'prize3_ratio']:
    model = Prophet(daily_seasonality=True)
    model.fit(df[['ds', prize]].rename(columns={prize: 'y'}))
    models[prize] = model

# 未来7日間の各等級の当選割合の予測
future = models['prize1_ratio'].make_future_dataframe(periods=7*24, freq='H')

forecasts = {}
for prize, model in models.items():
    forecast = model.predict(future)
    forecasts[prize] = forecast

    # 予測結果の表示
    print(f'--- {prize} ---')
    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
    print()

# 各等級の予測結果を合計
total_forecast = pd.DataFrame({
    'ds': forecasts['prize1_ratio']['ds'],
    'yhat': sum(forecast['yhat'] for forecast in forecasts.values()),
})

# 予測結果のプロット
for prize, model in models.items():
    model.plot(forecasts[prize])
