from graph_plotter import create_graph
import numpy as np

np.random.seed(1)

n = 100

X = [
    np.linspace(0, 1, n),
    np.linspace(0, 1, n),
    np.linspace(0, 1, n),
]

Y = [
    0.3 + 0.5 * X[0] + np.random.normal(0, 0.03, n),
    0.8 - 0.5 * X[1] + np.random.normal(0, 0.03, n),
    0.5 + np.random.normal(0, 0.03, n),
]

legends = ['going_up', 'going_down', 'stable']


create_graph(
    x=X,
    y=Y,
    PLotType=['-'] * len(X),
    legend=['going_up', 'going_down', 'stable'],
    xSymbol='Temperature',
    xUnit='C',
    ySymbol='Pressure',
    yUnit='Pa',
    filename='result',
    extension='pdf',

)



#extended call

'''
createGraph(
    x=X,
    y=Y,
    PLotType=['-'] * len(X),

    legend=legends,
    legx=None,
    legy=None,                       # None means automatic inline legend placement

    xSymbol='Temperature',
    xUnit='C',
    ySymbol='Money',
    yUnit='EU',

    limits=None,                     # automatic limits from all datasets

    filename='convergenceStdDev',
    extension='pdf',

    font='Arial',
    size_ticks=12,
    size_label=14,
    size_legend=14,

    color='black',

    addTickX=0,
    extraTickX=[],

    addTickY=0,
    extraTickY=[],

    dataNotVisibleOutLimits=False,

    ColorNames=None,                 # None means use default colour list

    x_label_gap_px=10,
    y_label_gap_px=4,
    y_label_top_gap_px=12,

    tick_rounding='auto',
    x_tick_rounding=None,
    y_tick_rounding=None,
)
'''
