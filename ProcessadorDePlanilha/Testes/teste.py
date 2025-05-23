import pandas as pd



incidente = pd.read_excel('ProcessadorDePlanilha\Testes\incident(2).xlsx')
task1 = pd.read_excel('ProcessadorDePlanilha\Testes\sc_task.xlsx')
task2 = pd.read_excel('ProcessadorDePlanilha\Testes\sc_task(1).xlsx')

tasks_concatened = pd.concat([task1, task2], ignore_index=True, axis=0)




def tratament_of_incident_sheet(incidente):
    incidente_sheet = incidente
    if 'Categoria' in incidente_sheet.columns:
        incidente_sheet = incidente_sheet.drop(columns='Categoria')
    if 'SLA efetuado' in incidente_sheet.columns:
        incidente_sheet = incidente_sheet.drop(columns='SLA efetuado')
    incidente_sheet = incidente_sheet.rename(columns={'Tipo de contacto': 'Catálogo', 'Resolvido': 'Fechado'})
    return incidente_sheet

def tratament_of_tasks_sheets(tasks_concatened):
    trated_tasks  = tasks_concatened
    if 'SLA efetuado' in tasks_concatened.columns:
        trated_tasks = tasks_concatened.drop(columns='SLA efetuado')
    
    return trated_tasks

tasks_test = tratament_of_tasks_sheets(tasks_concatened)
incidente_test = tratament_of_incident_sheet(incidente)


def normalize_data(taks_final, incidente_final):
    tasks = taks_final
    incidents = incidente_final
    normalized_data = pd.concat([tasks, incidents], axis=0, ignore_index=True)
    
    cols_to_change = ['Urgência', 'Impacto']
    changing_mapping = {'Alto' : 'High', 'Médio': 'Medium', 'Baixo': 'Low'}

    for col in normalized_data.columns:
        if col in cols_to_change:
            normalized_data[col] = normalized_data[col].replace(changing_mapping)


    return normalized_data



nomalized_test = normalize_data(tasks_test, incidente_test)


'''

print("Accounts sheet\n")
print(task1.head())

print("Tasks sheet\n")
print(task2.head())

print("Tasks concatened\n")
print(tasks_concatened.head())
'''
#print(task1.head())


#print("Index apos")
#print(tratament_of_incident_sheet(incidente.head()))






'''

df1 = pd.read_excel(planilhas[0])
df2 = pd.read_excel(planilhas[1])

# Ler a terceira planilha 'incident'
df3 = pd.read_excel(planilhas[2])

# Remover a coluna 'Categoria' da planilha 'incident' se existir
if 'Categoria' in df3.columns:
    df3 = df3.drop(columns='Categoria')

# Concatenar as duas primeiras planilhas 'sc_task'
df_sc_task = pd.concat([df1, df2], axis=0, ignore_index=True)

# Ajustar a planilha 'incident' para alinhar com 'sc_task'
df3_adjusted = df3.rename(columns={'Canal': 'Catálogo', 'Resolvido': 'Fechado a'})

# Manter apenas as colunas de 'sc_task' que estão presentes em 'incident'
colunas_comuns = [col for col in df_sc_task.columns if col in df3_adjusted.columns]
df3_aligned = df3_adjusted[colunas_comuns]

# Concatenar as planilhas verticalmente
df_final = pd.concat([df_sc_task, df3_aligned], axis=0, ignore_index=True)
'''

