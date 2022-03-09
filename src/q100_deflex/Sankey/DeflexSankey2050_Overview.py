import os

import numpy as np
import pandas as pd

import deflex as dflx


def create_deflex_sankey(path, file, show_plot):
    deflx = os.path.join(path, file)

    all_results = dflx.fetch_deflex_result_tables(deflx)

    # From Commodities to ...
    comm = all_results["commodity"]

    ComPP = np.sum(np.sum(comm.xs("power plant", level=4, axis=1)))
    ComCHP = np.sum(np.sum(comm.xs("chp plant", level=4, axis=1)))
    ComHPl = np.sum(np.sum(comm.xs("heat plant", level=4, axis=1)))
    ComDec = np.sum(np.sum(comm.xs("decentralised heat", level=4, axis=1)))
    ComMob = np.sum(np.sum(comm.xs("fuel converter", level=4, axis=1)))
    ComOther = np.sum(np.sum(comm.xs("other demand", level=4, axis=1)))

    # Electricity
    elect = all_results["electricity"]
    mob = all_results[
        "mobility"
    ]  # because there is excess and shortage in mobility

    # To Electricity bus
    Unregulated1 = np.sum(np.sum(elect.xs("excess", level=4, axis=1)))
    Unregulated2 = np.sum(
        np.sum(mob.xs("excess", level=4, axis=1))
    )  # excess in mobility
    Unregulated = Unregulated1 + Unregulated2

    Shortage1 = np.sum(
        np.sum(elect.xs("shortage", level=0, axis=1))
    )  # shortage in electricitiy
    Shortage2 = np.sum(
        np.sum(mob.xs("shortage", level=0, axis=1))
    )  # shortage in mobility
    ImportEbus = Shortage1 + Shortage2

    VolEbus = (
        np.sum(np.sum(elect.xs("volatile", level=1, axis=1))) - Unregulated
    )
    PPEbus = np.sum(np.sum(elect.xs("power plant", level=0, axis=1)))
    CHPEbus = np.sum(np.sum(elect.xs("chp plant", level=0, axis=1)))

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
    EbusElectrolyser = np.sum(
        np.sum(elect.xs("Electrolysis", level=5, axis=1))
    )

    # District heating
    dh = all_results["heat_district"]

    HPDHDh = np.sum(np.sum(dh.xs("heat pump DH", level=1, axis=1)))
    CHPDh = np.sum(np.sum(dh.xs("chp plant", level=0, axis=1)))
    HPlDh = np.sum(np.sum(dh.xs("heat plant", level=0, axis=1))) - HPDHDh

    # Decentralized heat
    decheat = all_results["heat_decentralised"]

    DecDecheat = np.sum(np.sum(decheat.xs("DE", level=3, axis=1))) / 2
    HPdecDecheat = np.sum(np.sum(decheat.xs("DE01", level=3, axis=1))) / 2

    # Electrolysis to H2
    ElectrolyserH2 = np.sum(np.sum(comm.xs("Electrolysis", level=1, axis=1)))

    # Create df (From, To, value)

    d = (
        ["Commodities", "Dec. Heat", ComDec],
        ["Commodities", "Heat Plant", ComHPl],
        ["Commodities", "CHP", ComCHP],
        ["Commodities", "PP", ComPP],
        ["Commodities", "H2/SynFuel Industry Demand", ComOther],
        ["Commodities", "Mobility Demand", ComMob],
        ["Dec. Heat", "Dec. Heat Demand", DecDecheat],
        ["Heat Plant", "DH Demand", HPlDh],
        ["CHP", "El Bus", CHPEbus],
        ["PP", "El Bus", PPEbus],
        ["Volatiles", "El Bus", VolEbus],
        ["EL Import", "El Bus", ImportEbus],
        ["CHP", "DH Demand", CHPDh],
        ["El Bus", "Electricity Demand", EbusEldemand],
        ["El Bus", "HP Decentralised", EbusHPdec],
        ["El Bus", "HP District heating", EbusHPDH],
        ["El Bus", "Mobility Demand", EbusMob],
        ["El Bus", "Electrolyser", EbusElectrolyser],
        ["HP Decentralised", "Dec. Heat Demand", HPdecDecheat],
        ["HP District heating", "DH Demand", HPDHDh],
        ["Electrolyser", "H2 Production", ElectrolyserH2],
        ["El Bus", "El Stor losses", EbusStorLoss],
        ["Volatiles", "Unregulated", Unregulated],
    )

    df = pd.DataFrame(data=d, columns=["From", "To", "Value"])
    df.loc[:, "Value"] = round(df.loc[:, "Value"] / 1000000, 1)
    
    return df
