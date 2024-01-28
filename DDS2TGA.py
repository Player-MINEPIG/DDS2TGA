import os
import json
from PIL import Image


def Convert(source_directory, destination_directory):
    # 检查源目录是否存在
    if not os.path.isdir(source_directory):
        PrintErrorWithFiles(settings.Language, "NoSourceDirectory", source_directory)
        return

    # 检查目标目录是否存在
    if not os.path.isdir(destination_directory):
        # 新建目标目录
        os.mkdir(destination_directory)

    for filename in os.listdir(source_directory):
        if filename.lower().endswith(".dds"):
            original_path = os.path.join(source_directory, filename)

            # 重命名文件
            base_name = filename.split(".")[0]
            new_name = "Avator_" + source_directory.split(os.sep)[-2]
            new_name = new_name + "_" + base_name + ".tga"
            new_path = os.path.join(destination_directory, new_name)

            # 检查目标文件是否存在
            if os.path.isfile(new_path):
                PrintErrorWithFiles(
                    settings.Language,
                    "DestinationFileExists",
                    new_path.split(os.sep)[-1],
                )
                continue

            # 将DDS转换为TGA
            try:
                with Image.open(original_path) as img:
                    # 垂直翻转图像
                    if settings.VerticalFlip:
                        flipped_img = img.transpose(Image.FLIP_TOP_BOTTOM)

                    # 将翻转后的图像以TGA格式保存
                    flipped_img.save(new_path, format="TGA")
            except IOError:
                PrintErrorWithFiles(settings.Language, "ProcessFileError", filename)
    return True


def PrintTips(language):
    if language == "zh-cn":
        print("-" * 50)
        print("请将源总目录拖入或输入此窗口并按回车")
        print("输入s并按回车更改设置")
        print("输入c并按回车结束程序")
        print("-" * 50)
        return
    if language == "en":
        print("-" * 50)
        print("Drag/Enter the source directory into this window and press enter")
        print("Enter s and press enter to change settings")
        print("Enter c and press enter to end the program")
        print("-" * 50)
        return


def PrintErrorWithFiles(language, condition: str, file):
    """
    打印错误信息。

    参数:
    condition -- 错误类型，只能是 "NoSourceDirectory"、"DestinationFileExists" 或 "ProcessFileError"
    """
    if condition not in [
        "NoSourceDirectory",
        "DestinationFileExists",
        "ProcessFileError",
    ]:
        raise ValueError(
            'condition must be "NoSourceDirectory", "DestinationFileExists" or "ProcessFileError"'
        )
    if language == "zh-cn":
        if condition == "NoSourceDirectory":
            print(f"源目录{file}不存在")
            return
        if condition == "DestinationFileExists":
            print(f"目标文件{file}已存在")
            return
        if condition == "ProcessFileError":
            print(f"处理文件{file}时出错")
            return
        return
    if language == "en":
        if condition == "NoSourceDirectory":
            print(f"Source directory {file} does not exist")
            return
        if condition == "DestinationFileExists":
            print(f"Target file {file} already exists")
            return
        if condition == "ProcessFileError":
            print(f"Error processing file {file}")
            return
        return


