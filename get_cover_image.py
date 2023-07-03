# coding=utf-8
# @Time : 2023/7/4
# @Author : Karasukaigan

import os
import csv
import fitz


def convert_pdf_to_png(file_path, page_number, output_directory):
    doc = fitz.open(file_path)
    if page_number < 1 or page_number > doc.page_count:
        print(f"Error: Page number {page_number} is out of range.")
        return

    output_filename = os.path.splitext(os.path.basename(file_path))[0]
    output_filename = f"{output_filename}.png"
    output_path = os.path.join(output_directory, output_filename)

    page = doc.load_page(page_number - 1)
    pix = page.get_pixmap(alpha=False)
    pix.save(output_path, "PNG")
    print(f"Converted page {page_number} of {file_path} to {output_path}")
    return output_path

def convert_pdf_pages_to_png(directory, page_number):
    pdf_png_mapping = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".pdf"):
                file_path = os.path.join(root, file)
                png_path = convert_pdf_to_png(file_path, page_number, root)
                file_path = file_path.replace("\\", "\\\\")
                png_path = png_path.replace("\\", "\\\\")

                pdf_png_mapping.append([file_path, png_path])
            # if file.endswith(".png"):
            #     file_path = os.path.join(root, file)
            #     os.remove(file_path)
            #     print(f"Deleted {file_path}.")

    js_array = "["
    for mapping in pdf_png_mapping:
        js_array += "["
        js_array += f"\"{mapping[0]}\","
        js_array += f"\"{mapping[1]}\""
        js_array += "],"
    js_array += "]"

    index_file = "取扱い説明書一覧.html"
    with open(index_file, "r", encoding="utf-8") as file:
        content = file.read()
    content = content.replace("${manual_info}", js_array)
    with open(index_file, "w", encoding="utf-8") as file:
        file.write(content)

target_directory = "marui_instruction_manuals"
page_number = 2

convert_pdf_pages_to_png(target_directory, page_number)