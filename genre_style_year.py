import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import nltk
from nltk.corpus import stopwords

df = pd.read_csv('data/df.csv')
df = df.drop(df[df.Year>2022].index)

def genre_year():
  df = pd.read_csv('data/df.csv')
  df = df.drop(df[df.Year>2022].index)
  plt.figure(figsize=(10,8))
  plt.scatter(df['Year'], df['Genre'])

def genre_style():
  df = pd.read_csv('data/df.csv')
  df = df.drop(df[df.Year>2022].index)
  plt.figure(figsize=(10,8))
  plt.scatter(df['Style'], df['Genre'])

def top_themes():
    dfnew = pd.read_csv('data/df_reduced.csv')
    dfnew=dfnew.drop(dfnew[dfnew.Year>2022].index)
    nltk.download('stopwords')
    swords = stopwords.words('english')
    name_map = {}
    for name in dfnew['Name']:
        for s in name.split(' '):
            s = s.lower()
            s = s.strip(',')
            if s in name_map and s not in swords:
                name_map[s] = name_map[s] + 1
            elif s not in name_map and s not in swords:
                name_map[s] = 1
    name_sorted_list = (sorted(name_map.items(), key = lambda kv:(kv[1], kv[0]),reverse=True))
    plt.figure(figsize=(20,8))
    x1 = list(x[0] for x in name_sorted_list)[:20]
    y1 = list(x[1] for x in name_sorted_list)[:20]
    plt.bar(x1,y1)
    plt.show()

genre_year()
genre_style()
top_themes()