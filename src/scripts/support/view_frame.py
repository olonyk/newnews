
import tkinter as tk
from collections import Counter
from datetime import datetime
from tkinter import ttk, scrolledtext
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
        tk.Frame.__init__(self, master, background="#0000ff")

        text_frame = tk.Frame(master, background="#000000")
        graph_frame = tk.Frame(master, background="#000000")
        
        self.text_prompt = self.create_text_widget(text_frame)

        (scrolled_frame, self.scrolled_canvas) = self.create_graph_widget(graph_frame)

        
        self.plot_frames = []
        self.populate(company_data, scrolled_frame)
        self.layout()

        text_frame.pack(side=tk.TOP, fill="x", expand=False)
        graph_frame.pack(side=tk.BOTTOM, fill="both", expand=True)

    def create_graph_widget(self, parent):
        canvas = tk.Canvas(parent, borderwidth=0, background="#000000")
        frame = tk.Frame(canvas, background="#000000")
        vsb = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)

        vsb.pack(side="right", fill="y", expand=0)
        canvas.pack(side="left", fill="both", expand=1)
        canvas.create_window((4,4), window=frame, anchor="nw", 
                                  tags="frame")

        frame.bind("<Configure>", self.onFrameConfigure)
        canvas.bind("<Configure>", self.onFrameConfigure)
        return frame, canvas


    def create_text_widget(self, parent):
        editArea = scrolledtext.ScrolledText(master=parent,
                                             wrap=tk.WORD,
                                             width=20,
                                             height=10,
                                             background="#000000",
                                             foreground="#00ff00")
        editArea.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        return editArea
        # Adding some text, to see if scroll is working as we expect it
        editArea
        """\
        Integer posuere erat a ante venenatis dapibus.
        Posuere velit aliquet.
        Aenean eu leo quam. Pellentesque ornare sem.
        Lacinia quam venenatis vestibulum.
        Nulla vitae elit libero, a pharetra augue.
        Cum sociis natoque penatibus et magnis dis.
        Parturient montes, nascetur ridiculus mus.
        """)
                

    def populate(self, company_data, scrolled_frame):
        self.plot_frames = []
        for i, company in enumerate(company_data):
            p_frame = self.build_plot_frame(scrolled_frame, company)
            self.plot_frames.append(p_frame)
    
    def layout(self):
        if self.plot_frames:
            for widget in self.plot_frames:
                widget.grid_remove()
            items_per_row = int(self.scrolled_canvas.winfo_width() / self.plot_frames[0].winfo_width())
            if items_per_row < 1:
                items_per_row = 1
            for i, widget in enumerate(self.plot_frames):
                widget.grid(row=int(i/items_per_row), column=i%items_per_row, sticky=S+E, padx=(0, 5), pady=(0, 5))

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.scrolled_canvas.configure(scrollregion=self.scrolled_canvas.bbox("all"))
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