import sqlite3
from datetime import datetime

DBNAME = "irex.db"
CREATE_TBL_ATTENDEE = """
CREATE TABLE IF NOT EXISTS attendees (
	id integer PRIMARY KEY,
	chat_id integer NOT NULL,
	join_date timestamp
);
"""
CREATE_TBL_DEPARTED = """
CREATE TABLE IF NOT EXISTS departed (
	id integer PRIMARY KEY,
	chat_id integer NOT NULL,
	depart_date timestamp
);
"""
ADD_ATTENDEE = "INSERT INTO attendees (chat_id, join_date) VALUES(?, ?);"
CHAT_LIST_QRY = "SELECT chat_id FROM attendees;"
ATTENDEE_EXISTS = "SELECT chat_id FROM attendees WHERE chat_id = ?;"
DEPARTED_EXISTS = "SELECT chat_id FROM departed WHERE chat_id = ?;"
REMOVE_ATTENDEE = "DELETE FROM attendees WHERE chat_id = ?;"
REMOVE_DEPARTED = "DELETE FROM departed WHERE chat_id = ?;"
ADD_DEPARTED = "INSERT INTO departed (chat_id, depart_date) VALUES(?, ?);"

class DBHandler:
	def __init__(self):
		try:
			self.connection = sqlite3.connect(DBNAME, check_same_thread=False)
			self.cursor = self.connection.cursor()
			self.cursor.execute(CREATE_TBL_ATTENDEE)
			self.cursor.execute(CREATE_TBL_DEPARTED)
		except Exception as e:
			raise
	
	def add_chat(self,chat_id):
		try:
			re_join = False
			existed = False
			# check if chat id already exists or not
			_exists = self.cursor.execute(ATTENDEE_EXISTS, (chat_id,)).fetchone()
			if _exists and _exists[0] == chat_id:
				return False, False, True
			# check if he/she was left before
			_exists = self.cursor.execute(DEPARTED_EXISTS, (chat_id,)).fetchone()
			if _exists and _exists[0] == chat_id:
				re_join = True
				self.cursor.execute(REMOVE_DEPARTED, (chat_id,))

			self.cursor.execute(ADD_ATTENDEE, (chat_id, datetime.now()))
			self.connection.commit()
			return True, re_join, False
		except Exception as e:
			print(f"# Error: {e}")
			return False, False, False
	
	def get_chats(self):
		try:
			chat_ids = []
			fetched_data = self.cursor.execute(CHAT_LIST_QRY).fetchall()
			if fetched_data:
				for chat_id in fetched_data:
					chat_ids.append(chat_id[0])
			return chat_ids
		except Exception as e:
			print(f"# Error: {e}")
			return None

	def remove_chat_id(self, chat_id):
		try:
			_exists = self.cursor.execute(ATTENDEE_EXISTS, (chat_id,)).fetchone()
			if not _exists and _exists[0] != chat_id:
				return False
			# on removing a chat_id, it'll be added to another list just for regreeting
			self.cursor.execute(REMOVE_ATTENDEE, (chat_id,))
			self.cursor.execute(ADD_DEPARTED, (chat_id, datetime.now()))
			self.connection.commit()
			return True
		except Exception as e:
			print(f"# Error: {e}")
			return False		

	def close(self):
		self.connection.close()