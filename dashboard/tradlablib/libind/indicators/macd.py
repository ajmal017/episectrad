from dashboard.tradlablib.exec_trade import *
from dashboard.tradlablib.model_train import *
from dashboard.tradlablib import technicalindicator as tind
from dashboard.tradlablib import tradelib

class MACD(object):

    def __init__(self, data, tii, ti):
        self.data = data
        self.tii = tii
        self.ti = ti

        graphdata = tind.display_indicator(self.data, self.tii.indicator.name, self.tii)
        self.ma1 = graphdata[0]['y']
        self.ma2 = graphdata[1]['y']
    
    def trigger(self):
        close = self.data['Close']
        ma1 = self.ma1
        ma2 = self.ma2

        signals = []

        signals_trade_buy = []
        signals_trade_sell = []

        signal_graph = []

        signals = []    # 0: stop 1: buy 2: sell
        prevsig = 0
        signals.append(prevsig)
        for i in range(1, len(close)):
            if ma1[i-1] < ma2[i-1] and ma1[i] > ma2[i]:
                #sell start
                if prevsig != 1:
                    signals_trade_sell.append({'x': i, 'y': (ma1[i] + ma2[i])/2})
                prevsig = 1
            elif ma1[i-1] > ma2[i-1] and ma1[i] < ma2[i]:
                #overbought end, sell start
                if prevsig != 2:
                    signals_trade_buy.append({'x': i, 'y': (ma1[i] + ma2[i])/2})
                prevsig = 2

            signals.append(prevsig)

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
            params1 = prepare_params_for_macd()

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
            self.ma1 = graphdata[0]['y']
            self.ma2 = graphdata[1]['y']

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