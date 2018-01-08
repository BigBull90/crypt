from Bitfinex import BitFinex
bitfinex = BitFinex()
def return_sell_amount(json):
	return int(json['asks']['amount'])
lines = []
print BitFinex.OMG
order_book = bitfinex.get_order_book("OMGUSD")
print order_book
lines.append(order_book)

for items in order_book:
	order_book[items] = sorted(order_book[items], key=lambda k: float(k.get('amount', 0)), reverse=True)
	count = 0
	print "-----------------" + items + "-------------"
	for line in order_book[items]:
		print line
		count = count + 1
		if count > 11:
			break
