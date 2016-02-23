#!/bin/python2
import matplotlib.pyplot as plt
import matplotlib as mpl
import sys
import csv
import numpy as np
mpl.rcParams['font.stretch'] = 'condensed'
mpl.rcParams['font.serif'] = ['Gentium Basic']
mpl.rcParams['font.family'] = 'serif'

def barPlot(spec):
    if type(spec['data']) is dict:
        data = spec['data']
        if spec['keyOrder']:
          categories = spec['keyOrder']
          categories.reverse()
          values = [data[c] for c in categories]
        else:
          categories = [key for key in data]
          values = [data[key] for key in data]
          categories = [x for (y,x) in sorted(zip(values, categories), key=lambda pair: pair[0])]
          values = sorted(values)
    elif type(spec['data']) is str:
        dataFile = open(spec['data'], r)
        csvData = csv.reader(dataFile, delimiter = spec['delimiter'])
        data = {}
        for x in csvData:
            data[x[0]] = x[1]
    fig = plt.figure(figsize=(8,4))
    ax = fig.add_axes((.1, .8, .8, .9))
    pos = np.arange(len(categories)) + .5
    rects = ax.barh(pos, values, align='center', color=spec['color'], edgecolor=spec['color'])
    for i in range(0,len(rects)):
        r = rects[i]
        length = r.get_width()
        alignment = 'right' if values[i]<0 else 'left'
        if spec['decimals']:
            valString = '{0:.1f}'.format(values[i])
        else:
            valString = int(values[i])
        ax.text(values[i] + (.52*r.get_height())*((values[i]+0.0001)/abs(values[i]+0.0001)), r.get_y()+r.get_height()/2, valString, ha=alignment, va='center')
    plt.yticks(pos, categories)
    plt.ylabel(spec['ylabel'])
    plt.xlabel(spec['xlabel'])
    if spec['lims']:
        plt.xlim(spec['lims'])
    plt.title(spec['title'])
    plt.figtext(.1, .63, 'ElectoralStatistics.com', color='#283D4B', ha='left')
    if spec['source']:
        plt.figtext(.9, .63, 'Source: ' + spec['source'], color='#283D4B', ha='right')
    plt.savefig(spec['outfile'], bbox_inches='tight')

def stackedBarPlot(spec):
    data = spec['data']
    fields = spec['fields']
    categories = [key for key in data]
    sumValues = [sum(data[key]) for key in categories]
    values = [data[key] for key in categories]
    categories = [x for (y,x) in sorted(zip(sumValues, categories), key=lambda pair: pair[0])]
    values =  [x for (y,x) in sorted(zip(sumValues, values), key=lambda pair: pair[0])]
    sumValues =  sorted(sumValues)
    fig = plt.figure(figsize=(8,4))
    ax = fig.add_axes((.1, .8, .8, .9))
    pos = np.arange(len(categories)) + .5
    widths = np.multiply(sumValues, 0)
    rectangles = []
    fields2 = []
    for n in range(0,len(fields)):
        j = len(fields) - 1 - n
        field = fields[j]
        value = [x[j] for x in values]
        rects = ax.barh(pos, value, align='center', color=spec['colors'][j], edgecolor=spec['colors'][j], left=widths)
        widths = np.add(widths, value)
        for i in range(0,len(rects)):
            r = rects[i]
            alignment = 'right' if value[i]<0 else 'left'
            if spec['decimals']:
                valString = '{0:.1f}'.format(value[i])
            else:
                valString = int(value[i])
            if not spec['labelendonly']:
                ax.text(-(.5*r.get_width())+(widths[i]), r.get_y()+r.get_height()/2, valString, ha=alignment, va='center')
        rectangles.append(rects[0])
        fields2.append(field)
    if spec['labelend']:
        for i in range(0, len(pos)):
            r = rectangles[0]
            ax.text(sumValues[i] +  (.52*r.get_height()), pos[i],  '{0:.1f}'.format(sumValues[i]), ha=alignment, va='center')
    plt.legend(rectangles, fields2, frameon=False, bbox_to_anchor=(.5,-.25), borderaxespad=0.5, loc='center')
    plt.yticks(pos, categories)
    plt.ylabel(spec['ylabel'])
    plt.xlabel(spec['xlabel'])
    if spec['lims']:
        plt.xlim(spec['lims'])
    plt.title(spec['title'])
    plt.figtext(.1, .45, 'ElectoralStatistics.com', color='#283D4B', ha='left')
    if spec['source']:
        plt.figtext(.9, .45, 'Source: ' + spec['source'], color='#283D4B', ha='right')
    plt.savefig(spec['outfile'], bbox_inches='tight')

