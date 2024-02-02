import ttkbootstrap as ttk
import pickle


class Events:
    def __init__(self):
        self.count = 0
        self.multiplier = 1
        self.x1_count = 0
        self.x10_count = 0
        self.x100_count = 0
        self.x1000_count = 0

    def counters(self):
        upgrade_buttons = [upgrade_x1, upgrade_x10, upgrade_x100, upgrade_x1000]
        save_label.forget()
        load_label.forget()
        for i, button in enumerate(upgrade_buttons):
            if self.count < 100 * 10 ** i:
                button.config(state="disabled")
            else:
                button.config(state="normal")
        self.count += self.multiplier
        clicker_count_var.set(self.count)
        self.totals()

    def upgrade_x1(self):
        self.x1_count += 1
        if self.count >= 100:
            self.count -= 100
            self.multiplier += 1
            upgrade_x2.config(state="disabled") if self.count < 100 else None
            clicker_count_var.set(self.count)
            self.totals()

    def upgrade_x10(self):
        self.x10_count += 1
        if self.count >= 1000:
            self.count -= 1000
            self.multiplier += 10
            upgrade_x4.config(state="disabled") if self.count < 1000 else None
            clicker_count_var.set(self.count)
            self.totals()

    def upgrade_x100(self):
        self.x100_count += 1
        if self.count >= 10000:
            self.count -= 10000
            self.multiplier += 100
            upgrade_x8.config(state="disabled") if self.count < 10000 else None
            clicker_count_var.set(self.count)
            self.totals()

    def upgrade_x1000(self):
        self.x1000_count += 1
        if self.count >= 100000:
            self.count -= 100000
            self.multiplier += 100
            upgrade_x10.config(state="disabled") if self.count < 100000 else None
            clicker_count_var.set(self.count)
            self.totals()

    def save_file(self):
        try:
            with open("save_data.dat", "wb") as file:
                pickle.dump([self.count, self.multiplier, self.x1_count, self.x10_count,
                             self.x100_count, self.x1000_count], file)
                save_label.pack(side="bottom")
                self.totals()
        except FileNotFoundError as error_code:
            print(error_code)

    def load_file(self):
        try:
            with open("save_data.dat", "rb") as file:
                count, multiplier, x1, x10, x100, x1000 = pickle.load(file)
                self.count = count
                self.multiplier = multiplier
                self.x1_count = x1
                self.x10_count = x10
                self.x100_count = x100
                self.x1000_count = x1000
                clicker_count_var.set(self.count)
                load_label.pack(side="bottom")
                self.totals()
        except FileNotFoundError as error_code:
            print(error_code)

    def totals(self):
        totals = f"Total Clicks = {self.multiplier} \
                    Total +1 = {self.x1_count} \
                    Total +10 = {self.x10_count} \
                    Total +100 = {self.x100_count} \
                    Total +1K = {self.x1000_count}"
        totals_var.get()
        totals_var.set(totals)


if __name__ == "__main__":

    # root
    root = ttk.Window(themename="darkly")
    root.geometry("")
    root.resizable(0,0)

    # save/load
    options_frame = ttk.Frame(root)
    clicker_instance = Events()
    save_button = ttk.Button(options_frame, text="Save", command=clicker_instance.save_file)
    load_button = ttk.Button(options_frame, text="Load", command=clicker_instance.load_file)

    # main area
    clicker_frame = ttk.Frame(root)
    clicker_count_var = ttk.IntVar()
    counter_label = ttk.Label(clicker_frame, textvariable=clicker_count_var, font="Verdana 24 bold")
    clicker = ttk.Button(clicker_frame, text="Click!", command=clicker_instance.counters)
    clicker.bind("<Return>", lambda event: "break")
    clicker.bind("<Button-3>", lambda event: clicker_instance.counters())

    # upgrade area
    upgrade_frame = ttk.Frame(root)
    upgrade_x1 = ttk.Button(upgrade_frame, text="+1 (c: 100)\n(Hotkey: F1)", command=clicker_instance.upgrade_x1)
    clicker.bind("<F1>", lambda event: clicker_instance.upgrade_x1())
    upgrade_x10 = ttk.Button(upgrade_frame, text="+10 (c: 1K)\n(Hotkey: F2)", command=clicker_instance.upgrade_x10)
    clicker.bind("<F2>", lambda event: clicker_instance.upgrade_x10())
    upgrade_x100 = ttk.Button(upgrade_frame, text="+100 (c: 10K)\n(Hotkey: F3)", command=clicker_instance.upgrade_x100)
    clicker.bind("<F3>", lambda event: clicker_instance.upgrade_x100())
    upgrade_x1000 = ttk.Button(upgrade_frame, text="+1K (c: 100K)\n(Hotkey: F4)", command=clicker_instance.upgrade_x1000)
    clicker.bind("<F4>", lambda event: clicker_instance.upgrade_x1000())

    # totals area
    totals_frame = ttk.Frame(root)
    totals_var = ttk.StringVar()
    totals_label = ttk.Label(totals_frame, textvariable=totals_var)

    # footer area
    footer_frame = ttk.Frame(root)
    save_label = ttk.Label(footer_frame, text="Game saved!", font="Verdana 8")
    load_label = ttk.Label(footer_frame, text="Game loaded!", font="Verdana 8")

    # Main Area Package
    # Save/Load package
    options_frame.grid(row=0, column=0, sticky="n", padx=10, pady=20)
    save_button.pack(side="left", ipady=5, ipadx=5, pady=10, padx=10)
    load_button.pack(side="right", ipady=5, ipadx=5, pady=10, padx=10)

    # Upgrades Package
    upgrade_frame.grid(row=1, column=0, pady=50, padx=10, sticky="nsew")
    upgrade_x1.pack(ipady=10, ipadx=60, pady=5)
    upgrade_x10.pack(ipady=10, ipadx=60, pady=5)
    upgrade_x100.pack(ipady=10, ipadx=55, pady=5)
    upgrade_x1000.pack(ipady=10, ipadx=55, pady=5)

    # Clicker Package
    clicker_frame.grid(row=1, column=1, pady=50, padx=10, sticky="nsew")
    counter_label.pack(pady=50, padx=50)
    clicker.pack(ipady=10, ipadx=50)

    # Totals Package
    totals_frame.grid(row=2, column=0, columnspan=2, pady=10, padx=50, sticky="nsew")
    totals_label.pack()

    # Footer Package
    footer_frame.grid(row=3, column=0, columnspan=2, pady=20, padx=10, sticky="nsew")

    # loop
    upgrade_x1.config(state="disabled")
    upgrade_x10.config(state="disabled")
    upgrade_x100.config(state="disabled")
    upgrade_x1000.config(state="disabled")
    
    clicker_instance.totals()
    clicker_instance.load_file()
    root.mainloop()
