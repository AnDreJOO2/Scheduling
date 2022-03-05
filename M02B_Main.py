class Job:
    # Konstruktor
    def __init__(self, i, p=1, w=1):
        assert (isinstance(p, int) and p > 0)
        self.i = i  # Identyfikator zadania (np. liczba lub ciąg znaków)
        self.p = p  # Czas wykonywania zadania
        assert (isinstance(w, int) and w > 0)
        self.w = w  # Waga zadania

    # Reprezentacja zadania
    def __repr__(self):
        return f"['{self.i}'; p = {self.p}, w = {self.w}]"


import random


class Instance:
    def __init__(self):
        self.jobs = []

    def generate(self, n, pmin=1, pmax=1):
        for i in range(1, n + 1):
            self.jobs.append(Job("J" + str(len(self.jobs) + 1), random.randint(pmin, pmax)))


class JobAssignment:
    # Konstruktor
    def __init__(self, j, s, c):
        assert (isinstance(j, Job))
        assert (isinstance(s, int) and s >= 0)
        assert (isinstance(c, int) and c > s)
        self.job = j  # Zadanie
        self.start = s  # Czas rozpoczęcia zadania
        self.complete = c  # Czas zakończenia zadania

    # Reprezentacja przydziału zadania do procesora
    def __repr__(self):
        return f"{self.job} ~ [{self.start}; {self.complete})"


class Schedule:
    # Konstruktor
    def __init__(self, i):
        assert (isinstance(i, Instance))
        self.instance = i
        self.assignments = []

    ###############################
    # WERYFIKACJA DOPUSZCZALNOŚCI #
    ###############################

    def isFeasible(self):
        if (len(self.instance.jobs) != len(self.assignments)):
            return False

        # Każde zadanie zostało przydzielone dokładnie raz
        for j in self.instance.jobs:
            assigned = 0
            for a in self.assignments:
                if j == a.job:
                    assigned += 1
            if assigned != 1:
                return False

        # Każdy przydział dotyczy istniejącego zadania
        for a in self.assignments:
            assigned = False
            for j in self.instance.jobs:
                if j == a.job:
                    assigned = True
                    break
            if assigned == False:
                return False

        # Każde zadanie wykonuje się dokładnie tyle ile powinno
        for a in self.assignments:
            if a.complete - a.start != a.job.p:
                return False

        # W danej chwili wykonuje się co najwyżej jedno zadanie
        for a in self.assignments:
            for aa in self.assignments:
                if a.job != aa.job:
                    if max(a.start, aa.start) < min(a.complete, aa.complete):
                        return False

        return True

    ################
    # FUNKCJE CELU #
    ################

    def cmax(self):
        assert self.isFeasible() == True
        return max(map(lambda x: x.complete, self.assignments))

    def csum(self):
        assert self.isFeasible() == True
        return sum(map(lambda x: x.complete, self.assignments))

    def cwsum(self):
        assert self.isFeasible() == True
        return sum(map(lambda x: x.complete * x.job.w, self.assignments))


from copy import deepcopy


def SPT(instance):
    instance = deepcopy(instance)
    schedule = Schedule(instance)
    schedule.instance.jobs.sort(key=lambda x: x.p)

    s = 0
    for j in schedule.instance.jobs:
        schedule.assignments.append(JobAssignment(j, s, s + j.p))
        s += j.p

    return schedule


def WSPT(instance):
    instance = deepcopy(instance)
    schedule = Schedule(instance)
    schedule.instance.jobs.sort(key=lambda x: x.p / x.w)

    s = 0
    for j in schedule.instance.jobs:
        schedule.assignments.append(JobAssignment(j, s, s + j.p))
        s += j.p

    return schedule


class Job(Job):
    # Konstruktor
    def __init__(self, i, p=1, w=1, r=0, d=0):
        super().__init__(i, p, w)
        assert (isinstance(r, int))
        self.r = r  # Czas gotowości zadania (domyślnie 0), może być też wartością ujemną
        assert (isinstance(d, int))
        self.d = d  # Pożądany czas zakończenia zadania (domyślnie 0), może być też wartością ujemną

    # Reprezentacja zadania
    def __repr__(self):
        return f"['{self.i}'; p = {self.p}, w = {self.w}, r = {self.r}, d = {self.d}]"


