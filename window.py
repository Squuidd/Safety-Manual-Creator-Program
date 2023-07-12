import PySimpleGUI as sg

WINDOW_NAME = "Safety Manual Creator"


def main(_in):
    search = [
        [
            sg.InputText(key="refine", enable_events=True, ),
        ]
    ]
    name = [
        [
            sg.InputText(key="name", ),
        ]
    ]
    Layout = [
        [
            sg.Listbox(
                values=_in,
                key="selected_not",
                change_submits=True,
                size=(50, 20)
            ),
            sg.Listbox(
                values=[],
                key="selected",
                change_submits=True,
                size=(50, 20)
            )
        ],
        [
            sg.Frame("Search", layout=search),
            sg.Frame("Company Name", layout=name)

        ],
        [
            sg.Button("Create Safety Programs", key="create_program"),
            sg.Button("Create Safety Manuals", key="create_manual"),
            sg.Button("Set directorys/files", key="set"), # Phase this out. Package docs?
            sg.Button("How to use.", key="how_to")
        ],
    ]
    # Create the Window
    return sg.Window(WINDOW_NAME, Layout)


def set(config):
    def update():
        window.Element("input_manual").update(config["manual"])
        window.Element("input_program").update(config["program"])


    space = 12
    wide = 35
    remote = [
        [
            sg.Text("Program Folder", size=(space, 0)),
            sg.InputText(k="input_program", size=(wide, 0)),
            sg.Button("Pick", key="program")
        ],
        [
            sg.Text("Manual File", size=(space, 0)),
            sg.InputText(k="input_manual", size=(wide, 0)),
            sg.Button("Pick", key="manual"),

        ],
    ]

    Layout = [
        [sg.Frame("", layout=remote), ],
        [sg.Button("OK", k="ok")]
    ]
    # Create the Window
    window = sg.Window(WINDOW_NAME, Layout)
    window.read(0)
    update()

    running = True
    while running:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            running = False
        else:

            if event == "program":
                config["program"] = folder_select()

            elif event == "manual":
                config["manual"] = file_select()

            elif event == "ok":
                if config["manual"] and config["program"]:
                    running = False
                else:
                    sg.PopupOK("All fields must be entered before proceeding")

            

            
            update()

    window.close()


def file_select():
    Layout = [
        [
            sg.InputText(visible=True, key='fig_path', size=(35, 0)), sg.FileBrowse("Select file"),

        ],
        [
            sg.Button("Done", key="done")
        ]
    ]
    window = sg.Window(WINDOW_NAME, Layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            window.close()
            return False

        elif (event in ['fig_path', "done"]) and (values['fig_path'] != ''):
            path = values['fig_path']
            break

    window.close()
    return path


def folder_select():
    Layout = [
        [
            sg.InputText(visible=True, key='fig_path', size=(35, 0)), sg.FolderBrowse("Select Folder"),

        ],
        [
            sg.Button("Done", key="done")
        ]
    ]
    window = sg.Window(WINDOW_NAME, Layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            window.close()
            return False

        elif (event in ['fig_path', "done"]) and (values['fig_path'] != ''):
            path = values['fig_path']
            break

    window.close()
    return path


def save_as(type):
    
    Layout = [
        [
            sg.InputText(visible=True, key='fig_path', size=(35, 0)),
            sg.FileSaveAs(
                key='fig_path',
                file_types=type,  # TODO: better names
                # (('PNG', '.png'), ('JPG', '.jpg'))
            ),

        ],
        [
            sg.Button("Done", key="done")
        ]
    ]
    window = sg.Window(WINDOW_NAME, Layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            window.close()
            return False

        elif (event in ['fig_path', "done"]) and (values['fig_path'] != ''):
            path = values['fig_path']
            break

    window.close()
    return path

def how_to(): # Displays the How To Use page
    layout = [[sg.Text("Here is how to operate the Safety Manual Creator software.", key="how_to_dialogue")]]
    window = sg.Window("How To Use", layout)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
    window.close()
 
class StickyPopup:
    def __init__(self, Text):
        self.window = sg.Window("", layout=[[sg.Text(Text)]], no_titlebar=True, keep_on_top=True)
        self.window.read(timeout=0)  # immediately read

    # Kill object and window
    def close(self):
        self.window.Close()


class StickyLoading:
    def __init__(self, max):
        self.window = sg.Window("",
                                layout=[[sg.ProgressBar(max_value=max, orientation='h', size=(20, 20), key='loading')]],
                                no_titlebar=True, keep_on_top=True)
        self.window.read(timeout=0)  # immediately read
        self.value = 0

    def inc(self):
        self.value += 1
        self.window.Element("loading").update(self.value)

    # Kill object and window
    def close(self):
        self.window.Close()
