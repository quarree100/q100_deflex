import os

import numpy as np
import pandas as pd

import deflex as dflx


def create_deflex_sankey(path, file, show_plot):
    deflx = os.path.join(path, file)

    all_results = dflx.fetch_deflex_result_tables(deflx)

    # From Commodities to ...
    comm = all_results["commodity"]

    FC = np.sum(
        comm.xs("fuel converter", level=4, axis=1)
    )  # All fuel converters
    ComoilMob = FC[0]

    # From Electricity bus
    elect = all_results["electricity"]

    EbusMob = np.sum(np.sum(elect.xs("fuel converter", level=4, axis=1)))

    # Create df (From, To, value)

    d = (
        ["From El Bus", "Mobility Demand", EbusMob],
        ["Oil", "Mobility Demand", ComoilMob],
    )

    df = pd.DataFrame(data=d, columns=["From", "To", "Value"])
    df.loc[:, "Value"] = round(df.loc[:, "Value"] / 1000000, 1)

    return df
