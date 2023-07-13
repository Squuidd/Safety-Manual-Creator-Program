import json

import PySimpleGUI as sg
import window as wd
import json
import os
import re

import safety_program_creator as scp


class Config():
    def __init__(self):
        if os.path.exists("config.json"):
            with open('config.json') as f:
                self.values = json.load(f)
        else:
            self.values = {}
            while not self.values.get("manual") or not self.values.get("program"):
                wd.set(self)

    def __setitem__(self, key, value):
        self.values[key] = value
        json_object = json.dumps(self.values, indent=4)
        with open("config.json", "w") as outfile:
            outfile.write(json_object)

    def __getitem__(self, item):
        return self.values.get(item)


class File():
    def __init__(self, direntry):
        self.dir_entry = direntry

    @property
    def path(self):
        return self.dir_entry.path

    def __repr__(self):
        return self.dir_entry.name[:-5]


def SaveBytes(path, b):
    with open(path, "wb") as f:
        f.write(b)


def Scandir(path):
    dir_list = os.scandir(path)

    found = []
    for i in list(dir_list):
        if i.is_file():
            if i.path[-4:len(i.path)] == "docx":
                found.append(File(i))
        else:
            found += Scandir(i.path)
    return found


def SetDisplay():
    def refine(_list):
        return [
            i for i in _list
            if values["refine"].lower() in i.__repr__().lower()
        ]

    In_List_Display = refine(In_List)
    Out_List_Display = refine(Out_List)

    window.Element("selected_not").update(values=In_List_Display)
    window.Element("selected").update(values=Out_List_Display)

# Replaces characters that are not compatible with xml
def fix_name(company_name):
    company_name = company_name.replace("&", "&amp;") #&#38;
    company_name = company_name.replace("<", "&lt;")
    company_name = company_name.replace(">", "&gt;")


    return company_name

try:
    CONFIG = Config()
    print(CONFIG["program"])
    In_List = Scandir(CONFIG["program"])
    Out_List = []
    In_List_Display = []
    Out_List_Display = []

    window = wd.main(In_List)
    while True:
        event, values = window.read()

        if values:
            company_name = fix_name(values["name"])

        if event == sg.WIN_CLOSED:
            break

        elif event == "set":
            wd.set(CONFIG)
            In_List = Scandir(CONFIG["program"])
            Out_List = []
            SetDisplay()

        elif event == "refine":
            SetDisplay()

        # zip
        elif event == "create_program":
            save_path = wd.save_as(
                (("ZIP", ".zip"),)
            )
            if save_path:
                pop = wd.StickyLoading(len(Out_List))
                _bytes = scp.create_program(
                    [i.path for i in Out_List],
                    company_name,
                    pop.inc
                )
                pop.close()
                SaveBytes(save_path, _bytes)

        # manual
        elif event == "create_manual":
            save_path = wd.save_as(
                (("DOCX", ".docx"),)
            )
            if save_path:
                pop = wd.StickyLoading(
                    len(Out_List) + 2
                )
                _bytes = scp.create_manual(
                    CONFIG["manual"],
                    [i.path for i in Out_List],
                    company_name,
                    pop.inc
                )
                pop.close()
                SaveBytes(save_path, _bytes)
                
        # How to use 
        elif event == "how_to":
            wd.how_to()

        # Move stuff around
        elif event in ["selected_not", "selected"]:
            item = values[event][0]
            if event == "selected_not":
                In_List.remove(item)
                Out_List.append(item)
            else:
                In_List.append(item)
                Out_List.remove(item)

            SetDisplay()

    window.close()
except Exception as e:
    import traceback

    sg.Popup(
        traceback.format_exc()
    )

    import pickle

    with open("error.pickle", 'wb') as f:
        pickle.dump(e, f)

# Test