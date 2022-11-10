import backtrader as bt

class TestStrategy(bt.Strategy):
    """
    TestStrategy extends bt.Strategy class 
    """

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Save a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # Keep track of order status 
        self.order = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return 

        if order.status in [order.Completed]:
            # recording buy/sell prices 
            if order.isbuy():
                self.log('Buy Executed {}'.format(order.executed.price))
            elif order.issell():
                self.log('Sell Executed {}'.format(order.executed.price))

            self.bar_executed = len(self)

        self.order = None 


    def next(self):
        """
        We define when we want to execute a buy 
        """
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        if self.order:
            return

        if not self.position:
            if self.dataclose[0] < self.dataclose[-1]:
                # current close less than previous close

                if self.dataclose[-1] < self.dataclose[-2]:
                    # previous close less than the previous close

                    # BUY, BUY, BUY!!! (with all possible default parameters)
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    self.order = self.buy()
        else:
            if len(self) >= (self.bar_executed + 5):
                self.log('Sell Created {}'.format(self.dataclose[0]))
                self.order = self.sell()