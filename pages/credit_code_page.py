from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QTextEdit, \
    QMessageBox, QTreeWidget, QTreeWidgetItem, QTreeWidgetItemIterator, QSizePolicy
from PyQt5.QtCore import Qt
from utils.social_credit_code_generator import SocialCreditCodeGenerator
from utils.random_data_generator import export_data, BasePage, RandomDataGenerator, show_legal_warning, EXPORT_MAX_COUNT
from utils import data

# 示例区划数据定义
provinces = data.provinces
random_data_generator = RandomDataGenerator()
registration_departments = data.registration_departments
institution_types = data.institution_types

class CreditCodePage(BasePage):
    def __init__(self):
        super().__init__()
        self.scc = SocialCreditCodeGenerator()
        self.district_code = None
        self.init_registration_department()  # 初始化登记管理部门
        self.data = None  # 初始化self.data

    def create_widgets(self):
        self.layout.addWidget(QLabel("生成统一社会信用代码"))

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

        form_layout.addWidget(QLabel("区划 (通过下方树状选择，非必填):"))
        self.district_search_entry = QLineEdit()
        self.district_search_entry.setPlaceholderText("搜索区划")
        self.district_search_entry.textChanged.connect(self.on_district_search_entry_changed)
        form_layout.addWidget(self.district_search_entry)

        self.district_tree = QTreeWidget()
        self.district_tree.setHeaderHidden(True)
        self.district_tree.itemClicked.connect(self.select_district)
        form_layout.addWidget(self.district_tree)

        self.district_clear_button = QPushButton("清除区划选择")
        self.district_clear_button.clicked.connect(self.clear_district_selection)
        form_layout.addWidget(self.district_clear_button)

        form_layout.addWidget(QLabel("登记管理部门(非必填):"))
        self.registration_department_combo = QComboBox()
        self.registration_department_combo.setEditable(False)
        self.registration_department_combo.setPlaceholderText("请选择登记管理部门")
        self.registration_department_combo.currentIndexChanged.connect(self.update_institution_types)
        form_layout.addWidget(self.registration_department_combo)

        form_layout.addWidget(QLabel("机构类别 (非必填):"))
        self.institution_type_combo = QComboBox()
        self.institution_type_combo.setEditable(False)
        self.institution_type_combo.setPlaceholderText("请选择机构类别")
        form_layout.addWidget(self.institution_type_combo)

        self.registration_clear_button = QPushButton("清除登记管理部门和机构类别选择")
        self.registration_clear_button.clicked.connect(self.clear_registration_and_institution_selection)
        form_layout.addWidget(self.registration_clear_button)

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

        # # 使用QScrollArea来支持大数据量的展示
        # self.result_text = QTextEdit()
        # self.result_text.setReadOnly(True)
        # self.layout.addWidget(self.result_text, stretch=1)

        # 设置QTextEdit显示区域的大小
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)

        # 设置固定高度为300像素
        self.result_text.setFixedHeight(300)

        # 设置水平和垂直都可以扩展的尺寸策略
        self.result_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.result_text.setStyleSheet("QTextEdit { font-size: 14pt; }")

        self.layout.addWidget(self.result_text, stretch=3)

        # 调用基类方法添加公司logo
        self.add_logo()

        self.populate_district_tree(provinces)

    def populate_district_tree(self, data, parent=None):
        for province, province_data in data.items():
            province_item = QTreeWidgetItem([province])
            province_item.setData(0, Qt.UserRole, province_data["province_code"])
            if parent:
                parent.addChild(province_item)
            else:
                self.district_tree.addTopLevelItem(province_item)

            for city, city_data in province_data.items():
                if city == "province_code":
                    continue

                city_item = QTreeWidgetItem([city])
                city_item.setData(0, Qt.UserRole, city_data["city_code"])
                province_item.addChild(city_item)

                for district, district_code in city_data.items():
                    if district == "city_code":
                        continue

                    district_item = QTreeWidgetItem([district])
                    district_item.setData(0, Qt.UserRole, district_code)
                    city_item.addChild(district_item)

    def on_district_search_entry_changed(self, text):
        if not text:
            self.district_code = None  # 清空输入框时，将district_code设置为None
        self.search_district(text)

    def search_district(self, text):
        iterator = QTreeWidgetItemIterator(self.district_tree, QTreeWidgetItemIterator.All)
        while iterator.value():
            item = iterator.value()
            item.setHidden(True)
            iterator += 1

        if text:
            iterator = QTreeWidgetItemIterator(self.district_tree, QTreeWidgetItemIterator.All)
            while iterator.value():
                item = iterator.value()
                if text.lower() in item.text(0).lower():
                    item.setHidden(False)
                    parent = item.parent()
                    while parent:
                        parent.setHidden(False)
                        parent.setExpanded(True)
                        parent = parent.parent()
                iterator += 1
        else:
            iterator = QTreeWidgetItemIterator(self.district_tree, QTreeWidgetItemIterator.All)
            while iterator.value():
                item = iterator.value()
                item.setHidden(False)
                item.setExpanded(False)
                iterator += 1

    def select_district(self, item):
        self.district_search_entry.setText(item.text(0))
        self.district_code = item.data(0, Qt.UserRole)

    def clear_district_selection(self):
        self.district_search_entry.clear()
        self.district_code = None

    def init_registration_department(self):
        for key in registration_departments.keys():
            self.registration_department_combo.addItem(key)

    def update_institution_types(self):
        selected_department = self.registration_department_combo.currentText()
        self.institution_type_combo.clear()
        if selected_department in registration_departments:
            self.institution_type_combo.addItems(institution_types[registration_departments[selected_department]])

    def clear_registration_and_institution_selection(self):
        self.registration_department_combo.setCurrentIndex(-1)
        self.institution_type_combo.clear()

    def generate_data(self):
        if not show_legal_warning(self):
            return
        try:
            # 获取输入框的内容，若为空则使用默认值 10
            num_text = self.num_entry.text().strip()  # 获取输入框的内容并去掉空白
            num = int(num_text) if num_text else 10  # 如果输入框为空，默认生成10个

            if num <= 0:
                QMessageBox.critical(self, "输入错误", "请输入正整数")
                return
            if num > EXPORT_MAX_COUNT:
                QMessageBox.critical(self, "数量超限", f"单次生成数量上限为 {EXPORT_MAX_COUNT} 条")
                return

            registration_department_name = self.registration_department_combo.currentText() or None
            institution_type_name = self.institution_type_combo.currentText() or None

            if registration_department_name and registration_department_name in registration_departments:
                registration_department = registration_departments[registration_department_name]
            else:
                registration_department = None

            if institution_type_name:
                institution_type = None
                for key, values in institution_types.items():
                    for value in values:
                        if institution_type_name == value:
                            institution_type = value[0]
                            break

                if institution_type is None:
                    QMessageBox.critical(self, "输入错误", "请选择正确的机构类别")
                    return
            else:
                institution_type = None

            self.data = [
                self.generate_credit_code(
                    self.district_code if self.district_code else random_data_generator.get_random_district_code(provinces),
                    registration_department,
                    institution_type
                )
                for _ in range(num)
            ]

            self.display_data()
            valid_codes = [code for code in self.data if self.scc.validate_social_credit_code(code) == '校验通过']
            invalid_codes = set(self.data) - set(valid_codes)
            # QMessageBox.information(self, "生成成功", f"成功生成 {len(valid_codes)} 条有效统一社会信用代码\n{len(invalid_codes)} 条无效代码")
        except ValueError:
            QMessageBox.critical(self, "输入错误", "请输入有效的数字")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"生成数据时发生错误: {e}")

    def generate_credit_code(self, district=None, registration_department=None, institution_type=None):
        try:
            district_code = district if district else random_data_generator.get_random_district_code(provinces)
            return self.scc.generate_social_credit_code(district_code, registration_department, institution_type)
        except Exception as e:
            raise

    def display_data(self):
        try:
            self.result_text.clear()
            for item in self.data:
                self.result_text.append(item)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"显示数据时发生错误: {e}")

    def export_data(self, data):
        export_data(self, data)  # 将当前窗口传递给export_data函数
