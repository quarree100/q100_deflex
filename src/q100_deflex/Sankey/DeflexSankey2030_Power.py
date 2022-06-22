import os

import numpy as np
import pandas as pd

import deflex as dflx


def create_deflex_sankey(path, file):
    deflx = os.path.join(path, file)

    all_results = dflx.fetch_deflex_result_tables(deflx)

    # From Commodities to ...
    comm = all_results["commodity"]

    PP = np.sum(comm.xs("power plant", level=4, axis=1))  # All PP
    ComPPH2 = PP[0]
    ComPPbio = PP[1]
    ComPPcoal = PP[2]
    ComPPlignite = PP[3]
    ComPPgas = PP[4]
    ComPPother = PP[5]

    CHP = np.sum(comm.xs("chp plant", level=4, axis=1))  # All CHP
    ComCHPH2 = CHP[0]
    ComCHPbio = CHP[1]
    ComCHPcoal = CHP[2]
    ComCHPgas = CHP[3]
    ComCHPother = CHP[4]

    # Electricity
    elect = all_results["electricity"]
    mob = all_results[
        "mobility"
    ]  # because there is excess and shortage in mobility
    dh = all_results[
        "heat_district"
    ]  # because there is shortage in district heating

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
    Shortage3 = (
        np.sum(np.sum(dh.xs("shortage", level=0, axis=1))) / 1.88
    )  # /1.88 which is the cop of the HP (because here the shortage is in MWh_th!)
    ImportEbus = Shortage1 + Shortage2 + Shortage3

    PPEbus = np.sum(elect.xs("power plant", level=0, axis=1))
    PPH2Ebus = PPEbus[0]
    PPbioEbus = PPEbus[1]
    PPcoalEbus = PPEbus[2]
    PPligniteEbus = PPEbus[3]
    PPgasEbus = PPEbus[4]
    PPotherEbus = PPEbus[5]

    CHPEbus = np.sum(elect.xs("chp plant", level=0, axis=1))
    CHPH2Ebus = CHPEbus[0]
    CHPbioEbus = CHPEbus[1]
    CHPcoalEbus = CHPEbus[2]
    CHPgasEbus = CHPEbus[3]
    CHPotherEbus = CHPEbus[4]

    # From Electrcitiy bus
    EbustoStor = np.sum(np.sum(elect.xs("storage", level=4, axis=1)))
    EbusfromStor = np.sum(np.sum(elect.xs("storage", level=0, axis=1)))
    EbusStorLoss = EbustoStor - EbusfromStor

    EbusEldemand = np.sum(np.sum(elect.xs("elect final", level=6, axis=1)))
    EbusHPdec = np.sum(np.sum(elect.xs("heat pump", level=6, axis=1)))
    EbusHPDH = (
        np.sum(np.sum(elect.xs("heat pump DH", level=5, axis=1))) + Shortage3
    )  # because of shortage effect
    EbusMob = (
        np.sum(np.sum(elect.xs("fuel converter", level=4, axis=1)))
        - Unregulated2
        + Shortage2
    )  # because shortage+excess effect
    EbusElectrolyser = np.sum(
        np.sum(elect.xs("Electrolysis", level=5, axis=1))
    )

    # Heat Output CHP
    # dh sheet already open

    CHPDh = np.sum(dh.xs("chp plant", level=0, axis=1))
    CHPH2DH = CHPDh[0]
    CHPbioDH = CHPDh[1]
    CHPcoalDH = CHPDh[2]
    CHPgasDH = CHPDh[3]
    CHPotherDH = CHPDh[4]

    # Create df (From, To, value)

    d = (
        ["H2", "CHP H2", ComCHPH2],
        ["Others", "CHP others", ComCHPother],
        ["Bioenergy", "CHP bioenergy", ComCHPbio],
        ["Natural Gas", "CHP natural gas", ComCHPgas],
        ["Hard Coal", "CHP hard coal", ComCHPcoal],
        ["H2", "PP H2", ComPPH2],
        ["Others", "PP others", ComPPother],
        ["Bioenergy", "PP bioenergy", ComPPbio],
        ["Natural Gas", "PP natural gas", ComPPgas],
        ["Hard Coal", "PP hard coal", ComPPcoal],
        ["Lignite", "PP lignite", ComPPlignite],
        ["CHP H2", "DH Demand", CHPH2DH],
        ["CHP others", "DH Demand", CHPotherDH],
        ["CHP bioenergy", "DH Demand", CHPbioDH],
        ["CHP natural gas", "DH Demand", CHPgasDH],
        ["CHP hard coal", "DH Demand", CHPcoalDH],
        ["CHP H2", "El Bus", CHPH2Ebus],
        ["CHP others", "El Bus", CHPotherEbus],
        ["CHP bioenergy", "El Bus", CHPbioEbus],
        ["CHP natural gas", "El Bus", CHPgasEbus],
        ["CHP hard coal", "El Bus", CHPcoalEbus],
        ["PP H2", "El Bus", PPH2Ebus],
        ["PP others", "El Bus", PPotherEbus],
        ["PP bioenergy", "El Bus", PPbioEbus],
        ["PP natural gas", "El Bus", PPgasEbus],
        ["PP hard coal", "El Bus", PPcoalEbus],
        ["PP lignite", "El Bus", PPligniteEbus],
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
    
    return df
