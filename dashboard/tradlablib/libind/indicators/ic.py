from dashboard.tradlablib.exec_trade import *
from dashboard.tradlablib.model_train import *
from dashboard.tradlablib import technicalindicator as tind
from dashboard.tradlablib import tradelib

class IchimokuCloud(object):

    def __init__(self, data, tii, ti):
        self.data = data
        self.tii = tii
        self.ti = ti

        graphdata = tind.display_indicator(self.data, self.tii.indicator.name, self.tii)
        for pltdt in graphdata:
            if pltdt['name'] == 'ic_a':
                self.ic_a=pltdt['y']
            if pltdt['name'] == 'ic_b':
                self.ic_b=pltdt['y']

    
    def trigger(self):
        close = self.data['Close']
        high = self.data['High']
        low = self.data['Low']
        ic_a = self.ic_a
        ic_b = self.ic_b

        signals_ovbs = []

        signals_ovbe = []

        signals_ovss = []

        signals_ovse = []

        signal_graph = []

        signals = []    # 0: stop 1: buy 2: sell
        prevsig = 0
        signals.append(prevsig)

        trend = 0       # 0: undetermined, 1: uptrend, 2: downtrend
        for i in range(1, len(close)):
            if close[i] > ic_a[i] and close[i] > ic_b[i]:
                trend = 1
            elif close[i] < ic_a[i] and close[i] < ic_b[i]:
                trend = 2
            else:
                trend = 0

            if trend == 1:
                if ic_a[i] > ic_b[i] and ic_a[i-1] <= ic_b[i-1]:
                    if prevsig != 1:
                        signals_ovbe.append({'x': i, 'y': max(ic_a[i], ic_b[i], high[i])})
                    prevsig = 1
                if ic_b[i] < close[i] and ic_b[i-1] >= close[i-1]:
                    if prevsig != 1:
                        signals_ovbe.append({'x': i, 'y': max(ic_a[i], ic_b[i], high[i])})
                    prevsig = 1
                if ic_b[i] > close[i] and ic_b[i-1] <= close[i-1]:
                    if prevsig == 1:
                        signals_ovbs.append({'x': i, 'y': max(ic_a[i], ic_b[i], high[i])})
                    prevsig = 0
                if ic_a[i] < ic_b[i] and ic_a[i-1] >= ic_b[i-1]:
                    if prevsig == 1:
                        signals_ovbs.append({'x': i, 'y': max(ic_a[i], ic_b[i], high[i])})
                    prevsig = 0

            if trend == 2:
                if ic_a[i] < ic_b[i] and ic_a[i-1] >= ic_b[i-1]:
                    if prevsig != 2:
                        signals_ovse.append({'x': i, 'y': min(ic_a[i], ic_b[i], low[i])})
                    prevsig = 2
                if ic_b[i] > close[i] and ic_b[i-1] <= close[i-1]:
                    if prevsig != 2:
                        signals_ovse.append({'x': i, 'y': min(ic_a[i], ic_b[i], low[i])})
                    prevsig = 2
                if ic_b[i] < close[i] and ic_b[i-1] >= close[i-1]:
                    if prevsig == 2:
                        signals_ovss.append({'x': i, 'y': min(ic_a[i], ic_b[i], low[i])})
                    prevsig = 0
                if ic_a[i] > ic_b[i] and ic_a[i-1] <= ic_b[i-1]:
                    if prevsig == 2:
                        signals_ovss.append({'x': i, 'y': min(ic_a[i], ic_b[i], low[i])})
                    prevsig = 0
            
            signals.append(prevsig)

        signal_graph.append({'data': signals_ovbs, 'type': 'signal-ovbs', 'name': 'signal-ovbs', 'id': 'main'})
        signal_graph.append({'data': signals_ovbe, 'type': 'signal-ovbe', 'name': 'signal-ovbe', 'id': 'main'})
        signal_graph.append({'data': signals_ovss, 'type': 'signal-ovss', 'name': 'signal-ovss', 'id': 'main'})
        signal_graph.append({'data': signals_ovse, 'type': 'signal-ovse', 'name': 'signal-ovse', 'id': 'main'})

        traderet = trade_with_signals(self.data, signals)

        return signal_graph, signals, traderet
        
