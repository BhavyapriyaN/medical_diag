import streamlit as st
st.title("EDA PAGE")
from home import data 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
st.set_option('deprecation.showPyplotGlobalUse', False)
plt.style.use("fivethirtyeight")

def main():
    # show data
    if st.sidebar.checkbox('Show data',False):
        st.write(data)

    st.sidebar.subheader("Choose the plot")

    #univariate histograms
    def histograms(data):
        st.write("Histograms")
        data.hist()
        plt.tight_layout()
        st.pyplot()

    def histplot_boxplot(data, feature, bins=None, figsize=(12,7)):
        fig, (ax_box, ax_hist)=plt.subplots(
        nrows=2,
        sharex=True,
        gridspec_kw={"height_ratios":(0.25, 0.75)},
        figsize=figsize)
        
        sns.boxplot(data=data, x=feature, showmeans=True, ax=ax_box, color="violet")
        sns.histplot(data=data, x=feature, bins=bins,ax=ax_hist, pallete="winter") if bins else sns.histplot(data=data,
                                                            x=feature, ax=ax_hist)
        ax_hist.axvline(data[feature].mean(), color='green', linestyle="--")
        ax_hist.axvline(data[feature].median(), color='black', linestyle="-")
        
        st.pyplot()
        
    def countplot(data, feature):
        plt.figure(figsize=(12,7))
        ax=sns.countplot(data=data, x=feature, color="green")
        for p in ax.patches:
            x=p.get_bbox().get_points()[:,0]
            y=p.get_bbox().get_points()[1,1]
            ax.annotate("{:.3g}%".format(100.*y/len(data)), (x.mean(), y), ha="center", va="bottom")
        st.pyplot()


    plot=st.sidebar.selectbox("Choose Univariate Plot", ('histograms', 'boxplot-histplot','countplot'))
    if plot=="histograms":
        if st.sidebar.button("PLOT"):
            histograms(data)

    if plot=="boxplot-histplot":
        if st.sidebar.button("PLOT"):
            for col in data.select_dtypes(exclude="O").columns:
                st.write(col)
                histplot_boxplot(data=data, feature=col)
    if plot=="countplot":
        if st.sidebar.button("PLOT"):
                countplot(data, feature="Outcome")

    Bivariate_plots = st.sidebar.selectbox('Choose Bivariate Plot', ('line and Scatterplot', 'heatmap','Bar Graph'))
    # Bivariate -categorical vs numerical
    def bivariate_barplot(data, feature1, feature2):
        data.groupby(feature1)[feature2].mean().plot(kind="bar", color="orange")
        plt.ylabel(feature2)
        st.pyplot()

    # numericall vs numerical
    def lineplot_scatterplot(data, feature1, feature2):
        plt.figure(figsize=(16,7))
        plt.subplot(1,2,1)
        sns.lineplot(data=data, x=feature1, y=feature2, color="green")
        plt.title("Lineplotbetween {0} and {1}".format(feature1, feature2))
        
        plt.subplot(1,2,2)
        sns.scatterplot(data=data, x=feature1, y=feature2, color="orange", hue="Outcome")
        plt.title("Scatter Plot Between {0} and {1}".format(feature1, feature2))
        st.pyplot()


    if Bivariate_plots == 'Bar Graph':
        if st.sidebar.button('PLOT', key = 'bivars'):
            for col in data.select_dtypes(exclude="O").columns:
                bivariate_barplot(data=data, feature1="Outcome",feature2=col)
    elif Bivariate_plots =='line and Scatterplot':
        if st.sidebar.button('PLOT', key = 'bivars'):
            for col in data.select_dtypes(exclude="O").columns:
                lineplot_scatterplot(data=data, feature1="Age", feature2=col)
    
    

    






if __name__=="__main__":
    main()

        