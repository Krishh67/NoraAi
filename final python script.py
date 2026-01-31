import psutil
import time
import win32gui
import win32process
from google.cloud import firestore
import datetime

# Initialize Firestore
db = firestore.Client.from_service_account_json("nora--x-firebase-adminsdk-fbsvc-82b89ee05d.json")


def get_active_window_info():
    try:
        hwnd = win32gui.GetForegroundWindow()
        pid = win32process.GetWindowThreadProcessId(hwnd)[1]
        process = psutil.Process(pid)
        process_name = process.name()
        window_title = win32gui.GetWindowText(hwnd)
        return process_name, window_title
    except Exception as e:
        return "Unknown", f"Error: {e}"

def get_running_apps():
    running_apps = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            cpu = proc.cpu_percent(interval=None)
            info = proc.info
            info['cpu_percent'] = cpu
            if info['name'] in [
                "Dell.TechHub.Instrumentation.SubAgent.exe",
                "DellSupportAssistRemedationService.exe",
                "RazerCentralService.exe",
                "svchost.exe",
                "System Idle Process",
                "System",
                ""
            ]:
                continue
            running_apps.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return running_apps

def main():
    while True:
        # safely warm-up CPU stats
        for proc in psutil.process_iter():
            try:
                proc.cpu_percent(interval=None)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        time.sleep(0.1)

        process_name, window_title = get_active_window_info()
        apps = get_running_apps()
        apps_sorted = sorted(apps, key=lambda x: x['cpu_percent'], reverse=True)
        
        snapshot = {
            "active_app": process_name,
            "active_title": window_title,
            "top_processes": [],
            "current_time": datetime.datetime.now().isoformat()
        }
        
        for app in apps_sorted[:5]:
            snapshot["top_processes"].append({
                "pid": app['pid'],
                "name": app['name'],
                "cpu": app['cpu_percent']
            })
        
        # Push to Firestore
        db.collection('activity').add(snapshot)
        print("✅ Data pushed to Firestore.")
        
        
        #print(snapshot)
        
        time.sleep(15)

if __name__ == "__main__":
    main()
