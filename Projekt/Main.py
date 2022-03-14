import pandas as pd
from time import process_time
from Pliki import Operacje

from Pliki.Szeregowania import RND
from Pliki.Szeregowania import LMR
from Pliki.Szeregowania import HMR
from Pliki.Szeregowania import LPT


from Pliki.Szeregowania import ALFA
from Pliki.Szeregowania import BETA

df = pd.read_csv('./zapat.csv', sep=';')
df = df[(df['Memory requirement (KB per CPU)'] > 0) & (df['Memory requirement (KB per CPU)'] <= 140509184) & (df['Processing time (s)'] > 0)]

NUM_OF_INSTANCES = 15 # 30
NUM_OF_MACHINES  = 16 # 3 # 16
NUM_OF_SAMPLE    = 100 # 5000

instances = Operacje.generateInstances(df, NUM_OF_INSTANCES, NUM_OF_MACHINES, NUM_OF_SAMPLE)

CMAXES = {
  'HMR': [],
  'LMR': [],
  'LPT': [],
  'RND': [],
  'ALFA': [],
  'BETA': [],
}
print('start')
n = 0
t1_start = process_time()
for instance in instances:
  CMAXES['HMR'].append(HMR(instance).cmax() / instance.bound())
  n += 1
  print(n)
  CMAXES['LMR'].append(LMR(instance).cmax() / instance.bound())
  n += 1
  print(n)
  CMAXES['LPT'].append(LPT(instance).cmax() / instance.bound())
  n += 1
  print(n)
  CMAXES['RND'].append(RND(instance).cmax() / instance.bound())
  n += 1
  print(n)
  CMAXES['ALFA'].append(ALFA(instance).cmax() / instance.bound())
  n += 1
  print(n)
  CMAXES['BETA'].append(BETA(instance).cmax() / instance.bound())
  n += 1
  print(n)

print(CMAXES)
print('It took: ', process_time() - t1_start)

Operacje.generateBoxPlot(CMAXES, 'Czas wykonania algorytmow', 'Pliki/wykresy/box_work.png')

