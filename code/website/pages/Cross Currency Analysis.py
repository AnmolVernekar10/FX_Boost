import streamlit as st
import pandas as pd
import requests
import pickle
import base64
from streamlit_lottie import st_lottie
import streamlit as st
from PIL import Image
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="FX_Exchange", page_icon="🫀" , layout="centered")

def header(url):
    st.markdown(f'<p style="background-color:transparent;color:white;font-size:50px;font-weight:bolder;border-radius:2%;">{url}</p>', unsafe_allow_html=True)

header("<u>Cross Currency Analysis</u>")

# Here we are Styling the sidebar of the website
st.markdown("""
<style>
    [data-testid="stSidebar"] .css-17lntkn  {
    color: white !important;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    display: table-cell;
}
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
    [data-testid="stSidebar"] .css-pkbazv  {
    color: white !important;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    display: table-cell;
}
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    [data-testid="stSidebar"]{
    background:black;
    color: white !important;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    display: table-cell;
}
}
</style>
""", unsafe_allow_html=True)


# We are using this section, to add background-image to the website
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header{visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: contain;
    backgr
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

# set_background('E:/Heart_Disease_Project/Code/Website/2923472.webp')
set_background('E:/Anmol_Projects/FX_Project/code/bg1.png')

# Used for importing the Css file ( style.css)
def local_css():
    with open("E:/Anmol_Projects/FX_Project/code/website/style/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Read the CSV file into a DataFrame
df = pd.read_csv('E:/Anmol_Projects/FX_Project/data/NTData3.csv')

# Convert the 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Define date range limits
min_date = df['Date'].min().date()  # Convert to date type
max_date = df['Date'].max().date()  # Convert to date type

# Set default values within the allowed date range
default_start_date = min_date
default_end_date = max_date


st.markdown("""
<style>
.big-font {
    font-size:20px !important;
    color: white;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# Streamlit app


# Date range input from the user
st.markdown("<div style='font-size: 20px; color: white;'>Start Date</div>", unsafe_allow_html=True)
start_date = st.date_input('', min_value=min_date, max_value=max_date, value=default_start_date)

st.markdown("<div style='font-size: 20px; color: white;'>End Date</div>", unsafe_allow_html=True)
end_date = st.date_input('', min_value=min_date, max_value=max_date, value=default_end_date)

currency_columns = [col for col in df.columns if col not in ['Date']]

if currency_columns:  # Check if currency_columns is not empty
    default_currency1 = currency_columns[0]  # Set the default currency1 to the first one in the list
    default_currency2 = currency_columns[1]  # Set the default currency2 to the second one in the list

    st.markdown("<div style='font-size: 20px; color: white;'>Select the Currency1</div>", unsafe_allow_html=True)
    curr1 = st.selectbox('Select Currency 1', currency_columns, index=currency_columns.index(default_currency1))
    st.markdown("<div style='font-size: 20px; color: white;'>Select the Currency2</div>", unsafe_allow_html=True)
    curr2= st.selectbox('Select Currency 2', currency_columns, index=currency_columns.index(default_currency2))
else:
    st.warning("No currency columns found in the DataFrame.")
    selected_currency1, selected_currency2 = None, None

st.markdown("")

st.markdown("<div style='font-size: 20px; color: white;'>Duration</div>", unsafe_allow_html=True)
time_interval = st.selectbox("", ["Weekly", "Monthly","Quarterly","Yearly"])

st.markdown("")
update_button = st.button("Update Chart")

# Convert start_date and end_date to datetime objects
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter DataFrame based on user input
filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
filtered_df.set_index('Date', inplace=True)

# if update_button and curr1!="" and curr2!="":
#     import json
#     from python.NT import diffcurr
#     json_data = diffcurr(curr1, curr2, start_date, end_date)
#     diff_df = pd.DataFrame(list(json_data.items()), columns=['Date', 'Values'])

#     # Convert 'Date' column to datetime and set it as the index
#     diff_df['Date'] = pd.to_datetime(diff_df['Date'])
#     diff_df.set_index('Date', inplace=True)

#     # Resample the data based on the selected time interval
#     if time_interval == "Weekly":
#         resampled_df = diff_df.resample('W-Mon', label='right', closed='right').mean()
#     elif time_interval == "Monthly":
#         resampled_df = diff_df.resample('M').mean()
#     elif time_interval == "Yearly":
#         resampled_df = diff_df.resample('Y').mean()
#     elif time_interval == "Quarterly":
#         resampled_df = diff_df.resample('Q').mean()

#     # Reset the index to make 'Date' a column again
#     resampled_df = resampled_df.reset_index()
#     st.markdown(diff_df)
#     fig = go.Figure([go.Scatter(x=resampled_df['Date'], y=resampled_df['Values'])])
#     fig.update_layout(
#         title=f'Currency Values Over Time ({time_interval} intervals)',
#         xaxis_title='Date',
#         yaxis_title='Values'
#     )
#     st.markdown("")
#     st.markdown("")
#     st.markdown("")
#     st.markdown('<p class="big-font">Chart</p>', unsafe_allow_html=True)
#     st.plotly_chart(fig)

#     max_value = resampled_df['Values'].max()
#     st.markdown(f'<p class="big-font">Maximum Value: {max_value}</p>', unsafe_allow_html=True)
#     min_value = resampled_df['Values'].min()
#     st.markdown(f'<p class="big-font">Minimum Value: {min_value}</p>', unsafe_allow_html=True)

if update_button and curr1!="" and curr2!="":
    import json
    from python.NT import diffcurr
    json_data = diffcurr(curr1, curr2, start_date, end_date)
    diff_df = pd.DataFrame(list(json_data.items()), columns=['Date', 'Values'])

    # Convert 'Date' column to datetime and set it as the index
    diff_df['Date'] = pd.to_datetime(diff_df['Date'])
    diff_df.set_index('Date', inplace=True)

    # Resample the data based on the selected time interval
    if time_interval == "Weekly":
        resampled_df = diff_df.resample('W-Mon', label='right', closed='right').mean()
        x_label = 'Week'
    elif time_interval == "Monthly":
        resampled_df = diff_df.resample('M').mean()
        x_label = 'Month'
    elif time_interval == "Yearly":
        resampled_df = diff_df.resample('Y').mean()
        x_label = 'Year'
    elif time_interval == "Quarterly":
        resampled_df = diff_df.resample('Q').mean()
        x_label = 'Quarter'

    # Reset the index to make 'Date' a column again
    resampled_df = resampled_df.reset_index()

    fig = go.Figure([go.Scatter(x=resampled_df['Date'], y=resampled_df['Values'])])
    fig.update_layout(
        title=f'Currency Values Over Time ({time_interval} intervals)',
        xaxis_title=f'{x_label}',
        yaxis_title='Values'
    )
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown('<p class="big-font">Chart</p>', unsafe_allow_html=True)
    st.plotly_chart(fig)

    max_value = resampled_df['Values'].max()
    st.markdown(f'<p class="big-font">Maximum Value: {max_value}</p>', unsafe_allow_html=True)
    min_value = resampled_df['Values'].min()
    st.markdown(f'<p class="big-font">Minimum Value: {min_value}</p>', unsafe_allow_html=True)