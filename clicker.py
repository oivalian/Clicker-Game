import ttkbootstrap as ttk
import pickle
import time
import threading


class Events:
    def __init__(self):
        self.count = 0
        self.multiplier = 1
        self.x1_count = 0
        self.x10_count = 0
        self.x100_count = 0
        self.x1000_count = 0
        self.x10000_count = 0
        self.x100000_count = 0
        self.x1000000_count = 0
        self.x10000000_count = 0
        self.x100000000_count = 0

    def counters(self):
        upgrade_buttons = [upgrade_x1, upgrade_x10, upgrade_x100, upgrade_x1000, upgrade_x10000, upgrade_x100000,
                           upgrade_x1000000, upgrade_x10000000, upgrade_x100000000]
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

    def upgrade(self, button, count, cost, multiplier):
        count_total = getattr(self, f"x{count}_count")
        if self.count >= cost:
            self.count -= cost
            self.multiplier += multiplier
            count_total += 1
            setattr(self, f"x{count}_count", count_total)
            button.config(state="disabled") if self.count <= cost else None
            clicker_count_var.set(self.count)
            self.totals()

    def upgrade_x1(self):
        self.upgrade(upgrade_x1, 1, 100, 1)

    def upgrade_x10(self):
        self.upgrade(upgrade_x10, 10, 1000, 10)

    def upgrade_x100(self):
        self.upgrade(upgrade_x100, 100, 10000, 100)

    def upgrade_x1000(self):
        self.upgrade(upgrade_x1000, 1000, 100000, 1000)

    def upgrade_x10000(self):
        self.upgrade(upgrade_x10000, 10000, 1000000, 10000)

    def upgrade_x100000(self):
        self.upgrade(upgrade_x100000, 100000, 10000000, 100000)

    def upgrade_x1000000(self):
        self.upgrade(upgrade_x1000000, 1000000, 100000000, 1000000)

    def upgrade_x10000000(self):
        self.upgrade(upgrade_x10000000, 10000000, 1000000000, 10000000)

    def upgrade_x100000000(self):
        self.upgrade(upgrade_x100000000, 100000000, 10000000000, 100000000)

    def auto_clicker_threader(self):
        clicker_threader = threading.Thread(target=self.auto_clicker)
        clicker_threader.start()

    def cooldown_threader(self):
        cooldown_threader = threading.Thread(target=self.auto_clicker_cooldown)
        cooldown_threader.start()

    def auto_clicker(self):
        timer = 25
        end_timer = time.time() + timer
        while time.time() < end_timer:
            self.counters()
            clicker_count_var.set(self.count)
            time.sleep(0.1)
            auto_clicker.config(state="disabled")
            clicker.bind("<F10>", lambda event: "break")
        self.cooldown_threader()

    def auto_clicker_cooldown(self, cooldown=120):
        while cooldown > 0:
            cooldown -= 1
            time.sleep(1)
            cooldown_var.set(cooldown)
            clicker.bind("<F10>", lambda event: "break")
        auto_clicker.config(state="enabled") if cooldown == 0 else auto_clicker.config(state="disabled")
        clicker.bind("<F10>", lambda event: self.auto_clicker_threader())
        cooldown = 120 if cooldown == 0 else None
        cooldown_var.set(cooldown)

    def save_file(self):
        try:
            with open("save_data.dat", "wb") as file:
                pickle.dump([self.count, self.multiplier, self.x1_count, self.x10_count,
                             self.x100_count, self.x1000_count, self.x10000_count, self.x100000_count,
                             self.x1000000_count, self.x10000000_count, self.x100000000_count], file)
                save_label.pack(side="bottom")
                self.totals()
        except FileNotFoundError as error_code:
            print(error_code)

    def load_file(self):
        try:
            with open("save_data.dat", "rb") as file:
                saved_data = pickle.load(file)
                count, multiplier, *upgrade_counts = saved_data
                if len(upgrade_counts) < 9:
                    upgrade_counts += [0] * (9 - len(upgrade_counts))
                self.count = count
                self.multiplier = multiplier
                self.x1_count, self.x10_count, self.x100_count, self.x1000_count, self.x10000_count, \
                    self.x100000_count, self.x1000000_count, self.x10000000_count, \
                    self.x100000000_count = upgrade_counts
                clicker_count_var.set(self.count)
                load_label.pack(side="bottom")
                self.totals()
        except (FileNotFoundError, ValueError, EOFError) as error_code:
            print(error_code)

    def totals(self):
        totals = [
            (x1_lbl, self.x1_count, "+1"), (x10_lbl, self.x10_count, "+10"), (x100_lbl, self.x100_count, "+100"),
            (x1000_lbl, self.x1000_count, "+1K"), (x10000_lbl, self.x1000_count, "+10K"),
            (x100000_lbl, self.x10000_count, "+100K"), (x1000000_lbl, self.x1000000_count, "+1M"),
            (x10000000_lbl, self.x1000000_count, "+10M"), (x100000000_lbl, self.x10000000_count, "+100M"),
            (totals_lbl, self.multiplier, "Clicks"),]
        try:
            for lbl, multiplier, total in totals:
                lbl.config(text=f"Total {total} = {multiplier}")
        except ValueError as error_code:
            print(error_code)


