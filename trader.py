import backtrader as bt
import datetime
from strategies import TestStrategy

cerebro = bt.Cerebro()

# set portfolio balance 
cerebro.broker.set_cash(1000000)


# Feed Data 
data = bt.feeds.YahooFinanceCSVData(
    dataname='Data/oracle.csv',
    # Do not pass values before this date
    fromdate=datetime.datetime(2000, 1, 1),
    # Do not pass values after this date
    todate=datetime.datetime(2000, 12, 31),
    reverse=False)

# Connecting Data Feed to Cerebro Object 
cerebro.adddata(data) 

cerebro.addstrategy(TestStrategy)

# modifying order size 
cerebro.addsizer(bt.sizers.FixedSize, stake = 1000)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.run()

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

# plotting 
cerebro.plot()