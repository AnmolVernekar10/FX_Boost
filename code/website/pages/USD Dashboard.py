import streamlit as st
import pandas as pd
import base64
from PIL import Image
import plotly.graph_objects as go

# # *******************************************************************************************************************
# Here we are setting the page configuration: page icon, page title, layout type
st.set_page_config(page_title="FX_Exchange", page_icon="🪙" , layout="centered")
# # *******************************************************************************************************************


# # *******************************************************************************************************************
# Function for Header
def header(url):
    st.markdown(f'<p style="background-color:transparent;color:white;font-size:50px;font-weight:bolder;border-radius:2%;">{url}</p>', unsafe_allow_html=True)

header("<u>USD Analysis</u>")
# # *******************************************************************************************************************

# # *******************************************************************************************************************
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
# # *******************************************************************************************************************

# # *******************************************************************************************************************
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

set_background('E:/Anmol_Projects/FX_Project_(CurrencyAnalysis)/code/bg1.png')
# # *******************************************************************************************************************


# Used for importing the Css file ( style.css)
def local_css():
    with open("E:/Anmol_Projects/FX_Project_(CurrencyAnalysis)/code/website/style/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Read the CSV file into a DataFrame
df = pd.read_csv('E:/Anmol_Projects/FX_Project_(CurrencyAnalysis)/data/NTData3.csv')

# Convert the 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Define date range limits
min_date = df['Date'].min().date()  # Convert to date type
max_date = df['Date'].max().date()  # Convert to date type

# Set default values within the allowed date range
default_start_date = min_date
default_end_date = max_date

# # *******************************************************************************************************************
# Code for Bigger font
st.markdown("""
<style>
.big-font {
    font-size:28px !important;
    color: white;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)
# # *******************************************************************************************************************


# # *******************************************************************************************************************
# Date range input from the user
st.markdown("<div style='font-size: 20px; color: white;'>Start Date</div>", unsafe_allow_html=True)
start_date = st.date_input('', min_value=min_date, max_value=max_date, value=default_start_date)
st.markdown("<div style='font-size: 20px; color: white;'>End Date</div>", unsafe_allow_html=True)
end_date = st.date_input('', min_value=min_date, max_value=max_date, value=default_end_date)
# # *******************************************************************************************************************


# # *******************************************************************************************************************
# For dropdown in currency field
currency_columns = [col for col in df.columns if col not in ['Date']]
if currency_columns:  # Check if currency_columns is not empty
    default_currency= currency_columns[0]  # Set the default currency1 to the first one in the list

    st.markdown("<div style='font-size: 20px; color: white;'>Select the Currency</div>", unsafe_allow_html=True)
    curr= st.selectbox('Select Currency 1', currency_columns, index=currency_columns.index(default_currency))
else:
    st.warning("No currency columns found in the DataFrame.")
    selected_curr= None
# # *******************************************************************************************************************

st.markdown('')

# # *******************************************************************************************************************
# Time interval selectbox
st.markdown("<div style='font-size: 20px; color: white;'>Duration</div>", unsafe_allow_html=True)
time_interval = st.selectbox("", ["Weekly", "Monthly","Quarterly","Yearly"])
# # *******************************************************************************************************************

# # *******************************************************************************************************************
# Button
st.markdown("")
update_button = st.button("Update Chart")
# # *******************************************************************************************************************

# Convert start_date and end_date to datetime objects
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter DataFrame based on user input
filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
filtered_df.set_index('Date', inplace=True)

# Resample the data based on the selected time interval
if time_interval == "Weekly":
    resampled_df = filtered_df.resample('W-Mon', label='right', closed='right').mean()
    x_label = 'Week'
elif time_interval == "Monthly":
    resampled_df = filtered_df.resample('M').mean()
    x_label = 'Monthly'
elif time_interval == "Yearly":
    resampled_df = filtered_df.resample('Y').mean()
    x_label = 'Monthly'
elif time_interval == "Quarterly":
    resampled_df = filtered_df.resample('Q').mean()
    x_label = 'Quarterly'

# Reset the index to make 'Date' a column again
resampled_df = resampled_df.reset_index()
# Create Plotly figure


if update_button and curr!="":
    import json
    from python.NT import get_json
    json_data=get_json(curr,start_date,end_date)
    json_data = json.loads(json_data)
    df = pd.DataFrame(list(json_data.items()), columns=['Date', 'Values'])
    fig = go.Figure([go.Scatter(x=resampled_df['Date'], y=resampled_df[curr])])
    fig.update_layout(
        title=f'Currency Values Over Time ({time_interval} intervals)',
        xaxis_title=f'{x_label}',
        yaxis_title='Values'
    )

    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown('<p class="big-font">Chart</p>', unsafe_allow_html=True)
    st.plotly_chart(fig)#Plot Chart

    max_value = resampled_df[curr].max() #Max value
    st.markdown(f'<p class="big-font"><b><u>Maximum {curr} Value</u></b>: {max_value}</p>', unsafe_allow_html=True)
    max_value = resampled_df[curr].min() #Min value
    st.markdown(f'<p class="big-font"><u><b>Minimum {curr} Value</u></b>: {max_value}</p>', unsafe_allow_html=True)

