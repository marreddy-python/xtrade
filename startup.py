from market_simulator import MarketSimulator,DataLoader,MarketDAOImpl,AmeritradeAdapter,SMAPreprocessor,SMADAOImpl,HighChartsAdapter
from params_config import config
import sys
sys.dont_write_bytecode=True


def main():
    
    stockSymbols = config['stockSymbols']
    strategyTypes = config['strategyType'] 

    preprocessors = []

    simulator = MarketSimulator()

    for i in range(len(strategyTypes)):
        if strategyTypes[i] == 'sma':
            if config['chartingTool'] == 'HighCharts':
                preprocessors.append('SMAPreprocessor(HighChartsAdapter)')

    simulator.loadSymbols(stockSymbols)
    simulator.loadStrategyTypes(preprocessors)


    if config['database'] == 'POSTGRESQL':
        simulator.setMarketDAO('PostgreMarketDAO')
    else:
        print('build_failed')


    if config['provider'] == 'Ameritrade':
        simulator.setReader('HighChartsAdapter')
    else:
        print('build_failed')


    simulator.run()








 
    