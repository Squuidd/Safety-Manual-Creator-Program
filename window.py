import PySimpleGUI as sg

WINDOW_NAME = "Safety Manual Creator"
font = ("Arial", 14)
white_space = '                                                                                                                  '

def main(_in):
    
    search = [
        [
            sg.InputText(key="refine", enable_events=True, size=(400, 90), font=font),
        ]
    ]
    name = [
        [
            sg.InputText(key="name", size=(400, 90), font=font),
        ]
    ]
    Layout = [
        [
            sg.Text(f"Unselected {white_space}", font=font), 
            sg.Text("Selected", font=font)
        ],
        [
            sg.Listbox(
                values=_in,
                key="selected_not",
                change_submits=True,
                size=(60, 30), #50, 20,
                font=font
            ),
            sg.Listbox(
                values=[],
                key="selected",
                change_submits=True,
                size=(60, 30), #50, 20
                font=font
            )
        ],
        [
            sg.Frame("Search", layout=search, size=(500, 60), font=font),
            sg.Frame("Company Name", layout=name, size=(500, 60), font=font)

        ],
        [
            sg.Button("Create Safety Programs", key="create_program", font=font),
            sg.Button("Create Safety Manuals", key="create_manual", font=font),
            # sg.Button("Set directorys/files", key="set", font=font), # Phase this out. Package docs?
            sg.Button("How to use.", key="how_to", font=font)
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
                    sg.PopupOK("All fields must be entered before proceeding", font=font)

            

            
            update()

    window.close()


def file_select():
    Layout = [
        [
            sg.InputText(visible=True, key='fig_path', size=(35, 0), font=font), sg.FileBrowse("Select file", font=font),

        ],
        [
            sg.Button("Done", key="done", font=font)
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
            sg.InputText(visible=True, key='fig_path', size=(35, 0), font=font), sg.FolderBrowse("Select Folder", font=font),

        ],
        [
            sg.Button("Done", key="done", font=font)
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
            sg.InputText(visible=True, key='fig_path', size=(35, 0), font=font),
            sg.FileSaveAs(
                key='fig_path',
                file_types=type,  # TODO: better names
                # (('PNG', '.png'), ('JPG', '.jpg'))
                font=font
            ),

        ],
        [
            sg.Button("Done", key="done", font=font)
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
    layout = [[sg.Text("Here is how to operate the Safety Manual Creator software.", key="how_to_dialogue", font=font)]]
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
                                layout=[[sg.ProgressBar(max_value=max, orientation='h', size=(50, 50), key='loading')]], #20, 20
                                no_titlebar=True, keep_on_top=True)
        self.window.read(timeout=0)  # immediately read
        self.value = 0

    def inc(self):
        self.value += 1
        self.window.Element("loading").update(self.value)

    # Kill object and window
    def close(self):
        self.window.Close()
