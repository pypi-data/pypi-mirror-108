# EasyPass
[![PyPi](https://img.shields.io/pypi/v/t)](https://pypi.org/project/easypass/)
![Python](https://img.shields.io/pypi/pyversions/Django)

Модуль для простой генерации паролей и почтовых ящиков
## Оглавление
1. [Установка](https://github.com/uprj/easypass.py#установка)
2. [Функции и классы](https://github.com/uprj/easypass.py#функции-и-классы)
    1. [Аргументы](https://github.com/uprj/easypass.py#аргументы)
        1. [Password](https://github.com/uprj/easypass.py#password)
        2. [Password.print()](https://github.com/uprj/easypass.py#passwordprint)
        3. [Password.save()](https://github.com/uprj/easypass.py#passwordsave)
        4. [Email](https://github.com/uprj/easypass.py#email)
        5. [Email.print()](https://github.com/uprj/easypass.py#Emailprint)
        6. [Email.save()](https://github.com/uprj/easypass.py#emailsave)
3. [Генерация пароля](https://github.com/uprj/easypass.py#генерация-пароля)
4. [Генерация почтового ящика](https://github.com/uprj/easypass.py#генерация-почтового-ящика)
## Установка
Установка осуществляется командой в терминале:
```
pip install easypass
```
## Функции и классы
В модуле есть два класса — ```Password``` и ```Email```. У них есть 3 функции. Это конечно же ```__init__()```, в котором создаётся пароль/почта, ```print()``` для вывода пароля или почты в консоль и  ```save()``` для сохранения в файл.
## Аргументы
В таблице указаны имя параметра, его значение по умолчанию и то, за что он отвечает.

### Password
| Параметр | Значение | Описание |
|:----------------:|:---------:|:----------------:|
| lenght | 8 | Длина пароля |
| lower | True | Наличие нижнего регистра |
| upper | True | Наличие верхнего регистра |
| numbers | True | Наличие цифр |
| symbols | False | Наличие специальных знаков |
### Password.print()
Нет никаких параметров, функция просто выводит пароль в консоль
### Password.save()
| Параметр | Значение | Описание |
|:----------------:|:---------:|:----------------:|
| path | None | Путь к файлу |
____
### Email
| Параметр | Значение | Описание |
|:----------------:|:---------:|:----------------:|
| lenght1 | 7 | Длина символов до знака "@" |
| lenght2 | 5 | Длина символов после знака "@" |
| lower | True | Наличие нижнего регистра |
| upper | True | Наличие верхнего регистра |
| numbers | True | Наличие цифр |
### Email.print()
Нет никаких параметров, функция просто выводит почту в консоль
### Email.save()
| Параметр | Значение | Описание |
|:----------------:|:---------:|:----------------:|
| path | None | Путь к файлу |
## Генерация пароля
Пример кода генерации пароля:
```python
import easypass

password = easypass.Password()
password.print()
password.save("my.password")
```
## Генерация почтового ящика
Пример кода генерации почтового ящика:
```python
import easypass

email = easypass.Email()
email.print()
email.save("my.password")
```
