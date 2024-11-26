import pandas as pd



incidente = pd.read_excel('incident.xlsx')
task1 = pd.read_excel('sc_task(2).xlsx')
task2 = pd.read_excel('sc_task(3).xlsx')


planilhas = [incidente, task1, task2]

for planilha in planilhas:
    concat = pd.concat(planilha, ignore_index=True)

