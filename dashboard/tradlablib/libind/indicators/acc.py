from dashboard.tradlablib.peakdetect import peakdetect
from dashboard.tradlablib.exec_trade import *
from dashboard.tradlablib.model_train import *
from dashboard.tradlablib import technicalindicator as tind
from dashboard.tradlablib import tradelib
import numpy as np

class AccumulationDistribution(object):

    def __init__(self, data, tii, ti):
        self.data = data
        self.tii = tii
        self.ti = ti

        graphdata = tind.display_indicator(self.data, self.tii.indicator.name, self.tii)
        for pltdt in graphdata:
            if pltdt['name'] == 'acc':
                self.acc=pltdt['y']
                break

    
    def trigger(self):
        close = self.data['Close']
        res = peakdetect(y_axis=close, lookahead=10)
        res = res[0]

        signals_acc_bull = []
        signals_acc_bear = []
        signals_main_bull = []
        signals_main_bear = []

        signal_graph = []

        signals = np.zeros(close.shape)
        for i in range(0, len(res)-1, 1):
            peak = res[i]
            nextpeak = res[i+1]

            if peak[1] > nextpeak[1] and self.acc[peak[0]] < self.acc[nextpeak[0]]:
                signals_main_bear.append({'x1': float(peak[0]), 'y1': peak[1], 'x2': float(nextpeak[0]), 'y2': nextpeak[1]})
                signals_acc_bull.append({'x1': float(peak[0]), 'y1': self.acc[peak[0]], 'x2': float(nextpeak[0]), 'y2': self.acc[nextpeak[0]]})
                signals[peak[0]:nextpeak[0]] = 2
            
            if peak[1] < nextpeak[1] and self.acc[peak[0]] > self.acc[nextpeak[0]]:
                signals_main_bull.append({'x1': float(peak[0]), 'y1': peak[1], 'x2': float(nextpeak[0]), 'y2': nextpeak[1]})
                signals_acc_bear.append({'x1': float(peak[0]), 'y1': self.acc[peak[0]], 'x2': float(nextpeak[0]), 'y2': self.acc[nextpeak[0]]})
                signals[peak[0]:nextpeak[0]] = 1

        signal_graph.append({'data': signals_acc_bull, 'type': 'divergence_bull', 'name': 'divergence', 'id': self.ti.pk})
        signal_graph.append({'data': signals_main_bull, 'type': 'divergence_bull', 'name': 'divergence', 'id': 'main'})
        signal_graph.append({'data': signals_acc_bear, 'type': 'divergence_bear', 'name': 'divergence', 'id': self.ti.pk})
        signal_graph.append({'data': signals_main_bear, 'type': 'divergence_bear', 'name': 'divergence', 'id': 'main'})

        traderet = trade_with_signals(self.data, signals)

        return signal_graph, signals, traderet
        