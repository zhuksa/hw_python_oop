"""Модуль фитнес трекер"""

from typing import Dict


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность:{self.duration: .3f} ч.; '
                f'Дистанция:{self.distance: .3f} км; '
                f'Ср. скорость:{self.speed: .3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки"""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """
        Получить дистанцию в км.

        Returns:
            (float): Дистанцию (в километрах),
                     которую преодолел пользователь
                     за время тренировки.
        """

        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """
        Получить среднюю скорость движения

        Returns:
            (float): Среднее значение скорости
                     вижения во время тренировки.
        """

        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError("Subclasses should implement this method!")

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    MINUTE: int = 60
    COEFF_CALORIE_1: int = 18
    COEFF_CALORIE_2: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.

        Returns:
            (float): Количество затраченных калорий
        """

        calories = ((self.COEFF_CALORIE_1 * self.get_mean_speed()
                     - self.COEFF_CALORIE_2) * self.weight / self.M_IN_KM
                    * (self.duration * self.MINUTE))
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба. """
    COEFF_CALORIE_3: float = 0.035
    COEFF_CALORIE_4: float = 0.029
    MINUTE: int = 60
    RATIO: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.

        Returns:
            (float): Количество затраченных калорий
        """
        calories = ((self.COEFF_CALORIE_3 * self.weight
                    + (self.get_mean_speed() ** self.RATIO // self.height)
                    * self.COEFF_CALORIE_4 * self.weight)
                    * (self.duration * self.MINUTE))
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    COEFF_CALORIE_5: float = 1.1
    COEFF_CALORIE_6: int = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения.а

        Returns:
            (float): Количество затраченных калорий
        """
        mean_speed: float = (self.length_pool * self.count_pool / self.M_IN_KM
                             / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.

        Returns:
            (float): Количество затраченных калорий
        """
        calories = ((self.get_mean_speed() + self.COEFF_CALORIE_5)
                    * self.COEFF_CALORIE_6 * self.weight)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict: Dict = {'SWM': Swimming,
                           'RUN': Running,
                           'WLK': SportsWalking}
    create_tren: Training = training_dict[workout_type]
    created_object: Training = create_tren(*data)
    return created_object


def main(training: Training) -> str:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
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
