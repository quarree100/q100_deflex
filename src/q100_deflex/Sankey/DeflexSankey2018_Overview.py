import os

import numpy as np
import pandas as pd

import deflex as dflx


def create_deflex_sankey(path, file):
    deflx = os.path.join(path, file)

    all_results = dflx.fetch_deflex_result_tables(deflx)

    # From Commodities to ...
    comm = all_results["commodity"]

    ComPP = np.sum(np.sum(comm.xs("power plant", level=4, axis=1)))
    ComCHP = np.sum(np.sum(comm.xs("chp plant", level=4, axis=1)))
    ComHPl = np.sum(np.sum(comm.xs("heat plant", level=4, axis=1)))
    ComDec = np.sum(np.sum(comm.xs("decentralised heat", level=4, axis=1)))
    ComMob = np.sum(np.sum(comm.xs("fuel converter", level=4, axis=1)))

    # Electricity
    elect = all_results["electricity"]

    # To Electricity bus
    VolEbus = np.sum(np.sum(elect.xs("volatile", level=1, axis=1)))
    PPEbus = np.sum(np.sum(elect.xs("power plant", level=0, axis=1)))
    CHPEbus = np.sum(np.sum(elect.xs("chp plant", level=0, axis=1)))

    # From Electrcitiy bus
    EbusExport = np.sum(np.sum(elect.xs("export", level=6, axis=1)))
    EbusEldemand = np.sum(np.sum(elect.xs("elect final", level=6, axis=1)))
    EbusHPdec = np.sum(np.sum(elect.xs("heat pump", level=6, axis=1)))
    EbusMob = np.sum(np.sum(elect.xs("fuel converter", level=4, axis=1)))

    # District heating
    dh = all_results["heat_district"]

    CHPDh = np.sum(np.sum(dh.xs("chp plant", level=0, axis=1)))
    HPlDh = np.sum(np.sum(dh.xs("heat plant", level=0, axis=1)))

    # Decentralized heat
    decheat = all_results["heat_decentralised"]

    DecDecheat = np.sum(np.sum(decheat.xs("DE", level=3, axis=1))) / 2
    HPdecDecheat = np.sum(np.sum(decheat.xs("DE01", level=3, axis=1))) / 2

    # Create df (From, To, value)

    d = (
        ["Commodities", "Dec. Heat", ComDec],
        ["Commodities", "Heat Plant", ComHPl],
        ["Commodities", "CHP", ComCHP],
        ["Commodities", "PP", ComPP],
        ["Commodities", "Mobility Demand", ComMob],
        ["Dec. Heat", "Dec. Heat Demand", DecDecheat],
        ["Heat Plant", "DH Demand", HPlDh],
        ["CHP", "El Bus", CHPEbus],
        ["CHP", "DH Demand", CHPDh],
        ["PP", "El Bus", PPEbus],
        ["Volatiles", "El Bus", VolEbus],
        ["El Bus", "Electricity Demand", EbusEldemand],
        ["El Bus", "Elect Export", EbusExport],
        ["El Bus", "HP Decentralised", EbusHPdec],
        ["El Bus", "Mobility Demand", EbusMob],
        ["HP Decentralised", "Dec. Heat Demand", HPdecDecheat],
    )

    df = pd.DataFrame(data=d, columns=["From", "To", "Value"])
    df.loc[:, "Value"] = round(df.loc[:, "Value"] / 1000000, 1)
    
    return df
