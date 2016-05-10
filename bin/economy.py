#!/usr/bin/env python

import random
import math
import sys

legal_items = []

legal_items.append("diamond_cut")
legal_items.append("oil_processed")
legal_items.append("glass")
legal_items.append("salt_refined")
legal_items.append("cement")
legal_items.append("iron_refined")
legal_items.append("copper_refined")
legal_items.append("diamond_uncut")

legal_items_market_volume = int(math.ceil(random.randint(int(sys.argv[1]), int(sys.argv[2])) / 1000.0) * 1000.0)

illegal_items = []

illegal_items.append("marijuana")
illegal_items.append("cocaine_processed")
illegal_items.append("heroin_processed")

illegal_items_market_volume = int(math.ceil(random.randint(int(sys.argv[3]), int(sys.argv[4])) / 1000.0) * 1000.0)

market_share_legal = float(random.randint(10, 30)) / 10

market_share_illegal = 1

#
# i suck at python. this is why there are so many useless loops over these items.
#
# this logic comes directly from my brain and expresses how i want the prices to be built for my small economy.
#
# but given the number of items we are dealing with i doubt it will become a runtime problem.
#
def create_economy(items, market_volume, market_share):
    prices = []
    adjusted_prices = []
    initial_market_volume = market_volume

    cumulative_sell_price = 0

    for item in items:
        sell_price = int(random.randint(0, int(market_volume / market_share)))

        cumulative_sell_price = cumulative_sell_price + sell_price

        buy_price = int(math.ceil(sell_price / 1000.0) * 1000.0)

        market_volume = market_volume - buy_price

        if market_volume < 2000:
            market_volume = 2000

        prices.append("%s:%s:%s" % (item, buy_price, sell_price))

    sys.stdout.write("# remaining market volume after simulation run: %s\n" % (initial_market_volume - cumulative_sell_price))

    if (initial_market_volume - cumulative_sell_price) < 0:
        sys.stdout.write("# this economy could be severely imbalanced. please run the simulation again.\n")

    for price in prices:
        if int(price.split(":")[2]) < 1500:
            sys.stdout.write("# adjusting price for item %s (was %s)\n" % (price.split(":")[0], price.split(":")[2]))
            if (initial_market_volume - cumulative_sell_price) > 3000:
                bottom = int((initial_market_volume - cumulative_sell_price) / 2)
                top = initial_market_volume - cumulative_sell_price
                sell_price = random.randint(bottom, top)
            else:
                sell_price = random.randint(1500, 3000)

            buy_price = int(math.ceil(sell_price / 1000.0) * 1000.0)

            adjusted_prices.append("%s:%s:%s" % (price.split(":")[0], buy_price, sell_price))
        else:
            adjusted_prices.append(price)

    cumulative_sell_price = 0

    for price in adjusted_prices:
        cumulative_sell_price = cumulative_sell_price + int(price.split(":")[2])

    #
    # there is money left in the bank, just add it to the diamond sell price and buy price
    #
    if cumulative_sell_price < initial_market_volume:
        bonus = initial_market_volume - cumulative_sell_price
        sys.stdout.write("# remaining market volume after adjustment run: %s\n" % bonus)
        prices = []
        for price in adjusted_prices:
            if price.split(":")[0] in ["diamond_cut", "cocaine_processed"]:
                sys.stdout.write("# adding bonus to sell price for item %s\n" % price.split(":")[0])
                sell_price = int(price.split(":")[2]) + bonus
                buy_price = int(math.ceil(sell_price / 1000.0) * 1000.0)
                prices.append("%s:%s:%s" % (price.split(":")[0], buy_price, sell_price))
            else:
                prices.append(price)
        return prices
    else:
        return adjusted_prices

if __name__ == "__main__":
    sys.stdout.write("#\n")
    sys.stdout.write("# using legal market share distribution factor: %s\n" % market_share_legal)

    sys.stdout.write("# legal items market volume in dollars: %s\n" % legal_items_market_volume)
    sys.stdout.write("# running economy simulation for legal prices\n")
    legal_prices = create_economy(legal_items, legal_items_market_volume, market_share_legal)
    sys.stdout.write("# done.\n")

    sys.stdout.write("# illegal items market volume in dollars: %s\n" % illegal_items_market_volume)
    sys.stdout.write("# running economy simulation for illegal prices\n")
    illegal_prices = create_economy(illegal_items, illegal_items_market_volume, market_share_illegal)
    sys.stdout.write("# done.\n")
    sys.stdout.write("#\n")

    prices = []

    for price in legal_prices:
        prices.append(price)

    for price in illegal_prices:
        prices.append(price)

    for price in prices:
        sys.stdout.write("@@@;@@@VITEM_%s_BUYPRICE@@@;%s\n" % (price.split(":")[0], price.split(":")[1]))
        sys.stdout.write("@@@;@@@VITEM_%s_SELLPRICE@@@;%s\n" % (price.split(":")[0], price.split(":")[2]))
