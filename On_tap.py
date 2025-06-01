import streamlit as st
from docxtpl import DocxTemplate
import datetime
from spire.doc import *
from spire.doc.common import *

st.set_page_config(page_title="Trà sữa béo", 
                   page_icon=":tropical_drink:", 
                   layout="wide")

st.title("Page đặt trà sữa béo")

menu_options = {"drink": [{"dname": "Trà sữa truyền thống", "price": 30000}, 
                          {"dname": "Trà sữa nướng", "price": 35000}, 
                          {"dname": "Matcha latte", "price": 40000}, 
                          {"dname": "Hống trà đào", "price": 30000}], 
                
                "sugar": [{"sname": "", "price": 0}, 
                          {"sname": "Đường mía", "price": 5000}, 
                          {"sname": "Đường đen", "price": 5000}, 
                          {"sname": "Đường trắng", "price": 5000}, 
                          {"sname": "Đường đặc biệt gia chuyền", "price": 10000}], 

                "topping": [{"tname": "", "price": 0}, 
                            {"tname": "Trân châu đen", "price": 5000}, 
                            {"tname": "Trân châu trắng", "price": 5000}, 
                            {"tname": "Thạch rau câu", "price": 5000}, 
                            {"tname": "Slime", "price": 5000}]     
                }

class App:
    a = {}

    def __init__(self, creden, uname, loc, drin, sug, top, drin_am, sug_am, top_am, re_num):
        self.per_info = creden
        self.username = uname
        self.location = loc
        self.drink = drin
        self.sugar = sug
        self.topps = top
        self.drink_amount = drin_am
        self.sugar_amount = sug_am
        self.topps_amount = top_am
        self.receipt_number = re_num

    @staticmethod
    def displaying_items(chosen_dict, showables1,  showables2):
        items_list = []
        for i in chosen_dict[showables1]:
            items_list.append(i[showables2])
        return items_list
    
    @staticmethod
    def displaying_prices(chosen_dict, showables1, showables2, chosen_item):
        for i in chosen_dict[showables1]:
            if i[showables2] == chosen_item:
                return i["price"]
            
    @staticmethod
    def price_calculation(original_price, own_amount, drin_amount, type):
        if type == "Drink":
            total = original_price * drin_amount
            return int(total)
        else:
            total = original_price * own_amount / 100 * drin_amount
            return int(total)

    @property
    def get_info(self):
        self.drink_ogprice = self.displaying_prices(menu_options, "drink", "dname", self.drink)
        self.sugar_ogprice = self.displaying_prices(menu_options, "sugar", "sname", self.sugar)
        self.topps_ogprice = self.displaying_prices(menu_options, "topping", "tname", self.topps)

        self.drink_total = self.price_calculation(self.drink_ogprice, self.drink_amount, 
                                                  self.drink_amount, "Drink")
        self.sugar_total = self.price_calculation(self.sugar_ogprice, self.sugar_amount, 
                                                  self.drink_amount, "Sugar")
        self.topps_total = self.price_calculation(self.topps_ogprice, self.topps_amount, 
                                                  self.drink_amount, "Topping")

        self.a["name"] = self.username
        self.a["info"] = self.per_info
        self.a["location"] = self.location
        self.a["receipt_number"] = self.receipt_number
        self.a["date"] = datetime.datetime.now().strftime("Ngày %d tháng %m năm %Y %H:%M")
        self.a["drink"] = self.drink
        self.a["sugar"] = self.sugar
        self.a["topping"] = self.topps
        self.a["drink_price"] = self.drink_ogprice
        self.a["sugar_price"] = self.sugar_ogprice
        self.a["topping_price"] = self.topps_ogprice
        self.a["drink_amount"] = self.drink_amount
        self.a["sugar_amount"] = self.sugar_amount
        self.a["topping_amount"] = self.topps_amount
        self.a["drink_total"] = self.drink_total
        self.a["sugar_total"] = self.sugar_total
        self.a["topping_total"] = self.topps_total
        self.a["total"] = self.drink_total + self.sugar_total + self.topps_total
        self.a["total_tax"] = int(self.drink_total + self.sugar_total + self.topps_total) * 5 / 100
        self.a["final_total"] = int(self.drink_total + self.sugar_total + self.topps_total + 
                                 (self.drink_total + self.sugar_total + self.topps_total) * 5 / 100)
        return self.a

    @get_info.deleter
    def get_info(self):
        self.a = {}

