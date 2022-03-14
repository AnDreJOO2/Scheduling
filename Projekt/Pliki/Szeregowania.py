from copy import deepcopy
import random

from Projekt.Pliki.Modele import JobAssignment
from Projekt.Pliki.Modele import Schedule

from Projekt.Pliki import Operacje

def RND(instance):
  instance = deepcopy(instance)
  schedule = Schedule(instance)
  jobs = deepcopy(schedule.instance.jobs)
  random.shuffle(jobs)

  machines = [[] for i in range(instance.machines)]
  while len(jobs) > 0:
    job_index = 0
    job = jobs[job_index]

    machine_index = Operacje.getMachineIndexWithLowestCMAX(machines)
    assignments_running_now = Operacje.getAssignmentsRunningNow(machines, machine_index)
    available_memory  = schedule.ram - Operacje.getMemoryUsage(assignments_running_now)

    if available_memory >= job.w:
      start_time = Operacje.getStartTime(machines, machine_index)
      machines[machine_index].append(JobAssignment(job, machine_index + 1, start_time, start_time + job.p))
    else:
      assigned = False
      for i in range(1, len(jobs)):
        if available_memory >= jobs[i].w:
          job_index = i
          start_time = Operacje.getStartTime(machines, machine_index)
          machines[machine_index].append(JobAssignment(jobs[job_index], machine_index + 1, start_time, start_time + jobs[job_index].p))
          assigned = True
          break

      if assigned == False:
        for assignment_by_complete_time in sorted(assignments_running_now, key=lambda x: x.complete):
          available_memory += assignment_by_complete_time.job.w
          is_assigned = False
          for i in range(len(jobs)):
            if available_memory >= jobs[i].w:
              job_index = i
              start_time = assignment_by_complete_time.complete
              machines[machine_index].append(JobAssignment(jobs[job_index], machine_index + 1, start_time, start_time + jobs[job_index].p))
              is_assigned = True
              break
          if is_assigned == True:
            break
    jobs.pop(job_index)

  for m in machines:
    schedule.assignments += m
  pass
  return schedule

def LPT(instance):
  instance = deepcopy(instance)
  schedule = Schedule(instance)
  jobs = sorted(deepcopy(schedule.instance.jobs), key=lambda j: j.p, reverse=True)

  machines = [[] for i in range(instance.machines)]
  while len(jobs) > 0:
    job_index = 0
    job = jobs[job_index]

    machine_index = Operacje.getMachineIndexWithLowestCMAX(machines)
    assignments_running_now = Operacje.getAssignmentsRunningNow(machines, machine_index)
    available_memory  = schedule.ram - Operacje.getMemoryUsage(assignments_running_now)

    if available_memory >= job.w:
      start_time = Operacje.getStartTime(machines, machine_index)
      machines[machine_index].append(JobAssignment(job, machine_index + 1, start_time, start_time + job.p))
    else:
      assigned = False
      for i in range(1, len(jobs)):
        if available_memory >= jobs[i].w:
          job_index = i
          start_time = Operacje.getStartTime(machines, machine_index)
          machines[machine_index].append(JobAssignment(jobs[job_index], machine_index + 1, start_time, start_time + jobs[job_index].p))
          assigned = True
          break

      if assigned == False:
        for assignment_by_complete_time in sorted(assignments_running_now, key=lambda x: x.complete):
          available_memory += assignment_by_complete_time.job.w
          is_assigned = False
          for i in range(len(jobs)):
            if available_memory >= jobs[i].w:
              job_index = i
              start_time = assignment_by_complete_time.complete
              machines[machine_index].append(JobAssignment(jobs[job_index], machine_index + 1, start_time, start_time + jobs[job_index].p))
              is_assigned = True
              break
          if is_assigned == True:
            break
    jobs.pop(job_index)

  for m in machines:
    schedule.assignments += m
  pass
  return schedule

def LMR(instance):
  instance = deepcopy(instance)
  schedule = Schedule(instance)
  jobs = sorted(deepcopy(schedule.instance.jobs), key=lambda j: j.w)

  machines = [[] for i in range(instance.machines)]
  while len(jobs) > 0:
    job_index = 0
    job = jobs[job_index]

    machine_index = Operacje.getMachineIndexWithLowestCMAX(machines)
    assignments_running_now = Operacje.getAssignmentsRunningNow(machines, machine_index)
    available_memory  = schedule.ram - Operacje.getMemoryUsage(assignments_running_now)

    if available_memory >= job.w:
      start_time = Operacje.getStartTime(machines, machine_index)
      machines[machine_index].append(JobAssignment(job, machine_index + 1, start_time, start_time + job.p))
    else:
      assigned = False
      for i in range(1, len(jobs)):
        if available_memory >= jobs[i].w:
          job_index = i
          start_time = Operacje.getStartTime(machines, machine_index)
          machines[machine_index].append(JobAssignment(jobs[job_index], machine_index + 1, start_time, start_time + jobs[job_index].p))
          assigned = True
          break

      if assigned == False:
        for assignment_by_complete_time in sorted(assignments_running_now, key=lambda x: x.complete):
          available_memory += assignment_by_complete_time.job.w
          is_assigned = False
          for i in range(len(jobs)):
            if available_memory >= jobs[i].w:
              job_index = i
              start_time = assignment_by_complete_time.complete
              machines[machine_index].append(JobAssignment(jobs[job_index], machine_index + 1, start_time, start_time + jobs[job_index].p))
              is_assigned = True
              break
          if is_assigned == True:
            break
    jobs.pop(job_index)

  for m in machines:
    schedule.assignments += m
  pass
  return schedule

