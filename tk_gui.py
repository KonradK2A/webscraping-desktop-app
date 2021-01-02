from tkinter import *
from tkinter import Frame

import ctypes


class AppWindow:
    def __init__(self):
        self.root = Tk(className="Webscraping desktop app")
        self.root.geometry("300x300")

        # app widgets and frames
        try:
            self.frames()
            self.widgets_initialize()
        except NameError:
            exit(1)

    # define window frames
    def frames(self):
        self.downloadingDataInfoFrame = Frame(self.root)
        self.firstWindowFrame: Frame = Frame(self.root)
        self.firstWindowFrame.grid()
        self.selectCountryWindow: Frame = Frame(self.root)
        self.selectCountryWindow.grid()
        self.compareWindowFrame: Frame = Frame(self.root)
        self.compareWindowFrame.grid()

    # define widgets
    def widgets_initialize(self):
        self.radioButton = StringVar()
        self.radioButton.set(" ")

        """Main window shown on hello"""
        self.helloLabel: Label = Label(self.firstWindowFrame,
                                       text="Welcome to the app\n"
                                       "Select option and click the button to run the program",
                                       justify="center")
        self.radioSingleCountry: Radiobutton = Radiobutton(self.firstWindowFrame,
                                                           text="Check data for one country",
                                                           value="SINGLE",
                                                           pady=5,
                                                           variable=self.radioButton)
        self.radioCompareCountry: Radiobutton = Radiobutton(self.firstWindowFrame,
                                                            text="Compare two countries",
                                                            value="CMP",
                                                            pady=5,
                                                            variable=self.radioButton)
        self.confirmButton: Button = Button(self.firstWindowFrame,
                                            text="Go",
                                            highlightcolor="blue",
                                            justify="center",
                                            pady=5,
                                            command=self.confirm_button_onclick)

        self.goBackButton: Button = Button(self.selectCountryWindow,
                                           text="<-- Back",
                                           command=self.hello_window,
                                           padx=5,
                                           pady=5)

        """Second window on radio button"""
        self.firstCountryLabel: Label = Label(self.selectCountryWindow,
                                              text="Choose country:",
                                              pady=5,
                                              padx=5)
        self.firstCountryEntry: Entry = Entry(self.selectCountryWindow)
        self.runScriptButton: Button = Button(self.selectCountryWindow,
                                              text="Confirm",
                                              highlightcolor="blue",
                                              justify="center",
                                              pady=5,
                                              command="")   # TODO fill the command
        self.secondCountryLabel: Label = Label(self.selectCountryWindow,
                                               text="Select second country",
                                               pady=5,
                                               padx=5)
        self.secondCountryEntry: Entry = Entry(self.selectCountryWindow)

    @staticmethod
    def forget_frame(frame: "window frame") -> "while used destroys frame":
        frame.grid_forget()
        # frame.destroy()

    # Replaced with ctypes box
    # @staticmethod
    # def window_on_error(parentWindow: Frame):
    #     errorLabel: Label = Label(parentWindow, text="Woopsie! Something went wrong.\n"
    #                                             "Quitting application",
    #                               justify="center")

    def hello_window(self) -> "buttons are put on grid":
        # if not self.isFirstRun:
        #     self.forget_frame(self.selectCountryWindow)
        self.helloLabel.grid(row=0, column=0)
        self.radioSingleCountry.grid(row=1, column=0)
        self.radioCompareCountry.grid(row=2, column=0)
        self.confirmButton.grid(row=3, column=0)
        self.firstWindowFrame.mainloop()

    def confirm_button_onclick(self) -> "Changes the layout of the window":
        self.forget_frame(self.firstWindowFrame)
        if self.radioButton.get() == "SINGLE":
            self.firstCountryLabel.grid(row=0, column=0)
            self.firstCountryEntry.grid(row=0, column=1)
            self.runScriptButton.grid(row=1, column=1)
            self.goBackButton.grid(row=2, column=1)
        elif self.radioButton.get() == "CMP":
            self.firstCountryLabel.grid(row=0, column=0)
            self.secondCountryLabel.grid(row=1, column=0)
            self.firstCountryEntry.grid(row=0, column=1)
            self.secondCountryEntry.grid(row=1, column=1)
            self.runScriptButton.grid(row=2, column=1)
            self.goBackButton.grid(row=3, column=0)
        else:
            ctypes.windll.user32.MessageBoxW(0, f"Application raised a warning.",
                                             "Warining!", 0x10)
        self.selectCountryWindow.mainloop()

    def return_values(self):
        return [self.radioButton.get(), self.firstCountryEntry, self.secondCountryEntry]


if __name__ == "__main__":
    AW = AppWindow()
    AW.hello_window()
