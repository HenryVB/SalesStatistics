import pandas as pd
import plotly.express as px
import streamlit as st


def get_excel_data(excel_file):
    # Consideramos solo estas columnas para el analisis
    valid_cols = ['Probabilidad', 'Valor en la divisa de la empresa',
                  'Propietario del negocio', 'Fuente de la Oportunidad', 'Origen Campaña',
                  'Nombre de la empresa',
                  'Fecha de cierre', 'Etapa del negocio',
                  'Deal ID', 'Company ID']

    sales_data = pd.read_excel(io=excel_file,
                               engine='openpyxl',
                               sheet_name=1,
                               usecols=valid_cols)

    return sales_data


def transform_clean_sales_data(sales_data):
    # Tranformamos los valores 'sin valor' en 0 para un mejor manejo de la data
    sales_data['Valor en la divisa de la empresa'] = sales_data['Valor en la divisa de la empresa'].replace(
        '(Sin valor)', 0)

    # Convertimos la columna divisa a float
    sales_data['Valor en la divisa de la empresa'] = sales_data['Valor en la divisa de la empresa'].astype(float)

    # Agregamos columna de mes y anio en base a la fecha
    sales_data['Mes Cierre'] = sales_data['Fecha de cierre'].dt.month
    sales_data['Anio Cierre'] = sales_data['Fecha de cierre'].dt.year


def get_df_prob_distribution(sales_data):
    # Agrupame por probabilidad y se calcula la cantidad y luego el percentage
    sum_dist_prob_df = sales_data.groupby('Probabilidad').size().reset_index(name='Cantidad')
    sum_dist_prob_df['Porcentaje'] = (sum_dist_prob_df['Cantidad'] / sum_dist_prob_df['Cantidad'].sum()) * 100
    return sum_dist_prob_df


def get_df_performance_owner(sales_data):
    # Agrupar por 'Propietario del negocio'y calcular el valor generado por cada propietario
    performance_owner_df = sales_data.groupby('Propietario del negocio')[
        'Valor en la divisa de la empresa'].sum().reset_index(name="Total Valor Generado")

    # Ordenamos de forma descendente
    performance_owner_df = performance_owner_df.sort_values(by='Total Valor Generado', ascending=False)

    return performance_owner_df


def get_df_prob_total_value(sales_data):
    prob_total_value_df = sales_data.groupby('Probabilidad')[
        'Valor en la divisa de la empresa'].sum().reset_index(name="Total Valor Generado")
    return prob_total_value_df


def get_df_deals_by_month(sales_data):
    # Group data by closing month and calculate count of opportunities
    opportunities_by_month_df = sales_data.groupby(['Anio Cierre', 'Mes Cierre']).size().reset_index(name='Cantidad')
    return opportunities_by_month_df


def get_df_company_total_value(sales_data, top_number=5):
    company_total_value_df = sales_data.groupby('Nombre de la empresa')[
        'Valor en la divisa de la empresa'].sum().reset_index(name="Total Valor Generado")
    return company_total_value_df.sort_values(by='Total Valor Generado', ascending=False).head(top_number)


def create_graph_first_insight(summary_df):
    # Plotting the pie chart using Plotly
    fig = px.pie(summary_df, values='Porcentaje', names='Probabilidad',
                 title='Distribución de oportunidades por Probabilidad')
    # Show the plot
    return fig


def create_graph_second_insight(summary_df):

    # Plotting the bar chart using Plotly
    fig = px.bar(summary_df, x='Propietario del negocio', y='Total Valor Generado', text_auto=',.0f',
                 title='Performance por Propietario de Negocio', labels={'Total Valor Generado': 'Total Valor Generado'}
                 )

    # Format y-axis with thousand separators
    fig.update_yaxes(tickformat=",.0f")

    # Adding a horizontal line to symbolize the threshold
    threshold = 500000  # Example threshold value
    fig.add_hline(y=threshold, line_dash="dash", line_color="red", name='Threshold')

    fig.update_layout(xaxis_tickangle=-45)

    # Add labels above each bar
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

    return fig


