class Job:
    # Konstruktor
    def __init__(self, i, p=1):
        assert (isinstance(p, int) and p > 0)
        self.i = i  # Identyfikator zadania (np. liczba lub ciąg znaków)
        self.p = p  # Czas wykonywania zadania

    # Reprezentacja zadania
    def __repr__(self):
        return f"['{self.i}'; p = {self.p}]"


import random


class Instance:
    def __init__(self):
        self.jobs = []

    def generate(self, n, pmin=1, pmax=1):
        ### POCZATEK ROZWIAZANIA
        for i in range(n):
            value = len(self.jobs) + 1
            rand = random.randint(pmin, pmax)
            self.jobs.append(Job(f"J{value}", rand))
        ### KONIEC ROZWIAZANIA

random.seed(1234567890)            # Ustaw ziarno generatora na stałe, aby wyniki były przewidywalne

instance = Instance()              # Utwórz zbiór zadań
instance.generate(4, 80, 100)      # Wygeneruj wektor czterech zadań o czasach wykonywania od 80 do 100 włącznie
instance.generate(5, 2, 10)        # Dopisz do tego wektora 5 zadań o czasach wykonywania od 2 do 10 włącznie
instance.generate(2)               # Dopisz do tego wektora 2 zadania o jednostkowych czasach wykonywania


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
        assert(isinstance(i, Instance))
        self.instance = i
        self.assignments = []

instance = Instance()
instance.generate(4, 80, 100)

schedule = Schedule(instance)

s = 0
for j in schedule.instance.jobs:
    schedule.assignments.append(JobAssignment(j, s, s + j.p))
    s += j.p

class Schedule(Schedule):
    def isFeasible(self):
        ### POCZATEK ROZWIAZANIA
        lista = []
        lista = self.assignments
        for i in range(0,len(lista)-1):
            if lista[i].complete > lista[i+1].start:
                return False

        if len(self.instance.jobs) > len(self.assignments):
            return False

        time = 0
        instance_jobs_keys = set([job.i for job in self.instance.jobs])
        for assignment in self.assignments:

            if (assignment.complete or assignment.start < 0) <= assignment.start:
                return False

            if assignment.job.i not in instance_jobs_keys:
                return False

            local_end_time = assignment.start + assignment.job.p

            if time > assignment.start:
                return False

            if local_end_time != assignment.complete:
                return False

            time = time + assignment.job.p
        return True

        ### KONIEC ROZWIAZANIA

ja = Job("J1", 10)
jb = Job("J2", 10)
jc = Job("J3", 10)

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

# Poprawne uszeregowanie
schedule.assignments = [
    JobAssignment(ja, 0, 10),
    JobAssignment(jb, 10, 20),
    JobAssignment(jc, 1020, 1030)
]

assert schedule.isFeasible() == True

# Dwa zadania na siebie nachodzą
schedule.assignments = [
    JobAssignment(ja, 0, 10),
    JobAssignment(jb, 9, 19),
    JobAssignment(jc, 19, 29)
]

assert schedule.isFeasible() == False

# Jedno zadanie wykonuje się zbyt krótko
schedule.assignments = [
    JobAssignment(ja, 0, 10),
    JobAssignment(jb, 10, 20),
    JobAssignment(jc, 20, 29)
]

assert schedule.isFeasible() == False

# Jedno zadanie wykonuje się zbyt długo
schedule.assignments = [
    JobAssignment(ja, 0, 10),
    JobAssignment(jb, 10, 25),
    JobAssignment(jc, 25, 35)
]

assert schedule.isFeasible() == False

# Jedno zadanie wykonuje się w dwóch częściach
schedule.assignments = [
    JobAssignment(ja, 0, 10),
    JobAssignment(jb, 10, 15),
    JobAssignment(jc, 15, 25),
    JobAssignment(jb, 25, 30)
]

assert schedule.isFeasible() == False

# Jedno zadanie nie wykonuje się w ogóle
schedule.assignments = [
    JobAssignment(ja, 0, 10),
    JobAssignment(jb, 10, 20)
]

assert schedule.isFeasible() == False

# W uszeregowaniu znajduje się zadanie, które nie jest częścią instancji
schedule.assignments = [
    JobAssignment(ja, 0, 10),
    JobAssignment(jb, 10, 20),
    JobAssignment(jc, 20, 30),
    JobAssignment(Job("X", 5), 30, 35)
]

assert schedule.isFeasible() == False

### BEGIN HIDDEN TESTS
ja = Job("J1", 5)
jb = Job("J2", 10)
jc = Job("J3", 15)
jd = Job("J4", 20)

instance = Instance()
instance.jobs = [ja, jb, jc, jd]

schedule = Schedule(instance)

# Poprawne uszeregowanie
schedule.assignments = [
    JobAssignment(ja, 0, 5),
    JobAssignment(jb, 5, 15),
    JobAssignment(jc, 15, 30),
    JobAssignment(jd, 30, 50),
]

assert schedule.isFeasible() == True

