from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QFileDialog, QCheckBox, QLabel,
    QScrollArea, QMessageBox, QGroupBox, QPlainTextEdit,
    QDialog, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon
from .dialogs import AddTemplateDialog


class MainWindowUI(QMainWindow):
    """主窗口 UI 类"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("批量文件夹创建工具")
        self.setWindowIcon(QIcon("logofast_1773751792401.png"))
        self.resize(1000, 700) 
        
        # 容器
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(30, 25, 30, 25)
        self.main_layout.setSpacing(20)

        # 1. 顶部标题
        self.setup_header()

        # 2. 中间主体布局（左右结构）
        self.content_layout = QHBoxLayout()
        self.content_layout.setSpacing(25)
        
        # --- 左侧列：路径 + 模板 + 预览按钮 ---
        self.left_column_layout = QVBoxLayout()
        self.left_column_layout.setSpacing(20)
        
        self.setup_path_section()
        self.setup_template_section()
        
        # 预览按钮 (左侧底部)
        self.preview_btn = QPushButton("👀 预览生成的目录")
        self.preview_btn.setMinimumHeight(48)
        self.left_column_layout.addWidget(self.preview_btn)
        
        # --- 右侧列：日志 + 执行按钮 ---
        self.right_column_layout = QVBoxLayout()
        self.right_column_layout.setSpacing(20)
        
        self.setup_log_section()
        self.right_column_layout.addWidget(self.log_group)
        
        # 执行按钮 (右侧底部)
        self.create_btn = QPushButton("🚀 执行批量创建")
        self.create_btn.setObjectName("PrimaryButton")
        self.create_btn.setMinimumHeight(48)
        self.right_column_layout.addWidget(self.create_btn)
        
        # 组装中间部分
        self.content_layout.addLayout(self.left_column_layout, 2)
        self.content_layout.addLayout(self.right_column_layout, 3)
        
        self.main_layout.addLayout(self.content_layout)

        self.checkboxes = {}

    def setup_header(self):
        """顶部标题和描述"""
        header_layout = QVBoxLayout()
        header_layout.setSpacing(2)
        title_label = QLabel("📁 批量文件夹创建工具")
        title_label.setStyleSheet("font-size: 22px; font-weight: 600; color: #1a1a1a;")
        desc_label = QLabel("快速部署项目目录结构，支持从 JSON 文件同步模板。")
        desc_label.setStyleSheet("font-size: 13px; color: #666;")
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(desc_label)
        self.main_layout.addLayout(header_layout)

    def setup_path_section(self):
        """路径选择区域"""
        path_group = QGroupBox("1. 设置目标工作区")
        path_layout = QHBoxLayout()
        path_layout.setContentsMargins(15, 20, 15, 15)
        path_layout.setSpacing(10)

        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("选择或输入目标根目录...")
        self.path_input.setMinimumHeight(36)
        
        self.browse_btn = QPushButton("浏览...")
        self.browse_btn.setMinimumHeight(36)
        
        path_layout.addWidget(self.path_input, 1)
        path_layout.addWidget(self.browse_btn)
        path_group.setLayout(path_layout)
        self.left_column_layout.addWidget(path_group)

    def setup_template_section(self):
        """模板选择区域"""
        template_group = QGroupBox("2. 选择项目模板")
        template_layout = QVBoxLayout()
        template_layout.setContentsMargins(15, 20, 15, 15)
        template_layout.setSpacing(12)

        # 模板管理的操作按钮
        manage_layout = QHBoxLayout()
        manage_layout.setSpacing(8)
        
        self.add_btn = QPushButton("✨ 新建")
        self.del_btn = QPushButton("🗑 删除")
        self.refresh_btn = QPushButton("🔄 刷新")
        
        for btn in [self.add_btn, self.del_btn, self.refresh_btn]:
            btn.setMinimumHeight(32)

        manage_layout.addWidget(self.add_btn)
        manage_layout.addWidget(self.del_btn)
        manage_layout.addStretch()
        manage_layout.addWidget(self.refresh_btn)
        template_layout.addLayout(manage_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setStyleSheet("background: transparent;")
        
        self.scroll_content = QWidget()
        self.scroll_content.setObjectName("ScrollContent")
        self.scroll_content.setStyleSheet("background: transparent;")
        
        self.template_list_layout = QVBoxLayout(self.scroll_content)
        self.template_list_layout.setSpacing(10)
        self.template_list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.scroll_area.setWidget(self.scroll_content)
        template_layout.addWidget(self.scroll_area)
        
        template_group.setLayout(template_layout)
        self.left_column_layout.addWidget(template_group)

    def setup_log_section(self):
        """日志操作区域"""
        self.log_group = QGroupBox("3. 操作日志与预览")
        log_layout = QVBoxLayout()
        log_layout.setContentsMargins(15, 20, 15, 15)

        self.log_area = QPlainTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setObjectName("LogArea")
        self.log_area.setPlaceholderText("日志信息将显示在这里...")
        self.log_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        log_layout.addWidget(self.log_area)
        self.log_group.setLayout(log_layout)



    # 封装通用的 UI 操作方法
    def show_message(self, title, text, type="info"):
        if type == "error":
            QMessageBox.critical(self, title, text)
        elif type == "warning":
            QMessageBox.warning(self, title, text)
        else:
            QMessageBox.information(self, title, text)

    def select_directory_dialog(self):
        return QFileDialog.getExistingDirectory(self, "选择目标工作区目录")