def create_graph_third_insight(summary_df):
    # Plotting the bar chart using Plotly
    fig = px.bar(summary_df, x='Probabilidad', y='Total Valor Generado', text_auto=',.0f',
                 title='Impacto de Probabilidad en Valor total')

    # Format y-axis with thousand separators and rotate labels 45 grados
    fig.update_yaxes(tickformat=",.0f")
    fig.update_layout(xaxis_tickangle=-45)

    # Add labels above each bar
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

    return fig


def create_graph_fourth_insight(df_deals_month):
    # Plotting with Plotly
    fig = px.line(df_deals_month, x='Mes Cierre', y='Cantidad', color='Anio Cierre',
                  markers=True, title='Análisis Temporal de Oportunidades',
                  labels={'Mes Cierre': 'Mes', 'Cantidad': 'Cantidad de Oportunidades'})

    # Set x-axis ticks for each month
    fig.update_xaxes(tickvals=list(range(1, 13)))

    return fig


def init_config_st_page(title):
    # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
    st.set_page_config(page_title=title, page_icon=":bar_chart:", layout="wide")
    st.title(f":bar_chart: {title}")
    st.markdown("##")


def set_general_dashboard_info(sales_data):
    total_sales_value = sales_data['Valor en la divisa de la empresa'].sum()
    average_deal_size = sales_data[sales_data['Probabilidad'] == 'Ganada']['Valor en la divisa de la empresa'].mean()
    conversion_rate = (len(sales_data[sales_data['Probabilidad'] == 'Ganada']) / len(sales_data)) * 100
    lost_rate = (len(sales_data[sales_data['Probabilidad'] != 'Ganada']) / len(sales_data)) * 100

    left_column, middle_column, right_column, right_column_2 = st.columns(4)
    with left_column:
        st.subheader("Total de Ventas:")
        st.subheader(f"S/. {total_sales_value: ,.0f}")
    with middle_column:
        st.subheader("Promedio Por Venta Ganada:")
        st.subheader(f"S/. {average_deal_size: ,.0f}")
    with right_column:
        st.subheader("Tasa de Conversión (%):")
        st.subheader(f"{conversion_rate:.2f}%")
    with right_column_2:
        st.subheader("Tasa de Cancelación (%):")
        st.subheader(f"{lost_rate:.2f}%")

    st.markdown("""---""")


def main():
    init_config_st_page("Dashboard de Ventas")
    file = "data/sales_data.xlsx"
    sales_df = get_excel_data(file)
    transform_clean_sales_data(sales_df)

    # ---- SIDEBAR FILTER ----
    filter_prob = st.sidebar.header("Filtros:")
    city = st.sidebar.multiselect(
        "Selecciona una Probabilidad:",
        options=sales_df["Probabilidad"].unique(),
        default=sales_df["Probabilidad"].unique()
    )

    print(filter_prob)

    set_general_dashboard_info(sales_df)

    df_sum_dist_prob = get_df_prob_distribution(sales_df)
    graph_dist_prob = create_graph_first_insight(df_sum_dist_prob)

    df_performance_owner = get_df_performance_owner(sales_df)
    graph_performance_owner = create_graph_second_insight(df_performance_owner)

    df_total_value_prob = get_df_prob_total_value(sales_df)
    graph_total_value_prob = create_graph_third_insight(df_total_value_prob)

    df_deals_month = get_df_deals_by_month(sales_df)
    graph_deals_month = create_graph_fourth_insight(df_deals_month)

    top_number = 10
    df_company_total_value = get_df_company_total_value(sales_df,top_number)

    left_column, mid_column, right_column = st.columns([2, 0.2, 2])
    left_column.plotly_chart(graph_dist_prob, use_container_width=True)
    mid_column.markdown("&nbsp;")
    right_column.plotly_chart(graph_performance_owner, use_container_width=True)

    st.markdown("""---""")
    left_column, mid_column, right_column = st.columns([2, 0.2, 2])
    left_column.plotly_chart(graph_total_value_prob, use_container_width=True)
    mid_column.markdown("&nbsp;")
    right_column.plotly_chart(graph_deals_month, use_container_width=True)

    st.markdown("""---""")

    st.write(f"Top {top_number} clientes con mayor valor generado:")
    st.write(df_company_total_value)


if __name__ == "__main__":
    main()
