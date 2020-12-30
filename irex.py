#!/usr/bin/python3
import json
import atexit
import urllib3
from config import *
from telegram import Update
from datetime import datetime
from dbhandler import DBHandler
from urllib3.util import Timeout
from persiantools.jdatetime import JalaliDate
from telegram.ext import (Updater, CommandHandler, 
	CallbackContext, MessageHandler, Filters)


def start(update: Update, context: CallbackContext) -> None:
	chat_id = update.effective_chat.id
	if chat_id:
		added, rejoin, existed = dbhandler.add_chat(chat_id)
		if existed:
			update.message.reply_text(EXISTING_MESSAGE)
		elif rejoin:
			update.message.reply_text(REJOIN_MESSAGE)
		elif added:
			update.message.reply_text(GREETING_MESSAGE)
		else:
			update.message.reply_text("Oops, Please try again later...")


def notify_all(context: CallbackContext) -> None:
	data_to_send = get_data()
	chat_list = dbhandler.get_chats()
	for chat_id in chat_list:
		context.bot.send_message(chat_id=chat_id, text=data_to_send, parse_mode='markdown')


def stop(update: Update, context: CallbackContext) -> None:
	update.message.reply_text(GOODBYE_MESSAGE)
	dbhandler.remove_chat_id(update.effective_chat.id)


def exit_bot() -> None:
	print("---> stopping jobs")
	job_queue.stop()
	print("---> stopping updater")
	updater.stop()
	print("---> closing database connection")
	dbhandler.close()


def get_channel_id(update: Update, context: CallbackContext) -> None:
	if (update.channel_post.chat_id):
		dbhandler.add_chat(update.channel_post.chat_id)


def get_data() -> str:
	response = request_manager.request("GET", IREX_URL)
	if response.status == 200:
		response_data = json.loads(response.data)
		fetch_time = response_data["check_time"]
		list_of_coins = response_data["coins"].keys()
		
		formatted_message = ""
		persian_fetch_date = JalaliDate.fromtimestamp(fetch_time).strftime("%Y/%m/%d ") + datetime.fromtimestamp(fetch_time).strftime("%H:%M:%S")

		for coin in list_of_coins:
			if coin in ALLOWED_COINS_LIST.keys():
				coin_exchanges_data = response_data["coins"][coin]
				
				formatted_message += "\n{0}".format(
					MESSAGE_HEADER.format(
						ALLOWED_COINS_LIST[coin],
						persian_fetch_date)
					)

				# for exchange in coin_exchanges_data.keys():
				# 	try:
				# 		_data = coin_exchanges_data[exchange]
				# 		formatted_message += ROW_TEMPLATE.format(
				# 			_data["exchange_lable"], EXCHANGES_LINK[exchange],
				# 			_data["buy"]["price"], _data["buy"]["vol"],
				# 			_data["sell"]["price"], _data["sell"]["vol"]
				# 		)
				# 	except Exception as e:
				# 		pass
				for exchange in EXCHANGES_ORDER:
					try:
						if exchange in coin_exchanges_data.keys():
							_data = coin_exchanges_data[exchange]
							formatted_message += ROW_TEMPLATE.format(
								_data["exchange_lable"], EXCHANGES_LINK[exchange],
								_data["buy"]["price"], _data["buy"]["vol"],
								_data["sell"]["price"], _data["sell"]["vol"]
							)
					except Exception as e:
						pass

		return formatted_message



if __name__ == "__main__":
	try:
		print("""

██ ██████  ███████ ██   ██ ██ 	 ██ ███████ ████████ 
██ ██   ██ ██       ██ ██  ██ 	 ██ ██         ██    
██ ██████  █████     ███   ██ 	 ██ ███████    ██    
██ ██   ██ ██       ██ ██  ██ 	 ██      ██    ██    
██ ██   ██ ███████ ██   ██ █████ ██ ███████    ██    
                                                       
		""")
		print("press ctrl+c to stop this bot")
		print("=============================")
		dbhandler = DBHandler()
		updater = Updater(TOKEN, use_context=True)

		job_queue = updater.job_queue
		job_send_prices = job_queue.run_repeating(notify_all, interval=EVERY_X_MIN * 60, first=0)

		request_manager = urllib3.PoolManager(timeout=Timeout(connect=1.0, read=1.0))

		updater.dispatcher.add_handler(CommandHandler('start', start))
		updater.dispatcher.add_handler(CommandHandler('stop', stop))
		updater.dispatcher.add_handler(MessageHandler(Filters.update.channel_post, get_channel_id))

		updater.start_polling()
		updater.idle()
	except KeyboardInterrupt as e:
		exit_bot()
	except Exception as e:
		print(f"# Error: {e}")
	finally:
		print("\nGood Bye...")
