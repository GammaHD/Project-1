import pandas as pd
from pathlib import Path
import plotly.express as px
import streamlit as st
import folium
from streamlit_folium import st_folium

Stolen_Funds_df = pd.read_csv(Path('/Users/CHD/desktop/Project-1/Resources/Stolen_Funds.csv'))

Stolen_Funds_df.rename(columns={'Hacker ID': 'hackerid'},inplace=True)

Stolen_Funds_df['Lost Funds'] = Stolen_Funds_df['Lost Funds'].str.replace(',','').astype(float)

st.set_page_config(page_title = 'Financal Hacks',page_icon=':chart_with_downwards_trend:',layout='wide')








#----- SIDEBAR -----
st.sidebar.header('Fliter Here')
Type = st.sidebar.multiselect(
    'Select Type:',
    options=Stolen_Funds_df['Type'].unique(),
    default=Stolen_Funds_df['Type'].unique()
)

hackerid = st.sidebar.multiselect(
    'Select Hacker ID:',
    options=Stolen_Funds_df['hackerid'].unique(),
    default=Stolen_Funds_df['hackerid'].unique()
)



Method = st.sidebar.multiselect(
    'Select Method:',
    options=Stolen_Funds_df['Method'].unique(),
    default=Stolen_Funds_df['Method'].unique()
)

Location = st.sidebar.multiselect(
    'Select Location:',
    options=Stolen_Funds_df['Location'].unique(),
    default=Stolen_Funds_df['Location'].unique()
)


df_selection = Stolen_Funds_df.query(
    "Type == @Type & Location == @Location & Method == @Method & hackerid == @hackerid"
)




st.title(':chart_with_downwards_trend: Total Lost')
st.markdown('##')

total_lost = int(df_selection['Lost Funds'].sum())
average_lost_by_year = round(df_selection['Lost Funds'].mean(),2)


#Display metrics

left_column, right_column = st.columns(2)
with left_column:
    st.subheader('Total Lost:')
    st.subheader(f'US $ {total_lost:,}')
with right_column:
    st.subheader('Average lost Per Year')
    st.subheader(f'US $ {average_lost_by_year}')



st.markdown('---')

#Add Charts

Hacker_ID_amount = (df_selection.groupby(['hackerid']).sum()[['Lost Funds']].sort_values(by='Lost Funds'))

Hacker_ID_chart = px.bar(
    Hacker_ID_amount,
    x='Lost Funds',
    y= Hacker_ID_amount.index,
    orientation='h',
    title = '<b>Total Stolen by Group</b>'

)


Hacker_ID_chart.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=(dict(showgrid=False))
)




st.plotly_chart(Hacker_ID_chart)



Method_amount = df_selection.groupby(['Method']).sum()[['Lost Funds']].sort_values(by='Lost Funds')

Method_amount_pie = px.pie(
    Method_amount,
    values = 'Lost Funds',
    names = Method_amount.index
    

)
st.plotly_chart(Method_amount_pie)


location_df = pd.DataFrame({
    'Location' :['Pakistan', 'Rwanda', 'Kenya', 'Nepal', 'United Kingdom', 'Russia', 'Bangladesh', 'Uganda', 'South Africa',
    'Mauritius', 'Norway', 'Chile', 'Taiwan', 'India', 'Mexico', 'Singapore', 'United Arab Emirates', 'Kuwait', 'Slovenian',
    'United States', 'Italy', 'South Korea', 'Bahamas', 'Netherlands', 'Japan'],
    'lat' : [ 30.3753, 1.9403, 0.0236, 28.3949, 55.3781, 61.524, 23.685, 1.3733, 30.5595, 20.3484, 60.472,
    35.6751, 23.6978, 20.5937, 23.6345, 1.3521, 23.4241, 29.3117, 46.1512,37.0902, 41.8719, 35.9078, 25.0343,
    52.1326, 36.2048],
    'lon' : [69.3451, 29.8739, 37.9062, 84.124, -3.436, 105.3188, 90.3563, 32.2903, 22.9375, 57.5522, 8.4689, -71.543,
    120.9605, 78.9629, -102.5528, 103.8198, 53.8478, 47.4818, 14.9955,-95.7129, 12.5674, 127.7669,-77.3963,5.2913,138.2529],
    'LostFunds' : [19500.00, 21306.82, 237025.00, 300000.00, 718392.00, 1550000.00, 3000000.00, 3200000.00, 3200000.00, 4000000.00, 10000000.00, 10000000.00,
    14000000.00, 14500000.00, 15000000.00, 20700000.00, 35000000.00, 49000000.00, 70000000.00,78163500.00, 170000000.00, 235001200.00, 477000000.00, 526000000.00,
    755000000.00]

})



