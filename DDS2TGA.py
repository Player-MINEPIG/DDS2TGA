import os
import json
from PIL import Image


def Convert(source_directory, destination_directory):
    # 检查源目录是否存在
    if not os.path.isdir(source_directory):
        PrintErrorWithFiles(settings.language, "NoSourceDirectory", source_directory)
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
                    settings.language,
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
                PrintErrorWithFiles(settings.language, "ProcessFileError", filename)
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
    # 定义错误消息模板
    messages = {
        "zh-cn": {
            "NoSourceDirectory": f"源目录{file}不存在",
            "DestinationFileExists": f"目标文件{file}已存在",
            "ProcessFileError": f"处理文件{file}时出错",
        },
        "en": {
            "NoSourceDirectory": f"Source directory {file} does not exist",
            "DestinationFileExists": f"Target file {file} already exists",
            "ProcessFileError": f"Error processing file {file}",
        },
    }

    # 验证condition参数
    if condition not in messages["en"]:
        raise ValueError(
            'condition must be "NoSourceDirectory", "DestinationFileExists" or "ProcessFileError"'
        )

    # 获取并打印错误信息
    message = messages.get(language, messages["en"]).get(condition)
    if message:
        print(message)
    else:
        raise ValueError(f"Unsupported language: {language}")


class Settings:
    def __init__(self, language):
        # 设置可选的设置值
        self.SettingsOptions = {
            "VerticalFlip": {1: True, 2: False},
            "Language": {1: "zh-cn", 2: "en"},
        }
        try:
            if language not in self.SettingsOptions["Language"].values():
                raise ValueError("invalid language")
        except:
            print(
                "非法的语言设置，请检查Setting.json，已默认选择中文/invalid language, please check Settings.json and select Chinese by default"
            )
            language = "zh-cn"
        self.dictionary = {}
        self.Language = language
        self.SetLanguage()
        # 设置除语言外的默认值
        self.VerticalFlip = True
        # 加载设置文件
        self.load_settings()

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
            print(self.dictionary["NoSettings"])
            print(self.dictionary["ShowSettings"])
            print(self.__str__())
            settings_complete = False
        if not settings_complete or len(self.SettingsOptions) != len(settings):
            self.save_settings()
            print(self.dictionary["SettingsNotComplete"])

    def set_settings(self):
        while True:
            print(self.__str__())
            print(self.dictionary["SetSettingsIndex"])
            print(self.dictionary["Back"])
            index = input()
            print()
            if index == "b":
                break
            if index == "c":
                print(self.dictionary["Exit"])
                exit()
            try:
                index = int(index)
                if index <= 0 or index > len(self.__dict__) - 2:
                    print(self.dictionary["IncorrectIndex"])
                    continue
                # 获取成员变量名
                key = list(self.SettingsOptions.keys())[index - 1]
                # 输出设置值选项
                if isinstance(self.__dict__[key], bool):
                    print(f"1: {self.dictionary[key]}: {self.dictionary['true']}")
                    print(f"2: {self.dictionary[key]}: {self.dictionary['false']}")
                else:
                    keyOptions = key + "Options"
                    for i in range(len(self.dictionary[keyOptions])):
                        print(f"{i+1}: {list(self.dictionary[keyOptions])[i]}")
                print(self.dictionary["SetSettingsValue"])
                value = input()
                print()
                if value == "b":
                    continue
                if value == "c":
                    print(self.dictionary["Exit"])
                    exit()
                value = int(value)
                if isinstance(self.__dict__[key], bool):
                    if value == 1:
                        self.__dict__[key] = True
                    elif value == 2:
                        self.__dict__[key] = False
                    else:
                        print(self.dictionary["IncorrectIndex"])
                        continue
                else:
                    keyOptions = key + "Options"
                    if value <= 0 or value > len(self.dictionary[keyOptions]):
                        print(self.dictionary["IncorrectIndex"])
                        continue
                    self.__dict__[key] = self.SettingsOptions[key][value]
            except ValueError:
                print(self.dictionary["IncorrectIndex"])
                continue
            # 检测Language是否改变
            if key == "Language":
                self.SetLanguage()
            self.save_settings()

    # 更新语言
    def SetLanguage(self):
        if self.Language == "zh-cn":
            try:
                with open("zh-cn.json", "r", encoding="utf-8") as f:
                    self.dictionary = json.load(f)
            except:
                raise FileNotFoundError("zh-cn.json not found")
        if self.Language == "en":
            try:
                with open("en.json", "r", encoding="utf-8") as f:
                    self.dictionary = json.load(f)
            except:
                raise FileNotFoundError("en.json not found")

    # 将设置保存到设置文件
    def save_settings(self):
        with open("Settings.json", "w", encoding="utf-8") as f:
            temp_dict = {}
            # 只留下SettingsOptions的key中有的值再存入
            for key in self.__dict__.keys():
                if key in self.SettingsOptions:
                    temp_dict[key] = self.__dict__[key]

            json.dump(temp_dict, f, indent=4)
        print(self.dictionary["SaveSettings"])

    # 打印设置
    def __str__(self):
        output = ""
        num = 1
        print()
        for key in self.SettingsOptions.keys():
            # 检查量是否为布尔值
            if isinstance(self.__dict__[key], bool):
                bool_str = str(self.__dict__[key]).lower()
                output += (
                    f"{num}: {self.dictionary[key]}: {self.dictionary[bool_str]}\n"
                )
            else:
                output += f"{num}: {self.dictionary[key]}\n"
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
            print(settings.dictionary["Exit"])
            exit()
        source_dir = main_dir + os.sep + "dds"  # 源dds目录路径
        dest_dir = main_dir + os.sep + "tga"  # 目标目录路径
        if Convert(source_dir, dest_dir):
            print(settings.dictionary["ConvertFinished"])
        PrintTips(settings.Language)


global settings
if __name__ == "__main__":
    # 检查Settings文件是否存在，并读取语言设置，若为第一次打开程序，则询问语言
    language = ""
    if not os.path.isfile("Settings.json"):
        while True:
            print("请选择您的语言的索引/Please enter the index of the language you want to use")
            print("1: 简体中文")
            print("2: English")
            language = input()
            print()
            if language == "1":
                language = "zh-cn"
                break
            if language == "2":
                language = "en"
                break
            print("Incorrect index, please re-enter")
    else:
        with open("Settings.json", "r", encoding="utf-8") as f:
            language = json.load(f)["Language"]
    settings = Settings(language)
    main()
