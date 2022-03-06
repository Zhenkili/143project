#!/usr/bin/env python
# coding: utf-8

# # Analysis on Color Distribution and Relationship with Genres and Styles


import csv
from collections import defaultdict, Counter
import numpy as np
import seaborn as sns
import copy
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm
from datetime import datetime
from wordcloud import WordCloud
# get_ipython().run_line_magic('matplotlib', 'inline')


def readCSV(path):
    """
    read csv to dict
    """
    with open(path, 'rt', encoding="utf8") as f:
        c = csv.reader(f)
        header = next(c)
        for l in c:
            d = dict(zip(header, l))
            yield d


def preprocess(raw):
    """
    preprocess data
    """
    data = raw
    for d in data:
        d['Colors'] = eval(d['Colors'])
    return data


# ## 1. Color Dist


def roundColor(color):
    """
    round a color to a color group it belongs to
    """
    color = list(color)
    for i in [2, 4, 6]:
        color[i] = '0'
    return ''.join(color)


def groupColors(colorCnt):
    """
    # group similar colors
    """
    colorRoundCnt = defaultdict(int)
    for c, n in colorCnt.items():
        colorRoundCnt[roundColor(c)] += n
    return colorRoundCnt


def drawColorDist(cnt, threshold, title="Color Distribution in All Painting"):
    """
    draw the distribution of colors
    """
    fig1, ax1 = plt.subplots()
    total = sum(cnt.values())
    print(f"total: {total}")
    thresholdValue = total * threshold
    labels, sizes = zip(*sorted(((i, j) for i, j in cnt.items()
                                 if j > thresholdValue), key=lambda x: -x[1]))
    print(len(labels))
    ax1.pie(sizes,
            colors=labels,
            # labels=labels, autopct='%1.1f%%',
            # shadow=True,
            startangle=90)
    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax1.axis('equal')
    plt.title("{} with Threshold as {}".format(title, threshold))
    fig1.savefig('colorDist_th{}.png'.format(threshold), dpi=600)


# ## 2. Color - Genre


def httpColorToRGB(httpColor):
    """
    http color to RGB tuple
    """
    return [int(httpColor[i:i+2], 16) for i in [1, 3, 5]]


def drawColorCondDist(grouppedCnt, roundGrouppedCnt, threshold, title, nPlotsPerRow=4):
    """ 
    draw conditional distribution of color
    """
    figWidth = nPlotsPerRow * 2.5

    nGroups = len(roundGrouppedCnt)
    nColumns = (2 * nGroups + nPlotsPerRow - 1) // nPlotsPerRow
    fig, axes = plt.subplots(nColumns, nPlotsPerRow)
    fig.set_size_inches(figWidth, figWidth / nPlotsPerRow * nColumns)
    for i, (g, cnt) in enumerate(roundGrouppedCnt.items()):
        # pie chart
        total = sum(cnt.values())
        thresholdValue = total * threshold
        labels, sizes = zip(
            *sorted(((i, j) for i, j in cnt.items() if j > thresholdValue), key=lambda x: -x[1]))
        print(f"{g}:{len(labels)}")
        axes[i*2//nPlotsPerRow][i*2 % nPlotsPerRow].pie(sizes,
                                                        colors=labels,
                                                        # labels=labels, autopct='%1.1f%%',
                                                        # shadow=True,
                                                        startangle=90)
        # Equal aspect ratio ensures that pie is drawn as a circle.
        axes[i*2//nPlotsPerRow][i*2 % nPlotsPerRow].axis('equal')
        axes[i*2//nPlotsPerRow][i*2 % nPlotsPerRow].set_title(g)

        # histogram
        for color, data in zip(['red', 'green', 'blue'], zip(*sum(([httpColorToRGB(c), ] * n for c, n in grouppedCnt[g].items()), []))):
            axes[i*2//nPlotsPerRow][i*2 % nPlotsPerRow +
                                    1].hist(data, bins=32, alpha=0.3, label=color, color=color)

    for i in range(2 * nGroups, nColumns * nPlotsPerRow):
        axes[i//nPlotsPerRow][i % nPlotsPerRow].axis('off')
    fig.suptitle("{} with Threshold as {}".format(title, threshold))
    fig.savefig('{}_th{}.png'.format(title, threshold), dpi=600)


# ## 3. Color - Style

# ## color analysis main routine

def colorAnalysis():
    """
    make analysis on colors, draw and save related pics
    """
    raw = list(readCSV("df.csv"))
    data = preprocess(raw)
    # to verify a color: https://www.w3schools.com/colors/colors_picker.asp

    # 1. color dist
    colorCnt = Counter(sum((list(d['Colors']) for d in data), []))
    colorRoundCnt = groupColors(colorCnt)
    for threshold in [0, 0.001, 0.005]:
        drawColorDist(colorRoundCnt, threshold)

    # 2. color - genre
    genreSet = set([x['Genre'] for x in data])
    print(len(genreSet))
    print(genreSet)
    # rounded counter of colors, groupped by genre
    colorRoundCntByGenre = {g: groupColors(Counter(
        sum((list(d['Colors']) for d in data if d['Genre'] == g), []))) for g in genreSet}
    colorCntByGenre = {g: Counter(
        sum((list(d['Colors']) for d in data if d['Genre'] == g), [])) for g in genreSet}
    drawColorCondDist(colorCntByGenre, colorRoundCntByGenre,
                      0.005, "Color Distribution by Genre", nPlotsPerRow=8)

    # 3. color - style
    styleSet = set([x['Style'] for x in data])
    print(len(styleSet))
    print(styleSet)
    # rounded counter of colors, groupped by genre
    colorRoundCntByStyle = {g: groupColors(Counter(
        sum((list(d['Colors']) for d in data if d['Style'] == g), []))) for g in styleSet}
    colorCntByStyle = {g: Counter(
        sum((list(d['Colors']) for d in data if d['Style'] == g), [])) for g in styleSet}
    drawColorCondDist(colorCntByStyle, colorRoundCntByStyle,
                      0.005, "Color Distribution by Style")


if __name__ == "__main__":
    colorAnalysis()
