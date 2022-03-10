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
    def __init__(self, machines=1):
        self.jobs = []
        assert (isinstance(machines, int) and machines > 0)
        self.machines = machines

    def generate(self, n, pmin=1, pmax=1):
        for i in range(1, n + 1):
            self.jobs.append(Job("J" + str(len(self.jobs) + 1), random.randint(pmin, pmax)))


class JobAssignment:
    # Konstruktor
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

class Schedule:
    # Konstruktor
    def __init__(self, i):
        assert(isinstance(i, Instance))
        self.instance = i
        self.assignments = []


        # for i in range(0,n):
        #     print("Id:", listaZadan[i].job.i, "Czas wykonania:", listaZadan[i].job.p, "waga:", listaZadan[i].job.w, "machine:", listaZadan[i].machine, "start:", listaZadan[i].start, "complete:", listaZadan[i].complete)

class Schedule(Schedule):
    def isFeasible(self):
        ### POCZATEK ROZWIAZANIA

        listaZadan = self.assignments
        n = len(listaZadan)

        #W danej chwili, na danym procesorze, wykonuje się co najwyżej jedno zadanie.
        for i in range(0,n-1):
            for j in range(i+1,n):
                if listaZadan[i].machine == listaZadan[j].machine:
                    if listaZadan[j].start < listaZadan[i].complete:
                        return False

        #Każde zadanie zostało wykonane. Czas łączny zadań ma się równać czas wykonania.
        for i in range(0,n-1):
            for j in range(i+1,n):
                if listaZadan[i].job.i == listaZadan[j].job.i:
                    czas1 = listaZadan[i].complete - listaZadan[i].start
                    czas2 = listaZadan[j].complete - listaZadan[j].start
                    if czas1+czas2 != listaZadan[i].job.p:
                        return False

        #Na procesorach wykonują się tylko te zadania, które zostały opisane w instancji problemu.
        assignments = self.assignments
        instancjaObiektow = self.instance.jobs
        lenA = len(assignments)
        lenI = len(instancjaObiektow)

        for i in range(0, lenA):
            czyPrzypisane = False
            for j in range(0,lenI):
                if assignments[i].job == instancjaObiektow[j]:
                    czyPrzypisane = True
                    break

            if czyPrzypisane == False:
                return False

        # Jedno zadanie wykonuje się na nieistniejącej maszynie.
        machines = instance.machines
        for i in range(0, n):
            if listaZadan[i].machine > machines or listaZadan[i].machine <=0:
                return False

        # Jedno zadanie wykonuje się jednocześnie na dwóch procesorach
        for i in range(0,n-1):
            for j in range(i+1,n):
                if listaZadan[i].job.i == listaZadan[j].job.i:
                    if listaZadan[i].machine != listaZadan[j].machine:
                        zakres = range(listaZadan[i].start+1, listaZadan[i].complete-1)
                        if listaZadan[j].start in zakres or listaZadan[j].complete in zakres:
                            return False

        return True
        ### KONIEC ROZWIAZANIA



class Schedule(Schedule):
    def cmax(self):
        assert self.isFeasible() == True
        ### POCZATEK ROZWIAZANIA
        return max(map(lambda x: x.complete, self.assignments))
        ### KONIEC ROZWIAZANIA

    def csum(self):
        assert self.isFeasible() == True
        ### POCZATEK ROZWIAZANIA

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
        ### KONIEC ROZWIAZANIA

    def cwsum(self):
        assert self.isFeasible() == True
        ### POCZATEK ROZWIAZANIA

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

        ### KONIEC ROZWIAZANIA

ja = Job("J1", p=10)
jb = Job("J2", p=10)
jc = Job("J3", p=10)

instance = Instance(machines=3)
instance.jobs = [ja, jb, jc]

schedule = Schedule(instance)

# Poprawne uszeregowanie
schedule.assignments = [
    JobAssignment(ja, 1, 0, 5),
    JobAssignment(jb, 2, 0, 5),
    JobAssignment(jc, 3, 0, 5),
    JobAssignment(jb, 1, 5, 10),
    JobAssignment(jc, 2, 5, 10),
    JobAssignment(ja, 3, 5, 10),
]

