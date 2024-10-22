import random

FIELD_SIZE = 10
SHIPS = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]  # Размеры кораблей


def create_empty_field():
    return [['.' for _ in range(FIELD_SIZE)] for _ in range(FIELD_SIZE)]


def print_field(field):
    for row in field:
        print(' '.join(row))
    print()


def is_valid_position(field, row, col, size, orientation):
    # Проверка границ поля и интервала в 1 клетку вокруг корабля
    for i in range(-1, size + 1):
        for j in range(-1, 2):
            if orientation == 'h':
                r, c = row + j, col + i
            else:
                r, c = row + i, col + j
            if 0 <= r < FIELD_SIZE and 0 <= c < FIELD_SIZE:
                if field[r][c] != '.':
                    return False
    return True


def place_ship(field, ship_size):
    while True:
        orientation = random.choice(['h', 'v'])
        if orientation == 'h':
            row = random.randint(0, FIELD_SIZE - 1)
            col = random.randint(0, FIELD_SIZE - ship_size)
        else:
            row = random.randint(0, FIELD_SIZE - ship_size)
            col = random.randint(0, FIELD_SIZE - 1)

        if is_valid_position(field, row, col, ship_size, orientation):
            for i in range(ship_size):
                if orientation == 'h':
                    field[row][col + i] = 'S'
                else:
                    field[row + i][col] = 'S'
            break


def setup_field():
    field = create_empty_field()
    for ship_size in SHIPS:
        place_ship(field, ship_size)
    return field


def is_ship_destroyed(field, row, col):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < FIELD_SIZE and 0 <= c < FIELD_SIZE:
            if field[r][c] == 'S':
                return False  # Найдена неповрежденная часть корабля
    return True  # Все части корабля уничтожены


def handle_shot(field, row, col, shot_history):
    if (row, col) in shot_history:
        return 'Уже стреляли сюда!', False, False

    shot_history.add((row, col))

    if field[row][col] == 'S':
        field[row][col] = 'X'
        ship_destroyed = is_ship_destroyed(field, row, col)
        return 'Попадание!', True, ship_destroyed
    elif field[row][col] == '.':
        field[row][col] = 'O'
        return 'Промах!', False, False

    return 'Уже стреляли сюда!', False, False
