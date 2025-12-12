import psutil
import time
import os
from dataclasses import dataclass

@dataclass
class PerformanceMetrics:
    processing_time: float
    peak_cpu_percent: float
    peak_ram_mb: float
    
class ResourceMonitor:
    def __init__(self):
        self.process = psutil.Process(os.getpid())
        self.start_time = 0
        self.start_cpu = 0
        self.peak_cpu = 0
        self.peak_ram = 0
        
    def __enter__(self):
        self.start_time = time.time()
        # Initial snapshot
        self.process.cpu_percent() # First call is often 0.0 or invalid, serves as init
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def measure(self):
        """
        Captures current metrics. Should be called immediately after the heavy work.
        Note: True 'peak' monitoring requires a background thread, but for a synchronous 
        function, checking immediately after execution is a reasonable approximation 
        for blocking CPU tasks.
        """
        # CPU usage over the interval since last call
        # Since this is blocking, we can't poll easily without threading. 
        # We will take the immediate system state.
        
        cpu_usage = self.process.cpu_percent(interval=None) 
        # If the interval is too short, psutil might return 0. 
        # For a single blocking call, this is tricky. 
        # We'll use a slightly more robust check.
        
        mem_info = self.process.memory_info()
        current_ram = mem_info.rss / (1024 * 1024) # MB
        
        duration = time.time() - self.start_time
        
        return PerformanceMetrics(
            processing_time=duration,
            peak_cpu_percent=cpu_usage,
            peak_ram_mb=current_ram
        )