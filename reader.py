import os
import sys
from dotenv import load_dotenv
import pytesseract
from pdf2image import convert_from_path
import pyttsx3
from concurrent.futures import ThreadPoolExecutor

# 加载 .env 文件中的环境变量
load_dotenv()
tesseract_cmd_path = os.getenv('TESSERACT')
temp_dir = os.getenv('TEMP_DIR')

if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)
    print(f"已创建临时文件夹：{temp_dir}")

pytesseract.pytesseract.tesseract_cmd = tesseract_cmd_path

# 配置文本转语音引擎
engine = pyttsx3.init()

# 定义 OCR 处理函数
def process_page(image):
    try:
        # OCR 文字识别
        text = pytesseract.image_to_string(image, lang='chi_sim+eng')  # 支持中英文
        return text
    except Exception as e:
        print(f"处理页面时出错: {e}")
        return ""


# 定义朗读函数
def read_text(text, page_number):
    if text.strip():
        print(f"开始朗读第 {page_number + 1} 页...")
        engine.say(text)  # 将识别出的文字加入到朗读队列中
        engine.runAndWait()  # 朗读识别到的文字
    else:
        print(f"第 {page_number + 1} 页没有识别到任何内容。")

# 主函数
def read_pdf_multithread(pdf_path, page_number = 0):
    # 使用 ThreadPoolExecutor 处理页面
    with ThreadPoolExecutor() as executor:
        # 逐页转换并处理
        while True:
            try:
                # 将 PDF 的单独页面转换为图像
                images = convert_from_path(pdf_path, first_page=page_number + 1, last_page=page_number + 1, output_folder=temp_dir)
                if len(images) > 0:
                    image = images[0]  # 只获取单页图像
                else:
                    raise StopIteration
                
                # 提交 OCR 任务
                future = executor.submit(process_page, image)
                text = future.result()  # 获取 OCR 结果
                
                # 朗读文本
                read_text(text, page_number)
                
                if os.path.exists(image.filename):
                    os.remove(image.filename)  # 删除图像文件
                
                page_number += 1  # 增加页码
            
            except StopIteration:
                print("所有页面处理完毕。")
                break
            except Exception as e:
                print(f"处理到第 {page_number + 1} 页时出错: {type(e).__name__} - {e}")
                break

if __name__ == "__main__":
    # 检查命令行参数数量
    if len(sys.argv) < 2:
        print("使用方法: python reader.py <pdf_file_path> <page_number>")
        sys.exit(1)

    # 获取 PDF 文件路径
    pdf_file_path = sys.argv[1]
    if len(sys.argv) > 2:
        page_number = int(sys.argv[2]) - 1
        read_pdf_multithread(pdf_file_path, page_number)
    else:
        read_pdf_multithread(pdf_file_path)
