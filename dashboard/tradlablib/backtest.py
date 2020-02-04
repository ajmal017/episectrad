from . import technicalindicator as tind

from .model_guilib import *
from .model_stats import *
from .exec_trade import *
from .model_train import *

from dashboard import models
from .tradlablib.libind.indicators import *

    
def get_backtest_results_for_tradei(df, trade):
    # if trade.backtest_mode == 0:       # traditional
    #     tii = trade.tradeindicatorindicator_set.filter(traditional=1).first()
        
    #     pargs = []
    #     for ii in tii.indicator.indicatorinputs.all():
    #         value = get_input_value(tii, ii.parameter)
    #         pargs.append(value)
    #     trade_fn = globals()['trade_with_' + tii.indicator.id_letter]
    #     sigtype, stopsig, trendsig, bssig = trade_fn(df, *pargs, True)
        
    # elif trade.backtest_mode == 1:     # threshold
    #     tipt = models.TradeIndicatorPlotThreshold.objects.filter(trade_indicator_indicator__trade_indicator = trade).first()
    #     tii = tipt.trade_indicator_indicator
    #     graphdata = tind.display_indicator(df, tii.indicator.name, tii)

    #     pargs = []
    #     for pltdt in graphdata:
    #         if pltdt['name'] == tipt.plot.plotname:
    #             pargs = [pltdt['y'], tipt.threshold_b, tipt.threshold_s]
    #             break

    #     bsrets, sigtype, stopsig, trendsig, bssig = trade_with_threshold(df, *pargs, True)

    # elif trade.backtest_mode == 2:     # cross2
    #     tic2 = models.TradeIndicatorCross2.objects.filter(trade_indicator_indicator1__trade_indicator = trade).first()
    #     tii1 = tic2.trade_indicator_indicator1
    #     tii2 = tic2.trade_indicator_indicator2
    #     graphdata1 = tind.display_indicator(df, tii1.indicator.name, tii1)

    #     dfnew = df.copy()
    #     for pltdt in graphdata1:
    #         dfnew[pltdt['name']] = pltdt['y']

    #     graphdata2 = tind.display_indicator(dfnew, tii2.indicator.name, tii2)

    #     pargs = []
    #     for pltdt in graphdata1:
    #         if pltdt['name'] == tic2.chart_plot1.plotname:
    #             pargs.append(pltdt['y'])
    #             break
        
    #     for pltdt in graphdata2:
    #         if pltdt['name'] == tic2.chart_plot2.plotname:
    #             pargs.append(pltdt['y'])
    #             break

    #     bsrets, sigtype, stopsig, trendsig, bssig = trade_with_cross2(df, *pargs, True)

    # elif trade.backtest_mode == 3:     # crossv
    #     ticv = models.TradeIndicatorCrossv.objects.filter(trade_indicator_indicator__trade_indicator = trade).first()
    #     tii = ticv.trade_indicator_indicator
    #     graphdata = tind.display_indicator(df, tii.indicator.name, tii)

    #     pargs = []
    #     for pltdt in graphdata:
    #         if pltdt['name'] == ticv.chart_plot.plotname:
    #             pargs.append(pltdt['y'])
    #             break
        
    #     bsrets, sigtype, stopsig, trendsig, bssig = trade_with_crossv(df, *pargs, True)

        

    ti = trade
    tii = ti.tradeindicatorindicator_set.first()
    indicator_letter = tii.indicator.id_letter

    if tii.indicator.value_indicator == 1:
        tipt = models.TradeIndicatorPlotThreshold.objects.filter(trade_indicator_indicator__trade_indicator = ti).first()

    if indicator_letter=='acc':
        ind = acc.AccumulationDistribution(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger()
    elif indicator_letter=='adr':
        ind = adr.AdvanceDeclineRatio(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger(tipt.threshold_b, tipt.threshold_s)
    elif indicator_letter=='aroon':
        ind = aroon.Aroon(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger(tipt.threshold_b, tipt.threshold_s)
    elif indicator_letter=='bop':
        ind = bop.BalanceOfPower(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger(tipt.threshold_b, tipt.threshold_s)
    elif indicator_letter=='alma':
        ind = alma.ArnaudLegouxMovingAverage(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger()
    elif indicator_letter=='bb_pb':
        ind = bb_pb.BollingerBandsPB(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger(tipt.threshold_b, tipt.threshold_s)
    elif indicator_letter=='bb_bw':
        ind = bb_bw.BollingerBandsBW(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger(tipt.threshold_b, tipt.threshold_s)
    elif indicator_letter=='co':
        ind = co.ChaikinOscillator(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger(tipt.threshold_b, tipt.threshold_s)
    elif indicator_letter=='cks':
        ind = cks.ChandeKrollStop(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger()
    elif indicator_letter=='cmo':
        ind = cmo.ChandeMomentumOscillator(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger(tipt.threshold_b, tipt.threshold_s)
    elif indicator_letter=='chop':
        ind = chop.ChoppinessIndex(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger(tipt.threshold_b, tipt.threshold_s)
    elif indicator_letter=='cci':
        ind = cci.CommodityChannelIndex(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger(tipt.threshold_b, tipt.threshold_s)
    elif indicator_letter=='cc':
        ind = cc.CoppockCurve(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger()
    elif indicator_letter=='dmi':
        ind = dmi.DirectionalMovementIndex(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger()
    elif indicator_letter=='eom':
        ind = eom.EaseOfMovement(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger(tipt.threshold_b, tipt.threshold_s)
    elif indicator_letter=='efi':
        ind = efi.ElderForceIndex(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger()
    elif indicator_letter=='fish':
        ind = fish.Fisher(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger(tipt.threshold_b, tipt.threshold_s)
    elif indicator_letter=='hv':
        ind = hv.HistoricalVolatility(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger(tipt.threshold_b, tipt.threshold_s)
    elif indicator_letter=='hma':
        ind = hma.HullMA(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger()
    elif indicator_letter=='ic':
        ind = ic.IchimokuCloud(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger()
    elif indicator_letter=='kst':
        ind = kst.KnowSureThingOscillator(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger()
    elif indicator_letter=='lsma':
        ind = lsma.LeastSquaresMovingAverage(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger()
    elif indicator_letter=='macross':
        ind = macross.MaCross(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger()
    elif indicator_letter=='macd':
        ind = macd.MACD(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger()
    elif indicator_letter=='mi':
        ind = mi.MassIndex(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger(tipt.threshold_b, tipt.threshold_s)
    elif indicator_letter=='md':
        ind = md.McGinleyDynamic(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger()
    elif indicator_letter=='mom':
        ind = mom.Momentum(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger()
    elif indicator_letter=='mfi':
        ind = mfi.MoneyFlowIndex(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger(tipt.threshold_b, tipt.threshold_s)
    elif indicator_letter=='ema':
        ind = ema.ExponentialMovingAverage(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger()
    elif indicator_letter=='sma':
        ind = sma.SimpleMovingAverage(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger()
    elif indicator_letter=='wma':
        ind = wma.WeightedMovingAverage(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger()
    elif indicator_letter=='obv':
        ind = obv.OnBalanceVolume(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger(tipt.threshold_b, tipt.threshold_s)
    elif indicator_letter=='psar':
        ind = psar.ParabolicSAR(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger()
    elif indicator_letter=='po':
        ind = po.PriceOscillator(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger()
    elif indicator_letter=='pvt':
        ind = pvt.PriceVolumeTrend(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger()
    elif indicator_letter=='rsi':
        ind = rsi.RelativeStrengthIndex(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger(tipt.threshold_b, tipt.threshold_s)
    elif indicator_letter=='rvgi':
        ind = rvgi.RelativeVigorIndex(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger(tipt.threshold_b, tipt.threshold_s)
    elif indicator_letter=='rvi':
        ind = rvi.RelativeVolatilityIndex(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger(tipt.threshold_b, tipt.threshold_s)
    elif indicator_letter=='smi':
        ind = smi.SMIErgodicOscillator(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger()
    elif indicator_letter=='smma':
        ind = smma.SmoothedMovingAverage(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger()
    elif indicator_letter=='stoch':
        ind = stoch.Stochastic(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger(tipt.threshold_b, tipt.threshold_s)
    elif indicator_letter=='stchrsi':
        ind = stchrsi.StochasticRSI(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger(tipt.threshold_b, tipt.threshold_s)
    elif indicator_letter=='trix':
        ind = trix.Trix(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger()
    elif indicator_letter=='tema':
        ind = tema.TripleEMA(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger()
    elif indicator_letter=='tsi':
        ind = tsi.TrueStrengthIndex(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger(tipt.threshold_b, tipt.threshold_s)
    elif indicator_letter=='uo':
        ind = uo.UltimateOscillator(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger(tipt.threshold_b, tipt.threshold_s)
    elif indicator_letter=='vwma':
        ind = vwma.VWMA(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger()
    elif indicator_letter=='volume':
        ind = volume.Volume(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger()
    elif indicator_letter=='vo':
        ind = vo.VolumeOscillator(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger(tipt.threshold_b, tipt.threshold_s)
    elif indicator_letter=='voi':
        ind = voi.VortexIndicator(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger()
    elif indicator_letter=='wpr':
        ind = wpr.WilliamsR(df, tii, ti)
        signal_graph, periods, traderet = ind.trigger(tipt.threshold_b, tipt.threshold_s)

    wlsts, sig, trp = get_wl_stats(df['Close'], bssig, commcrg)

    acts = []
    
    # signals = []    # 0: stop 1: buy 2: sell

    # prev = 0
    # for i in range(len(periods)):
    #     if periods[i] != prev and periods[i] != 0:
    #         start = i
            
    #     prev = periods[i]
    
    for i in range(len(bssig)):
        start = bssig[i]
        end = stopsig[i]
        trend = trendsig[i]
        if (i+sigtype) % 2 == 1:
            buysell = 'BUY'
        else:
            buysell = 'SELL'

        acts.append({'start': start, 'end': end, 'trend': trend, 'buysell': buysell})

    TRet = trp[-1]

    return acts, TRet


def get_backtest_results_for_pattern(df, mode, pattern):
    
    if mode == 1:       # pricebar pattern
        bsrets, sigtype, stopsig, trendsig, bssig = trade_with_pricebarpattern(df, pattern)
    elif mode == 2:     # chart pattern
        bsrets, sigtype, stopsig, trendsig, bssig = trade_with_chartpattern(df, pattern)

    wlsts, sig, trp = get_wl_stats(df['Close'], bssig, commcrg)

    acts = []

    close = df["Close"]
    open = df["Open"]

    for i in range(len(bssig)):
        start = bssig[i]
        end = stopsig[i]
        trend = trendsig[i]
        if close[bssig[i]] >= open[bssig[i]]:
            trend = 1
            buysell = 'BUY'
        else:
            trend = -1
            buysell = 'SELL'

        # if (i+sigtype) % 2 == 1:
        #     buysell = 'BUY'
        # else:
        #     buysell = 'SELL'

        acts.append({'start': start, 'end': end, 'trend': trend, 'buysell': buysell})

    TRet = trp[-1]

    return acts, TRet


def get_backtest_optresults_for_ti(df, trade):
    if trade.backtest_mode == 0:       # traditional
        tii = trade.tradeindicatorindicator_set.filter(traditional=1).first()
        sargs = []
        sargs.append(globals()['train_for_' + tii.indicator.id_letter])
        pargs = []
        for ii in tii.indicator.indicatorinputs.all():
            value = get_input_value(tii, ii.parameter)
            pargs.append(value)
        sargs.append(pargs)
    elif trade.backtest_mode == 1:     # threshold
        tipt = models.TradeIndicatorPlotThreshold.objects.filter(trade_indicator_indicator__trade_indicator = trade).first()
        tii = tipt.trade_indicator_indicator

        sargs = [train_for_threshold]
        pargs = [tii, tipt.plot.plotname]

        sargs.append(pargs)

    elif trade.backtest_mode == 2:     # cross2
        tic2 = models.TradeIndicatorCross2.objects.filter(trade_indicator_indicator1__trade_indicator = trade).first()
        tii1 = tic2.trade_indicator_indicator1
        tii2 = tic2.trade_indicator_indicator2

        sargs = [train_for_cross2]

        pargs = [tii1, tii2, tic2.chart_plot1.plotname, tic2.chart_plot2.plotname]
        sargs.append(pargs)

    elif trade.backtest_mode == 3:     # crossv
        ticv = models.TradeIndicatorCrossv.objects.filter(trade_indicator_indicator__trade_indicator = trade).first()
        tii = ticv.trade_indicator_indicator

        sargs = [train_for_crossv]

        pargs = [tii, ticv.chart_plot.plotname]
        
        sargs.append(pargs)

    psetb, wlsts, acts = get_stats_singleti(df, *sargs)

    return psetb, wlsts, acts


def comboActs(df, master, regular, slave):
    size = len(df['Close'])
    enters = [0]*size
    bssig = [0]*size    # 1: buy, -1:sell

    # calculate Enter 
    for i in range(size):
        if len(master) > 0:     # if master exists?
            masteract = 0
            buy = 0
            sell = 0
            for item in master:
                for act in item['acts']:
                    if i >= act['start'] and i <= act['end']:
                        masteract = 1
                        if act['buysell'] == 'BUY':
                            buy = buy + 1
                        else:
                            sell = sell + 1
                        break

            if buy >= sell:
                bssig[i] = 1
            else:
                bssig[i] = -1
            enters[i] = masteract
        else:
            slaveact = 0
            buy = 0
            sell = 0
            slavactcnt = 0
            for item in slave:
                for act in item['acts']:
                    if i >= act['start'] and i <= act['end']:
                        slavactcnt = slavactcnt + 1
                        if act['buysell'] == 'BUY':
                            buy = buy + 1
                        else:
                            sell = sell + 1
                        break
            if slavactcnt >= len(slave) - 1:
                slaveact = 1
            
            regularact = 0
            regactcnt = 0
            upcnt = 0
            downcnt = 0
            for item in regular:
                for act in item['acts']:
                    if i >= act['start'] and i <= act['end']:
                        regactcnt = regactcnt + 1
                        if act['buysell'] == 'BUY':
                            buy = buy + 1
                        else:
                            sell = sell + 1

                        if act['trend'] == 1:
                            upcnt += 1
                        else:
                            downcnt += 1
                        break
            if len(regular) == regactcnt and (len(regular)==upcnt or len(regular)==downcnt):
                regularact = 1

            if regularact == 1 and slaveact == 1:
                enters[i] = 1
            else:
                enters[i] = 0
            
            if buy >= sell:
                bssig[i] = 1
            else:
                bssig[i] = -1

    exits = [0]*size
    # calculate Exit 
    for i in range(size):
        if len(master) > 0:     # if master exists?
            for item in master:
                cont = 0
                for act in item['acts']:
                    if i >= act['start'] and i <= act['end']:
                        cont = 1
                if cont == 0:
                    exits[i] = 1
                    break
        else:
            slavexit = 0
            upcnt = 0
            downcnt = 0
            slavactcnt = 0
            for item in slave:
                for act in item['acts']:
                    if i >= act['start'] and i <= act['end']:
                        slavactcnt = slavactcnt + 1
                        if act['trend'] == 1:
                            upcnt += 1
                        else:
                            downcnt += 1
                        break
            if slavactcnt <= 1 or (len(regular) != upcnt and len(regular) != downcnt):
                slavexit = 1
            
            regularexit = 0
            regactcnt = 0
            upcnt = 0
            downcnt = 0
            for item in regular:
                for act in item['acts']:
                    if i >= act['start'] and i <= act['end']:
                        regactcnt = regactcnt + 1
                        if act['trend'] == 1:
                            upcnt += 1
                        else:
                            downcnt += 1
                        break
            if regactcnt == 0 or (len(regular)!=upcnt and len(regular)!=downcnt):
                regularexit = 1

            if regularexit == 1 and slavexit == 1:
                exits[i] = 1
            else:
                exits[i] = 0

    acts = np.logical_and(enters, np.logical_not(np.array(exits)))
    acts = np.where(acts==True, 1, acts)

    return acts, bssig


def get_results(df, backtests):

    mat = []
    master = []
    regular = []
    slave = []
    for bt in backtests:
        if bt.mode == 0:
            acts, TRet = get_backtest_results_for_tradei(df, bt.tradeindicator)
        elif bt.mode == 1:
            acts, TRet = get_backtest_results_for_pattern(df, 1, bt.pricebar_pattern)
        elif bt.mode == 2:
            acts, TRet = get_backtest_results_for_pattern(df, 2, bt.chart_pattern)

        item = {'id': bt.id, 'acts': acts, 'attr': bt.attribute}
        mat.append(item)
        if bt.attribute == 1:   # Master
            master.append(item)
        elif bt.attribute == 0:     # Regular
            regular.append(item)
        else:
            slave.append(item)
    
    actmap = dict()
    for item in mat:
        trend = ['white']*len(df['Close'])
        for act in item['acts']:
            index = act['start']
            while index<=act['end']:
                if act['trend'] == 1:
                    trend[index] = 'green'
                elif act['trend'] == -1:
                    trend[index] = 'red'
                index+=1
        actmap[item['id']] = trend

    acts, bssig = comboActs(df, master, regular, slave)

    periods = get_periods(acts)

    result = get_stats(df['Close'], periods, bssig)

    return actmap, result, acts.tolist()


def get_optresults(df, backtests):

    mat = []
    master = []
    regular = []
    slave = []

    bestparams = []

    for bt in backtests:
        if bt.mode == 0:
            psetb, wlsts, acts = get_backtest_optresults_for_ti(df, bt.tradeindicator)
            param = []

            for i,v in psetb.items():
                if i != 'Returns%' and i != 'MaxR':
                    param.append({'parameter':i, 'value':v})

            bestparams.append({'backtest_id': bt.id, 'title': bt.tradeindicator.title(), 'tradeindicator_id': bt.tradeindicator.id, 'params': param })

        elif bt.mode == 1:
            acts, TRet = get_backtest_results_for_pattern(df, 1, bt.pricebar_pattern)
        elif bt.mode == 2:
            acts, TRet = get_backtest_results_for_pattern(df, 2, bt.chart_pattern)

        item = {'id': bt.id, 'acts': acts, 'attr': bt.attribute}
        mat.append(item)
        if bt.attribute == 1:   # Master
            master.append(item)
        elif bt.attribute == 0:     # Regular
            regular.append(item)
        else:
            slave.append(item)
    
    actmap = dict()
    for item in mat:
        trend = ['white']*len(df['Close'])
        for act in item['acts']:
            index = act['start']
            while index<=act['end']:
                if act['trend'] == 1:
                    trend[index] = 'green'
                elif act['trend'] == -1:
                    trend[index] = 'red'
                index+=1
        actmap[item['id']] = trend

    acts, bssig = comboActs(df, master, regular, slave)

    periods = get_periods(acts)

    result = get_stats(df['Close'], periods, bssig)

    return actmap, result, acts.tolist(), bestparams


def ValidateBacktests(backtests):
    invalidbacktests = []
    for bt in backtests:
        if bt.mode == 0:
            if bt.tradeindicator.backtest_mode == 0:       # traditional
                tii = bt.tradeindicator.tradeindicatorindicator_set.filter(traditional=1).first()
                if tii is None:
                    invalidbacktests.append(bt.tradeindicator.title())
            elif bt.tradeindicator.backtest_mode == 1:     # threshold
                tipt = models.TradeIndicatorPlotThreshold.objects.filter(trade_indicator_indicator__trade_indicator = bt.tradeindicator).first()
                if tipt is None:
                    invalidbacktests.append(bt.tradeindicator.title())
            elif bt.tradeindicator.backtest_mode == 2:     # cross2
                tic2 = models.TradeIndicatorCross2.objects.filter(trade_indicator_indicator1__trade_indicator = bt.tradeindicator).first()
                if tic2 is None:
                    invalidbacktests.append(bt.tradeindicator.title())
            elif bt.tradeindicator.backtest_mode == 3:     # crossv
                ticv = models.TradeIndicatorCrossv.objects.filter(trade_indicator_indicator__trade_indicator = bt.tradeindicator).first()
                if ticv is None:
                    invalidbacktests.append(bt.tradeindicator.title())
    
    return invalidbacktests