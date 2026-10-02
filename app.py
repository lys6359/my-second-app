# -*- coding: utf-8 -*-
import streamlit as st
import urllib.parse
import random
import os
from datetime import datetime

# 1. Halaman & Visual CSS - Reka Bentuk Telefon App Mod Cerah 
st.set_page_config(page_title="Sistem Pesanan Makanan ALIS FRIED CHICKEN", page_icon="🍗", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background-color: #F9FAFB; 
        color: #1F2937 !important;
    }
    h1, h2, h3 {
        color: #991B1B !important;
        font-weight: 800 !important;
    }
    .stMarkdown p, span, p {
        color: #374151 !important;
    }
    [data-testid="stContainer"] {
        background-color: #FFFFFF !important; 
        border-radius: 16px !important;
        padding: 16px !important;
        border: 1px solid #E5E7EB !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
        margin-bottom: 14px !important;
    }
    [data-testid="stContainer"] h3 {
        color: #111827 !important;
        margin-bottom: 4px !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #E5E7EB !important;
        color: #374151 !important;
        border-radius: 20px !important;
        padding: 6px 16px !important;
        font-weight: bold !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #991B1B !important;
        color: #FFFFFF !important;
    }
    [data-testid="stContainer"] button {
        background-color: #DC2626 !important;
        color: #FFFFFF !important;
        font-weight: bold !important;
        font-size: 18px !important;
        border-radius: 8px !important;
        border: none !important;
        width: 100% !important;
        height: 42px !important;
        margin-top: 10px !important;
    }
    .custom-whatsapp-btn {
        display: block !important;
        width: 100% !important;
        background-color: #25D366 !important; 
        color: #FFFFFF !important;            
        text-align: center !important;
        padding: 14px !important;
        font-weight: bold !important;
        font-size: 18px !important;
        border-radius: 8px !important;
        text-decoration: none !important;
        margin-top: 20px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.15) !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# Tajuk Utama
# ==========================================
st.markdown("<h1 style='text-align: center;'>🍗 ALIS FRIED CHICKEN</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6B7280;'>Sajian panas, ranggup, dan segar setiap hari!</p>", unsafe_allow_html=True)
st.write("---")

dining_type = st.radio(" Sila pilih cara makan anda:", ["Makan Di Sini", "Bungkus (Takeaway)", "Penghantaran (Delivery)"], horizontal=True, index=None)
st.write("---")

menu_data = {
    "Ayam Gunting": {"price": 10.00, "img": "ayam_gunting.jpg", "desc": "Ayam gunting ranggup bersaiz besar with rempah istimewa."},
    "Sosej Jumbo": {"price": 6.00, "img": "sosej_jumbo.jpg", "desc": "Sosej jumbo premium, digoreng sempurna."},
    "Sotong": {"price": 14.00, "img": "sotong.jpg", "desc": "Sotong celup tepung ranggup gila, kegemaran ramai."},
    "Chicken Popcorn (7pcs)": {"price": 5.00, "img": "popcorn.jpg", "desc": "Bebola ayam bersaiz snek, mudah dimakan."},
    "Ayam Tender": {"price": 3.00, "img": "tender.jpg", "desc": "Isi ayam lembut tanpa tulang, digoreng ranggup."},
    "Satay Ayam": {"price": 3.00, "img": "satay.jpg", "desc": "Satay ayam digoreng wangi dengan perapan tradisional."}
}

CURRENCY = "RM"
MY_PHONE_NUMBER = "60162002352"

if "new_cart" not in st.session_state:
    st.session_state.new_cart = {}

if "order_id" not in st.session_state:
    st.session_state.order_id = f"EP-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"

is_address_missing = False
is_payment_missing = False
delivery_address = ""
table_number = ""
p_text = ""

tab1, tab2 = st.tabs(["🔥 Popular", "🍗 Semua Menu (Semua)"])

