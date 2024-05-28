from fontTools.ttLib import TTFont, TTLibError
import re
import os

# 装有ttf或者otf字体的目标文件夹
folder_path = 'C:\\Users\\easyh\\Desktop\\ziyou'

# 判断字符串中是否包含中文
def contains_chinese(text):
    return re.search(r'[\u4e00-\u9fff]', text) is not None

# 获取指定.ttf字体文件的内部中文名，如果没有中文名将使用英文名
def get_font_chinese_name(ttfFile):
    font = TTFont(ttfFile)
    c_name = ""
    for font_name in font['name'].names:
        if font_name.nameID == 1:  # 字体全名
            c_name = font_name.toUnicode()
            if contains_chinese(c_name):
                break
    return c_name

#重命名文件
def rename_file(old_name, new_name):
    try:
        os.rename(old_name, new_name)
        print(f"文件 {old_name} 已成功重命名为 {new_name}")
    except FileNotFoundError:
        print(f"文件 {old_name} 不存在，请检查路径是否正确。")

#批量重命名文件
if __name__ == "__main__":
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.lower().endswith(".ttf") or filename.lower().endswith(".otf"):
                ttfFile = os.path.join(root, filename)
                _, fileExtension = os.path.splitext(filename)
                try:
                    c_name = get_font_chinese_name(ttfFile)
                    newFileName = os.path.join(root,c_name+fileExtension)
                    print(newFileName)
                    rename_file(ttfFile,newFileName)
                except Exception as e:
                    print(e)
                    continue


