import streamlit as st
import urllib.parse
import random
import os
from datetime import datetime

# 1. 網頁基本設定
st.set_page_config(page_title="ALIS FRIED CHICKEN 網頁點餐系統", page_icon="🍗", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FBBF24; color: #1F2937 !important; }
    h1, h2, h3 { color: #000000 !important; font-weight: 800 !important; }
    [data-testid="stContainer"] {
        background-color: #1F2937 !important; 
        border-radius: 16px !important;
        padding: 20px !important;
        border: none !important;
        margin-bottom: 15px !important;
    }
    [data-testid="stContainer"] .stMarkdown p, [data-testid="stContainer"] h3 { color: #FFFFFF !important; }
    [data-testid="stContainer"] button {
        background-color: #FBBF24 !important; color: #000000 !important; font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🍔 前台顧客點餐大標題
# ==========================================
st.title("🍗 ALIS FRIED CHICKEN 網頁點餐系統")
st.write("歡迎光臨！請在下方選擇您的餐點。結帳後將引導至 WhatsApp 發送訂單給老闆喔！")
st.write("---")

dining_type = st.radio("🥡 請選擇您的用餐方式：", ["內用 🍽️", "外帶 🛍️", "外送 / 食物配送 🚗"], horizontal=True, index=None)

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

if "order_id" not in st.session_state:
    st.session_state.order_id = f"ALIS-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"

col1, col2 = st.columns(2)

with col1:
    st.subheader("【 🍱 今日菜單 】")
    is_menu_disabled = True if dining_type is None else False
    if dining_type is None:
        st.error("⚠️ 請在網頁最上方先選擇您的「用餐方式」，才可以開始點餐喔！")

    for food, price in menu.items():
        with st.container():
            st.markdown(f"### {food}")
            if "Ayam Gunting" in food:
                size = st.selectbox("📐 選擇份量", ["Saiz Normal (RM 10.00)", "Saiz Besar (+RM 3.00)"], key="gunting_size")
                spicy = st.selectbox("🌶️ 選擇辣度", ["不辣", "微辣", "大辣"], key="gunting_spicy")
                actual_price = price + 3.00 if "Saiz Besar" in size else price
                full_food_name = f"{food} ({size}/{spicy})"
            elif "Sosej Jumbo" in food:
                sauce = st.selectbox("🥫 選擇醬料", ["辣椒醬", "番茄醬", "美乃滋", "不需要醬料"], key="sosej_sauce")
                actual_price = price
                full_food_name = f"{food} ({sauce})"
            elif "Sotong" in food:
                spicy = st.selectbox("🌶️ 選擇口味/辣度", ["不辣", "辣椒粉", "招牌胡椒鹽"], key="sotong_spicy")
                actual_price = price
                full_food_name = f"{food} ({spicy})"
            elif "Chicken Popcorn" in food:
                flavor = st.selectbox("🍿 選擇口味", ["原味", "椒鹽味", "起司粉 (+RM 1.00)"], key="popcorn_flavor")
                actual_price = price + 1.00 if "起司粉" in flavor else price
                full_food_name = f"{food} ({flavor})"
            elif "Ayam Tender" in food:
                qty_opt = st.selectbox("🔢 選擇數量", ["1pcs (RM 3.00)", "3pcs (RM 8.00)", "5pcs (RM 11.00)"], key="tender_qty")
                actual_price = 8.00 if "3pcs" in qty_opt else (11.00 if "5pcs" in qty_opt else 3.00)
                full_food_name = f"{food} ({qty_opt})"
            else:
                satay_opt = st.selectbox("🍢 選擇數量", ["1串 (RM 3.00)", "5串 (RM 15.00)", "10串 (RM 30.00)"], key="satay_qty")
                actual_price = 15.00 if "5串" in satay_opt else (30.00 if "10串" in satay_opt else 3.00)
                full_food_name = f"{food} ({satay_opt})"
            
            st.markdown(f"💰 價格：**{CURRENCY} {actual_price:.2f}**")
            if st.button(f"➕ 點購 {food}", key=f"btn_{food}", disabled=is_menu_disabled):
                if full_food_name in st.session_state.new_cart:
                    st.session_state.new_cart[full_food_name]["qty"] += 1
                else:
                    st.session_state.new_cart[full_food_name] = {"qty": 1, "price": actual_price}
                st.toast("已加入購物車！")
                st.rerun()

with col2:
    st.subheader("【 🛒 您的購物車 】")
    display_type = dining_type if dining_type else "⚠️ 尚未選擇"
    st.markdown(f"✨ 目前選擇：**{display_type}** | 🔢 單號：**{st.session_state.order_id}**") 
    
    delivery_address = st.text_input("🏠 完整外送地址 (Delivery Address):") if dining_type == "外送 / 食物配送 🚗" else ""
    table_number = st.text_input("🔢 請輸入您的桌號 (Table Number):") if dining_type == "內用 🍽️" else ""
        
    if not st.session_state.new_cart:
        st.write("購物車目前是空的喔！")
    else:
        total = 0
        st.write("---")
        for food_info, item_data in list(st.session_state.new_cart.items()):
            qty = item_data["qty"]
            item_price = item_data["price"]
            total += item_price * qty
            
            c1, c2, c3 = st.columns(3)
            with c1: st.write(f"▪️ **{food_info}** \n 單價: {CURRENCY} {item_price:.2f} x {qty}")
            with c2: 
                if st.button("➖", key=f"m_{food_info}"):
                    st.session_state.new_cart[food_info]["qty"] -= 1
                    if st.session_state.new_cart[food_info]["qty"] <= 0: del st.session_state.new_cart[food_info]
                    st.rerun()
            with c3:
                if st.button("➕", key=f"p_{food_info}"):
                    st.session_state.new_cart[food_info]["qty"] += 1
                    st.rerun()
                    
        st.write("---")
        order_note = st.text_input("📝 訂單備註")
        coupon = st.text_input("🏷️ 輸入折扣碼")
        final_total = total * 0.9 if coupon == "VIP90" else total
        if coupon == "VIP90": st.info(f"🎉 成功套用 9 折！已折抵 {CURRENCY} {total*0.1:.2f}")
            
        st.markdown(f"### 💰 總金額：**{CURRENCY} {final_total:.2f}**")
        st.write("---")
        
        pay_method = st.radio("💳 請選擇您的付款方式：", ["DuitNow 線上轉賬", "到店支付現金"])
        if pay_method == "DuitNow 線上轉賬":
            st.markdown(f'<div style="background-color: #1F2937; padding: 15px; border-radius: 12px; color: #FFFFFF;"><h4>💳 DuitNow 轉賬收款說明</h4><p>請手動轉賬總金額至老闆賬號：</p><p style="font-size: 18px; font-weight: bold; color: #FBBF24;">📞 號碼：016-2002352</p></div>', unsafe_allow_html=True)
            p_text = "我已完成 DuitNow 轉帳，稍後附上收據。"
        else:
            st.info("💡 提示：請在現場取餐/用餐時向櫃檯支付現金。")
            p_text = "我選擇現場支付現金。"
            
        st.write("---")
        
        items_summary = ""
        for idx, (f_info, i_data) in enumerate(st.session_state.new_cart.items(), 1):
            items_summary += f"{idx}. {f_info} x{i_data['qty']}\n"
            
        loc = f"桌號: {table_number}" if dining_type == "內用 🍽️" else (f"外送地址: {delivery_address}" if dining_type == "外送 / 食物配送 🚗" else "外帶自取")
        
        # 採用完全單行安全字串，100% 避免括號未閉合語法錯誤
        whatsapp_message = f"🔔【ALIS FRIED CHICKEN 新訂單】\n單號：{st.session_state.order_id}\n方式：{dining_type}\n位置：{loc}\n明細：\n{items_summary}備註：{order_note if order_note else '無'}\n付款：{pay_method}\n總額：{CURRENCY} {final_total:.2f}\n💬 {p_text}"
        
        whatsapp_url = f"https://wa.me/{MY_PHONE_NUMBER}?text={urllib.parse.quote(whatsapp_message)}"
        st.link_button("🟢 確認下單並發送 WhatsApp 訂單", whatsapp_url, use_container_width=True)
