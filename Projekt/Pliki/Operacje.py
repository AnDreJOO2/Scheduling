import pandas as pd
import random
import plotly.express as px
import matplotlib.pyplot as plt

from Projekt.Pliki.Modele import Job
from Projekt.Pliki.Modele import Instance

# Generuje nowe instancje
def genNewInstances(df, sampleCount,  instanceCount, processorCount):
  instances = []
  for i in range(instanceCount):
    instance = Instance(machines=processorCount)
    for index, row in df.sample( #df.sample = funkcja która wybiera wartości losowo
      sampleCount,
      # random_state=1 # Pozwala ustawić ziarno/seed, aby wybierane wartości były przewidywane
    ).iterrows():
      memory = row['Memory requirement (KB per CPU)'].item()
      processing_time = row['Processing time (s)'].item()
      key = 'J' + str(index)
      instance.jobs.append(Job(key, processing_time, memory))
    instances.append(instance)
  return instances

# Przy odczycie danych z pliku brane pod uwagę są tylko: zadania które porzebują więcej ramu niż 0, mniej niż 134GB, czas wykonywania zadań jest większy niż 0
def readDataFromCSVFile(filePath, separator):
  df = pd.read_csv(filePath, sep=separator)
  df = df[(df["Memory requirement (KB per CPU)"] > 0) & (df["Memory requirement (KB per CPU)"] <= 140509184) & (df["Processing time (s)"] > 0)]
  return df


# Generuje wykres skrzynkowy
def generateBoxPlot(data, fileName, title):
  df = pd.DataFrame(data=data)
  plot = df.plot.box(title=title)
  fig = plot.get_figure()
  fig.set_size_inches(10, 6)
  fig.savefig(fileName)

# Generuje wykres punktowy
def generateScatterPlot(df, fileName, key1, key2):
  fig = px.scatter(
    df, x=key2, y=key1, opacity=0.65,
    trendline="ols", trendline_color_override="darkblue"
  )
  fig.write_image(fileName)

# Generuje historgram
def generateHistogramPlot(df, fileName, key):
  fig = px.histogram(df, x=key)
  fig.write_image(fileName)

# generateHistogramPlot(df, "Memory requirement (KB per CPU)")
# generateHistogramPlot(df, "Processing time (s)")
# generateScatterPlot(df)

# Szuka procasora który ma najmniejszy CMAX
def findLowestCMAXMachine(machines):
  current_index = 0
  for index, machine in enumerate(machines):
    if len(machine) == 0:
      return index
    if machines[current_index][-1].complete > machine[-1].complete:
      current_index = index
  return current_index

def getStartTime(machines, machine_index): # Znajduje czas startu procesora
  start_time = 0
  if len(machines[machine_index]) > 0:
    start_time = machines[machine_index][-1].complete
  return start_time

def flatten(t):
  return [item for sublist in t for item in sublist]

def checkUsedMemory(assignments):
  return sum(assignment.job.w for assignment in assignments)

def getAssignmentsRunningNow(machines, current_machine_index):
  complete_time = 0
  if len(machines[current_machine_index]) > 0:
    complete_time = machines[current_machine_index][-1].complete

  return list(filter(lambda a: a.complete > complete_time, flatten(filter(lambda m: len(m) > 0, [m for m in machines]))))


