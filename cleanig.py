import streamlit as st
import pandas as pd
import base64
from sklearn.preprocessing import StandardScaler
from scipy.stats import zscore


def clean_data(data, drop_columns, remove_null, fill_null, fill_value, data_types, column_filters,
               remove_duplicates, selected_columns_for_duplicates,
               remove_outliers, selected_columns_for_outliers, outlier_threshold,
               time_series_handling, timestamp_column, replace_categorical_column, replacement_mapping,
               modify_column):
    if drop_columns:
        data = data.drop(columns=drop_columns)

    if remove_null:
        data = data.dropna()

    if fill_null and fill_value is not None:
        data = data.fillna(fill_value)

    for column, dtype in data_types.items():
        try:
            data[column] = data[column].astype(dtype)
        except KeyError as e:
            st.error(f"KeyError: {e}. Please check if '{column}' exists in the DataFrame.")

    for column, values in column_filters.items():
        if values:
            data = data[data[column].astype(str).isin(values)]

    if remove_duplicates:
        data = data.drop_duplicates(subset=selected_columns_for_duplicates)

    # Remove outliers using z-scores
    if remove_outliers and selected_columns_for_outliers:
        z_scores = zscore(data[selected_columns_for_outliers])
        data = data[(z_scores < outlier_threshold).all(axis=1)]

    if time_series_handling:
        if timestamp_column in data.columns:
            data[timestamp_column] = pd.to_datetime(data[timestamp_column])
            data.sort_values(by=timestamp_column, inplace=True)
            for lag in range(1, 4):
                data[f'value_lag_{lag}'] = data['value'].shift(lag)

            st.success("Time series handling logic applied successfully.")

    # Replace categorical values in a specific column
    if replace_categorical_column and replacement_mapping:
        if replace_categorical_column in data.columns:
            data[replace_categorical_column] = data[replace_categorical_column].map(replacement_mapping)

    # Modify column values
    if modify_column:
        if modify_column['column'] in data.columns:
            start_index = modify_column['start_index']
            end_index = modify_column['end_index']

            # Remove specified range of characters
            data[modify_column['new_column']] = data[modify_column['column']].apply(
                lambda x: x[:start_index] + x[end_index + 1:])

            # Remove the original column if needed
            if modify_column['remove_original']:
                data = data.drop(columns=[modify_column['column']])

    return data


def create_download_link(df, filename="cleaned_data.csv"):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download Cleaned Data</a>'
    return href


def main():
    st.set_option('deprecation.showPyplotGlobalUse', False)

    st.title("Data Cleaning App")

    uploaded_file = st.file_uploader("Choose a file")

    replace_categorical_column = None  # Initialize the variable outside the if condition
    replacement_mapping = {}  # Initialize the mapping dictionary

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file, encoding='latin1')
        st.write("Data columns (total {} columns):".format(len(data.columns)))
        st.dataframe(data.dtypes.reset_index().rename(columns={0: 'Dtype', 'index': 'Column'}))

        st.write("DataFrame Summary:")
        st.dataframe(data.describe(include='all'))

        st.subheader("Original Data")
        st.dataframe(data)

        selected_columns_to_remove = st.multiselect("Select columns to remove", data.columns)

        remove_null = st.checkbox("Remove rows with null values")

        fill_null = st.checkbox("Fill null values")
        fill_value = None
        if fill_null:
            fill_value = st.text_input("Enter the value to fill null values", "")

        st.subheader("Change Column Data Types")
        data_types = {}
        for column in data.columns:
            if st.checkbox(column):
                selected_dtype = st.selectbox(f"Select data type for {column}", ["", "int", "float", "str"])
                if selected_dtype:
                    data_types[column] = selected_dtype

        st.subheader("Column Filters")
        selected_columns = st.multiselect("Select columns for filtering", data.columns)
        column_filters = {}
        for column in selected_columns:
            filter_values = st.text_input(f"Filter values for {column} (comma-separated)", "")
            if filter_values:
                column_filters[column] = [value.strip() for value in filter_values.split(',')]

        remove_duplicates = st.checkbox("Remove duplicate rows")
        selected_columns_for_duplicates = st.multiselect("Select columns for duplicate removal", data.columns)

        remove_outliers = st.checkbox("Remove outliers")
        selected_columns_for_outliers = st.multiselect("Select numeric columns for outlier removal",
                                                       data.select_dtypes('number').columns)

        outlier_threshold = st.number_input("Outlier threshold", value=3.0)

        # Show checkbox for replacing categorical values
        replace_categorical_checkbox = st.checkbox("Replace Categorical Values with Numeric")

        # Show additional options only if checkbox is selected
        if replace_categorical_checkbox:
            st.subheader("Replace Categorical Values with Numeric")
            replace_categorical_column = st.selectbox("Select column to replace categorical values", data.columns)

            # Create a dictionary to store selected column and mapping for string to int conversion
            if replace_categorical_column:
                unique_values = data[replace_categorical_column].unique()
                for value in unique_values:
                    replacement_mapping[value] = st.number_input(f"Replace '{value}' with (numeric value)", value=0)

        # Modify column values
        st.subheader("Modify Column Values")
        modify_column_checkbox = st.checkbox("Modify column values")
        modify_column = {}
        if modify_column_checkbox:
            modify_column['column'] = st.selectbox("Select column to modify", data.columns)
            modify_column['start_index'] = st.number_input("Specify start index to remove from", value=0)
            modify_column['end_index'] = st.number_input("Specify end index to remove to", value=0)
            modify_column['new_column'] = st.text_input("Enter new column name", "")
            modify_column['remove_original'] = st.checkbox("Remove original column after modification")

        if st.button("Clean Data and Find Null Values"):
            data = clean_data(data, selected_columns_to_remove, remove_null, fill_null, fill_value, data_types,
                              column_filters, remove_duplicates, selected_columns_for_duplicates,
                              remove_outliers, selected_columns_for_outliers, outlier_threshold,
                              time_series_handling=True, timestamp_column='timestamp',
                              replace_categorical_column=replace_categorical_column,
                              replacement_mapping=replacement_mapping,
                              modify_column=modify_column)

            st.subheader("Cleaned Data")
            st.dataframe(data)

            st.subheader("Null Values in Cleaned Data")
            st.write(data.isnull().sum())

            st.markdown(create_download_link(data), unsafe_allow_html=True)


if __name__ == "__main__":
    main()