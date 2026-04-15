from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QTextEdit, \
    QMessageBox, QScrollArea
from utils.random_data_generator import RandomDataGenerator, export_data, BasePage, show_legal_warning, EXPORT_MAX_COUNT


class RandomDataPage(BasePage):
    def __init__(self):
        self.data_generator = RandomDataGenerator()
        super().__init__()
        self.data = None  # 初始化self.data

    def create_widgets(self):
        self.layout.addWidget(QLabel("生成随机数据"))

        # form_layout = QVBoxLayout()
        # self.layout.addLayout(form_layout)
        #
        # form_layout.addWidget(QLabel("请输入需要生成的数量:"))
        # self.num_entry = QLineEdit()
        # form_layout.addWidget(self.num_entry)

        form_layout = QVBoxLayout()
        self.layout.addLayout(form_layout)
        form_layout.addWidget(QLabel("请输入需要生成的数量:"))

        self.num_entry = QLineEdit()

        # 使用 placeholder 来设置默认显示文本
        self.num_entry.setPlaceholderText("10")  # 显示默认值为10

        # 如果你想要在用户进入输入框时清除 placeholder，也可以实现
        self.num_entry.installEventFilter(self)  # 安装事件过滤器，用于监控焦点事件

        form_layout.addWidget(self.num_entry)

        form_layout.addWidget(QLabel("请选择数据类型:"))
        self.data_type_combo = QComboBox()
        self.data_type_combo.setEditable(False)
        self.data_type_combo.setPlaceholderText("请选择数据类型")
        form_layout.addWidget(self.data_type_combo)

        button_layout = QHBoxLayout()
        self.layout.addLayout(button_layout)

        generate_button = QPushButton("生成")
        generate_button.clicked.connect(self.generate_data)
        button_layout.addWidget(generate_button)
        generate_button.setIcon(QIcon('./resources/generate_button.png'))  # 设置按钮图标
        generate_button.setStyleSheet("QPushButton { text-align: left; padding-left: 10px; }")  # 设置图标靠左

        export_button = QPushButton("导出")
        export_button.clicked.connect(lambda: self.export_data(self.data))
        button_layout.addWidget(export_button)
        export_button.setIcon(QIcon('./resources/export_button.png'))  # 设置按钮图标
        export_button.setStyleSheet("QPushButton { text-align: left; padding-left: 10px; }")  # 设置图标靠左

        reset_button = QPushButton("重置")
        reset_button.clicked.connect(self.reset_fields)
        button_layout.addWidget(reset_button)
        reset_button.setIcon(QIcon('./resources/reset_button.png'))  # 设置按钮图标
        reset_button.setStyleSheet("QPushButton { text-align: left; padding-left: 10px; }")  # 设置图标靠左

        # 使用QScrollArea来支持大数据量的展示
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setStyleSheet("QTextEdit { font-size: 14pt; }")
        self.layout.addWidget(self.result_text, stretch=1)

        self.init_data_type_combo()

        # 调用基类方法添加公司logo
        self.add_logo()

        # self.init_data_type_combo()

    def init_data_type_combo(self):
        self.data_type_combo.addItems(["电子邮件", "地址"])

    def generate_data(self):
        if not show_legal_warning(self):
            return
        try:
            num_text = self.num_entry.text().strip()  # 获取输入框的内容并去掉空白
            num = int(num_text) if num_text else 10  # 如果输入框为空，默认生成10个
            if num > EXPORT_MAX_COUNT:
                QMessageBox.critical(self, "数量超限", f"单次生成数量上限为 {EXPORT_MAX_COUNT} 条")
                return
            data_type = self.data_type_combo.currentText()
            if data_type == "电子邮件":
                self.data = [self.data_generator.generate_email() for _ in range(num)]
            elif data_type == "地址":
                self.data = [self.data_generator.generate_address() for _ in range(num)]
            else:
                QMessageBox.critical(self, "输入错误", "请选择有效的数据类型")
                return
            self.display_data()
            # QMessageBox.information(self, "生成成功", f"成功生成 {num} 条随机{data_type}")
        except ValueError:
            QMessageBox.critical(self, "输入错误", "请输入有效的数字")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"生成数据时发生错误: {e}")

    def display_data(self):
        try:
            self.result_text.clear()
            for item in self.data:
                self.result_text.append(item)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"显示数据时发生错误: {e}")

    def export_data(self, data):
        export_data(self, data)  # 将当前窗口传递给export_data函数

