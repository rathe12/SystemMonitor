import time
import psutil
from rich.console import Console
from rich.table import Table

console = Console()


def get_cpu_usage():
    return psutil.cpu_percent(interval=1)


def get_memory_usage():
    mem = psutil.virtual_memory()
    return mem.percent, mem.used, mem.total


def get_disk_usage():
    disk = psutil.disk_usage('/')
    return disk.percent, disk.used, disk.total


def display_system_info():
    table = Table(title="System Monitor")

    table.add_column("Metric", justify="left", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")

    cpu = get_cpu_usage()
    table.add_row("CPU Usage", f"{cpu}%")

    mem_percent, mem_used, mem_total = get_memory_usage()
    table.add_row(
        "Memory Usage", f"{mem_percent}% (used: {mem_used/1024**2:.2f} MB of {mem_total/1024**2:.2f} MB)")

    disk_percent, disk_used, disk_total = get_disk_usage()
    table.add_row(
        "Disk Usage", f"{disk_percent}% (used: {disk_used/1024**3:.2f} GB of {disk_total/1024**3:.2f} GB)")

    console.clear()
    console.print(table)


def main():
    while True:
        display_system_info()
        time.sleep(2)  # Обновление данных каждые 2 секунды


if __name__ == "__main__":
    main()
