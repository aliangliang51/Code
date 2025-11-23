import os


def traverse_and_save_py_to_md(root_folder, output_md_filename="output_code_summary.md"):
    """
    递归遍历指定文件夹下的所有 .py 文件，并将它们的内容追加到单个 .md 文件中。

    Args:
        root_folder (str): 要开始搜索的根文件夹路径。
        output_md_filename (str): 最终生成的 Markdown 文件的名称。
    """

    # 检查根文件夹是否存在
    if not os.path.isdir(root_folder):
        print(f"❌ 错误：根文件夹 '{root_folder}' 不存在。请检查路径。")
        return

    # 初始化 Markdown 文件内容
    md_content = f"# 📁 代码项目摘要：{os.path.basename(root_folder)}\n\n"
    py_files_found = 0

    print(f"🔎 正在开始扫描 '{root_folder}' 及其子文件夹...")

    # os.walk(root_folder) 会递归地生成 (目录路径, 目录列表, 文件列表)
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:
            # 只处理 .py 文件
            if filename.endswith(".py"):
                # 构造完整的 .py 文件路径
                full_py_path = os.path.join(dirpath, filename)

                # 构造相对于根文件夹的路径，用于Markdown中的标题
                # os.path.relpath(full_py_path, root_folder)
                # 例如：如果 root_folder 是 'Project'，文件是 'Project/utils/helper.py'
                # 相对路径就是 'utils/helper.py'
                relative_path = os.path.relpath(full_py_path, root_folder)

                try:
                    # 1. 读取 .py 文件内容
                    with open(full_py_path, 'r', encoding='utf-8') as py_file:
                        py_content = py_file.read()

                    # 2. 格式化内容为 Markdown 代码块并追加
                    md_content += f"## 文件: `{relative_path}`\n\n"
                    md_content += f"```python\n{py_content}\n```\n\n---\n\n"

                    py_files_found += 1
                    print(f"   ➕ 已添加: {relative_path}")

                except Exception as e:
                    print(f"   ⚠️ 警告：无法读取文件 {relative_path}。跳过。错误: {e}")

    # 3. 写入最终的 .md 文件
    if py_files_found > 0:
        try:
            with open(output_md_filename, 'w', encoding='utf-8') as md_file:
                md_file.write(md_content)

            print(f"\n🎉 完成！共找到 {py_files_found} 个 .py 文件。")
            print(f"✅ 所有内容已成功保存到 '{output_md_filename}'。")
        except Exception as e:
            print(f"\n❌ 写入 Markdown 文件时发生错误: {e}")
    else:
        print(f"\n😔 未在 '{root_folder}' 及其子文件夹中找到任何 .py 文件。没有生成 Markdown 文件。")


# --- 示例用法 ---
if __name__ == "__main__":
    # 指定您要扫描的根文件夹
    # 建议使用一个测试文件夹，例如 'MyProject'
    # ROOT_FOLDER_TO_SCAN = "./OpenCV"
    # ROOT_FOLDER_TO_SCAN = "./RK3568人脸识别"
    ROOT_FOLDER_TO_SCAN = "./RK3568手势识别"
    # OUTPUT_FILE = "Project_Code_Summary.md"
    # OUTPUT_FILE = "Project_Code_Summary1.md"
    OUTPUT_FILE = "Project_Code_Summary2.md"

    # 注意：在运行之前，请确保您的 'MyProject' 文件夹存在，并且里面有 .py 文件！

    traverse_and_save_py_to_md(ROOT_FOLDER_TO_SCAN, OUTPUT_FILE)