# Graph Plotter

A small Python utility for creating clean Matplotlib figures with automatic axis limits, inline curve labels, custom colours, and automated tick formatting.

The main function is `create_graph`, defined in `graph_plotter.py`.

## Features

* Plot one or more `(x, y)` datasets.
* Automatically set the x- and y-axis limits from all datasets.
* Use a fixed default colour palette.
* Add inline curve labels instead of a standard legend box.
* Colour inline labels with the same colour as the corresponding dataset.
* Place horizontal x- and y-axis labels automatically.
* Put the y-axis unit on a second line.
* Format tick labels automatically based on their magnitude.
* Save figures directly as PDF, SVG, PNG, or another Matplotlib-supported format.

## Repository structure

```text
.
├── graph_plotter.py
├── example.py
├── requirements.txt
└── README.md
```

## Requirements

```text
matplotlib
numpy
```

Install them with:

```bash
pip install -r requirements.txt
```

A minimal `requirements.txt` is:

```text
matplotlib
numpy
```

## Basic usage

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
    PLotType=['.'] * len(X),
    legend=['going_up', 'going_down', 'stable'],
    xSymbol='Temperature',
    xUnit='C',
    ySymbol='Money',
    yUnit='EU',
    filename='convergenceStdDev',
    extension='pdf',
)
```

This creates:

```text
convergenceStdDev.pdf
```

## Input format

The data should be provided as lists of datasets.

```python
X = [
    x_values_dataset_1,
    x_values_dataset_2,
]

Y = [
    y_values_dataset_1,
    y_values_dataset_2,
]
```

Each `X[i]` is plotted against `Y[i]`.

The number of x-datasets, y-datasets, and plot styles must match:

```python
len(x) == len(y) == len(PLotType)
```

## Plot styles

`PLotType` uses standard Matplotlib style strings.

Examples:

```python
PLotType=['-'] * len(X)      # solid lines
PLotType=['.'] * len(X)      # points
PLotType=['--'] * len(X)     # dashed lines
```

Avoid hard-coding colours in `PLotType`, for example `'-k'`, because this overrides the automatic colour palette.

## Default colours

If `ColorNames=None`, the function uses:

```python
[
    'darkkhaki',
    'cornflowerblue',
    'green',
    'mediumseagreen',
    'tab:red',
    'lightcoral',
]
```

To use custom colours:

```python
create_graph(
    x=X,
    y=Y,
    PLotType=['-'] * len(X),
    ColorNames=['black', 'tab:blue', 'tab:red'],
)
```

## Inline labels

Inline labels can be added with `legend`.

```python
create_graph(
    x=X,
    y=Y,
    PLotType=['-'] * len(X),
    legend=['case A', 'case B', 'case C'],
)
```

If `legx=None` and `legy=None`, the labels are positioned automatically near their corresponding curves.

Manual label positions can also be provided:

```python
create_graph(
    x=X,
    y=Y,
    PLotType=['-'] * len(X),
    legend=['case A', 'case B'],
    legx=[0.8, 0.8],
    legy=[0.7, 0.3],
)
```

## Axis limits

By default, axis limits are computed automatically from all datasets:

```python
limits=None
```

Manual limits can be provided as:

```python
limits=[xmin, xmax, ymin, ymax]
```

Example:

```python
create_graph(
    x=X,
    y=Y,
    PLotType=['-'] * len(X),
    limits=[0, 1, 0, 1],
)
```

## Axis labels

Axis names and units are set separately:

```python
create_graph(
    x=X,
    y=Y,
    PLotType=['-'] * len(X),
    xSymbol='Temperature',
    xUnit='C',
    ySymbol='Money',
    yUnit='EU',
)
```

The x-axis label is shown horizontally below the x-axis.

The y-axis label is shown horizontally above the y-axis, with the unit on the next line.

## Tick formatting

Tick labels are formatted automatically by default:

```python
tick_rounding='auto'
```

The default logic is:

```text
abs(value) < 1       -> up to 3 decimals
1 <= abs(value) < 10 -> up to 2 decimals
abs(value) >= 10     -> 0 decimals
```

Use fixed rounding for both axes:

```python
create_graph(
    x=X,
    y=Y,
    PLotType=['-'] * len(X),
    tick_rounding=2,
)
```

Use different rounding for each axis:

```python
create_graph(
    x=X,
    y=Y,
    PLotType=['-'] * len(X),
    x_tick_rounding=0,
    y_tick_rounding=3,
)
```

Disable custom tick formatting:

```python
create_graph(
    x=X,
    y=Y,
    PLotType=['-'] * len(X),
    tick_rounding=None,
)
```

## Extra ticks

Extra ticks can be added manually.

```python
create_graph(
    x=X,
    y=Y,
    PLotType=['-'] * len(X),
    addTickX=2,
    extraTickX=[0.25, 0.75],
    addTickY=1,
    extraTickY=[0.5],
)
```

Ticks are built as:

```text
[min, extra ticks, max]
```

## Font sizes

The function separates font sizes for tick labels, axis labels, and inline labels.

```python
create_graph(
    x=X,
    y=Y,
    PLotType=['-'] * len(X),
    size_ticks=12,
    size_label=14,
    size_legend=14,
)
```

## Output format

The figure is saved automatically using `filename` and `extension`.

```python
create_graph(
    x=X,
    y=Y,
    PLotType=['-'] * len(X),
    filename='my_figure',
    extension='svg',
)
```

This creates:

```text
my_figure.svg
```

## Extended example

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
    legy=None,

    xSymbol='Temperature',
    xUnit='C',
    ySymbol='Money',
    yUnit='EU',

    limits=None,

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

    ColorNames=None,

    x_label_gap_px=10,
    y_label_gap_px=4,
    y_label_top_gap_px=12,

    tick_rounding='auto',
    x_tick_rounding=None,
    y_tick_rounding=None,
)
```

## Notes

This function is intended for simple, reusable plotting workflows. It is useful when several figures should share the same styling rules.

For more complex figures, direct Matplotlib customization may still be needed. The function returns the Matplotlib `Axes` object, so additional changes can be made after calling `create_graph`.

```python
ax = create_graph(
    x=X,
    y=Y,
    PLotType=['-'] * len(X),
)

ax.set_title("Additional custom title")
```

## License

This project is licensed under the MIT License.

You are free to use, modify, and distribute this code, provided that the original copyright notice and license text are included.

See the [`LICENSE`](LICENSE) file for details.

## Author

Diederik Coppitters