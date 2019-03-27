import sys
import tkinter as tk
import tkinter.ttk as ttk

from bets.ui.matches_observable import MatchesObservable
from bets.ui.matches_tab.matches_tab import MatchesTab
from bets.ui.menu_bar import MenuBar
from bets.ui.scenarios_tab.scenarios_tab import ScenariosTab
from bets.utils import log


class BetsApp:

    def __init__(self):
        self.win = tk.Tk()
        self.win.title("Bets App")

        # shared matches instance
        self.matches = MatchesObservable()

        # create tabs container
        self.tabs = ttk.Notebook(self.win)
        self.tabs.grid(column=0, row=0, padx=4, pady=2)

        # create tabs
        self.matches_tab = MatchesTab(self.win, self.tabs, self.matches)

        self.scenarios_tab = ScenariosTab(self.win, self.tabs, self.matches)
        # create menus
        self.menu_bar = MenuBar(self.win, self.matches)


def main(args):
    log.init()
    app = BetsApp()
    app.win.mainloop()


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
