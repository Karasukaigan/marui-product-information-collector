# coding=utf-8
# @Time : 2021/5/20 22:47
# @Author : Karasukaigan
# @File : get_marui_allproducts.py
# @Software : PyCharm


import time
import requests
import re
import html


def main():
    product_info = get_product_info()  # 製品情報を取る
    write_csv(product_info)  # データをCSVファイルに書き込む


def get_product_info():
    product_info = []  # 製品情報を保存するためのリスト

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,ja;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "Referer": "https://www.tokyo-marui.co.jp/products/",
    }

    series = [[1, 32, 2, 3, 4, 5, 6, 7, 8, 9], [29, 10, 11, 12, 13, 14],
              [15, 16, 17, 18, 19, 20, 21, 22]]  # 製品シリーズ番号、検索用
    this_series = series[0][0]
    payload = {'series': this_series, 'srchflg': 1}  # 送るパラメータ

    url = "https://www.tokyo-marui.co.jp/products/search/product_search.html"  # 検索ページを用いてシリーズ別製品を検索

    for i in range(0, len(series)):
        for j in range(0, len(series[i])):

            this_series = series[i][j]
            payload = {'series': this_series, 'srchflg': 1}
            response = requests.get(url, headers=headers, params=payload)  # 検索結果を取る

            # 役に立つ報を抽出
            all_name = re.findall('<a href="/products/(.+?)/(.+?)/(.+?)">(.+?)</a>', response.text)
            all_price = re.findall('<strong class="sw-Card_Products-Type1_Price">(.+?)</strong>', response.text)

            for x in range(0, len(all_name)):
                s1 = all_name[x][3].split('【', 1)  # split()を利用して不要な文字列を削除
                name = s1[0]
                name = html.unescape(name)  # ユニコード文字に変換
                name.replace("　", " ")  # 半角スペースに変換

                # 価額情報を正規化
                s1 = all_price[x].split(',', 1)
                s2 = s1[0].split('￥', 1)
                price = s2[1] + s1[1]

                # 抽出した情報をリストに保存
                product_info.append("%s,%s,%s,%s,%s,https://www.tokyo-marui.co.jp/products/%s/%s/%s" % (
                    name, price, all_name[x][0], all_name[x][1], all_name[x][2], all_name[x][0], all_name[x][1],
                    all_name[x][2]))

            print("(" + str(i + 1) + "/" + str(len(series)) + "),(" + str(j + 1) + "/" + str(
                len(series[i])) + ")")  # 進捗状況を表示

            time.sleep(1)  # 1秒待機

    return product_info


def write_csv(productinfo):
    # ファイルを生成し、データを書き込む
    print("Write to file: marui_products_information.csv")
    f = open('marui_products_information.csv', "a+", encoding='utf-8')
    f.write("name,price,category,series,id,url" + '\n')
    for i in productinfo:
        f.write(i + '\n')
    f.close()
    print("OK")


if __name__ == "__main__":
    main()
