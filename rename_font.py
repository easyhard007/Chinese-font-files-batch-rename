from fontTools.ttLib import TTFont, TTLibError
import re
import os
import argparse

# 默认目标文件夹
folder_path = './'

# 创建解析器
parser = argparse.ArgumentParser(description='命令行参数解析')

# 装有ttf或者otf字体的目标文件夹
parser.add_argument('-d', '--directory', type=str, help='目标文件夹')

# 解析参数
args = parser.parse_args()

if(args.directory!=None):
    folder_path = str(args.directory)
else:
    folder_path = './'



# 判断字符串中是否包含中文
def contains_chinese(text):
    return re.search(r'[\u4e00-\u9fff]', text) is not None

# 获取指定.ttf字体文件的内部中文名，如果没有中文名将使用英文名
def get_font_chinese_name(ttfFile):
    font = TTFont(ttfFile)
    name_dict = {}  #名称字典, 如果有多个中文名，按优先级序列选择（简体中文>繁体中文,windows>mac），如果没有中文名，则按优先级选择英文名（英语美国>英语英国,windows>mac）
    c_name_priority = [2052,3076, 36 ,1028, 19]
    e_name_priority = [1033,0,2057]
    for i,font_name in enumerate(font['name'].names):
        # print(i,font_name,font_name.langID,font_name.nameID)
        if font_name.nameID == 4: #包含字体家族详细信息:
            name_dict[font_name.langID] = font_name.toUnicode()

    # 按优先级序列搜索中文名，如果存在中文名直接返回中文名
    for lang_id in c_name_priority:
        if lang_id in name_dict.keys():
            return name_dict[lang_id].replace(" ","-")

    # 按优先级序列搜索英文名
    for lang_id in e_name_priority:
        if lang_id in name_dict.keys():
            return name_dict[lang_id].replace(" ","-")

    print("错误：",ttfFile,"无法找到中文名或英文名。")
    return -1

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
            if filename.lower().endswith(".ttf") or filename.lower().endswith(".otf") or filename.lower().endswith(".ttc"):
                ttfFile = os.path.join(root, filename)
                _, fileExtension = os.path.splitext(filename)
                try:
                    c_name = get_font_chinese_name(ttfFile)
                    if c_name==-1: continue
                    newFileName = os.path.join(root,c_name+fileExtension)
                    print(newFileName)
                    rename_file(ttfFile,newFileName)
                except Exception as e:
                    print(e)
                    continue

