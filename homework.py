"""Модуль фитнес трекер"""

from typing import Dict


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,  # имя класса тренировки;
                 duration: float,  # длительность тренировки в часах
                 distance: float,  # дист в км, которую преодолел пользователь
                 speed: float,  # средняя скорость, движения пользователя
                 calories: float  # количество килокал, за время тренировки
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        message = (f'Тип тренировки: {self.training_type}; '
                   f'Длительность:{self.duration: .3f} ч.; '
                   f'Дистанция:{self.distance: .3f} км; '
                   f'Ср. скорость:{self.speed: .3f} км/ч; '
                   f'Потрачено ккал: {self.calories:.3f}.')
        return message

    pass


class Training:
    """Базовый класс тренировки"""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,  # количество совершённых действий
                 duration: float,  # длительность тренировки
                 weight: float,  # вес спортсмена
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """
        Получить дистанцию в км.

        Args:
            action (int): Количество совершённых действий
            LEN_STEP (int): Константа для перевода значений из метров в км

        Returns:
            distance (float): Дистанцию (в километрах),
                              которую преодолел пользователь
                              за время тренировки.
        """

        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """
        Получить среднюю скорость движения

        Args:
            get_distance (int): Количество совершённых действий
            duration (float): Длительность тренировки

        Returns:
            mean_speed(float): Среднее значение скорости
                               движения во время тренировки.
        """

        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.
        Логика подсчета калорий для каждого вида тренировки своя,
        поэтому в базовом классе не нужно описывать поведение метода,
        в его теле останется ключевое слово
        """

    pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        info: InfoMessage = InfoMessage(self.__class__.__name__,
                                        self.duration,
                                        self.get_distance(),
                                        self.get_mean_speed(),
                                        self.get_spent_calories())
        return info


class Running(Training):
    """Тренировка: бег."""

    minute: int = 60
    coeff_calorie_1: int = 18
    coeff_calorie_2: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.

        Args:
            coeff_calorie_1 (int): Коэффициент для каллорий для бега
            coeff_calorie_2 (int): Коэфициент для определения каллорий бега
            weight (float): Вес спортсмена
            M_IN_KM (int): Константа для перевода значений из метров в км
            duration (float): Длительность тренировки
            get_mean_speed (float): Среднее значение
                                    скорости движения во время тренировки.
            minute (int): Константа для перевода в минуты
        Returns:
            calories (float): Количество затраченных калорий
        """

        calories = ((self.coeff_calorie_1 * self.get_mean_speed()
                     - self.coeff_calorie_2) * self.weight / self.M_IN_KM
                    * (self.duration * self.minute))
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба. """

    coeff_calorie_3: float = 0.035
    coeff_calorie_4: float = 0.029
    minute: int = 60

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

        Args:
            coeff_calorie_3 (float): Коэффициент Коэфициент
                                     для определения каллорий ходьбы
            coeff_calorie_4 (float): Коэффициент Коэфициент
                                     для определения каллорий ходьбы
            weight (float): Вес спортсмена
            height (int): Константа для перевода значений из метров в км
            get_mean_speed (float): Среднее значение скорости
                                    движения во время тренировки.
            duration (float): Длительность тренировки
            minute (int): Константа для перевода в минуты

        Returns:
            calories (float): Количество затраченных калорий
        """

        calories = ((self.coeff_calorie_3 * self.weight
                    + (self.get_mean_speed() ** 2 // self.height)
                    * self.coeff_calorie_4 * self.weight)
                    * (self.duration * self.minute))
        return calories


class Swimming(Training):
    """Тренировка: плавание."""

    # в классе переопределены методы get_spent_calories() и get_mean_speed()
    # добавлены атрибуты length_pool count_pool
    coeff_calorie_5: float = 1.1  # Коэфициент для опреления каллорий плавание
    coeff_calorie_6: int = 2  # Коэфициент для опреления каллорий плавание
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
        """Получить среднюю скорость движения.
        Args:
            length_pool (float): Длина бассейна в метрах;
            count_pool (float): Сколько раз пользователь переплыл бассейн
            M_IN_KM (int): Константа для перевода значений из метров в км
            weight (float): Вес спортсмена

        Returns:
            calories (float): Количество затраченных калорий
        """
        mean_speed: float = (self.length_pool * self.count_pool / self.M_IN_KM
                             / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.
        Args:
            get_mean_speed (float): Cреднюю скорость движения
            coeff_calorie_5 (float): Коэфициент для опреления каллорий плавания
            coeff_calorie_6 (float): Коэфициент для опреления каллорий плавания
            weight (float): Вес спортсмена

        Returns:
            calories (float): Количество затраченных калорий
        """
        calories = ((self.get_mean_speed() + self.coeff_calorie_5)
                    * self.coeff_calorie_6 * self.weight)
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


# заранее подготовленные тестовые данные для проверки фитнес-трекера"""
if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
