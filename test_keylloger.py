import pytest
from unittest.mock import patch, MagicMock
from keylloger import (
    get_active_window, get_current_layout, convert_to_english, convert_to_russian,
    is_phone_number

)

# Тест для Windows: функция должна вернуть название активного окна
@patch('keylloger.gw.getActiveWindow')
def test_get_active_window_windows(mock_get_active_window):
    mock_get_active_window.return_value.title = "Notepad - Untitled"
    assert get_active_window() == "Notepad - Untitled"

# Тест для Windows: функция должна вернуть "Unknown", если возникает ошибка
@patch('keylloger.gw.getActiveWindow')
def test_get_active_window_windows_exception(mock_get_active_window):
    mock_get_active_window.side_effect = Exception("Error")
    assert get_active_window() == "Unknown"

# Тест для Windows: раскладка RU
@patch('keylloger.ctypes.WinDLL')  # Путь должен быть корректным
def test_get_current_layout_windows_ru(mock_win_dll):
    mock_user32 = MagicMock()
    mock_win_dll.return_value = mock_user32
    mock_user32.GetForegroundWindow.return_value = 1
    mock_user32.GetWindowThreadProcessId.return_value = 1
    mock_user32.GetKeyboardLayout.return_value = 0x0419  # Раскладка RU

    assert get_current_layout() == "RU"

# Тест для Windows: раскладка EN
@patch('keylloger.ctypes.WinDLL')  # Путь должен быть корректным
def test_get_current_layout_windows_en(mock_win_dll):
    mock_user32 = MagicMock()
    mock_win_dll.return_value = mock_user32
    mock_user32.GetForegroundWindow.return_value = 1
    mock_user32.GetWindowThreadProcessId.return_value = 1
    mock_user32.GetKeyboardLayout.return_value = 0x0409  # Раскладка EN

    assert get_current_layout() == "EN"

# Тест для неподдерживаемой ОС (Linux)
@patch('keylloger.platform.system')  # Путь должен быть корректным
def test_get_current_layout_unsupported_os(mock_platform_system):
    mock_platform_system.return_value = "Linux"

    assert get_current_layout() == "Unsupported OS"

def test_convert_to_english_without_shift():
    assert convert_to_english('й') == 'q'
    assert convert_to_english('ц') == 'w'
    assert convert_to_english('у') == 'e'
    assert convert_to_english('к') == 'r'
    assert convert_to_english('е') == 't'
    assert convert_to_english('н') == 'y'
    assert convert_to_english('г') == 'u'
    assert convert_to_english('ш') == 'i'
    assert convert_to_english('щ') == 'o'
    assert convert_to_english('з') == 'p'
    assert convert_to_english('х') == '['
    assert convert_to_english('ъ') == ']'
    assert convert_to_english('ф') == 'a'
    assert convert_to_english('ы') == 's'
    assert convert_to_english('в') == 'd'
    assert convert_to_english('а') == 'f'
    assert convert_to_english('п') == 'g'
    assert convert_to_english('р') == 'h'
    assert convert_to_english('о') == 'j'
    assert convert_to_english('л') == 'k'
    assert convert_to_english('д') == 'l'
    assert convert_to_english('ж') == ';'
    assert convert_to_english('э') == "'"
    assert convert_to_english('я') == 'z'
    assert convert_to_english('ч') == 'x'
    assert convert_to_english('с') == 'c'
    assert convert_to_english('м') == 'v'
    assert convert_to_english('и') == 'b'
    assert convert_to_english('т') == 'n'
    assert convert_to_english('ь') == 'm'
    assert convert_to_english('б') == ','
    assert convert_to_english('ю') == '.'
    assert convert_to_english('/') == '.'
    assert convert_to_english('ё') == ''  # Не заменяется на символ
    assert convert_to_english('1') == '1'

