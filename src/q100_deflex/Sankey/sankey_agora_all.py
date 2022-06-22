"""Sankey"""
import os
from zipfile import ZipFile
import holoviews_sankey
from DeflexSankey2018_Heat import create_deflex_sankey as heat_2018
from DeflexSankey2018_Mobility_and_H2 import create_deflex_sankey as mobh2_2018
from DeflexSankey2018_Overview import create_deflex_sankey as overv_2018
from DeflexSankey2018_Power import create_deflex_sankey as power_2018
from DeflexSankey2030_Heat import create_deflex_sankey as heat_2030
from DeflexSankey2030_Mobility_and_H2 import create_deflex_sankey as mobh2_2030
from DeflexSankey2030_Overview import create_deflex_sankey as overv_2030
from DeflexSankey2030_Power import create_deflex_sankey as power_2030
from DeflexSankey2050_Heat import create_deflex_sankey as heat_2050
from DeflexSankey2050_Mobility_and_H2 import create_deflex_sankey as mobh2_2050
from DeflexSankey2050_Overview import create_deflex_sankey as overv_2050
from DeflexSankey2050_Power import create_deflex_sankey as power_2050

import deflex as dflx

url = (
    "https://files.de-1.osf.io/v1/resources/4nfam/providers/osfstorage"
    "/62222ea5c064270516d90efa?action=download&direct&version=1"
)

# path can be adapted to one owns need
q100_path = os.path.join(os.path.expanduser("~"), "deflex", "quarree100")

subtype = ""

fn = os.path.join(q100_path, "agora_examples.zip")
os.makedirs(os.path.dirname(fn), exist_ok=True)
if not os.path.isfile(fn):
    dflx.download(fn, url)
with ZipFile(fn, "r") as zip_ref:
    zip_ref.extractall(q100_path)

print("All examples extracted to %s." % q100_path)

path = os.path.join(q100_path, "results_cbc")
sankey_in = {}

year = 2018
result_file = f"{year}-DE02-Agora{subtype}.dflx"
sankey_in["Heat 2018"] = heat_2018(path, result_file)
sankey_in["Mob-H2 2018"] = mobh2_2018(path, result_file)
sankey_in["Overview 2018"] = overv_2018(path, result_file)
sankey_in["Power 2018"] = power_2018(path, result_file)

year = 2030
result_file = f"{year}-DE02-Agora{subtype}.dflx"
sankey_in["Heat 2030"] = heat_2030(path, result_file)
sankey_in["Mob-H2 2030"] = mobh2_2030(path, result_file)
sankey_in["Overview 2030"] = overv_2030(path, result_file)
sankey_in["Power _2030"] = power_2030(path, result_file)

year = 2050
result_file = f"{year}-DE02-Agora{subtype}.dflx"
sankey_in["Heat 2050"] = heat_2050(path, result_file)
sankey_in["Mob-H2 2050"] = mobh2_2050(path, result_file)
sankey_in["Overview 2050"] = overv_2050(path, result_file)
sankey_in["Power 2050"] = power_2050(path, result_file)

input_files = os.path.join(q100_path, "sankey", "sankey_input.xlsx")
os.makedirs(os.path.dirname(input_files), exist_ok=True)
dflx.dict2file(sankey_in, input_files)

kwargs = {
    "show_plot": False,
    "edge_color_index": "To",
    "fontsize": 20,
    "label_text_font_size": "12pt",
    "node_width": 45,
}

holoviews_sankey.main(input_files, **kwargs)
