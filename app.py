import streamlit as st

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pandas as pd
from database import Report
from visualization import *
from AnalyseData import Analyse

engine = create_engine('sqlite:///db.sqlite3')
Session = sessionmaker(bind=engine)
sess = Session()

analysis = Analyse()

st.title('Video Games Sales Analysis')
sidebar = st.sidebar

def viewForm():

    st.plotly_chart(plot())

    title = st.text_input("Report Title")
    desc = st.text_area('Report Description')
    btn = st.button("Submit")

    if btn:
        report1 = Report(title = title, desc = desc, data = "")
        sess.add(report1)
        sess.commit()
        st.success('Report Saved')

def analyse():
    data = analysis.getCategories()
    st.plotly_chart(plotBar(data.index, data.values))

def analysePlatform():
    data = analysis.getPlatform()
    st.plotly_chart(plotBar(analysis.getPlatform(), 'title', 'xlabel', 'ylabel'))

def analysePublisher():

    num = st.select_slider(options=[5, 10, 15, 20, 25, 30], label="Select the number of Publishers to show")
    st.header('Top Publishers By Release Count')
    st.plotly_chart(plotBar(analysis.getTopPublishersByCount(num), 'title', 'xlabel', 'ylabel'))

    st.header('Top Publishers By Total Sales')
    st.plotly_chart(plotBar(analysis.getTopPublishersBySum(num), 'title', 'xlabel', 'ylabel'))

    st.header('Top Publishers By Total Sales in Region')
    for region, name in analysis.getRegion():
        st.plotly_chart(plotBar(analysis.getTopPublishersBySumInRegion(num, region), 'Total Sales in '+name, 'xlabel', 'ylabel'))

def analyseGenre():

    st.header('Top Genres By Release Count')
    st.plotly_chart(plotBar(analysis.getTopGenresByCount(), 'title', 'xlabel', 'ylabel'))

    st.header('Top Genres By Total Sales')
    st.plotly_chart(plotBar(analysis.getTopGenresBySum(), 'title', 'xlabel', 'ylabel'))

    st.header('Top Genres By Total Sales in Region')
    for region, name in analysis.getRegion():
        st.plotly_chart(plotBar(analysis.getTopGenresBySumInRegion(region), 'Total Sales in '+name, 'xlabel', 'ylabel'))

    st.header('Top Genres By Total Sales in Region')
    for region, name in analysis.getRegion():
        st.plotly_chart(plotBar(analysis.getTopGenresByCountInRegion(region), 'Total Release Count in '+name, 'xlabel', 'ylabel'))

def viewDataset():
    st.header('Dataset Used for Video Game Sales Analysis')
    st.dataframe(analysis.getDataframe())

def analyseGameRelease():
    st.header("Year wise release")
    st.plotly_chart(plotLine(analysis.getYearWiseRelease(), 'title', 'xlabel', 'ylabel'))

# def 

def viewReport():
    reports = sess.query(Report).all()
    titlesList = [ report.title for report in reports ]
    selReport = st.selectbox(options = titlesList, label="Select Report")
    
    reportToView = sess.query(Report).filter_by(title = selReport).first()

    markdown = f"""
        ## {reportToView.title}
        ### {reportToView.desc}
        
    """

    st.markdown(markdown)

sidebar.header('Choose Your Option')
options = [ 'View Database', 'Timeline Analysis', 'Analyse Platform', 'Analyse Publisher', 'Analyse Genre' ]
choice = sidebar.selectbox( options = options, label="Choose Action" )

if choice == options[0]:
    viewDataset()
elif choice == options[1]:
    analyseGameRelease()
elif choice == options[2]:
    analysePlatform()
elif choice == options[3]:
    analysePublisher()
elif choice == options[4]:
    analyseGenre()