assert schedule.isFeasible() == True

# Poprawne uszeregowanie
schedule.assignments = [
    JobAssignment(ja, 1, 0, 10),
    JobAssignment(jb, 2, 0, 5),
    JobAssignment(jc, 3, 0, 5),
    JobAssignment(jb, 1, 105, 110),
    JobAssignment(jc, 2, 5, 10),
]

assert schedule.isFeasible() == True

# Dwa zadania wykonują się jednocześnie na pierwszym procesorze
schedule.assignments = [
    JobAssignment(ja, 1, 0, 5),
    JobAssignment(jb, 2, 0, 5),
    JobAssignment(jc, 3, 0, 5),
    JobAssignment(jb, 1, 4, 9),
    JobAssignment(jc, 2, 5, 10),
    JobAssignment(ja, 3, 5, 10),
]

assert schedule.isFeasible() == False

# Jedno zadanie wykonuje się jednocześnie na dwóch procesorach
schedule.assignments = [
    JobAssignment(ja, 1, 20, 25),
    JobAssignment(jb, 2, 0, 5),
    JobAssignment(jc, 3, 0, 5),
    JobAssignment(jb, 1, 5, 10),
    JobAssignment(jc, 2, 5, 10),
    JobAssignment(ja, 3, 23, 28),
]

assert schedule.isFeasible() == False

# Niektóre zadania nie zostały ukończone
schedule.assignments = [
    JobAssignment(ja, 1, 0, 5),
    JobAssignment(jb, 2, 0, 5),
    JobAssignment(jc, 3, 0, 4),
    JobAssignment(jb, 1, 5, 9),
    JobAssignment(jc, 2, 5, 10),
    JobAssignment(ja, 3, 5, 10),
]

assert schedule.isFeasible() == False

# W uszeregowaniu znajduje się zadanie, które nie jest częścią instancji
schedule.assignments = [
    JobAssignment(ja, 1, 0, 10),
    JobAssignment(jb, 2, 0, 10),
    JobAssignment(jc, 3, 0, 10),
    JobAssignment(Job("X", 5), 3, 10, 15)
]

assert schedule.isFeasible() == False

# Jedno zadanie wykonuje się na nieistniejącej maszynie
schedule.assignments = [
    JobAssignment(ja, 1, 0, 5),
    JobAssignment(jb, 2, 0, 5),
    JobAssignment(jc, 3, 0, 5),
    JobAssignment(jb, 1, 5, 10),
    JobAssignment(jc, 2, 5, 10),
    JobAssignment(ja, 4, 5, 10),
]

assert schedule.isFeasible() == False
### BEGIN HIDDEN TESTS
ja = Job("J1", p=5)
jb = Job("J2", p=10)
jc = Job("J3", p=15)
jd = Job("J4", p=20)

instance = Instance(machines=4)
instance.jobs = [ja, jb, jc, jd]

schedule = Schedule(instance)

# Poprawne uszeregowanie
schedule.assignments = [
    JobAssignment(ja, 1, 0, 5),
    JobAssignment(jb, 2, 0, 10),
    JobAssignment(jc, 2, 10, 25),
    JobAssignment(jd, 3, 0, 10),
    JobAssignment(jd, 2, 25, 35),
]

assert schedule.isFeasible() == True

# Poprawne uszeregowanie
schedule.assignments = [
    JobAssignment(ja, 1, 0, 5),
    JobAssignment(jb, 2, 0, 10),
    JobAssignment(jc, 2, 10, 25),
    JobAssignment(jd, 3, 0, 10),
    JobAssignment(jd, 2, 1025, 1035),
]

assert schedule.isFeasible() == True

# Dwa zadania wykonują się jednocześnie na pierwszym procesorze
schedule.assignments = [
    JobAssignment(ja, 1, 0, 5),
    JobAssignment(jb, 2, 0, 10),
    JobAssignment(jc, 2, 10, 25),
    JobAssignment(jd, 3, 0, 10),
    JobAssignment(jd, 1, 4, 14),
]

assert schedule.isFeasible() == False

