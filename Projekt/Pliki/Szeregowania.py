from copy import deepcopy

from Projekt.Pliki import Operacje
from Projekt.Pliki.Modele import JobAssignment
from Projekt.Pliki.Modele import Schedule


# zgodnie z którą zadania są przydzielane do rdzeni w kolejności losowej
def RND(instance):
    instance = deepcopy(instance)
    schedule = Schedule(instance)
    jobs = deepcopy(schedule.instance.jobs)

    procesory = Operacje.setDefaultProcesorValues(instance)

    while len(jobs) > 0:
        job_index = 0
        job = jobs[job_index]

        machine_index = Operacje.findLowestCMAXMachine(procesory)
        aktualneZadanie = Operacje.getAssignmentsRunningNow(procesory, machine_index)
        freeRam = Operacje.checkFreeRam(aktualneZadanie, schedule)

        if freeRam >= job.w:
            start_time = Operacje.getStartTime(procesory, machine_index)
            procesory[machine_index].append(JobAssignment(job, machine_index + 1, start_time, start_time + job.p))
        else:
            assigned = False
            for i in range(1, len(jobs)):
                if freeRam >= jobs[i].w:
                    job_index = i
                    start_time = Operacje.getStartTime(procesory, machine_index)
                    procesory[machine_index].append(
                        JobAssignment(jobs[job_index], machine_index + 1, start_time, start_time + jobs[job_index].p))
                    assigned = True
                    break

            if assigned == False:
                for assignment_by_complete_time in sorted(aktualneZadanie, key=lambda x: x.complete):
                    freeRam += assignment_by_complete_time.job.w
                    is_assigned = False
                    for i in range(len(jobs)):
                        if freeRam >= jobs[i].w:
                            job_index = i
                            start_time = assignment_by_complete_time.complete
                            procesory[machine_index].append(
                                JobAssignment(jobs[job_index], machine_index + 1, start_time,
                                              start_time + jobs[job_index].p))
                            is_assigned = True
                            break
                    if is_assigned == True:
                        break
        jobs.pop(job_index)

    for m in procesory:
        schedule.assignments += m
    return schedule


# zgodnie z którą zadania są przydzielane do rdzeni począwszy od tego o najmniejszym zapotrzebowaniu na pamięć
def LMR(instance):
    instance = deepcopy(instance)
    schedule = Schedule(instance)

    jobs = sorted(deepcopy(schedule.instance.jobs), key=lambda j: j.w)  # sortowanie zadań według rosnącego ramu

    procesory = Operacje.setDefaultProcesorValues(instance)

    while len(jobs) > 0:
        job_index = 0
        job = jobs[job_index]

        machine_index = Operacje.findLowestCMAXMachine(procesory)
        aktualneZadanie = Operacje.getAssignmentsRunningNow(procesory, machine_index)
        freeRam = Operacje.checkFreeRam(aktualneZadanie, schedule)

        if freeRam >= job.w:
            start_time = Operacje.getStartTime(procesory, machine_index)
            procesory[machine_index].append(JobAssignment(job, machine_index + 1, start_time, start_time + job.p))
        else:
            assigned = False
            for i in range(1, len(jobs)):
                if freeRam >= jobs[i].w:
                    job_index = i
                    start_time = Operacje.getStartTime(procesory, machine_index)
                    procesory[machine_index].append(
                        JobAssignment(jobs[job_index], machine_index + 1, start_time, start_time + jobs[job_index].p))
                    assigned = True
                    break

            if assigned == False:
                for assignment_by_complete_time in sorted(aktualneZadanie, key=lambda x: x.complete):
                    freeRam += assignment_by_complete_time.job.w
                    is_assigned = False
                    for i in range(len(jobs)):
                        if freeRam >= jobs[i].w:
                            job_index = i
                            start_time = assignment_by_complete_time.complete
                            procesory[machine_index].append(
                                JobAssignment(jobs[job_index], machine_index + 1, start_time,
                                              start_time + jobs[job_index].p))
                            is_assigned = True
                            break
                    if is_assigned == True:
                        break
        jobs.pop(job_index)

    for m in procesory:
        schedule.assignments += m
    return schedule


