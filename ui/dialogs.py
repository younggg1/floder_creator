from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QTextEdit, QLabel, QFormLayout
)
from PyQt6.QtCore import Qt


class AddTemplateDialog(QDialog):
    """添加模板对话框"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("新增模板")
        self.setMinimumWidth(450)
        self.setMinimumHeight(400)
        self.setup_ui()

    def setup_ui(self):
        # 垂直主布局且边缘有很大 padding
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # 头部标题说明
        title_label = QLabel("✨ 定义新模板")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #0067c0;")
        layout.addWidget(title_label)

        # 表单区域
        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(12)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("例如: Flutter Pro")
        form_layout.addRow("🚀 模板名称:", self.name_input)

        self.paths_input = QTextEdit()
        self.paths_input.setAcceptRichText(False)
        self.paths_input.setPlaceholderText( r"每行一个路径，例如：src/components")
        form_layout.addRow("📁 目录结构:", self.paths_input)


        layout.addLayout(form_layout)

        # 辅助说明
        help_label = QLabel("提示：每行输入一个文件夹路径，多级目录用斜杠 / 分隔。")
        help_label.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(help_label)

        # 按钮
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        btn_layout.addStretch()
        
        self.save_btn = QPushButton("保存模板")
        self.save_btn.setObjectName("PrimaryButton")
        self.save_btn.clicked.connect(self.accept)
        
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.save_btn)
        layout.addLayout(btn_layout)

    def get_data(self):
        """获取输入并格式化"""
        name = self.name_input.text().strip()
        paths_text = self.paths_input.toPlainText().strip()
        paths = [p.strip() for p in paths_text.split('\n') if p.strip()]
        return name, paths
