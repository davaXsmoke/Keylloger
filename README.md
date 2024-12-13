
# Документация к скрипту

## Общее описание

Этот скрипт представляет собой функциональную систему для логирования нажатий клавиш с возможностью работы на нескольких операционных системах (Windows и macOS). Основные возможности:
- Настройка автозапуска и обеспечение сохранности скрипта в системе.
- Функционал кейлоггера для записи пользовательских вводов, включая определение электронной почты, паролей и номеров телефонов.
- Конвертация раскладок клавиатуры между русской и английской.
- Отправка отчетов на электронную почту.
- Динамическая установка необходимых зависимостей.

---

## Функции

### 1. unpack_to_system32
- Копирует скрипт в папку System32 на Windows.
- Проверяет наличие прав администратора.

### 2. setup_autostart_windows
- Добавляет скрипт в реестр Windows для автозапуска при старте системы.

### 3. unpack_to_macos_directory
- Копирует скрипт в папку `/usr/local/bin` на macOS, делая его исполняемым.

### 4. setup_autostart_unix
- Создает и загружает `.plist` файл в папке `LaunchAgents` на macOS для автозапуска скрипта.

### 5. install_and_import
- Динамически устанавливает и импортирует необходимые Python-пакеты.

### 6. get_active_window
- Получает заголовок текущего активного окна для Windows и macOS.

### 7. get_current_layout
- Определяет текущую раскладку клавиатуры для Windows или macOS.

### 8. convert_to_english / convert_to_russian
- Конвертирует символы между русской и английской раскладками, включая символы с модификатором Shift.

### 9. is_phone_number / is_email_or_username_or_phone / is_probable_password
- Определяет, является ли строка телефонным номером, email, логином или паролем.

### 10. process_inputs
- Обрабатывает пользовательский ввод, связывает его с активным окном и сохраняет данные.

### 11. on_press / on_release
- Обрабатывает события нажатия и отпускания клавиш, включая специальные символы и конвертацию раскладок.

### 12. Класс Keylogger
- Управляет основным функционалом кейлоггера, включая отправку отчетов на почту и сохранение логов.

---

## Настройки

### Почта
- `EMAIL_ADDRESS`: Электронный адрес, используемый для отправки отчетов.
- `EMAIL_PASSWORD`: Пароль для аутентификации.

### Константы
- `SEND_REPORT_EVERY`: Интервал (в секундах) между отправкой отчетов.

---

## Использование

Запустите скрипт с правами администратора:
```bash
python keylloger.py
```

Убедитесь, что все зависимости Python установлены.

---

## Заметки по безопасности
- Этот скрипт должен использоваться только в этических и авторизованных целях.
- Перед использованием скрипта убедитесь в наличии согласия пользователей и соблюдении всех применимых законов.

---

## Известные проблемы и их решение

### Ошибки прав доступа
- Используйте `sudo` на macOS или запустите от имени Администратора на Windows.

### Отсутствие зависимостей
- Скрипт автоматически устанавливает зависимости. Убедитесь в наличии активного интернет-соединения.

---

