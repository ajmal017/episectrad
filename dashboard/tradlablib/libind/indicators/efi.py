from dashboard.tradlablib.peakdetect import peakdetect
from dashboard.tradlablib.exec_trade import *
from dashboard.tradlablib.model_train import *
from dashboard.tradlablib import technicalindicator as tind
from dashboard.tradlablib import tradelib
import numpy as np

class ElderForceIndex(object):

    def __init__(self, data, tii, ti):
        self.data = data
        self.tii = tii
        self.ti = ti

        graphdata = tind.display_indicator(self.data, self.tii.indicator.name, self.tii)
        for pltdt in graphdata:
            if pltdt['name'] == 'efi':
                self.efi=pltdt['y']
                break

    
    def trigger(self):
        close = self.data['Close']
        efi = self.efi
        res = peakdetect(y_axis=close, lookahead=10)
        res = res[0]

        signals_efi_bull = []
        signals_efi_bear = []
        signals_main_bull = []
        signals_main_bear = []

        signals_trade_buy = []
        signals_trade_sell = []

        signal_graph = []

        signals = np.zeros(close.shape)
        for i in range(0, len(res)-1, 1):
            peak = res[i]
            nextpeak = res[i+1]

            if peak[1] > nextpeak[1] and self.efi[peak[0]] < self.efi[nextpeak[0]]:
                signals_main_bear.append({'x1': float(peak[0]), 'y1': peak[1], 'x2': float(nextpeak[0]), 'y2': nextpeak[1]})
                signals_efi_bull.append({'x1': float(peak[0]), 'y1': self.efi[peak[0]], 'x2': float(nextpeak[0]), 'y2': self.efi[nextpeak[0]]})
                signals[peak[0]:nextpeak[0]] = 2
            
            if peak[1] < nextpeak[1] and self.efi[peak[0]] > self.efi[nextpeak[0]]:
                signals_main_bull.append({'x1': float(peak[0]), 'y1': peak[1], 'x2': float(nextpeak[0]), 'y2': nextpeak[1]})
                signals_efi_bear.append({'x1': float(peak[0]), 'y1': self.efi[peak[0]], 'x2': float(nextpeak[0]), 'y2': self.efi[nextpeak[0]]})
                signals[peak[0]:nextpeak[0]] = 1

        prevsig = 0
        for i in range(1, len(efi)):
            if (efi[i-1] < 0 and efi[i] > 0):
                #sell
                if prevsig != 2:
                    signals_trade_sell.append({'x': i, 'y': efi[i]})
                prevsig = 2
            elif efi[i-1] > 0 and efi[i] < 0:
                #overbought end, sell start
                if prevsig != 1:
                    signals_trade_buy.append({'x': i, 'y': efi[i]})
                prevsig = 1
            
            signals[i] = prevsig

        signal_graph.append({'data': signals_efi_bull, 'type': 'divergence_bull', 'name': 'divergence', 'id': self.ti.pk})
        signal_graph.append({'data': signals_main_bull, 'type': 'divergence_bull', 'name': 'divergence', 'id': 'main'})
        signal_graph.append({'data': signals_efi_bear, 'type': 'divergence_bear', 'name': 'divergence', 'id': self.ti.pk})
        signal_graph.append({'data': signals_main_bear, 'type': 'divergence_bear', 'name': 'divergence', 'id': 'main'})

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

        if len(params1) > 0:
            params1 = prepare_params_for_efi()

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
                if pltdt['name'] == 'efi':
                    self.efi=pltdt['y']

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
        