import sys
from PyQt6.QtWidgets import QApplication, QCheckBox, QDialog
from PyQt6.QtCore import Qt

# 导入逻辑层
from logic import TemplateManager
# 导入 UI 层
from ui.main_window import MainWindowUI
from ui.dialogs import AddTemplateDialog
from ui.styles import get_win11_style


class FolderCreatorController(MainWindowUI):
    """控制器类：连接 UI 表现与业务逻辑"""

    def __init__(self):
        super().__init__()
        self.manager = TemplateManager()
        
        # 应用 Win11 风格样式
        self.setStyleSheet(get_win11_style())
        
        # 绑定信号与槽
        self.bind_events()
        
        # 初始化列表
        self.refresh_template_list()

    def bind_events(self):
        """绑定 UI 组件的事件"""
        self.browse_btn.clicked.connect(self.handle_select_directory)
        self.add_btn.clicked.connect(self.handle_show_add_dialog)
        self.del_btn.clicked.connect(self.handle_delete_templates)
        self.refresh_btn.clicked.connect(self.refresh_template_list)
        self.preview_btn.clicked.connect(self.handle_preview)
        self.create_btn.clicked.connect(self.handle_execute_creation)

    def handle_select_directory(self):
        path = self.select_directory_dialog()
        if path:
            self.path_input.setText(path)

    def refresh_template_list(self):
        """刷新 UI 中的模板列表"""
        # 清空旧组件
        for i in reversed(range(self.template_list_layout.count())):
            widget = self.template_list_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        self.checkboxes.clear()
        self.manager.load_templates()
        templates = self.manager.get_templates()
        
        for name in templates.keys():
            cb = QCheckBox(name)
            cb.setCursor(Qt.CursorShape.PointingHandCursor)
            self.template_list_layout.addWidget(cb)
            self.checkboxes[name] = cb

    def handle_show_add_dialog(self):
        dialog = AddTemplateDialog(self)
        dialog.setStyleSheet(get_win11_style()) # 对话框也应用样式
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name, paths = dialog.get_data()
            if not name:
                self.show_message("错误", "模板名称不能为空", "error")
                return
            if not paths:
                self.show_message("错误", "至少需要一个有效的目录路径", "error")
                return
            
            self.manager.add_template(name, paths)
            self.refresh_template_list()
            self.log_msg(f"✅ 已添加新模板: {name}")

    def handle_delete_templates(self):
        to_delete = [name for name, cb in self.checkboxes.items() if cb.isChecked()]
        if not to_delete:
            self.show_message("提示", "请先勾选要删除的模板")
            return
        
        self.manager.remove_template(to_delete[0]) # 示例：删除第一个选中的，也可以循环删除
        # 如果需要批量删除，可以在 logic.py 扩展
        for name in to_delete:
            self.manager.remove_template(name)
            
        self.refresh_template_list()
        self.log_msg(f"🗑 已从库中移除模板: {', '.join(to_delete)}")

    def get_selected_data(self):
        """获取当前勾选的模板数据内容"""
        selected_names = [name for name, cb in self.checkboxes.items() if cb.isChecked()]
        all_data = self.manager.get_templates()
        return {name: all_data[name] for name in selected_names}

    def handle_preview(self):
        selected_data = self.get_selected_data()
        if not selected_data:
            self.show_message("提示", "请至少勾选一个模板进行预览")
            return
        
        self.log_area.clear()
        self.log_msg("--- 🔍 目录结构预览 ---")
        for name, paths in selected_data.items():
            self.log_msg(f"\n【{name}】")
            for p in paths:
                self.log_msg(f"  └─ {p}")

    def handle_execute_creation(self):
        base_dir = self.path_input.text().strip()
        selected_data = self.get_selected_data()
        
        if not base_dir:
            self.show_message("错误", "请先指定目标工作区目录", "error")
            return
        if not selected_data:
            self.show_message("警告", "请勾选至少一个模板后再执行创建", "warning")
            return

        self.log_area.clear()
        self.log_msg(f"🚀 开始执行任务...")
        
        success_count, error = self.manager.create_folders(
            base_dir, 
            selected_data, 
            log_callback=self.log_msg
        )
        
        if error:
            self.show_message("任务异常", f"创建过程中出现错误：\n{error}", "error")
        else:
            self.log_msg("\n✨ 任务全部完成！")
            self.show_message("同步成功", f"文件夹已成功部署！\n新创建数量: {success_count}")

    def log_msg(self, text):
        self.log_area.appendPlainText(text)


if __name__ == "__main__":
    # Windows 环境下开启高 DPI 支持
    if sys.platform == "win32":
        from PyQt6.QtCore import QCoreApplication
        # 兼容某些 Python 环境下的 DPI 缩放
    
    app = QApplication(sys.argv)
    app.setApplicationName("批量文件夹创建工具")
    
    controller = FolderCreatorController()
    controller.show()
    
    sys.exit(app.exec())
