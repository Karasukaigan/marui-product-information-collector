# coding=utf-8
# @Time : 2021/8/26 16:55
# @Author : Karasukaigan
# @File : get_all_instruction_manuals.py
# @Software : PyCharm

import time
import requests
import re
import html
import os


def main():
    # 必要な情報を取得
    product_type_name_l1, product_type_name_l2, product_name, pdf_url, num = get_instruction_manuals_url()
    # CSVファイルに書き込む
    write_csv(product_type_name_l1, product_type_name_l2, product_name, pdf_url)
    # ディレクトリを作成
    make_dir(product_type_name_l1, product_type_name_l2)
    # PDFファイルをダウンロード
    download_pdf(product_type_name_l1, product_type_name_l2, product_name, pdf_url, num)


def get_instruction_manuals_url():
    instruction_manuals_url = []
    main_url = "https://www.tokyo-marui.co.jp"
    headers1 = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,ja;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Referer": "https://www.tokyo-marui.co.jp/support/manuals/",
    }
    headers2 = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,ja;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
    }
    payload = {'Referer': ""}
    product_type = ["electric", "gas", "aircocking"]
    product_type_name_l1 = []
    product_type_name_l2 = []
    manuals_url = []
    pdf_url = []
    product_name = []

    for i in range(3):
        url = main_url + "/support/manuals/" + product_type[i] + "/index.html"
        response = requests.get(url, headers=headers1)
        # print(response.text)
        # print(type(response.text))

        # 製品のカテゴリを取得
        type_name_l1 = []
        type_name_l1 = re.findall('<h3 class="sw-Typography_Heading-type3 text_normal text_bold">(.*?)</h3>',
                                  response.text)
        product_type_name_l1.append(type_name_l1[0])

        # 製品の細別名を取得
        type_name_l2 = []
        type_name_l2 = re.findall('<h4 id="(.*?)" class="(.*?)">(.*?)</h4>', response.text)
        l = []
        for j in range(len(type_name_l2)):
            l.append(type_name_l2[j][2])
        product_type_name_l2.append(l)

        # 説明書URLを取得
        name_list_l1 = []
        name_list_l1 = re.findall('<div class="col-md">(.*?)<p class="sw-Heading', response.text, re.S)
        l1 = []
        for j in range(len(name_list_l1)):
            name_list_l2 = []
            name_list_l2 = re.findall('<a class="(.*?)" href="(.*?)">', name_list_l1[j])
            l2 = []
            for k in range(len(name_list_l2)):
                l2.append(name_list_l2[k][1])
            l1.append(l2)
        manuals_url.append(l1)
        time.sleep(0.5)

    print("種類：", end="")
    print(product_type_name_l1)
    print("細別：", end="")
    print(product_type_name_l2)
    print("説明書URL：", end="")
    print(manuals_url)

    # 製品の数を計算
    num = 0
    for i in range(len(manuals_url)):
        for j in range(len(manuals_url[i])):
            for k in range(len(manuals_url[i][j])):
                num += 1
    print("製品数：" + str(num))

    # 製品名とPDFファイルURLを取得
    print("データを要求……")
    for i in range(len(manuals_url)):
        l1 = []
        n1 = []
        for j in range(len(manuals_url[i])):
            l2 = []
            n2 = []
            for k in range(len(manuals_url[i][j])):
                url = main_url + "/support/manuals/" + product_type[i] + "/index.html"
                payload = {'Referer': url}
                response = requests.get(main_url + manuals_url[i][j][k], headers=merge(headers2, payload))
                a = re.findall('<h1 class="sw-Typography_Heading-type2 text">【(.*?)】取扱い説明書(.*?)</h1>', response.text)
                u = re.findall('<a class="sw-Btn_MorePdf-type1 text__normal" href="(.*?)"', response.text)
                s = a[0][0]
                s = re.sub('\s', ' ', s)
                s = html.unescape(s)
                s = s.replace("　", " ")
                s = s.replace("/", "・")
                n2.append(s)
                l2.append(u[0])
                time.sleep(0.5)
                print("█", end="")
            print("")
            print(n2)
            print(l2)
            n1.append(n2)
            l1.append(l2)
        product_name.append(n1)
        pdf_url.append(l1)

    print("")
    print("製品名：", end="")
    print(product_name)
    print("PDFファイルURL：", end="")
    print(pdf_url)

    return product_type_name_l1, product_type_name_l2, product_name, pdf_url, num


# 取得したテータをCSVファイルに書き込む
def write_csv(product_type_name_l1, product_type_name_l2, product_name, pdf_url):
    print("書き込み: marui_products_information.csv")
    # ファイルを作成
    f = open('marui_instruction_manuals.csv', "a+", encoding='utf-8')
    f.write("種類,細別,製品名,説明書URL" + '\n')
    num = 0
    for i in range(len(product_name)):
        for j in range(len(product_name[i])):
            for k in range(len(product_name[i][j])):
                num += 1
                # データを書き込む
                f.write(product_type_name_l1[i] + "," + product_type_name_l2[i][j] + "," + product_name[i][j][k] + "," + pdf_url[i][j][k] + '\n')
    f.close()

    return 1


# ディレクトリ作成
def make_dir(product_type_name_l1, product_type_name_l2):
    path = "marui_instruction_manuals"
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
    print("ディレクトリ作成：marui_instruction_manuals")
    print("ディレクトリ構造：")
    for i in range(len(product_type_name_l1)):
        path = "marui_instruction_manuals\\" + product_type_name_l1[i]
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
        for j in range(len(product_type_name_l2[i])):
            path = "marui_instruction_manuals\\" + product_type_name_l1[i] + "\\" + product_type_name_l2[i][j]
            print(path)
            isExists = os.path.exists(path)
            if not isExists:
                os.makedirs(path)

    return 1


# PDFファイルダウンロード
def download_pdf(product_type_name_l1, product_type_name_l2, product_name, pdf_url, maxnum):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,ja;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
    }
    num = 0
    print("ダウンロード……")
    for i in range(len(product_name)):
        for j in range(len(product_name[i])):
            for k in range(len(product_name[i][j])):
                num += 1
                if os.path.exists('marui_instruction_manuals\\%s\\%s\\%s取扱い説明書.pdf' % (product_type_name_l1[i], product_type_name_l2[i][j], product_name[i][j][k])) :
                    continue
                pdf_f = requests.get(pdf_url[i][j][k], headers=headers)
                f = open('marui_instruction_manuals\\%s\\%s\\%s取扱い説明書.pdf' % (
                product_type_name_l1[i], product_type_name_l2[i][j], product_name[i][j][k]), 'wb')
                f.write(pdf_f.content)
                f.close()
                print('(%s/%s) marui_instruction_manuals\\%s\\%s\\%s取扱い説明書.pdf' % (
                str(num), str(maxnum), product_type_name_l1[i], product_type_name_l2[i][j], product_name[i][j][k]))
                time.sleep(0.5)
    print("ダウンロード完了")

    return 1


# 辞書組み合わせ
def merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res


if __name__ == "__main__":
    main()
