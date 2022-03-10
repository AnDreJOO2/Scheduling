class Job:
    # Konstruktor
    def __init__(self, i, p1=1, p2=1):
        self.i = i  # Identyfikator zadania (np. liczba lub ciąg znaków)
        assert (isinstance(p1, int) and p1 > 0)
        assert (isinstance(p2, int) and p2 > 0)
        self.p1 = p1  # Czas wykonywania operacji na pierwszym procesorze
        self.p2 = p2  # Czas wykonywania operacji na drugim procesorze

    # Reprezentacja zadania
    def __repr__(self):
        return f"['{self.i}'; p = [{self.p1}, {self.p2}]]"

import random

class Instance:
    def __init__(self):
        self.jobs = []


class JobAssignment:
    # Konstruktor
    def __init__(self, j, m, s, c):
        assert (isinstance(j, Job))
        assert (m == 1 or m == 2)
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


#is feasible
# Żadna operacja nie wykonuje się na niedostepnym procesorze.
# Na procesorach wykonują się tylko te zadania, które zostały opisane w instancji problemu.
# W danej chwili, na danym procesorze, wykonuje się co najwyżej jedna operacja.
# Każda operacja wykonuje się dokładnie tyle czasu, ile powinna.
# Operacje w ramach tego samego zadania nie wykonują się jednocześnie na więcej niż jednym procesorze.
# Każda operacja została wykonana.

class Schedule(Schedule):
    def isFeasible(self):
        ### POCZATEK ROZWIAZANIA

        listaZadan = self.assignments
        n = len(listaZadan)

        # Jedna operacja jest zbyt krótka
        # Jedna operacja jest zbyt długa
        for i in range(0,n):
            czas_trwania_zadania = listaZadan[i].complete - listaZadan[i].start
            wybrany_procesor = listaZadan[i].machine
            czas_na_procesorze = 0
            if wybrany_procesor == 1:
                czas_na_procesorze = listaZadan[i].job.p1
            if wybrany_procesor == 2:
                czas_na_procesorze = listaZadan[i].job.p2

            if czas_na_procesorze != czas_trwania_zadania:
                return False

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


        # Jedna operacja nie została wykonana
        instacjaJobs = self.instance.jobs
        a = len(instacjaJobs)

        listaId = []
        for i in range(0,a):
            listaId.append(instacjaJobs[i].i)

        if listaZadan[i].job.i not in listaId or n%2 != 0:
            return False

        # W uszeregowaniu znajduje się zadanie, które nie jest częścią instancji
        for i in range(0,n):
            przypisane = False
            for j in range(0, a):
                if listaZadan[i].job == instacjaJobs[j]:
                    przypisane = True
                    break
            if przypisane == False:
                return False

        return True
        ### KONIEC ROZWIAZANIA


ja = Job("J1", p1=10, p2=10)
jb = Job("J2", p1=10, p2=10)
jc = Job("J3", p1=10, p2=10)

instance = Instance()
instance.jobs = [ja, jb, jc]

schedule = Schedule(instance)

# Poprawne uszeregowanie
schedule.assignments = [
    JobAssignment(ja, 1, 0, 10),
    JobAssignment(jb, 1, 10, 20),
    JobAssignment(jc, 1, 20, 30),
    JobAssignment(jb, 2, 0, 10),
    JobAssignment(jc, 2, 10, 20),
    JobAssignment(ja, 2, 20, 30),
]

assert schedule.isFeasible() == True

# Dwie operacje wykonują się jednocześnie na pierwszym procesorze
schedule.assignments = [
    JobAssignment(ja, 1, 0, 10),
    JobAssignment(jb, 1, 11, 21),
    JobAssignment(jc, 1, 20, 30),
    JobAssignment(jb, 2, 0, 10),
    JobAssignment(jc, 2, 10, 20),
    JobAssignment(ja, 2, 20, 30),
]

assert schedule.isFeasible() == False

# Dwie operacje w ramach tego samego zadania wykonują się jednocześnie na obu procesorach
schedule.assignments = [
    JobAssignment(ja, 1, 0, 10),
    JobAssignment(jb, 1, 10, 20),
    JobAssignment(jc, 1, 20, 30),
    JobAssignment(jb, 2, 0, 10),
    JobAssignment(jc, 2, 11, 21),
    JobAssignment(ja, 2, 21, 31),
]

assert schedule.isFeasible() == False