class Schedule(Schedule):
    def isFeasible(self):
        if not super().isFeasible():
            return False

        ### POCZATEK ROZWIAZANIA
        listaZadan = self.assignments
        n = len(listaZadan)

        #czas startu < czas gotowości
        for i in range(0, n):
            if listaZadan[i].start < listaZadan[i].job.r:
                return False

        return True

        ### KONIEC ROZWIAZANIA

ja = Job("J1", p=10)
jb = Job("J2", p=10, r=5)
jc = Job("J3", p=10)

instance = Instance()
instance.jobs = [ja, jb, jc]

schedule = Schedule(instance)

# Poprawne uszeregowanie
schedule.assignments = [
    JobAssignment(ja, 0, 10),
    JobAssignment(jb, 10, 20),
    JobAssignment(jc, 20, 30)
]

assert schedule.isFeasible() == True

# Zadanie J2 wykonuje się zbyt wcześnie
schedule.assignments = [
    JobAssignment(jb, 0, 10),
    JobAssignment(ja, 10, 20),
    JobAssignment(jc, 20, 30)
]

assert schedule.isFeasible() == False

### BEGIN HIDDEN TESTS
ja = Job("J1", p=5)
jb = Job("J2", p=10)
jc = Job("J3", p=15)
jd = Job("J4", p=20, r=32)

instance = Instance()
instance.jobs = [ja, jb, jc, jd]

schedule = Schedule(instance)

# Poprawne uszeregowanie
schedule.assignments = [
    JobAssignment(ja, 0, 5),
    JobAssignment(jb, 5, 15),
    JobAssignment(jc, 15, 30),
    JobAssignment(jd, 32, 52),
]

assert schedule.isFeasible() == True

# Dwa zadania na siebie nachodzą
schedule.assignments = [
    JobAssignment(ja, 0, 5),
    JobAssignment(jb, 5, 15),
    JobAssignment(jc, 10, 25),
    JobAssignment(jd, 32, 52),
]

assert schedule.isFeasible() == False

# Zadanie J4 zaczyna się zbyt wcześnie
schedule.assignments = [
    JobAssignment(ja, 0, 5),
    JobAssignment(jb, 5, 15),
    JobAssignment(jc, 15, 30),
    JobAssignment(jd, 30, 50),
]

assert schedule.isFeasible() == False
### END HIDDEN TESTS

class Schedule(Schedule):
    def lmax(self):
        assert self.isFeasible() == True
        ### POCZATEK ROZWIAZANIA
        n = len(self.self.instance.jobs)
        zmienna = 0;
        max_opoznienie = 0;
        for j in n:
            zmienna = j.complete - j.job.d
            if zmienna > max_opoznienie:
                max_opoznienie = zmienna;
        return max_opoznienie;
        ### KONIEC ROZWIAZANIA

    def usum(self):
        assert self.isFeasible() == True
        ### POCZATEK ROZWIAZANIA
        n = len(self.self.instance.jobs)
        ile = 0;
        for j in n:
            if j.complete > j.job.d:
                ile += 1;
        return ile
        ### KONIEC ROZWIAZANIA

    def uwsum(self):
        assert self.isFeasible() == True
        ### POCZATEK ROZWIAZANIA
        n = len(self.self.instance.jobs)
        sum_wag = 0;
        for j in n:
            if j.complete > j.job.d:
                sum_wag += j.w;
        return sum_wag
        ### KONIEC ROZWIAZANIA

    def tsum(self):
        assert self.isFeasible() == True
        ### POCZATEK ROZWIAZANIA
        n = len(self.self.instance.jobs)
        sum_spoznien = 0;
        zmienna = 0;
        for j in n:
            zmienna = j.complete - j.job.d
            if zmienna > 0:
                sum_spoznien += zmienna;
        return sum_spoznien;
        ### KONIEC ROZWIAZANIA

    def twsum(self):
        assert self.isFeasible() == True
        ### POCZATEK ROZWIAZANIA
        n = len(self.self.instance.jobs)
        sum_wag = 0;
        zmienna = 0;
        for j in n:
            zmienna = j.complete - j.job.d
            if zmienna > 0:
                sum_wag += j.w;
        return sum_wag;
        ### KONIEC ROZWIAZANIA

