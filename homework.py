from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    # :3f - округление и не менее трёх знаков после точки.
    MESSAGE_TEMPLATE: str = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        """Получить сообщение, содержащее информацию о тренировке."""
        message = self.MESSAGE_TEMPLATE.format(
            training_type=self.training_type,
            duration=self.duration,
            distance=self.distance,
            speed=self.speed,
            calories=self.calories,
        )
        return message


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65  # Метров
    M_IN_KM: int = 1000
    MINUTE: int = 60  # Секунд

    def __init__(
        self,
        action: int,  # Кол-во действий
        duration: float,  # В часах
        weight: float,  # КГ
    ) -> None:
        self.action = action
        self.duration_h = duration
        self.duration_m = duration * self.MINUTE
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_h

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(
            training_type=self.__class__.__name__,
            duration=self.duration_h,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories(),
        )
        return message


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1: int = 18
    COEFF_CALORIE_2: int = 20

    def get_spent_calories(self) -> float:
        temp1 = self.COEFF_CALORIE_1 * self.get_mean_speed()
        temp2 = temp1 - self.COEFF_CALORIE_2
        return temp2 * self.weight / self.M_IN_KM * self.duration_m


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIE_1: float = 0.035
    COEFF_CALORIE_2: float = 0.029

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: int
    ):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        part_1 = self.COEFF_CALORIE_1 * self.weight
        part_2 = self.get_mean_speed()**2 // self.height
        part_3 = self.COEFF_CALORIE_2 * self.weight
        return (part_1 + part_2 * part_3) * self.duration_m


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEFF_CALORIE_1: float = 1.1

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: int,
        count_pool: int
    ):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        temp = self.length_pool * self.count_pool
        return temp / self.M_IN_KM / self.duration_h

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed() + self.COEFF_CALORIE_1) * 2 * self.weight


def read_package(
    workout_type: str,
    data: list,
    raise_exceptions: bool = True,
) -> Training:
    """Прочитать данные полученные от датчиков.
    Возвращает экземпляр класса Training.
    Если передан некорректный workout_type,
    будет выброшено исключение ValueError,
    если при этом raise_exceptions равен False,
    будет возвращено None.
    """
    mapping = {
        'RUN': Running,
        'SWM': Swimming,
        'WLK': SportsWalking,
    }
    if workout_type not in mapping:
        if not raise_exceptions:
            return
        raise ValueError('Invalid workout_type')
    training_class = mapping[workout_type]
    training = training_class(*data)
    return training


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