# Jedna operacja jest zbyt długa
schedule.assignments = [
    JobAssignment(ja, 1, 0, 10),
    JobAssignment(jb, 1, 10, 20),
    JobAssignment(jc, 1, 20, 30),
    JobAssignment(jb, 2, 0, 10),
    JobAssignment(jc, 2, 10, 20),
    JobAssignment(ja, 2, 20, 31),
]

assert schedule.isFeasible() == False

# Jedna operacja jest zbyt krótka
schedule.assignments = [
    JobAssignment(ja, 1, 0, 10),
    JobAssignment(jb, 1, 10, 20),
    JobAssignment(jc, 1, 20, 29),
    JobAssignment(jb, 2, 0, 10),
    JobAssignment(jc, 2, 10, 20),
    JobAssignment(ja, 2, 20, 30),
]

assert schedule.isFeasible() == False

# Jedna operacja nie została wykonana
schedule.assignments = [
    JobAssignment(ja, 1, 0, 10),
    JobAssignment(jb, 1, 10, 20),
    JobAssignment(jb, 2, 0, 10),
    JobAssignment(jc, 2, 10, 20),
    JobAssignment(ja, 2, 20, 30),
]

assert schedule.isFeasible() == False

# Jedna operacja została wykonana w dwóch częściach
schedule.assignments = [
    JobAssignment(ja, 1, 0, 10),
    JobAssignment(jb, 1, 10, 20),
    JobAssignment(jc, 1, 20, 25),
    JobAssignment(jc, 1, 26, 31),
    JobAssignment(jb, 2, 0, 10),
    JobAssignment(jc, 2, 10, 20),
    JobAssignment(ja, 2, 20, 30),
]

assert schedule.isFeasible() == False

# W uszeregowaniu znajduje się zadanie, które nie jest częścią instancji
schedule.assignments = [
    JobAssignment(ja, 1, 0, 10),
    JobAssignment(jb, 1, 10, 20),
    JobAssignment(jc, 1, 20, 30),
    JobAssignment(jb, 2, 0, 10),
    JobAssignment(jc, 2, 10, 20),
    JobAssignment(ja, 2, 20, 30),
    JobAssignment(Job("X", p1=10, p2=10), 1, 30, 40),
]

assert schedule.isFeasible() == False
### BEGIN HIDDEN TESTS
ja = Job("J1", p1=5, p2=10)
jb = Job("J2", p1=10, p2=15)
jc = Job("J3", p1=15, p2=5)
jd = Job("J4", p1=5, p2=5)

instance = Instance()
instance.jobs = [ja, jb, jc, jd]

schedule = Schedule(instance)

# Poprawne uszeregowanie
schedule.assignments = [
    JobAssignment(ja, 1, 0, 5),
    JobAssignment(jb, 1, 5, 15),
    JobAssignment(jc, 1, 15, 30),
    JobAssignment(jd, 1, 30, 35),
    JobAssignment(jc, 2, 0, 5),
    JobAssignment(ja, 2, 5, 15),
    JobAssignment(jb, 2, 15, 30),
    JobAssignment(jd, 2, 35, 40),
]

assert schedule.isFeasible() == True

# Dwie operacje wykonują się jednocześnie na pierwszym procesorze
schedule.assignments = [
    JobAssignment(ja, 1, 0, 5),
    JobAssignment(jb, 1, 5, 15),
    JobAssignment(jc, 1, 15, 30),
    JobAssignment(jd, 1, 29, 34),
    JobAssignment(jc, 2, 0, 5),
    JobAssignment(ja, 2, 5, 15),
    JobAssignment(jb, 2, 15, 30),
    JobAssignment(jd, 2, 35, 40),
]

assert schedule.isFeasible() == False

# Dwie operacje w ramach tego samego zadania wykonują się jednocześnie na obu procesorach
schedule.assignments = [
    JobAssignment(ja, 1, 0, 5),
    JobAssignment(jb, 1, 5, 15),
    JobAssignment(jc, 1, 15, 30),
    JobAssignment(jd, 1, 30, 35),
    JobAssignment(jc, 2, 0, 5),
    JobAssignment(ja, 2, 5, 15),
    JobAssignment(jb, 2, 15, 30),
    JobAssignment(jd, 2, 34, 39),
]

assert schedule.isFeasible() == False

