all: prices

prices:
	./bin/economy.py 20000 40000 40000 60000 > tmp/prices.txt
