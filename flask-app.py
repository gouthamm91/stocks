from flask import Flask, render_template
import yfinance as yf

app = Flask(__name__)

# stocks = ['RELIANCE.NS', 'TATASTEEL.NS', 'ADANIPORTS.NS', 'ASIANPAINT.NS', 'AXISBANK.NS', 'BAJAJ-AUTO.NS', 'BAJAJFINSV.NS', 'BHARTIARTL.NS',
#           'BAJFINANCE.NS', 'BPCL.NS', 'BRITANNIA.NS', 'CIPLA.NS', 'COALINDIA.NS', 'DRREDDY.NS', 'DIVISLAB.NS', 'EICHERMOT.NS', 'GRASIM.NS',
#           'HCLTECH.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS', 'HEROMOTOCO.NS', 'HINDALCO.NS', 'HINDUNILVR.NS', 'ICICIBANK.NS', 'INDUSINDBK.NS',
#           'INFY.NS', 'IOC.NS', 'JSWSTEEL.NS', 'KOTAKBANK.NS', 'LT.NS', 'M&M.NS', 'MARUTI.NS', 'NESTLEIND.NS', 'NTPC.NS', 'ONGC.NS',
#           'POWERGRID.NS', 'SBIN.NS', 'SBILIFE.NS', 'SHREECEM.NS', 'SUNPHARMA.NS', 'TATACONSUM.NS', 'TCS.NS', 'TATAMOTORS.NS', 'TECHM.NS',
#           'TITAN.NS', 'ADANIENT.NS', 'WIPRO.NS', 'ULTRACEMCO.NS']

def calcAvgRange(stock):
  data = yf.Ticker(stock).history(period='15D', interval='1D')
  highList = list(data['High'])[:-1]
  lowList = list(data['Low'])[:-1]
  rangesList = [highList[i] - lowList[i] for i in range(0, len(highList))]
  # print('Ranges List: {}'.format(rangesList))
  avgRange = sum(rangesList)/len(rangesList)
  # print('Avg Range: {}'.format(avgRange))
  return avgRange

def categorizeDays(stock, noOfDays=1):
  period = str(noOfDays) + 'D'
  data = yf.Ticker(stock).history(period=period, interval='1h')
  highList = list(data['High'])
  lowList = list(data['Low'])
  indexStr = [str(i) for i in list(data.index)]
  indexDayStart = [idx for idx, val in enumerate(indexStr) if '9:15:00' in val]
  # print('indexStr: {}'.format(indexStr))
  # print('indexDayStart: {}'.format(indexDayStart))
  rangesDays = [(round(max(highList[i:i+2]) - min(lowList[i:i+2]), 2), str(list(data.index)[i])) for i in indexDayStart]
  return rangesDays

def get_breakout_data(stocks):
  d = []
  for stock in stocks:
    avgRange = calcAvgRange(stock)
    dayStartRange = categorizeDays(stock, noOfDays=1)
    rangeRatio = [(r/avgRange, d) for r, d in dayStartRange]
    categories = [('✅' if r <= (0.39) else '✔️' if (0.39) <= round(r, 2) <= (0.59) else '❌', round(r, 2), d) for r, d in rangeRatio]
    last_date = dayStartRange[0][1];
    d.append({'name': categories[0][0] + '<br>' + stock, 'avgrange': round(avgRange, 2),'initialrange': round(dayStartRange[0][0], 2),'ratio': round(rangeRatio[0][0], 2)})
  return d, last_date

@app.route('/getdata/<name>', methods=['GET', 'POST'])
def process(name):
  response = get_breakout_data([name])[0]
  return response


@app.route('/', methods=['GET', 'POST'])
def home():
	breakout_data, last_date = get_breakout_data()
	return render_template('index.html')
# 	return '''

# <!DOCTYPE html>
# <html>
# <head>
# 	<title>Stock Suggestions</title>
# 	<meta charset="utf-8">
# 	<meta name="viewport" content="width=device-width, initial-scale=1.0">
# 	<style type="text/css">		
# 		table, td {
# 			padding: 2px;
# 			text-align: center;
# 			border: 1px solid gray;
# 		}
# 		body {
# 			background-color: #252525;
# 			color: #eeeeee;
# 			font-family: verdana;
# 		}
# 	</style>
# 	<script>
# 		// breakoutData = [
# 		// 	{'name': '✅<br>TATASTEEL.NS', 'avgrange': 1.85, 'initialrange': 0.5, 'ratio': 0.37},
# 		// 	{'name': '✔️<br>RELIANCE.NS', 'avgrange': 1.85, 'initialrange': 0.5, 'ratio': 0.37},
# 		// 	{'name': '❌<br>DRREDDY.NS', 'avgrange': 1.85, 'initialrange': 0.5, 'ratio': 0.37}
# 		// ]

# 		const breakoutData = '''+str(breakout_data)+''';

# 		const tableHeader = '<tr><td>Symbol</td><td>Avg Range</td><td>Initial Range</td><td>Ratio</td></tr>';

# 		function filterBreakout(t) {
# 			var outputStr = '';
# 			for (s=0; s<breakoutData.length; s++) {
# 				var stock = breakoutData[s]['name'];
# 				if (stock.indexOf(t) > -1) {
# 					var outputStr = outputStr + '<tr><td>'+stock+'</td><td>'+breakoutData[s]['avgrange']+'</td><td>'+breakoutData[s]['initialrange']+'</td><td>'+breakoutData[s]['ratio']+'</td></tr>';
# 				}
# 			}
# 			var outputStr = '<table>' + tableHeader + outputStr + '</table>';
# 			return outputStr
# 		}
# 		function displayDiv(i, n) {
# 			var eles = document.getElementsByName(n);
# 			for (e=0; e<eles.length; e++) {
# 				eles[e].style.display = 'none';
# 			}
# 			document.getElementById(i).style.display = 'block';
# 		}
# 	</script>
# </head>
# <body>
# 	<button onclick="displayDiv('outputcontainer', 'outputdisplays')">Breakout</button>
# 	<center>
# 		<button onclick="outputvalues.innerHTML=filterBreakout('✅');">✅ Measured Breakout</button>
# 		<button onclick="outputvalues.innerHTML=filterBreakout('✔️');">✔️ Less Than Measured</button>
# 		<button onclick="outputvalues.innerHTML=filterBreakout('❌');">❌ No Breakout</button>
# 		<button onclick="outputvalues.innerHTML=filterBreakout('.NS');">ALL</button>
# 		<div name="outputdisplays" id="outputcontainer">
# 		<h2>Breakout Stocks</h2>
# 		<h2>'''+str(last_date)+'''</h2>
# 		<div id="outputvalues">
# 		</div>
# 	</center>
# </body>
# </html>

# 	'''

if __name__ == '__main__':
	app.run()