# Jedna operacja jest zbyt długa
schedule.assignments = [
    JobAssignment(ja, 1, 0, 5),
    JobAssignment(jb, 1, 5, 15),
    JobAssignment(jc, 1, 15, 30),
    JobAssignment(jd, 1, 30, 35),
    JobAssignment(jc, 2, 0, 5),
    JobAssignment(ja, 2, 5, 15),
    JobAssignment(jb, 2, 15, 31),
    JobAssignment(jd, 2, 35, 40),
]

assert schedule.isFeasible() == False

# Jedna operacja jest zbyt krótka
schedule.assignments = [
    JobAssignment(ja, 1, 0, 5),
    JobAssignment(jb, 1, 5, 15),
    JobAssignment(jc, 1, 15, 30),
    JobAssignment(jd, 1, 30, 34),
    JobAssignment(jc, 2, 0, 5),
    JobAssignment(ja, 2, 5, 15),
    JobAssignment(jb, 2, 15, 30),
    JobAssignment(jd, 2, 35, 40),
]

assert schedule.isFeasible() == False

# Jedna operacja nie została wykonana
schedule.assignments = [
    JobAssignment(ja, 1, 0, 5),
    JobAssignment(jb, 1, 5, 15),
    JobAssignment(jc, 1, 15, 30),
    JobAssignment(jd, 1, 30, 35),
    JobAssignment(ja, 2, 5, 15),
    JobAssignment(jb, 2, 15, 30),
    JobAssignment(jd, 2, 35, 40),
]

assert schedule.isFeasible() == False

# Jedna operacja została wykonana w dwóch częściach
schedule.assignments = [
    JobAssignment(ja, 1, 0, 5),
    JobAssignment(jb, 1, 5, 15),
    JobAssignment(jc, 1, 15, 30),
    JobAssignment(jd, 1, 30, 35),
    JobAssignment(jd, 1, 40, 45),
    JobAssignment(jc, 2, 0, 5),
    JobAssignment(ja, 2, 5, 15),
    JobAssignment(jb, 2, 15, 30),
    JobAssignment(jd, 2, 35, 40),
]

assert schedule.isFeasible() == False

# W uszeregowaniu znajduje się zadanie, które nie jest częścią instancji
je = Job("X", p1=5, p2=5)
schedule.assignments = [
    JobAssignment(ja, 1, 0, 5),
    JobAssignment(jb, 1, 5, 15),
    JobAssignment(jc, 1, 15, 30),
    JobAssignment(jd, 1, 30, 35),
    JobAssignment(jc, 2, 0, 5),
    JobAssignment(ja, 2, 5, 15),
    JobAssignment(jb, 2, 15, 30),
    JobAssignment(jd, 2, 35, 40),
    JobAssignment(je, 1, 35, 40),
    JobAssignment(je, 2, 40, 45),
]

assert schedule.isFeasible() == False
### END HIDDEN TESTS


class Schedule(Schedule):
    def cmax(self):
        assert self.isFeasible() == True
        ### POCZATEK ROZWIAZANIA

        return max(map(lambda x: x.complete, self.assignments))

        ### KONIEC ROZWIAZANIA

ja = Job("J1", p1=10, p2=10)
jb = Job("J2", p1=10, p2=10)
jc = Job("J3", p1=10, p2=10)

instance = Instance()
instance.jobs = [ja, jb, jc]

schedule = Schedule(instance)

# Poprawne uszeregowanie
schedule.assignments = [
    JobAssignment(ja, 1, 0, 10),
    JobAssignment(jb, 1, 10, 20),
    JobAssignment(jc, 1, 20, 30),
    JobAssignment(jb, 2, 0, 10),
    JobAssignment(jc, 2, 10, 20),
    JobAssignment(ja, 2, 20, 30),
]

assert schedule.cmax() == 30
### BEGIN HIDDEN TESTS
ja = Job("J1", p1=5, p2=10)
jb = Job("J2", p1=10, p2=15)
jc = Job("J3", p1=15, p2=5)
jd = Job("J4", p1=5, p2=5)

instance = Instance()
instance.jobs = [ja, jb, jc, jd]

schedule = Schedule(instance)

schedule.assignments = [
    JobAssignment(ja, 1, 0, 5),
    JobAssignment(jb, 1, 5, 15),
    JobAssignment(jc, 1, 15, 30),
    JobAssignment(jd, 1, 30, 35),
    JobAssignment(jc, 2, 0, 5),
    JobAssignment(ja, 2, 5, 15),
    JobAssignment(jb, 2, 15, 30),
    JobAssignment(jd, 2, 35, 40),
]

