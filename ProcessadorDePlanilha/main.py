import pandas as pd
import streamlit as st
from io import BytesIO

st.title("Processador de Planilhas")

planilhas = st.file_uploader(
    "Selecione as Bases de Dados",
    type=["xlsx"],
    accept_multiple_files=True
)


if len(planilhas) == 3:
    if st.button("Processar"):
        try:
            # Ler as duas primeiras planilhas 'sc_task'
            task1 = pd.read_excel(planilhas[0])
            task2 = pd.read_excel(planilhas[1])
            
            # Ler a terceira planilha 'incident'
            incident = pd.read_excel(planilhas[2])
            
            tasks_concatened = pd.concat([task1, task2], ignore_index=True, axis=0)

            def tratament_of_incident_sheet(incident):
                incident_sheet = incident
                if 'Categoria' in incident_sheet.columns:
                    incident_sheet = incident_sheet.drop(columns='Categoria')
                if 'SLA efetuado' in incident_sheet.columns:
                    incident_sheet = incident_sheet.drop(columns='SLA efetuado')
                incident_sheet = incident_sheet.rename(columns={'Tipo de contacto': 'Catálogo', 'Resolvido': 'Fechado'})
                return incident_sheet

            def tratament_of_tasks_sheets(tasks_concatened):
                trated_tasks  = tasks_concatened
                if 'SLA efetuado' in tasks_concatened.columns:
                    trated_tasks = tasks_concatened.drop(columns='SLA efetuado')
                
                return trated_tasks


            tasks = tratament_of_tasks_sheets(tasks_concatened)
            incidents = tratament_of_incident_sheet(incident)



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


            
            nomalized_data = normalize_data(tasks, incidents)

            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
               nomalized_data.to_excel(writer, index=False, sheet_name='Dados Processados')
            processed_data = output.getvalue()
            
            st.download_button(
                label="Baixar Planilha processada",
                data=processed_data,
                file_name="planilha_processada.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception as e:
            st.error(f"Erro no processamento das planilhas: {e}")
else:
    st.warning("Por favor envie exatamente 3 arquivos")





#incidente = incidente.drop(columns=['Categoria','SLA efetuado'])


#print("Colunas apos a exclusão", incidente.columns)





