import pandas as pd
import seaborn as sns
from matplotlib import pyplot
from ast import literal_eval

def women_color():
    """
    Docstring
    This method returns the ten most used colors when Van Gogh drew women
    """
    df = pd.read_csv('df.csv')
    df = df.drop(columns=['Year', 'Genre', 'Style','Link'])
    df = df[df['Name'].str.contains("Women | Girl | Woman | Girls | Mother | Daughter | women | woman | girl | girls | mother | daughter | lady | Lady")]
    df = df.drop(columns=['Name'])
    df = df.reset_index(drop=True)
    new_cols = ['c1', 'c2', 'c3', 'c4', 'c5']
    l = df['Colors'].tolist()
    h = []
    for i in l:
        h.append(literal_eval(i))
    df[new_cols] = pd.DataFrame(h, index=df.index)
    df = df.drop(columns=['Colors'])
    df = df.stack().reset_index().drop(columns=['level_0','level_1'])
    f = df.value_counts().head(10)
    l = f.index.tolist()
    h = []
    for i in l:
        h.append(i[0])
    sns.set()
    rgb_colors = list(map(hex_to_rgb, h))
    sns.palplot(rgb_colors)
    
def hex_to_rgb(hex_value):
  h = hex_value.lstrip('#')
  return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))

def men_color():
    """
    Docstring
    This method returns the ten most used colors when Van Gogh drew men
    """
    df = pd.read_csv('df.csv')
    df = df.drop(columns=['Year', 'Genre', 'Style','Link'])
    df = df[df['Name'].str.contains("Men | Boy | Man | Boys | Father | Son | men | man | boy | boys | father | son")]
    df = df.drop(columns=['Name'])
    df = df.reset_index(drop=True)
    new_cols = ['c1', 'c2', 'c3', 'c4', 'c5']
    l = df['Colors'].tolist()
    h = []
    for i in l:
        h.append(literal_eval(i))
    df[new_cols] = pd.DataFrame(h, index=df.index)
    df = df.drop(columns=['Colors'])
    df = df.stack().reset_index().drop(columns=['level_0','level_1'])
    f = df.value_counts().head(10)
    l = f.index.tolist()
    h = []
    for i in l:
        h.append(i[0])
    sns.set()
    rgb_colors = list(map(hex_to_rgb, h))
    sns.palplot(rgb_colors)