# Poprawne uszeregowanie
schedule.assignments = [
    JobAssignment(jb, 0, 10),
    JobAssignment(ja, 10, 15),
    JobAssignment(jc, 15, 30),
    JobAssignment(jd, 310, 330),
]

assert schedule.isFeasible() == True

# Dwa zadania na siebie nachodzą
schedule.assignments = [
    JobAssignment(jb, 0, 10),
    JobAssignment(ja, 20, 25),
    JobAssignment(jc, 15, 30),
    JobAssignment(jd, 310, 330),
]

assert schedule.isFeasible() == False

# Jedno zadanie wykonuje się zbyt krótko
schedule.assignments = [
    JobAssignment(jb, 0, 10),
    JobAssignment(ja, 10, 11),
    JobAssignment(jc, 15, 30),
    JobAssignment(jd, 310, 330),
]

assert schedule.isFeasible() == False

# Jedno zadanie wykonuje się zbyt długo
schedule.assignments = [
    JobAssignment(jb, 0, 10),
    JobAssignment(ja, 10, 15),
    JobAssignment(jc, 15, 30),
    JobAssignment(jd, 310, 340),
]

assert schedule.isFeasible() == False

# Jedno zadanie wykonuje się w dwóch częściach
schedule.assignments = [
    JobAssignment(jb, 0, 10),
    JobAssignment(ja, 10, 15),
    JobAssignment(jc, 15, 25),
    JobAssignment(jd, 310, 330),
    JobAssignment(jc, 330, 335),
]

assert schedule.isFeasible() == False

# Jedno zadanie nie wykonuje się w ogóle
schedule.assignments = [
    JobAssignment(jb, 0, 10),
    JobAssignment(ja, 10, 15),
    JobAssignment(jd, 310, 330),
]

assert schedule.isFeasible() == False

# W uszeregowaniu znajduje się zadanie, które nie jest częścią instancji
schedule.assignments = [
    JobAssignment(jb, 0, 10),
    JobAssignment(ja, 10, 15),
    JobAssignment(jc, 15, 30),
    JobAssignment(Job("X", 5), 30, 35),
    JobAssignment(jd, 310, 330),
]

assert schedule.isFeasible() == False
### END HIDDEN TESTS

class Schedule(Schedule):
    def cmax(self):
        assert self.isFeasible() == True
        ### POCZATEK ROZWIAZANIA

        t_max = float('-inf')
        for assignment in self.assignments:
            if assignment.complete > t_max:
                t_max = assignment.complete
        return t_max

        ### KONIEC ROZWIAZANIA

    def csum(self):
        assert self.isFeasible() == True
        ### POCZATEK ROZWIAZANIA

        return sum([assignment.complete for assignment in self.assignments])

        ### KONIEC ROZWIAZANIA

ja = Job("J1", 10)
jb = Job("J2", 10)
jc = Job("J3", 10)

instance = Instance()
instance.jobs = [ja, jb, jc]

schedule = Schedule(instance)
schedule.assignments = [
    JobAssignment(ja, 0, 10),
    JobAssignment(jb, 10, 20),
    JobAssignment(jc, 1020, 1030)
]

assert schedule.cmax() == 1030
assert schedule.csum() == 1060

### BEGIN HIDDEN TESTS
ja = Job("J1", 5)
jb = Job("J2", 10)
jc = Job("J3", 15)
jd = Job("J4", 20)

instance = Instance()
instance.jobs = [ja, jb, jc, jd]

schedule = Schedule(instance)
schedule.assignments = [
    JobAssignment(jb, 0, 10),
    JobAssignment(ja, 10, 15),
    JobAssignment(jc, 15, 30),
    JobAssignment(jd, 310, 330),
]

assert schedule.cmax() == 330
assert schedule.csum() == 385
### END HIDDEN TESTS

instance = Instance()
instance.generate(4, 80, 100)

schedule = Schedule(instance)

s = 0
for j in schedule.instance.jobs:
    schedule.assignments.append(JobAssignment(j, s, s + j.p))
    s += j.p

from copy import deepcopy

def L(instance):
    instance = deepcopy(instance)
    ### POCZATEK ROZWIAZANIA
    shedule = Schedule(instance)
    time =0
    for job in shedule.instance.jobs:
        shedule.assignments.append(JobAssignment(job, time, time+job.p))
        time += job.p
    ### KONIEC ROZWIAZANIA
    return shedule

random.seed(1234567890)

instance = Instance()
instance.generate(10, 1, 100)

opt = L(instance)

# Weryfikuję poprawność uszeregowania zadania J4
assert opt.assignments[3].job.i == "J4"
assert opt.assignments[3].start == 178
assert opt.assignments[3].complete == 235
assert opt.cmax() == 522
### BEGIN HIDDEN TESTS
ja = Job(1, 5)
jb = Job(4, 8)
jc = Job(7, 2)
jd = Job(2, 12)
je = Job(3, 1)

instance = Instance()
instance.jobs = [ja, jb, jc, jd, je]