# Jedno zadanie wykonuje się jednocześnie na dwóch procesorach
schedule.assignments = [
    JobAssignment(ja, 1, 0, 5),
    JobAssignment(jb, 2, 0, 10),
    JobAssignment(jc, 2, 10, 25),
    JobAssignment(jd, 3, 0, 10),
    JobAssignment(jd, 4, 5, 15),
]

assert schedule.isFeasible() == False

# Niektóre zadania nie zostały ukończone
schedule.assignments = [
    JobAssignment(ja, 1, 0, 5),
    JobAssignment(jb, 2, 0, 10),
    JobAssignment(jc, 2, 10, 25),
    JobAssignment(jd, 3, 0, 10),
    JobAssignment(jd, 2, 25, 34),
]

assert schedule.isFeasible() == False

# W uszeregowaniu znajduje się zadanie, które nie jest częścią instancji
schedule.assignments = [
    JobAssignment(ja, 1, 0, 5),
    JobAssignment(jb, 2, 0, 10),
    JobAssignment(jc, 2, 10, 25),
    JobAssignment(jd, 3, 0, 10),
    JobAssignment(jd, 2, 25, 35),
    JobAssignment(Job("X", 5), 3, 1010, 1015)
]

assert schedule.isFeasible() == False

# Jedno zadanie wykonuje się na nieistniejącej maszynie
schedule.assignments = [
    JobAssignment(ja, 1, 0, 5),
    JobAssignment(jb, 2, 0, 10),
    JobAssignment(jc, 2, 10, 25),
    JobAssignment(jd, 5, 0, 10),
    JobAssignment(jd, 2, 25, 35),
]

assert schedule.isFeasible() == False
### END HIDDEN TESTS

class Schedule(Schedule):
    def cmax(self):
        assert self.isFeasible() == True
        ### POCZATEK ROZWIAZANIA
        return max(map(lambda x: x.complete, self.assignments))
        ### KONIEC ROZWIAZANIA

    def csum(self):
        assert self.isFeasible() == True
        ### POCZATEK ROZWIAZANIA

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
        ### KONIEC ROZWIAZANIA

    def cwsum(self):
        assert self.isFeasible() == True
        ### POCZATEK ROZWIAZANIA
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

        ### KONIEC ROZWIAZANIA

ja = Job("J1", p=10)
jb = Job("J2", p=10)
jc = Job("J3", w=2, p=10)

instance = Instance(machines=3)
instance.jobs = [ja, jb, jc]

schedule = Schedule(instance)

schedule.assignments = [
    JobAssignment(ja, 1, 0, 5),
    JobAssignment(jb, 2, 0, 5),
    JobAssignment(jc, 3, 0, 5),
    JobAssignment(jb, 1, 5, 10),
    JobAssignment(jc, 2, 5, 10),
    JobAssignment(ja, 3, 5, 10),
]

assert schedule.cmax() == 10
assert schedule.csum() == 30
assert schedule.cwsum() == 40
### BEGIN HIDDEN TESTS
ja = Job("J1", w=5, p=5)
jb = Job("J2", w=4, p=10)
jc = Job("J3", w=2, p=15)
jd = Job("J4", w=1, p=20)

instance = Instance(machines=3)
instance.jobs = [ja, jb, jc, jd]

schedule = Schedule(instance)

schedule.assignments = [
    JobAssignment(ja, 3, 0, 5),
    JobAssignment(jb, 3, 5, 10),
    JobAssignment(jb, 2, 0, 5),
    JobAssignment(jc, 1, 0, 10),
    JobAssignment(jc, 1, 12, 17),
    JobAssignment(jd, 2, 5, 25),
]

assert schedule.cmax() == 25
assert schedule.csum() == 57
assert schedule.cwsum() == 124
### END HIDDEN TESTS

from copy import deepcopy

