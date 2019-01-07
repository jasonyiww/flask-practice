import os
from flask import Flask, render_template, request, redirect
import requests
import pandas as pd

##DATA
response = requests.get("https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?api_key=yYZunJR-i1PMXuzAdryy")
data = response.json()
x = data['datatable']
pre_colns = x['columns']
colns = []
for i in range(len(pre_colns)):
    colns.append(pre_colns[i]['name'])
pre_df = pd.DataFrame()
pre_dict = {}
for coln in colns:
    pre_dict[coln] = []
pre_data = x['data']
l = len(pre_data)
for row in pre_data:
    for i in range(14):
        pre_dict[colns[i]].append(row[i])
for coln in colns:
    pre_df[coln] = pre_dict[coln]
ZQK = pre_df.loc[pre_df['ticker']=='ZQK']
ZQK = ZQK.iloc[::-1].reset_index(drop=True)
ZTS = pre_df.loc[pre_df['ticker']=='ZTS']
ZTS = ZTS.iloc[::-1].reset_index(drop=True)
ZUMZ = pre_df.loc[pre_df['ticker']=='ZUMZ']
ZUMZ = ZUMZ.iloc[::-1].reset_index(drop=True)
##

##PLOT
import numpy as np
from bokeh.embed import components
from bokeh.plotting import figure, show

def datetime(x):
    return np.array(x, dtype=np.datetime64)

def create(feature,option):
    p = figure(x_axis_type="datetime", title=option)
    p.grid.grid_line_alpha=0.3
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Price'
    p.line(datetime(ZQK['date']), ZQK[feature], color='#A6CEE3', legend='ZQK')
    p.line(datetime(ZTS['date']), ZTS[feature], color='#B2DF8A', legend='ZTS')
    p.line(datetime(ZUMZ['date']), ZUMZ[feature], color='#FB9A99', legend='ZUMZ')
    p.legend.location = "top_left"
    return p
##

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def select():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        return redirect('/plot')

@app.route('/plot', methods=['POST'])
def plot():
    if request.form.get('option')=='Closing price':
        option='Stock Closing Prices'
        feature = 'close'
    elif request.form.get('option')=='Opening price':
        option='Stock Opening Prices'
        feature = 'open'
    plot = create(feature,option)
    script, div = components(plot)
    return render_template('plot.html', script = script, div = div)
    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
