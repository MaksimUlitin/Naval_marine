import random

# Игровые параметры
FIELD_SIZE = 10
SHIPS = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]  # Размеры кораблей

def create_empty_field():
    """Создание пустого поля 10x10."""
    return [['.' for _ in range(FIELD_SIZE)] for _ in range(FIELD_SIZE)]

def print_field(field):
    """Отображение игрового поля."""
    for row in field:
        print(' '.join(row))
    print()

def place_ship(field, ship_size):
    """Расстановка корабля на поле случайным образом."""
    while True:
        orientation = random.choice(['h', 'v'])  # Горизонтальная или вертикальная ориентация
        if orientation == 'h':  # Горизонтально
            row = random.randint(0, FIELD_SIZE - 1)
            col = random.randint(0, FIELD_SIZE - ship_size)
            if all(field[row][col + i] == '.' for i in range(ship_size)):
                for i in range(ship_size):
                    field[row][col + i] = 'S'
                break
        else:  # Вертикально
            row = random.randint(0, FIELD_SIZE - ship_size)
            col = random.randint(0, FIELD_SIZE - 1)
            if all(field[row + i][col] == '.' for i in range(ship_size)):
                for i in range(ship_size):
                    field[row + i][col] = 'S'
                break

def setup_field():
    """Создание поля с расставленными кораблями."""
    field = create_empty_field()
    for ship_size in SHIPS:
        place_ship(field, ship_size)
    return field

def handle_shot(field, row, col, shot_history):
    """
    Обработка выстрела по координатам.
    Возвращает результат выстрела и обновляет поле.
    """
    if (row, col) in shot_history:
        return 'Уже стреляли сюда!', False  # Повторный выстрел

    shot_history.add((row, col))  # Добавляем координаты в историю выстрелов

    if field[row][col] == 'S':
        field[row][col] = 'X'  # Попадание
        return 'Попадание!', True
    elif field[row][col] == '.':
        field[row][col] = 'O'  # Промах
        return 'Промах!', False

    return 'Уже стреляли сюда!', False
