import os

import numpy as np
import pandas as pd

import deflex as dflx


def create_deflex_sankey(path, file, show_plot):
    deflx = os.path.join(path, file)

    all_results = dflx.fetch_deflex_result_tables(deflx)

    # From Commodities to ...
    comm = all_results["commodity"]

    PP = np.sum(comm.xs("power plant", level=4, axis=1))  # All PP
    ComPPbio = PP[0]
    ComPPcoal = PP[1]
    ComPPlignite = PP[2]
    ComPPgas = PP[3]
    ComPPnuclear = PP[4]
    ComPPother = PP[5]

    CHP = np.sum(comm.xs("chp plant", level=4, axis=1))  # All CHP
    ComCHPbio = CHP[0]
    ComCHPcoal = CHP[1]
    ComCHPlignite = CHP[2]
    ComCHPgas = CHP[3]
    ComCHPother = CHP[4]

    # Electricity
    elect = all_results["electricity"]

    # To Electricity bus
    Vol = np.sum(elect.xs("volatile", level=1, axis=1))
    HydroVol = Vol[0]
    PVVol = Vol[1]
    WoffVol = Vol[2]
    WonVol = Vol[3]
    VolEbus = HydroVol + PVVol + WoffVol + WonVol

    PPEbus = np.sum(elect.xs("power plant", level=0, axis=1))
    PPbioEbus = PPEbus[0]
    PPcoalEbus = PPEbus[1]
    PPligniteEbus = PPEbus[2]
    PPgasEbus = PPEbus[3]
    PPnuclearEbus = PPEbus[4]
    PPotherEbus = PPEbus[5]

    CHPEbus = np.sum(elect.xs("chp plant", level=0, axis=1))
    CHPbioEbus = CHPEbus[0]
    CHPcoalEbus = CHPEbus[1]
    CHPligniteEbus = CHPEbus[2]
    CHPgasEbus = CHPEbus[3]
    CHPotherEbus = CHPEbus[4]

    # From Electrcitiy bus
    EbusExport = np.sum(np.sum(elect.xs("export", level=6, axis=1)))
    EbusEldemand = np.sum(np.sum(elect.xs("elect final", level=6, axis=1)))
    EbusHPdec = np.sum(np.sum(elect.xs("heat pump", level=6, axis=1)))
    EbusMob = np.sum(np.sum(elect.xs("fuel converter", level=4, axis=1)))

    # Heat Output CHP
    dh = all_results["heat_district"]

    CHPDh = np.sum(dh.xs("chp plant", level=0, axis=1))
    CHPbioDH = CHPDh[0]
    CHPcoalDH = CHPDh[1]
    CHPligniteDH = CHPDh[2]
    CHPgasDH = CHPDh[3]
    CHPotherDH = CHPDh[4]

    # Create df (From, To, value)

    d = (
        ["Others", "CHP others", ComCHPother],
        ["Bioenergy", "CHP bioenergy", ComCHPbio],
        ["Natural Gas", "CHP natural gas", ComCHPgas],
        ["Lignite", "CHP lignite", ComCHPlignite],
        ["Hard Coal", "CHP hard coal", ComCHPcoal],
        ["Others", "PP others", ComPPother],
        ["Bioenergy", "PP bioenergy", ComPPbio],
        ["Natural Gas", "PP natural gas", ComPPgas],
        ["Lignite", "PP lignite", ComPPlignite],
        ["Hard Coal", "PP hard coal", ComPPcoal],
        ["Nuclear", "PP nuclear", ComPPnuclear],
        ["CHP others", "DH Demand", CHPotherDH],
        ["CHP bioenergy", "DH Demand", CHPbioDH],
        ["CHP natural gas", "DH Demand", CHPgasDH],
        ["CHP lignite", "DH Demand", CHPligniteDH],
        ["CHP hard coal", "DH Demand", CHPcoalDH],
        ["CHP others", "El Bus", CHPotherEbus],
        ["CHP bioenergy", "El Bus", CHPbioEbus],
        ["CHP natural gas", "El Bus", CHPgasEbus],
        ["CHP lignite", "El Bus", CHPligniteEbus],
        ["CHP hard coal", "El Bus", CHPcoalEbus],
        ["PP others", "El Bus", PPotherEbus],
        ["PP bioenergy", "El Bus", PPbioEbus],
        ["PP natural gas", "El Bus", PPgasEbus],
        ["PP lignite", "El Bus", PPligniteEbus],
        ["PP hard coal", "El Bus", PPcoalEbus],
        ["PP nuclear", "El Bus", PPnuclearEbus],
        ["Hydro", "Volatiles", HydroVol],
        ["Wind Offshore", "Volatiles", WoffVol],
        ["Wind Onshore", "Volatiles", WonVol],
        ["PV", "Volatiles", PVVol],
        ["Volatiles", "El Bus", VolEbus],
        ["El Bus", "Mobility Demand", EbusMob],
        ["El Bus", "HP Decentralised", EbusHPdec],
        ["El Bus", "Electricity Demand", EbusEldemand],
        ["El Bus", "Elect Export", EbusExport],
    )

    df = pd.DataFrame(data=d, columns=["From", "To", "Value"])
    df.loc[:, "Value"] = round(df.loc[:, "Value"] / 1000000, 1)
    
    return df
