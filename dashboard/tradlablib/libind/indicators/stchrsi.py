from dashboard.tradlablib.peakdetect import peakdetect
from dashboard.tradlablib.exec_trade import *
from dashboard.tradlablib.model_train import *
from dashboard.tradlablib import technicalindicator as tind
from dashboard.tradlablib import tradelib

class StochasticRSI(object):

    def __init__(self, data, tii, ti):
        self.data = data
        self.tii = tii
        self.ti = ti

        graphdata = tind.display_indicator(self.data, self.tii.indicator.name, self.tii)
        for pltdt in graphdata:
            if pltdt['name'] == 'STCHRSI':
                self.stoch=pltdt['y']
                break

    
    def trigger(self, ovb, ovs):
        stoch = self.stoch
        close = self.data['Close']
        res = peakdetect(y_axis=close, lookahead=10)
        res = res[0]

        signals_ovbs = []

        signals_ovbe = []

        signals_ovss = []

        signals_ovse = []

        signal_graph = []

        signals = []    # 0: stop 1: buy 2: sell

        signals_stoch_bull = []
        signals_stoch_bear = []
        signals_main_bull = []
        signals_main_bear = []

        prevsig = 0
        
        signals = np.zeros(close.shape)
        for i in range(0, len(res)-1, 1):
            peak = res[i]
            nextpeak = res[i+1]

            if peak[1] > nextpeak[1] and self.stoch[peak[0]] < self.stoch[nextpeak[0]]:
                signals_main_bear.append({'x1': float(peak[0]), 'y1': peak[1], 'x2': float(nextpeak[0]), 'y2': nextpeak[1]})
                signals_stoch_bull.append({'x1': float(peak[0]), 'y1': self.stoch[peak[0]], 'x2': float(nextpeak[0]), 'y2': self.stoch[nextpeak[0]]})
                signals[peak[0]:nextpeak[0]] = 1
            
            if peak[1] < nextpeak[1] and self.stoch[peak[0]] > self.stoch[nextpeak[0]]:
                signals_main_bull.append({'x1': float(peak[0]), 'y1': peak[1], 'x2': float(nextpeak[0]), 'y2': nextpeak[1]})
                signals_stoch_bear.append({'x1': float(peak[0]), 'y1': self.stoch[peak[0]], 'x2': float(nextpeak[0]), 'y2': self.stoch[nextpeak[0]]})
                signals[peak[0]:nextpeak[0]] = 2

        for i in range(1, len(stoch)):
            if (stoch[i] >= ovb and stoch[i-1] < ovb):
                #overbought start
                signals_ovbs.append({'x': i, 'y': stoch[i]})
                prevsig = 0
            elif (stoch[i-1] > ovb and stoch[i] <= ovb):
                #overbought end, sell start
                signals_ovbe.append({'x': i, 'y': stoch[i]})
                prevsig = 2
            elif (stoch[i-1] > ovs and stoch[i] <= ovs):
                #oversold start
                signals_ovss.append({'x': i, 'y': stoch[i]})
                prevsig = 0
            elif (stoch[i-1] < ovs and stoch[i] >= ovs):
                #oversold end, buy start
                signals_ovse.append({'x': i, 'y': stoch[i]})
                prevsig = 1
            
            signals[i] = prevsig

        signal_graph.append({'data': signals_stoch_bull, 'type': 'divergence_bull', 'name': 'divergence', 'id': self.ti.pk})
        signal_graph.append({'data': signals_main_bull, 'type': 'divergence_bull', 'name': 'divergence', 'id': 'main'})
        signal_graph.append({'data': signals_stoch_bear, 'type': 'divergence_bear', 'name': 'divergence', 'id': self.ti.pk})
        signal_graph.append({'data': signals_main_bear, 'type': 'divergence_bear', 'name': 'divergence', 'id': 'main'})

        signal_graph.append({'data': signals_ovbs, 'type': 'signal-ovbs', 'name': 'signal-ovbs', 'id': self.ti.pk})
        signal_graph.append({'data': signals_ovbe, 'type': 'signal-ovbe', 'name': 'signal-ovbe', 'id': self.ti.pk})
        signal_graph.append({'data': signals_ovss, 'type': 'signal-ovss', 'name': 'signal-ovss', 'id': self.ti.pk})
        signal_graph.append({'data': signals_ovse, 'type': 'signal-ovse', 'name': 'signal-ovse', 'id': self.ti.pk})

        signal_graph.append({'y': [ovb], 'type': 'signal-threshold-ovb', 'name': 'signal-threshold-ovb', 'id': self.ti.pk})
        signal_graph.append({'y': [ovs], 'type': 'signal-threshold-ovs', 'name': 'signal-threshold-ovs', 'id': self.ti.pk})

        traderet = trade_with_signals(self.data, signals)

        return signal_graph, signals, traderet
        

    def train(self):
        cols = []
        params1 = []
        for ii in self.tii.indicator.indicatorinputs.all():
            params1.append(get_input_value(self.tii, ii.parameter))
            cols.append(ii.parameter)

        if len(params1) > 0:
            params1 = prepare_params_for_stoch()

        cols.extend(['ovb', 'ovs', 'Returns%', 'MaxR'])
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
                if pltdt['name'] == 'STCHRSI':
                    pltdt1=pltdt['y']
                    break
            maxv = max(pltdt1)
            minv = min(pltdt1)
            ovba = np.arange((maxv+minv)/2, maxv, (maxv-minv)/20, dtype=int)
            ovsa = np.arange((maxv+minv)/2, minv, -(maxv-minv)/20, dtype=int)

            ovba = np.delete(ovba, 0)
            ovsa = np.delete(ovsa, 0)
            for ovb in ovba:
                for ovs in ovsa:
                    self.stoch = pltdt1

                    signal_graph, signals, traderet = self.trigger(ovb, ovs)
                    if traderet['winlossratio'] is None or traderet['winlossratio'] == np.inf:
                        traderet = 0
                    else:
                        traderet = traderet['winlossratio']

                    parama = argset.copy()
                    parama.extend([ovb, ovs, traderet, ''])
                    pret.loc[ipret] = parama
                    signalsmap[ipret] = signals
                    ipret+=1
        
        retcol = pret['Returns%']
        imax = np.array(retcol).argmax()
        pret.at[imax, 'MaxR'] = 'MR'
        psetb = pret.loc[imax]
        return psetb, pret, signalsmap[imax]