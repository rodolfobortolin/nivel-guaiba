from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import requests
from bs4 import BeautifulSoup
import io
import base64
import os

app = Flask(__name__)

def fetch_data():
    url = 'https://nivelguaiba.com/all'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'class': 'table table-responsive table-sm table-bordered'})

    rows = []
    for row in table.find('tbody').find_all('tr'):
        cols = row.find_all('td')
        rows.append({
            'Horário': pd.to_datetime(cols[0].text, format='%d/%m/%Y %H:%M'),
            'Cota': float(cols[1].text.replace(' m', '').replace(',', '.'))
        })

    df = pd.DataFrame(rows)
    df = df.set_index('Horário')
    return df

def create_plot():
    df = fetch_data()

    start_date = '2024-05-14 20:15'
    df = df[df.index >= start_date]

    df['Seconds'] = (df.index - df.index[0]).total_seconds()
    decreasing_intervals = df[df['Cota'].diff() < 0]

    if len(decreasing_intervals) < 5:
        return None, "Insufficient data for a robust analysis."

    X = decreasing_intervals['Seconds'].values.reshape(-1, 1)
    y = decreasing_intervals['Cota'].values

    model = LinearRegression()
    model.fit(X, y)

    target_elevations = [3.0, 1.0]
    initial_elevation = df['Cota'].iloc[-1]
    rate_of_decrease = model.coef_[0]

    if rate_of_decrease == 0:
        return None, "The rate of decrease is zero, it's not possible to predict the elevations."

    times_to_reach_targets = [(target_elevation - initial_elevation) / rate_of_decrease for target_elevation in target_elevations]
    time_targets = [df.index[-1] + pd.Timedelta(seconds=t) for t in times_to_reach_targets]

    future_seconds = np.linspace(df['Seconds'].iloc[-1], df['Seconds'].iloc[-1] + max(times_to_reach_targets), num=100)
    future_elevations = model.predict(future_seconds.reshape(-1, 1))

    future_dates = [df.index[-1] + pd.Timedelta(seconds=sec - df['Seconds'].iloc[-1]) for sec in future_seconds]
    future_df = pd.DataFrame({'Horário': future_dates, 'Cota': future_elevations})

    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df['Cota'], marker='o', label='Actual data')
    plt.plot(future_df['Horário'], future_df['Cota'], linestyle='--', color='red', label='Projection')

    plt.axvline(x=time_targets[0], color='blue', linestyle='--', label='3m Elevation Prediction')
    plt.axvline(x=time_targets[1], color='green', linestyle='--', label='1m Elevation Prediction')

    plt.text(time_targets[0], 3, time_targets[0].strftime('%d/%m/%Y %H:%M'), color='blue', ha='right')
    plt.text(time_targets[1], 1, time_targets[1].strftime('%d/%m/%Y %H:%M'), color='green', ha='right')

    plt.axhline(y=3, color='purple', linestyle='--')
    plt.text(df.index[0], 3, 'Flood Elevation', color='purple', va='bottom', ha='right', backgroundcolor='white')

    plt.title('Elevation over time with prediction')
    plt.xlabel('Time')
    plt.ylabel('Elevation (m)')
    plt.legend()
    plt.grid(True)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return plot_url, f'3m Elevation Prediction: {time_targets[0]}<br>1m Elevation Prediction: {time_targets[1]}'

@app.route('/')
def home():
    plot_url, prediction_text = create_plot()
    if plot_url is None:
        return f"<h1>Error: {prediction_text}</h1>"
    return render_template('index.html', plot_url=plot_url, prediction_text=prediction_text)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
