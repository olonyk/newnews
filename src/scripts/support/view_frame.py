
import tkinter as tk
from collections import Counter
from datetime import datetime
from tkinter import ttk
from tkinter.ttk import Frame, Radiobutton, Label, Scrollbar, Button, OptionMenu, Entry
from tkinter import Spinbox, IntVar
from tkinter import *
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2TkAgg)
from matplotlib.figure import Figure

class ViewFrame(tk.Frame):
    def __init__(self, master=None, company_data=None):
        self.master = master
        self.master.title("View frame")
        tk.Frame.__init__(self, master)

        # Disable toolbar
        #mpl.rcParams['toolbar'] = 'None'
        
        self.canvas = tk.Canvas(master, borderwidth=0, background="#000000")
        self.frame = tk.Frame(self.canvas, background="#000000")
        self.vsb = tk.Scrollbar(master, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw", 
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind("<Configure>", self.onFrameConfigure)
        self.plot_frames = []
        self.populate(company_data)
        self.layout()

    def populate(self, company_data):
        self.plot_frames = []
        for i, company in enumerate(company_data):
            p_frame = self.build_plot_frame(self.frame, company)
            self.plot_frames.append(p_frame)
    
    def layout(self):
        if self.plot_frames:
            for widget in self.plot_frames:
                widget.grid_remove()
            items_per_row = int(self.canvas.winfo_width() / self.plot_frames[0].winfo_width())
            if items_per_row < 1:
                items_per_row = 1
            for i, widget in enumerate(self.plot_frames):
                widget.grid(row=int(i/items_per_row), column=i%items_per_row, sticky=S+E, padx=(0, 5), pady=(0, 5))

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.layout()

    def build_plot_frame(self, parent_container, company_data):
        """ Given a company dictionary, creates a plot on a frame.
        """
        p_frame = Frame(parent_container, relief=GROOVE, borderwidth=2, background="#000000")
        # Create a list of datetime.
        dates = []
        for sighting in company_data["sightings"]:
            dates.append(datetime.strptime(sighting["datetime"][:10], "%Y-%m-%d"))
        # Create the plot
        
        dates = list(Counter(dates).items())
        x, y = zip(*dates)
        fig = plt.figure(figsize=(5, 5), dpi=100)
        axis = fig.add_subplot(111)
        axis.bar(x, y, color='green')
        axis.set_facecolor((0, 0, 0))
        fig.autofmt_xdate()
        axis.spines['top'].set_color('green')
        axis.spines['right'].set_color('green')
        axis.spines['bottom'].set_color('green')
        axis.spines['left'].set_color('green')
        axis.xaxis.label.set_color('green')
        axis.tick_params(axis='x', colors='green')
        axis.tick_params(axis='y', colors='green')
        fig.patch.set_facecolor('black')
    
        #hide the toolbar
        fig.canvas.toolbar.pack_forget()
        axis.set_clip_on(False)
        # Populate the tkinter frame
        label = tk.Label(p_frame, text=company_data["name"], font=("Monaco", 24), background="#000000", foreground="#00ff00")
        label.pack(pady=10,padx=10)
        canvas = FigureCanvasTkAgg(fig, p_frame)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        #toolbar = NavigationToolbar2TkAgg(canvas, p_frame)
        #toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        return p_frame