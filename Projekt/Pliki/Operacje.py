import pandas as pd
import plotly.express as px

from Projekt.Pliki.Modele import Instance
from Projekt.Pliki.Modele import Job


# odczytuje dane z pliku
# Przy odczycie danych z pliku brane pod uwagę są tylko: zadania które porzebują więcej ramu niż 0, mniej niż 134GB, czas wykonywania zadań jest większy niż 0
def readDataFromCSVFile(filePath, separator):
    df = pd.read_csv(filePath, sep=separator)
    df = df[(df["Memory requirement (KB per CPU)"] > 0) & (df["Memory requirement (KB per CPU)"] <= 140509184) & (
            df["Processing time (s)"] > 0)]
    return df


# Generuje nowe instancje
def genNewInstances(df, sampleCount, instanceCount, processorCount):
    instances = []
    for i in range(instanceCount):
        instance = Instance(machines=processorCount)
        for index, row in df.sample(  # df.sample = funkcja która wybiera wartości losowo
                sampleCount,
                # random_state=123456789 # Pozwala ustawić ziarno/seed, aby wybierane wartości były przewidywane
        ).iterrows():
            memory = row['Memory requirement (KB per CPU)'].item()
            processing_time = row['Processing time (s)'].item()
            key = 'J' + str(index)
            instance.jobs.append(Job(key, processing_time, memory))
        instances.append(instance)
    return instances


# Generuje wykres skrzynkowy
def generateBoxPlot(data, fileName, title):
    df = pd.DataFrame(data=data)
    plot = df.plot.box(title=title)
    fig = plot.get_figure()
    fig.set_size_inches(12, 7)
    fig.savefig(fileName)


# Generuje wykres punktowy
def generateScatterPlot(df, fileName, key1, key2, title):
    fig = px.scatter(df,
                     x=key1,
                     y=key2,
                     color=key1,
                     title=title,
                     width=1280,
                     height=720
                     )
    fig.write_image(fileName)


# Generuje historgram
def generateHistogramPlot(df, fileName, key, title):  # count 10k = 10000 zadań, 1M = 1000 sekund
    fig = px.histogram(df, x=key,
                       title=title,
                       opacity=0.8,
                       log_y=True,  # represent bars with log scale
                       log_x=False,
                       color_discrete_sequence=['#ff3636'],  # color of histogram bars
                       width=1280,
                       height=720
                       )
    fig.write_image(fileName)


# Szuka procasora który ma najmniejszy CMAX
def findLowestCMAXMachine(machines):
    current_index = 0
    for index, machine in enumerate(machines):
        if len(machine) == 0:
            return index
        if machines[current_index][-1].complete > machine[-1].complete:
            current_index = index
    return current_index


# Ustawia domyślne wartości procesoró dla instancji
def setDefaultProcesorValues(instance):
    procesory = [[] for i in range(instance.machines)]
    return procesory


# Sprawdza ile jest dostępnego ramu
def checkFreeRam(assignments_running_now, schedule):
    freeRam = schedule.ram - checkUsedMemory(assignments_running_now)
    return freeRam


# Znajduje czas startu procesora
def getStartTime(machines, machine_index):
    start_time = 0
    if len(machines[machine_index]) > 0:
        start_time = machines[machine_index][-1].complete
    return start_time


def flatten(t):
    return [item for sublist in t for item in sublist]


# Sprawdza ile ramu jest używane w uszeregowaniu
def checkUsedMemory(assignments):
    suma = 0
    for i in assignments:
        suma = suma + i.job.w
    return suma


# Sprawdza obecne uszeregowanie
def getAssignmentsRunningNow(machines, current_machine_index):
    complete_time = 0
    if len(machines[current_machine_index]) > 0:
        complete_time = machines[current_machine_index][-1].complete

    return list(
        filter(lambda a: a.complete > complete_time, flatten(filter(lambda m: len(m) > 0, [m for m in machines]))))
