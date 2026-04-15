from main import App
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 加载并应用QSS文件
    try:
        with open("resources/style.qss", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("QSS file not found. Continuing without stylesheet.")

    main_app = App()
    main_app.show()
    sys.exit(app.exec_())
