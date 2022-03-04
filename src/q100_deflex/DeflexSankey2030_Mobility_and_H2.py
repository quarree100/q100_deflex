import os
import numpy as np
import pandas as pd
from holoviews_sankey import create_and_save_sankey

import deflex as dflx

path = "/home/uwe/deflex/quarree100/results_cbc/"
dump = "2030-DE02-Agora.dflx"
deflx = os.path.join(path, dump)

all_results = dflx.fetch_deflex_result_tables(deflx)

#From Commodities to ...
comm=all_results["commodity"]

AllSources=np.sum(comm.xs("source", level=0, axis=1)) #all sources
H2importH2bus=AllSources[0]

ElectrolyserH2bus=np.sum(np.sum(comm.xs("Electrolysis", level=1, axis=1)))

H2bus=np.sum(comm.xs("H2", level=5, axis=1)) #H2 bus (H2bus[4] is out since its H2 storage)
H2busCHP=H2bus[0]
H2busMob=H2bus[1]
H2busOtherdemand=H2bus[2]
H2busPP=H2bus[3]

FC=np.sum(comm.xs("fuel converter", level=4, axis=1)) # All fuel converters
ComoilMob=FC[1] #FC[0] is H2busMob

#From Electricity bus
elect=all_results["electricity"]
mob=all_results["mobility"] #because there is excess and shortage in mobility

Unregulated2=np.sum(np.sum(mob.xs("excess", level=4, axis=1))) #excess in mobility (see DeflexSankey2030 - Power)
Shortage2=np.sum(np.sum(mob.xs("shortage", level=0, axis=1))) #shortage in mobility (see DeflexSankey2030 - Power)

EbusMob=np.sum(np.sum(elect.xs("fuel converter", level=4, axis=1)))-Unregulated2+Shortage2 # because shortage+excess effect
EbusElectrolyser=np.sum(np.sum(elect.xs("Electrolysis", level=5, axis=1)))

#Create df (From, To, value)

d=(
["Oil", "Mobility Demand", ComoilMob],
["From El Bus", "Electrolyser", EbusElectrolyser],
["From El Bus", "Mobility Demand", EbusMob],
["H2 Import", "H2", H2importH2bus],
["Electrolyser", "H2", ElectrolyserH2bus],
["H2", "H2 Industry Demand", H2busOtherdemand],
["H2", "Mobility Demand", H2busMob],
["H2", "CHP H2", H2busCHP],
["H2", "PP H2", H2busPP]
)

df=pd.DataFrame(data=d, columns=["From", "To", "Value"])
df.loc[:,"Value"]=round(df.loc[:,"Value"]/1000000,1)
print(df)

a=create_and_save_sankey(df,
                         filename=os.path.join(path, "Sankey Deflex - 2030 Mobility & H2 Sector"),
                         title="Mobility & H2 Sector - 2030",
                         edge_color_index="To",
                         fontsize=20,
                         label_text_font_size="12pt",
                         node_width=45)