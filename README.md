# RedmiBuds-PC

<p align="center">
  <img src="https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge" alt="License" />
</p>

*Read this in other languages: [English](#english) | [Русский](#русский)*

---

## Русский

Стильное и легкое приложение для Windows, которое отображает уровень заряда наушников Redmi Buds 6 (и кейса) прямо в системном трее. 

### Особенности
* 🔋 **Детальный мониторинг**: Отдельный заряд для Левого, Правого наушника и Кейса.
* 🖥️ **Красивый UI**: Плавающее полупрозрачное окно с анимациями в стиле Windows 11.
* ✨ **Умный трей**: Иконка в системном трее динамически меняется в зависимости от того, сколько наушников подключено, и показывает заряд кейса.
* 🌍 **Мультиязычность**: Автоматическая адаптация под язык системы (Русский / Английский).
* 💾 **Запоминание позиции**: Перетащите окно куда угодно, и оно запомнит свое положение.

### 🚀 В планах (To-Do)
* **Управление режимами**: Переключение между Активным шумоподавлением (ANC), Прозрачностью и Обычным режимом.
* **Настройка жестов**: Полная кастомизация сенсорных нажатий на наушниках.
* **Поиск наушников**: Воспроизведение звукового сигнала для поиска затерявшегося наушника.
* **Системные настройки**: Управление авто-обнаружением уха и мультипоинтом (двойное соединение).
* **Звуковые эффекты**: Настройка пространственного звучания и баланса звука.

### Как использовать (Для пользователей)
1. Перейдите во вкладку [Releases](../../releases).
2. Скачайте последний `.exe` файл.
3. Запустите его (программа автоматически появится в трее возле часов).
4. Наслаждайтесь! Программу можно добавить в автозагрузку Windows.

### Сборка из исходников (Для разработчиков)
1. Убедитесь, что у вас установлен Python 3.10 или новее.
2. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/ВАШ_НИК/RedmiBuds-PC.git
   cd RedmiBuds-PC
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Запуск и сборка EXE:
   ```bash
   python main.py
   pip install pyinstaller
   pyinstaller --noconsole --onefile --windowed --name RedmiBudsPC main.py
   ```

---

## English

A stylish and lightweight Windows application that displays the battery level of your Redmi Buds 6 (and case) right in the system tray.

### Features
* 🔋 **Detailed Monitoring**: Separate battery levels for the Left earbud, Right earbud, and Case.
* 🖥️ **Beautiful UI**: A floating translucent window with Windows 11 style aesthetics.
* ✨ **Smart Tray**: The system tray icon dynamically updates based on how many earbuds are connected and shows the case battery.
* 🌍 **Multilingual**: Automatically adapts to your system language (English / Russian).
* 💾 **Position Memory**: Drag the window anywhere, and it will remember its position.

### 🚀 Planned Features (To-Do)
* **Noise Control**: Toggle between Active Noise Cancellation (ANC), Transparency mode, and Off.
* **Gestures Customization**: Full control over touch actions on the earbuds.
* **Find My Earbuds**: Play a loud sound to locate a missing earbud.
* **System Settings**: Toggle in-ear detection and multipoint (dual device) connection.
* **Sound Effects**: Customize spatial audio and sound balance.

### How to Use (For Users)
1. Go to the [Releases](../../releases) tab.
2. Download the latest `.exe` file.
3. Run it (the app will automatically appear in your system tray).
4. Enjoy! You can add the program to Windows startup.

### Build from Source (For Developers)
1. Make sure you have Python 3.10 or newer installed.
2. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/RedmiBuds-PC.git
   cd RedmiBuds-PC
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run and build EXE:
   ```bash
   python main.py
   pip install pyinstaller
   pyinstaller --noconsole --onefile --windowed --name RedmiBudsPC main.py
   ```

---

## License / Лицензия
This project is licensed under the MIT License - see the `LICENSE` file for details.
