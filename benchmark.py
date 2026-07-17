import timeit
import sys
import os
from PyQt6.QtWidgets import QApplication

os.environ['QT_QPA_PLATFORM'] = 'offscreen'
app = QApplication(sys.argv)

def original():
    min_x = min(s.geometry().left() for s in QApplication.screens())
    max_x = max(s.geometry().right() for s in QApplication.screens())
    min_y = min(s.geometry().top() for s in QApplication.screens())
    max_y = max(s.geometry().bottom() for s in QApplication.screens())

def optimized():
    screens = QApplication.screens()
    min_x = min(s.geometry().left() for s in screens)
    max_x = max(s.geometry().right() for s in screens)
    min_y = min(s.geometry().top() for s in screens)
    max_y = max(s.geometry().bottom() for s in screens)

print("Original:", timeit.timeit(original, number=10000))
print("Optimized:", timeit.timeit(optimized, number=10000))