def HMR(instance):
  instance = deepcopy(instance)
  schedule = Schedule(instance)
  jobs = sorted(deepcopy(schedule.instance.jobs), key=lambda j: j.w, reverse=True)

  machines = [[] for i in range(instance.machines)]
  while len(jobs) > 0:
    job_index = 0
    job = jobs[job_index]

    machine_index = Operacje.getMachineIndexWithLowestCMAX(machines)
    assignments_running_now = Operacje.getAssignmentsRunningNow(machines, machine_index)
    available_memory  = schedule.ram - Operacje.getMemoryUsage(assignments_running_now)

    if available_memory >= job.w:
      start_time = Operacje.getStartTime(machines, machine_index)
      machines[machine_index].append(JobAssignment(job, machine_index + 1, start_time, start_time + job.p))
    else:
      assigned = False
      for i in range(1, len(jobs)):
        if available_memory >= jobs[i].w:
          job_index = i
          start_time = Operacje.getStartTime(machines, machine_index)
          machines[machine_index].append(JobAssignment(jobs[job_index], machine_index + 1, start_time, start_time + jobs[job_index].p))
          assigned = True
          break

      if assigned == False:
        for assignment_by_complete_time in sorted(assignments_running_now, key=lambda x: x.complete):
          available_memory += assignment_by_complete_time.job.w
          is_assigned = False
          for i in range(len(jobs)):
            if available_memory >= jobs[i].w:
              job_index = i
              start_time = assignment_by_complete_time.complete
              machines[machine_index].append(JobAssignment(jobs[job_index], machine_index + 1, start_time, start_time + jobs[job_index].p))
              is_assigned = True
              break
          if is_assigned == True:
            break
    jobs.pop(job_index)

  for m in machines:
    schedule.assignments += m
  pass
  return schedule

def ALFA(instance):
  instance = deepcopy(instance)
  schedule = Schedule(instance)
  jobs = sorted(deepcopy(schedule.instance.jobs), key=lambda j: j.p)

  machines = [[] for i in range(instance.machines)]
  while len(jobs) > 0:
    job_index = 0
    job = jobs[job_index]

    machine_index = Operacje.getMachineIndexWithLowestCMAX(machines)
    assignments_running_now = Operacje.getAssignmentsRunningNow(machines, machine_index)
    available_memory  = schedule.ram - Operacje.getMemoryUsage(assignments_running_now)

    if available_memory >= job.w:
      start_time = Operacje.getStartTime(machines, machine_index)
      machines[machine_index].append(JobAssignment(job, machine_index + 1, start_time, start_time + job.p))
    else:
      assigned = False
      for i in range(1, len(jobs)):
        if available_memory >= jobs[i].w:
          job_index = i
          start_time = Operacje.getStartTime(machines, machine_index)
          machines[machine_index].append(JobAssignment(jobs[job_index], machine_index + 1, start_time, start_time + jobs[job_index].p))
          assigned = True
          break

      if assigned == False:
        for assignment_by_complete_time in sorted(assignments_running_now, key=lambda x: x.complete):
          available_memory += assignment_by_complete_time.job.w
          is_assigned = False
          for i in range(len(jobs)):
            if available_memory >= jobs[i].w:
              job_index = i
              start_time = assignment_by_complete_time.complete
              machines[machine_index].append(JobAssignment(jobs[job_index], machine_index + 1, start_time, start_time + jobs[job_index].p))
              is_assigned = True
              break
          if is_assigned == True:
            break
    jobs.pop(job_index)

  for m in machines:
    schedule.assignments += m
  pass
  return schedule

def BETA(instance):
  instance = deepcopy(instance)
  schedule = Schedule(instance)
  jobs = sorted(deepcopy(schedule.instance.jobs), key=lambda j: j.p / j.w)

  machines = [[] for i in range(instance.machines)]
  while len(jobs) > 0:
    job_index = 0
    job = jobs[job_index]

    machine_index = Operacje.getMachineIndexWithLowestCMAX(machines)
    assignments_running_now = Operacje.getAssignmentsRunningNow(machines, machine_index)
    available_memory  = schedule.ram - Operacje.getMemoryUsage(assignments_running_now)

    if available_memory >= job.w:
      start_time = Operacje.getStartTime(machines, machine_index)
      machines[machine_index].append(JobAssignment(job, machine_index + 1, start_time, start_time + job.p))
    else:
      assigned = False
      for i in range(1, len(jobs)):
        if available_memory >= jobs[i].w:
          job_index = i
          start_time = Operacje.getStartTime(machines, machine_index)
          machines[machine_index].append(JobAssignment(jobs[job_index], machine_index + 1, start_time, start_time + jobs[job_index].p))
          assigned = True
          break

      if assigned == False:
        for assignment_by_complete_time in sorted(assignments_running_now, key=lambda x: x.complete):
          available_memory += assignment_by_complete_time.job.w
          is_assigned = False
          for i in range(len(jobs)):
            if available_memory >= jobs[i].w:
              job_index = i
              start_time = assignment_by_complete_time.complete
              machines[machine_index].append(JobAssignment(jobs[job_index], machine_index + 1, start_time, start_time + jobs[job_index].p))
              is_assigned = True
              break
          if is_assigned == True:
            break
    jobs.pop(job_index)

  for m in machines:
    schedule.assignments += m
  pass
  return schedule