# Readme

[English version](https://github.com/Player-MINEPIG/DDS2TGA/blob/master/Readme_en.md)

## 简介

一个

- 将DDS格式转换为tga格式
- 将其垂直翻转
- 按照一定格式重命名

的工具。

为了方便自己学习[@给你柠檬椰果养乐多你会跟我玩吗](https://space.bilibili.com/32704665)大佬的课程，制作了该工具。

## 安装

请将'projects'替换为你想安装到的目录

```
cd ~/'projects'
git clone https://github.com/Player-MINEPIG/DDS2TGA.git
cd ./DDS2TGA
pip install -r requirements.txt
```

## 用法

- 转换界面

  1. 启动程序

     `python DDS2TGA.py`

  2. 确认源文件夹中包含一个`dds`目录，如`Bronya_00/dds`
  3. 将源文件夹，如上述的Bronya_00文件夹拖入程序窗口并按回车即可
  4. 转换完成后会等待下一个目录的输入直到退出或者切换至设置界面

- 设置界面

  1. 启动程序

     `python DDS2TGA.py`

  2. 在窗口中按s然后回车，会进入设置界面

  3. 根据程序指引调整[设置](https://github.com/Player-MINEPIG/DDS2TGA/blob/master/Settings.md)

  4. 每次调整设置都会进行自动保存
  5. 退出设置界面后会重新进入转换界面，除非按c直接退出程序

- 重命名及输出规则

  基于该项目针对的需求，未开发重命名规则的编辑，如有需要，请自行更改DDS2TGA.py中21至25行

  重命名规则：

  - 文件开头添加"Avator_"
  - 之后接源文件夹名称
  - 之后接dds文件名称

  示例：

  源文件夹为`Bronya_00`
  dds文件存储在`Bronya_00/dds`文件夹中，以其中一个文件为例，其名称为`Body1_Color`，目录为`Bronya_00/dds/Body1_Color`
  那么tga文件将会被输出到`Bronya_00/tga`文件夹，并被命名为`Avator_Bronya_00_Body1_Colo`r，目录为`Bronya_00/tga/Avator_Bronya_00_Body1_Color`

  