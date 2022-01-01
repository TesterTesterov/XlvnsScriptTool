# XlvnsScriptTool
## English
 Dual languaged (rus+eng) tool for decompiling and compiling (actually, this tool is more than just (dis)assenbler, but less than (de)compiler) scripts .SDT from the visual novel's engine xlvns. It mostly used in [Leaf](https://vndb.org/p21) and [Aquaplus](https://vndb.org/p87) games, albeit not all. With it thou can fully edit all the code, not just strings. Thou can add message breaks and change scenarios without restrictions!

Definations: "#0-" are "free bytes", "#1-" are commands (and "\[...]" are arguments below), "#2-" are labels.

## Русский
 Двуязычное (рус+англ) средство для декомпиляции и компиляции (на самом деле, сие средство имеет больше функционала, чем у простых дизассемблеров, но при это меньше, чем у декомпиляторов) скриптов .mes движка визуальных новелл xlvns. В основном он используется в играх [Leaf](https://vndb.org/p21) и [Aquaplus](https://vndb.org/p87), хоть и не всех. С ним вы можете полностью редактирвоать код, а не только строки; по вашему повелению добавлять разрывы между сообщений и даже менять сценарии по своему замыслу!
  
 Определения: "#0-" есть "вольные байты", "#1-" есть команды (и под ними "\[...]" аргументы), "#2-" есть метки.
 
 # Usage / Использование
## English
![image](https://user-images.githubusercontent.com/66121918/147859755-ee795f12-b6ff-4559-8b49-5af0b7239037.png)
1. Choose the mode, file or directory. In first mode you will work with one .mes - .txt pair, in second -- with all files in a pair of directories.
2. Enter a name of the .mes file in the top entry (do see, with extension) or the directory name. Thou can also enter relative or absolute path. You can also click on "..." to choose.
3. Enter a name of the .txt file (do see, with extension) or the directory name. Thou can also enter relative or absolute path. You can also click on "..." to choose.
4. Choose the script version.
5. To decompile push the button "Decompile".
6. To compile push the button "Compile".
7. Status will be displayed on the text area below.

## Русский
![image](https://user-images.githubusercontent.com/66121918/147859749-77e589b0-0fc3-4837-b7af-01ab4fafade7.png)
1. Выберите режим: файл или директорию. В первом вы будете работать с парой .mes - .txt, во втором -- со всеми файлами в паре директорий.
2. Введите название файла .mes в верхней форме (заметьте, с расширением) или имя директории. Также можно вводить относительный или абсолютный до него путь. Также вы можете нажать на кнопку "...", чтобы выбрать.
3. Введите название файла .txt в нижней форме (заметьте, с расширением) или имя директории. Также можно вводить относительный или абсолютный до него путь. Также вы можете нажать на кнопку "...", чтобы выбрать.
4. Выберите версию скрипта.
5. Для декомпиляции нажмите на кнопку "Декомпилировать".
6. Для компиляции нажмите на кнопку "Компилировать".
7. Статус сих операций будет отображаться на текстовом поле ниже.

# Line and message breaks help / Помощь по организации переносов по строкам и сообщениям
## English

For line break add "\\n" special symbol in the string, to message break -- "\\k".
If by any chance message break did not work, append new message command, as showed below. (Insert your string instead of \<Somestring\>).
```
#1-MESSAGE
[
    "<Somestring>",
    2,
    "*MESSAGE_NUM*"
]
```

## Русский

Для переноса по строкам добавьте в строку спецсимвол "\\n", для переноса по сообщениям -- "\\k".
Если перенос по сообещниям почему-то не сработал, просто добавьте новую команду сообщения, как показано ниже. (Вместо \<Какая-то строка\> введите вашу строку).
```
#1-MESSAGE
[
    "<Какая-то строка>",
    2,
    "*MESSAGE_NUM*"
]
```

# Tested on / Протестировано на
## English

- [Shizuku](https://vndb.org/v235) - [Renewal DVD-ROM Edition](https://vndb.org/r602).

## Русский

- [Капля](https://vndb.org/v235) - [Обновлённая версия на DVD](https://vndb.org/r602).
