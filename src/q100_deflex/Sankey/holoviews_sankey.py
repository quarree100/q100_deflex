# -*- coding: utf-8 -*-

"""Plot a Sankey chart from a spreadsheet in the `xlsx` format.

Create a ``Sankey`` plot as png, svg and html with data from an `xlsx` file.

For more info on creating Sankeys with HoloViews, see
http://holoviews.org/reference/elements/bokeh/Sankey.html

SPDX-FileCopyrightText: 2022 Joris Zimmermann (original code)
SPDX-FileCopyrightText: 2022 Uwe Krien <krien@uni-bremen.de> (adaptions)

SPDX-License-Identifier: MIT
"""

import os

from holoviews import Sankey, extension
from holoviews.plotting import bokeh
import pandas as pd
from bokeh.io import export_png, export_svgs, output_file, show, webdriver
from bokeh.layouts import gridplot


def main(filename, **kwargs):
    """
    Create a sankey plot from every sheet of a given xlsx file.

    Parameters
    ----------
    filename : str
        Full path to the input spreadsheet file (xlsx format).
    """
    df_dict = pd.read_excel(
        filename, header=0, sheet_name=None, index_col=[0]
    )

    sankey_list = []

    # Create sankey for each sheet in the workbook
    for sheet_name, df in df_dict.items():

        # Use same name as input file, plus sheet_name
        plot_file = os.path.splitext(filename)[0] + " " + str(sheet_name)

        # Create the plot figure from DataFrame
        bkplot = create_and_save_sankey(
            df, plot_file, sheet_name, sheet_name, **kwargs
        )
        sankey_list += [bkplot]  # Add result to list of sankeys

    # Create html output
    output_file(
        os.path.splitext(filename)[0] + ".html",
        title=os.path.splitext(filename)[0],
    )
    show(gridplot(sankey_list, ncols=1, sizing_mode="stretch_width"))


def create_and_save_sankey(
    edges,
    filename=None,
    title="",
    title_html="",
    edge_color_index="To",
    show_plot=False,
    fontsize=11,
    label_text_font_size="17pt",
    node_width=45,
    export_title=True,
):
    """
    Use HoloViews to create a Sankey plot from the input data.

    Parameters
    ----------
    edges : pandas.DataFrame
        Table with the columns 'From', 'To' and 'Value'. Names are arbitrary,
        but must match ``edge_color_index``.
    filename : str
        Filename (without extension) of exported png and svg. (default: None)
    title : str
        Diagram title. (default: empty string)
    title_html : str
        Diagram title for html output. (default: empty string)
    edge_color_index : str
        Name of column to use for edge color. With 'To', all edges arriving at
        a node have the same color. (default: 'To')
    show_plot : bool
        Whether to show the plot or not. (default: False)
    fontsize : numeric
        Size of the fonts. (default: 11)
    label_text_font_size : str
        Size of the label fonts. (default: "17pt")
    node_width : numeric
        Width of the nodes. (default: 45)
    export_title : bool


    Returns
    -------
    bkplot (object): The Bokeh plot object.

    """
    try:
        # If export_png or export_svgs are called repeatedly, by default
        # a new webdriver is created each time. For me, on Windows, those
        # webdrivers survive the script and the processes keep running
        # in task manager.
        # A solution is to manually define a webdriver that we can actually
        # close automatically:
        web_driver = webdriver.create_firefox_webdriver()
    except Exception as e:
        print(e)
        web_driver = None

    extension("bokeh")  # Some HoloViews magic to make it work with Bokeh

    palette = [
        "#f14124",
        "#ff8021",
        "#e8d654",
        "#5eccf3",
        "#b4dcfa",
        "#4e67c8",
        "#56c7aa",
        "#24f198",
        "#2160ff",
        "#c354e8",
        "#e73384",
        "#c76b56",
        "#facdb4",
    ]

    # Only keep non-zero rows (flow with zero width cannot be plotted)
    edges = edges.loc[(edges != 0).all(axis=1)]

    # Use HoloViews to create the plot
    hv_sankey = Sankey(edges).options(
        width=1800,
        height=800,
        node_sort=False,
        label_position="outer",
        edge_color_index=edge_color_index,
        cmap=palette,
        edge_cmap=palette,
        node_width=node_width,  # default 15
        fontsize=fontsize,
        label_text_font_size=label_text_font_size,
        node_padding=20,  # default 10
    )

    # HoloViews is mainly used for creating html content. Getting the simple
    # PNG is a little more involved
    hvplot = bokeh.BokehRenderer.get_plot(hv_sankey)
    bkplot = hvplot.state
    bkplot.toolbar_location = None  # disable Bokeh toolbar
    if export_title is True:  # Add the title to the file export
        bkplot.title.text = str(title)

    if filename is not None:
        # Create the output folder, if it does not already exist
        if not os.path.exists(os.path.abspath(os.path.dirname(filename))):
            os.makedirs(os.path.abspath(os.path.dirname(filename)))

        export_png(bkplot, filename=filename + ".png", webdriver=web_driver)
        bkplot.output_backend = "svg"
        export_svgs(bkplot, filename=filename + ".svg", webdriver=web_driver)

    if web_driver is not None:
        web_driver.quit()  # Quit webdriver after finishing using it

    # For html output
    bkplot.title.text = str(title)
    bkplot.sizing_mode = "stretch_width"

    if filename is not None:
        if title_html == "":
            title_html = title
        # Create html output
        output_file(filename + ".html", title=title_html)

    if show_plot:
        show(bkplot)

    return bkplot


if __name__ == "__main__":
    pass
