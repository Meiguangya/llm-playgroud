from pathlib import Path

from app.ai.rag.loader.txt_loader import load_txt
from app.ai.rag.loader.pdf_loader import load_pdf

# 定义资源路径
RESOURCE_DIR = Path(__file__).parent.parent / "data"

# 获取当前文件的路径
CURRENT_FILE = Path(__file__).resolve()
# 获取当前文件所在目录（即 app/）
CURRENT_DIR = CURRENT_FILE.parent
# 获取项目根目录（即 app 的父目录）
PROJECT_ROOT = CURRENT_DIR.parent

FILE_LOADERS = {
    '.txt': load_txt,
    '.pdf': load_pdf,
}


class LoadSystemFile:

    @classmethod
    def load_system_file(cls):

        print(f"读取文件夹:{RESOURCE_DIR}中的文件")

        data_dir = Path(RESOURCE_DIR)

        # 检查目录是否存在
        if not data_dir.exists():
            print(f"❌ 目录不存在: {data_dir}")
            return

        if not data_dir.is_dir():
            print(f"❌ 路径不是目录: {data_dir}")
            return

        # 非递归遍历，只处理当前层级的文件
        found_files = False
        for item in data_dir.iterdir():
            if item.is_file():  # 只处理文件，跳过子目录
                ext = item.suffix.lower()  # 转小写，确保匹配
                loader = FILE_LOADERS.get(ext)

                if loader:
                    try:
                        result = loader(item)  # 调用对应的处理函数

                    except Exception as e:
                        print(f"❌ 处理文件 {item.name} 时出错: {e}")
                else:
                    print(f"还没有定义处理{ext}文件的方法")

                found_files = True

        if not found_files:
            print("📭 该目录中没有找到任何文件。")