assert schedule.cmax() == 40
### END HIDDEN TESTS


#lapt

from copy import deepcopy

# def LAPT(instance):
#     instance = deepcopy(instance)
#     ### POCZATEK ROZWIAZANIA
#
#     schedule = Schedule(instance)
#     listaZadan = schedule.instance.jobs
#
#     n = len(listaZadan)
#
#     for i in range(0, n):
#         print(listaZadan[i])
#
#     ### KONIEC ROZWIAZANIA
#     return schedule
#
#
# ja = Job("J1", p1=8, p2=3)
# jb = Job("J2", p1=7, p2=11)
# jc = Job("J3", p1=5, p2=12)
# jd = Job("J4", p1=10, p2=5)
#
# instance = Instance()
# instance.jobs = [ja, jb, jc, jd]
#
# assert LAPT(instance).cmax() == 31
#
# ja = Job("J1", p1=10, p2=23)
# jb = Job("J2", p1=11, p2=22)
# jc = Job("J3", p1=12, p2=21)
# jd = Job("J4", p1=13, p2=20)
#
# instance = Instance()
# instance.jobs = [ja, jb, jc, jd]
#
# assert LAPT(instance).cmax() == 86
# ### BEGIN HIDDEN TESTS
# ja = Job("J1", p1=3, p2=5)
# jb = Job("J2", p1=2, p2=4)
# jc = Job("J3", p1=8, p2=4)
# jd = Job("J4", p1=1, p2=2)
#
# instance = Instance()
# instance.jobs = [ja, jb, jc, jd]
#
# assert LAPT(instance).cmax() == 16
#
# ja = Job("J1", p1=1, p2=1)
# jb = Job("J2", p1=2, p2=2)
# jc = Job("J3", p1=3, p2=3)
# jd = Job("J4", p1=4, p2=4)
# je = Job("J5", p1=5, p2=5)
# jf = Job("J6", p1=6, p2=6)
#
# instance = Instance()
# instance.jobs = [ja, jb, jc, jd, je, jf]
#
# assert LAPT(instance).cmax() == 21
#
#
# ### END HIDDEN TESTS


# Systemy typu flow shop

class Schedule(Schedule):
    def isFeasible(self):
        if not super().isFeasible():
            return False

        ### POCZATEK ROZWIAZANIA

        listaZadan = self.assignments
        n = len(listaZadan)

        for i in range(0, n-1):
            if listaZadan[i].machine == listaZadan[i+1].machine:
                if listaZadan[i].complete > listaZadan[i+1].start:
                    return False

        return True
        ### KONIEC ROZWIAZANIA


ja = Job("J1", p1=10, p2=10)
jb = Job("J2", p1=10, p2=10)

instance = Instance()
instance.jobs = [ja, jb]

schedule = Schedule(instance)

# Poprawne uszeregowanie
schedule.assignments = [
    JobAssignment(ja, 1, 0, 10),
    JobAssignment(jb, 1, 10, 20),
    JobAssignment(ja, 2, 10, 20),
    JobAssignment(jb, 2, 20, 30),
]

assert schedule.isFeasible() == True

# Zadanie J2 wykonuje operacje w nieprawidłowej kolejności
schedule.assignments = [
    JobAssignment(ja, 1, 0, 10),
    JobAssignment(jb, 1, 10, 20),
    JobAssignment(ja, 2, 10, 20),
    JobAssignment(jb, 2, 0, 10),
]

assert schedule.isFeasible() == False
### BEGIN HIDDEN TESTS
ja = Job("J1", p1=5, p2=5)
jb = Job("J2", p1=5, p2=5)
jc = Job("J3", p1=5, p2=5)
jd = Job("J4", p1=5, p2=5)

instance = Instance()
instance.jobs = [ja, jb, jc, jd]

schedule = Schedule(instance)

# Poprawne uszeregowanie
schedule.assignments = [
    JobAssignment(ja, 1, 0, 5),
    JobAssignment(jb, 1, 5, 10),
    JobAssignment(jc, 1, 10, 15),
    JobAssignment(jd, 1, 15, 20),
    JobAssignment(ja, 2, 5, 10),
    JobAssignment(jb, 2, 10, 15),
    JobAssignment(jc, 2, 15, 20),
    JobAssignment(jd, 2, 20, 25),
]

