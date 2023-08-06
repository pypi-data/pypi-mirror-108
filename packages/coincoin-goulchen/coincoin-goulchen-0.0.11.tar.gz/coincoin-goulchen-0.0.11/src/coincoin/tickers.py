from datetime import datetime
import pandas as pd
import sys
from pymongo import MongoClient, ASCENDING, DESCENDING

def createTickers(collection, since, until, timeRangeSeconds):
    '''
    create tickers from a pymongo collection of trades
    collection : pymongo collection of trades 
    since : "01-01-2019"
    until : same
    timeRangeSeconds = time in seconds (int)
    '''
    since_time_obj = datetime.strptime(since, '%d-%m-%Y')
    since_nanoUnixTime = int(since_time_obj.timestamp()*1e4)
    match = {"time": {"$gt": since_nanoUnixTime}}
    if(until != ''):
      until_time_obj = datetime.strptime(until, '%d-%m-%Y')
      until_nanoUnixTime = int(until_time_obj.timestamp()*1e4)
      match['time']['$lt'] = until_nanoUnixTime
    pipeline = [
            {
                "$match": match
            },
            {
                "$group": {
                    "_id": {"$toInt": {"$divide": ["$time", timeRangeSeconds * 1e3]}},
                    "time": {"$min": "$time"},
                    "open": {"$first": "$price"},
                    "close":{"$last": "$price"},
                    "high":  {"$max": "$price"},
                    "low":  {"$min": "$price"},
                    "volume" : {"$sum":1}
                }
            },
            {
                "$sort": {
                    "time":  ASCENDING,
                }
            },

        ]
    results = collection.aggregate(pipeline, allowDiskUse=True)
    listcur = list(results)
    if len(listcur) == 0:
        return []
    df = pd.DataFrame(listcur).drop(['_id'], axis=1)
    df['Datetime'] = pd.to_datetime((df['time']*100000), unit='ns')
    df.set_index(pd.DatetimeIndex(df['Datetime']), inplace=True)
    df = df.drop(['time','Datetime'], axis=1)
    ope =  df["open"].resample(str(timeRangeSeconds) + 'S').first()
    clos = df["close"].resample( str(timeRangeSeconds) + 'S').last()
    high = df["high"].resample( str(timeRangeSeconds) + 'S').max()
    low = df["low"].resample( str(timeRangeSeconds) + 'S').min()
    volume = df["volume"].resample( str(timeRangeSeconds) + 'S').sum()
    return pd.concat([ope, clos, high, low,volume], axis=1).pad()

class mod_call:
    def __call__(self,collection, since = "01-01-2019", until = '', timeRangeSeconds = 60):
        return createTickers(collection, since, until, timeRangeSeconds)

sys.modules[__name__] = mod_call()
