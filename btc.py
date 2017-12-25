from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
import atexit
import itertools
import json
import os
import mlp
import time
from mlp.mlph import MLP
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import threading
import sqlite3

# GET_PRICE = 'https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=,USD'


currencies = ['BTC', 'USD', 'XMR', 'ETH']
curr_combs = list(itertools.combinations(currencies, 2))
value_labels = [c[0]+'_'+c[1] for c in curr_combs]
df = pd.DataFrame(columns=['ts'] + value_labels, index=['ts'])

ONLY_SHOW = ['BTC_XMR']

class Scraper(threading.Thread):
	def __init__(self,store=True, restore=True, interval=0.5):
		threading.Thread.__init__(self)
		self.interval = interval
		if store or restore:
			self.db = sqlite3.connect('cryptocurrencies.sqlite',check_same_thread=False)
			self.db.execute('''CREATE TABLE IF NOT EXISTS price (timestamp INTEGER PRIMARY KEY ASC, btc_usd REAL, btc_xmr REAL, btc_eth REAL, usd_xmr REAL, usd_eth REAL, xmr_eth REAL);''')
			if restore:
				rows = self.db.execute('SELECT * FROM price').fetchall()
				global df
				for row in rows:
					df.loc[l222222222222222222222222en(df)] = row



	def make_query(self, cu, in_, ts=None):
		if not ts: ts = int(time.time())
		return 'https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms={}&ts={}'.format(cu,in_,ts)

	def run(self):
		global df, curr_combs
		session = requests.session()
		fig, ax = plt.subplots()
		plt.suptitle('Crypto')
		ax.ticklabel_format(useOffset=False, style='plain')
		colors = ['green', 'chocolate', 'navy', 'orange', 'darkgreen', 'purple']
		ax.set_color_cycle(colors)
		which_col = lambda comb: comb[0]+'_'+comb[1]
		if self.db:
			atexit.register(self.db.close)
			db_iterator = df.iterrows()
			row = next(db_iterator)[1] #wat
			row = next(db_iterator)[1]
			while row is not None:
				row = list(row)
				ts = row.pop(0)
				for price in row:
					if which_col(curr_combs[row.index(price)]) in ONLY_SHOW:
						ax.scatter(ts, price, alpha=0.2, color=colors[row.index(price)])
				plt.pause(0.05)
				row = next(db_iterator, None)
				if row: row=row[1]
		while True:
			ts = int(time.time())
			row = [ts]
			for comb in curr_combs:
				response = json.loads(session.get(self.make_query(*comb, ts=ts)).text)
				price = response['RAW'][comb[0]][comb[1]]['PRICE']
				col = which_col(comb)
				row.append(price)
				if col in ONLY_SHOW:
					ax.scatter(ts,price, alpha=0.6, color=colors[value_labels.index(col)], s=0.5)
					plt.pause(0.05)
			df.loc[len(df)] = row
			time.sleep(self.interval)
			if self.db:
				self.db.execute('INSERT OR REPLACE INTO price(timestamp,'+','.join(value_labels)+') VALUES(?,?,?,?,?,?,?)', row)
				self.db.commit()

def main():
	s = Scraper()
	s.start()

main()