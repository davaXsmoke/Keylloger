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