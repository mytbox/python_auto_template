from pathlib import Path


def get_project_root():
    """
    获取项目根目录
    通过查找项目标识文件（如 .git、requirements.txt）来确定项目根目录
    """
    current_path = Path(__file__).resolve().parent  # 当前文件所在的目录 (config/)
    project_markers = ['.git', 'requirements.txt', 'setup.py', 'pyproject.toml', '.env']

    # 向上遍历目录树，直到找到项目标识文件
    while current_path != current_path.parent:
        if any((current_path / marker).exists() for marker in project_markers):
            return current_path
        current_path = current_path.parent

    # 如果没找到典型的项目标识，返回当前文件的父目录作为默认值
    return Path(__file__).resolve().parent.parent

project_root = get_project_root()

if __name__ == '__main__':
    print(project_root)