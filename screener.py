from kiteconnect import KiteConnect
from datetime import datetime, timedelta
import requests

# 🔑 Zerodha
api_key = "YOUR_API_KEY"
access_token = "YOUR_ACCESS_TOKEN"

kite = KiteConnect(api_key=api_key)
kite.set_access_token(access_token)

# 📲 Telegram
BOT_TOKEN = "8770078207:AAEx81u3m75I2p69QStnem78L6LMSVQZNpY"
CHAT_ID = "819994547"

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.get(url, params={"chat_id": CHAT_ID, "text": msg})

# 🔥 High volume stocks
stocks = [
"RELIANCE","TCS","INFY","HDFCBANK","ICICIBANK","SBIN","ITC",
"AXISBANK","KOTAKBANK","LT","BHARTIARTL","MARUTI",
"TATAMOTORS","ADANIPORTS","ADANIENT","JSWSTEEL",
"TATASTEEL","POWERGRID","NTPC","COALINDIA"
]

msg = "🔥 VOLUME BREAKOUT ALERT:\n\n"

for stock in stocks:
    try:
        s = f"NSE:{stock}"

        # 🔎 Token
        ltp_data = kite.ltp(s)
        token = ltp_data[s]["instrument_token"]

        # ⏰ First 5 min candle
        first = kite.historical_data(
            token,
            datetime.now().replace(hour=9, minute=15),
            datetime.now().replace(hour=9, minute=20),
            "5minute"
        )

        if not first:
            continue

        high = first[0]['high']
        low = first[0]['low']
        first_vol = first[0]['volume']

        # 📊 Last 5 candles (volume compare)
        past = kite.historical_data(
            token,
            datetime.now() - timedelta(minutes=30),
            datetime.now(),
            "5minute"
        )

        avg_vol = sum([c['volume'] for c in past]) / len(past)

        # 📈 Current price
        cmp = kite.ltp(s)[s]["last_price"]

        # 🔥 Volume filter
        if first_vol > avg_vol:

            if cmp > high:
                msg += f"🚀 {stock} HIGH BREAKOUT + HIGH VOLUME\n"

            elif cmp < low:
                msg += f"🔻 {stock} LOW BREAKDOWN + HIGH VOLUME\n"

    except:
        continue

send(msg)
print("✅ Done")
