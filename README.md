# Graph Plotter

Small Matplotlib utilities for creating clean line plots and horizontal bar plots.

The package currently contains two plotting functions:

* `create_graph(...)` for one or more line or point series.
* `create_bar_plot(...)` for clean horizontal bar plots with outlined bars.

## Repository structure

```text
.
├── graph_plotter.py
├── bar_plotter.py
├── example_graph.py
├── example_bar.py
├── README.md
├── requirements.txt
├── pyproject.toml
├── LICENSE
└── .gitignore
```

## Requirements

```text
matplotlib
numpy
```

The dependencies are listed in both `requirements.txt` and `pyproject.toml`.

## Installation

Clone the repository and move into the project folder:

```bash
git clone <repository-url>
cd graph_plotter_dc
```

Install the package:

```bash
pip install .
```

For development, install it in editable mode:

```bash
pip install -e .
```

Editable mode is useful when you are still changing `graph_plotter.py` or `bar_plotter.py`. Changes in the local project folder are then used directly without reinstalling the package.

After installation, the functions can be imported from anywhere in the same Python environment:

```python
from graph_plotter import create_graph
from bar_plotter import create_bar_plot
```

To check whether the package is installed:

```bash
pip show graph-plotter-dc
```

To uninstall it:

```bash
pip uninstall graph-plotter-dc
```

## Packaging note

If you use both plotting modules, make sure `pyproject.toml` contains both modules:

```toml
[tool.setuptools]
py-modules = ["graph_plotter", "bar_plotter"]
```

## Line plots

Use `create_graph(...)` to plot one or more x-y series with consistent axis formatting, inline labels, and automatic tick formatting.

### Basic line-plot example

```python
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
```

### Extended line-plot example

```python
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

    legend=legends,
    legx=None,
    legy=None,                       # None means automatic inline legend placement

    xSymbol='Temperature',
    xUnit='C',
    ySymbol='Pressure',
    yUnit='Pa',

    limits=None,                     # automatic limits from all datasets

    filename='result',
    extension='pdf',

    font='Arial',
    size_ticks=12,
    size_label=14,
    size_legend=14,

    color='black',

    addTickX=1,
    extraTickX=[],

    addTickY=1,
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
```

## Horizontal bar plots

Use `create_bar_plot(...)` to create horizontal bars with black or coloured outlines, no fill colour, a separate x-axis, and values shown to the right of the bars.

### Basic bar-plot example

```python
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
    x_max=1,
    xSymbol='Cost',
    xUnit='EUR',
    filename='bar_plot',
    extension='pdf',
    bar_color='blue',
)
```

### Extended bar-plot example

```python
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
)
```

## Main options for `create_graph(...)`

### Input data

The `x`, `y`, and `PLotType` arguments must have the same length.

Each entry in `x` and `y` is one data series.

```python
x = [x_series_1, x_series_2]
y = [y_series_1, y_series_2]
PLotType = ['-', '.']
```

### Plot styles

`PLotType` is passed directly to Matplotlib.

Common options are:

```python
'-'     # line
'.'     # points
'o'     # circle markers
'--'    # dashed line
```

### Inline labels

If `legend` is provided and both `legx` and `legy` are `None`, the labels are placed automatically near the corresponding lines.

```python
legend=['case 1', 'case 2']
legx=None
legy=None
```

Manual label positions can also be provided:

```python
legend=['case 1', 'case 2']
legx=[0.8, 0.7]
legy=[0.4, 0.6]
```

### Axis limits

If `limits=None`, the axis limits are computed automatically from all data.

```python
limits=None
```

Manual limits can be passed as:

```python
limits=[xmin, xmax, ymin, ymax]
```

### Extra ticks

By default, only minimum and maximum axis ticks are shown. Extra ticks can be added with:

```python
addTickX=1
extraTickX=[0.5]

addTickY=1
extraTickY=[0.5]
```

## Main options for `create_bar_plot(...)`

### Axis range

If `x_max=None`, the maximum value is taken automatically from the largest bar.

```python
x_min=0
x_max=None
```

You can overwrite the maximum manually:

```python
x_min=0
x_max=1
```

The x-axis itself only shows the minimum and maximum ticks.

### Bar values

By default, values are shown slightly to the right of the bars.

```python
show_values=True
value_gap_frac=0.02
```

Increase `value_gap_frac` to move the values further to the right.

### Bar style

Bars are not filled. Only the outlines are shown.

```python
bar_color='black'
bar_height=0.6
line_width=1.2
```

Changing `bar_color` only changes the bar outlines. It does not change labels, axes, or values.

### Axis and text colours

The colours are controlled separately:

```python
bar_color='black'         # bar outlines only
axis_color='black'        # x-axis line, x-axis ticks, x-axis tick labels
text_color='black'        # bar labels, bar values, x-axis label
y_axis_color='lightgray'  # vertical y-axis line
```

### X-axis spacing

The x-axis can be moved downward, away from the y-axis and the bars.

```python
x_axis_gap_pt=18
```

Increase this value to move the x-axis further down.

## Tick formatting

Both plotting functions support automatic tick formatting.

```python
tick_rounding='auto'
```

With automatic rounding:

```text
abs(value) < 1       -> up to 3 decimals
1 <= abs(value) < 10 -> up to 2 decimals
abs(value) >= 10     -> 0 decimals
```

You can also force a fixed number of decimals:

```python
tick_rounding=2
```

For `create_graph(...)`, axis-specific rounding can be set with:

```python
x_tick_rounding=2
y_tick_rounding=1
```

For `create_bar_plot(...)`, value labels can be rounded separately:

```python
value_rounding=2
```

## Output format

The figures are saved automatically using:

```python
filename='result'
extension='pdf'
```

This creates:

```text
result.pdf
```

Other common extensions are:

```python
extension='svg'
extension='png'
```

## License

This project is released under the MIT License. See the `LICENSE` file for details.

## Author

Diederik Coppitters
