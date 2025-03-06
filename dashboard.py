import streamlit as st
import pandas as pd
import plotly.express as px
import json

# Configuração da página
st.set_page_config(page_title="Indicadores UTI 2025", layout="wide")

# Dados da tabela com base no documento
data = {
    "Indicador": [
        "Mortalidade ajustada",
        "Necessidade de cuidados de enfermagem (NAS)",
        "Taxa de mortalidade",
        "Taxa de RAS",
        "Densidade de Incidência de Pneumonia Associada à Ventilação Mecânica (PAV)",
        "Taxa de utilização de Ventilação Mecânica (VM)",
        "Presença de Cateter Venoso Central (CVC)",
        "Taxa de infecção de cateter venoso",
        "Presença de Sonda Nasogástrica (SNG)",
        "Taxa de cateter vesical de demora (CVD)",
        "Taxa de absenteísmo",
        "Turnover",
        "Adesão ao Protocolo de Prevenção de PAV",
        "Adesão ao Protocolo de Prevenção de Úlceras por Pressão (UPP)",
        "Média de Permanência",
        "Taxa de Desocupação de UTI",
        "Taxa de Readmissão em até 48h"
    ],
    "Meta": [
        "0%", "80%", "15%", "10%", "5%", "30%", "10%", "5%", "5%", "5%", "2%", "NA", "95%", "95%", "7 dias", "5%", "0%"
    ],
    "Jan": [
        "-1%", "70%", "21%", "12%", "10%", "41%", "14%", "5.95%", "6%", "5.05%", "2.4%", "NA", "90%", "90%", "8 dias", "5%", "0%"
    ],
    "Fev": [
        "0.01%", "75%", "14%", "17%", "8%", "33%", "12%", "5.7%", "5%", "5.7%", "2.5%", "NA", "75%", "75%", "10 dias", "6%", "1%"
    ],
    "Mar": ["NA"] * 17,
    "Abr": ["NA"] * 17,
    "Mai": ["NA"] * 17,
    "Jun": ["NA"] * 17,
    "Jul": ["NA"] * 17,
    "Ago": ["NA"] * 17,
    "Set": ["NA"] * 17,
    "Out": ["NA"] * 17,
    "Nov": ["NA"] * 17,
    "Dez": ["NA"] * 17,
    "2024": ["NA"] * 17
}

# Criar DataFrame
df = pd.DataFrame(data)

# Função para destacar metas alcançadas ou não
def highlight_meta(row):
    styles = [''] * len(row)
    for col in row.index[2:]:  # Ignora as colunas 'Indicador' e 'Meta'
        if row[col] and row[col] != "NA":  # Se a célula tiver valor
            meta = row['Meta']
            value = row[col]
            try:
                if 'dias' in meta:
                    meta_value = float(meta.replace(' dias', '').strip())
                    value_num = float(value.replace(' dias', '').strip())
                    if value_num <= meta_value:
                        styles[row.index.get_loc(col)] = 'background-color: lightgreen'
                    else:
                        styles[row.index.get_loc(col)] = 'background-color: lightcoral'
                elif '%' in meta:
                    meta_value = float(meta.replace('%', '').strip())
                    value_num = float(value.replace('%', '').strip())
                    if value_num <= meta_value:
                        styles[row.index.get_loc(col)] = 'background-color: lightgreen'
                    else:
                        styles[row.index.get_loc(col)] = 'background-color: lightcoral'
                else:
                    meta_value = float(meta.strip())
                    value_num = float(value.strip())
                    if value_num <= meta_value:
                        styles[row.index.get_loc(col)] = 'background-color: lightgreen'
                    else:
                        styles[row.index.get_loc(col)] = 'background-color: lightcoral'
            except ValueError:
                styles[row.index.get_loc(col)] = ''
    return styles

# Título do Dashboard
st.title("Indicadores Unidade de Terapia Intensiva 2025")

# Filtro por Indicador
indicador = st.selectbox("Filtrar por Indicador", ["Todos"] + list(df['Indicador']))

# Filtrar o DataFrame
if indicador != "Todos":
    df_filtered = df[df['Indicador'] == indicador]
else:
    df_filtered = df

# Tabela Editável com Destaque
st.write("### Tabela de Indicadores Mensais")
edited_df = st.data_editor(
    df_filtered.style.apply(highlight_meta, axis=1),
    use_container_width=True,
    num_rows="dynamic"
)

# Gráfico de Tendência Mensal
st.write("### Tendência Mensal")
if indicador != "Todos" and not edited_df.empty:
    # Preparar dados para o gráfico
    months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    values = []
    for month in months:
        value = edited_df[month].iloc[0]
        try:
            values.append(float(value.replace('%', '').replace(' dias', '').strip()) if value != "NA" else None)
        except (ValueError, AttributeError):
            values.append(None)
    
    # Criar DataFrame para o gráfico
    trend_data = pd.DataFrame({
        "Mês": months,
        "Valor": values
    })
    
    # Gráfico de linha
    fig = px.line(trend_data, x="Mês", y="Valor", title=f"Tendência de {indicador}")
    st.plotly_chart(fig, use_container_width=True)

