from dashboard.tradlablib.exec_trade import *
from dashboard.tradlablib.model_train import *
from dashboard.tradlablib import technicalindicator as tind
from dashboard.tradlablib import tradelib

class ParabolicSAR(object):

    def __init__(self, data, tii, ti):
        self.data = data
        self.tii = tii
        self.ti = ti

        graphdata = tind.display_indicator(self.data, self.tii.indicator.name, self.tii)
        for pltdt in graphdata:
            if pltdt['name'] == 'psar':
                self.psar=pltdt['y']
            if pltdt['name'] == 'psarbull':
                self.psarbull=pltdt['y']
            if pltdt['name'] == 'psarbear':
                self.psarbear=pltdt['y']

    
    def trigger(self):
        psar = self.psar
        psarbull = self.psarbull
        psarbear = self.psarbear

        signals_ovbs = []

        signals_ovbe = []

        signals_ovss = []

        signals_ovse = []

        signal_graph = []

        signals = []    # 0: stop 1: buy 2: sell
        prevsig = 0
        for i in range(len(psar)):
            if psarbull[i] != 0.0:
                if prevsig != 1:
                    signals_ovss.append({'x': i, 'y': psarbull[i]})
                prevsig = 1
            elif psarbear[i] != 0.0:
                if prevsig != 2:
                    signals_ovbe.append({'x': i, 'y': psarbear[i]})
                prevsig = 2
            else:
                if prevsig == 1:
                    signals_ovse.append({'x': i, 'y': psar[i]})
                if prevsig == 2:
                    signals_ovbs.append({'x': i, 'y': psar[i]})

                prevsig = 0

            signals.append(prevsig)

        signal_graph.append({'data': signals_ovbs, 'type': 'signal-ovbs', 'name': 'signal-ovbs', 'id': 'main'})
        signal_graph.append({'data': signals_ovbe, 'type': 'signal-ovbe', 'name': 'signal-ovbe', 'id': 'main'})
        signal_graph.append({'data': signals_ovss, 'type': 'signal-ovss', 'name': 'signal-ovss', 'id': 'main'})
        signal_graph.append({'data': signals_ovse, 'type': 'signal-ovse', 'name': 'signal-ovse', 'id': 'main'})

        traderet = trade_with_signals(self.data, signals)

        return signal_graph, signals, traderet
        

    def train(self):
        cols = []
        params1 = []
        for ii in self.tii.indicator.indicatorinputs.all():
            params1.append(get_input_value(self.tii, ii.parameter))
            cols.append(ii.parameter)

        if len(params1) > 0:
            params1 = prepare_params_for_psar(*params1)

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
                if pltdt['name'] == 'psar':
                    self.psar=pltdt['y']
                if pltdt['name'] == 'psarbull':
                    self.psarbull=pltdt['y']
                if pltdt['name'] == 'psarbear':
                    self.psarbear=pltdt['y']


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