import tkinter as tk
import ctypes
from ctypes import wintypes
import psutil
import wmi

# Windows API Constants
GWL_EXSTYLE = -20
WS_EX_TOOLWINDOW = 0x00000080
WS_EX_NOACTIVATE = 0x08000000

class DesktopWidget:
    def __init__(self):
        self.root = tk.Tk()
        
        # Initialize WMI connection for GPU metrics
        try:
            self.wmi_client = wmi.WMI(namespace="root\\CIMV2")
        except Exception:
            self.wmi_client = None
        
        # 1. Configure frameless and transparent window
        self.root.overrideredirect(True)
        self.root.config(bg='black')
        self.root.wm_attributes("-transparentcolor", "black")
        
        # 2. Position near the taskbar (Bottom Right)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        widget_width = 180
        widget_height = 100
        x = screen_width - widget_width
        y = screen_height - widget_height - 60
        self.root.geometry(f"{widget_width}x{widget_height}+{x}+{y}")

        # 3. UI Elements
        self.cpu_label = tk.Label(self.root, text="CPU: 0%", fg="#CACACA", bg="black", font=("Consolas", 12, "bold"))
        self.cpu_label.pack(anchor="w", padx=10, pady=2)
        
        self.ram_label = tk.Label(self.root, text="RAM: 0%", fg="#CACACA", bg="black", font=("Consolas", 12, "bold"))
        self.ram_label.pack(anchor="w", padx=10, pady=2)
        
        self.gpu_label = tk.Label(self.root, text="GPU: 0%", fg="#CACACA", bg="black", font=("Consolas", 12, "bold"))
        self.gpu_label.pack(anchor="w", padx=10, pady=2)

        # 4. Apply Windows-specific styles
        self.apply_windows_styles()

        # 5. Start update loop
        self.update_metrics()
        self.root.mainloop()

    def apply_windows_styles(self):
        hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
        style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        style |= WS_EX_TOOLWINDOW | WS_EX_NOACTIVATE
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
        
        HWND_BOTTOM = 1
        SWP_NOMOVE = 0x0002
        SWP_NOSIZE = 0x0001
        SWP_NOACTIVATE = 0x0010
        
        ctypes.windll.user32.SetWindowPos(
            hwnd, HWND_BOTTOM, 0, 0, 0, 0, 
            SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE
        )

    def get_gpu_usage(self):
        if not self.wmi_client:
            return 0.0
        try:
            # Query Windows Performance Counters for GPU Engine utilization
            query = "SELECT UtilizationPercentage FROM Win32_PerfFormattedData_GPUPerformanceCounters_GPUEngine WHERE Name LIKE '%engtype_3D%'"
            results = self.wmi_client.query(query)
            if results:
                # Sum up performance across engines or take the maximum active load
                return float(max(int(item.UtilizationPercentage) for item in results))
        except Exception:
            pass
        return 0.0

    def update_metrics(self):
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        gpu_usage = self.get_gpu_usage()

        self.cpu_label.config(text=f"CPU: {cpu_usage:5.1f}%")
        self.ram_label.config(text=f"RAM: {ram_usage:5.1f}%")
        self.gpu_label.config(text=f"GPU: {gpu_usage:5.1f}%")

        hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
        ctypes.windll.user32.SetWindowPos(hwnd, 1, 0, 0, 0, 0, 0x0002 | 0x0001 | 0x0010)

        self.root.after(1000, self.update_metrics)

if __name__ == "__main__":
    DesktopWidget()