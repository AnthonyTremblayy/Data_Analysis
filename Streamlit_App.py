import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import streamlit as st

st.set_page_config(layout="wide")

#Import file
xlsx_file = st.sidebar.file_uploader('Import .xlsx File', type = 'xlsx') 

st.title('Data Analysis - CDPQ')

if xlsx_file is not None:
    df = pd.read_excel(xlsx_file)

    #Select Variables of interest
    SelectVar = df.select_dtypes(exclude=['object', 'bool']) 
    Vec1Name = st.sidebar.selectbox("First Variable Name", SelectVar.columns, index=0)
    Vec2Name = st.sidebar.selectbox("Second Variable Name", SelectVar.columns,index=1)
    
    #Main Dataframe
    col1, col2 = st.columns((3,1))
    col1.write(''' #### Dataframe''')
    col1.write(df)
    
    #Display Variables of Interest and Visualization
    if st.sidebar.button('GO'):
        
        #Store Variables
        Vec1 = df[str(Vec1Name)]
        Vec2 = df[str(Vec2Name)]

        #Variables of Interest
        col2.write(''' #### Variables of Interest''')
        col2.write(df[[str(Vec1Name),str(Vec2Name)]])

        #Descriptive Statistics
        col3, col4 = st.columns((1,2))
        col3.write(''' #### Descriptive Statistics ''')
        Describe = pd.DataFrame({Vec1Name: Vec1, Vec2Name: Vec2, 'Absolute Difference': abs(Vec1-Vec2)})
        col3.write(Describe.describe())
        
        #Ridge Plot 
        col4.write(''' #### Ridgeline Plot ''')
        df_SNS1 = df[[str(Vec1Name)]]
        df_SNS1['Source'] = Vec1Name
        df_SNS2 = df[[str(Vec2Name)]]
        df_SNS2['Source'] = Vec2Name
        df_SNS2.rename(columns={Vec2Name: Vec1Name}, inplace=True)
        df_SNS = df_SNS1.append(df_SNS2)

        sns.set_theme(style="white", rc={"axes.facecolor": (0, 0, 0, 0), 'axes.linewidth':1.5}, font_scale = 1.2)

        g = sns.FacetGrid(df_SNS, row ='Source', hue = "Source", aspect=7, height=2.2, palette = ['#9AC9D3', '#046B67'])
        g.map_dataframe(sns.kdeplot, x = Vec1Name, fill = True, alpha = 1)
        g.map_dataframe(sns.kdeplot, x = Vec1Name, color = 'black')

        def label(x, color, label):
            ax = plt.gca()
            ax.text(0, .2, label, color='black', fontsize=13,
                    ha="left", va="center", transform=ax.transAxes)
            
        g.map(label, "Source")

        g.fig.subplots_adjust(hspace=-0.6)

        g.set_titles("")
        g.set(yticks=[], xlabel = "Value", ylabel = "")
        g.despine(left=True)

        col4.pyplot(g)
        sns.reset_defaults()

        #Quantile-quantile plot
        col5, col6 = st.columns((1,1))
        col5.write(''' #### Quantile-quantile Plot ''')
        fig, ax = plt.subplots(figsize=(12,6))
        ax.scatter(np.sort(Vec1), np.sort(Vec2), color = '#9AC9D3', alpha=0.5, edgecolor = 'k')
        ax.set_xlabel("{}'s quantiles".format(Vec1Name))
        ax.set_ylabel("{}'s quantiles".format(Vec2Name))
        ax.axline([0, 0], [1, 1], color = '#9AC9D3')
        col5.pyplot(fig)

        #Density Plot
        col6.write(''' #### Density Plot ''')
        fig2, ax2 = plt.subplots(figsize=(12,6))
        sns.distplot(Vec1, hist = False, kde = True, kde_kws = {'shade': True, 'linewidth': 1.5}, label = [Vec1Name], ax=ax2, color='#9AC9D3')
        sns.distplot(Vec2, hist = False, kde = True, kde_kws = {'shade': True, 'linewidth': 1.5},label = [Vec2Name], ax=ax2,color='#046B67')
        ax2.legend()
        ax2.set_ylabel('Density')
        ax2.set_xlabel('Value')
        col6.pyplot(fig2)

        #Differences
        col7, col8, col9 = st.columns((0.5,1,0.5))
        idx = list(range(df.shape[0]))
        col8.write(''' #### Differences ({} - {}) '''.format(Vec1Name,Vec2Name))
        fig3, ax3 = plt.subplots(figsize=(12,6))
        ax3.plot(idx, Vec1-Vec2, linewidth=0.5, color='#9AC9D3')
        ax3.plot(idx, np.repeat(Vec1.median(),len(idx)), '--', label = 'Median - Var1', color = '#16254B', linewidth=1)
        ax3.plot(idx, -np.repeat(Vec1.median(),len(idx)), '--', color = '#16254B', linewidth=1)
        ax3.plot(idx, np.repeat(Vec2.median(),len(idx)), '--', label = 'Median - Var2', color = '#046B67', linewidth=1)
        ax3.plot(idx, -np.repeat(Vec2.median(),len(idx)), '--', color = '#046B67', linewidth=1)
        ax3.set_xlabel('Instances')
        ax3.set_ylabel('Differences')
        ax3.legend()
        ax3.yaxis.grid()
        col8.pyplot(fig3)




        