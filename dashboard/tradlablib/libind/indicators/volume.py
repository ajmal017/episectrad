from dashboard.tradlablib.exec_trade import *
from dashboard.tradlablib.model_train import *
from dashboard.tradlablib import technicalindicator as tind
from dashboard.tradlablib import tradelib

class Volume(object):

    def __init__(self, data, tii, ti):
        self.data = data
        self.tii = tii
        self.ti = ti

        graphdata = tind.display_indicator(self.data, self.tii.indicator.name, self.tii)
        for pltdt in graphdata:
            if pltdt['name'] == 'PVI':
                self.PVI=pltdt['y']
            if pltdt['name'] == 'NVI':
                self.NVI=pltdt['y']
    
    def trigger(self):
        close = self.data['Close']
        PVI = self.PVI
        NVI = self.NVI

        signals = []

        signals_trade_buy = []
        signals_trade_sell = []

        signal_graph = []

        signals = []    # 0: stop 1: buy 2: sell
        prevsig = 0
        signals.append(prevsig)
        for i in range(1, len(close)):
            if PVI[i-1] < NVI[i-1] and PVI[i] > NVI[i]:
                #sell start
                if prevsig != 2:
                    signals_trade_sell.append({'x': i, 'y': (PVI[i] + NVI[i])/2})
                prevsig = 2
            elif PVI[i-1] > NVI[i-1] and PVI[i] < NVI[i]:
                #overbought end, sell start
                if prevsig != 1:
                    signals_trade_buy.append({'x': i, 'y': (PVI[i] + NVI[i])/2})
                prevsig = 1

            signals.append(prevsig)

        signal_graph.append({'data': signals_trade_buy, 'type': 'signal-trade-buy', 'name': 'signal-trade-buy', 'id': self.ti.pk})
        signal_graph.append({'data': signals_trade_sell, 'type': 'signal-trade-sell', 'name': 'signal-trade-sell', 'id': self.ti.pk})


        traderet = trade_with_signals(self.data, signals)

        return signal_graph, signals, traderet
        

    