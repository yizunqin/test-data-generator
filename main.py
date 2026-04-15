# coding=utf-8
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton
from pages.increment_page import IncrementPage
from pages.merge_files_page import MergeFilesPage
from pages.name_page import NamePage
from pages.pass_word_generation_page import PasswordGeneratorPage
from pages.phone_number_page import PhoneNumberPage
from pages.id_card_page import IDCardPage
from pages.credit_code_page import CreditCodePage
from pages.random_data_page import RandomDataPage
from pages.welcome_page import WelcomePage
import os
from utils.random_data_generator import BasePage


class App(QMainWindow, BasePage):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("测试数据生成工具")
        self.setGeometry(100, 100, 1000, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QHBoxLayout(self.central_widget)

        self.navbar = QVBoxLayout()
        self.layout.addLayout(self.navbar)

        self.container = QVBoxLayout()
        self.layout.addLayout(self.container)

        self.pages = {}
        for Page in (WelcomePage, IDCardPage, CreditCodePage, RandomDataPage, PhoneNumberPage, NamePage,
                     IncrementPage, PasswordGeneratorPage, MergeFilesPage):
            page = Page()
            self.pages[Page.__name__] = page
            page.hide()  # 初始化时隐藏页面
            self.container.addWidget(page)

        self.create_navbar()
        self.show_page("WelcomePage")  # 初始显示页面

    def create_navbar(self):
        self.add_nav_button("欢迎使用本工具", lambda: self.show_page("WelcomePage"), 'resources/welcome_icon.png')
        self.add_nav_button("生成随机身份证号", lambda: self.show_page("IDCardPage"), 'resources/IDCard.png')
        self.add_nav_button("生成统一社会信用代码", lambda: self.show_page("CreditCodePage"), 'resources/CreditCode.png')
        self.add_nav_button("生成随机数据", lambda: self.show_page("RandomDataPage"), 'resources/RandomData.png')
        self.add_nav_button("生成随机手机号码", lambda: self.show_page("PhoneNumberPage"), 'resources/PhoneNumber.png')
        self.add_nav_button("生成随机姓名", lambda: self.show_page("NamePage"), 'resources/Name.png')
        self.add_nav_button("生成自增数据", lambda: self.show_page("IncrementPage"), 'resources/Increment.png')  # 新增的生成自增数据按钮
        self.add_nav_button("生成随机密码", lambda: self.show_page("PasswordGeneratorPage"),
                            'resources/Password.png')  # 新增的生成随机密码按钮
        self.add_nav_button("合并文件", lambda: self.show_page("MergeFilesPage"), 'resources/MergeFiles.png')  # 新增的合并文件按钮

    def add_nav_button(self, label, callback, icon_path):
        button = QPushButton(label)
        button.clicked.connect(callback)
        button.setIcon(QIcon(icon_path))
        button.setStyleSheet("QPushButton { text-align: left; padding-left: 10px; }")  # 设置图标靠左
        self.navbar.addWidget(button)

    def show_page(self, page_name):
        for page in self.pages.values():
            page.hide()
        self.pages[page_name].show()
        if hasattr(self.pages[page_name], 'reset_fields'):
            self.pages[page_name].reset_fields()  # 如果页面有reset_fields方法则调用


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 获取当前执行路径
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    # 加载样式表
    style_path = os.path.join(base_path, 'resources/style.qss')
    try:
        with open(style_path, 'r') as f:
            app.setStyleSheet(f.read())
    except Exception as e:
        print(f"Failed to load stylesheet: {e}")

    main_app = App()
    main_app.show()
    sys.exit(app.exec_())
