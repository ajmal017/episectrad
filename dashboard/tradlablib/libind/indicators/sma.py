from dashboard.tradlablib.peakdetect import peakdetect
from dashboard.tradlablib.exec_trade import *
from dashboard.tradlablib.model_train import *
from dashboard.tradlablib import technicalindicator as tind
from dashboard.tradlablib import tradelib
import numpy as np

class SimpleMovingAverage(object):

    def __init__(self, data, tii, ti):
        self.data = data
        self.tii = tii
        self.ti = ti

        graphdata = tind.display_indicator(self.data, self.tii.indicator.name, self.tii)
        for pltdt in graphdata:
            if pltdt['name'] == 'sma':
                self.sma=pltdt['y']
                break

    
    def trigger(self):
        close = self.data['Close']
        res = peakdetect(y_axis=self.sma, lookahead=5)
        maxpeaks = res[0]
        minpeaks = res[1]

        signal_graph = []

        signals_trade_buy = []
        signals_trade_sell = []

        signals = np.zeros(close.shape)
        for peak in maxpeaks:
            signals_trade_sell.append({'x': float(peak[0]), 'y': peak[1]})
            signals[peak[0]] = 2
        
        for peak in minpeaks:
            signals_trade_buy.append({'x': float(peak[0]), 'y': peak[1]})
            signals[peak[0]] = 1

        prevSignal = 0
        for i in range(len(close)):
            if signals[i] != 0:
                prevSignal = signals[i]
            signals[i] = prevSignal

        signal_graph.append({'data': signals_trade_buy, 'type': 'signal-trade-buy', 'name': 'signal-trade-buy', 'id': 'main'})
        signal_graph.append({'data': signals_trade_sell, 'type': 'signal-trade-sell', 'name': 'signal-trade-sell', 'id': 'main'})

        traderet = trade_with_signals(self.data, signals)

        return signal_graph, signals, traderet
        
    
    def train(self):
        cols = []
        params1 = []
        for ii in self.tii.indicator.indicatorinputs.all():
            cols.append(ii.parameter)

        params1 = prepare_params_for_sma()

        cols.extend(['Returns%', 'MaxR'])
        pret = pd.DataFrame(columns=cols)

        arglist = [[]]      # make all possible parameter combinations
        for p in params1:
            newarglist = []
            for pp in p:
                for argset in arglist:
                    newargset = argset.copy()
                    newargset.append(pp)
                    newarglist.append(newargset)

            arglist = newarglist
        
        signalsmap = dict()

        ipret = 0
        for argset in arglist:
            graphdata = tind.display_indicator(self.data, self.tii.indicator.name, self.tii, True, *argset)
            for pltdt in graphdata:
                if pltdt['name'] == 'sma':
                    pltdt1=pltdt['y']
                    break
                    
            self.sma = pltdt1

            signal_graph, signals, traderet = self.trigger()
            if traderet['winlossratio'] is None or traderet['winlossratio'] == np.inf:
                traderet = 0
            else:
                traderet = traderet['winlossratio']

            parama = argset.copy()
            parama.extend([traderet, ''])
            pret.loc[ipret] = parama
            signalsmap[ipret] = signals
            ipret+=1
        
        retcol = pret['Returns%']
        imax = np.array(retcol).argmax()
        pret.at[imax, 'MaxR'] = 'MR'
        psetb = pret.loc[imax]
        return psetb, pret, signalsmap[imax]
        