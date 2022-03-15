from copy import deepcopy

from Projekt.Pliki import Operacje
from Projekt.Pliki.Modele import JobAssignment
from Projekt.Pliki.Modele import Schedule


# zgodnie z którą zadania są przydzielane do rdzeni w kolejności losowej
def RND(instance):
    instance = deepcopy(instance)
    schedule = Schedule(instance)

    jobs = deepcopy(schedule.instance.jobs)  # Zadania

    procesory = Operacje.setDefaultProcesorValues(
        instance)  # Ustawia domyśle wartości dla każdego procesora, puste tablice

    while len(jobs) > 0:
        job_index = 0
        job = jobs[job_index]

        indexPocecesoraLowestCMAX = Operacje.findLowestCMAXMachine(
            procesory)  # index procesora który ma najmniejszy CMAX

        obecneZadania = Operacje.getAssignmentsRunningNow(procesory,
                                                          indexPocecesoraLowestCMAX)  # obecne zadanie w uszeregowaniu

        freeRam = Operacje.checkFreeRam(obecneZadania,
                                        schedule)  # wartość obecnie wolnej pamięci ram = 134GB - używany ram

        if freeRam >= job.w:  # Jeśli wolny ram jest większy niż ram potrzebny przez zadanie:
            start_time = Operacje.getStartTime(procesory, indexPocecesoraLowestCMAX)
            procesory[indexPocecesoraLowestCMAX].append(
                JobAssignment(job, indexPocecesoraLowestCMAX + 1, start_time, start_time + job.p))
        else:
            zadanieJestprzypisane = False
            for i in range(1, len(jobs)):
                if freeRam >= jobs[i].w:
                    job_index = i
                    start_time = Operacje.getStartTime(procesory, indexPocecesoraLowestCMAX)
                    procesory[indexPocecesoraLowestCMAX].append(
                        JobAssignment(jobs[job_index], indexPocecesoraLowestCMAX + 1, start_time,
                                      start_time + jobs[job_index].p))
                    zadanieJestprzypisane = True
                    break

            if zadanieJestprzypisane == False:
                sortedByComplete = sorted(obecneZadania, key=lambda x: x.complete)
                for assignment_by_complete_time in sortedByComplete:
                    freeRam += assignment_by_complete_time.job.w
                    czyPrzypisano = False

                    for i in range(len(jobs)):

                        if freeRam >= jobs[i].w:
                            job_index = i
                            start_time = assignment_by_complete_time.complete
                            procesory[indexPocecesoraLowestCMAX].append(
                                JobAssignment(jobs[job_index], indexPocecesoraLowestCMAX + 1, start_time,
                                              start_time + jobs[job_index].p))
                            czyPrzypisano = True
                            break
                    if czyPrzypisano == True:
                        break
        jobs.pop(job_index)  # usuwa zadanie z listy

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

        indexPocecesoraLowestCMAX = Operacje.findLowestCMAXMachine(procesory)
        obecneZadania = Operacje.getAssignmentsRunningNow(procesory, indexPocecesoraLowestCMAX)
        freeRam = Operacje.checkFreeRam(obecneZadania, schedule)

        if freeRam >= job.w:
            start_time = Operacje.getStartTime(procesory, indexPocecesoraLowestCMAX)
            procesory[indexPocecesoraLowestCMAX].append(
                JobAssignment(job, indexPocecesoraLowestCMAX + 1, start_time, start_time + job.p))
        else:
            zadanieJestprzypisane = False
            for i in range(1, len(jobs)):
                if freeRam >= jobs[i].w:
                    job_index = i
                    start_time = Operacje.getStartTime(procesory, indexPocecesoraLowestCMAX)
                    procesory[indexPocecesoraLowestCMAX].append(
                        JobAssignment(jobs[job_index], indexPocecesoraLowestCMAX + 1, start_time,
                                      start_time + jobs[job_index].p))
                    zadanieJestprzypisane = True
                    break

            if zadanieJestprzypisane == False:
                sortedByComplete = sorted(obecneZadania, key=lambda x: x.complete)
                for assignment_by_complete_time in sortedByComplete:
                    freeRam += assignment_by_complete_time.job.w
                    czyPrzypisano = False
                    for i in range(len(jobs)):
                        if freeRam >= jobs[i].w:
                            job_index = i
                            start_time = assignment_by_complete_time.complete
                            procesory[indexPocecesoraLowestCMAX].append(
                                JobAssignment(jobs[job_index], indexPocecesoraLowestCMAX + 1, start_time,
                                              start_time + jobs[job_index].p))
                            czyPrzypisano = True
                            break
                    if czyPrzypisano == True:
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

        indexPocecesoraLowestCMAX = Operacje.findLowestCMAXMachine(procesory)
        obecneZadania = Operacje.getAssignmentsRunningNow(procesory, indexPocecesoraLowestCMAX)

        freeRam = Operacje.checkFreeRam(obecneZadania, schedule)

        if freeRam >= job.w:
            start_time = Operacje.getStartTime(procesory, indexPocecesoraLowestCMAX)
            procesory[indexPocecesoraLowestCMAX].append(
                JobAssignment(job, indexPocecesoraLowestCMAX + 1, start_time, start_time + job.p))
        else:
            zadanieJestprzypisane = False
            for i in range(1, len(jobs)):
                if freeRam >= jobs[i].w:
                    job_index = i
                    start_time = Operacje.getStartTime(procesory, indexPocecesoraLowestCMAX)
                    procesory[indexPocecesoraLowestCMAX].append(
                        JobAssignment(jobs[job_index], indexPocecesoraLowestCMAX + 1, start_time,
                                      start_time + jobs[job_index].p))
                    zadanieJestprzypisane = True
                    break

            if zadanieJestprzypisane == False:
                sortedByComplete = sorted(obecneZadania, key=lambda x: x.complete)
                for assignment_by_complete_time in sortedByComplete:
                    freeRam += assignment_by_complete_time.job.w
                    czyPrzypisano = False
                    for i in range(len(jobs)):
                        if freeRam >= jobs[i].w:
                            job_index = i
                            start_time = assignment_by_complete_time.complete
                            procesory[indexPocecesoraLowestCMAX].append(
                                JobAssignment(jobs[job_index], indexPocecesoraLowestCMAX + 1, start_time,
                                              start_time + jobs[job_index].p))
                            czyPrzypisano = True
                            break
                    if czyPrzypisano == True:
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

        indexPocecesoraLowestCMAX = Operacje.findLowestCMAXMachine(procesory)

        obecneZadania = Operacje.getAssignmentsRunningNow(procesory, indexPocecesoraLowestCMAX)

        freeRam = Operacje.checkFreeRam(obecneZadania, schedule)

        if freeRam >= job.w:
            start_time = Operacje.getStartTime(procesory, indexPocecesoraLowestCMAX)
            procesory[indexPocecesoraLowestCMAX].append(
                JobAssignment(job, indexPocecesoraLowestCMAX + 1, start_time, start_time + job.p))
        else:
            zadanieJestprzypisane = False
            for i in range(1, len(jobs)):
                if freeRam >= jobs[i].w:
                    job_index = i
                    start_time = Operacje.getStartTime(procesory, indexPocecesoraLowestCMAX)
                    procesory[indexPocecesoraLowestCMAX].append(
                        JobAssignment(jobs[job_index], indexPocecesoraLowestCMAX + 1, start_time,
                                      start_time + jobs[job_index].p))
                    zadanieJestprzypisane = True
                    break

            if zadanieJestprzypisane == False:
                sortedByComplete = sorted(obecneZadania, key=lambda x: x.complete)
                for assignment_by_complete_time in sortedByComplete:
                    freeRam += assignment_by_complete_time.job.w
                    czyPrzypisano = False
                    for i in range(len(jobs)):
                        if freeRam >= jobs[i].w:
                            job_index = i
                            start_time = assignment_by_complete_time.complete
                            procesory[indexPocecesoraLowestCMAX].append(
                                JobAssignment(jobs[job_index], indexPocecesoraLowestCMAX + 1, start_time,
                                              start_time + jobs[job_index].p))
                            czyPrzypisano = True
                            break
                    if czyPrzypisano == True:
                        break
        jobs.pop(job_index)

    for m in procesory:
        schedule.assignments += m

    return schedule