def paparkan_menu(senarai_makanan, tab_name):
    is_menu_disabled = True if dining_type is None else False
    for food in senarai_makanan:
        price = menu_data[food]["price"]
        img_file = menu_data[food]["img"]
        desc_text = menu_data[food]["desc"]
        
        with st.container():
            img_col, info_col = st.columns(2)
            with img_col:
                if os.path.exists(img_file):
                    st.image(img_file, use_container_width=True)
                else:
                    st.markdown(f'<div style="background-color: #E5E7EB; width: 100%; aspect-ratio: 1; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #9CA3AF; border: 1px dashed #D1D5DB;">📷 {food}</div>', unsafe_allow_html=True)
            
            with info_col:
                st.markdown(f"### {food}")
                st.markdown(f"<p style='color: #6B7280; font-size: 14px; margin-top:-5px;'>{desc_text}</p>", unsafe_allow_html=True)
                
                if "Ayam Gunting" in food:
                    size = st.selectbox("Saiz", ["Saiz Normal (RM 10.00)", "Saiz Besar (+RM 3.00)"], key=f"{food}_sz_{tab_name}")
                    flavor = st.selectbox("Perisa", ["Original", "Pedas"], key=f"{food}_flv_{tab_name}")
                    actual_price = price + 3.00 if "Saiz Besar" in size else price
                    full_food_name = f"{food} ({size}/{flavor})"
                elif "Ayam Tender" in food:
                    qty_opt = st.selectbox("Kuantiti", ["1pcs (RM 3.00)", "3pcs (RM 8.00)", "5pcs (RM 11.00)"], key=f"{food}_qt_{tab_name}")
                    flavor = st.selectbox("Perisa", ["Original", "Pedas"], key=f"{food}_flv_{tab_name}")
                    actual_price = 8.00 if "3pcs" in qty_opt else (11.00 if "5pcs" in qty_opt else 3.00)
                    full_food_name = f"{food} ({qty_opt}/{flavor})"
                else:
                    flavor = st.selectbox("Perisa", ["Original", "Pedas"], key=f"{food}_flv_{tab_name}")
                    actual_price = price
                    full_food_name = f"{food} ({flavor})"
                
                st.markdown(f"<p style='color: #DC2626; font-weight: bold; font-size: 18px; margin-top:5px;'>{CURRENCY} {actual_price:.2f}</p>", unsafe_allow_html=True)
                if st.button(f" Tambah", key=f"btn_{food}_{tab_name}", disabled=is_menu_disabled):
                    if full_food_name in st.session_state.new_cart:
                        st.session_state.new_cart[full_food_name]["qty"] += 1
                    else:
                        st.session_state.new_cart[full_food_name] = {"qty": 1, "price": actual_price}
                    st.toast("Telah ditambah ke troli!")
                    st.rerun()

with tab1: paparkan_menu(["Ayam Gunting", "Sotong", "Chicken Popcorn (7pcs)"], "Popular")
with tab2: paparkan_menu(list(menu_data.keys()), "Semua")

# ==========================================
# Bahagian Troli & Pesanan Anda
# ==========================================
st.write("---")
st.markdown("<h2>🛒 Troli & Pesanan Anda</h2>", unsafe_allow_html=True)

if dining_type is None:
    st.error(" Sila pilih 'cara makan' anda di bahagian atas terlebih dahulu sebelum memesan!")

if dining_type:
    if "Delivery" in dining_type or "Penghantaran" in dining_type:
        delivery_address = st.text_input("🏠 Masukkan Alamat Penghantaran Lengkap (Delivery Address):")
        st.info("💡 **Nota Penghantaran:** Sila ambil perhatian, caj penghantaran akan dibayar secara berasingan kepada penghantar (runner) semasa menerima makanan.")
        if not delivery_address.strip():
            is_address_missing = True
            st.error(" Sila masukkan alamat penghantaran anda terlebih dahulu!")
    elif "Makan Di Sini" in dining_type:
        table_number = st.text_input(" Nombor Meja Anda (Table Number):")

total = 0
if not st.session_state.new_cart:
    st.info("Troli anda masih kosong. Sila klik  Tambah pada menu di atas.")
else:
    for food_info, item_data in list(st.session_state.new_cart.items()):
        qty = item_data["qty"]
        item_price = item_data["price"]
        total += item_price * qty
        
        cart_col1, cart_col2 = st.columns(2)
        with cart_col1: 
            st.markdown(f"**{food_info}** <br><span style='color: #6B7280;'>({CURRENCY} {item_price:.2f} x {qty})</span>", unsafe_allow_html=True)
        with cart_col2:
            btn_m, btn_p = st.columns(2)
            with btn_m:
                if st.button("➖", key=f"m_{food_info}_app"):
                    st.session_state.new_cart[food_info]["qty"] -= 1
                    if st.session_state.new_cart[food_info]["qty"] <= 0: del st.session_state.new_cart[food_info]
                    st.rerun()
            with btn_p:
                if st.button("➕", key=f"p_{food_info}_app"):
                    st.session_state.new_cart[food_info]["qty"] += 1
                    st.rerun()

st.write("---")
order_note = st.text_input(" Nota Pesanan (cth: nak garing lebih, pedas lebih)")
coupon = st.text_input(" Masukkan Kod Kupon")
final_total = total * 0.9 if coupon == "VIP90" else total
if coupon == "VIP90" and total > 0: st.info(f" Diskaun 10% berjaya digunakan!")
    
st.markdown(f"###  Jumlah Keseluruhan: **{CURRENCY} {final_total:.2f}**")
st.write("---")

pay_method = st.radio(" Sila pilih kaedah pembayaran:", ["DuitNow (Pindahan Dalam Talian)", "Bayar Tunai Semasa Ambil / Makan"], index=None)

if pay_method == "DuitNow (Pindahan Dalam Talian)":
