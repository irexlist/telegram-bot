IREX_URL = "https://fullnode.ir/fee"
# this is token of your own telegram bot
TOKEN = ""
# here you specify every x minutes to send data to users
EVERY_X_MIN = 1
# which coins are you interested in? add here with it's label
ALLOWED_COINS_LIST={
	"BTC": "بیتکوین",
	"ETH": "اتریوم",
	"TRX": "ترون"
}
# put your affiliate link for every exchange 
EXCHANGES_LINK={
	"exir": "https://irexlist.com",
	"wallex": "https://irexlist.com",
	"exnovin": "https://irexlist.com",
	"arzpaya": "https://irexlist.com",
	"coinnik": "https://irexlist.com",
	"jibitex": "https://irexlist.com",
	"nobitex": "https://irexlist.com",
	"ramzinex": "https://irexlist.com",
	"changekon": "https://irexlist.com",
}
EXCHANGES_ORDER=[
	"exir",
	"wallex",
	"exnovin",
	"arzpaya",
	"coinnik",
	"jibitex",
	"nobitex",
	"ramzinex"
	"changekon"
]
# on /start message 
GREETING_MESSAGE="""
از اینکه از ربات irex ticker استفاده می‌کنید متشکریم 🙏🏻

شما می‌توانید برای اطلاع از قیمت لحظه‌ای رمز ارزها از سایت irexlist.com 💰 نیز بهره ببرید
"""
# when a left user come back again
REJOIN_MESSAGE="""
از بازگشت شما بسیار خوشحالیم 🌹😊
"""
EXISTING_MESSAGE=" شما در حال حاضر در ربات عضو هستید"
# on /stop message
GOODBYE_MESSAGE="به امید دیدار مجدد شما 👋🏻"
# price message header
MESSAGE_HEADER="""
💵 قیمت {0}
⏱ لحظه دریافت {1}
"""
# each row of price is show this like
ROW_TEMPLATE="""
[{0}]({1})
خرید	{2} / {3} 
فروش	{4} / {5}\n
"""