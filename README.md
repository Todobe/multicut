# multicut
同时裁剪多张图片的小破工具

## 使用方法

**鼠标操作**
`python cut_mouse.py image_path1 image_path2 image_path3 ...`

例如：
```commandline
python cut_mouse.py ./data/baseline.png ./data/HR.png
```

使用鼠标左键对裁剪位置进行框选，使用右键保存当前框选位置，**注意目录下需要有output文件夹**，按任意键退出。

**键盘操作**

`python cut_key.py image_path1 image_path2 image_path3 ...`
例如：
```commandline
python cut_mouse.py ./data/baseline.png ./data/HR.png
```

在命令行中输入裁剪图像的左上角、右下角的坐标，在图像上会显示出对应的位置，再按下`y`即可保存。输入0后回车退出程序。