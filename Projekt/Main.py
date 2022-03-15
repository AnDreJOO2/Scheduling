from time import process_time

from Pliki import Operacje
from Pliki.Szeregowania import ALFA
from Pliki.Szeregowania import BETA
from Pliki.Szeregowania import HMR
from Pliki.Szeregowania import LMR
from Pliki.Szeregowania import LPT
from Pliki.Szeregowania import RND

ILOSC_DANYCH = 5000  # 5000 rekordów
ILOSC_PROCESOROW = 16  # 16 procesorow
ILOSC_INSTANCJI = 30 # 30 instancji na każdy algorytm

df = Operacje.readDataFromCSVFile("./zapat.csv", ";")  # odczyt
instances = Operacje.genNewInstances(df, ILOSC_DANYCH, ILOSC_INSTANCJI, ILOSC_PROCESOROW)  # instancje

Dane = {
    'RND': {'CZAS': [], 'CMAX': []},
    'LMR': {'CZAS': [], 'CMAX': []},
    'HMR': {'CZAS': [], 'CMAX': []},
    'LPT': {'CZAS': [], 'CMAX': []},
    'ALFA': {'CZAS': [], 'CMAX': []},
    'BETA': {'CZAS': [], 'CMAX': []}
}

print("Początek")
print("Ustawione wartości dla każdego algorytmu")
print("   Ilość wczytanych rekordów z pliku zapat.csv:", ILOSC_DANYCH, ", Ilość procesorów:", ILOSC_PROCESOROW,
      ", Ilość instancji", ILOSC_INSTANCJI)

iteracja = 0
ileInstancji = len(instances)
run = process_time()
for instance in instances:
    iteracja = iteracja + 1
    print("Instancja numer:", iteracja, "/", ileInstancji)
    print("   Trwa wykonywanie ...")

    start = process_time()
    i = RND(instance)
    end = process_time()
    Dane['RND']['CZAS'].append(end - start)
    Dane['RND']['CMAX'].append(i.cmax() / instance.check())

    start = process_time()
    i = LMR(instance)
    end = process_time()
    Dane['LMR']['CZAS'].append(end - start)
    Dane['LMR']['CMAX'].append(i.cmax() / instance.check())

    start = process_time()
    i = HMR(instance)
    end = process_time()
    Dane['HMR']['CZAS'].append(end - start)
    Dane['HMR']['CMAX'].append(i.cmax() / instance.check())

    start = process_time()
    i = LPT(instance)
    end = process_time()
    Dane['LPT']['CZAS'].append(end - start)
    Dane['LPT']['CMAX'].append(i.cmax() / instance.check())

    start = process_time()
    i = ALFA(instance)
    end = process_time()
    Dane['ALFA']['CZAS'].append(end - start)
    Dane['ALFA']['CMAX'].append(i.cmax() / instance.check())

    start = process_time()
    i = BETA(instance)
    end = process_time()
    Dane['BETA']['CZAS'].append(end - start)
    Dane['BETA']['CMAX'].append(i.cmax() / instance.check())

print()
print("Generowanie wykresów ...")

Operacje.generateBoxPlot({
    'RND': Dane['RND']['CZAS'],
    'LMR': Dane['LMR']['CZAS'],
    'HMR': Dane['HMR']['CZAS'],
    'LPT': Dane['LPT']['CZAS'],
    'ALFA': Dane['ALFA']['CZAS'],
    'BETA': Dane['BETA']['CZAS']
}, 'Pliki/wykresy/czasy_wykonania_.png',
    'Czasy wykonania algorytmów')  # wykres skrzynkowy dla czasów wykonania algorytmów

Operacje.generateBoxPlot({
    'RND': Dane['RND']['CMAX'],
    'LMR': Dane['LMR']['CMAX'],
    'HMR': Dane['HMR']['CMAX'],
    'LPT': Dane['LPT']['CMAX'],
    'ALFA': Dane['ALFA']['CMAX'],
    'BETA': Dane['BETA']['CMAX']
}, 'Pliki/wykresy/maksymalne_czasy_wykonania.png',
    'Maksymalne czasy wykonania algorytmów')  # wykres skrzynkowy dla czasów wykonania algorytmów

Operacje.generateHistogramPlot(df, "Pliki/wykresy/zużycie_pamięci.png", "Memory requirement (KB per CPU)",
                               "Histogram - zużycie pamięci")
Operacje.generateHistogramPlot(df, "Pliki/wykresy/wymagany_czas.png", "Processing time (s)",
                               "Histogram - wymagany czas")
Operacje.generateScatterPlot(df, "Pliki/wykresy/wykres_punktowy.png", "Memory requirement (KB per CPU)",
                             "Processing time (s)", "Wykres punktowy")

print()
finish = process_time()
print("Czas wykonania całego programu:", finish - run, "s")
print("Wygenerowane wykresy znajdują się w ścieżce: Projekt/Pliki/wykresy/")
print("Koniec")
