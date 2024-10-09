# client.py
import socket
import tkinter as tk


class GameClient:
    def __init__(self, server_ip, server_port):
        """Авторизация клиента и подключение к серверу."""
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = None
        self.results_label = None
        self.con_serv()

    def con_serv(self):
        """Подключения к серверу"""
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_ip, self.server_port))
            print(f"Успешно подключен к серверу {self.server_ip}:{self.server_port}")
        except socket.error as err:
            print(f"Не удалось подключиться к серверу: {err}")
            self.ry_con_serv()

    def ry_con_serv(self):
        """Повторная попытка подключения"""
        retry = input("Хотите попробовать снова подключиться? (y/n): ").strip().lower()
        if retry == 'y':
            self.con_serv()
        else:
            print("Выход из программы.")
            exit()

    def send_coord(self, coord):
        """Отправка координат на сервер и получение ответа"""
        if not self.valid_coord(coord):
            self.result("Некорректный формат координат.")
            return

        try:
            self.client_socket.sendall(coord.encode())
            response = self.client_socket.recv(1024).decode()
            self.prov_serv(response)
        except socket.error as err:
            print(f"Ошибка при отправке данных: {err}")
            self.result("Ошибка связи с сервером.")

    @staticmethod
    def valid_coord(coord):
        """Проверка формата координат перед отправкой"""
        try:
            row, col = map(int, coord.split())
            return 1 <= row <= 10 and 1 <= col <= 10
        except ValueError:
            return False

    def prov_serv(self, response):
        """Обработка ответа от сервера"""
        if "попадание" in response:
            self.result("Вы попали!")
        elif "промах" in response:
            self.result("Вы промахнулись.")
        elif "повторный" in response:
            self.result("Вы уже стреляли в эту точку.")
        else:
            self.result("Неизвестный ответ от сервера.")

    def result(self, results):
        """Обновление метки с результатом"""
        if self.results_label:
            self.results_label.config(text=results)

    def interface(self):
        """Запуск графического интерфейса для взаимодействия с пользователем."""
        window = tk.Tk()
        window.title("Морской Бой")
        window.geometry("350x250")
        window.configure(bg="#ddeeff")

        frame = tk.Frame(window, bg="#ddeeff", padx=10, pady=10)
        frame.pack(padx=20, pady=20)

        label = tk.Label(frame, text="Введите координаты (строка столбец):", bg="#ddeeff", font=("Arial", 12))
        label.pack(pady=10)

        entry = tk.Entry(frame, width=20, font=("Arial", 14))
        entry.pack(pady=10)

        button = tk.Button(frame, text="Отправить", command=lambda: self.send_coord(entry.get()), bg="#0055ff",
                           fg="white", font=("Arial", 12))
        button.pack(pady=10)

        self.results_label = tk.Label(frame, text="", font=("Arial", 12), bg="#ddeeff")
        self.results_label.pack(pady=10)

        window.mainloop()


client = GameClient('127.0.0.1', 9999)
client.interface()