if __name__ == "__main__":
    # root
    root = ttk.Window(themename="darkly")
    root.title("Clicker Game")
    root.geometry("")
    root.resizable(0, 0)

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

    # upgrade area
    upgrade_frame = ttk.Frame(root)
    upgrade_x1 = ttk.Button(upgrade_frame, text="+1 (c: 100)\n(Hotkey: F1)", command=clicker_instance.upgrade_x1)
    upgrade_x10 = ttk.Button(upgrade_frame, text="+10 (c: 1K)\n(Hotkey: F2)", command=clicker_instance.upgrade_x10)
    upgrade_x100 = ttk.Button(upgrade_frame, text="+100 (c: 10K)\n(Hotkey: F3)", command=clicker_instance.upgrade_x100)
    upgrade_x1000 = ttk.Button(upgrade_frame, text="+1K (c: 100K)\n(Hotkey: F4)",
                               command=clicker_instance.upgrade_x1000)
    upgrade_x10000 = ttk.Button(upgrade_frame, text="10K (c: 1M)\n Hotkey: F5", command=clicker_instance.upgrade_x10000)
    upgrade_x100000 = ttk.Button(upgrade_frame, text="100K (c: 10M)\n Hotkey: F6",
                                 command=clicker_instance.upgrade_x100000)
    upgrade_x1000000 = ttk.Button(upgrade_frame, text="+1M (c: 100M)\n(Hotkey: F7)",
                                  command=clicker_instance.upgrade_x1000000)
    upgrade_x10000000 = ttk.Button(upgrade_frame, text="+10M (c: 1B)\n(Hotkey: F8)",
                                   command=clicker_instance.upgrade_x10000000)
    upgrade_x100000000 = ttk.Button(upgrade_frame, text="+100M (c: 10B)\n(Hotkey: F9)",
                                    command=clicker_instance.upgrade_x100000000)

    # auto clicker
    auto_clicker = ttk.Button(upgrade_frame, text="Auto Clicker (25s)\n(Hotkey: F10)",
                              command=clicker_instance.auto_clicker_threader)
    cooldown_var = ttk.IntVar()
    cooldown_label = ttk.Label(upgrade_frame, textvariable=cooldown_var, font="Verdana 8")
    timer_counter_var = ttk.IntVar()
    timer_counter_label = ttk.Label(upgrade_frame, textvariable=timer_counter_var, font="Verdana 8")

    # totals area
    totals_frame = ttk.Frame(root)

    # header area
    header_frame = ttk.Frame(root)
    save_label = ttk.Label(header_frame, text="Game saved!", font="Verdana 8")
    load_label = ttk.Label(header_frame, text="Game loaded!", font="Verdana 8")

    # Main Area Package
    # Save/Load package
    options_frame.grid(row=0, column=0, sticky="nw", padx=50, pady=40)
    save_button.pack(side="left", ipady=5, ipadx=5, pady=10, padx=10)
    load_button.pack(side="right", ipady=5, ipadx=5, pady=10, padx=10)

    # Upgrades Package
    # upgrade buttons configuration
    upgrade_frame.grid(row=1, column=0, pady=50, padx=50, sticky="nsew")
    upgrade_package = {upgrade_x1: [0, 0], upgrade_x10: [1, 0], upgrade_x100: [2, 0], upgrade_x1000: [3, 0],
                       upgrade_x10000: [4, 0], upgrade_x100000: [0, 1], upgrade_x1000000: [1, 1],
                       upgrade_x10000000: [2, 1], upgrade_x100000000: [3, 1], auto_clicker: [4, 1]}

    for upgrade_button, (row, col) in upgrade_package.items():  # treat upgrade as upgrade button - [X, X] as (row, col)
        upgrade_button.grid(row=row, column=col, ipady=10, ipadx=50, pady=10, padx=10)
        upgrade_button.config(width=10)        # sets button width to 10
    cooldown_label.grid(row=4, column=1, sticky="se")

    # Clicker Package
    clicker_frame.grid(row=1, column=1, pady=50, padx=50, sticky="nsew")
    counter_label.pack(pady=50, padx=50)
    clicker.pack(ipady=10, ipadx=50)

    # Totals Package
    totals_frame.grid(row=2, column=0, columnspan=2, pady=10, padx=50, sticky="nsew")

    x1_lbl = ttk.Label(totals_frame, text=f"Total +1 = {clicker_instance.x1_count}")
    x10_lbl = ttk.Label(totals_frame, text=f"Total +10 = {clicker_instance.x10_count}")
    x100_lbl = ttk.Label(totals_frame, text=f"Total +100 = {clicker_instance.x100_count}")
    x1000_lbl = ttk.Label(totals_frame, text=f"Total +1K = {clicker_instance.x1000_count}")
    x10000_lbl = ttk.Label(totals_frame, text=f"Total +10K = {clicker_instance.x10000_count}")
    x100000_lbl = ttk.Label(totals_frame, text=f"Total +100K = {clicker_instance.x100000_count}")
    x1000000_lbl = ttk.Label(totals_frame, text=f"Total +1M = {clicker_instance.x1000000_count}")
    x10000000_lbl = ttk.Label(totals_frame, text=f"Total +10M = {clicker_instance.x10000000_count}")
    x100000000_lbl = ttk.Label(totals_frame, text=f"Total +100M = {clicker_instance.x100000000_count}")
    totals_lbl = ttk.Label(totals_frame, text=f"Total Clicks = {clicker_instance.multiplier}")

    count_package = {x1_lbl: [1, 0], x10_lbl: [1, 1], x100_lbl: [1, 2], x1000_lbl: [1, 3], x10000_lbl: [1, 4],
                     x100000_lbl: [2, 0], x1000000_lbl: [2, 1], x10000000_lbl: [2, 2], x100000000_lbl: [2, 3],
                     totals_lbl: [3, 0]}


    for label, (row, col) in count_package.items():
        label.grid(row=row, column=col, pady=10, padx=30, sticky="w")

    # Header Package
    header_frame.grid(row=3, column=0, columnspan=2, pady=20, padx=10, sticky="nsew")

    # loop options
    # Button state on launch - Sets as disabled
    upgrades = [upgrade_x1, upgrade_x10, upgrade_x100, upgrade_x1000, upgrade_x10000,
                upgrade_x100000, upgrade_x1000000, upgrade_x10000000, upgrade_x100000000, auto_clicker]
    for buttons in upgrades:
        buttons.config(state="disabled")

    # key bindings
    # upgrades
    keys = {"F1": "upgrade_x1", "F2": "upgrade_x10", "F3": "upgrade_x100", "F4": "upgrade_x1000",
            "F5": "upgrade_x10000", "F6": "upgrade_x100000", "F7": "upgrade_x1000000",
            "F8": "upgrade_x10000000", "F9": "upgrade_x10000000"}
    for key, function in keys.items():
        clicker.bind(f"<{key}>", lambda event, func=function: getattr(clicker_instance, func)())


    # others
    clicker.bind("<F10>", lambda event: clicker_instance.auto_clicker_threader())
    clicker.bind("<Return>", lambda event: "break")
    clicker.bind("<Button-3>", lambda event: clicker_instance.counters())

    clicker_instance.totals()
    clicker_instance.load_file()
    clicker_instance.cooldown_threader()
    root.mainloop()
