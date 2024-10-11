import socket
import tkinter as tk

class GameClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = None
        self.results_label = None
        self.buttons = []
        self.player_board = [['.' for _ in range(10)] for _ in range(10)]
        self.enemy_board = [['.' for _ in range(10)] for _ in range(10)]
        self.con_serv()

    def con_serv(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_ip, self.server_port))
            print(f"Успешно подключен к серверу {self.server_ip}:{self.server_port}")
        except socket.error as err:
            print(f"Не удалось подключиться к серверу: {err}")
            self.ry_con_serv()

    def ry_con_serv(self):
        retry = input("Хотите попробовать снова подключиться? (y/n): ").strip().lower()
        if retry == 'y':
            self.con_serv()
        else:
            print("Выход из программы.")
            exit()

    def send_coord(self, row, col):
        coord = f"{row} {col}"
        try:
            self.client_socket.sendall(coord.encode())
            response = self.client_socket.recv(1024).decode()
            self.prov_serv(response, row, col)
        except socket.error as err:
            print(f"Ошибка при отправке данных: {err}")
            self.result("Ошибка связи с сервером.")

    def prov_serv(self, response, row, col):
        if "попадание" in response.lower():
            self.result("Вы попали!")
            self.update_board(self.enemy_board, row, col, "X")
            self.update_button(row, col, "red")
            if "корабль уничтожен" in response.lower():
                self.mark_destroyed_ship(row, col)
        elif "промах" in response.lower():
            self.result("Вы промахнулись.")
            self.update_board(self.enemy_board, row, col, "O")
            self.update_button(row, col, "blue")
        elif "повторный" in response.lower():
            self.result("Вы уже стреляли в эту точку.")
        else:
            self.result("Неизвестный ответ от сервера.")

    def result(self, results):
        if self.results_label:
            self.results_label.config(text=results)

    def update_board(self, board, row, col, symbol):
        board[row][col] = symbol

    def update_button(self, row, col, color):
        self.buttons[row][col].config(bg=color)

    def mark_destroyed_ship(self, row, col):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        stack = [(row, col)]
        visited = set()  # Для избежания повторного посещения клеток

        while stack:
            r, c = stack.pop()
            if (r, c) in visited:
                continue
            visited.add((r, c))

            # Проверка на выход за границы и на то, что клетка помечена как часть уничтоженного корабля
            if 0 <= r < 10 and 0 <= c < 10 and self.enemy_board[r][c] == 'X':
                self.update_button(r, c, "black")  # Помечаем клетку как уничтоженную

                # Добавляем соседние клетки в стек, если они валидные
                for dr, dc in directions:
                    stack.append((r + dr, c + dc))

    def interface(self):
        window = tk.Tk()
        window.title("Морской Бой")
        window.geometry("700x600")
        window.configure(bg="#ddeeff")

        enemy_frame = tk.Frame(window, bg="#ddeeff", padx=10, pady=10)
        enemy_frame.pack(side=tk.LEFT, padx=20, pady=20)

        self.results_label = tk.Label(window, text="", font=("Arial", 12), bg="#ddeeff")
        self.results_label.pack()

        for row in range(10):
            button_row = []
            for col in range(10):
                btn = tk.Button(enemy_frame, text='', width=3, height=1,
                                command=lambda r=row, c=col: self.send_coord(r, c),
                                bg='#ffffff', font=("Arial", 12))
                btn.grid(row=row, column=col)
                button_row.append(btn)
            self.buttons.append(button_row)

        window.mainloop()

client = GameClient('127.0.0.1', 8882)
client.interface()