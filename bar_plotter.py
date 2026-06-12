import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter


def create_bar_plot(
    values=None,
    labels=None,
    x_min=0,
    x_max=None,
    xSymbol='',
    xUnit='',
    filename='bar_plot',
    extension='pdf',
    font='Arial',
    size_ticks=12,
    size_label=14,
    size_values=None,
    bar_height=0.6,
    line_width=1.2,
    bar_color='black',
    axis_color='black',
    text_color='black',
    y_axis_color='lightgray',
    tick_rounding='auto',
    x_tick_rounding=None,
    value_rounding='auto',
    show_values=True,
    value_gap_frac=0.02,
    x_axis_gap_pt=18,
    x_label_gap_px=10,
    dataNotVisibleOutLimits=False,
    ax=None,
    save=True,
):
    """
    Create a clean horizontal bar plot.

    Main features:
    - Horizontal bars.
    - Bar outline colour controlled by bar_color.
    - No coloured bar fill.
    - Light-gray vertical y-axis line by default.
    - Horizontal x-axis with only minimum and maximum values.
    - Horizontal x-axis stops at x_min and x_max, even if extra space is added for values.
    - Horizontal axis can be shifted downward.
    - Bar labels shown horizontally next to the bars.
    - Bar values shown slightly right of the end of each bar.
    - Automatic maximum x-value from the largest bar, unless overwritten.
    - Can create a standalone figure or draw into an existing Matplotlib axis.

    Colour controls:
    - bar_color: bar outlines only
    - axis_color: x-axis line, x-axis tick marks, and x-axis tick labels
    - text_color: bar labels, bar values, and x-axis label
    - y_axis_color: vertical y-axis line

    Subplot usage:
    - ax=None creates a new standalone figure.
    - ax=<existing axis> draws into that axis.
    - save=True saves the figure.
    - save=False only draws and returns the axis.
    """

    # ----------------------------- validation ------------------------------------
    if values is None:
        raise ValueError("values must be provided.")

    values = np.asarray(values, dtype=float).ravel()

    if len(values) == 0:
        raise ValueError("values must contain at least one element.")

    if not np.all(np.isfinite(values)):
        raise ValueError("values must only contain finite numbers.")

    if labels is None:
        labels = [''] * len(values)

    if len(labels) != len(values):
        raise ValueError("labels must have the same length as values.")

    if size_values is None:
        size_values = size_ticks

    if x_tick_rounding is None:
        x_tick_rounding = tick_rounding

    if x_max is None:
        x_max = np.max(values)

    if not np.isfinite(x_min) or not np.isfinite(x_max):
        raise ValueError("x_min and x_max must be finite values.")

    if x_max <= x_min:
        raise ValueError("x_max must be larger than x_min.")

    if np.any(values < x_min):
        raise ValueError("All values must be larger than or equal to x_min.")

    # Add extra plotting space to the right for value labels.
    # The visible x-axis line itself will still stop at x_max.
    x_range = x_max - x_min
    value_gap = value_gap_frac * x_range
    plot_x_max = x_max

    if show_values:
        plot_x_max = x_max + 0.12 * x_range

    # ----------------------------- helpers ---------------------------------------
    def _format_value(value, rounding):
        """
        Format one value.

        rounding:
        - 'auto': decimals depend on absolute value
        - int: fixed maximum number of decimals
        - None: simple default string conversion
        """

        if rounding is None:
            return str(value)

        if np.isclose(value, 0.0):
            return "0"

        abs_value = abs(value)

        if rounding == 'auto':
            if abs_value < 1:
                decimals = 3
            elif abs_value < 10:
                decimals = 2
            else:
                decimals = 0

        elif isinstance(rounding, int):
            decimals = max(rounding, 0)

        else:
            raise ValueError(
                "tick_rounding, x_tick_rounding, and value_rounding must be "
                "'auto', an integer, or None."
            )

        formatted = f"{value:.{decimals}f}"

        if "." in formatted:
            formatted = formatted.rstrip("0").rstrip(".")

        if formatted == "-0":
            formatted = "0"

        return formatted

    def _add_custom_x_label(
        fig,
        ax,
        x_label,
        x_max,
        font,
        size_label,
        text_color,
        x_label_gap_px=10,
    ):
        """
        Add a horizontal x-axis label, right-aligned with the x_max tick.
        """

        if x_label == '':
            return

        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()

        x_tick_bboxes = [
            tick.get_window_extent(renderer=renderer)
            for tick in ax.get_xticklabels()
            if tick.get_visible() and tick.get_text() != ''
        ]

        if len(x_tick_bboxes) > 0:
            lowest_x_tick = min(bbox.y0 for bbox in x_tick_bboxes)
        else:
            axes_bbox = ax.get_window_extent(renderer=renderer)
            lowest_x_tick = axes_bbox.y0

        # Use the actual x_max data coordinate, not the full right edge of the axes.
        # This matters because the plot can extend beyond x_max to make room for value labels.
        x_label_x_px = ax.transData.transform((x_max, 0))[0]
        x_label_y_px = lowest_x_tick - x_label_gap_px

        x_label_fig = fig.transFigure.inverted().transform(
            (x_label_x_px, x_label_y_px)
        )

        fig.text(
            x_label_fig[0],
            x_label_fig[1],
            x_label,
            ha='right',
            va='top',
            fontsize=size_label,
            fontname=font,
            color=text_color,
        )

    # --------------------------- plotting core -----------------------------------
    plt.rcParams['mathtext.fontset'] = 'stix'

    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure

    y_positions = np.arange(len(values))

    ax.barh(
        y_positions,
        values - x_min,
        left=x_min,
        height=bar_height,
        facecolor='none',
        edgecolor=bar_color,
        linewidth=line_width,
        clip_on=dataNotVisibleOutLimits,
    )

    # Put first label at the top.
    ax.invert_yaxis()

    # Axis limits
    ax.set_xlim(x_min, plot_x_max)
    ax.set_ylim(len(values) - 0.5, -0.5)

    # Bar labels
    ax.set_yticks(y_positions)
    ax.set_yticklabels(labels)

    # Horizontal axis: only min and actual max, not the extra label margin.
    ax.set_xticks([x_min, x_max])

    ax.xaxis.set_major_formatter(
        FuncFormatter(lambda value, position: _format_value(value, x_tick_rounding))
    )

    # Bar values slightly right of bar ends.
    if show_values:
        for y_pos, value in zip(y_positions, values):
            ax.text(
                value + value_gap,
                y_pos,
                _format_value(value, value_rounding),
                ha='left',
                va='center',
                fontsize=size_values,
                fontname=font,
                color=text_color,
                clip_on=dataNotVisibleOutLimits,
            )

    # Spine styling
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # Light-gray vertical y-axis line.
    ax.spines['left'].set_color(y_axis_color)
    ax.spines['left'].set_linewidth(line_width)
    ax.spines['left'].set_position(('outward', 0))

    # Horizontal x-axis, shifted downward.
    # It stops at x_min and x_max even though the plot area may extend further right.
    ax.spines['bottom'].set_color(axis_color)
    ax.spines['bottom'].set_linewidth(line_width)
    ax.spines['bottom'].set_position(('outward', x_axis_gap_pt))
    ax.spines['bottom'].set_bounds(x_min, x_max)

    # Tick styling
    ax.tick_params(axis='x', direction='in', colors=axis_color)
    ax.tick_params(axis='y', length=0, colors=text_color, pad=6)

    for ticklabel in ax.get_xticklabels():
        ticklabel.set_fontsize(size_ticks)
        ticklabel.set_fontname(font)
        ticklabel.set_color(axis_color)

    for ticklabel in ax.get_yticklabels():
        ticklabel.set_fontsize(size_ticks)
        ticklabel.set_fontname(font)
        ticklabel.set_color(text_color)

    # Optional x-axis label
    if xUnit == '':
        x_label = xSymbol
    else:
        x_label = f"{xSymbol} [{xUnit}]"

    _add_custom_x_label(
        fig=fig,
        ax=ax,
        x_label=x_label,
        x_max=x_max,
        font=font,
        size_label=size_label,
        text_color=text_color,
        x_label_gap_px=x_label_gap_px,
    )

    # Save file
    if save:
        fig.savefig(f"{filename}.{extension}", bbox_inches='tight')

    return ax