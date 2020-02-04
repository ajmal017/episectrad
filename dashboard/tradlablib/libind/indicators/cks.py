from dashboard.tradlablib.exec_trade import *
from dashboard.tradlablib.model_train import *
from dashboard.tradlablib import technicalindicator as tind
from dashboard.tradlablib import tradelib

class ChandeKrollStop(object):

    def __init__(self, data, tii, ti):
        self.data = data
        self.tii = tii
        self.ti = ti

        graphdata = tind.display_indicator(self.data, self.tii.indicator.name, self.tii)
        for pltdt in graphdata:
            if pltdt['name'] == 'ss':
                self.ss=pltdt['y']
            if pltdt['name'] == 'ls':
                self.ls=pltdt['y']
    
    def trigger(self):
        close = self.data['Close']
        high = self.data['High']
        low = self.data['Low']
        ss = self.ss
        ls = self.ls

        signals_ovbe = []

        signals = []

        signals_ovss = []

        signals_trade_buy = []
        signals_trade_sell = []

        signal_graph = []

        signals = []    # 0: stop 1: buy 2: sell
        prevsig = 0
        signals.append(prevsig)
        for i in range(1, len(close)):
            if (ss[i] > close[i] and ls[i] > close[i]):
                #buy start
                if prevsig != 1:
                    signals_ovbe.append({'x': i, 'y': max(ss[i], ls[i], high[i])})
                prevsig = 1
            elif (ss[i] < close[i] and ls[i] < close[i]):
                #overbought end, sell start
                if prevsig != 2:
                    signals_ovss.append({'x': i, 'y': min(ss[i], ls[i], low[i])})
                prevsig = 2

            if (ss[i-1] > ls[i-1] and ss[i] < ls[i]) or (ss[i-1] < ls[i-1] and ss[i] > ls[i]):
                signals.append(prevsig)
                if prevsig == 1:
                    signals_trade_buy.append({'x': i, 'y': (ss[i] + ls[i])/2})
                elif prevsig == 2:
                    signals_trade_sell.append({'x': i, 'y': (ss[i] + ls[i])/2})
            else:
                signals.append(0)

        signal_graph.append({'data': signals_ovbe, 'type': 'signal-ovbe', 'name': 'signal-ovbe', 'id': 'main'})
        signal_graph.append({'data': signals_ovss, 'type': 'signal-ovss', 'name': 'signal-ovss', 'id': 'main'})
        signal_graph.append({'data': signals_trade_buy, 'type': 'signal-trade-buy', 'name': 'signal-trade-buy', 'id': 'main'})
        signal_graph.append({'data': signals_trade_sell, 'type': 'signal-trade-sell', 'name': 'signal-trade-sell', 'id': 'main'})


        traderet = trade_with_signals(self.data, signals)

        return signal_graph, signals, traderet
        

    def train(self):
        cols = []
        params1 = []
        for ii in self.tii.indicator.indicatorinputs.all():
            params1.append(get_input_value(self.tii, ii.parameter))
            cols.append(ii.parameter)

        if len(params1) > 0:
            params1 = prepare_params_for_adr(*params1)

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
                if pltdt['name'] == 'adr':
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
                    self.adr = pltdt1

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