from copy import deepcopy

def NoOrdering(instance):
    instance = deepcopy(instance)
    ### POCZATEK ROZWIAZANIA
    schedule = Schedule(instance)
    listaZadan = schedule.instance.jobs # wszystkie zadania
    n = len(listaZadan)
    machines = schedule.instance.jobs
    print(machines)
    print(listaZadan)
    print(n)

    for i in range(0, n):
        print(listaZadan[i])

    ### KONIEC ROZWIAZANIA
    return schedule

def EDD(instance):
    instance = deepcopy(instance)
    ### POCZATEK ROZWIAZANIA
    schedule = sorted(instance.jobs, key= lambda  j: j.d)
    ### KONIEC ROZWIAZANIA
    return schedule

def ERT(instance):
    instance = deepcopy(instance)
    ### POCZATEK ROZWIAZANIA
    schedule = sorted(instance.jobs, key=lambda j: j.r)
    ### KONIEC ROZWIAZANIA
    return schedule

random.seed(1234567890) # Ustaw ziarno generatora na stałe, aby wyniki były przewidywalne

instance = Instance()
instance.generate(100, 1, 100) # Wygeneruj 100 zadań o czasach wykonywania z przedziału od 1 do 100

# Każdemu z zadań przypisz losową wagę, czas gotowości i pożądany czas zakończenia
for i in instance.jobs:
    i.w = random.randint(1, 1000)
    i.r = random.randint(1, 7500)
    i.d = i.r + random.randint(50, 200)

no = NoOrdering(instance)
edd = EDD(instance)
ert = ERT(instance)

assert no.cmax() == 11624
assert edd.cmax() == 7582
assert ert.cmax() == 7567

assert no.csum() == 912068
assert edd.csum() == 381577
assert ert.csum() == 380051

assert no.lmax() == 10957
assert edd.lmax() == 114
assert ert.lmax() == 163

assert no.usum() == 96
assert edd.usum() == 37
assert ert.usum() == 29

assert no.uwsum() == 48479
assert edd.uwsum() == 18110
assert ert.uwsum() == 15448

assert no.tsum() == 528458
assert edd.tsum() == 1755
assert ert.tsum() == 1639

assert no.twsum() == 271037321
assert edd.twsum() == 909069
assert ert.twsum() == 870507
### BEGIN HIDDEN TESTS
random.seed(1234567890)

instance = Instance()
instance.generate(100, 1, 100)
instance.generate(20, 200, 300)

# Każdemu z zadań przypisz losową wagę, czas gotowości i pożądany czas zakończenia
for i in instance.jobs:
    i.w = random.randint(1, 1000)
    i.r = random.randint(1, 7500)
    i.d = i.r + random.randint(50, 200)

no = NoOrdering(instance)
edd = EDD(instance)
ert = ERT(instance)

assert no.cmax() == 16551
assert edd.cmax() == 9943
assert ert.cmax() == 9933

assert no.csum() == 1189714
assert edd.csum() == 600837
assert ert.csum() == 597428

assert no.lmax() == 16438
assert edd.lmax() == 2630
assert ert.lmax() == 2671

assert no.usum() == 117
assert edd.usum() == 115
assert ert.usum() == 114

assert no.uwsum() == 61533
assert edd.uwsum() == 60287
assert ert.uwsum() == 59884

assert no.tsum() == 725451
assert edd.tsum() == 136545
assert ert.tsum() == 133260

assert no.twsum() == 391108480
assert edd.twsum() == 71321799
assert ert.twsum() == 69455351
### END HIDDEN TESTS