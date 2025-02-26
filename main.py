import time
import psutil
import argparse
import json
import os
from datetime import datetime
from rich.console import Console
from rich.table import Table

# Версия программы
VERSION = "1.0.0"

console = Console()


def get_cpu_usage():
    return psutil.cpu_percent(interval=1)


def get_memory_usage():
    mem = psutil.virtual_memory()
    return mem.percent, mem.used, mem.total


def get_disk_usage():
    disk = psutil.disk_usage('/')
    return disk.percent, disk.used, disk.total


def get_network_usage():
    net1 = psutil.net_io_counters()
    time.sleep(1)
    net2 = psutil.net_io_counters()

    download_speed = (net2.bytes_recv - net1.bytes_recv) / 1024
    upload_speed = (net2.bytes_sent - net1.bytes_sent) / 1024

    return download_speed, upload_speed


def log_data(data):
    """Функция логирования данных в JSON с таймстампами и сохранением в папку logs/."""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)  # Создаём папку, если её нет

    log_file = os.path.join(
        log_dir, f"logs-{datetime.now().strftime('%Y-%m-%d')}.json")

    # Добавляем timestamp в данные
    data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with open(log_file, "r", encoding="utf-8") as file:
            logs = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []

    logs.append(data)

    with open(log_file, "w", encoding="utf-8") as file:
        json.dump(logs, file, indent=4, ensure_ascii=False)

    print(f"Log saved to {log_file}")  # Сообщаем, куда сохраняется лог


def display_system_info(show_network, log_enabled, threshold, stop_on_threshold):
    table = Table(title="System Monitor")

    table.add_column("Metric", justify="left", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")

    cpu = get_cpu_usage()
    mem_percent, mem_used, mem_total = get_memory_usage()
    disk_percent, disk_used, disk_total = get_disk_usage()

    # Определяем цвет CPU
    if cpu > 80:
        cpu_color = "red"
    elif cpu > 50:
        cpu_color = "yellow"
    else:
        cpu_color = "green"

    # Определяем цвет памяти
    if mem_percent > 90:
        mem_color = "red"
    elif mem_percent > 70:
        mem_color = "yellow"
    else:
        mem_color = "green"

    data = {
        "CPU Usage (%)": cpu,
        "Memory Usage (%)": mem_percent,
        "Memory Used (MB)": round(mem_used / 1024**2, 2),
        "Memory Total (MB)": round(mem_total / 1024**2, 2),
        "Disk Usage (%)": disk_percent,
        "Disk Used (GB)": round(disk_used / 1024**3, 2),
        "Disk Total (GB)": round(disk_total / 1024**3, 2),
    }

    table.add_row("CPU Usage", f"[{cpu_color}]{cpu}%[/]")
    table.add_row(
        "Memory Usage", f"[{mem_color}]{mem_percent}%[/] (used: {data['Memory Used (MB)']} MB of {data['Memory Total (MB)']} MB)")
    table.add_row(
        "Disk Usage", f"{disk_percent}% (used: {data['Disk Used (GB)']} GB of {data['Disk Total (GB)']} GB)")

    if show_network:
        download_speed, upload_speed = get_network_usage()
        data["Download Speed (KB/s)"] = round(download_speed, 2)
        data["Upload Speed (KB/s)"] = round(upload_speed, 2)
        table.add_row("Download Speed", f"{download_speed:.2f} KB/s")
        table.add_row("Upload Speed", f"{upload_speed:.2f} KB/s")

    console.clear()
    console.print(table)

    # Проверяем превышение порога
    if threshold:
        if cpu > threshold or mem_percent > threshold:
            console.print(
                f"[red]Warning! CPU or RAM usage exceeded {threshold}%![/]")

            if stop_on_threshold:
                console.print(
                    "[bold red]Threshold exceeded! Stopping program.[/]")
                exit(0)  # Завершаем программу

    # Логируем данные, если включено логирование
    if log_enabled:
        log_data(data)


def main():
    parser = argparse.ArgumentParser(
        description="System Monitor CLI - A simple system monitoring tool.",
        epilog="Example usage: python main.py --interval 5 --no-network --log --threshold 80"
    )

    parser.add_argument("--interval", type=int, default=2,
                        help="Interval between updates in seconds")
    parser.add_argument("--no-network", action="store_true",
                        help="Disable network monitoring")
    parser.add_argument("--once", action="store_true",
                        help="Run only once and exit")
    parser.add_argument("--version", action="store_true",
                        help="Show program version and exit")
    parser.add_argument("--log", action="store_true",
                        help="Enable logging to a JSON file (logs-YYYY-MM-DD.json)")
    parser.add_argument("--threshold", type=int,
                        help="Set CPU/RAM usage warning threshold (%)")
    parser.add_argument("--stop-on-threshold", action="store_true",
                        help="Stop program if threshold is exceeded")

    args = parser.parse_args()

    if args.version:
        print(f"System Monitor CLI, version {VERSION}")
        return

    log_enabled = args.log  # Включаем логирование, если передан --log

    if args.once:
        display_system_info(not args.no_network, log_enabled,
                            args.threshold, args.stop_on_threshold)
    else:
        while True:
            display_system_info(not args.no_network, log_enabled,
                                args.threshold, args.stop_on_threshold)
            time.sleep(args.interval)


if __name__ == "__main__":
    main()
