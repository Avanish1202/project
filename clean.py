import streamlit as st
import pandas as pd
import base64

# Function to perform data cleaning
def clean_data(data, drop_columns, remove_null, fill_null, fill_value, data_types):
    if drop_columns:
        data = data.drop(columns=drop_columns)

    if remove_null:
        data = data.dropna()

    if fill_null:
        data = data.fillna(fill_value)

    # Convert selected columns to specified data types
    for column, dtype in data_types.items():
        data[column] = data[column].astype(dtype)

    return data

# Function to create a download link for the cleaned data
def create_download_link(df, filename="cleaned_data.csv"):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download Cleaned Data</a>'
    return href

# Streamlit app
def main():
    st.title("Data Cleaning App")

    # File upload
    uploaded_file = st.file_uploader("Choose a file")

    if uploaded_file is not None:
        # Read data from the uploaded file with a different encoding
        data = pd.read_csv(uploaded_file, encoding='latin1')
        st.write("Data columns (total {} columns):".format(len(data.columns)))
        st.dataframe(data.dtypes.reset_index().rename(columns={0: 'Dtype', 'index': 'Column'}))

        # Display DataFrame summary
        st.write("DataFrame Summary:")
        st.dataframe(data.describe(include='all'))

        # Display the original data
        st.subheader("Original Data")
        st.write(data)

        # User input for column removal
        drop_columns = st.multiselect("Select columns to remove", data.columns)

        # User input for removing null values
        remove_null = st.checkbox("Remove rows with null values")

        # User input for filling null values
        fill_null = st.checkbox("Fill null values")

        # User input for changing column data types
        st.subheader("Change Column Data Types")

        # Create a dictionary to store selected column and data type
        data_types = {}
        for column in data.columns:
            # Use checkboxes to select multiple columns
            if st.checkbox(column):
                selected_dtype = st.selectbox(f"Select data type for {column}", ["", "int", "float", "str"])
                if selected_dtype:
                    data_types[column] = selected_dtype

        # Button to trigger data cleaning and find null values
        if st.button("Clean Data and Find Null Values"):
            # Perform data cleaning
            data = clean_data(data, drop_columns, remove_null, fill_null, None, data_types)

            # Display the cleaned data
            st.subheader("Cleaned Data")
            st.write(data)

            # Display null values in the cleaned data
            st.subheader("Null Values in Cleaned Data")
            st.write(data.isnull().sum())

            # Create a download link for the cleaned data
            st.markdown(create_download_link(data), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
