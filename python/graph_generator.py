import pandas as pd

data = {
    "date": [],
    "open": [],
    "high": [],
    "low": [],
    "close": [],
    "volume": []
}


def plot(intraday_data):
    for x in intraday_data:
        data['date'].append(x)
        data['open'].append(float(intraday_data[x]['1. open']))
        data['high'].append(float(intraday_data[x]['2. high']))
        data['low'].append(float(intraday_data[x]['3. low']))
        data['close'].append(float(intraday_data[x]['4. close']))
        data['volume'].append(float(intraday_data[x]['5. volume']))

    plot_data(data)
    data.clear()


def plot_data(table):
    df = pd.DataFrame(table)
    new_df = df.sort_values('date')

    fig = new_df.plot.line(x='date', y='close').get_figure()
    fig.savefig('..//resources//plot-close.png')
    print(new_df)
