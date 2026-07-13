class AdvancedWaterLevelSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Automated Water Level Indicator & Controller")
        self.root.geometry("500x650")
        self.root.configure(bg="#1e1e2e") # Modern Dark Theme

        # Project Variables
        self.water_level = 30.0  # Initial Level in %
        self.pump_status = False # False = OFF, True = ON
        self.auto_mode = True    # Automation ON by default
        self.simulation_speed = 100 #ms

        # UI Styling Setup
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Main Layout Setup
        self.create_widgets()
        
        # Start the Background Real-time Simulation Loop
        self.run_simulation()

    def create_widgets(self):
        # 1. Header Title
        title = tk.Label(self.root, text="HYDRO-SIM v1.0", font=("Helvetica", 20, "bold"), bg="#1e1e2e", fg="#cdd6f4")
        title.pack(pady=15)

        subtitle = tk.Label(self.root, text="Automated Software Simulation Project", font=("Helvetica", 10, "italic"), bg="#1e1e2e", fg="#a6adc8")
        subtitle.pack(pady=2)

        # 2. Main Display Canvas for Water Tank
        # Tank Container Dimensions: Width=160, Height=300
        self.canvas = tk.Canvas(self.root, width=180, height=320, bg="#313244", highlightthickness=3, highlightbackground="#45475a")
        self.canvas.pack(pady=20)

        # 3. Dynamic Telemetry Data Labels
        self.lbl_percentage = tk.Label(self.root, text="Level: 30.0%", font=("Helvetica", 14, "bold"), bg="#1e1e2e", fg="#f5c2e7")
        self.lbl_percentage.pack()

        self.lbl_pump = tk.Label(self.root, text="PUMP STATUS: OFF", font=("Helvetica", 12, "bold"), bg="#1e1e2e", fg="#f38ba8")
        self.lbl_pump.pack(pady=5)

        # 4. Control Panel Frame
        control_frame = tk.LabelFrame(self.root, text=" Control Desk ", bg="#1e1e2e", fg="#cdd6f4", font=("Helvetica", 10, "bold"), padx=15, pady=15)
        control_frame.pack(pady=15, fill="x", padx=30)

        # Toggle Automation Switch Button
        self.btn_auto = tk.Button(control_frame, text="Auto Mode: ON", font=("Helvetica", 10, "bold"), bg="#a6e3a1", fg="#11111b", width=15, command=self.toggle_auto_mode)
        self.btn_auto.grid(row=0, column=0, padx=10, pady=5)

        # Manual Pump Trigger Button
        self.btn_pump = tk.Button(control_frame, text="Toggle Pump Manually", font=("Helvetica", 10, "bold"), bg="#89b4fa", fg="#11111b", width=20, state="disabled", command=self.toggle_pump_manual)
        self.btn_pump.grid(row=0, column=1, padx=10, pady=5)

        # 5. Live Activity Logs Terminal
        log_frame = tk.Frame(self.root, bg="#11111b")
        log_frame.pack(fill="both", expand=True, padx=30, pady=10)
        
        self.log_box = tk.Text(log_frame, height=5, bg="#11111b", fg="#a6e3a1", font=("Courier", 9), state="disabled")
        self.log_box.pack(fill="both", expand=True)
        self.log_message("System Initialized. Auto-Controller Active.")

    def log_message(self, message):
        """Helper to push live telemetry data into the GUI terminal console."""
        self.log_box.config(state="normal")
        self.log_box.insert(tk.END, f">> {message}\n")
        self.log_box.see(tk.END)
        self.log_box.config(state="disabled")

    def toggle_auto_mode(self):
        self.auto_mode = not self.auto_mode
        if self.auto_mode:
            self.btn_auto.config(text="Auto Mode: ON", bg="#a6e3a1")
            self.btn_pump.config(state="disabled")
            self.log_message("Switched to AUTOMATIC Control Mode.")
        else:
            self.btn_auto.config(text="Auto Mode: OFF", bg="#f38ba8")
            self.btn_pump.config(state="normal")
            self.log_message("Switched to MANUAL Control Mode.")

    def toggle_pump_manual(self):
        if not self.auto_mode:
            self.pump_status = not self.pump_status
            status_str = "ON" if self.pump_status else "OFF"
            self.log_message(f"Manual Override: Pump turned {status_str}")

    def run_simulation(self):
        """Core mathematical loop tracking physical flow dynamics."""
        # 1. Automatic Controller Logic (Emulating hardware microcontrollers)
        if self.auto_mode:
            if self.water_level <= 15.0 and not self.pump_status:
                self.pump_status = True
                self.log_message("[ALERT] Low Level Trigger! Turning Pump ON.")
                messagebox.showinfo("Auto Controller", "Water Level critical (<15%). Pump started automatically!")
            elif self.water_level >= 95.0 and self.pump_status:
                self.pump_status = False
                self.log_message("[ALERT] Max Capacity Reached! Turning Pump OFF.")
                messagebox.showwarning("Auto Controller", "Tank Full (>95%). Pump shutdown executed to prevent overflow!")

        # 2. Simulate Water Consumption / Drain Rate (Random minor usage drops)
        drain_rate = random.uniform(0.05, 0.15)
        self.water_level -= drain_rate

        # 3. Simulate Pump Output Rate (Inflow speed minus continuous drain speed)
        if self.pump_status:
            inflow_rate = random.uniform(0.35, 0.55)
            self.water_level += inflow_rate

        # Boundary constraints check (Strictly cap between 0 and 100)
        self.water_level = max(0.0, min(100.0, self.water_level))

        # 4. Refresh Graphics & GUI State
        self.update_tank_ui()

        # Infinite loop trigger via Tkinter event loop scheduler
        self.root.after(self.simulation_speed, self.run_simulation)

    def update_tank_ui(self):
        # Clear frame for next frame rendering step
        self.canvas.delete("fluid")

        # Map percentage parameters to pixel arrays
        # Max canvas height window bound tracking is 320px
        tank_padding = 10
        usable_height = 320 - (2 * tank_padding)
        
        water_height_pixels = (self.water_level / 100.0) * usable_height
        y_top = 310 - water_height_pixels

        # Dynamic Color Palette Selection Architecture
        if self.water_level <= 20.0:
            fluid_color = "#f38ba8" # Warning Red
            self.lbl_percentage.config(fg="#f38ba8")
        elif self.water_level >= 85.0:
            fluid_color = "#a6e3a1" # System Safe Green
            self.lbl_percentage.config(fg="#a6e3a1")
        else:
            fluid_color = "#89b4fa" # Standard Aqua Blue
            self.lbl_percentage.config(fg="#89b4fa")

        # Render fluid vectors
        self.canvas.create_rectangle(10, y_top, 170, 310, fill=fluid_color, outline="", tags="fluid")

        # Update text sensors
        self.lbl_percentage.config(text=f"Level: {self.water_level:.1f}%")
        
        if self.pump_status:
            self.lbl_pump.config(text="PUMP STATUS: ON (FILLING)", fg="#a6e3a1")
        else:
            self.lbl_pump.config(text="PUMP STATUS: OFF (DRAINING)", fg="#f38ba8")

if __name__ == "__main__":
    window = tk.Tk()
    app = AdvancedWaterLevelSimulator(window)
    window.mainloop()