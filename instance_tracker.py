import customtkinter as ctk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime, timedelta, timezone

# --- Configuration ---
DATA_FILE = "iro_instance_data.json"
SERVER_UTC_OFFSET = -8  # iRO is PST (UTC-8)

# --- Theme Settings ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# --- Full Instance Database ---
DEFAULT_INSTANCES = [
    # --- HOURLY (1 - 12 Hours) ---
    {"category": "Hourly", "name": "Malangdo Culvert", "level": "99/140", "boss": "Coelacanths", "type": "hours", "cooldown": 1},
    {"category": "Hourly", "name": "Hazy Forest", "level": "99+", "boss": "Purple Dragon", "type": "hours", "cooldown": 1.5},
    {"category": "Hourly", "name": "Octopus Cave", "level": "Unknown", "boss": "Giant Octopus", "type": "hours", "cooldown": 3},
    {"category": "Hourly", "name": "VIP Summoner", "level": "70+", "boss": "Private MVP", "type": "hours", "cooldown": 6},
    {"category": "Hourly", "name": "Sealed Shrine", "level": "75+", "boss": "Unsealed Baphomet", "type": "hours", "cooldown": 12},

    # --- DAILY (16 - 23 Hours Duration) ---
    {"category": "Daily (16h+)", "name": "Orc's Memory", "level": "60+", "boss": "Fake Orc Hero", "type": "hours", "cooldown": 16},
    {"category": "Daily (16h+)", "name": "Geffen Magic Tournament", "level": "90+", "boss": "Fenrir", "type": "hours", "cooldown": 16},
    {"category": "Daily (16h+)", "name": "Sara's Memory", "level": "99+", "boss": "Doyen Irene", "type": "hours", "cooldown": 16},
    {"category": "Daily (16h+)", "name": "Room of Consciousness", "level": "100+", "boss": "Bijou", "type": "hours", "cooldown": 16},
    {"category": "Daily (16h+)", "name": "Heart Hunter War Base 2", "level": "100+", "boss": "Ebel", "type": "hours", "cooldown": 16},
    {"category": "Daily (16h+)", "name": "Werner Laboratory", "level": "100+", "boss": "Pet Child", "type": "hours", "cooldown": 16},
    {"category": "Daily (16h+)", "name": "2nd OS Search", "level": "110+", "boss": "Miguel", "type": "hours", "cooldown": 16},
    {"category": "Daily (16h+)", "name": "Cor Memorial", "level": "110+", "boss": "EL1_A17T", "type": "hours", "cooldown": 16},
    {"category": "Daily (16h+)", "name": "Ghost Palace", "level": "120+", "boss": "Torturous Redeemer", "type": "hours", "cooldown": 16},
    {"category": "Daily (16h+)", "name": "Nightmarish Jitterbug", "level": "120+", "boss": "Awakened Ferre", "type": "hours", "cooldown": 16},
    {"category": "Daily (16h+)", "name": "Devil's Tower", "level": "130+", "boss": "Evil Fanatic", "type": "hours", "cooldown": 16},
    {"category": "Daily (16h+)", "name": "Old Glast Heim (Normal)", "level": "130+", "boss": "Root / Amdarais", "type": "hours", "cooldown": 16},
    {"category": "Daily (16h+)", "name": "Central Laboratory", "level": "140+", "boss": "3 Random MVPs", "type": "hours", "cooldown": 16},
    {"category": "Daily (16h+)", "name": "Faceworm Nest", "level": "140+", "boss": "Faceworm Queen", "type": "hours", "cooldown": 16},
    {"category": "Daily (16h+)", "name": "Horror Toy Factory", "level": "140+", "boss": "Celine Kimi", "type": "hours", "cooldown": 16},
    {"category": "Daily (16h+)", "name": "Poring Village", "level": "30-60", "boss": "King Poring", "type": "hours", "cooldown": 20},
    {"category": "Daily (16h+)", "name": "EDDA Arunafeltz", "level": "80/130", "boss": "Ktullanux", "type": "hours", "cooldown": 23},
    {"category": "Daily (16h+)", "name": "Airship Raid", "level": "125+", "boss": "Captain Ferlock", "type": "hours", "cooldown": 23},
    {"category": "Daily (16h+)", "name": "Buwaya's Cave", "level": "130+", "boss": "Buwaya", "type": "hours", "cooldown": 23},
    {"category": "Daily (16h+)", "name": "Charleston Crisis", "level": "130+", "boss": "Charleston 3", "type": "hours", "cooldown": 23},
    {"category": "Daily (16h+)", "name": "The Last Room", "level": "150+", "boss": "T_W_O", "type": "hours", "cooldown": 23},
    {"category": "Daily (16h+)", "name": "Isle of Bios", "level": "160+", "boss": "Reaper Yanku", "type": "hours", "cooldown": 23},
    {"category": "Daily (16h+)", "name": "Morse's Cave", "level": "160+", "boss": "Necromancer", "type": "hours", "cooldown": 23},
    {"category": "Daily (16h+)", "name": "Temple of Demon God", "level": "160+", "boss": "Desperate Morroc", "type": "hours", "cooldown": 23},

    # --- DAILY (Server Reset 04:00 AM) ---
    {"category": "Daily (4AM)", "name": "EDDA Fall of Glast Heim", "level": "130+", "boss": "Schmidt / King", "type": "daily_4am", "cooldown": 1},
    {"category": "Daily (4AM)", "name": "Farm Forgotten in Time", "level": "130+", "boss": "Pitaya Boss", "type": "daily_4am", "cooldown": 1},
    {"category": "Daily (4AM)", "name": "Hey, Sweetie!", "level": "130+", "boss": "Sweety", "type": "daily_4am", "cooldown": 1},
    {"category": "Daily (4AM)", "name": "Hidden Flower Garden", "level": "130+", "boss": "Red Pepper", "type": "daily_4am", "cooldown": 1},
    {"category": "Daily (4AM)", "name": "Floating Garden", "level": "130+", "boss": "Silva Papilla", "type": "daily_4am", "cooldown": 1},
    {"category": "Daily (4AM)", "name": "EDDA Biolab", "level": "170+", "boss": "Nameless Swordsman", "type": "daily_4am", "cooldown": 1},
    {"category": "Daily (4AM)", "name": "Sanctuary Purification", "level": "170+", "boss": "Normal Monsters", "type": "daily_4am", "cooldown": 1},
    {"category": "Daily (4AM)", "name": "Villa of Deception", "level": "170+", "boss": "Schulang / Freyja", "type": "daily_4am", "cooldown": 1},
    {"category": "Daily (4AM)", "name": "Hidden Flower (Hard)", "level": "180+", "boss": "Senior Red Pepper", "type": "daily_4am", "cooldown": 1},
    {"category": "Daily (4AM)", "name": "Floating Garden (Hard)", "level": "180+", "boss": "Grand Papillia", "type": "daily_4am", "cooldown": 1},
    {"category": "Daily (4AM)", "name": "Memories of Thanatos", "level": "180+", "boss": "Thanatos", "type": "daily_4am", "cooldown": 1},
    {"category": "Daily (4AM)", "name": "Tomb of Remorse", "level": "220+", "boss": "Tiara / Sakray", "type": "daily_4am", "cooldown": 1},
    {"category": "Daily (4AM)", "name": "Constellation Tower", "level": "240+", "boss": "Betelgeuse", "type": "daily_4am", "cooldown": 1},

    # --- 3 DAYS ---
    {"category": "3 Days", "name": "Sunken Tower", "level": "40+", "boss": "Various", "type": "days_3", "cooldown": 3},
    {"category": "3 Days", "name": "Nidhoggur's Nest", "level": "70+", "boss": "Shadow", "type": "days_3", "cooldown": 3},
    {"category": "3 Days", "name": "Wolfchev's Laboratory", "level": "145+", "boss": "Biolab MVPs", "type": "days_3", "cooldown": 3},
    {"category": "3 Days", "name": "Sky Fortress", "level": "145+", "boss": "Stefan Wolf", "type": "days_3", "cooldown": 3},
    {"category": "3 Days", "name": "Adv. Old Glast Heim", "level": "160+", "boss": "Root H / Amdarais H", "type": "days_3", "cooldown": 3},
    {"category": "3 Days", "name": "Challenge Old Glast Heim", "level": "170+", "boss": "Phantom Amdarais", "type": "days_3", "cooldown": 3},
    {"category": "3 Days", "name": "EDDA Fall of GH (Adv)", "level": "170+", "boss": "Schmidt / King", "type": "days_3", "cooldown": 3},
    {"category": "3 Days", "name": "Airship Crash", "level": "200+", "boss": "Unknown", "type": "days_3", "cooldown": 3},
    {"category": "3 Days", "name": "Geffen Night Arena", "level": "210+", "boss": "Midnight Fenrir", "type": "days_3", "cooldown": 3},

    # --- WEEKLY (7 Days / Specific Days) ---
    {"category": "Weekly", "name": "Endless Tower", "level": "50+", "boss": "Naght Sieger", "type": "weekly_tue", "cooldown": 7},
    {"category": "Weekly", "name": "Bangungot's Instance", "level": "100+", "boss": "Bangungot", "type": "weekly_tue", "cooldown": 7},
    {"category": "Weekly", "name": "Bakonawa Extermination", "level": "140+", "boss": "Bakonawa", "type": "weekly_tue", "cooldown": 7},
    {"category": "Weekly", "name": "Sarah and Fenrir", "level": "145+", "boss": "Sarah Irene", "type": "weekly_tue", "cooldown": 7},
    {"category": "Weekly", "name": "Beginner Old Glast Heim", "level": "65+", "boss": "Bloody Knight", "type": "weekly_tue", "cooldown": 7},
    {"category": "Weekly", "name": "Friday Instance", "level": "99+", "boss": "Lich Lord", "type": "weekly_fri", "cooldown": 7},
    {"category": "Weekly", "name": "Weekend Instance", "level": "60+", "boss": "None", "type": "weekly_fri", "cooldown": 7},
]

class IROTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("iRO Instance Tracker v9.1 (Fixed)")
        self.geometry("1450x850")
        
        self.server_tz = timezone(timedelta(hours=SERVER_UTC_OFFSET))
        
        self.data = self.load_data()
        self.selected_account = None
        self.selected_char = None
        
        # PERFORMANCE: Widget Recycling Maps
        self.widgets_map = {} 
        self.fav_widgets_map = {} 
        
        self.setup_ui()
        self.update_timers()

    def get_server_time(self):
        return datetime.now(timezone.utc).astimezone(self.server_tz)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_data(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.data, f, indent=4)

    def get_char_instance_data(self, instance_name):
        if not self.selected_char: return {"time": None, "count": 0, "fav": False}
        raw_data = self.data[self.selected_account][self.selected_char].get(instance_name)
        
        if raw_data is None: return {"time": None, "count": 0, "fav": False}
        if isinstance(raw_data, str): # Migration
            new_data = {"time": raw_data, "count": 1, "fav": False}
            self.data[self.selected_account][self.selected_char][instance_name] = new_data
            return new_data
        return raw_data

    def set_char_instance_data(self, instance_name, new_data_dict):
        self.data[self.selected_account][self.selected_char][instance_name] = new_data_dict
        self.save_data()

    def setup_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)

        self.logo = ctk.CTkLabel(self.sidebar, text="iRO Tracker", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo.grid(row=0, column=0, padx=20, pady=(30, 20))

        self.btn_acc = ctk.CTkButton(self.sidebar, text="+ Account", command=self.add_account)
        self.btn_acc.grid(row=1, column=0, padx=20, pady=10)
        self.btn_char = ctk.CTkButton(self.sidebar, text="+ Character", command=self.add_character)
        self.btn_char.grid(row=2, column=0, padx=20, pady=10)
        self.btn_del = ctk.CTkButton(self.sidebar, text="- Delete", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.delete_entry)
        self.btn_del.grid(row=3, column=0, padx=20, pady=10)

        self.tree_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.tree_frame.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
        
        self.tree = ttk.Treeview(self.tree_frame, show="tree", selectmode="browse")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select_tree)
        
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", borderwidth=0, font=('Arial', 12))
        style.map('Treeview', background=[('selected', '#1f538d')], foreground=[('selected', 'white')])

        # --- Main Area ---
        self.right_area = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.right_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.right_area.grid_rowconfigure(2, weight=1)
        self.right_area.grid_columnconfigure(0, weight=1)

        self.top_bar = ctk.CTkFrame(self.right_area, fg_color="transparent")
        self.top_bar.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        self.lbl_title = ctk.CTkLabel(self.top_bar, text="Select a Character", font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_title.pack(side="left")
        
        self.btn_reset_all = ctk.CTkButton(self.top_bar, text="Reset All", fg_color="#C0392B", hover_color="#E74C3C", width=100, command=self.reset_all_instances)
        self.btn_reset_all.pack(side="left", padx=20)
        self.btn_reset_all.configure(state="disabled")

        self.lbl_clock = ctk.CTkLabel(self.top_bar, text="Loading...", font=ctk.CTkFont(size=16), text_color="#3B8ED0")
        self.lbl_clock.pack(side="right")

        # Tabs
        self.tabs = ctk.CTkTabview(self.right_area)
        self.tabs.grid(row=2, column=0, sticky="nsew")
        
        self.tab_names = ["Favorites", "Hourly", "Daily (4AM)", "Daily (16h+)", "3 Days", "Weekly"]
        for t in self.tab_names:
            self.tabs.add(t)
        
        # Build widgets once
        self.build_widgets_once()
        self.refresh_tree()

    def build_widgets_once(self):
        """Constructs all instance rows once and keeps them in memory."""
        headers = ["Fav", "Instance", "Runs", "Level", "Boss", "Status", "Action"]
        col_weights = [0, 2, 1, 1, 2, 1, 1]

        # 1. Standard Tabs
        for tab_name in self.tab_names:
            if tab_name == "Favorites": continue

            parent = self.tabs.tab(tab_name)
            for i, w in enumerate(col_weights):
                parent.grid_columnconfigure(i, weight=w)
            for col, text in enumerate(headers):
                ctk.CTkLabel(parent, text=text, font=ctk.CTkFont(weight="bold")).grid(row=0, column=col, padx=5, pady=10, sticky="w")

            tab_instances = [i for i in DEFAULT_INSTANCES if i.get("category") == tab_name]
            for i, inst in enumerate(tab_instances):
                r = i + 1
                self.create_row_widgets(parent, inst, r, self.widgets_map)

        # 2. Favorites Tab (Hidden initially)
        fav_parent = self.tabs.tab("Favorites")
        for i, w in enumerate(col_weights):
            fav_parent.grid_columnconfigure(i, weight=w)
        for col, text in enumerate(headers):
            ctk.CTkLabel(fav_parent, text=text, font=ctk.CTkFont(weight="bold")).grid(row=0, column=col, padx=5, pady=10, sticky="w")
        
        for i, inst in enumerate(DEFAULT_INSTANCES):
            r = i + 1
            self.create_row_widgets(fav_parent, inst, r, self.fav_widgets_map)
            # Hide initially - iterate over the widgets dict values
            for w in self.fav_widgets_map[inst["name"]].values():
                if isinstance(w, (ctk.CTkLabel, ctk.CTkButton)): # Only hide actual UI elements
                    w.grid_remove()

    def create_row_widgets(self, parent, inst, row, storage_map):
        name = inst["name"]
        
        btn_fav = ctk.CTkButton(parent, text="?", width=30, height=30, fg_color="transparent", text_color="yellow", font=ctk.CTkFont(size=20), hover_color="#444")
        btn_fav.configure(command=lambda n=name: self.toggle_favorite(n))
        btn_fav.grid(row=row, column=0, padx=2, pady=5)
        
        lbl_name = ctk.CTkLabel(parent, text=name)
        lbl_name.grid(row=row, column=1, padx=5, pady=5, sticky="w")

        lbl_runs = ctk.CTkLabel(parent, text="Runs: 0", text_color="gray")
        lbl_runs.grid(row=row, column=2, padx=5, pady=5, sticky="w")

        lbl_lvl = ctk.CTkLabel(parent, text=inst["level"], text_color="gray")
        lbl_lvl.grid(row=row, column=3, padx=5, pady=5, sticky="w")

        lbl_boss = ctk.CTkLabel(parent, text=inst["boss"])
        lbl_boss.grid(row=row, column=4, padx=5, pady=5, sticky="w")

        lbl_status = ctk.CTkLabel(parent, text="...", width=100)
        lbl_status.grid(row=row, column=5, padx=5, pady=5)

        btn_action = ctk.CTkButton(parent, text="Mark Done", width=80, height=25)
        btn_action.grid(row=row, column=6, padx=5, pady=5)

        storage_map[name] = {
            "data": inst,
            "btn_fav": btn_fav,
            "lbl_name": lbl_name,
            "lbl_runs": lbl_runs,
            "lbl_lvl": lbl_lvl,
            "lbl_boss": lbl_boss,
            "lbl_status": lbl_status,
            "btn_action": btn_action
        }

    # --- Standard Logic ---
    def refresh_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for acc, chars in self.data.items():
            node = self.tree.insert("", "end", text=f"📂 {acc}", open=True, values=("account",))
            for char in chars:
                self.tree.insert(node, "end", text=f"   👤 {char}", values=("character",))

    def add_account(self):
        name = simpledialog.askstring("New", "Account Name:")
        if name and name not in self.data:
            self.data[name] = {}
            self.save_data()
            self.refresh_tree()

    def add_character(self):
        sel = self.tree.selection()
        if not sel: return
        item = self.tree.item(sel[0])
        acc = item['text'].replace("📂 ", "") if item['values'][0] == "account" else self.tree.item(self.tree.parent(sel[0]))['text'].replace("📂 ", "")
        if len(self.data[acc]) >= 9: return
        name = simpledialog.askstring("New", "Character Name:")
        if name and name not in self.data[acc]:
            self.data[acc][name] = {}
            self.save_data()
            self.refresh_tree()

    def delete_entry(self):
        sel = self.tree.selection()
        if not sel: return
        item = self.tree.item(sel[0])
        name = item['text'].replace("📂 ", "").replace("   👤 ", "")
        if messagebox.askyesno("Confirm", f"Delete {name}?"):
            if item['values'][0] == "account": del self.data[name]
            else: del self.data[self.tree.item(self.tree.parent(sel[0]))['text'].replace("📂 ", "")][name]
            self.save_data()
            self.refresh_tree()

    def on_select_tree(self, event):
        sel = self.tree.selection()
        if not sel: return
        item = self.tree.item(sel[0])
        if item['values'][0] == "character":
            self.selected_account = self.tree.item(self.tree.parent(sel[0]))['text'].replace("📂 ", "")
            self.selected_char = item['text'].replace("   👤 ", "")
            self.btn_reset_all.configure(state="normal")
            self.update_single_char_ui()
        else:
            self.btn_reset_all.configure(state="disabled")

    def toggle_favorite(self, instance_name):
        current = self.get_char_instance_data(instance_name)
        current["fav"] = not current["fav"]
        self.set_char_instance_data(instance_name, current)
        self.update_single_char_ui()

    def mark_done(self, instance_name):
        current = self.get_char_instance_data(instance_name)
        current["time"] = self.get_server_time().isoformat()
        current["count"] = current.get("count", 0) + 1
        self.set_char_instance_data(instance_name, current)
        self.update_single_char_ui()

    def reset_instance(self, instance_name):
        if messagebox.askyesno("Reset", f"Reset {instance_name}?"):
            current = self.get_char_instance_data(instance_name)
            current["time"] = None
            self.set_char_instance_data(instance_name, current)
            self.update_single_char_ui()

    def reset_all_instances(self):
        if not self.selected_char: return
        if messagebox.askyesno("Reset All", "Reset all timers?"):
            char_d = self.data[self.selected_account][self.selected_char]
            for key in char_d:
                if isinstance(char_d[key], dict): char_d[key]["time"] = None
            self.save_data()
            self.update_single_char_ui()

    def get_reset_time(self, inst, last_done):
        itype, cd = inst["type"], inst["cooldown"]
        if itype == "hours": return last_done + timedelta(hours=cd)
        if itype == "daily_4am":
            reset = last_done.replace(hour=4, minute=0, second=0, microsecond=0)
            if last_done >= reset: reset += timedelta(days=1)
            return reset
        if itype == "days_3":
            target = last_done + timedelta(days=cd)
            reset = target.replace(hour=4, minute=0, second=0, microsecond=0)
            if target >= reset: reset += timedelta(days=1)
            return reset
        if itype.startswith("weekly"):
            d = 1
            if itype == "weekly_mon": d = 0
            if itype == "weekly_fri": d = 4
            reset = last_done.replace(hour=4, minute=0, second=0, microsecond=0)
            while reset <= last_done or reset.weekday() != d: reset += timedelta(days=1)
            return reset
        return self.get_server_time()

    def update_single_char_ui(self):
        if not self.selected_char: return
        self.lbl_title.configure(text=f"Instances: {self.selected_char}")
        now = self.get_server_time()
        
        # 1. Update Standard Tabs
        for name, widgets in self.widgets_map.items():
            self.update_row_visuals(name, widgets, now)

        # 2. Update Favorites Tab
        for name, widgets in self.fav_widgets_map.items():
            db_data = self.get_char_instance_data(name)
            is_fav = db_data.get("fav", False)
            
            # Show/Hide Logic
            if is_fav:
                for key, w in widgets.items():
                    if key != "data": w.grid() # Only show widgets
                self.update_row_visuals(name, widgets, now)
            else:
                for key, w in widgets.items():
                    if key != "data": w.grid_remove() # Only hide widgets

    def update_row_visuals(self, name, widgets, now):
        db_data = self.get_char_instance_data(name)
        inst_def = widgets["data"]
        
        # Fav Icon
        widgets["btn_fav"].configure(text="★" if db_data.get("fav") else "☆")
        
        # Run Count
        widgets["lbl_runs"].configure(text=f"Runs: {db_data.get('count', 0)}")
        
        # Timer / Status
        last_str = db_data.get("time")
        if last_str:
            try:
                reset = self.get_reset_time(inst_def, datetime.fromisoformat(last_str))
                if now < reset:
                    rem = reset - now
                    d, rem = divmod(int(rem.total_seconds()), 86400)
                    h, rem = divmod(rem, 3600)
                    m, _ = divmod(rem, 60)
                    widgets["lbl_status"].configure(text=f"{d}d {h:02}:{m:02}", text_color="#FF5555")
                    widgets["btn_action"].configure(text="Reset", fg_color="#C0392B", hover_color="#E74C3C",
                                                  command=lambda n=name: self.reset_instance(n))
                else:
                    widgets["lbl_status"].configure(text="Ready", text_color="#50FA7B")
                    widgets["btn_action"].configure(text="Mark Done", fg_color="#3B8ED0", hover_color="#36719F",
                                                  command=lambda n=name: self.mark_done(n))
            except: pass
        else:
            widgets["lbl_status"].configure(text="Ready", text_color="#50FA7B")
            widgets["btn_action"].configure(text="Mark Done", fg_color="#3B8ED0", hover_color="#36719F",
                                          command=lambda n=name: self.mark_done(n))

    def update_timers(self):
        self.lbl_clock.configure(text=f"Server Time: {self.get_server_time().strftime('%Y-%m-%d %H:%M:%S')}")
        if self.selected_char: self.update_single_char_ui()
        self.after(1000, self.update_timers)

if __name__ == "__main__":
    app = IROTrackerApp()
    app.mainloop()