def multiBarPlot(spec):
    data = spec['data']
    plots = spec['plots']
    valuesinit = [data[key][0] for key in data]
    categories = [key for key in data]
    categories = [x for (y,x) in sorted(zip(valuesinit, categories), key=lambda pair: pair[0])]
    f, axarr = plt.subplots(1, plots, sharey=True, figsize = (12,6))
    pos = np.arange(len(categories)) + .5
    plt.yticks(pos, categories)
    for p in range(0, plots):
        ax = axarr[p]
        values = [x for (y,x) in sorted(zip(valuesinit, [data[k][p] for k in data]), key=lambda pair: pair[0])]
        rects = ax.barh(pos, values, align='center', color=spec['color'], edgecolor=spec['color'])
        for i in range(0,len(rects)):
            r = rects[i]
            length = r.get_width()
            alignment = 'right' if values[i]<0 else 'left'
            if spec['decimals']:
                valString = '{0:.1f}'.format(values[i])
            else:
                valString = int(values[i])
            ax.text(values[i] + (.52*r.get_height())*(values[i]/abs(values[i])), r.get_y()+r.get_height()/2, valString, ha=alignment, va='center')
        ax.set_title(spec['fields'][p])
        ax.set_ylabel(spec['ylabels'][p])
        ax.set_xlabel(spec['xlabels'][p])
        if spec['lims']:
            ax.set_xlim(spec['lims'][p])
    plt.suptitle(spec['title'])
    plt.figtext(0.1, -0.03, 'ElectoralStatistics.com', color='#283D4B', ha='left')
    if spec['source']:
        plt.figtext(.9, -.03, 'Source: ' + spec['source'], color='#283D4B', ha='right')
    plt.savefig(spec['outfile'], bbox_inches='tight')


def scatterPlot(spec):
    if type(spec['data']) is dict:
        x = spec['data']['x']
        y = spec['data']['y']
    elif type(spec['data']) is list and len(spec['data'])==2:
        x = spec['data'][0]
        y = spec['data'][1]
    elif type(spec['data']) is list and len(spec['data'])!=2:
        x = [z[0] for z in spec['data']]
        y = [z[1] for z in spec['data']]
    elif type(spec['data']) is str:
        dataFile = open(spec['data'], "r")
        csvData = csv.reader(dataFile, delimiter = spec['delimiter'])
        data = [z for z in csvData]
        x = [float(z[0]) for z in data]
        y = [float(z[1]) for z in data]
    fig = plt.figure(figsize=(8,4))
    ax = fig.add_axes((.1, .8, .8, .9))
    plt.scatter(x,y, c=spec['color'], marker='.', lw=0, s=130)
    if spec['connect']:
        plt.plot(x,y, c=spec['color'])
    plt.ylabel(spec['ylabel'])
    plt.xlabel(spec['xlabel'])
    if spec['lims']:
        plt.xlim(spec['lims'][0])
        plt.ylim(spec['lims'][1])
    else:
        plt.xlim(ax.get_xlim())
        plt.ylim(ax.get_ylim())
    if spec['regress']:
        m, b = np.polyfit(x, y, 1)
        print m, b
        plotx = np.arange(np.floor(ax.get_xlim()[0]), 2*np.ceil(ax.get_xlim()[1]))
        ploty = np.add(np.multiply(plotx, m),b)
        plt.plot(plotx, ploty, c=spec['regresscolor'])
    if spec['line']:
        m = spec['line'][0]
        b = spec['line'][1]
        plotx = np.arange(np.floor(ax.get_xlim()[0]), 2*np.ceil(ax.get_xlim()[1]))
        ploty = np.add(np.multiply(plotx, m),b)
        plt.plot(plotx, ploty, c=spec['linecolor'])
    if spec['add_axes']:
        plt.axhline(0, color="#000000")
        plt.axvline(0, color="#000000")
    plt.title(spec['title'])
    plt.figtext(.1, .63, 'ElectoralStatistics.com', color='#283D4B', ha='left')
    if spec['source']:
        plt.figtext(.9, .63, 'Source: ' + spec['source'], color='#283D4B', ha='right')
    plt.savefig(spec['outfile'], bbox_inches='tight')

