import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(layout='wide',page_title='Startup Funding Analysis')

df = pd.read_csv('cleaned_startup_funding.csv')


def load_overview():
    st.title("Startup Funding Analysis - Overview")

    st.image("Startup_image1.png")  #width=150

    st.header("Project Introduction & Motivation")
    st.write("""
    This project aims to provide an interactive analysis of startup funding trends in India, useful for investors, entrepreneurs, and analysts.
    The app allows users to explore funding dynamics, discover which startups and sectors are attracting investments, and understand investor activity.
    """)

    st.header("Dataset Details")
    st.markdown("""
    - **Source:** Startup Funding data is picked from Kaggle.
    - **Timeframe:** [January 2015 - December 2022]
    - **Rows:** {rows}  
    - **Columns:** {cols}
    """.format(rows=len(df), cols=len(df.columns)))

    st.header("Dataset Descriptions")
    st.markdown("""
    - **date**: Date when the funding was announced.
    - **startup**: Name of the funded startup.
    - **vertical**: Sector or industry vertical of the startup.
    - **subvertical**: Sub-sector or industry sub-vertical of the startup.
    - **city**: City where the startup is based.
    - **round**: Funding round.
    - **amount**: Funding amount.
    - **investors_clean**: Name(s) of the investors involved.
    - **year**: Year of funding.
    - **month**: Month of funding.
    """)

    st.header("Note on Data Quality")

    st.markdown("""
    - Many columns such as Vertical, Subvertical, and City contain entries labeled as **"Unknown"**, indicating missing or unavailable data in the original sources.
    - The **"Unknown"** values are retained to maintain transparency and completeness of the dataset.
    - Some records have funding amounts set to **0**, which were assigned during data cleaning to represent Undisclosed funding information.
    - These **0** values do not imply no funding but stand for Unknown or Unreported amounts.
    - Displaying **"Unknown"** and zero values helps users understand real-world data limitations without hiding incomplete data.
    """)

    st.header("How to use the App")
    st.markdown("""
    - Use the sidebar to navigate between Overall Analysis, StartUp, or Investor-centric views.
    - Don't Forget to Click the button Analyze
    - On each page, interactive charts and summaries will help you dig deeper into the funding landscape.
    - 
    """)


def load_overall_analysis():
    st.title('Overall Analysis')

    # total invested amount
    total = round(df['amount']).sum()
    # average funding
    avg_funding=df.groupby('startup')['amount'].sum().mean()
    # number of startups funded
    num_funded= df['startup'].nunique()
    # number of unique investors
    unique_investors = df['investors_clean'].str.split(', ').explode().nunique()

    col1 , col2 = st.columns(2)
    with col1:
        st.metric('Startups Funded', str(num_funded))

    with col2:
        st.metric('Unique Investors', str(unique_investors))

    col3 , col4 = st.columns(2)
    with col3:
        st.metric('Total Investment', str(total) + " Crore")
    with col4:
        st.metric('Average Investment', str(round(avg_funding)) + " Crore")

# Plot 1
    st.header('Deals Over the Years')
    temp_df1 = df.groupby(['year'])['startup'].count().reset_index()
    temp_df1['x_axis'] = temp_df1['year']

    fig1 = px.line(
        temp_df1,
        x='x_axis',
        y='startup',
        title='Count of Deals',
        labels={'x_axis': 'Year', 'startup': 'Count'},
        markers=True
    )
    # Rotate x-axis ticks for better readability
    fig1.update_xaxes(tickangle=0)
    st.plotly_chart(fig1)

# Plot 2
    st.header('Deals Over the Months')
    temp_df2 = df.groupby(['year', 'month'])['startup'].count().reset_index()
    temp_df2['x_axis'] = temp_df2['month'].astype('str') + '-' + temp_df2['year'].astype('str')

    fig2 = px.line(
        temp_df2,
        x='x_axis',
        y='startup',
        title='Count of Deals',
        labels={'x_axis': 'Month-Year', 'startup': 'Count'},
        markers=True
    )
    # Rotate x-axis ticks for better readability
    fig2.update_xaxes(tickangle=45)
    st.plotly_chart(fig2)

# Plot 3
    st.header('Funding Amount')
    temp_df3 = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    temp_df3['x_axis'] = temp_df2['month'].astype('str') + '-' + temp_df3['year'].astype('str')

    fig3 = px.line(
        temp_df3,
        x='x_axis',
        y='amount',
        title='Invested Amount Over The Months',
        labels={'x_axis': 'Month-Year', 'amount': 'Total Amount'},
        markers=True
    )
    # Rotate x-axis ticks for better readability
    fig3.update_xaxes(tickangle=45)
    st.plotly_chart(fig3)

# Plot 4
    st.header('Maximum Funding Raised By')
    temp_df4 = df.groupby('startup')['amount'].sum().sort_values(ascending=False).reset_index().head(5)
    fig4 = px.bar(temp_df4, x='startup', y='amount', labels={'x': 'Startup','y': 'Amount'},text_auto=True)
    fig4.update_traces(textposition='outside')
    st.plotly_chart(fig4)

    col1,col2 = st.columns(2)
    with col1:
# Plot 5
        st.header('Top 5 Categories By Funding')
        temp_df5 = df.groupby('vertical')['amount'].sum().sort_values(ascending=False).reset_index().head(5)
        fig5 = px.pie(temp_df5, names= 'vertical' , values = 'amount')
        fig5.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig5)

    with col2:
        # Plot 6
        st.header('Top 5 Rounds By Funding')
        temp_df5 = df.groupby('round')['amount'].sum().sort_values(ascending=False).reset_index().head(5)
        fig5 = px.bar(
            temp_df5,
            x='amount',
            y='round',
            orientation='h',
            text='amount',
            labels={'amount': 'Amount', 'round': 'Round'}
        )
        fig5.update_traces(textposition='outside')
        fig5.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig5)

    col3,col4 = st.columns(2)
    with col3:
