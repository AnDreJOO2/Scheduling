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
        return job.mr / 140509184

    def bound(self):
        m1 = sum(job.p / self.machines for job in self.jobs)
        m2 = sum(job.p * self.normalize(job) for job in self.jobs)
        return max(m1, m2)


class Job:
    # Konstruktor
    def __init__(self, i, p, mr):
        assert (isinstance(p, int) and p > 0)
        assert (isinstance(mr, int) and mr > 0)
        self.i = i  # Identyfikator zadania (np. liczba lub ciąg znaków)
        self.p = p  # Czas wykonywania zadania
        self.mr = mr  # Memory

    # Reprezentacja zadania
    def __repr__(self):
        return f"'{self.i}'; p = {self.p}, mr = {self.mr}"


class JobAssignment:
    def __init__(self, j, m, s, c):
        assert (isinstance(j, Job))
        assert (isinstance(m, int) and m > 0)
        assert (isinstance(s, int) and s >= 0)
        assert (isinstance(c, int) and c > s)
        self.job = j  # Zadanie
        self.machine = m  # Procesor, na którym zadanie się wykonuje
        self.start = s  # Czas rozpoczęcia zadania
        self.complete = c  # Czas zakończenia zadania

    def __repr__(self):
        return f"{self.job} ~ machine:{self.machine}[{self.start}; {self.complete})\n"


class Schedule:
    def __init__(self, i):
        assert (isinstance(i, Instance))
        self.instance = i
        self.assignments = []
        self.memory = 140509184  # 134 GB

    def isFeasible(self):
        # current_memory_usage = sum(map(lambda x: x.job.mr, filter(lambda x: x.start >= start or x.complete < start, assignments)))
        # if current_memory_usage > self.memory:
        #     return False

        # Sprawdzenie czy indetyfikator istnieje w jobs
        unique_keys = [job.i for job in self.instance.jobs]
        for assignment_key in [assignment.job.i for assignment in self.assignments]:
            if assignment_key not in unique_keys:
                print('ERROR: Sprawdzenie czy indetyfikator istnieje w jobs: {} {}'.format(assignment_key))
                return False

        # W danej chwili, na danym procesorze, wykonuje się co najwyżej jedno zadanie.
        machcines = {}
        for assignment in self.assignments:
            key = assignment.machine
            if key in machcines:
                machcines[key].append(assignment)
            else:
                machcines[key] = [assignment]

        values = []
        for key in machcines:
            values.append(machcines[key])

        for machine in values:
            for a in machine:
                for aa in machine:
                    if a.job != aa.job:
                        if max(a.start, aa.start) < min(a.complete, aa.complete):
                            print(
                                'ERROR: W danej chwili, na danym procesorze, wykonuje się co najwyżej jedno zadanie: {} {}'.format(
                                    a, aa))
                            return False

        # To samo zadanie nie wykonuje się jednocześnie na więcej niż jednym procesorze.
        for a in self.assignments:
            for aa in self.assignments:
                if a.job == aa.job and a.machine != aa.machine:
                    if max(a.start, aa.start) < min(a.complete, aa.complete):
                        print(
                            'ERROR: To samo zadanie nie wykonuje się jednocześnie na więcej niż jednym procesorze: {} {}'.format(
                                a, aa))
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

        for v in values:
            worked_time = 0
            for k in v:
                worked_time += k.complete - k.start
            if worked_time != v[0].job.p:
                print('Każde zadanie zostało wykonane.: {}'.format(v[0].job.p))
                return False
            
        # Na procesorach wykonują się tylko te zadania, które zostały opisane w instancji problemu.
        if len(self.assignments) != len(self.instance.jobs):
            print('ERROR: Na procesorach wykonują się tylko te zadania, które zostały opisane w instancji problemu')
            return False

        assignment_keys = [assignment.job.i for assignment in self.assignments]
        job_keys = [jobs.i for jobs in self.instance.jobs]
        for job_key in job_keys:
            if not job_key in assignment_keys:
                print('ERROR: Na procesorach wykonują się tylko te zadania, które zostały opisane w instancji problemu')
                return False

        # Żadne zadanie nie wykonuje się na niedostepnym procesorze
        for assignment in self.assignments:
            if assignment.machine < 1 or assignment.machine > self.instance.machines:
                print('ERROR: Żadne zadanie nie wykonuje się na niedostepnym procesorze')
                return False

        return True
        pass

    def cmax(self):
        assert self.isFeasible() == True
        return max(map(lambda x: x.complete, self.assignments))
        pass
