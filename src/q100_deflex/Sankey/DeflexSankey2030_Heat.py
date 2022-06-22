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
    ComCHPcoal = CHP[2]
    ComCHPgas = CHP[3]
    ComCHPother = CHP[4]

    HeatPlant = np.sum(
        comm.xs("heat plant", level=4, axis=1)
    )  # All heat plant
    ComHeatPlantbio = HeatPlant[0]
    ComHeatPlantcoal = HeatPlant[1]
    ComHeatPlantgas = HeatPlant[2]
    ComHeatPlantother = HeatPlant[3]

    DecHeat = np.sum(
        comm.xs("decentralised heat", level=4, axis=1)
    )  # All decnetralized heat technologies
    ComDecHeatbio = DecHeat[0]
    ComDecHeatcoal = DecHeat[1]
    ComDecHeatgas = DecHeat[2]
    ComDecHeatoil = DecHeat[3]
    ComDecHeatother = DecHeat[4]

    # Electricity
    elect = all_results["electricity"]
    dh = all_results["heat_district"]  # there is shortage in DH

    ShortageHPDHheat = np.sum(
        np.sum(dh.xs("shortage", level=0, axis=1))
    )  # this is the shortage in MW_th
    ShortageHPDHelectr = (
        ShortageHPDHheat / 1.88
    )  # this is the shortage in MW_el

    # To Electricity bus
    CHPEbus = np.sum(elect.xs("chp plant", level=0, axis=1))
    CHPH2Ebus = CHPEbus[0]
    CHPbioEbus = CHPEbus[1]
    CHPcoalEbus = CHPEbus[2]
    CHPgasEbus = CHPEbus[3]
    CHPotherEbus = CHPEbus[4]

    # From Electrcitiy bus
    EbusHPdec = np.sum(np.sum(elect.xs("heat pump", level=6, axis=1)))
    EbusHPDH = (
        np.sum(np.sum(elect.xs("heat pump DH", level=5, axis=1)))
        + ShortageHPDHelectr
    )

    # District heating, dh sheet already open

    CHPDh = np.sum(dh.xs("chp plant", level=0, axis=1))
    CHPH2DH = CHPDh[0]
    CHPbioDH = CHPDh[1]
    CHPcoalDH = CHPDh[2]
    CHPgasDH = CHPDh[3]
    CHPotherDH = CHPDh[4]

    HeatPl = np.sum(dh.xs("heat plant", level=0, axis=1))
    HeatPlantbioDH = HeatPl[0]
    HeatPlantcoalDH = HeatPl[1]
    HeatPlantHPDH = HeatPl[2] + ShortageHPDHheat
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
    DecHeatgasDecHeatdemand = decheat[3]
    DecHeatoilDecHeatdemand = decheat[4]
    DecHeatotherDecHeatdemand = decheat[5]

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
        ["Hard Coal", "Dec. Heat hard coal", ComDecHeatcoal],
        ["Others", "Heat Plant others", ComHeatPlantother],
        ["Bioenergy", "Heat Plant bioenergy", ComHeatPlantbio],
        ["Natural Gas", "Heat Plant natural gas", ComHeatPlantgas],
        ["Hard Coal", "Heat Plant hard coal", ComHeatPlantcoal],
        ["Others", "CHP others", ComCHPother],
        ["Bioenergy", "CHP bioenergy", ComCHPbio],
        ["Natural Gas", "CHP natural gas", ComCHPgas],
        ["Hard Coal", "CHP hard coal", ComCHPcoal],
        ["H2", "CHP H2", ComCHPH2],
        ["Dec. Heat others", "Dec. Heat Demand", DecHeatotherDecHeatdemand],
        ["Dec. Heat bioenergy", "Dec. Heat Demand", DecHeatbioDecHeatdemand],
        ["Dec. Heat natural gas", "Dec. Heat Demand", DecHeatgasDecHeatdemand],
        ["Dec. Heat oil", "Dec. Heat Demand", DecHeatoilDecHeatdemand],
        ["Dec. Heat hard coal", "Dec. Heat Demand", DecHeatcoalDecHeatdemand],
        ["From El Bus", "Heat Pump DH", EbusHPDH],
        ["Heat Pump DH", "DH Demand", HeatPlantHPDH],
        ["Heat Plant others", "DH Demand", HeatPlantotherDH],
        ["Heat Plant bioenergy", "DH Demand", HeatPlantbioDH],
        ["Heat Plant natural gas", "DH Demand", HeatPlantgasDH],
        ["Heat Plant hard coal", "DH Demand", HeatPlantcoalDH],
        ["CHP others", "DH Demand", CHPotherDH],
        ["CHP bioenergy", "DH Demand", CHPbioDH],
        ["CHP natural gas", "DH Demand", CHPgasDH],
        ["CHP hard coal", "DH Demand", CHPcoalDH],
        ["CHP H2", "DH Demand", CHPH2DH],
        ["CHP others", "To El Bus", CHPotherEbus],
        ["CHP bioenergy", "To El Bus", CHPbioEbus],
        ["CHP natural gas", "To El Bus", CHPgasEbus],
        ["CHP hard coal", "To El Bus", CHPcoalEbus],
        ["CHP H2", "To El Bus", CHPH2Ebus],
    )

    df = pd.DataFrame(data=d, columns=["From", "To", "Value"])
    df.loc[:, "Value"] = round(df.loc[:, "Value"] / 1000000, 1)
    
    return df