# strategia alfa
def ALFA(instance):
    instance = deepcopy(instance)
    schedule = Schedule(instance)
    jobs = sorted(deepcopy(schedule.instance.jobs), key=lambda j: j.p)  # sortowanie przez czas wykoniania zadania

    procesory = Operacje.setDefaultProcesorValues(instance)

    while len(jobs) > 0:  # dopóki są zadania wykonuj:
        job_index = 0
        job = jobs[job_index]

        indexPocecesoraLowestCMAX = Operacje.findLowestCMAXMachine(procesory)
        obecneZadania = Operacje.getAssignmentsRunningNow(procesory, indexPocecesoraLowestCMAX)
        freeRam = Operacje.checkFreeRam(obecneZadania, schedule)

        if freeRam >= job.w:
            start_time = Operacje.getStartTime(procesory, indexPocecesoraLowestCMAX)
            procesory[indexPocecesoraLowestCMAX].append(
                JobAssignment(job, indexPocecesoraLowestCMAX + 1, start_time, start_time + job.p))
        else:
            zadanieJestprzypisane = False
            for i in range(1, len(jobs)):
                if freeRam >= jobs[i].w:
                    job_index = i
                    start_time = Operacje.getStartTime(procesory, indexPocecesoraLowestCMAX)
                    procesory[indexPocecesoraLowestCMAX].append(
                        JobAssignment(jobs[job_index], indexPocecesoraLowestCMAX + 1, start_time,
                                      start_time + jobs[job_index].p))
                    zadanieJestprzypisane = True
                    break

            if zadanieJestprzypisane == False:

                sortedByComplete = sorted(obecneZadania, key=lambda x: x.complete)

                for assignment_by_complete_time in sortedByComplete:
                    freeRam += assignment_by_complete_time.job.w
                    czyPrzypisano = False
                    for i in range(len(jobs)):
                        if freeRam >= jobs[i].w:
                            job_index = i
                            start_time = assignment_by_complete_time.complete
                            procesory[indexPocecesoraLowestCMAX].append(
                                JobAssignment(jobs[job_index], indexPocecesoraLowestCMAX + 1, start_time,
                                              start_time + jobs[job_index].p))
                            czyPrzypisano = True
                            break
                    if czyPrzypisano == True:
                        break
        jobs.pop(job_index)

    for m in procesory:
        schedule.assignments += m
    return schedule


