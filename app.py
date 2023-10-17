import requests
import redis
import pygal
from flask import Flask
from datetime import datetime, timedelta

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

api_symbol = "IBM"
api_timeSeries = "INTRADAY"
api_timeframe = "2009-01"
graph_type = "line"

beginning_date = "2009-01-01"
end_date = "2009-01-30"

# example will populate the actualy array once the loop for data runs
datetime_array = []

r = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_{api_timeSeries}&symbol={api_symbol}&outputsize=full&interval=5min&apikey=V33ZAOO7VB64CV9C')
all_data = r.json()
data = all_data["Time Series (5min)"]

def extract_x_axis():
    for key in data: 
        date_object = datetime.strptime(key, "%Y-%m-%d %H:%M:%S")
        year = date_object.year
        month = date_object.month
        day =  date_object.day
        datetime_array.append(datetime(year,month,day))  
@app.route('/') # change this later for dynamic purpose
def test():
    for key in data: 
        date_object = datetime.strptime(key, "%Y-%m-%d %H:%M:%S")
        year = date_object.year
        month = date_object.month
        day =  date_object.day
        datetime_array.append(datetime(year,month,day))        
    return 

@app.route('/test')
def Line_graph():
    chart = pygal.Line()
    chart.title = 'chart name' # title
    chart.x_labels = map(lambda d: d.strftime('%Y-%m-%d'),datetime_array)
    
    chart.add('Open', []) # adds a line each data is a data point on graph
    chart.add('High',  [])
    chart.add('Low',   [])
    chart.add('Close', [])

    chart.render() # finalizes the graph 

    return chart.render_response() # prints to screen