def L(instance):
    instance = deepcopy(instance)
    ### POCZATEK ROZWIAZANIA

    schedule = Schedule(instance)
    instancjaJobs = instance.jobs #wszystkie zadania

    n = len(instancjaJobs)
    machines = schedule.instance.machines #dostępne procesory
    times = [0] * machines #w zależności ile jest procesorow, na początku czas wszystkich ustawia na 0, tablica wyników z czasem dla każdego procesora
    for i in range(0,n):
        pierwszy = 0
        for j in range(0,machines):
            if times[j] < times[pierwszy]:
                pierwszy = j
        schedule.assignments.append(JobAssignment(instancjaJobs[i], pierwszy + 1, times[pierwszy], times[pierwszy] + instancjaJobs[i].p))
        times[pierwszy] += instancjaJobs[i].p

    ### KONIEC ROZWIAZANIA
    return schedule

random.seed(1234567890)

instance = Instance()
instance.generate(50, 1, 100)

instance.machines = 1
schedule = L(instance)
assert schedule.cmax() == 2333

instance.machines = 2
schedule = L(instance)
assert schedule.cmax() == 1170

instance.machines = 5
schedule = L(instance)
assert schedule.cmax() == 495
### BEGIN HIDDEN TESTS
random.seed(1234567890)

instance = Instance()
instance.generate(100, 1, 100)

instance.machines = 1
schedule = L(instance)
assert schedule.cmax() == 4728

instance.machines = 2
schedule = L(instance)
assert schedule.cmax() == 2391

instance.machines = 5
schedule = L(instance)
assert schedule.cmax() == 996
### END HIDDEN TESTS

from copy import deepcopy

def LPT(instance):
    instance = deepcopy(instance)
    ### POCZATEK ROZWIAZANIA

    schedule = Schedule(instance)
    listaZadan = schedule.instance.jobs

    listaZadan.sort(reverse=True, key=lambda x: x.p) #sortowanie zadan według malejącego p
    n = len(listaZadan)

    machines = schedule.instance.machines #dostępne procesory

    times = [0] * machines #w zależności ile jest procesorow, na początku czas wszystkich ustawia na 0, tablica wyników z czasem dla każdego procesora

    value = 0
    for i in range(0,n):

        pierwszy = 0
        for j in range(0,machines):
            if times[j] < times[pierwszy]:
                pierwszy = j
        schedule.assignments.append(JobAssignment(listaZadan[i], pierwszy + 1, times[pierwszy], times[pierwszy] + listaZadan[i].p))
        times[pierwszy] += listaZadan[i].p
        value += times[pierwszy]

    ### KONIEC ROZWIAZANIA
    return schedule

random.seed(1234567890)

instance = Instance()
instance.generate(50, 1, 100)

instance.machines = 1
assert L(instance).cmax() == 2333
assert LPT(instance).cmax() == 2333

instance.machines = 2
assert L(instance).cmax() == 1170
assert LPT(instance).cmax() == 1167

instance.machines = 5
assert L(instance).cmax() == 495
assert LPT(instance).cmax() == 471
### BEGIN HIDDEN TESTS
random.seed(1234567890)

instance = Instance()
instance.generate(100, 1, 100)

instance.machines = 1
assert LPT(instance).cmax() == 4728

instance.machines = 3
assert LPT(instance).cmax() == 1578

instance.machines = 5
assert LPT(instance).cmax() == 946

instance.machines = 10
assert LPT(instance).cmax() == 475
### END HIDDEN TESTS

from copy import deepcopy

def SPT(instance):
    instance = deepcopy(instance)
    ### POCZATEK ROZWIAZANIA

    schedule = Schedule(instance)
    listaZadan = schedule.instance.jobs

    listaZadan.sort(key=lambda x: x.p) #sortowanie zadan według rosnacego p
    n = len(listaZadan)

    machines = schedule.instance.machines #dostepne procesory
    times = [0] * machines #w zależności ile jest procesorow, na początku czas wszystkich ustawia na 0, tablica wyników z czasem dla każdego procesora

    for i in range(0,n):

        pierwszy = 0
        for j in range(0, machines):
            if times[j] < times[pierwszy]:
                pierwszy = j
        schedule.assignments.append(JobAssignment(listaZadan[i], pierwszy + 1, times[pierwszy], times[pierwszy] + listaZadan[i].p))
        times[pierwszy] += listaZadan[i].p
    ### KONIEC ROZWIAZANIA
    return schedule

random.seed(1234567890)

instance = Instance()
instance.generate(50, 1, 100)

