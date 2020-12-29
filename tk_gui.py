from tkinter import *
from _tkinter import *


class AppWindow:
    def __init__(self):
        self.root = Tk(className="Webscraping desktop app")
        self.root.geometry("300x300")

        # set window frames
        self.firstWindowFrame = Frame(self.root)
        self.firstWindowFrame.grid()
        self.selectOneWindowFrame = Frame(self.root)
        self.selectOneWindowFrame.grid()
        self.compareWindowFrame = Frame(self.root)
        self.compareWindowFrame.grid()

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

        # self.goBackButton: Button = Button(self.root,
        #                                    text="<-- Back",
        #                                    command=self.put_on_grid()
        #                                    )

        """Second window on radio button - single country (shown if conditions met)"""
        self.inputLabel: Label = Label(self.selectOneWindowFrame,
                                       text="Choose country:",
                                       pady=5,
                                       padx=5)
        self.firstCountry: Entry = Entry(self.selectOneWindowFrame,
                                         pady=5,
                                         padx=5)
        self.confirmButton_2: Button = Button(self.selectOneWindowFrame,
                                              text="Confirm",
                                              highlightcolor="blue",
                                              justify="center",
                                              pady=5,
                                              command="")   # TODO fill the command

        """Second window on radio button - compare (shown if conditions met)"""
        self.inputLabelCompare: Label = Label(self.compareWindowFrame,
                                              text="Choose first country: ",
                                              pady=5,
                                              padx=5)
        self.inputLabelCompareSecond: Label = Label(self.compareWindowFrame,
                                                    text="Choose second country: ",
                                                    pady=5,
                                                    padx=5)
        self.firstCountry_2: Entry = Entry(self.compareWindowFrame,
                                           pady=5,
                                           padx=5)
        self.comparingCountry: Entry = Entry(self.compareWindowFrame,
                                             pady=5,
                                             padx=5)
        self.confirmButton_2: Button = Button(self.compareWindowFrame,
                                              text="Confirm",
                                              highlightcolor="blue",
                                              justify="center",
                                              pady=5,
                                              command="")  # TODO fill the command

    @staticmethod
    def destroy_frame(frame: "window frame") -> "while used destroys frame":
        frame.grid_forget()
        # frame.destroy()

    def hello_window(self) -> "buttons are put on grid":
        # try:
        #     self.destroy_frame(self.selectOneWindowFrame)
        # except TclError as e:
        #     print(e)
        #     try:
        #         self.destroy_frame(self.radioCompareCountry)
        #     except TclError:
        #         pass
        # finally:
        self.helloLabel.grid(row=0)
        self.radioSingleCountry.grid(row=1)
        self.radioCompareCountry.grid(row=2)
        self.confirmButton.grid(row=3)
        self.firstWindowFrame.mainloop()

    def confirm_button_onclick(self) -> "Changes the layout of the window":
        self.destroy_frame(self.firstWindowFrame)
        if self.radioButton.get() == "SINGLE":
            self.inputLabel.grid(row=0, column=0)
            self.firstCountry.grid(row=0, column=1)
            self.confirmButton.grid(row=1, column=1)
            self.selectOneWindowFrame.mainloop()

        elif self.radioButton.get() == "CMP":
            self.inputLabelCompare.grid(row=0, column=0)
            self.inputLabelCompareSecond.grid(row=1, column=0)
            self.firstCountry_2.grid(row=0, column=1)
            self.comparingCountry.grid(row=1, column=1)
            self.confirmButton_2.grid(row=2, column=1)
            self.compareWindowFrame.mainloop()
        else:
            pass
            # TODO throw custom exception


if __name__ == "__main__":
    AW = AppWindow()
    AW.hello_window()
