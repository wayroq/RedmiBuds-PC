import sys
from PyQt6.QtWidgets import QApplication
from ui import AppTrayIcon
from bluetooth_manager import BluetoothManager

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    tray_ui = AppTrayIcon(on_exit=app.quit)

    def on_battery(left, right, case):
        tray_ui.update_battery(left, right, case)

    def on_status(status):
        tray_ui.update_status(status)

    bt_manager = BluetoothManager(on_battery_update=on_battery, on_status_update=on_status)

    # Connect UI buttons to BluetoothManager
    tray_ui.window.battery_widget.on_noise_control = bt_manager.set_noise_control

    bt_manager.start()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