# zgodnie z którą zadania są przydzielane do rdzeni począwszy od tego o największym zapotrzebowaniu na pamięć
def HMR(instance):
    instance = deepcopy(instance)
    schedule = Schedule(instance)
    jobs = sorted(deepcopy(schedule.instance.jobs), key=lambda j: j.w,
                  reverse=True)  # sortowanie zadań według malejącego ramu

    procesory = Operacje.setDefaultProcesorValues(instance)
    while len(jobs) > 0:
        job_index = 0
        job = jobs[job_index]

        machine_index = Operacje.findLowestCMAXMachine(procesory)
        aktualneZadanie = Operacje.getAssignmentsRunningNow(procesory, machine_index)

        freeRam = Operacje.checkFreeRam(aktualneZadanie, schedule)

        if freeRam >= job.w:
            start_time = Operacje.getStartTime(procesory, machine_index)
            procesory[machine_index].append(JobAssignment(job, machine_index + 1, start_time, start_time + job.p))
        else:
            assigned = False
            for i in range(1, len(jobs)):
                if freeRam >= jobs[i].w:
                    job_index = i
                    start_time = Operacje.getStartTime(procesory, machine_index)
                    procesory[machine_index].append(
                        JobAssignment(jobs[job_index], machine_index + 1, start_time, start_time + jobs[job_index].p))
                    assigned = True
                    break

            if assigned == False:
                for assignment_by_complete_time in sorted(aktualneZadanie, key=lambda x: x.complete):
                    freeRam += assignment_by_complete_time.job.w
                    is_assigned = False
                    for i in range(len(jobs)):
                        if freeRam >= jobs[i].w:
                            job_index = i
                            start_time = assignment_by_complete_time.complete
                            procesory[machine_index].append(
                                JobAssignment(jobs[job_index], machine_index + 1, start_time,
                                              start_time + jobs[job_index].p))
                            is_assigned = True
                            break
                    if is_assigned == True:
                        break
        jobs.pop(job_index)

    for m in procesory:
        schedule.assignments += m
    return schedule


# zgodnie z którą zadania są przydzielane do rdzeni począwszy od tego o największym zapotrzebowaniu na czas
def LPT(instance):
    instance = deepcopy(instance)
    schedule = Schedule(instance)
    jobs = sorted(deepcopy(schedule.instance.jobs), key=lambda j: j.p, reverse=True)

    procesory = Operacje.setDefaultProcesorValues(instance)
    while len(jobs) > 0:
        job_index = 0
        job = jobs[job_index]

        machine_index = Operacje.findLowestCMAXMachine(procesory)

        aktualneZadanie = Operacje.getAssignmentsRunningNow(procesory, machine_index)

        freeRam = Operacje.checkFreeRam(aktualneZadanie, schedule)

        if freeRam >= job.w:
            start_time = Operacje.getStartTime(procesory, machine_index)
            procesory[machine_index].append(JobAssignment(job, machine_index + 1, start_time, start_time + job.p))
        else:
            assigned = False
            for i in range(1, len(jobs)):
                if freeRam >= jobs[i].w:
                    job_index = i
                    start_time = Operacje.getStartTime(procesory, machine_index)
                    procesory[machine_index].append(
                        JobAssignment(jobs[job_index], machine_index + 1, start_time, start_time + jobs[job_index].p))
                    assigned = True
                    break

            if assigned == False:
                for assignment_by_complete_time in sorted(aktualneZadanie, key=lambda x: x.complete):
                    freeRam += assignment_by_complete_time.job.w
                    is_assigned = False
                    for i in range(len(jobs)):
                        if freeRam >= jobs[i].w:
                            job_index = i
                            start_time = assignment_by_complete_time.complete
                            procesory[machine_index].append(
                                JobAssignment(jobs[job_index], machine_index + 1, start_time,
                                              start_time + jobs[job_index].p))
                            is_assigned = True
                            break
                    if is_assigned == True:
                        break
        jobs.pop(job_index)

    for m in procesory:
        schedule.assignments += m

    return schedule


