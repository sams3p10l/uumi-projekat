from tkinter import *
from tkinter import messagebox

from PIL import ImageTk, Image


class Gui(Tk):

    def __init__(self):
        super().__init__()

        main_frame = Frame(self, borderwidth=2, relief=GROOVE, padx=10, pady=10)

        img = ImageTk.PhotoImage(Image.open("klinika.png"))
        panel = Label(main_frame, image=img)
        panel.pack(side="bottom", fill="both", expand="yes")

        menu = Menu(self)
        self.config(menu=menu)

        subMenu = Menu(menu)
        menu.add_cascade(label="Pacijenti", menu=subMenu)
        subMenu.add_command(label="Prikaz pacijenata")
        subMenu.add_command(label="Dodavanje pacijenata")
        subMenu.add_command(label="Izmena pacijenata")

        snimakMenu = Menu()
        menu.add_cascade(label="Snimanja", menu=snimakMenu)
        snimakMenu.add_command(label="Lista snimanja")
        snimakMenu.add_command(label="Dodavanje snimanja")
        snimakMenu.add_command(label="Izmena ili brisanje snimanja")

        izlazMenu = Menu()
        menu.add_cascade(label="Izlaz", menu=izlazMenu)
        izlazMenu.add_command(label="Izlaz", command=self.komanda_izlaz)

        main_frame.mainloop()

    def komanda_izlaz(self):
        odgovor = messagebox.askokcancel("Upozorenje", "Da li ste sigurni da želite da napustite aplikaciju?",
                                         icon="warning")
        if odgovor:
            self.destroy()


if __name__ == '__main__':
    gui = Gui()
