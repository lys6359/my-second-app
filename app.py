# -*- coding: utf-8 -*-
import streamlit as st
import urllib.parse
import random
import os
from datetime import datetime

# 1. Konfigurasi Halaman 
st.set_page_config(page_title="Sistem Pesanan Makanan ALIS FRIED CHICKEN", page_icon="\U0001F357", layout="wide")

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
    /* Style untuk butang WhatsApp custom */
    .whatsapp-btn {
        display: block;
        width: 100%;
        background-color: #25D366;
        color: white !important;
        text-align: center;
        padding: 12px;
        font-weight: bold;
        font-size: 18px;
        border-radius: 8px;
        text-decoration: none;
        margin-top: 10px;
    }
    .whatsapp-btn:hover {
        background-color: #128C7E;
        text-decoration: none;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# Tajuk Utama
# ==========================================
st.title("\U0001F357 Sistem Pesanan Makanan ALIS FRIED CHICKEN")
st.write("Selamat datang! Sila pilih hidangan anda di bawah. Selepas daftar keluar, anda akan diarahkan ke WhatsApp untuk hantar pesanan kepada bos!")
st.write("---")

# 🌟 已經修復好第 54 行的錯誤編碼了！
dining_type = st.radio("Pilih cara makan anda:", ["Makan Di Sini \U0001F37D", "Bungkus (Takeaway) \U0001F41C", "Penghantaran (Delivery) \U0001F697"], horizontal=True, index=None)

# 使用 Unicode 安全編碼替換菜單名稱
menu = {
    "Ayam Gunting \U0001F357": 10.00,
    "Sosej Jumbo \U0001F32D": 6.00,
    "Sotong \U0001F991": 14.00,
    "Chicken Popcorn (7pcs) \U0001F37F": 5.00,
    "Ayam Tender \U0001F357\u2728": 3.00,
    "Satay Ayam \U0001F362": 3.00
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
            
            st.markdown(f"💰 Harga: **{CURRENCY} {actual_price:.2f}**")
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
    
    delivery_address = st.text_input("Masukkan Alamat Penghantaran Lengkap (Delivery Address):") if dining_type == "Penghantaran (Delivery) \U0001F697" else ""
    table_number = st.text_input("Masukkan Nombor Meja Anda (Table Number):") if dining_type == "Makan Di Sini \U0001F37D" else ""
        
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
            
        loc = f"No Meja: {table_number}" if dining_type == "Makan Di Sini \U0001F37D" else (f"Alamat: {delivery_address}" if dining_type == "Penghantaran (Delivery) \U0001F697" else "Ambil Sendiri (Takeaway)")
        
        whatsapp_message = (
            f"\U0001F31F【PESANAN BARU ALIS FRIED CHICKEN】\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"\U0001F4CC ID Pesanan: {st.session_state.order_id}\n"
            f"\U0001F41C Cara Makan: {dining_type}\n"
            f"\U0001F4CD Lokasi: {loc}\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"\U0001F4E6 Perincian:\n{items_summary}"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"\U0001F34A Nota: {order_note if order_note else 'Tiada'}\n"
            f"\U0001F4B3 Pembayaran: {pay_method}\n"
            f"\U0001F4B0 Jumlah: {CURRENCY} {final_total:.2f}\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"\U0001F4AC {p_text}"
        )
        
        encoded_message = urllib.parse.quote(whatsapp_message)
        whatsapp_url = f"https://wa.me{MY_PHONE_NUMBER}?text={encoded_message}"
        
        st.markdown(f'<a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">\u2705 SAHKAN PESANAN & HANTAR KE WHATSAPP</a>', unsafe_allow_html=True)
