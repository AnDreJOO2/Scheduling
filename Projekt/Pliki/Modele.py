import random
import numpy as np
from sklearn import preprocessing

class Instance:
    def __init__(self, machines=16):
        self.jobs = []
        assert (isinstance(machines, int) and machines > 0)
        self.machines = machines

    def generate(self, n, pmin=1, pmax=1):
        for i in range(1, n + 1):
            self.jobs.append(Job("J" + str(len(self.jobs) + 1), random.randint(pmin, pmax)))

    def normalize(self, job):
        return job.w / 140509184

    def bound(self):
        m1 = sum(job.p / self.machines for job in self.jobs)
        m2 = sum(job.p * self.normalize(job) for job in self.jobs)
        return max(m1, m2)


class Job:
    # Konstruktor
    def __init__(self, i, p, w):
        assert (isinstance(p, int) and p > 0)
        assert (isinstance(w, int) and w > 0)
        self.i = i  # Identyfikator zadania (np. liczba lub ciąg znaków)
        self.p = p  # Czas wykonywania zadania
        self.w = w  # Waga zadania (Pamięć ram)

    # Reprezentacja zadania
    def __repr__(self):
        return f"'{self.i}'; p = {self.p}, w = {self.w}"


class JobAssignment:
    def __init__(self, j, m, s, c):
        assert (isinstance(j, Job))
        assert (isinstance(m, int) and m > 0)
        assert (isinstance(s, int) and s >= 0)
        assert (isinstance(c, int) and c > s)
        self.job = j  # Id zadania
        self.machine = m  # Procesor
        self.start = s  # Czas rozpoczęcia zadania
        self.complete = c  # Czas zakończenia zadania

    def __repr__(self):
        return f"{self.job} ~ machine:{self.machine}[{self.start}; {self.complete})\n"


class Schedule:
    def __init__(self, i):
        assert (isinstance(i, Instance))
        self.instance = i
        self.assignments = []
        self.ram = 140509184  # 140509184KB /1024/1024 =  134 GB

    def isFeasible(self):
        listaZadan = self.assignments
        n = len(listaZadan)

        # Sprawdzenie czy id istnieje w jobs
        instacjaJobs = self.instance.jobs
        a = len(instacjaJobs)
        listaId = []
        for i in range(0, a):
            listaId.append(instacjaJobs[i].i)

        #Sprawdzenie czy id istnieje w jobs
        unique_keys = [job.i for job in self.instance.jobs]
        for assignment_key in [assignment.job.i for assignment in self.assignments]:
            if assignment_key not in unique_keys:
                return False

        # W danej chwili, na danym procesorze, wykonuje się co najwyżej jedno zadanie.
        machines = {}
        for assignment in self.assignments:
            key = assignment.machine
            if key in machines:
                machines[key].append(assignment)
            else:
                machines[key] = [assignment]

        # W danej chwili, na danym procesorze, wykonuje się co najwyżej jedno zadanie.
        for i in range(0, n - 1):
            for j in range(i + 1, n):
                if listaZadan[i].machine == listaZadan[j].machine:
                    zakres = range(listaZadan[i].start + 1, listaZadan[i].complete)
                    if listaZadan[j].start in zakres or listaZadan[j].complete in zakres:
                        return False

        # Na procesorach wykonują się tylko te zadania, które zostały opisane w instancji problemu.
        if len(self.assignments) != len(self.instance.jobs):
                return False

        # Żadne zadanie nie wykonuje się na niedostepnym procesorze
        for assignment in self.assignments:
            if assignment.machine < 1 or assignment.machine > self.instance.machines:
                return False

        # To samo zadanie nie wykonuje się jednocześnie na więcej niż jednym procesorze.
        for i in range(0, n - 1):
            for j in range(i + 1, n):
                if listaZadan[i].job.i == listaZadan[j].job.i:
                    if listaZadan[i].machine != listaZadan[j].machine:
                        zakres = range(listaZadan[i].start + 1, listaZadan[i].complete)
                        if listaZadan[j].start in zakres or listaZadan[j].complete in zakres:
                            return False

        jobs = {}
        for assignment in self.assignments:
            key = assignment.job.i
            if key in jobs:
                jobs[key].append(assignment)
            else:
                jobs[key] = [assignment]

        values = []
        for key in jobs:
            values.append(jobs[key])

        #Każde zadanie zostało wykonane
        for v in values:
            worked_time = 0
            for k in v:
                worked_time += k.complete - k.start
            if worked_time != v[0].job.p:
                return False


        #Na procesorach wykonują się tylko te zadania, które zostały opisane w instancji problemu
        assignment_keys = [assignment.job.i for assignment in self.assignments]
        job_keys = [jobs.i for jobs in self.instance.jobs]
        for job_key in job_keys:
            if not job_key in assignment_keys:
                return False

        return True


    def cmax(self):
        assert self.isFeasible() == True
        return max(map(lambda x: x.complete, self.assignments))
        pass
