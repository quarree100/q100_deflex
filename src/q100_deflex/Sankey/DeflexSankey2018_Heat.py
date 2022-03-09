import os

import numpy as np
import pandas as pd

import deflex as dflx


def create_deflex_sankey(path, file, show_plot):
    deflx = os.path.join(path, file)

    all_results = dflx.fetch_deflex_result_tables(deflx)

    # From Commodities to ...
    comm = all_results["commodity"]

    CHP = np.sum(comm.xs("chp plant", level=4, axis=1))  # All CHP
    ComCHPbio = CHP[0]
    ComCHPcoal = CHP[1]
    ComCHPlignite = CHP[2]
    ComCHPgas = CHP[3]
    ComCHPother = CHP[4]

    HeatPlant = np.sum(
        comm.xs("heat plant", level=4, axis=1)
    )  # All heat plant
    ComHeatPlantbio = HeatPlant[0]
    ComHeatPlantcoal = HeatPlant[1]
    ComHeatPlantlignite = HeatPlant[2]
    ComHeatPlantgas = HeatPlant[3]
    ComHeatPlantother = HeatPlant[4]

    DecHeat = np.sum(
        comm.xs("decentralised heat", level=4, axis=1)
    )  # All decnetralized heat technologies
    ComDecHeatbio = DecHeat[0]
    ComDecHeatcoal = DecHeat[1]
    ComDecHeatlignite = DecHeat[2]
    ComDecHeatgas = DecHeat[3]
    ComDecHeatoil = DecHeat[4]
    ComDecHeatother = DecHeat[5]

    # Electricity
    elect = all_results["electricity"]

    # To Electricity bus
    CHPEbus = np.sum(elect.xs("chp plant", level=0, axis=1))
    CHPbioEbus = CHPEbus[0]
    CHPcoalEbus = CHPEbus[1]
    CHPligniteEbus = CHPEbus[2]
    CHPgasEbus = CHPEbus[3]
    CHPotherEbus = CHPEbus[4]

    # From Electrcitiy bus
    EbusHPdec = np.sum(np.sum(elect.xs("heat pump", level=6, axis=1)))

    # District heating
    dh = all_results["heat_district"]

    CHPDh = np.sum(dh.xs("chp plant", level=0, axis=1))
    CHPbioDH = CHPDh[0]
    CHPcoalDH = CHPDh[1]
    CHPligniteDH = CHPDh[2]
    CHPgasDH = CHPDh[3]
    CHPotherDH = CHPDh[4]

    HeatPl = np.sum(dh.xs("heat plant", level=0, axis=1))
    HeatPlantbioDH = HeatPl[0]
    HeatPlantcoalDH = HeatPl[1]
    HeatPlantligniteDH = HeatPl[2]
    HeatPlantgasDH = HeatPl[3]
    HeatPlantotherDH = HeatPl[4]

    # Decentralised Heat
    decentralisedheat = all_results["heat_decentralised"]

    decheat = np.sum(
        decentralisedheat.xs("decentralised heat", level=0, axis=1)
    )
    DecHeatbioDecHeatdemand = decheat[0]
    DecHeatcoalDecHeatdemand = decheat[1]
    DecHeatheatpumpDecHeatdemand = decheat[2]
    DecHeatligniteDecHeatdemand = decheat[3]
    DecHeatgasDecHeatdemand = decheat[4]
    DecHeatoilDecHeatdemand = decheat[5]
    DecHeatotherDecHeatdemand = decheat[6]

    # Create df (From, To, value)

    d = (
        ["From El Bus", "Heat Pump decentralised", EbusHPdec],
        [
            "Heat Pump decentralised",
            "Dec. Heat Demand",
            DecHeatheatpumpDecHeatdemand,
        ],
        ["Others", "Dec. Heat others", ComDecHeatother],
        ["Bioenergy", "Dec. Heat bioenergy", ComDecHeatbio],
        ["Natural Gas", "Dec. Heat natural gas", ComDecHeatgas],
        ["Oil", "Dec. Heat oil", ComDecHeatoil],
        ["Lignite", "Dec. Heat lignite", ComDecHeatlignite],
        ["Hard Coal", "Dec. Heat hard coal", ComDecHeatcoal],
        ["Others", "Heat Plant others", ComHeatPlantother],
        ["Bioenergy", "Heat Plant bioenergy", ComHeatPlantbio],
        ["Natural Gas", "Heat Plant natural gas", ComHeatPlantgas],
        ["Lignite", "Heat Plant lignite", ComHeatPlantlignite],
        ["Hard Coal", "Heat Plant hard coal", ComHeatPlantcoal],
        ["Others", "CHP others", ComCHPother],
        ["Bioenergy", "CHP bioenergy", ComCHPbio],
        ["Natural Gas", "CHP natural gas", ComCHPgas],
        ["Lignite", "CHP lignite", ComCHPlignite],
        ["Hard Coal", "CHP hard coal", ComCHPcoal],
        ["Dec. Heat others", "Dec. Heat Demand", DecHeatotherDecHeatdemand],
        ["Dec. Heat bioenergy", "Dec. Heat Demand", DecHeatbioDecHeatdemand],
        ["Dec. Heat natural gas", "Dec. Heat Demand", DecHeatgasDecHeatdemand],
        ["Dec. Heat oil", "Dec. Heat Demand", DecHeatoilDecHeatdemand],
        ["Dec. Heat lignite", "Dec. Heat Demand", DecHeatligniteDecHeatdemand],
        ["Dec. Heat hard coal", "Dec. Heat Demand", DecHeatcoalDecHeatdemand],
        ["Heat Plant others", "DH Demand", HeatPlantotherDH],
        ["Heat Plant bioenergy", "DH Demand", HeatPlantbioDH],
        ["Heat Plant natural gas", "DH Demand", HeatPlantgasDH],
        ["Heat Plant lignite", "DH Demand", HeatPlantligniteDH],
        ["Heat Plant hard coal", "DH Demand", HeatPlantcoalDH],
        ["CHP others", "DH Demand", CHPotherDH],
        ["CHP bioenergy", "DH Demand", CHPbioDH],
        ["CHP natural gas", "DH Demand", CHPgasDH],
        ["CHP lignite", "DH Demand", CHPligniteDH],
        ["CHP hard coal", "DH Demand", CHPcoalDH],
        ["CHP others", "To El Bus", CHPotherEbus],
        ["CHP bioenergy", "To El Bus", CHPbioEbus],
        ["CHP natural gas", "To El Bus", CHPgasEbus],
        ["CHP lignite", "To El Bus", CHPligniteEbus],
        ["CHP hard coal", "To El Bus", CHPcoalEbus],
    )

    df = pd.DataFrame(data=d, columns=["From", "To", "Value"])
    df.loc[:, "Value"] = round(df.loc[:, "Value"] / 1000000, 1)

    return df
