#DATADAO
def get_dd():
    from datadao import DataDAO
    DD = DataDAO()
    return DD

#DATASERVICE
def get_ds():
    from service import DataService
    DS = DataService()
    return DS

#STRATEGYSERVICE
def get_ss():
    from service import StrategyService
    SS = StrategyService()
    return SS

#STRATEGYDAO 
def get_sd():
    from strategydao import StrategyDAO,SMAStrategyProcessor
    SD = StrategyDAO()
    return SD

#SMAStrategyProcessor
def get_smastprsr():
    from strategydao import SMAStrategyProcessor
    SMASP = SMAStrategyProcessor()
    return SMASP
