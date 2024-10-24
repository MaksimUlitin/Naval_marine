import socket
import threading
from game_logic import setup_field, handle_shot, print_field

fields = {}
shot_histories = [set(), set()]
current_turn = 0


def print_fields():
    print("Поле игрока 1:")
    print_field(fields[0])
    print("Поле игрока 2:")
    print_field(fields[1])


def handle_client(client_socket, player_number):
    global current_turn
    opponent_number = 1 - player_number

    # Отправляем клиенту его поле сразу после подключения
    field_str = '\n'.join([''.join(row) for row in fields[player_number]])
    client_socket.send(f"INIT {field_str}".encode('utf-8'))

    while True:
        if current_turn == player_number:
            try:
                shot = client_socket.recv(1024).decode('utf-8')
                if not shot:
                    break

                row, col = map(int, shot.split())
                result, hit, ship_destroyed = handle_shot(fields[opponent_number], row, col,
                                                          shot_histories[opponent_number])

                if ship_destroyed:
                    result += " Корабль уничтожен!"

                client_socket.send(result.encode('utf-8'))

                print_fields()

                if not hit:
                    current_turn = opponent_number
                    print(f"Сейчас ход игрока {current_turn + 1}")
            except (ValueError, IndexError):
                client_socket.send("Некорректный ввод! Введите два числа (0-9).".encode('utf-8'))


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8881))
    server.listen(2)
    print("Ожидание подключения игроков...")

    for i in range(2):
        client_socket, addr = server.accept()
        print(f"Подключен игрок {i + 1}: {addr}")
        fields[i] = setup_field()

        client_handler = threading.Thread(target=handle_client, args=(client_socket, i))
        client_handler.start()


if __name__ == "__main__":
    start_server()