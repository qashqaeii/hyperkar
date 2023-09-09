import streamlit as st
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import io
import os
rows = []
def extract(category):

    if category == 'موتور':
        keyword = 'engine'
    elif category == 'سیستم انتقال قدرت':
        keyword = 'Transmission'
    elif category == 'سیستم الکتریکی خودرو':
        keyword = 'Electronic-system'
    elif category == 'سیستم های رفاهی و ایمنی':
        keyword = 'Welfare-and-safety'
    elif category == 'شاسی وبدنه خودرو':
        keyword = 'Chassis-and-car-body'
    elif category == 'سیستم صوتی و تصویری':
        keyword = 'Audio-and-video-system'
    elif category == 'سیستم تعلیق، ترمز و ایمنی':
        keyword = 'Suspension-brakes-and-steering'
    elif category == 'مایعات و روان کاوها':
        keyword = 'Fluids-and-lubricants'
    elif category == 'مکمل ها ، اسپری ها و تمیزکننده ها':
        keyword = 'Supplements-sprays-and-cleaners'
    elif category == 'قطعات آپشن':
        keyword = 'Options'

    headers = {
        'authority': 'services.hypercariran.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en,fa;q=0.9',
        'content-type': 'application/json; charset=UTF-8',
        'customerid': 'yTxBQysP+dnf8UpthP9gJg==',
        'origin': 'https://www.hypercariran.com',
        'referer': 'https://www.hypercariran.com/',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'token': 'VGwMlD90mfSTRL/JN5nEHkf/OTT/Cm5FSu91bxV3tefJYkkV/CaZ0IAJX0no1cgMze4KvdJl1vb0n/0TxL1TaJq5IYGzwIR0x5YNMRQBAy0anb+M5rHtGfUwRPP/64lqyneDhX7/Bu7db8xMoZbZPiYqQiWhXYc5tNL/l2TvGK9LiihKxIsmAGG9i6D0bO55xx2wDv1HiNmLKt8WmPH/uw==',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }

    json_data = {
        'where_clause': f'https://www.hypercariran.com/search/{keyword}=undefined&group={keyword}',
        'sort': '',
        'pagenumber': '1',
        'pagesize': '30',
    }

    response = requests.post('https://services.hypercariran.com/OnlineShop.asmx/GET_All_Product', headers=headers,
                             json=json_data)
    data = response.json()
    l_cat = []
    for item in data['dt_ChildrenGroup']:
        cat_name = item['categoryName']
        l_cat.append(cat_name)
    st.markdown("------")
    st.text_area("لیست زیر دسته ها", value=l_cat)
    st.markdown("------")

    pages = data['pageCount'][0]['pageCount']
    pages = int(pages)

    all_items = data['pageCount'][0]['rowCount']
    col1, col2 = st.columns([2, 2])
    st.write(f"لطفا منتظر بمانید تا تمام اطلاعات استخراج شوند ، زمان باقی مانده :  {pages} ثانیه ")

    col1.write(f"تعداد کل صفحات : {pages}")
    col2.write(f"تعداد کل محصولات : {all_items}")
    st.markdown("------")

    n = 1
    pagess = 1
    for i in range(1, pages):

        headers = {
            'authority': 'services.hypercariran.com',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en,fa;q=0.9',
            'content-type': 'application/json; charset=UTF-8',
            'customerid': 'yTxBQysP+dnf8UpthP9gJg==',
            'origin': 'https://www.hypercariran.com',
            'referer': 'https://www.hypercariran.com/',
            'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'token': 'VGwMlD90mfSTRL/JN5nEHkf/OTT/Cm5FSu91bxV3tefJYkkV/CaZ0IAJX0no1cgMze4KvdJl1vb0n/0TxL1TaJq5IYGzwIR0x5YNMRQBAy0anb+M5rHtGfUwRPP/64lqyneDhX7/Bu7db8xMoZbZPiYqQiWhXYc5tNL/l2TvGK9LiihKxIsmAGG9i6D0bO55xx2wDv1HiNmLKt8WmPH/uw==',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        }

        json_data = {
            'where_clause': f'https://www.hypercariran.com/search/{keyword}=undefined&group={keyword}',
            'sort': '',
            'pagenumber': f'{i}',
            'pagesize': '30',
        }

        response = requests.post('https://services.hypercariran.com/OnlineShop.asmx/GET_All_Product', headers=headers,
                                 json=json_data)
        data = response.json()
        items = data['dt_Data']

        for item in items:
            title = item['name']
            price =item['minPrice']
            image = item['img']
            productCode = item['productCode']
            productCode = int(productCode)
            productlink = f"https://www.hypercariran.com/product/{productCode}"
            row = {
                "شماره": n,
                "نام محصول": title,
                "قیمت": price,
                "لینک محصول": productlink,
                "لینک عکس": image,
                }
            n = n+1
            rows.append(row)
    return(rows)

def scrape_item(item):
    url = f"https://www.hypercariran.com/product/{item}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    detailsParts = soup.find('div', class_='detailsPart')
    detailsParts = detailsParts.text.replace("شناسه محصول", "").strip(":")
    return (detailsParts)


st.set_page_config(
    page_title="استخراج گر حسن پور",
)
st.markdown("""
<style type="text/css">
body{
 direction:rtl;
}
</style>
""",unsafe_allow_html=True)
st.markdown("# استخراج اطلاعات از سایت هایپرکار  ")



option = st.selectbox(
    'یک دسته بندی را انتخاب کنید ',
    ('موتور', 'سیستم انتقال قدرت', 'سیستم الکتریکی خودرو', 'سیستم های رفاهی و ایمنی', 'سیستم تعلیق، ترمز و ایمنی',
     'شاسی وبدنه خودرو', 'مایعات و روان کاوها', 'مکمل ها ، اسپری ها و تمیزکننده ها', 'سیستم صوتی و تصویری',
     'قطعات آپشن'))

if st.button("استخراج اطلاعات"):
    scrap = extract(option)
    st.write("داده های استخراج شده: 📝 ")
    st.markdown("""
            <style type="text/css">
        body{
         direction:ltr;
        }
        </style>
            """,unsafe_allow_html=True)

    st.dataframe(scrap, width=1500, height=500)
    df = pd.DataFrame(data=scrap)
    df.to_excel("hypercar_data.xlsx", index=False)
    with open("hypercar_data.xlsx", "rb") as file:
        data = file.read()
        st.download_button(
            label="دریافت فایل Excel",
            data=data,
            file_name="hypercar_data.xlsx",
            key="excel-download",
        )
    st.markdown("# تقدیم شما آقای حسن پور")
    st.write("ادامه دارد ... ")
    st.write("سازنده حسین قشقایی 09357930033")
    