opt = L(instance)

assert opt.assignments[0].job.i == 1 and opt.assignments[0].start == 0 and opt.assignments[0].complete == 5
assert opt.assignments[1].job.i == 4 and opt.assignments[1].start == 5 and opt.assignments[1].complete == 13
assert opt.assignments[2].job.i == 7 and opt.assignments[2].start == 13 and opt.assignments[2].complete == 15
assert opt.assignments[3].job.i == 2 and opt.assignments[3].start == 15 and opt.assignments[3].complete == 27
assert opt.assignments[4].job.i == 3 and opt.assignments[4].start == 27 and opt.assignments[4].complete == 28
assert opt.cmax() == 28
### END HIDDEN TESTS

from copy import deepcopy


def SPT(instance):
    instance = deepcopy(instance)
    ### POCZATEK ROZWIAZANIA
    schedule = Schedule(instance)

    sortedBy = sorted(schedule.instance.jobs, key=lambda job: job.p)

    time = 0
    for job in sortedBy:
        schedule.assignments.append(JobAssignment(job, time, time + job.p))
        time += job.p
    ### KONIEC ROZWIAZANIA
    return schedule

random.seed(1234567890) # Ustaw ziarno generatora na stałe, aby wyniki były przewidywalne

instance = Instance()
instance.generate(100, 1, 100) # Wygeneruj 100 zadań o czasach wykonywania z przedziału od 1 do 100

subopt = L(instance)
assert subopt.csum() == 236222

opt = SPT(instance)
assert opt.csum() == 157876
### BEGIN HIDDEN TESTS
random.seed(1234567890)

instance = Instance()
instance.generate(100, 1, 100)
instance.generate(20, 100, 200)
instance.generate(50, 1000, 1500)

opt = SPT(instance)
assert opt.csum() == 2162706
### END HIDDEN TESTS

class Job(Job):
    # Konstruktor
    def __init__(self, i, p=1, w=1):
        super().__init__(i, p)
        assert (isinstance(w, int) and w > 0)
        self.w = w  # Waga zadania

    # Reprezentacja zadania
    def __repr__(self):
        return f"['{self.i}'; p = {self.p}, w = {self.w}]"

class Schedule(Schedule):
    def cwsum(self):
        assert self.isFeasible() == True
        ### POCZATEK ROZWIAZANIA
        return sum([assignment.complete * assignment.job.w for assignment in self.assignments])
        ### KONIEC ROZWIAZANIA

ja = Job("J1", 10, 2)
jb = Job("J2", 10, 4)
jc = Job("J3", 10, 6)

instance = Instance()
instance.jobs = [ja, jb, jc]

schedule = Schedule(instance)
schedule.assignments = [
    JobAssignment(ja, 0, 10),
    JobAssignment(jb, 10, 20),
    JobAssignment(jc, 1020, 1030)
]

assert schedule.cmax() == 1030
assert schedule.csum() == 1060
assert schedule.cwsum() == 6280

### BEGIN HIDDEN TESTS
ja = Job("J1", 5, 2)
jb = Job("J2", 10, 1)
jc = Job("J3", 15, 4)
jd = Job("J4", 20, 5)

instance = Instance()
instance.jobs = [ja, jb, jc, jd]

schedule = Schedule(instance)
schedule.assignments = [
    JobAssignment(jb, 0, 10),
    JobAssignment(ja, 10, 15),
    JobAssignment(jc, 15, 30),
    JobAssignment(jd, 310, 330),
]

assert schedule.cmax() == 330
assert schedule.csum() == 385
assert schedule.cwsum() == 1810
### END HIDDEN TESTS

from copy import deepcopy


def WSPT(instance):
    instance = deepcopy(instance)
    ### POCZATEK ROZWIAZANIA
    schedule = Schedule(instance)
    sortedBy = sorted(schedule.instance.jobs, key=lambda job: job.p / job.w)
    time = 0

    for job in sortedBy:
        schedule.assignments.append(JobAssignment(job, time, time + job.p))
        time += job.p
    ### KONIEC ROZWIAZANIA
    return schedule

random.seed(1234567890) # Ustaw ziarno generatora na stałe, aby wyniki były przewidywalne

instance = Instance()
instance.generate(100, 1, 100) # Wygeneruj 100 zadań o czasach wykonywania z przedziału od 1 do 100

# Każdemu z zadań przypisz losową wagę z przedziału od 1 do 1000
for i in instance.jobs:
    i.w = random.randint(1, 1000)

opt = WSPT(instance)

assert opt.csum() == 184418
assert opt.cwsum() == 60765719

### BEGIN HIDDEN TESTS
random.seed(1234567890)

instance = Instance()
instance.generate(100, 1, 100)
instance.generate(20, 100, 200)
instance.generate(50, 1000, 1500)

for i in instance.jobs:
    i.w = random.randint(1, 1000)

opt = WSPT(instance)

assert opt.cwsum() == 850726351
### END HIDDEN TESTS

print("wszystko działa")