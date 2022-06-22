import os

import numpy as np
import pandas as pd


import deflex as dflx


def create_deflex_sankey(path, file):
    deflx = os.path.join(path, file)

    all_results = dflx.fetch_deflex_result_tables(deflx)

    # From Commodities to ...
    comm = all_results["commodity"]

    CHP = np.sum(comm.xs("chp plant", level=4, axis=1))  # All CHP
    ComCHPH2 = CHP[0]
    ComCHPbio = CHP[1]
    ComCHPother = CHP[2]

    HeatPlant = np.sum(
        comm.xs("heat plant", level=4, axis=1)
    )  # All heat plant
    ComHeatPlantbio = HeatPlant[0]
    ComHeatPlantother = HeatPlant[1]

    DecHeat = np.sum(
        comm.xs("decentralised heat", level=4, axis=1)
    )  # All decnetralized heat technologies
    ComDecHeatbio = DecHeat[0]
    ComDecHeatoil = DecHeat[1]
    ComDecHeatother = DecHeat[2]

    # Electricity
    elect = all_results["electricity"]

    # To Electricity bus
    CHPEbus = np.sum(elect.xs("chp plant", level=0, axis=1))
    CHPH2Ebus = CHPEbus[0]
    CHPbioEbus = CHPEbus[1]
    CHPotherEbus = CHPEbus[2]

    # From Electrcitiy bus
    EbusHPdec = np.sum(np.sum(elect.xs("heat pump", level=6, axis=1)))
    EbusHPDH = np.sum(np.sum(elect.xs("heat pump DH", level=5, axis=1)))

    # District heating
    dh = all_results["heat_district"]

    CHPDh = np.sum(dh.xs("chp plant", level=0, axis=1))
    CHPH2DH = CHPDh[0]
    CHPbioDH = CHPDh[1]
    CHPotherDH = CHPDh[2]

    HeatPl = np.sum(dh.xs("heat plant", level=0, axis=1))
    HeatPlantbioDH = HeatPl[0]
    HeatPlantHPDH = HeatPl[1]
    HeatPlantotherDH = HeatPl[2]

    # Decentralised Heat
    decentralisedheat = all_results["heat_decentralised"]

    decheat = np.sum(
        decentralisedheat.xs("decentralised heat", level=0, axis=1)
    )
    DecHeatbioDecHeatdemand = decheat[0]
    DecHeatheatpumpDecHeatdemand = decheat[1]
    DecHeatoilDecHeatdemand = decheat[2]
    DecHeatotherDecHeatdemand = decheat[3]

    # Create df (From, To, value)

    d = (
        ["Oil", "Dec. Heat oil", ComDecHeatoil],
        ["Dec. Heat oil", "Dec. Heat Demand", DecHeatoilDecHeatdemand],
        ["From El Bus", "Heat Pump decentralised", EbusHPdec],
        [
            "Heat Pump decentralised",
            "Dec. Heat Demand",
            DecHeatheatpumpDecHeatdemand,
        ],
        ["Others", "Dec. Heat others", ComDecHeatother],
        ["Bioenergy", "Dec. Heat bioenergy", ComDecHeatbio],
        ["Others", "Heat Plant others", ComHeatPlantother],
        ["Bioenergy", "Heat Plant bioenergy", ComHeatPlantbio],
        ["Others", "CHP others", ComCHPother],
        ["Bioenergy", "CHP bioenergy", ComCHPbio],
        ["H2", "CHP H2", ComCHPH2],
        ["Dec. Heat others", "Dec. Heat Demand", DecHeatotherDecHeatdemand],
        ["Dec. Heat bioenergy", "Dec. Heat Demand", DecHeatbioDecHeatdemand],
        ["From El Bus", "Heat Pump DH", EbusHPDH],
        ["Heat Pump DH", "DH Demand", HeatPlantHPDH],
        ["Heat Plant others", "DH Demand", HeatPlantotherDH],
        ["Heat Plant bioenergy", "DH Demand", HeatPlantbioDH],
        ["CHP others", "DH Demand", CHPotherDH],
        ["CHP bioenergy", "DH Demand", CHPbioDH],
        ["CHP H2", "DH Demand", CHPH2DH],
        ["CHP others", "To El Bus", CHPotherEbus],
        ["CHP bioenergy", "To El Bus", CHPbioEbus],
        ["CHP H2", "To El Bus", CHPH2Ebus],
    )

    df = pd.DataFrame(data=d, columns=["From", "To", "Value"])
    df.loc[:, "Value"] = round(df.loc[:, "Value"] / 1000000, 1)
    
    return df