# strategia alfa
def ALFA(instance):
    instance = deepcopy(instance)
    schedule = Schedule(instance)
    jobs = sorted(deepcopy(schedule.instance.jobs), key=lambda j: j.p)

    procesory = Operacje.setDefaultProcesorValues(instance)

    while len(jobs) > 0:
        job_index = 0
        job = jobs[job_index]

        machine_index = Operacje.findLowestCMAXMachine(procesory)
        aktualneZadanie = Operacje.getAssignmentsRunningNow(procesory, machine_index)
        freeRam = Operacje.checkFreeRam(aktualneZadanie, schedule)

        if freeRam >= job.w:
            start_time = Operacje.getStartTime(procesory, machine_index)
            procesory[machine_index].append(JobAssignment(job, machine_index + 1, start_time, start_time + job.p))
        else:
            assigned = False
            for i in range(1, len(jobs)):
                if freeRam >= jobs[i].w:
                    job_index = i
                    start_time = Operacje.getStartTime(procesory, machine_index)
                    procesory[machine_index].append(
                        JobAssignment(jobs[job_index], machine_index + 1, start_time, start_time + jobs[job_index].p))
                    assigned = True
                    break

            if assigned == False:
                for assignment_by_complete_time in sorted(aktualneZadanie, key=lambda x: x.complete):
                    freeRam += assignment_by_complete_time.job.w
                    is_assigned = False
                    for i in range(len(jobs)):
                        if freeRam >= jobs[i].w:
                            job_index = i
                            start_time = assignment_by_complete_time.complete
                            procesory[machine_index].append(
                                JobAssignment(jobs[job_index], machine_index + 1, start_time,
                                              start_time + jobs[job_index].p))
                            is_assigned = True
                            break
                    if is_assigned == True:
                        break
        jobs.pop(job_index)

    for m in procesory:
        schedule.assignments += m
    return schedule


# strategia beta
def BETA(instance):
    instance = deepcopy(instance)
    schedule = Schedule(instance)
    jobs = sorted(deepcopy(schedule.instance.jobs), key=lambda j: j.p / j.w)

    procesory = Operacje.setDefaultProcesorValues(instance)
    while len(jobs) > 0:
        job_index = 0
        job = jobs[job_index]

        machine_index = Operacje.findLowestCMAXMachine(procesory)
        aktualneZadanie = Operacje.getAssignmentsRunningNow(procesory, machine_index)
        freeRam = Operacje.checkFreeRam(aktualneZadanie, schedule)

        if freeRam >= job.w:
            start_time = Operacje.getStartTime(procesory, machine_index)
            procesory[machine_index].append(JobAssignment(job, machine_index + 1, start_time, start_time + job.p))
        else:
            assigned = False
            for i in range(1, len(jobs)):
                if freeRam >= jobs[i].w:
                    job_index = i
                    start_time = Operacje.getStartTime(procesory, machine_index)
                    procesory[machine_index].append(
                        JobAssignment(jobs[job_index], machine_index + 1, start_time, start_time + jobs[job_index].p))
                    assigned = True
                    break

            if assigned == False:
                for assignment_by_complete_time in sorted(aktualneZadanie, key=lambda x: x.complete):
                    freeRam += assignment_by_complete_time.job.w
                    is_assigned = False
                    for i in range(len(jobs)):
                        if freeRam >= jobs[i].w:
                            job_index = i
                            start_time = assignment_by_complete_time.complete
                            procesory[machine_index].append(
                                JobAssignment(jobs[job_index], machine_index + 1, start_time,
                                              start_time + jobs[job_index].p))
                            is_assigned = True
                            break
                    if is_assigned == True:
                        break
        jobs.pop(job_index)

    for m in procesory:
        schedule.assignments += m
    return schedule
