import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter


def create_graph(
    x=None,
    y=None,
    PLotType=None,
    legend=None,
    legx=None,
    legy=None,
    xSymbol='',
    xUnit='',
    ySymbol='',
    yUnit='',
    limits=None,
    filename='result',
    extension='pdf',
    font='Arial',
    size_ticks=12,
    size_label=14,
    size_legend=14,
    color='black',
    addTickX=1,
    extraTickX=None,
    addTickY=1,
    extraTickY=None,
    dataNotVisibleOutLimits=False,
    ColorNames=None,
    x_label_gap_px=10,
    y_label_gap_px=4,
    y_label_top_gap_px=12,
    tick_rounding='auto',
    x_tick_rounding=None,
    y_tick_rounding=None,
    ax=None,
    save=True,
):
    """
    Plot one or more (x, y) series with consistent styling.

    Main features:
    - Uses a fixed default colour list.
    - Automatically sets axis limits from all x and y datasets if limits=None.
    - Places inline legend labels automatically if legend is provided and legx=legy=None.
    - Colours inline legend labels with the same colour as the corresponding line.
    - Places the x-axis label horizontally below the final x tick.
    - Places the y-axis label horizontally above the top y tick.
    - Places the y-axis unit on a second line, right-aligned.
    - Formats tick labels automatically.
    - Can create a standalone figure or draw into an existing Matplotlib axis.

    Subplot usage:
    - ax=None creates a new standalone figure.
    - ax=<existing axis> draws into that axis.
    - save=True saves the figure.
    - save=False only draws and returns the axis.
    """

    # ----------------------------- validation ------------------------------------
    if x is None or y is None or PLotType is None:
        raise ValueError("x, y, and PLotType must be provided.")

    if not (len(x) == len(y) == len(PLotType)):
        raise ValueError("x, y, and PLotType must have the same number of series.")

    L = len(x)

    if L == 0:
        raise ValueError("At least one data series must be provided.")

    auto_legend_position = False

    if legend is not None:
        if len(legend) != L:
            raise ValueError("legend must match the number of series.")

        if legx is None and legy is None:
            auto_legend_position = True

        elif legx is not None and legy is not None:
            if not (len(legx) == len(legy) == L):
                raise ValueError("legx and legy must match the number of series.")

        else:
            raise ValueError(
                "Provide both legx and legy, or set both to None for automatic placement."
            )

    if extraTickX is None:
        extraTickX = []

    if extraTickY is None:
        extraTickY = []

    if x_tick_rounding is None:
        x_tick_rounding = tick_rounding

    if y_tick_rounding is None:
        y_tick_rounding = tick_rounding

    default_colors = [
        'darkkhaki',
        'cornflowerblue',
        'green',
        'mediumseagreen',
        'tab:red',
        'lightcoral',
    ]

    if ColorNames is None or len(ColorNames) == 0:
        ColorNames = default_colors

    # ----------------------------- helpers ---------------------------------------
    def _adjust_spines(ax, spines=('left', 'bottom')):
        """Show only selected spines and move them outward."""
        for loc, spine in ax.spines.items():
            if loc in spines:
                spine.set_position(('outward', 35))
            else:
                spine.set_color('none')

        ax.yaxis.set_ticks_position('left' if 'left' in spines else 'none')
        ax.xaxis.set_ticks_position('bottom' if 'bottom' in spines else 'none')

    def _build_ticks(minmax, n_extra, extras):
        """Return [min, *extras[:n_extra], max]."""
        lo, hi = minmax

        if not isinstance(n_extra, int) or n_extra <= 0 or len(extras) == 0:
            return [lo, hi]

        take = min(n_extra, len(extras))

        return [lo, *extras[:take], hi]

    def _compute_limits(x_data, y_data):
        """Compute axis limits from all finite x and y values."""
        all_x = np.concatenate([
            np.asarray(xi, dtype=float).ravel()
            for xi in x_data
        ])

        all_y = np.concatenate([
            np.asarray(yi, dtype=float).ravel()
            for yi in y_data
        ])

        all_x = all_x[np.isfinite(all_x)]
        all_y = all_y[np.isfinite(all_y)]

        if len(all_x) == 0 or len(all_y) == 0:
            raise ValueError("x and y must contain at least one finite value.")

        xmin = np.min(all_x)
        xmax = np.max(all_x)
        ymin = np.min(all_y)
        ymax = np.max(all_y)

        return [xmin, xmax, ymin, ymax]

    def _format_tick_value(value, rounding):
        """
        Format one tick value.

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
                "tick_rounding, x_tick_rounding, and y_tick_rounding must be "
                "'auto', an integer, or None."
            )

        formatted = f"{value:.{decimals}f}"

        if "." in formatted:
            formatted = formatted.rstrip("0").rstrip(".")

        if formatted == "-0":
            formatted = "0"

        return formatted

    def _apply_tick_formatting(ax, x_rounding, y_rounding):
        """Apply tick-label formatting to x- and y-axes."""

        ax.xaxis.set_major_formatter(
            FuncFormatter(lambda value, position: _format_tick_value(value, x_rounding))
        )

        ax.yaxis.set_major_formatter(
            FuncFormatter(lambda value, position: _format_tick_value(value, y_rounding))
        )

    def _point_box_distance(points, box):
        """Minimum pixel distance between points and a rectangular box."""
        x0, y0, x1, y1 = box

        dx = np.maximum(np.maximum(x0 - points[:, 0], 0), points[:, 0] - x1)
        dy = np.maximum(np.maximum(y0 - points[:, 1], 0), points[:, 1] - y1)

        return np.sqrt(dx**2 + dy**2)

    def _box_overlap(box_a, box_b):
        """Area of overlap between two rectangular boxes."""
        ax0, ay0, ax1, ay1 = box_a
        bx0, by0, bx1, by1 = box_b

        overlap_x = max(0, min(ax1, bx1) - max(ax0, bx0))
        overlap_y = max(0, min(ay1, by1) - max(ay0, by0))

        return overlap_x * overlap_y

    def _add_custom_axis_labels(
        fig,
        ax,
        xSymbol,
        xUnit,
        ySymbol,
        yUnit,
        font,
        size_label,
        color,
        x_label_gap_px=10,
        y_label_gap_px=4,
        y_label_top_gap_px=12,
    ):
        """
        Add horizontal x- and y-axis labels with automatic positioning.
        """

        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()

        axes_bbox = ax.get_window_extent(renderer=renderer)

        x_label = xSymbol if xUnit == '' else f"{xSymbol} [{xUnit}]"

        if yUnit == '':
            y_label = ySymbol
        else:
            y_label = f"{ySymbol}\n[{yUnit}]"

        # ------------------------- x-axis label -------------------------
        x_tick_bboxes = [
            tick.get_window_extent(renderer=renderer)
            for tick in ax.get_xticklabels()
            if tick.get_visible() and tick.get_text() != ''
        ]

        if len(x_tick_bboxes) > 0:
            lowest_x_tick = min(bbox.y0 for bbox in x_tick_bboxes)
        else:
            lowest_x_tick = axes_bbox.y0

        x_label_x_px = axes_bbox.x1
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
            color=color,
        )

        # ------------------------- y-axis label -------------------------
        y_tick_bboxes = [
            tick.get_window_extent(renderer=renderer)
            for tick in ax.get_yticklabels()
            if tick.get_visible() and tick.get_text() != ''
        ]

        if len(y_tick_bboxes) > 0:
            top_y_tick = max(bbox.y1 for bbox in y_tick_bboxes)
        else:
            top_y_tick = axes_bbox.y1

        spine_outward_pt = 35
        spine_outward_px = spine_outward_pt * fig.dpi / 72

        y_axis_x_px = axes_bbox.x0 - spine_outward_px
        y_label_right_edge_px = y_axis_x_px - y_label_gap_px
        y_label_bottom_px = top_y_tick + y_label_top_gap_px

        y_label_fig = fig.transFigure.inverted().transform(
            (y_label_right_edge_px, y_label_bottom_px)
        )

        fig.text(
            y_label_fig[0],
            y_label_fig[1],
            y_label,
            ha='right',
            va='bottom',
            multialignment='right',
            linespacing=1.1,
            fontsize=size_label,
            fontname=font,
            color=color,
        )

    def _auto_place_inline_labels(ax, x_data, y_data, labels, text_styles):
        """
        Place inline labels close to their corresponding lines while trying to avoid
        overlap with data lines, other labels, and the plot boundary.
        """
        fig = ax.figure
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()

        axes_bbox = ax.get_window_extent(renderer=renderer)

        all_points_display = []

        for xi, yi in zip(x_data, y_data):
            xi = np.asarray(xi, dtype=float).ravel()
            yi = np.asarray(yi, dtype=float).ravel()

            mask = np.isfinite(xi) & np.isfinite(yi)
            xi = xi[mask]
            yi = yi[mask]

            if len(xi) == 0:
                continue

            points = np.column_stack([xi, yi])

            sampled = []

            for j in range(len(points) - 1):
                p0 = points[j]
                p1 = points[j + 1]

                for t in np.linspace(0.0, 1.0, 20):
                    sampled.append(p0 + t * (p1 - p0))

            sampled.append(points[-1])

            sampled = np.asarray(sampled)
            sampled_display = ax.transData.transform(sampled)
            all_points_display.append(sampled_display)

        if len(all_points_display) > 0:
            all_points_display = np.vstack(all_points_display)
        else:
            all_points_display = np.empty((0, 2))

        placed_boxes = []

        def _outside_axes_penalty(box):
            x0, y0, x1, y1 = box

            penalty = 0.0
            penalty += max(0, axes_bbox.x0 - x0)
            penalty += max(0, x1 - axes_bbox.x1)
            penalty += max(0, axes_bbox.y0 - y0)
            penalty += max(0, y1 - axes_bbox.y1)

            return penalty

        for i, label in enumerate(labels):
            if label == "":
                continue

            xi = np.asarray(x_data[i], dtype=float).ravel()
            yi = np.asarray(y_data[i], dtype=float).ravel()

            mask = np.isfinite(xi) & np.isfinite(yi)
            xi = xi[mask]
            yi = yi[mask]

            if len(xi) == 0:
                continue

            temp_text = ax.text(
                0,
                0,
                label,
                fontdict=text_styles[i],
                visible=False,
            )

            bbox = temp_text.get_window_extent(renderer=renderer)
            text_width = bbox.width
            text_height = bbox.height
            temp_text.remove()

            points_data = np.column_stack([xi, yi])
            points_display = ax.transData.transform(points_data)

            candidate_indices = list(range(len(points_display) - 1, -1, -1))

            candidate_offsets = [
                (10, 0, "left", "center"),
                (-10, 0, "right", "center"),
                (10, 10, "left", "bottom"),
                (10, -10, "left", "top"),
                (-10, 10, "right", "bottom"),
                (-10, -10, "right", "top"),
                (0, 12, "center", "bottom"),
                (0, -12, "center", "top"),
                (18, 0, "left", "center"),
                (-18, 0, "right", "center"),
                (18, 14, "left", "bottom"),
                (18, -14, "left", "top"),
                (-18, 14, "right", "bottom"),
                (-18, -14, "right", "top"),
            ]

            best_score = np.inf
            best_position_data = None
            best_ha = "left"
            best_va = "center"
            best_box = None

            for rank, idx in enumerate(candidate_indices):
                point_display = points_display[idx]

                for dx, dy, ha, va in candidate_offsets:
                    label_x = point_display[0] + dx
                    label_y = point_display[1] + dy

                    if ha == "left":
                        x0 = label_x
                        x1 = label_x + text_width
                    elif ha == "right":
                        x0 = label_x - text_width
                        x1 = label_x
                    else:
                        x0 = label_x - text_width / 2
                        x1 = label_x + text_width / 2

                    if va == "bottom":
                        y0 = label_y
                        y1 = label_y + text_height
                    elif va == "top":
                        y0 = label_y - text_height
                        y1 = label_y
                    else:
                        y0 = label_y - text_height / 2
                        y1 = label_y + text_height / 2

                    margin = 4
                    box = (
                        x0 - margin,
                        y0 - margin,
                        x1 + margin,
                        y1 + margin,
                    )

                    score = 0.0

                    score += 1000.0 * _outside_axes_penalty(box)

                    if len(all_points_display) > 0:
                        distances = _point_box_distance(all_points_display, box)
                        min_distance = np.min(distances)

                        if min_distance < 8:
                            score += 500.0 * (8 - min_distance)

                    for placed_box in placed_boxes:
                        score += 1000.0 * _box_overlap(box, placed_box)

                    score += rank * 2.0
                    score += 0.01 * np.sqrt(dx**2 + dy**2)

                    if score < best_score:
                        best_score = score
                        best_position_display = np.array([label_x, label_y])
                        best_position_data = ax.transData.inverted().transform(
                            best_position_display
                        )
                        best_ha = ha
                        best_va = va
                        best_box = box

            if best_position_data is not None:
                ax.text(
                    best_position_data[0],
                    best_position_data[1],
                    label,
                    fontdict=text_styles[i],
                    ha=best_ha,
                    va=best_va,
                )

                placed_boxes.append(best_box)

    # --------------------------- automatic limits --------------------------------
    if limits is None:
        limits = _compute_limits(x, y)

    elif len(limits) != 4:
        raise ValueError("limits must be None or [xmin, xmax, ymin, ymax].")

    # --------------------------- plotting core -----------------------------------
    plt.rcParams['mathtext.fontset'] = 'stix'

    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure

    text_styles = []

    for i in range(L):
        line_kwargs = {
            'clip_on': dataNotVisibleOutLimits,
            'color': ColorNames[i % len(ColorNames)],
        }

        line_objs = ax.plot(
            x[i],
            y[i],
            PLotType[i],
            **line_kwargs,
        )

        color_i = line_objs[0].get_color()

        text_styles.append({
            'family': font,
            'color': color_i,
            'weight': 'normal',
            'size': size_legend,
        })

    # Axis limits
    ax.set_xlim(limits[0], limits[1])
    ax.set_ylim(limits[2], limits[3])

    # Explicit ticks
    ax.set_xticks(_build_ticks(limits[:2], addTickX, extraTickX))
    ax.set_yticks(_build_ticks(limits[2:], addTickY, extraTickY))

    # Tick formatting
    _apply_tick_formatting(
        ax=ax,
        x_rounding=x_tick_rounding,
        y_rounding=y_tick_rounding,
    )

    # Spine and tick styling
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    _adjust_spines(ax, ('left', 'bottom'))

    ax.tick_params(axis='both', direction='in', colors=color)
    ax.spines['left'].set_color(color)
    ax.spines['bottom'].set_color(color)

    # Tick fonts
    for ticklabel in ax.get_xticklabels() + ax.get_yticklabels():
        ticklabel.set_fontsize(size_ticks)
        ticklabel.set_fontname(font)

    # Custom horizontal axis labels
    _add_custom_axis_labels(
        fig=fig,
        ax=ax,
        xSymbol=xSymbol,
        xUnit=xUnit,
        ySymbol=ySymbol,
        yUnit=yUnit,
        font=font,
        size_label=size_label,
        color=color,
        x_label_gap_px=x_label_gap_px,
        y_label_gap_px=y_label_gap_px,
        y_label_top_gap_px=y_label_top_gap_px,
    )

    # Inline legend labels
    if legend is not None:
        if auto_legend_position:
            _auto_place_inline_labels(
                ax=ax,
                x_data=x,
                y_data=y,
                labels=legend,
                text_styles=text_styles,
            )
        else:
            for i in range(L):
                ax.text(
                    legx[i],
                    legy[i],
                    legend[i],
                    fontdict=text_styles[i],
                )

    # Save file
    if save:
        fig.savefig(f"{filename}.{extension}", bbox_inches='tight')

    return ax