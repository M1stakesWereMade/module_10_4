import threading
from queue import Queue
import time
import random

class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None

class Guest(threading.Thread):
    def __init__(self, name, table_number):
        super().__init__()
        self.name = name
        self.table_number = table_number
        self.is_running = False

    def is_running(self):
        return self.is_running

    def run(self):
        self.is_running = True
        print(f"{self.name} сел(-а) за стол номер {self.table_number}")
        time.sleep(random.randint(3, 10))
        print(f"{self.name} покушал(-а) и ушёл(ушла)")
        self.is_running = False

class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()
        self.tables = list(tables)

    def guest_arrival(self, *guests):
        for guest in guests:
            if any(table.guest is None for table in self.tables):
                for table in self.tables:
                    if table.guest is None:
                        table.guest = guest
                        print(f"{guest.name} сел(-а) за стол номер {table.number}")
                        guest.start()
                        break
                else:
                    self.queue.put(guest)
                    print(f"{guest.name} в очереди")
            else:
                print(f"{guest.name} в очереди")

    def discuss_guests(self):
        while not self.queue.empty() or any(table.guest is not None for table in self.tables):
            for table in self.tables:
                if table.guest and not table.guest.is_alive():
                    table.guest = None
                    print(f"Стол номер {table.number} свободен")
                    
                    if not self.queue.empty():
                        next_guest = self.queue.get()
                        table.guest = next_guest
                        print(f"{next_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")
                        next_guest.start()
                    break
                elif table.guest.is_running():
                    time.sleep(0.1)
            else:
                continue
            break

# Создание столов
tables = [Table(number) for number in range(1, 6)]

# Имена гостей
guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]

# Создание гостей
guests = []
for i, name in enumerate(guests_names):
    guest = Guest(name, tables[i % len(tables)].number)
    guests.append(guest)

# Заполнение кафе столами
cafe = Cafe(*tables)

# Приём гостей
cafe.guest_arrival(*guests)

# Обслуживание гостей
cafe.discuss_guests()