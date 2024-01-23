import sys
sys.path.append('../')
from tools.periodic_table_trend import PeriodicTablePlotter
import json

ptp = PeriodicTablePlotter()

ptp.initialize()


with open('test_dist.json') as json_file:
    test_dist_dict = json.load(json_file)

ptp.get_plot(test_dist_dict)
ptp.save_plot('test.png')