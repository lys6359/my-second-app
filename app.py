# -*- coding: utf-8 -*-
import streamlit as st
import urllib.parse
import random
import os
from datetime import datetime

# ==========================================
# 1. 頁面配置與極簡亮色風格 CSS 樣式
# ==========================================
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
    [data-testid="stContainer"] button {
        background-color: #DC2626 !important; color: #FFFFFF !important; font-weight: bold !important;
        font-size: 16px !important; border-radius: 8px !important; border: none !important; width: 100% !important; height: 40px !important;
    }
    /* 強制將官方連結按鈕渲染成漂亮的 WhatsApp App 亮綠色外觀 */
    div.stLinkButton > a {
        background-color: #25D366 !important; color: #FFFFFF !important; font-weight: bold !important;
        font-size: 18px !important; border-radius: 8px !important; border: none !important;
        padding: 14px 20px !important; text-align: center !important; display: block !important;
        box-shadow: 0 4px 10px rgba(37, 211, 102, 0.3) !important;
    }
    div.stLinkButton > a:hover { background-color: #128C7E !important; color: #FFFFFF !important; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 全域持久狀態初始化 (st.session_state)
# ==========================================
if "new_cart" not in st.session_state: st.session_state.new_cart = {}
if "order_id" not in st.session_state: st.session_state.order_id = f"EP-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
if "dining_type" not in st.session_state: st.session_state.dining_type = None
if "delivery_address" not in st.session_state: st.session_state.delivery_address = ""
if "table_number" not in st.session_state: st.session_state.table_number = ""

CURRENCY = "RM"
MY_PHONE_NUMBER = "60162002352"

# ==========================================
# 3. 標題與用餐方式選擇
# ==========================================
st.markdown("<h1 style='text-align: center;'>🍗 ALIS FRIED CHICKEN</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6B7280;'>Sajian panas, ranggup, dan segar setiap hari!</p>", unsafe_allow_html=True)
st.write("---")

# 透過選單即時更新系統緩存狀態
selected_dining = st.radio("🥡 Sila pilih cara makan anda:", ["Makan Di Sini", "Bungkus (Takeaway)", "Penghantaran (Delivery)"], horizontal=True, index=None)
if selected_dining:
    st.session_state.dining_type = selected_dining

st.write("---")

# ==========================================
# 4. 菜單資料庫
# ==========================================
menu_data = {
    "Ayam Gunting": {"price": 10.00, "img": "ayam_gunting.jpg", "desc": "Ayam gunting ranggup bersaiz besar with rempah istimewa."},
    "Sosej Jumbo": {"price": 6.00, "img": "sosej_jumbo.jpg", "desc": "Sosej jumbo premium, digoreng sempurna."},
    "Sotong": {"price": 14.00, "img": "sotong.jpg", "desc": "Sotong celup tepung ranggup gila, kegemaran ramai."},
    "Chicken Popcorn (7pcs)": {"price": 5.00, "img": "popcorn.jpg", "desc": "Bebola ayam bersaiz snek, mudah dimakan."},
    "Ayam Tender": {"price": 3.00, "img": "tender.jpg", "desc": "Isi ayam lembut tanpa tulang, digoreng ranggup."},
    "Satay Ayam": {"price": 3.00, "img": "satay.jpg", "desc": "Satay ayam digoreng wangi dengan perapan tradisional."}
}

# ==========================================
# 5. 菜單渲染邏輯
# ==========================================
tab1, tab2 = st.tabs(["🔥 Popular", "🍗 Semua Menu (Semua)"])

def paparkan_menu(senarai_makanan, tab_name):
    is_menu_disabled = True if st.session_state.dining_type is None else False
    
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
# 6. 購物車與欄位輸入區塊
# ==========================================
st.write("---")
st.markdown("<h2>🛒 Troli & Pesanan Anda</h2>", unsafe_allow_html=True)

if st.session_state.dining_type is None:
    st.markdown("<p style='color:red; font-weight:bold;'>⚠️ Sila pilih cara makan anda di bahagian atas terlebih dahulu!</p>", unsafe_allow_html=True)

is_address_missing = False

# 當顧客選了用餐方式，立即渲染輸入欄位
if st.session_state.dining_type:
    if st.session_state.dining_type in ["Bungkus (Takeaway)", "Penghantaran (Delivery)"]:
        input_address = st.text_input("🏠 Masukkan Alamat Lengkap Sila (Address Required):", value=st.session_state.delivery_address)
        st.session_state.delivery_address = input_address
        
        if st.session_state.dining_type == "Penghantaran (Delivery)":
            st.info("💡 **Nota Penghantaran:** Caj penghantaran akan dibayar kepada runner semasa menerima makanan.")
        
        if not st.session_state.delivery_address.strip():
            is_address_missing = True
            
    elif st.session_state.dining_type == "Makan Di Sini":
        input_table = st.text_input("🔢 Nombor Meja Anda (Table Number):", value=st.session_state.table_number)
        st.session_state.table_number = input_table
        
        if not st.session_state.table_number.strip():
            is_address_missing = True

total_amount = 0.0

if not st.session_state.new_cart:
    st.markdown("<p style='color:#6B7280;'>Troli anda masih kosong. Sila klik ➕ Tambah pada menu di atas.</p>", unsafe_allow_html=True)
else:
    # 渲染購物車內品項
    for food_name, item_data in list(st.session_state.new_cart.items()):
        item_total = item_data["qty"] * item_data["price"]
        total_amount += item_total
        
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"**{food_name}**")
                st.markdown(f"<p style='color:#6B7280; font-size:14px;'>{CURRENCY} {item_data['price']:.2f} x {item_data['qty']}</p>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"**{CURRENCY} {item_total:.2f}**")
            with col3:
                if st.button("❌", key=f"del_{food_name}"):
                    del st.session_state.new_cart[food_name]
                    st.rerun()

    st.write("---")
