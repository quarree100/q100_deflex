import os
import numpy as np
import pandas as pd
from holoviews_sankey import create_and_save_sankey

import deflex as dflx

path = "/home/uwe/deflex/quarree100/results_cbc/"
dump = "2050-DE02-Agora.dflx"
deflx = os.path.join(path, dump)

all_results = dflx.fetch_deflex_result_tables(deflx)


# From Commodities to ...
comm = all_results["commodity"]

PP = np.sum(comm.xs("power plant", level=4, axis=1))  # All PP
ComPPH2 = PP[0]

CHP = np.sum(comm.xs("chp plant", level=4, axis=1))  # All CHP
ComCHPH2 = CHP[0]
ComCHPbio = CHP[1]
ComCHPother = CHP[2]

# Electricity
elect = all_results["electricity"]
mob = all_results[
    "mobility"
]  # because there is excess and shortage in mobility

# To Electricity bus
Vol = np.sum(elect.xs("volatile", level=1, axis=1))
HydroVol = Vol[0]
PVVol = Vol[1]
WoffVol = Vol[2]
WonVol = Vol[3]

Unregulated1 = np.sum(np.sum(elect.xs("excess", level=4, axis=1)))
Unregulated2 = np.sum(
    np.sum(mob.xs("excess", level=4, axis=1))
)  # excess in mobility
VolUnregulated = Unregulated1 + Unregulated2
VolEbus = HydroVol + PVVol + WoffVol + WonVol - VolUnregulated

Shortage1 = np.sum(
    np.sum(elect.xs("shortage", level=0, axis=1))
)  # shortage in electricitiy
Shortage2 = np.sum(
    np.sum(mob.xs("shortage", level=0, axis=1))
)  # shortage in mobility
ImportEbus = Shortage1 + Shortage2

PPEbus = np.sum(elect.xs("power plant", level=0, axis=1))
PPH2Ebus = PPEbus[0]

CHPEbus = np.sum(elect.xs("chp plant", level=0, axis=1))
CHPH2Ebus = CHPEbus[0]
CHPbioEbus = CHPEbus[1]
CHPotherEbus = CHPEbus[2]


# From Electrcitiy bus
EbustoStor = np.sum(np.sum(elect.xs("storage", level=4, axis=1)))
EbusfromStor = np.sum(np.sum(elect.xs("storage", level=0, axis=1)))
EbusStorLoss = EbustoStor - EbusfromStor

EbusEldemand = np.sum(np.sum(elect.xs("elect final", level=6, axis=1)))
EbusHPdec = np.sum(np.sum(elect.xs("heat pump", level=6, axis=1)))
EbusHPDH = np.sum(np.sum(elect.xs("heat pump DH", level=5, axis=1)))
EbusMob = (
    np.sum(np.sum(elect.xs("fuel converter", level=4, axis=1)))
    - Unregulated2
    + Shortage2
)  # because shortage+excess effect
EbusElectrolyser = np.sum(np.sum(elect.xs("Electrolysis", level=5, axis=1)))


# Heat Output CHP
dh = all_results["heat_district"]

CHPDh = np.sum(dh.xs("chp plant", level=0, axis=1))
CHPH2DH = CHPDh[0]
CHPbioDH = CHPDh[1]
CHPotherDH = CHPDh[2]


# Create df (From, To, value)

d = (
    ["Others", "CHP others", ComCHPother],
    ["Bioenergy", "CHP bioenergy", ComCHPbio],
    ["H2", "CHP H2", ComCHPH2],
    ["H2", "PP H2", ComPPH2],
    ["CHP others", "DH Demand", CHPotherDH],
    ["CHP bioenergy", "DH Demand", CHPbioDH],
    ["CHP H2", "DH Demand", CHPH2DH],
    ["CHP others", "El Bus", CHPotherEbus],
    ["CHP bioenergy", "El Bus", CHPbioEbus],
    ["CHP H2", "El Bus", CHPH2Ebus],
    ["PP H2", "El Bus", PPH2Ebus],
    ["Hydro", "Volatiles", HydroVol],
    ["Wind Offshore", "Volatiles", WoffVol],
    ["Wind Onshore", "Volatiles", WonVol],
    ["PV", "Volatiles", PVVol],
    ["EL Import", "El Bus", ImportEbus],
    ["Volatiles", "El Bus", VolEbus],
    ["El Bus", "HP District Heating", EbusHPDH],
    ["El Bus", "Mobility Demand", EbusMob],
    ["El Bus", "HP Decentralised", EbusHPdec],
    ["El Bus", "Electricity Demand", EbusEldemand],
    ["El Bus", "Electrolyser", EbusElectrolyser],
    ["El Bus", "El Storage losses", EbusStorLoss],
    ["Volatiles", "Unregulated", VolUnregulated],
)

df = pd.DataFrame(data=d, columns=["From", "To", "Value"])
df.loc[:, "Value"] = round(df.loc[:, "Value"] / 1000000, 1)
print(df)

a = create_and_save_sankey(
    df,
    filename=os.path.join(path, "Sankey Deflex - 2050 Power Sector"),
    title="Power Sector - 2050",
    edge_color_index="To",
    fontsize=20,
    label_text_font_size="12pt",
    node_width=45,
)
