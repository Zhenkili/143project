import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


def hex2rgb(s):
    '''
    this function converts hex color to rgb color
    '''
    
    assert isinstance(s, str)
    assert len(s) == 7
    assert s[0] == '#'
    
    # 0-9 -> 0-9, A-F -> 10-16
    hex_map = {str(i): i for i in range(10)}
    hex_map.update({c: i+10 for i,c in enumerate('ABCDEF')})
    
    
    r = hex_map[s[1]] * 16 + hex_map[s[2]] * 1
    g = hex_map[s[3]] * 16 + hex_map[s[4]] * 1
    b = hex_map[s[5]] * 16 + hex_map[s[6]] * 1
    
    return (r, g, b)




def avg_color_by_year(df, year):
    '''
    return tuple of average rgb values of most popular colors during the year
    '''
    assert isinstance(year, int)
    assert year in set(df['Year'])
    
    colors = df[df["Year"] == year]['Colors']
    
    n = len(colors) * 5
    r,g,b = 0,0,0
    
    for row in colors:
        c_list = row[1:-1].split(', ')
        c_list = [c[1:-1] for c in c_list]
        
        rgb = [hex2rgb(c) for c in c_list]
        
        r += sum([t[0] for t in rgb])
        g += sum([t[1] for t in rgb])
        b += sum([t[2] for t in rgb])
        
    return r/n, g/n, b/n

def compute_luminance(r,g,b):
    '''
    perceived luminance
    '''
    return np.sqrt(0.299*(r**2) + 0.587*(g**2) + 0.114*(b**2))
    #return 0.2126*r + 0.7152*g + 0.0722*b
    
    
    
    
def get_colors_by_years(df, year_start, year_end, skip=0):
    '''
    skip the the first to skip-th common color in each row
    to avoid counting for example too much shadow colors
    '''
    assert isinstance(year_start, int)
    assert isinstance(year_end, int)
    assert year_end > year_start
    
    colors = df[(year_start <= df['Year']) & (df['Year'] < year_end)]['Colors']
    
    result = []
    for row in colors:
        c_list = row[1:-1].split(', ')
        c_list = [c[1:-1] for c in c_list][skip:]
        
        result += c_list
        
    return result



def plot_color_scatter(colors, year1, year2, x_max=10, y_max=10, x_min=0, y_min=0):
    '''
    this funtion plot colors as scatter with random position and boldness
    '''
    np.random.shuffle(colors)
    n = len(colors)
    x = [np.random.uniform(x_min, x_max) for i in range(n)]
    y = [np.random.uniform(y_min, y_max) for i in range(n)]
    areas = [np.pi * np.random.randint(2, 8)**2 for i in range(n)]
    # draw the plot
    plt.figure()
    plt.scatter(x, y, s=areas, c=colors, alpha=0.8)
    plt.title(str(year1) + ' - ' + str(year2))

    plt.axis('off')
    plt.show()
    
    
if __name__ == '__main__':
    # read data
    color_space = pd.read_csv('data/color_space.csv')

    df = pd.read_csv('data/df.csv')
    df.loc[df['Year'] > 1890, 'Year'] = 1889

    df_reduced = pd.read_csv('data/df_reduced.csv')
    
    
    # histogram
    plt.hist(df["Year"])
    plt.title("Number of Van Gogh paintings against time")
    plt.xlabel("Year")
    plt.ylabel("Number of paintings")
    
    
    # scatter
    c1 = get_colors_by_years(df, 1862, 1885)
    c2 = get_colors_by_years(df, 1885, 1888)
    c3 = get_colors_by_years(df, 1888, 1890)

    plot_color_scatter(c1, 1862, 1885)
    plot_color_scatter(c2, 1885, 1888)
    plot_color_scatter(c3, 1888, 1890)
    
    
    
    # line
    # plot r/g/b/luminance against year
    rs, gs, bs = [], [], []
    lumi = []
    years = []

    for y in set(df['Year']):
        r,g,b = avg_color_by_year(df, y)
        l = compute_luminance(r, g, b)

        years.append(y)
        rs.append(r)
        gs.append(g)
        bs.append(b)
        lumi.append(l)
        
    plt.plot(years, rs, color='r')
    plt.plot(years, gs, color='g')
    plt.plot(years, bs, color='b')
    plt.plot(years, lumi, color='gray')

    plt.legend(['r', 'g', 'b', 'luminance'])
    plt.ylabel('Year')
    plt.xlabel('Average value')
    plt.title('Average value of R/G/B/Luminance in Van Gogh Paintings across year')