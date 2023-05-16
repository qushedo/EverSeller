import customtkinter


class App(customtkinter.CTk):
    def __init__(self, size=(860, 500), name="NeverSeller v1.4.0"):
        super().__init__()
        self.geometry(f"{size[0]}x{size[1]}")
        self.title(name)
        self.minsize(width=860, height=500)
        self.maxsize(width=8128, height=500)
        customtkinter.set_appearance_mode("Dark")
        self.NameFont = customtkinter.CTkFont(family="MicrogrammaDBolExt", size=18)
        self.CodeFont = customtkinter.CTkFont(family="Cascadia Code", size=12)
        self.Name2Font = customtkinter.CTkFont(family="Cascadia Mono", size=14)