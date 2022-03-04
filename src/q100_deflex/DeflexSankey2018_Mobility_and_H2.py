import os

import numpy as np
import pandas as pd

import deflex as dflx
from holoviews_sankey import create_and_save_sankey

path = "/home/uwe/deflex/quarree100/results_cbc/"
dump = "2018-DE02-Agora.dflx"
deflx = os.path.join(path, dump)

all_results = dflx.fetch_deflex_result_tables(deflx)

# From Commodities to ...
comm = all_results["commodity"]

FC = np.sum(comm.xs("fuel converter", level=4, axis=1))  # All fuel converters
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
print(df)

a = create_and_save_sankey(
    df,
    filename=os.path.join(path, "Sankey Deflex - 2018 Mobility Sector"),
    title="Mobility Sector - 2018",
    edge_color_index="To",
    fontsize=20,
    label_text_font_size="12pt",
    node_width=45,
)