class Settings:
    def __init__(self):
        # 设置多语言对应的字典
        self.dictionary = {
            "VerticalFlip": {"zh-cn": "垂直翻转", "en": "Vertically Flip"},
            "Language": {
                "zh-cn": "语言: 简体中文",
                "en": "Language: English",
            },  # 顺序需与后续的options一致
            True: {"zh-cn": "启用", "en": "On"},
            False: {"zh-cn": "禁用", "en": "Off"},
            "SaveSettings": {"zh-cn": "设置已保存", "en": "Settings have been saved"},
            "SetSettingsIndex": {
                "zh-cn": "请输入你要更改的设置索引",
                "en": "Please enter the index of the setting you want to change",
            },
            "Back": {
                "zh-cn": "按b返回上一级",
                "en": "Press b to return to the previous level",
            },
            "IncorrectIndex": {
                "zh-cn": "输入错误的索引，请重新输入",
                "en": "Incorrect index, please re-enter",
            },
            "SetSettingsValue": {
                "zh-cn": "请输入你要更改的设置值的索引",
                "en": "Please enter the index of the value you want to change",
            },
            "ConvertFinished": {"zh-cn": "转换结束", "en": "Convert finished"},
            "Exit": {"zh-cn": "程序结束", "en": "Program exit"},
        }
        # 设置可选的设置值
        self.SettingsOptions = {
            "VerticalFlip": {1: True, 2: False},
            "Language": {1: "zh-cn", 2: "en"},
        }

        # 设置默认值
        self.VerticalFlip = True
        self.Language = "zh-cn"

    def load_settings(self):
        # 创建一个布尔变量来检查设置文件是否完整
        settings_complete = True
        # 读取并设置设置文件
        try:
            with open("Settings.json", "r") as f:
                settings = json.load(f)
                # 遍历成员变量来检查设置文件是否完整
                for key in self.SettingsOptions.keys():
                    if key not in settings:
                        settings[key] = self.__dict__[key]
                        settings_complete = False
                    else:
                        # 检查设置值是否符合规范
                        if settings[key] not in self.SettingsOptions[key].values():
                            settings[key] = self.__dict__[key]
                            settings_complete = False
                        else:
                            self.__dict__[key] = settings[key]
        except FileNotFoundError:
            # 如果设置文件不存在，创建设置文件
            print(
                "设置文件不存在，已创建默认设置文件/Settings file does not exist, default settings file has been created"
            )
            print("项目设置/Project Settings:")
            print(self.__str__())
            settings_complete = False
        if not settings_complete:
            with open("Settings.json", "w") as f:
                json.dump(self.__dict__, f)
            print(
                "设置文件不符合规范，已按默认设置补全/Settings file does not conform to the specifications, has been completed according to the default settings"
            )

    def set_settings(self):
        while True:
            print(self.__str__())
            print(self.dictionary["SetSettingsIndex"][self.Language])
            print(self.dictionary["Back"][self.Language])
            index = input()
            print()
            if index == "b":
                break
            if index == "c":
                print(self.dictionary["Exit"][self.Language])
                exit()
            try:
                index = int(index)
                if index <= 0 or index > len(self.__dict__) - 2:
                    print(self.dictionary["IncorrectIndex"][self.Language])
                    continue
                # 获取成员变量名
                key = list(self.SettingsOptions.keys())[index - 1]
                # 输出设置值选项
                if isinstance(self.__dict__[key], bool):
                    print(
                        f"1: {self.dictionary[key][self.Language]}: {self.dictionary[True][self.Language]}"
                    )
                    print(
                        f"2: {self.dictionary[key][self.Language]}: {self.dictionary[False][self.Language]}"
                    )
                else:
                    for i in range(len(self.dictionary[key])):
                        print(f"{i+1}: {list(self.dictionary[key].values())[i]}")
                print(self.dictionary["SetSettingsValue"][self.Language])
                value = input()
                print()
                if value == "b":
                    continue
                if value == "c":
                    print(self.dictionary["Exit"][self.Language])
                    exit()
                value = int(value)
                if isinstance(self.__dict__[key], bool):
                    if value == 1:
                        self.__dict__[key] = True
                    elif value == 2:
                        self.__dict__[key] = False
                    else:
                        print(self.dictionary["IncorrectIndex"][self.Language])
                        continue
                else:
                    if value <= 0 or value > len(self.dictionary[key]):
                        print(self.dictionary["IncorrectIndex"][self.Language])
                        continue
                    self.__dict__[key] = self.SettingsOptions[key][value]
            except ValueError:
                print(self.dictionary["IncorrectIndex"][self.Language])
                continue
            self.save_settings()

    # 将设置保存到设置文件
    def save_settings(self):
        with open("Settings.json", "w") as f:
            temp_dict = {}
            # 只留下SettingsOptions的key中有的值再存入
            for key in self.__dict__.keys():
                if key in self.SettingsOptions:
                    temp_dict[key] = self.__dict__[key]

            json.dump(temp_dict, f)
        print(self.dictionary["SaveSettings"][self.Language])

    # 打印设置
    def __str__(self):
        output = ""
        num = 1
        print()
        for key in self.SettingsOptions.keys():
            # 检查量是否为布尔值
            if isinstance(self.__dict__[key], bool):
                output += f"{num}: {self.dictionary[key][self.Language]}: {self.dictionary[self.__dict__[key]][self.Language]}\n"
            else:
                output += f"{num}: {self.dictionary[key][self.Language]}\n"
            num += 1
        return output


def main():
    print("DDS2TGA")
    PrintTips(settings.Language)

    while True:
        main_dir = input()  # 源总目录路径
        # 如果输入两边有引号，去掉引号
        if (main_dir.startswith('"') and main_dir.endswith('"')) or (
            main_dir.startswith("'") and main_dir.endswith("'")
        ):
            main_dir = main_dir[1:-1]
        if main_dir == "s":
            settings.set_settings()
            PrintTips(settings.Language)
            continue
        if main_dir == "c":
            settings.save_settings()
            print(settings.dictionary["Exit"][settings.Language])
            exit()
        source_dir = main_dir + os.sep + "dds"  # 源dds目录路径
        dest_dir = main_dir + os.sep + "tga"  # 目标目录路径
        if Convert(source_dir, dest_dir):
            print(settings.dictionary["ConvertFinished"][settings.Language])
        PrintTips(settings.Language)


global settings
if __name__ == "__main__":
    settings = Settings()
    settings.load_settings()
    main()
