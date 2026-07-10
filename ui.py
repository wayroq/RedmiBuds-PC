import sys
import os
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QSystemTrayIcon, QMenu)
from PyQt6.QtGui import QIcon, QPainter, QColor, QPen, QBrush, QFont, QPixmap, QPainterPath
from PyQt6.QtCore import Qt, QPoint, QRect, QTimer, QSettings, QLocale

class BatteryWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.left_bat = -1
        self.right_bat = -1
        self.case_bat = -1
        lang = QLocale.system().name()
        is_ru = lang.startswith("ru")
        self.status = "Поиск наушников..." if is_ru else "Searching for earbuds..."
        self.setMinimumSize(250, 350)

    def update_battery(self, left, right, case):
        self.left_bat = left
        self.right_bat = right
        self.case_bat = case
        self.update()

    def update_status(self, status):
        self.status = status
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Background
        painter.setBrush(QColor(30, 30, 30, 240))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 20, 20)

        # Text format
        pen = QPen(QColor(240, 240, 240))
        painter.setPen(pen)
        font = QFont("Segoe UI", 11)
        painter.setFont(font)

        # Draw Status
        painter.drawText(QRect(10, 15, 230, 30), Qt.AlignmentFlag.AlignCenter, self.status)

        # Draw Left Earbud
        self._draw_earbud(painter, 50, 80, self.left_bat, is_right=False)
        
        # Draw Right Earbud
        self._draw_earbud(painter, 150, 80, self.right_bat, is_right=True)

        # Draw Case
        self._draw_case(painter, 90, 210, self.case_bat)

    def _draw_earbud(self, painter, x, y, bat, is_right):
        # Draw earbud shape
        painter.setPen(QPen(QColor(240, 240, 240), 3))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        
        # Circle
        painter.drawEllipse(x, y, 40, 40)
        
        # Stem
        path = QPainterPath()
        if is_right:
            path.moveTo(x + 10, y + 35)
            path.lineTo(x + 15, y + 80)
            path.lineTo(x + 25, y + 80)
            path.lineTo(x + 30, y + 35)
        else:
            path.moveTo(x + 30, y + 35)
            path.lineTo(x + 25, y + 80)
            path.lineTo(x + 15, y + 80)
            path.lineTo(x + 10, y + 35)
            
        painter.drawPath(path)

        # Fill if we have battery
        if bat >= 0:
            fill_height = int(45 * (bat / 100))
            color = QColor(255, 80, 80, 150) if bat < 20 else QColor(100, 255, 100, 150)
            painter.setBrush(color)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(x + 10, y + 80 - fill_height, 20, fill_height)

        # Text
        painter.setPen(QPen(QColor(240, 240, 240)))
        font = QFont("Segoe UI", 12, QFont.Weight.Bold)
        painter.setFont(font)
        text = f"{bat}%" if bat >= 0 else "--%"
        painter.drawText(QRect(x, y + 90, 40, 30), Qt.AlignmentFlag.AlignCenter, text)

    def _draw_case(self, painter, x, y, bat):
        painter.setPen(QPen(QColor(240, 240, 240), 3))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        
        painter.drawRoundedRect(x, y, 70, 60, 15, 15)
        painter.drawLine(x, y + 25, x + 70, y + 25)

        if bat >= 0:
            fill_width = int(66 * (bat / 100))
            color = QColor(255, 80, 80, 150) if bat < 20 else QColor(100, 255, 100, 150)
            painter.setBrush(color)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(x + 2, y + 27, fill_width, 31, 13, 13)

        painter.setPen(QPen(QColor(240, 240, 240)))
        font = QFont("Segoe UI", 12, QFont.Weight.Bold)
        painter.setFont(font)
        text = f"{bat}%" if bat >= 0 else "--%"
        painter.drawText(QRect(x, y + 65, 70, 30), Qt.AlignmentFlag.AlignCenter, text)


class FloatingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(250, 350)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.battery_widget = BatteryWidget()
        self.layout.addWidget(self.battery_widget)
        self._drag_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self._drag_pos is not None:
            new_pos = event.globalPosition().toPoint() - self._drag_pos
            
            # Ограничиваем область перетаскивания (с учетом всех мониторов)
            min_x = min(s.geometry().left() for s in QApplication.screens()) - self.width() // 2
            max_x = max(s.geometry().right() for s in QApplication.screens()) - self.width() // 2
            min_y = min(s.geometry().top() for s in QApplication.screens()) - self.height() // 2
            max_y = max(s.geometry().bottom() for s in QApplication.screens()) - self.height() // 2
            
            new_x = max(min_x, min(new_pos.x(), max_x))
            new_y = max(min_y, min(new_pos.y(), max_y))
            
            self.move(new_x, new_y)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self._drag_pos is not None:
            settings = QSettings("RedmiBuds", "BatteryApp")
            settings.setValue("pos_x", self.pos().x())
            settings.setValue("pos_y", self.pos().y())
            self._drag_pos = None

    def show_at_cursor(self):
        settings = QSettings("RedmiBuds", "BatteryApp")
        if settings.contains("pos_x") and settings.contains("pos_y"):
            x = int(settings.value("pos_x"))
            y = int(settings.value("pos_y"))
        else:
            pos = QApplication.primaryScreen().geometry().bottomRight()
            x = pos.x() - self.width() - 20
            y = pos.y() - self.height() - 60
            
        # Проверяем, чтобы сохраненная позиция не оказалась за пределами экранов (например, при смене монитора)
        min_x = min(s.geometry().left() for s in QApplication.screens()) - self.width() // 2
        max_x = max(s.geometry().right() for s in QApplication.screens()) - self.width() // 2
        min_y = min(s.geometry().top() for s in QApplication.screens()) - self.height() // 2
        max_y = max(s.geometry().bottom() for s in QApplication.screens()) - self.height() // 2
        
        x = max(min_x, min(x, max_x))
        y = max(min_y, min(y, max_y))
            
        self.move(x, y)
        self.show()
        self.activateWindow()


class AppTrayIcon:
    def __init__(self, on_exit):
        self.app = QApplication.instance()
        self.window = FloatingWindow()
        
        self.tray = QSystemTrayIcon()
        
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setBrush(QColor(200, 200, 200))
        painter.drawEllipse(4, 4, 10, 24)
        painter.drawEllipse(18, 4, 10, 24)
        painter.end()
        
        self.icon = QIcon(pixmap)
        self.tray.setIcon(self.icon)
        
        self.menu = QMenu()
        
        # Определяем язык системы
        lang = QLocale.system().name()
        exit_text = "Выход" if lang.startswith("ru") else "Exit"
        
        exit_action = self.menu.addAction(exit_text)
        exit_action.triggered.connect(on_exit)
        
        self.tray.setContextMenu(self.menu)
        self.tray.activated.connect(self.on_tray_activated)
        self.tray.show()

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.window.isVisible():
                self.window.hide()
            else:
                self.window.show_at_cursor()

    def update_battery(self, left, right, case):
        self.window.battery_widget.update_battery(left, right, case)
        
        # Update tray tooltip
        tooltip = f"Redmi Buds\nL: {left if left>=0 else '--'}% | R: {right if right>=0 else '--'}% | Case: {case if case>=0 else '--'}%"
        self.tray.setToolTip(tooltip)
        
        # Draw dynamic icon
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        has_case = case >= 0
        has_left = left >= 0
        has_right = right >= 0
        
        # Layout metrics
        earbud_h = 18 if has_case else 24
        earbud_y = 4
        
        def get_color(bat):
            return QColor(255, 100, 100) if bat < 20 else QColor(100, 255, 100)
            
        def draw_bar(x, y, w, h, bat):
            painter.setBrush(QColor(80, 80, 80))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(x, y, w, h, 3, 3)
            if bat >= 0:
                fill = int(h * (bat / 100))
                painter.setBrush(get_color(bat))
                painter.drawRoundedRect(x, y + h - fill, w, fill, 3, 3)

        def draw_horizontal_bar(x, y, w, h, bat):
            painter.setBrush(QColor(80, 80, 80))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(x, y, w, h, 3, 3)
            if bat >= 0:
                fill = int(w * (bat / 100))
                painter.setBrush(get_color(bat))
                painter.drawRoundedRect(x, y, fill, h, 3, 3)

        # Draw left earbud
        if has_left:
            x_pos = 11 if not has_right else 4
            draw_bar(x_pos, earbud_y, 10, earbud_h, left)
            
        # Draw right earbud
        if has_right:
            x_pos = 11 if not has_left else 18
            draw_bar(x_pos, earbud_y, 10, earbud_h, right)
            
        # Draw case
        if has_case:
            draw_horizontal_bar(4, 24, 24, 6, case)
            
        painter.end()
        self.tray.setIcon(QIcon(pixmap))

    def update_status(self, status):
        self.window.battery_widget.update_status(status)