# Тестирование конвертации с Shift (заглавные символы и спецсимволы)
def test_convert_to_english_with_shift():
    assert convert_to_english('Й', shift_pressed=True) == 'q'
    assert convert_to_english('Ц', shift_pressed=True) == 'w'
    assert convert_to_english('У', shift_pressed=True) == 'e'
    assert convert_to_english('К', shift_pressed=True) == 'r'
    assert convert_to_english('Е', shift_pressed=True) == 't'
    assert convert_to_english('Н', shift_pressed=True) == 'y'
    assert convert_to_english('Г', shift_pressed=True) == 'u'
    assert convert_to_english('Ш', shift_pressed=True) == 'i'
    assert convert_to_english('Щ', shift_pressed=True) == 'o'
    assert convert_to_english('З', shift_pressed=True) == 'p'
    assert convert_to_english('Х', shift_pressed=True) == '['
    assert convert_to_english('Ъ', shift_pressed=True) == ']'
    assert convert_to_english('Ф', shift_pressed=True) == 'a'
    assert convert_to_english('Ы', shift_pressed=True) == 's'
    assert convert_to_english('В', shift_pressed=True) == 'd'
    assert convert_to_english('А', shift_pressed=True) == 'f'
    assert convert_to_english('П', shift_pressed=True) == 'g'
    assert convert_to_english('Р', shift_pressed=True) == 'h'
    assert convert_to_english('О', shift_pressed=True) == 'j'
    assert convert_to_english('Л', shift_pressed=True) == 'k'
    assert convert_to_english('Д', shift_pressed=True) == 'l'
    assert convert_to_english('Ж', shift_pressed=True) == ';'
    assert convert_to_english('Э', shift_pressed=True) == "'"
    assert convert_to_english('Я', shift_pressed=True) == 'z'
    assert convert_to_english('Ч', shift_pressed=True) == 'x'
    assert convert_to_english('С', shift_pressed=True) == 'c'
    assert convert_to_english('М', shift_pressed=True) == 'v'
    assert convert_to_english('И', shift_pressed=True) == 'b'
    assert convert_to_english('Т', shift_pressed=True) == 'n'
    assert convert_to_english('Ь', shift_pressed=True) == 'm'
    assert convert_to_english('Б', shift_pressed=True) == ','
    assert convert_to_english('Ю', shift_pressed=True) == '.'
    assert convert_to_english(',', shift_pressed=True) == '/'
    assert convert_to_english('Ё', shift_pressed=True) == ''
    assert convert_to_english('!', shift_pressed=True) == '1'
    assert convert_to_english('@', shift_pressed=True) == '2'
    assert convert_to_english('№', shift_pressed=True) == '3'
    assert convert_to_english(';', shift_pressed=True) == '4'

# Тестирование, когда символ не найден в раскладке
def test_convert_to_english_not_found():
    assert convert_to_english('z') == 'z'  # Символ не найден в раскладке
    assert convert_to_english('Z', shift_pressed=True) == 'Z'  # Символ не найден в раскладке с Shift
    assert convert_to_english('~') == '~'  # Специальный символ, не находящийся в раскладке
    assert convert_to_english('&', shift_pressed=True) == '&'  # Специальный символ с Shift

def test_convert_to_russian_without_shift():
    # Проверка обычных символов
    assert convert_to_russian('q') == 'й'
    assert convert_to_russian('w') == 'ц'
    assert convert_to_russian('e') == 'у'
    assert convert_to_russian('r') == 'к'
    assert convert_to_russian('t') == 'е'
    assert convert_to_russian('y') == 'н'
    assert convert_to_russian('u') == 'г'
    assert convert_to_russian('i') == 'ш'
    assert convert_to_russian('o') == 'щ'
    assert convert_to_russian('p') == 'з'
    assert convert_to_russian('[') == 'х'
    assert convert_to_russian(']') == 'ъ'
    assert convert_to_russian('a') == 'ф'
    assert convert_to_russian('s') == 'ы'
    assert convert_to_russian('d') == 'в'
    assert convert_to_russian('f') == 'а'
    assert convert_to_russian('g') == 'п'
    assert convert_to_russian('h') == 'р'
    assert convert_to_russian('j') == 'о'
    assert convert_to_russian('k') == 'л'
    assert convert_to_russian('l') == 'д'
    assert convert_to_russian(';') == 'ж'
    assert convert_to_russian("'") == 'э'
    assert convert_to_russian('z') == 'я'
    assert convert_to_russian('x') == 'ч'
    assert convert_to_russian('c') == 'с'
    assert convert_to_russian('v') == 'м'
    assert convert_to_russian('b') == 'и'
    assert convert_to_russian('n') == 'т'
    assert convert_to_russian('m') == 'ь'
    assert convert_to_russian(',') == 'б'
    assert convert_to_russian('.') == 'ю'
    assert convert_to_russian('/') == '.'
    assert convert_to_russian('1') == '1'

