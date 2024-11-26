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

            # fazer o replace das colunas especificas
            col_p_mudar = ['Urgência', 'Impacto']
            mapeamento = {"Alto": "High", "Médio": "Medium", "Baixo": "Low"}
            for coluna in colunas_comuns:
                if coluna in df_final.columns:
                    df_final[coluna] = df_final[coluna].replace(mapeamento)
            
            # Preparar o arquivo para download
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df_final.to_excel(writer, index=False, sheet_name='Dados Processados')
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