# Plot 7
        st.header('Deals Location Wise')
        temp_df4 = df.groupby('city')['startup'].count().sort_values(ascending=False).reset_index().head(5)
        fig4 = px.pie(temp_df4, names='city', values= 'startup')
        fig4.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig4)

    with col4:
       # Plot 8
       st.header('Amount Invested By Location')
       temp_df4 = df.groupby('city')['amount'].sum().sort_values(ascending=False).reset_index().head(5)
       fig4 = px.bar(
           temp_df4,
           x='amount',
           y='city',
           orientation='h',
           text='amount',
           labels={'amount': 'Amount', 'city': 'City'}
       )
       fig4.update_traces(textposition='outside')
       fig4.update_layout(yaxis={'categoryorder': 'total ascending'})
       st.plotly_chart(fig4)


def load_startup_details(startup):
    st.title(startup)

    # Filter data for the selected startup
    startup_df = df[df['startup'] == startup]

    # Total Funding Raised
    total_funding = startup_df['amount'].sum()
    st.metric('Total Funding Raised', f"{total_funding:.2f} Crore")


    # Top Investors
    st.subheader('Top Investors')
    # Explode the investors_clean column for the selected startup
    inv_series = startup_df['investors_clean'].str.split(', ').explode()
    # Get the top 5 investors by appearance count
    top_investor_names = inv_series.value_counts().head(5).index.tolist()
    # Display the top investors as a list
    for i, name in enumerate(top_investor_names, start=1):
        st.write(f"{i}. {name}")

    # Sector & Subvertical Profile
    st.subheader('Sector & Subvertical Profile')

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Verticals**")
        vertical_counts = startup_df['vertical'].value_counts().head(5)
        st.table(vertical_counts)

    with col2:
        st.write("**Subverticals**")
        subvertical_counts = startup_df['subvertical'].value_counts().head(5)
        st.table(subvertical_counts)

    # Funding by Round Type
    st.subheader('Funding by Round Type')
    # Group by round type and sum the funding amount
    round_funding = startup_df.groupby('round')['amount'].sum().sort_values(ascending=False).reset_index()

    # Bar chart using plotly express
    fig = px.bar(
        round_funding,
        x='amount',
        y='round',
        orientation='h',
        text='amount',
        labels={'amount': 'Funding Amount', 'round': 'Round Type'}
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(yaxis={'categoryorder':'total ascending'})

    st.plotly_chart(fig)

    # Geographic Funding Focus
    st.subheader('Geographic Funding Focus')
    # Group by city and sum funding amount
    city_funding = startup_df.groupby('city')['amount'].sum().sort_values(ascending=False).reset_index()

    # Pie chart using plotly express
    fig = px.pie(
        city_funding,
        values='amount',
        names='city',
        title='Funding Amount by City'
    )
    fig.update_traces(textinfo='percent+label', textposition='inside')
    st.plotly_chart(fig)




def load_investor_details(investor):

    st.title(investor)

    # load the recent 5 investments of the investor
    last5_df = df[df['investors_clean'].str.contains(investor)].head(5)[
        ['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)


    # biggest investments
    big_series = df[df['investors_clean'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
    st.subheader('Biggest Investments')

    fig11 = px.bar(
        x=big_series.index,
        y=big_series.values,
        labels={'x': 'Startup', 'y': 'Total Amount'}
    )
    st.plotly_chart(fig11)


    col1, col2 = st.columns(2)
    with col1:
        vertical_series = df[df['investors_clean'].str.contains(investor)].groupby('vertical')['amount'].sum().head(10)
        st.subheader('Sectors Invested In')

        fig12 = px.pie(vertical_series, values=vertical_series.values, names=vertical_series.index)
        st.plotly_chart(fig12)
    with col2:
        round_series = df[df['investors_clean'].str.contains(investor)].groupby('round')['amount'].sum().reset_index().head(10)
        st.subheader('Rounds Invested In')

        fig13 = px.bar(
            round_series,
            x='amount',
            y='round',
            orientation='h',
            text='amount',
            labels={'round': 'Round','amount': 'Amount'}
        )
        fig13.update_traces(textposition='outside')
        fig13.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig13)


    col3, col4 = st.columns(2)
    with col3:
        # city invested in
        city_series = df[df['investors_clean'].str.contains(investor)].groupby('city')['amount'].sum().head(10)
        st.subheader('City Invested In')

        fig14 = px.pie(city_series, values=city_series.values, names=city_series.index)
        st.plotly_chart(fig14)

    with col4:
        year_series = df[df['investors_clean'].str.contains(investor)].groupby('year')['amount'].sum()
        st.subheader('YoY Investment')

        fig15 = px.line(
            x=year_series.index,
            y=year_series.values,
            labels={'x': 'Year','y': 'Amount'}
        )
        st.plotly_chart(fig15)




st.sidebar.title('What to Analyze ?')

option = st.sidebar.selectbox('Select one',['Overview','Overall Analysis','StartUp','Investor'])

if option == 'Overview':
    load_overview()

elif option == 'Overall Analysis':
    load_overall_analysis()

elif option == "StartUp":
    selected_startup = st.sidebar.selectbox('Select Startup', sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button("Analyze Startup")
    if btn1:
        load_startup_details(selected_startup)

else:
    selected_investor = st.sidebar.selectbox('Select Investor',sorted(set(df['investors_clean'].str.split(',').sum())))
    btn2 = st.sidebar.button("Analyze")
    if btn2:
        load_investor_details(selected_investor)
