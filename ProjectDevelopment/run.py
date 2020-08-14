from Signal import Signal
from Evaluation import Evaluation

#File to run signal/evaluation metrics

signal = Signal('1995-01-01', '2000-01-01', '2000-01-02', '2019-12-31')
signal.run_testing()
signal_ret = signal.get_daily_returns()

evaluate = Evaluation()
evaluate.bond_system_v_passive_bonds_quarterly(signal_ret)
evaluate.compare_with_equities_cumulative(signal_ret)