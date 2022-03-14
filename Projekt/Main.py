import pandas as pd
from time import process_time
from Pliki import Operacje

from Pliki.Szeregowania import RND
from Pliki.Szeregowania import LMR
from Pliki.Szeregowania import HMR
from Pliki.Szeregowania import LPT


from Pliki.Szeregowania import ALFA
from Pliki.Szeregowania import BETA

ILOSC_DANYCH = 1500 # 5000 rekordów
ILOSC_PROCESOROW  = 16 # 16 procesorow
ILOSC_INSTANCJI = 10 # 30 instancji na każdy algorytm


df = pd.read_csv('./zapat.csv', sep=';') #wczytanie danych z pliku zapat.csv
df = df[(df['Memory requirement (KB per CPU)'] > 0) & (df['Memory requirement (KB per CPU)'] <= 140509184) & (df['Processing time (s)'] > 0)]

instances = Operacje.genNewInstances(df, ILOSC_DANYCH, ILOSC_INSTANCJI, ILOSC_PROCESOROW) #instancje

DATA = {
  'RND': { 'CZAS': [], 'CMAX': [] },
  'LMR': { 'CZAS': [], 'CMAX': [] },
  'HMR': { 'CZAS': [], 'CMAX': [] },
  'LPT': { 'CZAS': [], 'CMAX': [] },
  'ALFA': { 'CZAS': [], 'CMAX': [] },
  'BETA': { 'CZAS': [], 'CMAX': [] }
}

n = 0
t1_start = process_time()
for instance in instances:

  start = process_time()
  i = RND(instance)
  end = process_time()
  DATA['RND']['CZAS'].append(end - start)
  DATA['RND']['CMAX'].append(i.cmax() / instance.bound())
  n += 1
  print(n)

  start = process_time()
  i = LMR(instance)
  end = process_time()
  DATA['LMR']['CZAS'].append(end - start)
  DATA['LMR']['CMAX'].append(i.cmax() / instance.bound())
  n += 1
  print(n)

  start = process_time()
  i = HMR(instance)
  end = process_time()
  DATA['HMR']['CZAS'].append(end - start)
  DATA['HMR']['CMAX'].append(i.cmax() / instance.bound())
  n += 1
  print(n)

  start = process_time()
  i = LPT(instance)
  end = process_time()
  DATA['LPT']['CZAS'].append(end - start)
  DATA['LPT']['CMAX'].append(i.cmax() / instance.bound())
  n += 1
  print(n)

  start = process_time()
  i = ALFA(instance)
  end = process_time()
  DATA['ALFA']['CZAS'].append(end - start)
  DATA['ALFA']['CMAX'].append(i.cmax() / instance.bound())
  n += 1
  print(n)

  start = process_time()
  i = BETA(instance)
  end = process_time()
  DATA['BETA']['CZAS'].append(end - start)
  DATA['BETA']['CMAX'].append(i.cmax() / instance.bound())
  n += 1
  print(n)

# print(DATA)
# print("RDN czasy: ", DATA['RND']['CZAS'])
# print("RDN cmax: ", DATA['RND']['CMAX'])

Operacje.generateBoxPlot({
  'RND': DATA['RND']['CZAS'],
  'LMR': DATA['LMR']['CZAS'],
  'HMR': DATA['HMR']['CZAS'],
  'LPT': DATA['LPT']['CZAS'],
  'ALFA': DATA['ALFA']['CZAS'],
  'BETA': DATA['BETA']['CZAS']
}, 'Czasy wykonania algorytmów', 'Pliki/wykresy/czasy_wykonania_.png') # wykres skrzynkowy dla czasów wykonania algorytmów

Operacje.generateBoxPlot({
  'RND': DATA['RND']['CMAX'],
  'LMR': DATA['LMR']['CMAX'],
  'HMR': DATA['HMR']['CMAX'],
  'LPT': DATA['LPT']['CMAX'],
  'ALFA': DATA['ALFA']['CMAX'],
  'BETA': DATA['BETA']['CMAX']
}, 'Maksymalne czasy wykonania algorytmów', 'Pliki/wykresy/maksymalne_czasy_wykonania.png') # wykres skrzynkowy dla czasów wykonania algorytmów



