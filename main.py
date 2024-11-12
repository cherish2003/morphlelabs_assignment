from flask import Flask
import os
import psutil
from datetime import datetime
import pytz

app = Flask(__name__)

@app.route('/htop')
def htop():
    full_name = "Polu Siva Sai Cherish"
    
    system_username = os.getlogin()
    
    ist = pytz.timezone('Asia/Kolkata')
    server_time = datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S %Z%z')
    
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage('/')
    processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent']):
        try:
            proc_info = proc.info
            if proc_info['cpu_percent'] is not None:
                processes.append(proc_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    top_processes = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:5]

    response = f"""
    <html>
        <head><title>HTop Information</title></head>
        <body>
            <h1>HTop Endpoint</h1>
            <p><b>Name:</b> {full_name}</p>
            <p><b>Username:</b> {system_username}</p>
            <p><b>Server Time (IST):</b> {server_time}</p>
            <h2>System Stats:</h2>
            <p><b>CPU Usage:</b> {cpu_percent}%</p>
            <p><b>Memory Usage:</b> {memory_info.percent}%</p>
            <p><b>Disk Usage:</b> {disk_info.percent}%</p>
            <h2>Top Processes (by CPU usage):</h2>
            <pre>
            {"PID".ljust(8)}{"Name".ljust(20)}{"Username".ljust(15)}{"CPU (%)"}
            {'-'*50}
    """
    for proc in top_processes:
        response += f"{str(proc['pid']).ljust(8)}{proc['name'][:20].ljust(20)}{proc['username'][:15].ljust(15)}{proc['cpu_percent']}\n"

    response += "</pre></body></html>"
    
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
