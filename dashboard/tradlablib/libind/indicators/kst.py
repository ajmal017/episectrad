from dashboard.tradlablib.peakdetect import peakdetect
from dashboard.tradlablib.exec_trade import *
from dashboard.tradlablib.model_train import *
from dashboard.tradlablib import technicalindicator as tind
from dashboard.tradlablib import tradelib
import numpy as np

class KnowSureThingOscillator(object):

    def __init__(self, data, tii, ti):
        self.data = data
        self.tii = tii
        self.ti = ti

        graphdata = tind.display_indicator(self.data, self.tii.indicator.name, self.tii)
        for pltdt in graphdata:
            if pltdt['name'] == 'KST':
                self.kst=pltdt['y']
                break

    
    def trigger(self):
        close = self.data['Close']
        kst = self.kst

        signals_trade_buy = []
        signals_trade_sell = []

        signal_graph = []

        signals = np.zeros(close.shape)

        prevsig = 0
        for i in range(1, len(kst)):
            if (kst[i-1] < 0 and kst[i] > 0):
                #sell
                if prevsig != 2:
                    signals_trade_sell.append({'x': i, 'y': kst[i]})
                prevsig = 2
            elif kst[i-1] > 0 and kst[i] < 0:
                #overbought end, sell start
                if prevsig != 1:
                    signals_trade_buy.append({'x': i, 'y': kst[i]})
                prevsig = 1
            
            signals[i] = prevsig

        signal_graph.append({'data': signals_trade_buy, 'type': 'signal-trade-buy', 'name': 'signal-trade-buy', 'id': self.ti.pk})
        signal_graph.append({'data': signals_trade_sell, 'type': 'signal-trade-sell', 'name': 'signal-trade-sell', 'id': self.ti.pk})

        traderet = trade_with_signals(self.data, signals)

        return signal_graph, signals, traderet


    def train(self):

        cols = []
        params1 = []
        for ii in self.tii.indicator.indicatorinputs.all():
            params1.append(get_input_value(self.tii, ii.parameter))
            cols.append(ii.parameter)

        psetb, pret = train_for_kst(self.data, *params1)
        
        graphdata = tind.display_indicator(self.data, self.tii.indicator.name, self.tii, True, *psetb)
        for pltdt in graphdata:
            if pltdt['name'] == 'KST':
                self.kst=pltdt['y']
                break

        signal_graph, signals, traderet = self.trigger()

        return psetb, pret, signals
        