import bt
import pandas as pd
from datetime import datetime
from hyperopt import hp, fmin, tpe, Trials
import sys
import dill as pickle
import numpy as np

def pickStrategy(strategyCollection,id="1"):
    strategy_data = strategyCollection.find_one({'id' : str(1)})
    strategy = pickle.loads(strategy_data['function'])
    strategy_space = pickle.loads(strategy_data['hyperopt'])
    return strategy, strategy_space

def Objective(strategie,dbPair,since, until,com):
    def lossFunction(params):
        signals = strategie(params,dbPair,since, until)
        data, weighTarget = signals[['price']], signals[['weights']]
        data.columns = weighTarget.columns = ['a']
        commission = lambda quantity, price: abs(price * quantity * com) #0.0026
        strategy = bt.Strategy('loss_Function_strategy', [bt.algos.WeighTarget(weighTarget),bt.algos.Rebalance()])
        BT = bt.Backtest(strategy, data, integer_positions=False, commissions=commission)
        result = bt.run(BT)
        return result.prices.iloc[-1,0]
    
    def objective(params):
        score = lossFunction(params) 
        loss = 1 / score
        return loss
    
    return objective

def searchBestParams(strategy,strategy_space,db_trades, pair,since,until,commission,max_evals):
    trials = Trials()
    best = fmin(fn=Objective(strategy,db_trades[pair], since,until,commission),space=strategy_space, max_evals=max_evals, rstate=np.random.RandomState(42), algo=tpe.suggest, trials = trials)
    print(min(trials.losses()))
    return best, min(trials.losses())

def storeBestParams(db_best, params, loss, pair, strategy_id, since,until, commission, max_evals):
    db_best.insert_one({
        'params':params, 
        "loss" :loss, 
        "strategy_id" :strategy_id, 
        "pair":pair, 
        "since" : since, 
        "until" : until, 
        "commission" : commission, 
        "max_evals":max_evals ,
        'time':datetime.timestamp(datetime.now())
    })

def searchAndStoreBestArgs(db, db_trades, strategy_id, pair, since, until, commission, max_evals):
    strategy, strategy_space = pickStrategy(db.strategy,id=str(strategy_id))
    best, loss = searchBestParams(strategy,strategy_space, db_trades, pair,since,until,commission,max_evals)
    print("best args : ", best )
    print("loss : ", loss )
    storeBestParams(db.best, best, loss, pair, strategy_id, since, until, commission, max_evals)
