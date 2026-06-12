from bar_plotter import create_bar_plot

values = [0.35, 0.72, 0.51, 0.64, 0.28, 0.83, 0.46, 0.59]

labels = [
    'case A',
    'case B',
    'case C',
    'case D',
    'case E',
    'case F',
    'case G',
    'case H',
]

create_bar_plot(
    values=values,
    labels=labels,

    x_min=0,
    x_max=1,              # automatic maximum from values

    xSymbol='Cost',
    xUnit='EUR',

    filename='bar_plot',
    extension='pdf',

    font='Arial',
    size_ticks=12,
    size_label=14,

    bar_height=0.6,
    line_width=1.2,
    bar_color='blue',

    tick_rounding='auto',
)

'''
#Extended call

create_bar_plot(
    values=values,
    labels=labels,

    x_min=0,
    x_max=None,                    # None means automatic maximum from values

    xSymbol='Cost',
    xUnit='EUR',

    filename='bar_plot',
    extension='pdf',

    font='Arial',

    size_ticks=12,
    size_label=14,
    size_values=12,

    bar_height=0.6,
    line_width=1.2,

    bar_color='black',             # only changes bar outlines
    axis_color='black',            # x-axis line, x-axis ticks, x-axis tick labels
    text_color='black',            # bar labels, bar values, x-axis label
    y_axis_color='lightgray',      # vertical y-axis line

    tick_rounding='auto',
    x_tick_rounding=None,
    value_rounding='auto',

    show_values=True,
    value_gap_frac=0.02,

    x_axis_gap_pt=18,
    x_label_gap_px=10,

    dataNotVisibleOutLimits=False,
'''





