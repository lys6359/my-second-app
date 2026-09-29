import streamlit as st
import urllib.parse
import random
import os
from datetime import datetime

# 1. 網頁基本設定
st.set_page_config(page_title="ALIS FRIED CHICKEN 網頁點餐系統", page_icon="🍗", layout="wide")

# 利用 CSS 注入，將背景改成高級明亮黃與深灰色調
st.markdown("""
    <style>
    .stApp {
        background-color: #FBBF24; 
        color: #1F2937 !important;
    }
    h1, h2, h3 {
        color: #000000 !important;
        font-weight: 800 !important;
    }
    [data-testid="stContainer"] {
        background-color: #1F2937 !important; 
        border-radius: 16px !important;
        padding: 20px !important;
        border: none !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
        margin-bottom: 15px !important;
    }
    [data-testid="stContainer"] .stMarkdown p, [data-testid="stContainer"] h3 {
        color: #FFFFFF !important;
    }
    [data-testid="stContainer"] button {
        background-color: #FBBF24 !important;
        color: #000000 !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# 老闆專用營業控制：True = 正常營業 | False = 店鋪打烊
IS_OPEN = True 

if not IS_OPEN:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<h1 style='text-align: center; color: #FBBF24 !important;'>🌙 店鋪休息中 / Closed</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 18px; color: #FFFFFF !important;'>謝謝您的光臨！我們目前的營業時間已結束，明天請早喔！🙏</p>", unsafe_allow_html=True)
    st.stop() 

# ==========================================
# 🍔 前台顧客點餐大標題
# ==========================================
st.title("🍗 ALIS FRIED CHICKEN 網頁點餐系統")
st.write("歡迎光臨！請在下方選擇您的餐點。結帳後將引導至 WhatsApp 發送訂單給老闆喔！")
st.write("---")

# 用餐方式選擇
dining_type = st.radio(
    "🥡 請選擇您的用餐方式：", 
    ["內用 🍽️", "外帶 🛍️", "外送 / 食物配送 🚗"], 
    horizontal=True,
    index=None
)

# 重新定義菜單與基礎價格
menu = {
    "Ayam Gunting (炸雞排) 🍗": 10.00,
    "Sosej Jumbo (巨無霸香腸) 🌭": 6.00,
    "Sotong (炸魷魚) 🦑": 14.00,
    "Chicken Popcorn (7pcs) (爆米花雞) 🍿": 5.00,
    "Ayam Tender (雞柳) 🍗✨": 3.00,
    "Satay Ayam (沙爹雞肉串) 🍢": 3.00
}

CURRENCY = "RM"
MY_PHONE_NUMBER = "60162002352"

if "new_cart" not in st.session_state:
    st.session_state.new_cart = {}

# 自動生成唯一的訂單單號
if "order_id" not in st.session_state:
    date_str = datetime.now().strftime("%Y%m%d")
    st.session_state.order_id = f"ALIS-{date_str}-{random.randint(1000, 9999)}"

# 建立左右兩欄排版
col1, col2 = st.columns(2)

with col1:
    st.subheader("【 🍱 今日菜單 】")
    
    if dining_type is None:
        st.error("⚠️ 請在網頁最上方先選擇您的「用餐方式」，才可以開始點餐喔！")
        is_menu_disabled = True
    else:
        is_menu_disabled = False

    for food, price in menu.items():
        with st.container():
            st.markdown(f"### {food}")
            
            # 為新餐點設計客製化加點與口味選項
            if "Ayam Gunting" in food:
                size = st.selectbox("📐 選擇份量", ["Saiz Normal (RM 10.00)", "Saiz Besar (+RM 3.00)"], key="gunting_size")
                spicy = st.selectbox("🌶️ 選擇辣度", ["不辣", "微辣", "大辣"], key="gunting_spicy")
                actual_price = price + 3.00 if "Saiz Besar" in size else price
                full_food_name = f"{food} ({size}/{spicy})"
                st.markdown(f"💰 價格：**{CURRENCY} {actual_price:.2f}**")
                
            elif "Sosej Jumbo" in food:
                sauce = st.selectbox("🥫 選擇醬料", ["辣椒醬", "番茄醬", "美乃滋", "不需要醬料"], key="sosej_sauce")
                actual_price = price
                full_food_name = f"{food} ({sauce})"
                st.markdown(f"💰 價格：**{CURRENCY} {actual_price:.2f}**")
                
            elif "Sotong" in food:
                spicy = st.selectbox("🌶️ 選擇口味/辣度", ["不辣", "辣椒粉", "招牌胡椒鹽"], key="sotong_spicy")
                actual_price = price
                full_food_name = f"{food} ({spicy})"
                st.markdown(f"💰 價格：**{CURRENCY} {actual_price:.2f}**")
                
            elif "Chicken Popcorn" in food:
                flavor = st.selectbox("🍿 選擇口味", ["原味", "椒鹽味", "起司粉 (+RM 1.00)"], key="popcorn_flavor")
                actual_price = price + 1.00 if "起司粉" in flavor else price
                full_food_name = f"{food} ({flavor})"
                st.markdown(f"💰 價格：**{CURRENCY} {actual_price:.2f}**")
                
            elif "Ayam Tender" in food:
                qty_opt = st.selectbox("🔢 選擇數量", ["1pcs (RM 3.00)", "3pcs (RM 8.00)", "5pcs (RM 11.00)"], key="tender_qty")
                if "3pcs" in qty_opt:
                    actual_price = 8.00
                elif "5pcs" in qty_opt:
                    actual_price = 11.00
                else:
                    actual_price = 3.00
                full_food_name = f"{food} ({qty_opt})"
                st.markdown(f"💰 價格：**{CURRENCY} {actual_price:.2f}**")
                
            else:  # Satay Ayam
                satay_opt = st.selectbox("🍢 選擇數量", ["1串 (RM 3.00)", "5串 (RM 15.00)", "10串 (RM 30.00)"], key="satay_qty")
                if "5串" in satay_opt:
                    actual_price = 15.00
                elif "10串" in satay_opt:
                    actual_price = 30.00
                else:
                    actual_price = 3.00
                full_food_name = f"{food} ({satay_opt})"
                st.markdown(f"💰 價格：**{CURRENCY} {actual_price:.2f}**")
                
            if st.button(f"➕ 點購 {food}", key=f"btn_{food}", disabled=is_menu_disabled):
                if full_food_name in st.session_state.new_cart and isinstance(st.session_state.new_cart[full_food_name], dict):
                    st.session_state.new_cart[full_food_name]["qty"] += 1
                else:
                    st.session_state.new_cart[full_food_name] = {"qty": 1, "price": actual_price}
                st.toast(f"已加入購物車！")
                st.rerun()

with col2:
    st.subheader("【 🛒 您的購物車 】")
    
    display_type = dining_type if dining_type else "⚠️ 尚未選擇"
    st.markdown(f"✨ 目前選擇：**{display_type}** | 🔢 自動生成單號：**{st.session_state.order_id}**") 
    
    delivery_address = ""
    table_number = ""
    
    if dining_type == "外送 / 食物配送 🚗":
        delivery_address = st.text_input("🏠 請輸入您的完整外送地址 (Delivery Address):")
    elif dining_type == "內用 🍽️":
        table_number = st.text_input("🔢 請輸入您的桌號 (Table Number):")
        
    for k, v in list(st.session_state.new_cart.items()):
        if not isinstance(v, dict):
            st.session_state.new_cart = {}
            st.rerun()
    
    if not st.session_state.new_cart:
        st.write("購物車目前是空的喔！請從左側今日菜單點擊按鈕加入餐點。")
        total = 0
    else:
        total = 0
        st.write("---")
        
        for food_info, item_data in list(st.session_state.new_cart.items()):
            qty = item_data["qty"]
            item_price = item_data["price"]
            item_total = item_price * qty
            total += item_total
            
            cart_col1, cart_col2, cart_col3 = st.columns(3)
            with cart_col1:
                st.write(f"▪️ **{food_info}**  \n💰 單價: {CURRENCY} {item_price:.2f} x {qty}")
            with cart_col2:
                if st.button("➖", key=f"minus_{food_info}"):
                    st.session_state.new_cart[food_info]["qty"] -= 1
                    if st.session_state.new_cart[food_info]["qty"] <= 0:
                        del st.session_state.new_cart[food_info]
                    st.rerun()
            with cart_col3:
                if st.button("➕", key=f"plus_{food_info}"):
                    st.session_state.new_cart[food_info]["qty"] += 1
                    st.rerun()
                    
        st.write("---")
        order_note = st.text_input("📝 訂單備註（例如：辣椒粉多一點、炸脆一點）")
        coupon = st.text_input("🏷️ 輸入折扣碼 (提示: VIP90 )")
        
        if coupon == "VIP90":
            discount = total * 0.1
            final_total = total - discount
            st.info(f"🎉 成功套用 9 折折扣碼！已折抵 {CURRENCY} {discount:.2f}")
        else:
            if coupon != "":
                st.error("❌ 折扣碼無效！")
            final_total = total
            
        st.markdown(f"### 💰 總金額：**{CURRENCY} {final_total:.2f}**")
        st.write("---")
        
        pay_method = st.radio(
            "💳 請選擇您的付款方式：", 
            ["DuitNow 線上轉賬", "到店支付現金 / 拿食物時付款"]
        )
        
        payment_closing_text = ""
        if pay_method == "DuitNow 線上轉賬":
            st.markdown(f"""
                <div style="background-color: #1F2937; padding: 15px; border-radius: 12px; margin-bottom: 10px; color: #FFFFFF;">
                    <h4 style="color: #FBBF24; margin-top: 0px; margin-bottom: 8px;">💳 DuitNow 轉賬收款說明</h4>
                    <p style="margin: 0px; font-size: 15px;">請手動轉賬總金額至老闆賬號，並在下單時附上截圖：</p>
                    <p style="margin: 5px 0px; font-size: 18px; font-weight: bold; color: #FBBF24;">📞 DuitNow 號碼：016-2002352</p>
                </div>
            """, unsafe_allow_html=True)
            payment_closing_text = f"老闆，我已經完成 DuitNow 轉賬 {CURRENCY} {final_total:.2f}，附圖是我的付款收據，請查收並核對單號 {st.session_state.order_id}，謝謝！"
        else:
            st.info("💡 提示：請在下單後，於現場取餐/用餐時向櫃檯支付現金。")
            payment_closing_text = f"老闆，我選擇現場支付現金。請幫我準備訂單，我會準時到店領取/用餐，謝謝！"
            
        st.write("---")
        
        # 建立發送給老闆的 WhatsApp 訊息格式
        items_summary = ""
        for idx, (food_info, item_data) in enumerate(st.session_state.new_cart.items(), 1):
            items_summary += f"{idx}. {food_info} x{item_data['qty']} ({CURRENCY} {item_data['price'] * item_data['qty']:.2f})\n"
            
        location_info = f"桌號: {table_number}" if dining_type == "內用 🍽️" else (f"外送地址: {delivery_address}" if dining_type == "外送 / 食物配送 🚗" else "外帶自取")
        
        whatsapp_message = (
            f"🔔【ALIS FRIED CHICKEN 新訂單】\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"📌 訂單單號：{st.session_state.order_id}\n"
            f"🥡 用餐方式：{dining_type}\n"
