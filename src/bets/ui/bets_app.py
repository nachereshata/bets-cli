from tkinter import Tk
from tkinter.ttk import Notebook

from bets.ui.matches_observable import MatchesObservable
from bets.ui.matches_tab.matches_tab_frame import MatchesTabFrame
from bets.ui.menu_bar import MenuBar
from bets.ui.scenarios_tab.scenarios_tab import ScenariosTab
from bets.utils import log


class BetsApp:

    def __init__(self):
        self.win = Tk()
        self.win.title("Bets App")
        self.win.resizable(0, 0)

        # shared matches instance
        self.matches = MatchesObservable()

        # create tabs container
        self.tabs = Notebook(self.win)
        self.tabs.grid(column=0, row=0, padx=4, pady=2, sticky="WE")

        # create tabs
        self.matches_tab = MatchesTabFrame(self.win, self.tabs, self.matches)
        self.scenarios_tab = ScenariosTab(self.win, self.tabs, self.matches)

        # create menus
        self.menu_bar = MenuBar(self.win, self.matches)


def main():
    log.init()
    app = BetsApp()
    app.win.mainloop()


def run():
    """Entry point for console_scripts
    """
    main()


if __name__ == "__main__":
    main()