# Тестирование конвертации с Shift (заглавные символы и спецсимволы)
def test_convert_to_russian_with_shift():
    # Проверка символов с Shift
    assert convert_to_russian('q', shift_pressed=True) == 'Й'
    assert convert_to_russian('w', shift_pressed=True) == 'Ц'
    assert convert_to_russian('e', shift_pressed=True) == 'У'
    assert convert_to_russian('r', shift_pressed=True) == 'К'
    assert convert_to_russian('t', shift_pressed=True) == 'Е'
    assert convert_to_russian('y', shift_pressed=True) == 'Н'
    assert convert_to_russian('u', shift_pressed=True) == 'Г'
    assert convert_to_russian('i', shift_pressed=True) == 'Ш'
    assert convert_to_russian('o', shift_pressed=True) == 'Щ'
    assert convert_to_russian('p', shift_pressed=True) == 'З'
    assert convert_to_russian('[' , shift_pressed=True) == 'Х'
    assert convert_to_russian(']', shift_pressed=True) == 'Ъ'
    assert convert_to_russian('a', shift_pressed=True) == 'Ф'
    assert convert_to_russian('s', shift_pressed=True) == 'Ы'
    assert convert_to_russian('d', shift_pressed=True) == 'В'
    assert convert_to_russian('f', shift_pressed=True) == 'А'
    assert convert_to_russian('g', shift_pressed=True) == 'П'
    assert convert_to_russian('h', shift_pressed=True) == 'Р'
    assert convert_to_russian('j', shift_pressed=True) == 'О'
    assert convert_to_russian('k', shift_pressed=True) == 'Л'
    assert convert_to_russian('l', shift_pressed=True) == 'Д'
    assert convert_to_russian(';', shift_pressed=True) == 'Ж'
    assert convert_to_russian("'", shift_pressed=True) == 'Э'
    assert convert_to_russian('z', shift_pressed=True) == 'Я'
    assert convert_to_russian('x', shift_pressed=True) == 'Ч'
    assert convert_to_russian('c', shift_pressed=True) == 'С'
    assert convert_to_russian('v', shift_pressed=True) == 'М'
    assert convert_to_russian('b', shift_pressed=True) == 'И'
    assert convert_to_russian('n', shift_pressed=True) == 'Т'
    assert convert_to_russian('m', shift_pressed=True) == 'Ь'
    assert convert_to_russian(',', shift_pressed=True) == 'Б'
    assert convert_to_russian('.', shift_pressed=True) == 'Ю'
    assert convert_to_russian('/', shift_pressed=True) == ','

# Тестирование, когда символ не найден в раскладке
def test_convert_to_russian_not_found():
    # Символы, которые не существуют в раскладке, должны возвращаться как есть 
    assert convert_to_russian('Z', shift_pressed=True) == 'Z'  # Символ не найден в раскладке с Shift
    assert convert_to_russian('~') == '~'  # Специальный символ, не находящийся в раскладке
    assert convert_to_russian('&', shift_pressed=True) == '&'  # Специальный символ с Shift
    assert convert_to_russian('1') == '1'  # Символ цифры, не изменяется

# Тестирование с пустыми символами
def test_convert_to_russian_empty_char():
    # Проверка на пустой символ (символ, который вообще не был передан)
    assert convert_to_russian('') == ''  # Пустой символ должен возвращаться пустым

# Тестирование с пробелом
def test_convert_to_russian_space():
    # Проверка на пробел, который не должен изменяться
    assert convert_to_russian(' ') == ' '  # Пробел не изменяется

def test_valid_phone_numbers():
    """
    Проверка корректных номеров телефонов.
    """
    assert is_phone_number("+1234567890") == True  # Международный номер с "+"
    assert is_phone_number("+123456") == True  # Международный номер с кодом страны
    assert is_phone_number("+123456789012345") == True  # Максимально возможный номер с "+" (15 цифр)

def test_invalid_phone_numbers():
    """
    Проверка некорректных номеров телефонов.
    """
    assert is_phone_number("+1") == False  # Слишком короткий номер с "+"
    assert is_phone_number("1") == False  # Слишком короткий номер без "+"
    assert is_phone_number("abcd1234") == False  # Строка с буквами
    assert is_phone_number("12345@67890") == False  # Номер с нецифровыми символами
    assert is_phone_number("1234567890123456") == False  # Слишком длинный номер (16 символов)
    assert is_phone_number("+1234567890123456") == False  # Слишком длинный номер с "+"
    
