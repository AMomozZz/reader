# reader

不想看了，让电脑帮我念书用的。

需要添加`.env`文件，内容如下：

```bash
# tesseract的安装路径，指向tesseract.exe但是不要加.exe
TESSERACT=C:/Program Files/Tesseract-OCR/tesseract

# 保存images的临时文件夹路径
TEMP_DIR=./temp
```

感谢 [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)

## 未来功能

- [ ] 朗读当前页时处理下一页，使得朗读中间没有间断
- [ ] 制作UI，匹配pdf和音频
- [ ] 按页保存音频，方便倍速和/或跳过（待定）
