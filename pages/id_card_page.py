import random

from PyQt5.QtGui import QIcon, QTextCharFormat, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QTextEdit, \
    QMessageBox, QTreeWidget, QTreeWidgetItem, QTreeWidgetItemIterator, QCalendarWidget, \
    QSpinBox, QToolButton, QMenu, QWidgetAction, QSizePolicy
from PyQt5.QtCore import Qt, QDate, QSize
import re
from faker import Faker
from utils.random_data_generator import export_data, BasePage, RandomDataGenerator, show_legal_warning, EXPORT_MAX_COUNT
from utils import data

fake = Faker('zh_CN')
provinces = data.provinces
random_data_generator = RandomDataGenerator()

class DateComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditable(True)
        self.setInsertPolicy(QComboBox.NoInsert)
        self.setCompleter(None)
        self.setStyleSheet("""
            QComboBox {
                border-radius: 6px;
                border: 1px solid #cccccc;
                padding: 3px 0px 3px 6px;
                color: #000000;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(resources/down_arrow.png);
                border: none;
            }
        """)

        self.lineEdit().setPlaceholderText("搜索生日 (YYYY.MM.DD)")
        self.lineEdit().textChanged.connect(self.validate_date)

        self.calendar = QCalendarWidget()
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendar.setGridVisible(True)
        self.calendar.setMinimumDate(QDate(1900, 1, 1))
        self.calendar.setMaximumDate(QDate.currentDate())
        self.calendar.clicked.connect(self.set_date_from_calendar)

        self.calendar.setStyleSheet("""
            QCalendarWidget {
                background-color: #FFFFFF;
                border: 1px solid #FFA500;
            }
            QCalendarWidget QAbstractItemView:enabled {
                color: #000000;
                background-color: #ffffff;
                selection-color: white;
                selection-background-color: #007bff;
            }
            QCalendarWidget QSpinBox#qt_calendar_yearedit {
                background: #ffffff;
                height: 34px;
                width: 125px;
                selection-background-color: #007bff;
            }
            QCalendarWidget QToolButton {
                background-color: #FFFFFF;
                height: 34px;
                width: 125px;
                color: #000000;
            }
            QCalendarWidget QToolButton:hover {
                border: 1px solid #007bff;
            }
            QCalendarWidget QToolButton::menu-indicator#qt_calendar_monthbutton {
                subcontrol-position: right center;
                subcontrol-origin: padding;
            }
            QCalendarWidget QToolButton QMenu {
                background-color: #FFFFFF;
                width: 125px;
                border: 1px solid #007bff;
            }
            QCalendarWidget QToolButton QMenu::item:selected {
                color: #FFFFFF;
                background: #007bff;
            }
        """)

        format = QTextCharFormat()
        format.setForeground(QColor(Qt.black))
        self.calendar.setWeekdayTextFormat(Qt.Saturday, format)
        self.calendar.setWeekdayTextFormat(Qt.Sunday, format)

        toolbtn_list = self.calendar.findChildren(QToolButton)
        for btn in toolbtn_list:
            btn.setCursor(Qt.PointingHandCursor)

        size = QSize(32, 32)
        prev_month_btn = self.calendar.findChild(QToolButton, "qt_calendar_prevmonth")
        prev_month_btn.setIcon(QIcon("resources/left_ar.png"))
        prev_month_btn.setIconSize(size)

        next_month_btn = self.calendar.findChild(QToolButton, "qt_calendar_nextmonth")
        next_month_btn.setIcon(QIcon("resources/right_ar.png"))
        next_month_btn.setIconSize(size)

        calendar_action = QWidgetAction(self)
        calendar_action.setDefaultWidget(self.calendar)

        self.dropdown_menu = QMenu(self)
        self.dropdown_menu.addAction(calendar_action)

    def showPopup(self):
        self.dropdown_menu.exec_(self.mapToGlobal(self.rect().bottomLeft()))

    def set_date_from_calendar(self, date):
        self.setEditText(date.toString("yyyy.MM.dd"))

    def validate_date(self, text):
        if not text:
            self.setStyleSheet("""
                QComboBox {
                    border-radius: 6px;
                    border: 1px solid #cccccc;
                    padding: 3px 0px 3px 6px;
                    color: #000000;
                }
            """)
            return

        if re.match(r'^\d{4}\.\d{2}\.\d{2}$', text):
            date = QDate.fromString(text, "yyyy.MM.dd")
            if date.isValid():
                self.setStyleSheet("""
                    QComboBox {
                        border-radius: 6px;
                        border: 1px solid #cccccc;
                        padding: 3px 0px 3px 6px;
                        color: #000000;
                    }
                """)
                self.calendar.setSelectedDate(date)  # 同步更新日历
            else:
                self.setStyleSheet("""
                    QComboBox {
                        border-radius: 6px;
                        border: 1px solid red;
                        padding: 3px 0px 3px 6px;
                        color: #000000;
                    }
                """)
        else:
            self.setStyleSheet("""
                QComboBox {
                    border-radius: 6px;
                    border: 1px solid red;
                    padding: 3px 0px 3px 6px;
                    color: #000000;
                }
            """)

    def clear_date(self):
        self.setEditText("")
        self.calendar.setSelectedDate(QDate())  # 清空日历选择

