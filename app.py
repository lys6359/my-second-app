# -*- coding: utf-8 -*-
import streamlit as st
import urllib.parse
import random
import os
from datetime import datetime

# 1. Konfigurasi Halaman & CSS Style Mod Cerah
st.set_page_config(page_title="Sistem Pesanan Makanan ALIS FRIED CHICKEN", page_icon="🍗", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #F9FAFB; color: #1F2937 !important; }
    h1, h2, h3 { color: #991B1B !important; font-weight: 800 !important; }
    .stMarkdown p, span, p { color: #374151 !important; }
    [data-testid="stContainer"] {
        background-color: #FFFFFF !important; border-radius: 16px !important; padding: 16px !important;
        border: 1px solid #E5E7EB !important; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important; margin-bottom: 14px !important;
    }
    [data-testid="stContainer"] h3 { color: #111827 !important; margin-bottom: 4px !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #E5E7EB !important; color: #374151 !important;
        border-radius: 20px !important; padding: 6px 16px !important; font-weight: bold !important;
    }
    .stTabs [aria-selected="true"] { background-color: #991B1B !important; color: #FFFFFF !important; }
    
    .stButton > button {
        background-color: #DC2626 !important; color: #FFFFFF !important; font-weight: bold !important;
        font-size: 14px !important; border-radius: 8px !important; border: none !important; width: 100% !important; height: 35px !important;
    }
    
    /* 確保手機 App 亮綠色 WhatsApp 按鈕 100% 穩定強制顯示 */
    [data-testid="stBaseButton-link"] {
        background-color: #25D366 !important; 
        color: #FFFFFF !important; 
        font-weight: bold !important;
        font-size: 18px !important; 
        border-radius: 8px !important; 
        border: none !important;
        padding: 14px 20px !important; 
        text-align: center !important; 
        display: inline-flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        box-shadow: 0 4px 10px rgba(37, 211, 102, 0.3) !important;
        text-decoration: none !important;
    }
    [data-testid="stBaseButton-link"]:hover { 
        background-color: #128C7E !important; 
        color: #FFFFFF !important; 
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 初始化 Session State
# ==========================================
if "new_cart" not in st.session_state: st.session_state.new_cart = {}
if "order_id" not in st.session_state: st.session_state.order_id = f"EP-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
if "address_val" not in st.session_state: st.session_state.address_val = ""
if "table_val" not in st.session_state: st.session_state.table_val = ""
if "note_val" not in st.session_state: st.session_state.note_val = ""  

# ==========================================
# Tajuk Utama
# ==========================================
st.markdown("<h1 style='text-align: center;'>🍗 ALIS FRIED CHICKEN</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6B7280;'>Sajian panas, ranggup, dan segar setiap hari!</p>", unsafe_allow_html=True)
st.write("---")

dining_type = st.radio("🥡 Sila pilih cara makan anda:", ["Makan Di Sini", "Bungkus (Takeaway)", "Penghantaran (Delivery)"], horizontal=True, index=None)
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
                    st.markdown(f'<div style="background-color: #E5E7EB; width: 100%; aspect-ratio: 1; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #9CA3AF; border: 1px dashed #D1D5DB; font-size:14px; text-align:center; padding:5px;">📷<br>{food}</div>', unsafe_allow_html=True)
            
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
                
                st.markdown(f"<p style='color: #DC2626; font-weight: bold; font-size: 18px; margin-top:5px;'>Harga: {CURRENCY} {actual_price:.2f}</p>", unsafe_allow_html=True)
                if st.button(f"➕ Tambah", key=f"btn_{food}_{tab_name}", disabled=is_menu_disabled):
                    if full_food_name in st.session_state.new_cart: 
                        st.session_state.new_cart[full_food_name]["qty"] += 1
                    else: 
                        st.session_state.new_cart[full_food_name] = {"qty": 1, "price": actual_price}
                    st.toast(f"{full_food_name} ditambahkan ke troli!")
                    st.rerun()

with tab1: paparkan_menu(["Ayam Gunting", "Sotong", "Chicken Popcorn (7pcs)"], "Popular")
with tab2: paparkan_menu(list(menu_data.keys()), "Semua")

# ==========================================
# Bahagian Troli & Pengesahan
# ==========================================
st.write("---")
st.markdown("<h2>🛒 Troli & Pesanan Anda</h2>", unsafe_allow_html=True)

if dining_type is None:
    st.markdown("<p style='color:red; font-weight:bold;'>⚠️ Sila pilih cara makan anda di bahagian atas terlebih dahulu!</p>", unsafe_allow_html=True)
else:
    if "Makan Di Sini" in dining_type:
        st.session_state.table_val = st.text_input("🔢 Nombor Meja Anda (Table Number):", value=st.session_state.table_val)
    elif "Penghantaran (Delivery)" in dining_type:
        st.session_state.address_val = st.text_input("🏠 Masukkan Alamat Lengkap Sila (Address Required):", value=st.session_state.address_val)
        st.info("💡 **Nota Penghantaran:** Caj penghantaran akan dibayar kepada runner semasa menerima makanan.")
    elif "Bungkus (Takeaway)" in dining_type:
        st.session_state.address_val = st.text_input("🏠 Masukkan Alamat Lengkap (Opsional untuk Takeaway):", value=st.session_state.address_val)

    st.session_state.note_val = st.text_area("📝 Catatan / Nota (Remark / Special Request):", value=st.session_state.note_val, placeholder="Cth: Jangan letak pedas, atau bungkus asing...")

total_amount = 0.0

if not st.session_state.new_cart:
    st.markdown("<p style='color:#6B7280;'>Troli anda masih kosong. Sila klik ➕ Tambah pada menu di atas.</p>", unsafe_allow_html=True)
else:
    # 🌟 徹底根除方案：移除 st.markdown("""...""") 改用最安全、絕不報錯的單行字串拼接呈現購物車明細
    for food_name, item_data in list(st.session_state.new_cart.items()):
        item_total = item_data["qty"] * item_data["price"]
        total_amount += item_total
        
        with st.container():
            st.markdown("🔹 **" + str(food_name) + "**")
            st.write("Kuantiti: " + str(item_data['qty']) + " | Harga Seunit: " + CURRENCY + " " + f"{item_data['price']:.2f}" + " | Jumlah: " + CURRENCY + " " + f"{item_total:.2f}")
            
            if st.button("🗑️ Kurangkan 1", key="del_btn_" + str(food_name)):
                st.session_state.new_cart[food_name]["qty"] -= 1
                if st.session_state.new_cart[food_name]["qty"] <= 0:
                    del st.session_state.new_cart[food_name]
                st.rerun()

    st.write("---")
    st.markdown(f"<h3 style='text-align: right;'>Jumlah Keseluruhan: <span style='color:#DC2626;'>{CURRENCY} {total_amount:.2f}</span></h3>", unsafe_allow_html=True)
    
    # 💰 銀行付款資訊
    st.write("---")
    with st.container():
        st.markdown("### 💰 Cara Pembayaran (Maklumat Bank)")
        st.markdown("""
