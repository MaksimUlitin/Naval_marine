# server.py
import socket
import threading
from game_logic import setup_field, handle_shot, print_field

# Глобальные переменные для управления состоянием игры
fields = {}  # Словарь для хранения полей игроков
shot_histories = [set(), set()]  # История выстрелов для каждого игрока
current_turn = 0  # Переменная для отслеживания текущего хода

def print_fields():
    """Отображение полей обоих игроков на сервере."""
    print("Поле игрока 1:")
    print_field(fields[0])
    print("Поле игрока 2:")
    print_field(fields[1])

def handle_client(client_socket, player_number):
    """Обработка запросов клиента."""
    global current_turn

    # Получаем поле для игрока
    field = fields[player_number]

    while True:
        if current_turn == player_number:
            try:
                # Получаем координаты выстрела от клиента
                shot = client_socket.recv(1024).decode('utf-8')
                if not shot:
                    break  # Клиент отключился

                row, col = map(int, shot.split())
                result, hit = handle_shot(fields[1 - player_number], row, col, shot_histories[1 - player_number])  # Ход противника

                # Отправляем результат выстрела игроку
                client_socket.send(result.encode('utf-8'))

                # Печатаем поля на сервере
                print_fields()

                # Переключаем очередь, если промах
                if not hit:
                    current_turn = 1 - current_turn
                    print(f"Сейчас ход игрока {current_turn + 1}")
            except (ValueError, IndexError):
                client_socket.send("Некорректный ввод! Введите два числа (0-9).".encode('utf-8'))

def start_server():
    """Запуск сервера."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(2)  # Ожидание подключения двух клиентов
    print("Ожидание подключения игроков...")

    for i in range(2):
        client_socket, addr = server.accept()
        print(f"Подключен игрок {i + 1}: {addr}")
        fields[i] = setup_field()  # Настраиваем поле для каждого игрока

        # Запуск потока для работы с клиентом
        client_handler = threading.Thread(target=handle_client, args=(client_socket, i))
        client_handler.start()

if __name__ == "__main__":
    start_server()
