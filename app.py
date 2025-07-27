import time
from ibapi.client import EClient
from ibapi.wrapper import EWrapper

from ibapi.contract import Contract
from ibapi.order import Order


from threading import Thread


class IBClient(EWrapper, EClient):

    def __init__(self, host, port, client_id):
        EClient.__init__(self, self)

        self.connect(host, port, client_id)

        thread = Thread(target=self.run)
        thread.start()

    def error(self, req_id, code, msg, misc):
        if code in [2104, 2106, 2158]:
            print(msg)
        else:
            print('Error {}: {}'.format(code, msg))

    def historicalData(self, req_id, bar):
        print(bar)

    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        print(
            f"Order Status - OrderId: {orderId}, Status: {status}, Filled: {filled}, Remaining: {remaining}, AvgFillPrice: {avgFillPrice}, LastFillPrice: {lastFillPrice}")

    def nextValidId(self, orderId):
        self.nextValidOrderId = orderId

    def realtimeBar(self, reqId, time, open_, high, low, close, volume, wap, count):
        print(
            f"Realtime Bar - ReqId: {reqId}, Time: {time}, Open: {open_}, High: {high}, Low: {low}, Close: {close}, Volume: {volume}, WAP: {wap}, Count: {count}")

    def historicalDataEnd(self, reqId, start, end):
        print(f"end of data {start} {end}")

    def position(self, account, contract, position, avgCost):
        print(
            f"Position - Account: {account}, Contract: {contract.symbol}, Position: {position}, AvgCost: {avgCost}")


def mainLoop(client: IBClient):
    client.reqPositions()

    while True:
        tickerinpt = input("Enter ticker symbol (or 'exit' to quit): ")
        if tickerinpt.lower() == 'exit':
            break
        else:
            ctr = Contract()
            ctr.symbol = tickerinpt.upper()
            ctr.secType = 'STK'
            ctr.exchange = 'SMART'
            ctr.currency = 'USD'

            # client.reqRealTimeBars(3001, ctr, 5, "MIDPOINT", 0, [])
            client.reqHistoricalData(
                3001, ctr, '', '1 D', '5 mins', 'MIDPOINT', 0, 1, False, [])

            buyorsell = input("Buy or Sell? (B/S): ").strip().upper()
            if buyorsell == 'B':
                action = 'BUY'
            elif buyorsell == 'S':
                action = 'SELL'
            else:
                print("Invalid input. Please enter 'B' for Buy or 'S' for Sell.")
                continue
            quantity = int(input("Enter quantity: "))
            if quantity <= 0:
                print("Quantity must be greater than 0.")
                continue

            lmt = input("Enter limit price (blank for market price): ")

            stock_order = Order()
            stock_order.action = action
            stock_order.totalQuantity = quantity
            if lmt.strip() == '':
                stock_order.orderType = 'MKT'
            else:
                stock_order.orderType = 'LMT'
                stock_order.lmtPrice = float(lmt)
            client.placeOrder(client.nextValidOrderId, ctr, stock_order)
            client.nextValidOrderId += 1
            client.reqPositions()
            continue


if __name__ == '__main__':
    client = IBClient('127.0.0.1', 7497, 1)
    time.sleep(1)
    mainLoop(client)

    # client.run()
