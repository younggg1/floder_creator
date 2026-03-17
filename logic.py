import os
import json
from pathlib import Path


class TemplateManager:
    """模板持久化与文件夹创建逻辑类"""

    def __init__(self, config_path="templates.json"):
        self.config_path = config_path
        self._templates = {}
        self.load_templates()

    def load_templates(self):
        """加载模板 JSON"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self._templates = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._templates = {}
        else:
            self.save_templates()

    def save_templates(self):
        """保存模板 JSON"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self._templates, f, indent=4, ensure_ascii=False)
        except IOError:
            pass

    def get_templates(self):
        return self._templates

    def add_template(self, name, paths):
        self._templates[name] = paths
        self.save_templates()

    def remove_template(self, name):
        if name in self._templates:
            del self._templates[name]
            self.save_templates()

    def create_folders(self, base_dir, selected_templates, log_callback):
        """
        在目标目录下执行创建逻辑
        :param base_dir: 根目录字符串
        :param selected_templates: 选中的模板内容 {name: [paths]}
        :param log_callback: 日志回调函数 (str)
        :return: (success_count, error)
        """
        base_path = Path(base_dir)
        if not base_path.exists() or not base_path.is_dir():
            return 0, "目标目录不存在或不是一个目录"

        success_count = 0
        try:
            for template_name, paths in selected_templates.items():
                log_callback(f"正在应用模板: {template_name}")
                for folder_path in paths:
                    full_path = base_path / folder_path
                    if full_path.exists():
                        log_callback(f"  [跳过] 已存在: {folder_path}")
                    else:
                        full_path.mkdir(parents=True, exist_ok=True)
                        log_callback(f"  [创建] 成功: {folder_path}")
                        success_count += 1
            return success_count, None
        except Exception as e:
            return success_count, str(e)
