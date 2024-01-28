# Readme

[Chinese Version](https://github.com/Player-MINEPIG/DDS2TGA/blob/master/Readme.md)

## Introduction

A tool for:
- Converting DDS to TGA format
- Vertically flipping images
- Renaming files in a specific pattern

Created for ease of learning from a course by [@给你柠檬椰果养乐多你会跟我玩吗](https://space.bilibili.com/32704665).

## Installation

Replace 'projects' with your desired directory:

```
cd ~/projects
git clone https://github.com/Player-MINEPIG/DDS2TGA.git
cd DDS2TGA
pip install -r requirements.txt
```

## Usage

- Set the language in the setting interface:
  1. Lunch the program
  2. Press 's'
  3. Press '2'
  4. Press '2'
  5. Now it's the English UI

- Conversion Interface:

  1. Launch the program: `python DDS2TGA.py`
  2. Ensure a `dds` directory is in the source folder, like `Bronya_00/dds`
  3. Drag and drop the source folder into the program window and press enter
  4. After conversion, the program waits for the next directory input or switches to the settings interface

- Settings Interface:
  1. Launch the program: `python DDS2TGA.py`
  2. Press 's' then enter in the window to enter [settings](https://github.com/Player-MINEPIG/DDS2TGA/blob/master/Settings.md)
  3. Adjust settings as guided by the program
  4. Settings are saved automatically after each adjustment

- Renaming and Output Rules:
  The renaming rules are hard-coded based on project requirements. Modifications can be made in lines 21-25 of `DDS2TGA.py`.

  Renaming Rules:

  - Prefix the file name with "Avatar_".
  - Follow with the name of the source folder.
  - Then append the name of the DDS file.

  Example:

  - Source folder: `Bronya_00`
  - DDS file located in `Bronya_00/dds`, for instance, named `Body1_Color` in the directory `Bronya_00/dds/Body1_Color`.
  - The TGA file will be output to `Bronya_00/tga` folder, named `Avatar_Bronya_00_Body1_Color`, in the directory `Bronya_00/tga/Avatar_Bronya_00_Body1_Color`.