class IDCardPage(BasePage):

    def __init__(self):
        super().__init__()
        self.district_code = None  # 初始化district_code
        self.birthdate = None  # 初始化生日
        self.data = None  # 初始化self.data

    def create_widgets(self):
        self.layout.addWidget(QLabel("生成随机身份证号"))

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

        form_layout.addWidget(QLabel("生日 (非必填):"))
        self.birthdate_entry = DateComboBox()
        form_layout.addWidget(self.birthdate_entry)

        self.clear_birthdate_button = QPushButton("清除生日选择")
        self.clear_birthdate_button.clicked.connect(self.birthdate_entry.clear_date)
        form_layout.addWidget(self.clear_birthdate_button)

        form_layout.addWidget(QLabel("性别 (男/女，非必填):"))
        self.gender_entry = QComboBox()
        self.gender_entry.addItems(["男", "女"])
        self.gender_entry.setCurrentIndex(-1)  # 设置为不选中任何值
        form_layout.addWidget(self.gender_entry)

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

            # 获取输入的生日
            birthdate_text = self.birthdate_entry.currentText()
            birthdate = QDate.fromString(birthdate_text, "yyyy.MM.dd") if re.match(r'^\d{4}\.\d{2}\.\d{2}$', birthdate_text) else None

            gender = self.gender_entry.currentText() if self.gender_entry.currentIndex() != -1 else None

            # 如果没有选择区划代码，每条数据的区划代码都是随机生成的
            self.data = [self.generate_id_card(
                self.district_code if self.district_code else random_data_generator.get_random_district_code(provinces), birthdate,
                gender) for _ in range(num)]

            self.display_data()
            # QMessageBox.information(self, "生成成功", f"成功生成 {num} 条随机身份证号")
        except ValueError:
            QMessageBox.critical(self, "输入错误", "请输入有效的数字")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"生成数据时发生错误: {e}")

    def generate_id_card(self, district=None, birthdate=None, gender=None):
        try:
            # 确保区划代码为6位数字
            district_code = str(district).zfill(6)
            id_card = district_code

            # 确保出生日期为8位数字
            if birthdate:
                id_card += birthdate.toString("yyyyMMdd")
            else:
                id_card += fake.date(pattern="%Y%m%d", end_datetime=None)

            # 确保顺序码和性别码正确生成
            seq_code = str(fake.random_number(digits=2, fix_len=True)).zfill(2)
            if gender:
                if gender == "男":
                    gender_code = random.choice(range(1, 10, 2))
                elif gender == "女":
                    gender_code = random.choice(range(0, 10, 2))
            else:
                gender_code = random.choice(range(0, 10))

            id_card += seq_code + str(gender_code)

            # 计算校验码
            weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
            check_codes = '10X98765432'
            total = sum(int(id_card[i]) * weights[i] for i in range(17))
            check_code = check_codes[total % 11]
            id_card += check_code

            # 验证生成的身份证号码是否符合正则表达式
            if not re.match(r'^\d{6}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]$', id_card):
                raise ValueError("生成的身份证号码不合法")

            # 返回生成的身份证号码
            return id_card
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
