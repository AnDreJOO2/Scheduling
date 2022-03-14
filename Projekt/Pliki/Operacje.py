import pandas as pd
import random
import plotly.express as px

from Projekt.Pliki.Modele import Job
from Projekt.Pliki.Modele import Instance

def generateInstances(df, NUM_OF_INSTANCES=30, NUM_OF_MACHINES=16, NUM_OF_SAMPLE=100):
  instances = []
  for i in range(NUM_OF_INSTANCES):
    instance = Instance(machines=NUM_OF_MACHINES)
    for index, row in df.sample(
      NUM_OF_SAMPLE,
      # random_state=1
    ).iterrows():
      memory = row['Memory requirement (KB per CPU)'].item()
      processing_time = row['Processing time (s)'].item()
      key = 'J' + str(index)
      instance.jobs.append(Job(key, processing_time, memory))
    instances.append(instance)
  return instances

df = pd.read_csv("./zapat.csv", sep=";")
df = df[(df["Memory requirement (KB per CPU)"] > 0) & (df["Memory requirement (KB per CPU)"] <= 140509184) & (df["Processing time (s)"] > 0)]

def generateBoxPlot(data, title, filename):
  df = pd.DataFrame(data=data)
  plot = df.plot.box(title=title)
  fig = plot.get_figure()
  fig.set_size_inches(10, 6)
  fig.savefig(filename)

def generateScatterPlot(df):
  fig = px.scatter(
    df, x="Processing time (s)", y="Memory requirement (KB per CPU)", opacity=0.65,
    trendline="ols", trendline_color_override="darkblue"
  )
  fig.show()

def generateHistogramPlot(df, key):
  fig = px.histogram(df, x=key)
  fig.show()

# generateHistogramPlot(df, "Memory requirement (KB per CPU)")
# generateHistogramPlot(df, "Processing time (s)")
generateScatterPlot(df)

def flatten(t):
  return [item for sublist in t for item in sublist]

def getMemoryUsage(assignments):
  return sum(assignment.job.mr for assignment in assignments)

def getAssignmentsRunningNow(machines, current_machine_index):
  complete_time = 0
  if len(machines[current_machine_index]) > 0:
    complete_time = machines[current_machine_index][-1].complete

  return list(filter(lambda a: a.complete > complete_time, flatten(filter(lambda m: len(m) > 0, [m for m in machines]))))

def getMachineIndexWithLowestCMAX(machines):
  current_index = 0
  for index, machine in enumerate(machines):
    if len(machine) == 0:
      return index
    if machines[current_index][-1].complete > machine[-1].complete:
      current_index = index
  return current_index

def getStartTime(machines, machine_index):
  start_time = 0
  if len(machines[machine_index]) > 0:
    start_time = machines[machine_index][-1].complete
  return start_time

def countAssignments(assignments):
  return sum(len(m) for m in assignments)