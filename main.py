# pip install streamlit fbprophet yfinance plotly
import streamlit as st
from datetime import date

import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go

START = "2016-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title('나스닥 100 주가 예측')

stocks = ('GOOG', 'AAPL', 'MSFT', 'GME', 'AMZN', 'LCID','JD','ZM','ZS','SIRI','ENPH','ALGN','FANG','EBAY','TEAM','WBA','ANSS','ILMN','WBD','CEG','DDOG','DLTR','FAST','CRWD','GFS','VRSK','CTSH','XEL','BKR','TTD','GEHC','SGEN','CSGP','EA','ROST','BIIB','AZN','ON','EXC','ODFL','CPRT','KHC','ADSK','AEP','PAYX','KDP','WDAY','IDXX','PCAR','LULU','MRNA','PDD','MCHP','DXCM','CTAS','MRVL','NXPI','ORLY','MAR','ASML','CHTR','MELI','FTNT','ABNB','MNST','KLAC','CDNS','CSX','SNPS','MU','PANW','REGN','PYPL','LRCX','VRTX','ADI','GILD','ADP','MDLZ','BKNG','ISRG','AMAT','SBUX','AMGN','INTU','QCOM','HON','INTC','TXN','TMUS','AMD','CMCSA','NFLX','CSCO','ADBE','COST','PEP','GOOG','AVGO','TSLA','META','NVDA')
selected_stock = st.selectbox('예측하고 싶은 기업 선택', stocks)

n_years = st.slider('Years of prediction:', 1, 3)
period = n_years * 365


@st.cache
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data

	
data_load_state = st.text('데이터 로딩중입니다...잠시만 기다려주세요')
data = load_data(selected_stock)
data_load_state.text('데이터 로딩중입니다... 완료!!')

st.subheader('Raw data')
st.write(data.tail())

# Plot raw data
def plot_raw_data():
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
	fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
	st.plotly_chart(fig)
	
plot_raw_data()

# Predict forecast with Prophet.
df_train = data[['Date','Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

# Show and plot forecast
st.subheader('Forecast data')
st.write(forecast.tail())
    
st.write(f'Forecast plot for {n_years} years')
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

st.write("Forecast components")
fig2 = m.plot_components(forecast)
st.write(fig2)
