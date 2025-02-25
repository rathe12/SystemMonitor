import psutil
from rich.console import Console
from rich.table import Table

# Функция для получения загрузки CPU
def get_cpu_usage():
    # interval=1 означает, что psutil будет измерять за 1 секунду
    return psutil.cpu_percent(interval=1)

# Функция для получения информации об оперативной памяти
def get_memory_usage():
    mem = psutil.virtual_memory()
    # Возвращаем процент использования, использованную и общую память
    return mem.percent, mem.used, mem.total

# Функция для получения информации о диске
def get_disk_usage():
    # Получаем информацию по корневому разделу
    disk = psutil.disk_usage('/')
    return disk.percent, disk.used, disk.total

def main():
    # Создаём объект консоли из rich для красивого вывода
    console = Console()

    # Создаем таблицу с заголовком "System Monitor"
    table = Table(title="System Monitor")
    
    # Добавляем колонки в таблицу
    table.add_column("Metric", justify="left", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")

    # Получаем данные по CPU и добавляем строку в таблицу
    cpu = get_cpu_usage()
    table.add_row("CPU Usage", f"{cpu}%")
    
    # Получаем данные по памяти
    mem_percent, mem_used, mem_total = get_memory_usage()
    # Преобразуем байты в мегабайты (MB) для удобства
    table.add_row("Memory Usage", f"{mem_percent}% (used: {mem_used/1024**2:.2f} MB of {mem_total/1024**2:.2f} MB)")
    
    # Получаем данные по диску
    disk_percent, disk_used, disk_total = get_disk_usage()
    # Преобразуем байты в гигабайты (GB)
    table.add_row("Disk Usage", f"{disk_percent}% (used: {disk_used/1024**3:.2f} GB of {disk_total/1024**3:.2f} GB)")
    
    # Выводим таблицу в консоль
    console.print(table)

if __name__ == "__main__":
    main()