instance.machines = 1
assert L(instance).csum() == 60506
assert SPT(instance).csum() == 39761

instance.machines = 2
assert L(instance).csum() == 30653
assert SPT(instance).csum() == 20478

instance.machines = 5
assert L(instance).csum() == 12659
assert SPT(instance).csum() == 8920
### BEGIN HIDDEN TESTS
random.seed(1234567890)

instance = Instance()
instance.generate(100, 1, 100)

instance.machines = 1
assert SPT(instance).csum() == 157876

instance.machines = 3
assert SPT(instance).csum() == 54225

instance.machines = 5
assert SPT(instance).csum() == 33505

instance.machines = 10
assert SPT(instance).csum() == 17990
### END HIDDEN TESTS

from copy import deepcopy

def McNaughton(instance):
    instance = deepcopy(instance)
    ### POCZATEK ROZWIAZANIA

    schedule = Schedule(instance)
    listaZadan1 = schedule.instance.jobs
    n = len(listaZadan1)
    ileProcesorow1 = schedule.instance.machines

    schedule2 = Schedule(instance)

    pSum = int(sum(map(lambda x: x.p, listaZadan1)) / ileProcesorow1)
    cMax = max(pSum, max(map(lambda x: x.p, listaZadan1)))


    leftover = 0
    unfinished = 0

    ileProcesorow2 = schedule2.instance.machines
    for i in range(0, ileProcesorow2):
        ss = 0
        machineFull = False
        if leftover != 0:
            schedule.assignments.append(JobAssignment(unfinished, i + 1, ss, leftover))
            ss += leftover
        for a in schedule2.instance.jobs:
            if machineFull == False and n > 0:
                if ss + a.p < cMax:
                    schedule.assignments.append(JobAssignment(a, i + 1, ss, ss + a.p))
                    ss += a.p
                elif ss + a.p == cMax:
                    schedule.assignments.append(JobAssignment(a, i + 1, ss, ss + a.p))
                elif ss + a.p > cMax and ss < cMax:
                    schedule.assignments.append(JobAssignment(a, i + 1, ss, cMax))
                    leftover = a.p - (cMax - ss)
                    unfinished = a
                    machineFull = True
                n -= 1
        for c in range(len(schedule.assignments)):
            if schedule2.instance.jobs.count(schedule.assignments[c].job) != 0:
                schedule2.instance.jobs.remove(schedule.assignments[c].job)
            if listaZadan1.count(schedule.assignments[c].job) == 0:
                listaZadan1.append(schedule.assignments[c].job)
                ### KONIEC ROZWIAZANIA
    return schedule

ja = Job("J1", p=10)
jb = Job("J2", p=10)
jc = Job("J3", p=10)

instance = Instance()
instance.machines = 2
instance.jobs = [ja, jb, jc]

assert LPT(instance).cmax() == 20
assert McNaughton(instance).cmax() == 15

random.seed(1234567890) # Ustaw ziarno generatora na stałe, aby wyniki były przewidywalne

instance = Instance()
instance.generate(200, 1, 100) # Wygeneruj 100 zadań o czasach wykonywania z przedziału od 1 do 100
instance.machines = 7

assert LPT(instance).cmax() == 1418
assert McNaughton(instance).cmax() == 1417

random.seed(1234567890) # Ustaw ziarno generatora na stałe, aby wyniki były przewidywalne

instance = Instance()
instance.generate(200, 1, 100) # Wygeneruj 100 zadań o czasach wykonywania z przedziału od 1 do 100
instance.jobs.append(Job("J", p = 1420))
instance.machines = 8

assert LPT(instance).cmax() == 1420
assert McNaughton(instance).cmax() == 1420
### BEGIN HIDDEN TESTS
random.seed(1234567890)

instance = Instance()
instance.generate(120, 1, 100)
instance.machines = 3

assert McNaughton(instance).cmax() == 1932

random.seed(1234567890)

instance = Instance()
instance.generate(120, 1, 100)
instance.jobs.append(Job("J", p = 1933))
instance.machines = 4

assert McNaughton(instance).cmax() == 1933
### END HIDDEN TESTS

print("wszystko działa")