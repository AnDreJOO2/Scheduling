
# Wprowadzenie
# MetaCentrum Czech National Grid zarządza trzydziestoma dwoma klastrami obliczeniowymi. Operatorzy MetaCentrum monitorowali,
# w okresie od stycznia 2013 roku do kwietnia 2015 roku, parametry wszystkich zadań wykonywanych na tych klastrach. Pełen zestaw zebranych danych,
# w formacie swf, można pobrać tutaj. Opis struktury pobranego pliku swf można natomiast znaleźć tutaj.
#
# Jednym z klastrów utrzymywanych przez MetaCentrum jest klaster Zapat, zbudowany ze 112 węzłów, z których każdy wyposażony jest w 16 rdzeni
# CPU oraz 134 GB pamięci RAM. W pliku zapat.csv zebrano częściowe wyniki dotyczące zadań realizowanych w tym klastrze. Obejmują one jedynie
# wycinek oryginalnych danych, tzn. czas (w sekundach) oraz ilość pamięci RAM (w KB na rdzeń), jakie zostały przydzielone zadaniu. W pełnym obrazie,
# występuje tu także trzeci wymiar --- liczba rdzeni procesora przydzielonych zadaniu: od 1 do 16. Ten wymiar jednak zignorujemy i w dalszej części modułu
# będziemy zakładać, że każdemu zadaniu przydzielono dokładnie jeden rdzeń CPU.
#
# Każdy wiersz w pliku zapat.csv (z wyjątkiem pierwszego) opisuje więc jedno zadanie, które wymaga dokładnie jednego rdzenia przez wskazaną ilość czasu oraz
# dokładnie tyle pamięci operacyjnej, ile wskazano. Zadania realizowane w klastrach obliczeniowych są, co do zasady, niepodzielne.


# Pełen zestaw zebranych danych, w formacie swf, można pobrać tutaj.
# https://www.cs.huji.ac.il/labs/parallel/workload/l_metacentrum2/index.html

# Opis struktury pobranego pliku swf można natomiast znaleźć tutaj.
# https://www.cs.huji.ac.il/labs/parallel/workload/swf.html


import pandas as pd
import random
import csv

# df = pd.read_csv('zapat.csv', sep=";")
#
# print(df)




# (134 GB = 140509184 kb)

class Job:
    # Konstruktor
    def init(self, i, p=1, w=1):
        assert(isinstance(p, int) and p > 0)
        self.i = i # Identyfikator zadania (np. liczba lub ciąg znaków)
        self.p = p # Czas wykonywania zadania
        assert(isinstance(w, int) and w > 0)
        self.w = w # rozmiar zadania

    # Reprezentacja zadania
    def repr(self):
        return f"['{self.i}'; p = {self.p}, w = {self.w}]"

class Instance:
    def init(self, machines=1):
        self.jobs = []
        self.jobsShuffled = [] # pojemnik tymczasowy na potasowane zadania
        assert(isinstance(machines, int) and machines > 0)
        self.machines = machines

    def generateFromCsvFile(self):
        with open('zapat.csv','r') as csvfile:
            plots = csv.reader(csvfile, delimiter = ';')
            next(plots)
            for row in plots:
                index = len(self.jobs) + 1
                if int(row[0]) == 0 or int(row[1]) == 0 or int(row[1]) > 140509184:
                    continue;
                else:
                    self.jobs.append(Job(f"J{index}", int(row[0]), int(row[1])))

    def getInstanceProblem(self):
        half = int(len(self.jobs)/2)
        for i in range(half):
            self.jobsShuffled.append(self.jobs[i])
            self.jobsShuffled.append(self.jobs[half + i])

        self.jobs.clear()

        for _ in range(5000):
            rand = random.randint(1,len(self.jobsShuffled))
            self.jobs.append(self.jobsShuffled[rand])
            self.jobsShuffled.remove(self.jobsShuffled[rand])

random.seed(1234567890)
instanceProblem = Instance()
instanceProblem.generateFromCsvFile()
instanceProblem.getInstanceProblem()