assert schedule.isFeasible() == True

# Zadanie J4 wykonuje operacje w nieprawidłowej kolejności
schedule.assignments = [
    JobAssignment(ja, 1, 0, 5),
    JobAssignment(jb, 1, 5, 10),
    JobAssignment(jc, 1, 10, 15),
    JobAssignment(jd, 1, 15, 20),
    JobAssignment(ja, 2, 5, 10),
    JobAssignment(jb, 2, 15, 20),
    JobAssignment(jc, 2, 20, 25),
    JobAssignment(jd, 2, 10, 15),
]

assert schedule.isFeasible() == False
### END HIDDEN TESTS

#Algorytm Johnsona

from copy import deepcopy


def Johnson(instance):
    instance = deepcopy(instance)
    ### POCZATEK ROZWIAZANIA

    schedule = Schedule(instance)
    listaZadan = schedule.instance.jobs

    n = len(listaZadan)

    P = []
    R = []

    # 1 krok
    for i in range(0, n):
        if listaZadan[i].p1 < listaZadan[i].p2:
            P.append(listaZadan[i])
        else:
            R.append(listaZadan[i])

    # # 2 krok
    A = sorted(P, key=lambda p: p.p1) # B = porortowana lista od najkrotszych p1

    # # 3 krok
    B = sorted(R, key=lambda r: r.p2, reverse=True) # B = porortowana lista od najdluzszych p2

    # 4 krok
    start_zadania = 0

    #Dodawanie zadan do P1 z listy A
    for i in range(0,len(A)):
        complete = start_zadania + A[i].p1
        schedule.assignments.append(JobAssignment(A[i], 1, start_zadania, complete))
        start_zadania = complete

    # Dodawanie zadan do P1 z listy B
    for i in range(0,len(B)):
        complete = start_zadania + B[i].p1
        schedule.assignments.append(JobAssignment(B[i], 1, start_zadania, complete))
        start_zadania = complete

    listaZadan = schedule.assignments

    start_zadania = 0
    # Dodawanie zadan do P2 z listy A
    for i in range(0, len(A)):
        if listaZadan[i].complete > start_zadania:
            start_zadania = listaZadan[i].complete
        complete = start_zadania + A[i].p2
        schedule.assignments.append(JobAssignment(A[i], 2, start_zadania, complete))
        start_zadania = complete

    # Dodawanie zadan do P2 z listy B
    for i in range(0, len(B)):
        n = len(A)
        if listaZadan[i+n].complete > start_zadania:
            start_zadania = listaZadan[i+n].complete
        complete = start_zadania + B[i].p2
        schedule.assignments.append(JobAssignment(B[i], 2, start_zadania, complete))
        start_zadania = complete

    ### KONIEC ROZWIAZANIA
    return schedule

ja = Job("J1", p1=1, p2=2)
jb = Job("J2", p1=3, p2=2)
jc = Job("J3", p1=2, p2=3)
jd = Job("J4", p1=4, p2=4)
je = Job("J5", p1=6, p2=1)
jf = Job("J6", p1=2, p2=1)
jg = Job("J7", p1=1, p2=2)
jh = Job("J8", p1=2, p2=3)

instance = Instance()
instance.jobs = [ja, jb, jc, jd, je, jf, jg, jh]

assert Johnson(instance).cmax() == 22

ja = Job("J1", p1=3, p2=2)
jb = Job("J2", p1=2, p2=3)
jc = Job("J3", p1=4, p2=3)
jd = Job("J4", p1=1, p2=2)
je = Job("J5", p1=1, p2=1)
jf = Job("J6", p1=1, p2=1)

instance = Instance()
instance.jobs = [ja, jb, jc, jd, je, jf]

assert Johnson(instance).cmax() == 14
### BEGIN HIDDEN TESTS
ja = Job("J1", p1=1, p2=2)
jb = Job("J2", p1=5, p2=8)
jc = Job("J3", p1=4, p2=7)
jd = Job("J4", p1=7, p2=11)
je = Job("J5", p1=8, p2=4)
jf = Job("J6", p1=11, p2=2)
jg = Job("J7", p1=2, p2=5)
jh = Job("J8", p1=4, p2=3)

instance = Instance()
instance.jobs = [ja, jb, jc, jd, je, jf, jg, jh]

assert Johnson(instance).cmax() == 44
### END HIDDEN TESTS

print("Wszystko działa")