# Seção de Descrições Detalhadas
st.write("### Descrições Detalhadas")
descriptions = {
    "Mortalidade ajustada": "Taxa de mortalidade ajustada para pacientes da UTI, calculada com base em escores de gravidade como SAPS 3. Em janeiro, a taxa foi de -1%, e em fevereiro, 0.01%, ambas dentro da meta de 0%. Ação: Continuar monitorando e mantendo as práticas atuais.",
    "Necessidade de cuidados de enfermagem (NAS)": "Avalia a demanda por cuidados de enfermagem com base na escala NAS. Em janeiro, a taxa foi de 70%, e em fevereiro, 75%, ambas abaixo da meta de 80%. Ação: Aumentar o suporte de enfermagem para atingir a meta.",
    "Taxa de mortalidade": "Taxa geral de mortalidade na UTI. Em janeiro, a taxa foi de 21%, acima da meta de ≤15%. Em fevereiro, melhorou para 14%, atingindo a meta. Ação: Investigar causas da alta mortalidade em janeiro e consolidar melhorias.",
    "Taxa de RAS": "Taxa de eventos adversos na UTI. Em janeiro, a taxa foi de 12%, e em fevereiro, 17%, ambas acima da meta de ≤10%. Ação: Revisar protocolos para reduzir eventos adversos e aumentar a segurança do paciente.",
    "Densidade de Incidência de Pneumonia Associada à Ventilação Mecânica (PAV)": "Incidência de PAV por 1.000 dias de ventilação. Em janeiro, a taxa foi de 10%, e em fevereiro, 8%, ambas acima da meta de ≤5%. Ação: Reforçar protocolos de prevenção de PAV.",
    "Taxa de utilização de Ventilação Mecânica (VM)": "Percentual de pacientes em ventilação mecânica. Em janeiro, a taxa foi de 41%, e em fevereiro, 33%, ambas acima da meta de ≤30%. Ação: Revisar indicações para ventilação mecânica e promover desmame precoce.",
    "Presença de Cateter Venoso Central (CVC)": "Percentual de pacientes com cateter venoso central. Em janeiro, a taxa foi de 14%, e em fevereiro, 12%, ambas acima da meta de ≤10%. Ação: Reduzir o uso desnecessário de cateteres.",
    "Taxa de infecção de cateter venoso": "Incidência de infecção associada ao cateter. Em janeiro, a taxa foi de 5.95%, e em fevereiro, 5.7%, ambas acima da meta de ≤5%. Ação: Melhorar a adesão aos protocolos de inserção e manutenção de cateteres.",
    "Presença de Sonda Nasogástrica (SNG)": "Percentual de pacientes com sonda nasogástrica. Em janeiro, a taxa foi de 6%, e em fevereiro, 5%, ambas dentro da meta de ≤5%. Ação: Monitorar o uso de sondas para evitar complicações.",
    "Taxa de cateter vesical de demora (CVD)": "Percentual de pacientes com cateter vesical. Em janeiro, a taxa foi de 5.05%, e em fevereiro, 5.7%, ambas acima da meta de ≤5%. Ação: Implementar protocolos para remoção precoce de cateteres vesicais.",
    "Taxa de absenteísmo": "Percentual de absenteísmo da equipe. Em janeiro, a taxa foi de 2.4%, e em fevereiro, 2.5%, ambas acima da meta de ≤2%. Ação: Investigar causas do absenteísmo e implementar medidas de suporte à equipe.",
    "Turnover": "Taxa de rotatividade de pessoal. Não foram fornecidos dados para este indicador em janeiro ou fevereiro. Ação: Monitorar e implementar estratégias de retenção de talentos.",
    "Adesão ao Protocolo de Prevenção de PAV": "Percentual de adesão ao protocolo de prevenção de PAV. Em janeiro, a taxa foi de 90%, e em fevereiro, 75%, ambas abaixo da meta de ≥95%. Ação: Reforçar treinamento da equipe.",
    "Adesão ao Protocolo de Prevenção de Úlceras por Pressão (UPP)": "Percentual de adesão ao protocolo de prevenção de UPP. Em janeiro, a taxa foi de 90%, e em fevereiro, 75%, ambas abaixo da meta de ≥95%. Ação: Melhorar a implementação do protocolo.",
    "Média de Permanência": "Média de dias de permanência dos pacientes na UTI. Em janeiro, a média foi de 8 dias, e em fevereiro, 10 dias, ambas acima da meta de ≤7 dias. Ação: Otimizar processos de cuidado para reduzir o tempo de internação.",
    "Taxa de Desocupação de UTI": "Percentual de leitos desocupados na UTI. Em janeiro, a taxa foi de 5%, e em fevereiro, 6%, ambas dentro da meta de 5%. Ação: Continuar monitorando a ocupação de leitos.",
    "Taxa de Readmissão em até 48h": "Percentual de pacientes readmitidos na UTI dentro de 48 horas após a alta. Em janeiro, a taxa foi de 0%, atingindo a meta. Em fevereiro, foi de 1%, acima da meta de 0%. Ação: Investigar causas das readmissões."
}

for idx, row in edited_df.iterrows():
    st.write(f"**{row['Indicador']}**")
    st.write(descriptions.get(row['Indicador'], 'Descrição não disponível.'))

# Botão para salvar os dados editados
if st.button('Salvar Dados'):
    edited_df.to_csv('indicadores_2025.csv', index=False)
    st.success('Dados salvos com sucesso!')

# Exportar dados como JSON
if st.button('Exportar como JSON'):
    edited_df.to_json('indicadores_2025.json', orient='records', force_ascii=False)
    st.success('Dados exportados como JSON com sucesso!')
