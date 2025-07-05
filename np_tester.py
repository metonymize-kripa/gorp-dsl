from neuralprophet import NeuralProphet
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# Load example data
data_location = "https://raw.githubusercontent.com/ourownstory/neuralprophet-data/main/datasets/"
df = pd.read_csv(data_location + "wp_log_peyton_manning.csv")
print(df.head())

# -------------------------------
# Fit NeuralProphet model
m = NeuralProphet()
metrics = m.fit(df, freq='D')

# Predict
forecast = m.predict(df)

# Simple plot: actual vs forecast
plt.figure(figsize=(12, 6))

# Actuals
plt.plot(forecast['ds'], forecast['y'], label='Actual', marker='o', linestyle='None', color='black')

# Forecast
plt.plot(forecast['ds'], forecast['yhat1'], label='Forecast', color='blue')

plt.title('NeuralProphet Forecast vs Actuals')
plt.xlabel('Date')
plt.ylabel('Value')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()