import socket
from game_logic import print_field

class GameClient:
    def __init__(self, server_ip, server_port): # конструктор класса GameClient
        """
        Инициализация клиента игры.

        :param server_ip: IP-адрес сервера
        :param server_port: Порт сервера
        """
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = None
        self.player_board = [['.' for _ in range(10)] for _ in range(10)]
        self.enemy_board = [['.' for _ in range(10)] for _ in range(10)]
        self.con_serv()

    def con_serv(self):
        """
        Устанавливает соединение с сервером.

        Если не удается, повторяет подключение.
        """
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_ip, self.server_port))
            print(f"Успешно подключен к серверу {self.server_ip}:{self.server_port}")
        except socket.error as err:
            print(f"Не удалось подключиться к серверу: {err}")
            self.ry_con_serv()

    def ry_con_serv(self):
        """
        Запрашивает у пользователя, хочет ли он повторить попытку подключения к серверу. 
        """
        r = input("Хотите попробовать снова подключиться? (y/n): ").strip().lower()
        if r == 'y':
            self.con_serv()
        else:
            print("Выход из программы.")
            exit()

    def send_coord(self, row, col):
        """
        Отправляет координаты выстрела на сервер.

        :param row: Номер строки (координата Y)
        :param col: Номер столбца (координата X)
        
        Обрабатывает ответ от сервера
        """
        coord = f"{row} {col}"
        try:
            self.client_socket.sendall(coord.encode())
            response = self.client_socket.recv(1024).decode()
            self.prov_serv(response, row, col)
        except socket.error as err:
            print(f"Ошибка при отправке данных: {err}")
            self.result("Ошибка связи с сервером.")

    def prov_serv(self, response, row, col):
        """
        Обрабатывает ответ сервера на отправленные координаты.

        :param response: Ответ сервера
        :param row: Номер строки (координата Y)
        :param col: Номер столбца (координата X)
        
        Определяет результат выстрела и обновляет игровую доску соответствующим образом.
        """
        if "попадание" in response.lower():
            self.result("Вы попали!")
            self.update_board(self.enemy_board, row, col, "X")
            if "корабль уничтожен" in response.lower():
                self.mark_destroyed_ship(row, col)
        elif "промах" in response.lower():
            self.result("Вы промахнулись.")
            self.update_board(self.enemy_board, row, col, "O")
        elif "повторный" in response.lower():
            self.result("Вы уже стреляли в эту точку.")
        else:
            self.result("Неизвестный ответ от сервера.")

    def result(self, results):
        print(results)

    def update_board(self, board, row, col, symbol):
        board[row][col] = symbol

    def print_board(self, board):
        print("  " + " ".join([str(i) for i in range(10)]))
        for i, row in enumerate(board):
            print(f"{i} " + " ".join(row))



    def mark_destroyed_ship(self, row, col):
        d = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        s = [(row, col)]
        vis = set()  # чтобы не было поподания на одну и ту же клетку

        while s:
            r, c = s.pop()
            if (r, c) in vis:
                continue
            vis.add((r, c))

            if 0 <= r < 10 and 0 <= c < 10 and self.enemy_board[r][c] == 'X':
                self.enemy_board[r][c] = 'D'

                for dr, dc in d:
                    s.append((r + dr, c + dc))

    def game_loop(self):
        """
       Основной игровой цикл.

       Запрашивает у игрока координаты выстрела и обрабатывает их,
       пока игра не будет завершена.
       """
        while True:
            print("\nВаше поле:")
            self.print_board(self.player_board)
            print("\nПоле противника:")
            self.print_board(self.enemy_board)

            try:
                row = int(input("Введите номер строки (0-9): "))
                col = int(input("Введите номер столбца (0-9): "))
                if 0 <= row < 10 and 0 <= col < 10:
                    self.send_coord(row, col)
                else:
                    print("Координаты вне допустимого диапазона.")
            except ValueError:
                print("Неверный ввод. Пожалуйста, введите числа.")

if __name__ == "__main__":
    server_ip = input("Введите IP сервера: ")
    server_port = int(input("Введите порт сервера: "))
    client = GameClient(server_ip, server_port)
    client.game_loop()
