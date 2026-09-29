# -*- coding: utf-8 -*-
import streamlit as st
import urllib.parse
import random
import os
from datetime import datetime

# 定義 100% 安全的 Emoji 變數 (使用 chr 避開所有轉碼 Bug)
EMOJI_AYAM = chr(127879)      # 🍗
EMOJI_PLATE = chr(127837)     # 🍽️
EMOJI_BAG = chr(128093)       # 🛍️
EMOJI_CAR = chr(128663)       # 🚗
EMOJI_HOTDOG = chr(127853)    # 🌭
EMOJI_SQUID = chr(129425)     # 🦑
EMOJI_POPCORN = chr(127871)   # 🍿
EMOJI_SPARKLE = chr(10024)    # ✨
EMOJI_SATAY = chr(127842)     # 🍢
EMOJI_MONEY = chr(128176)     # 💰
EMOJI_STAR = chr(127775)      # 🌟
EMOJI_PIN = chr(128204)       # 📌
EMOJI_BOX = chr(128230)       # 📦
EMOJI_NOTE = chr(127818)      # 📝
EMOJI_CARD = chr(128179)      # 💳
EMOJI_CHAT = chr(128172)      # 💬
EMOJI_CHECK = chr(9989)       # ✅

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Sistem Pesanan Makanan ALIS FRIED CHICKEN", page_icon=EMOJI_AYAM, layout="wide")

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
    .whatsapp-btn {
        display: block;
        width: 100%;
        background-color: #25D366;
        color: white !important;
        text-align: center;
        padding: 14px;
        font-weight: bold;
        font-size: 18px;
        border-radius: 8px;
        text-decoration: none;
        margin-top: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .whatsapp-btn:hover {
        background-color: #128C7E;
        text-decoration: none;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# Tajuk Utama
# ==========================================
st.title(f"{EMOJI_AYAM} Sistem Pesanan Makanan ALIS FRIED CHICKEN")
st.write("Selamat datang! Sila pilih hidangan anda di bawah. Selepas daftar keluar, anda akan diarahkan ke WhatsApp untuk hantar pesanan kepada bos!")
st.write("---")

# 獲取用餐方式選擇
dining_type = st.radio(
    "Pilih cara makan anda:", 
    [f"Makan Di Sini {EMOJI_PLATE}", f"Bungkus (Takeaway) {EMOJI_BAG}", f"Penghantaran (Delivery) {EMOJI_CAR}"], 
    horizontal=True, 
    index=None
)

menu = {
    f"Ayam Gunting {EMOJI_AYAM}": 10.00,
    f"Sosej Jumbo {EMOJI_HOTDOG}": 6.00,
    f"Sotong {EMOJI_SQUID}": 14.00,
    f"Chicken Popcorn (7pcs) {EMOJI_POPCORN}": 5.00,
    f"Ayam Tender {EMOJI_AYAM}{EMOJI_SPARKLE}": 3.00,
    f"Satay Ayam {EMOJI_SATAY}": 3.00
}

CURRENCY = "RM"
MY_PHONE_NUMBER = "60162002352"

if "new_cart" not in st.session_state:
    st.session_state.new_cart = {}

if "order_id" not in st.session_state:
    date_str = datetime.now().strftime("%Y%m%d")
    st.session_state.order_id = f"ALIS-{date_str}-{random.randint(1000, 9999)}"

col1, col2 = st.columns(2)

with col1:
    st.subheader(" Menu Hari Ini ")
    is_menu_disabled = True if dining_type is None else False
    if dining_type is None:
        st.error(" Sila pilih 'cara makan' anda di bahagian atas halaman terlebih dahulu sebelum membuat pesanan!")

    for food, price in menu.items():
        with st.container():
            st.markdown(f"### {food}")
            if "Ayam Gunting" in food:
                size = st.selectbox("Pilih Saiz", ["Saiz Normal (RM 10.00)", "Saiz Besar (+RM 3.00)"], key="gunting_size")
                spicy = st.selectbox("Tahap Kepedasan", ["Kurang Pedas", "Pedas Biasa", "Sangat Pedas"], key="gunting_spicy")
                actual_price = price + 3.00 if "Saiz Besar" in size else price
                full_food_name = f"{food} ({size}/{spicy})"
            elif "Sosej Jumbo" in food:
                sauce = st.selectbox("Pilih Sos", ["Sos Cili", "Sos Tomato", "Mayonis", "Tanpa Sos"], key="sosej_sauce")
                actual_price = price
                full_food_name = f"{food} ({sauce})"
            elif "Sotong" in food:
                spicy = st.selectbox("Pilih Perisa / Kepedasan", ["Original", "Serbuk Cili", "Serbuk Lada Hitam (Signature)"], key="sotong_spicy")
                actual_price = price
                full_food_name = f"{food} ({spicy})"
            elif "Chicken Popcorn" in food:
                flavor = st.selectbox("Pilih Perisa", ["Original", "Perisa Lada Sulah", "Serbuk Keju (+RM 1.00)"], key="popcorn_flavor")
                actual_price = price + 1.00 if "Keju" in flavor else price
                full_food_name = f"{food} ({flavor})"
            elif "Ayam Tender" in food:
                qty_opt = st.selectbox("Pilih Kuantiti", ["1pcs (RM 3.00)", "3pcs (RM 8.00)", "5pcs (RM 11.00)"], key="tender_qty")
                actual_price = 8.00 if "3pcs" in qty_opt else (11.00 if "5pcs" in qty_opt else 3.00)
                full_food_name = f"{food} ({qty_opt})"
            else:
                satay_opt = st.selectbox("Pilih Kuantiti", ["1 Cucuk (RM 3.00)", "5 Cucuk (RM 15.00)", "10 Cucuk (RM 30.00)"], key="satay_qty")
                actual_price = 15.00 if "5 Cucuk" in satay_opt else (30.00 if "10 Cucuk" in satay_opt else 3.00)
                full_food_name = f"{food} ({satay_opt})"
            
            st.markdown(f"{EMOJI_MONEY} Harga: **{CURRENCY} {actual_price:.2f}**")
            if st.button(f" Tambah {food}", key=f"btn_{food}", disabled=is_menu_disabled):
                if full_food_name in st.session_state.new_cart:
                    st.session_state.new_cart[full_food_name]["qty"] += 1
                else:
                    st.session_state.new_cart[full_food_name] = {"qty": 1, "price": actual_price}
                st.toast("Telah ditambah ke troli!")
                st.rerun()

with col2:
    st.subheader(" Troli Anda ")
    display_type = dining_type if dining_type else "Belum Pilih"
    st.markdown(f" Pilihan: **{display_type}** | No ID Pesanan: **{st.session_state.order_id}**") 
    
    # 🌟 修正點：使用關鍵字檢查 dining_type，確保不論是否有變數都能完美判斷地址與桌號輸入框！
    delivery_address = ""
    table_number = ""
    if dining_type:
        if "Delivery" in dining_type:
            delivery_address = st.text_input("Masukkan Alamat Penghantaran Lengkap (Delivery Address):")
        elif "Makan Di Sini" in dining_type:
            table_number = st.text_input("Masukkan Nombor Meja Anda (Table Number):")
        
    if not st.session_state.new_cart:
        st.write("Troli anda masih kosong!")
    else:
        total = 0
        st.write("---")
        for food_info, item_data in list(st.session_state.new_cart.items()):
            qty = item_data["qty"]
            item_price = item_data["price"]
            total += item_price * qty
            
            c1, c2, c3 = st.columns(3)
            with c1: st.write(f"- **{food_info}** \nHarga: {CURRENCY} {item_price:.2f} x {qty}")
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
        order_note = st.text_input("Nota Pesanan (cth: nak pedas lebih, goreng garing)")
        coupon = st.text_input("Masukkan Kod Kupon")
        final_total = total * 0.9 if coupon == "VIP90" else total
        if coupon == "VIP90": st.info(f"🎉 Diskaun 10% berjaya digunakan! Dijimatkan {CURRENCY} {total*0.1:.2f}")
            
        st.markdown(f"### Jumlah Keseluruhan: **{CURRENCY} {final_total:.2f}**")
        st.write("---")
        
        pay_method = st.radio("Sila pilih kaedah pembayaran:", ["DuitNow (Pindahan Dalam Talian)", "Bayar Tunai Semasa Ambil / Makan"])
        if pay_method == "DuitNow (Pindahan Dalam Talian)":
            st.markdown(f'<div style="background-color: #1F2937; padding: 15px; border-radius: 12px; color: #FFFFFF;"><h4>Arahan Pembayaran DuitNow</h4><p>Sila buat pindahan tunai jumlah keseluruhan ke akaun bos:</p><p style="font-size: 18px; font-weight: bold; color: #FBBF24;">No. DuitNow: 016-2002352</p></div>', unsafe_allow_html=True)
            p_text = "Saya telah buat pembayaran melalui DuitNow. Resit akan dihantar sekejap lagi."
        else:
            st.info("💡 Nota: Sila buat pembayaran tunai di kaunter semasa mengambil makanan / makan di kedai.")
            p_text = "Saya memilih untuk bayar tunai di kedai."
            
        st.write("---")
        
        items_summary = ""
        for idx, (f_info, i_data) in enumerate(st.session_state.new_cart.items(), 1):
            items_summary += f"{idx}. {f_info} x{i_data['qty']}\n"
            
        # 🌟 修正點：比對位置文字時改用靈活判斷，徹底防止按鈕失蹤
        if dining_type and "Makan Di Sini" in dining_type:
            loc = f"No Meja: {table_number}"
        elif dining_type and "Delivery" in dining_type:
            loc = f"Alamat: {delivery_address}"
        else:
            loc = "Ambil Sendiri (Takeaway)"
        
        whatsapp_message = (
            f"{EMOJI_STAR}【PESANAN BARU ALIS FRIED CHICKEN】\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"{EMOJI_PIN} ID Pesanan: {st.session_state.order_id}\n"
            f"{EMOJI_BAG} Cara Makan: {dining_type}\n"
            f"{EMOJI_PIN} Lokasi: {loc}\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"{EMOJI_BOX} Perincian:\n{items_summary}"
            f"━━━━━━━━━━━━━━━━━━━\n"