# strategia beta
def BETA(instance):
    instance = deepcopy(instance)
    schedule = Schedule(instance)

    posortowaneJoby = sorted(deepcopy(schedule.instance.jobs), key=lambda j: j.p / j.w)  # czas wykonania / pamięć ram

    procesory = Operacje.setDefaultProcesorValues(instance)
    while len(posortowaneJoby) > 0:
        job_index = 0
        job = posortowaneJoby[job_index]

        indexPocecesoraLowestCMAX = Operacje.findLowestCMAXMachine(procesory)
        obecneZadania = Operacje.getAssignmentsRunningNow(procesory, indexPocecesoraLowestCMAX)
        freeRam = Operacje.checkFreeRam(obecneZadania, schedule)

        if freeRam >= job.w:
            start_time = Operacje.getStartTime(procesory, indexPocecesoraLowestCMAX)
            procesory[indexPocecesoraLowestCMAX].append(
                JobAssignment(job, indexPocecesoraLowestCMAX + 1, start_time, start_time + job.p))
        else:
            zadanieJestprzypisane = False
            for i in range(1, len(posortowaneJoby)):
                if freeRam >= posortowaneJoby[i].w:
                    job_index = i
                    start_time = Operacje.getStartTime(procesory, indexPocecesoraLowestCMAX)
                    procesory[indexPocecesoraLowestCMAX].append(
                        JobAssignment(posortowaneJoby[job_index], indexPocecesoraLowestCMAX + 1, start_time,
                                      start_time + posortowaneJoby[job_index].p))
                    zadanieJestprzypisane = True
                    break

            if zadanieJestprzypisane == False:

                sortedByComplete = sorted(obecneZadania, key=lambda x: x.complete)

                for assignment_by_complete_time in sortedByComplete:
                    freeRam += assignment_by_complete_time.job.w
                    czyPrzypisano = False
                    for i in range(len(posortowaneJoby)):
                        if freeRam >= posortowaneJoby[i].w:
                            job_index = i
                            start_time = assignment_by_complete_time.complete
                            procesory[indexPocecesoraLowestCMAX].append(
                                JobAssignment(posortowaneJoby[job_index], indexPocecesoraLowestCMAX + 1, start_time,
                                              start_time + posortowaneJoby[job_index].p))
                            czyPrzypisano = True
                            break
                    if czyPrzypisano == True:
                        break
        posortowaneJoby.pop(job_index)

    for m in procesory:
        schedule.assignments += m
    return schedule
