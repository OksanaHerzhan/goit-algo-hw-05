# Необхідно створити функцію generator_numbers

# Вимоги до завдання:

# Функція generator_numbers(text: str) повинна приймати рядок як 
# аргумент і повертати генератор, що ітерує по всіх дійсних числах у тексті. 
# Дійсні числа у тексті вважаються записаними без помилок і чітко 
# відокремлені пробілами з обох боків.

# Функція sum_profit(text: str, func: Callable) має використовувати 
# генератор generator_numbers для обчислення загальної суми чисел у
# вхідному рядку та приймати його як аргумент при виклику.

# Критерії оцінювання:

# Правильність визначення та повернення дійсних чисел функцією generator_numbers.
# Коректність обчислення загальної суми в sum_profit.
# Чистота коду, наявність коментарів та відповідність стилю кодування PEP8.

from typing import Callable

def is_float(hello: str)->float:          # конвертуємо str to float
    try:    return float(hello)
    except: return None                  # в іншому випадку повертаємо None (нічого не повертаємо)

def generator_numbers(text: str):
    str_list = text.split(' ')           # Дійсні числа у тексті чітко відокремлені пробілами
    for hello in str_list[1:(len(str_list)-1)]:
        num = is_float(hello)             # повертає float для Float
        if num is not None:               # або  None для str
            yield num                     # створення генератора

def sum_profit(text: str, func: Callable)->float: # має використовувати генератор generator_numbers для обчислення загальної суми чисел у вхідному рядку та приймати його як аргумент при виклику
    total_sum=0.0
    for num in func(text):                # підсумовіє float
        total_sum +=num
    return total_sum

def main():
    text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")

if __name__ == "__main__":
    main()