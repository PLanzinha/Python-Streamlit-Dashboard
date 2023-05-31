import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    layout="wide",
    initial_sidebar_state="auto",
)
st.title("Streamlit Visualization Dashboard")
st.markdown("*Pedro Lanzinha*")

with st.sidebar:
    with st.expander("Project Objectives:"):
        st.write("""
        The purpose behind this project is to enable users to combine, visualize, and download data easily. 
        Users can select and combine various columns and visualize them with ease.
        The following points will be addressed in this project:

        - **Table Selection**: Create a dropdown or checkbox widget listing available tables that users can select and combine.
        - **Visualization Window Selection**: Allow the user to select the number of windows (up to 3), each with a dropdown to select tables.
        - **Data Combination For Each Window**: Merge or combine the selected columns based on user choices.
        - **Visualization Generation**: Display visualizations based on user-selected combinations.
        - **Data Export and Download**: Enable the user to export and download combined columns as well as the visualized data.
        """)


    @st.cache(allow_output_mutation=True)
    def load_file(upload):
        if upload is None:
            return None
        elif upload.name.endswith('.csv'):
            data = pd.read_csv(upload)
        elif upload.name.endswith(('.xls', '.xlsx')):
            data = pd.read_excel(upload)
        elif upload.name.endswith('.json'):
            data = pd.read_json(upload)
        else:
            return "Selected file type is invalid!"
        return data


    upload = st.file_uploader("Select a '.csv', '.json', '.xls'/'.xlsx' type of file.")

    if upload is not None:
        df = load_file(upload)
    else:
        st.info("Please upload a file.")
        st.stop()

    selected_columns = st.multiselect("Select Columns to Visualize.", df.columns)
    checkbox_preview = st.checkbox("Enable Data Preview")

    graph_num = st.select_slider("Select the number of Graphs (1-4)", options=[1, 2, 3, 4])
    graph = []

    for i in range(graph_num):
        st.subheader(f"Graph {i + 1}")
        graph_type = st.selectbox(f"Select which graph for Graph {i + 1}:",
                                  ["--", "Bar Chart", "Line Chart", "Scatter Plot"])
        x_column = st.selectbox(f"Select the X-Axis Column {i + 1}:", selected_columns)
        y_columns = st.selectbox(f"Select the Y-Axis Column {i + 1}:", selected_columns)

        if graph_type != "--" and x_column and y_columns:
            chart_title = f'{graph_type}'
            plot = None

            if graph_type == "Bar Chart":
                plot = px.bar(df, x=x_column, y=y_columns, title=chart_title)
            elif graph_type == "Line Chart":
                plot = px.line(df, x=x_column, y=y_columns, title=chart_title)
            elif graph_type == "Scatter Plot":
                plot = px.scatter(df, x=x_column, y=y_columns, color=x_column, title=chart_title)

            if plot is not None:
                graph.append(plot)

    checkbox_viz = st.checkbox("Enable Graphic Visualization")

    def download_df(df):
        return df.to_csv(index=False).encode('utf-8')

    def download_graph(plot):
        img = plot.to_image(format="png")
        return img


    csv = download_df(df)

    if checkbox_preview is True:
        st.download_button(
            "Download Csv",
            csv,
            "file.csv",
            "text/csv",
            key='download-csv'
        )
    if checkbox_viz is True:
        for i, plot in enumerate(graph):
            img = download_graph(plot)
            st.download_button(
                f"Download Graph {i + 1}",
                img,
                f"image_{i}.png",
                "image/png",
                key=f"download-image-{i}"
            )

if selected_columns:
    if checkbox_preview is True:
        with st.expander("Columns Data Preview:"):
            st.dataframe(df[selected_columns])

    if checkbox_viz is True:
        num_columns = len(graph)
        num_columns = max(num_columns, 1)  # Ensure at least one column
        columns = st.columns(num_columns)
        for i, plot in enumerate(graph):
            with columns[i]:
                st.plotly_chart(plot)
