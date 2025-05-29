import streamlit as st
from docxtpl import DocxTemplate
import datetime
import io

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

    def __init__(self, creden, uname, drin, sug, top):
        self.per_info = creden
        self.username = uname
        self.drink = drin
        self.sugar = sug
        self.topps = top

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
    def taxes_calculation(original_price):
        tax = original_price * 5 / 100
        return int(tax)

    @property
    def get_info(self):
        self.drink_ogprice = self.displaying_prices(menu_options, "drink", "dname", self.drink)
        self.sugar_ogprice = self.displaying_prices(menu_options, "sugar", "sname", self.sugar)
        self.topps_ogprice = self.displaying_prices(menu_options, "topping", "tname", self.topps)

        self.taxed_drink = self.taxes_calculation(self.drink_ogprice)
        self.taxed_sugar = self.taxes_calculation(self.sugar_ogprice)
        self.taxed_topping = self.taxes_calculation(self.topps_ogprice)

        self.og_total = self.drink_ogprice + self.sugar_ogprice + self.topps_ogprice
        self.total_tax = (self.taxed_drink + self.taxed_sugar + self.taxed_topping)
        self.final_total = self.og_total + self.total_tax

        self.a["name"] = self.username
        self.a["info"] = self.per_info
        self.a["date"] = datetime.datetime.now().strftime("%d/%m%Y %H:%M")
        self.a["drink"] = self.drink
        self.a["sugar"] = self.sugar
        self.a["topping"] = self.topps
        self.a["drink_price"] = self.drink_ogprice
        self.a["sugar_price"] = self.sugar_ogprice
        self.a["topping_price"] = self.topps_ogprice
        self.a["drink_tax"] = self.taxed_drink
        self.a["sugar_tax"] = self.taxed_sugar
        self.a["topping_tax"] = self.taxed_topping
        self.a["total"] = self.og_total
        self.a["total_tax"] = self.total_tax
        self.a["final_total"] = self.final_total
        return self.a

    @get_info.deleter
    def get_info(self):
        self.a = {}

with st.form(key="order_menu", clear_on_submit=True):
    name = st.text_input("Tên người đặt đơn:")
    credentials = st.text_input("Gmail / SĐT:")

    drink_choice = st.selectbox(label="Đồ uống:", 
                 options=App.displaying_items(menu_options, "drink", "dname"))
    
    sugar_choice = st.selectbox(label="Đường:", 
                 options=App.displaying_items(menu_options, "sugar", "sname"))
    
    topping_choice = st.selectbox(label="Topping:", 
                 options=App.displaying_items(menu_options, "topping", "tname"))
    
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
            st.error("Vui lòng điền tên của bạn vào")
        elif credentials == "":
            st.error("Vui lòng điền thông tin liên lạc của bạn vào")
        elif drink_choice == "":
            st.error("Vui lòng chọn nước uống bạn muốn mua")
        else:
            st.title(f"**:blue[Đơn hàng của {name}]**")
            st.write(f"Gmail / SĐT: {credentials}")
            st.write(f"Nước uống: {drink_choice} - {App.displaying_prices(menu_options, "drink", 
                                                                        "dname", drink_choice)}")
            st.write(f"Đường: {sugar_choice} - {App.displaying_prices(menu_options, "sugar", 
                                                                        "sname", sugar_choice)}")
            st.write(f"Topping: {topping_choice} - {App.displaying_prices(menu_options, "topping", 
                                                                        "tname", topping_choice)}")
            col3, col4 = st.columns([0.75, 1])
            if receipt == True:
                a = App(credentials, name, drink_choice, sugar_choice, topping_choice)
                data = a.get_info
                doc = DocxTemplate("receipt template.docx")
                doc.render(data)
                doc.save("generated receipt.docx") 

                with col4:
                    with open("generated receipt.docx", "rb") as adu:
                        st.download_button(label="Chốt đơn hàng", data=adu, 
                                           file_name="Hóa đơn.docx")

            else:
                with col4:
                    st.button("Xác nhận đơn hàng")