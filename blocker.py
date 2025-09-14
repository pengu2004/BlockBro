import time, sys, os, signal
from datetime import datetime, timedelta
import psutil

# configure
BROWSERS = ["chrome", "chrome.exe", "firefox", "firefox.exe",
            "msedge", "msedge.exe", "brave", "brave.exe", "opera", "opera.exe", "safari","comet"]
EMERGENCY_FILE = r"C:\allow_browsing" if os.name == "nt" else "/tmp/allowbrowsing"

def kill_browser_procs():
    killed = []
    for p in psutil.process_iter(["pid","name","exe","cmdline"]):
        try:
            name = (p.info["name"] or "").lower()
            if any(b in name for b in BROWSERS):
                p.kill()
                killed.append((p.pid, name))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return killed

def main(minutes):
    end = datetime.now() + timedelta(minutes=minutes)
    print(f"Blocking browsers until {end.isoformat()} (or create {EMERGENCY_FILE} to stop). Run as admin/root.")
    try:
        while datetime.now() < end:
            if os.path.exists(EMERGENCY_FILE):
                print("Emergency override detected. Exiting.")
                return
            killed = kill_browser_procs()
            if killed:
                print("Killed:", killed)
            time.sleep(1.5)
        print("Timer expired. Browsing allowed.")
    except KeyboardInterrupt:
        print("Interrupted by user — exiting.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python blocker.py <minutes>")
        sys.exit(1)
    main(int(sys.argv[1]))