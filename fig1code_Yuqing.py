import pandas as pd
import seaborn as sns
from matplotlib import pyplot

def plotstyleyear():
    """
    Docstring
    This function plots the styles of Van Gogh against time
    """
    df = pd.read_csv('df.csv')
    df = df.drop(columns=['Name', 'Colors', 'Genre','Link'])
    df = df.groupby(["Year", "Style"]).size().reset_index(name="Frequency")
    df = df.sort_values(by=['Year'])
    df = df.iloc[:-1 , :]
    df = df.pivot('Style','Year','Frequency').fillna(0)
    pyplot.figure(figsize=(10, 2.5))
    ax = sns.heatmap(df,annot=True,cbar=False,fmt='g')
    return ax