with st.form(key="order_menu", clear_on_submit=True):
    name = st.text_input("Tên người đặt đơn:")
    credentials = st.text_input("Gmail / SĐT:")
    location_info = st.text_input("Địa chỉ: ")

    drink_choice = st.selectbox(label="Đồ uống:", 
                 options=App.displaying_items(menu_options, "drink", "dname"))
    Drink_amount = st.slider(min_value=1, max_value=20, label="Số lượng nước uống")
    
    sugar_choice = st.selectbox(label="Đường:", 
                 options=App.displaying_items(menu_options, "sugar", "sname"))
    Sugar_amount = st.slider(min_value=0, max_value=100, label="% đường")
    
    topping_choice = st.selectbox(label="Topping:", 
                 options=App.displaying_items(menu_options, "topping", "tname"))
    Topping_amount = st.slider(min_value=0, max_value=100, label="% topping")
    
    col1, col2 = st.columns([8, 1])
    with col1:
        receipt = st.checkbox("Lấy hóa đơn")
        update = st.form_submit_button("Cập nhật đơn")
    with col2:
        clear = st.form_submit_button("Xóa đơn")

with st.sidebar:
    if clear:
            del App.get_info
    if update:
        if name == "":
            st.error("Vui lòng điền tên của bạn")
        elif credentials == "":
            st.error("Vui lòng điền thông tin liên lạc của bạn")
        elif location_info == "":
            st.error("Vui lòng điền địa chỉ của bạn")
        elif drink_choice == "":
            st.error("Vui lòng chọn nước uống bạn muốn mua")
        else:
            a = open("receipt_numbers", "r")
            b = a.read()
            receipt_number = int(b) + 1
            receipt_number = f"{receipt_number:.0f}"
            a.close()

            c = open("receipt_numbers", "w")
            c.write(receipt_number)
            c.close()

            st.title(f"**:blue[Đơn hàng của {name}]**")
            st.write(f"Gmail / SĐT: {credentials}")
            st.write(f"Địa chỉ: {location_info}")
            st.write(f"Nước uống: {drink_choice} - {App.displaying_prices(menu_options, "drink", 
                                                                        "dname", drink_choice)}")
            st.write(f"Đường: {sugar_choice} - {App.displaying_prices(menu_options, "sugar", 
                                                                        "sname", sugar_choice)}")
            st.write(f"Topping: {topping_choice} - {App.displaying_prices(menu_options, "topping", 
                                                                        "tname", topping_choice)}")
            col3, col4 = st.columns([0.75, 1])
            if receipt == True:
                a = App(credentials, name, location_info, 
                        drink_choice, sugar_choice, topping_choice, 
                        Drink_amount, Sugar_amount, Topping_amount, receipt_number)
                data = a.get_info
                doc = DocxTemplate("receipt template.docx")
                doc.render(data)
                doc.save("generated receipt.docx")

                document = Document()
                document.LoadFromFile("generated receipt.docx")
                images = document.SaveImageToStreams(ImageType.Bitmap)

                with open("receipt.png", "wb") as f:
                    f.write(images[0].ToArray())

                with col4:
                    with open("receipt.png", "rb") as lk:
                        st.download_button("Chốt hóa đơn", lk, "Hóa đơn.png")

            else:
                with col4:
                    st.button("Xác nhận đơn hàng")