def bubbleScatter(spec):
    if type(spec['data']) is dict:
        x = spec['data']['x']
        y = spec['data']['y']
        s = spec['data']['s']
    elif type(spec['data']) is list and len(spec['data'])==2:
        x = spec['data'][0]
        y = spec['data'][1]
        s = spec['data'][2]
    elif type(spec['data']) is list and len(spec['data'])!=2:
        x = [z[0] for z in spec['data']]
        y = [z[1] for z in spec['data']]
        s = [z[2] for z in spec['data']]
    elif type(spec['data']) is str:
        dataFile = open(spec['data'], "r")
        csvData = csv.reader(dataFile, delimiter = spec['delimiter'])
        data = [z for z in csvData]
        x = [z[0] for z in data]
        y = [float(z[1]) for z in data]
        s = [float(z[2])*100 for z in data]
    refFile = open(spec['reference'], "r")
    csvRef = csv.reader(refFile, delimiter = spec['delimiter'])
    ref = [z for z in csvRef]
    print ref
    xref = [z[0] for z in ref]
    yref = [float(z[1]) for z in ref]
    sref = [float(z[2])*100 for z in ref]
    print xref, yref
    fig = plt.figure(figsize=(8,4))
    ax = fig.add_axes((.1, .8, .8, .9))
    plt.scatter(x,y, c=spec['color'], marker='.', lw=0, s=s, alpha=.4)
    plt.scatter(xref, yref, facecolors='none', marker='.', lw=.5, s=sref)
    if spec['connect']:
        plt.plot(x,y, c=spec['color'])
    plt.ylabel(spec['ylabel'])
    plt.xlabel(spec['xlabel'])
    if spec['lims']:
        plt.xlim(spec['lims'][0])
        plt.ylim(spec['lims'][1])
    else:
        plt.xlim(ax.get_xlim())
        plt.ylim(ax.get_ylim())
    if spec['regress']:
        m, b = np.polyfit(x, y, 1)
        print m, b
        plotx = np.arange(np.floor(ax.get_xlim()[0]), 2*np.ceil(ax.get_xlim()[1]))
        ploty = np.add(np.multiply(plotx, m),b)
        plt.plot(plotx, ploty, c=spec['regresscolor'])
    if spec['line']:
        m = spec['line'][0]
        b = spec['line'][1]
        plotx = np.arange(np.floor(ax.get_xlim()[0]), 2*np.ceil(ax.get_xlim()[1]))
        ploty = np.add(np.multiply(plotx, m),b)
        plt.plot(plotx, ploty, c=spec['linecolor'])
    if spec['add_axes']:
        plt.axhline(0, color="#000000")
        plt.axvline(0, color="#000000")
    plt.title(spec['title'])
    plt.figtext(.1, .63, 'ElectoralStatistics.com', color='#283D4B', ha='left')
    if spec['source']:
        plt.figtext(.9, .63, 'Source: ' + spec['source'], color='#283D4B', ha='right')
    plt.savefig(spec['outfile'], bbox_inches='tight')




specFileLocation = sys.argv[1]
spec = {"title":"",
        "xlabel":"",
        "ylabel":"",
        "type":"barplot",
        "color":"#1185D7",
        "regresscolor":"#1185D7",
        "linecolor":"#1185D7",
        "colors":["#1185D7", "#54A7E2", "#22435A"],
        "regress":False,
        "connect":False,
        "delimiter":" ",
        "source":"",
        "lims":"",
        "plots":1,
        "ylabels":["","","","","","","",""],
        "xlabels":["","","","","","","",""],
        "decimals":True,
        "line":False,
        "outfile":False,
        "add_axes":False,
	"keyOrder":False,
	"labelend":False,
	"labelendonly":False,
}
execfile(specFileLocation, spec)
spec['outfile'] = spec['outfile'] if spec['outfile'] else specFileLocation.replace(".conf", ".png")
if spec['type'] == "barplot":
    barPlot(spec)
elif spec['type'] == "multibarplot":
    multiBarPlot(spec)
elif spec['type'] == 'stackedbarplot':
    stackedBarPlot(spec)
elif spec['type'] == 'scatter':
    scatterPlot(spec)
elif spec['type'] == 'bubblescatter':
  bubbleScatter(spec)
