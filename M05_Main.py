
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

from matplotlib import pyplot as plt


#przykład
# x = [1,2,3]
# plt.boxplot(x)
# plt.show()


# df = pd.read_csv('zapat.csv', sep=";")
#
# print(df)




# (134 GB = 140509184 kb)

class Job:
    # Konstruktor Job
    def __init__(self, i, p=1, w=1):
        assert (isinstance(p, int) and p > 0)
        self.i = i  # Identyfikator zadania (np. liczba lub ciąg znaków)
        self.p = p  # Czas wykonywania zadania
        assert (isinstance(w, int) and w > 0)
        self.w = w  # rozmiar zadania

    # Reprezentacja zadania
    def __repr__(self):
        return f"['{self.i}'; p = {self.p}, w = {self.w}]"


class Instance:
    # Konstruktor Instance
    def __init__(self, machines=16):
        self.jobs = []
        self.jobsShuffled = []  # pojemnik tymczasowy na potasowane zadania
        assert (isinstance(machines, int) and machines > 0)
        self.machines = machines

    #odczytuje dane z pliku zapat.csv
    def generateFromCsvFile(self):
        with open('zapat.csv', 'r') as csvfile:
            plots = csv.reader(csvfile, delimiter=';')
            next(plots)  # Pomija nagłówek pliku csv
            for row in plots:
                index = len(self.jobs) + 1
                if int(row[0]) == 0 or int(row[1]) == 0 or int(row[1]) > 140509184: #pomija jeśli zadanie ma czas == 0 lub ram > 134GB
                    continue;
                else:
                    self.jobs.append(Job(f"J{index}", int(row[0]), int(row[1])))

    # tworzy instancje i dodaje joby do pojemnika tymczasowego
    def getInstanceProblem(self):
        half = int(len(self.jobs) / 2)
        for i in range(half):
            self.jobsShuffled.append(self.jobs[i])
            self.jobsShuffled.append(self.jobs[half + i])

        self.jobs.clear()

        for _ in range(5000):
            rand = random.randint(1, len(self.jobsShuffled)) #losowo wybiera 5000 zadań
            self.jobs.append(self.jobsShuffled[rand])
            self.jobsShuffled.remove(self.jobsShuffled[rand])


class Schedule:
    # Konstruktor Schedule
    def __init__(self, i):
        assert(isinstance(i, Instance))
        self.instance = i
        self.assignments = []

    # Maksymalny czas zakończenia
    def cmax(self):
        assert self.isFeasible() == True
        return max(map(lambda x: x.complete, self.assignments))

    # Suma czasów zakończenia zadań
    def csum(self):
        assert self.isFeasible() == True
        listaZadan = self.assignments
        zbiorZadan = set(map(lambda x: x.job.i, self.assignments))
        listaId = list(zbiorZadan)
        a = len(listaId)
        csum = 0
        for i in range(0, a):
            lista = set(filter(lambda x: x.job.i == listaId[i], listaZadan))
            value = max(map(lambda x: x.complete, lista))
            csum = csum + value
        return csum

    # Ważona suma czasów zakończenia zadań
    def cwsum(self):
        assert self.isFeasible() == True
        listaZadan = self.assignments
        zbiorZadan = set(map(lambda x: x.job.i, self.assignments))
        listaId = list(zbiorZadan)
        a = len(listaId)
        cwsum = 0
        for i in range(0, a):
            lista = set(filter(lambda x: x.job.i == listaId[i], listaZadan))
            maxwaga = max(map(lambda x: x.job.w, lista))
            maxValue = max(map(lambda x: x.complete, lista))
            value = maxwaga * maxValue
            cwsum = cwsum + value
        return cwsum


    # Sprawdzanie poprawności szeregowania
    def isFeasible(self):

        # Lista zadan
        listaZadan = self.assignments
        n = len(listaZadan)


        # Zadania z instancji
        instacjaJobs = self.instance.jobs
        a = len(instacjaJobs)

        # W danej chwili, na danym procesorze, wykonuje się co najwyżej jedno zadanie.
        for i in range(0, n - 1):
            for j in range(i + 1, n):
                if listaZadan[i].machine == listaZadan[j].machine:
                    zakres = range(listaZadan[i].start + 1, listaZadan[i].complete)
                    if listaZadan[j].start in zakres or listaZadan[j].complete in zakres:
                        return False

        # Dwie operacje w ramach tego samego zadania wykonują się jednocześnie na obu procesorach
        for i in range(0, n - 1):
            for j in range(i + 1, n):
                if listaZadan[i].job.i == listaZadan[j].job.i:
                    if listaZadan[i].machine != listaZadan[j].machine:
                        zakres = range(listaZadan[i].start + 1, listaZadan[i].complete)
                        if listaZadan[j].start in zakres or listaZadan[j].complete in zakres:
                            return False


        # Sprawdza czy każde zadanie zostało wykonane we właściwym czasie
        for i in listaZadan:
            czas = 0
            for j in listaZadan:
                if i.job == j.job:
                    czas += j.complete - j.start
            if czas != i.job.p:
                return False

        # W uszeregowaniu znajduje się zadanie, które nie jest częścią instancji
        for i in range(0, n):
            przypisane = False
            for j in range(0, a):
                if listaZadan[i].job == instacjaJobs[j]:
                    przypisane = True
                    break
            if przypisane == False:
                return False

        return True


class JobAssignment:
    # Konstruktor JobAssignment
    def __init__(self, j, m, s, c):
        assert (isinstance(j, Job))
        assert (isinstance(m, int) and m > 0)
        assert (isinstance(s, int) and s >= 0)
        assert (isinstance(c, int) and c > s)
        self.job = j  # Zadanie
        self.machine = m  # Procesor, na którym zadanie się wykonuje
        self.start = s  # Czas rozpoczęcia zadania
        self.complete = c  # Czas zakończenia zadania

    # Reprezentacja przydziału zadania do procesora
    def __repr__(self):
        return f"{self.job} ~ P{self.machine}[{self.start}; {self.complete})"


def RND(instance):
    # instance = deepcopy(instance)
    schedule = Schedule(instance)

    cores = schedule.instance.machines # 16 rdzeni
    machines = [0] * cores  # tworzenie macierzy z 16 rdzeniami

    for job in schedule.instance.jobs:
        core = 0  # wybrany rdzeń

        for machine in range(0, cores):  # szuka rdzenia, który wykona zadanie najszybciej
            if machines[machine] < machines[core]:
                core = machine

        machine = core + 1  # indeksujemy rdzenie od 1
        start = machines[core]
        complete = machines[core] + job.p

        schedule.assignments.append(JobAssignment(job, machine, start, complete)) # dodanei zadania do szeregowania

        machines[core] += job.p
    return schedule



random.seed(1234567890) #losowść
instanceProblem = Instance()
instanceProblem.generateFromCsvFile()
instanceProblem.getInstanceProblem()


scheduleRDN = RND(instanceProblem)
assert scheduleRDN.isFeasible() == True
# print("maksymalny czas zakończenia", scheduleRDN.cmax())
# print("suma czasów zakończenia zadań", scheduleRDN.csum())
# print("ważona suma czasów zakończenia zadań", scheduleRDN.cwsum())

for i in scheduleRDN.assignments:
    print(i)