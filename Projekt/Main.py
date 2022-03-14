import pandas as pd
from time import process_time
from Pliki import Operacje

from Pliki.Szeregowania import RND
from Pliki.Szeregowania import LMR
from Pliki.Szeregowania import HMR
from Pliki.Szeregowania import LPT


from Pliki.Szeregowania import ALFA
from Pliki.Szeregowania import BETA

ILOSC_DANYCH = 100 # 5000 rekordów
ILOSC_PROCESOROW  = 16 # 16 procesorow
ILOSC_INSTANCJI = 15 # 15 instancji na każdy algorytm


df = pd.read_csv('./zapat.csv', sep=';') #wczytanie danych z pliku zapat.csv
df = df[(df['Memory requirement (KB per CPU)'] > 0) & (df['Memory requirement (KB per CPU)'] <= 140509184) & (df['Processing time (s)'] > 0)]

instances = Operacje.genNewInstances(df, ILOSC_DANYCH, ILOSC_INSTANCJI, ILOSC_PROCESOROW) #instancje

CMAXES = {
  'RND': [],
  'LMR': [],
  'HMR': [],
  'LPT': [],
  'ALFA': [],
  'BETA': [],
}
print('start')
n = 0
t1_start = process_time()
for instance in instances:

  CMAXES['RND'].append(RND(instance).cmax() / instance.bound())
  n += 1
  print(n)

  CMAXES['LMR'].append(LMR(instance).cmax() / instance.bound())
  n += 1
  print(n)

  CMAXES['HMR'].append(HMR(instance).cmax() / instance.bound())
  n += 1
  print(n)

  CMAXES['LPT'].append(LPT(instance).cmax() / instance.bound())
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


Operacje.generateBoxPlot(CMAXES, 'Czasy wykonania algorytmów', 'Pliki/wykresy/wykres_skrzynkowy.png')


