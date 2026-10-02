# -*- coding: utf-8 -*-
import streamlit as st
import urllib.parse
import random
from datetime import datetime

# 1. Konfigurasi Halaman & CSS Style Mod Cerah (強效鎖定白底紅鈕外觀，不佔行數)
st.set_page_config(page_title="Sistem Pesanan Makanan ALIS FRIED CHICKEN", page_icon="🍗", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #F9FAFB; color: #1F2937 !important; }
    h1, h2, h3 { color: #991B1B !important; font-weight: 800 !important; }
    .stMarkdown p, span, p { color: #374151 !important; }
    [data-testid="stContainer"] {
        background-color: #FFFFFF !important; border-radius: 16px !important; padding: 16px !important;
        border: 1px solid #E5E7EB !important; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05) !important; margin-bottom: 14px !important;
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
    </style>
""", unsafe_allow_html=True)

# ==========================================
# Tajuk Utama
# ==========================================
st.markdown("<h1 style='text-align: center;'>🍗 ALIS FRIED CHICKEN</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6B7280;'>Sajian panas, ranggup, dan segar setiap hari!</p>", unsafe_allow_html=True)
st.write("---")

dining_type = st.radio("🥡 Sila pilih cara makan anda:", ["Makan Di Sini", "Bungkus (Takeaway)", "Penghantaran (Delivery)"], horizontal=True, index=None)
st.write("---")

menu_data = {
    "Ayam Gunting": {"price": 10.00, "desc": "Ayam gunting ranggup bersaiz besar with rempah istimewa."},
    "Sosej Jumbo": {"price": 6.00, "desc": "Sosej jumbo premium, digoreng sempurna."},
    "Sotong": {"price": 14.00, "desc": "Sotong celup tepung ranggup gila, kegemaran ramai."},
    "Chicken Popcorn (7pcs)": {"price": 5.00, "desc": "Bebola ayam bersaiz snek, mudah dimakan."},
    "Ayam Tender": {"price": 3.00, "desc": "Isi ayam lembut tanpa tulang, digoreng ranggup."},
    "Satay Ayam": {"price": 3.00, "desc": "Satay ayam digoreng wangi dengan perapan tradisional."}
}

CURRENCY = "RM"
MY_PHONE_NUMBER = "60162002352"

if "new_cart" not in st.session_state: st.session_state.new_cart = {}
if "order_id" not in st.session_state: st.session_state.order_id = f"EP-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"

is_address_missing = False
delivery_address = ""
table_number = ""
p_text = ""

tab1, tab2 = st.tabs(["🔥 Popular", "🍗 Semua Menu (Semua)"])

def paparkan_menu(senarai_makanan, tab_name):
    is_menu_disabled = True if dining_type is None else False
    for food in senarai_makanan:
        price = menu_data[food]["price"]
        desc_text = menu_data[food]["desc"]
        
        with st.container():
            st.markdown(f"### {food}")
            st.write(desc_text)
            
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
            
            st.markdown(f"<p style='color: #DC2626; font-weight: bold; font-size: 16px;'>Harga: {CURRENCY} {actual_price:.2f}</p>", unsafe_allow_html=True)
            if st.button(f"➕ Tambah", key=f"btn_{food}_{tab_name}", disabled=is_menu_disabled):
                if full_food_name in st.session_state.new_cart: st.session_state.new_cart[full_food_name]["qty"] += 1
                else: st.session_state.new_cart[full_food_name] = {"qty": 1, "price": actual_price}
                st.toast("Telah ditambah ke troli!")
                st.rerun()

with tab1: paparkan_menu(["Ayam Gunting", "Sotong", "Chicken Popcorn (7pcs)"], "Popular")
with tab2: paparkan_menu(list(menu_data.keys()), "Semua")

# ==========================================
# Bahagian Troli 
# ==========================================
st.write("---")
st.markdown("<h2>🛒 Troli & Pesanan Anda</h2>", unsafe_allow_html=True)

if dining_type is None: st.error("⚠️ Sila pilih 'cara makan' anda di bahagian atas terlebih dahulu!")

if dining_type:
    if "Delivery" in dining_type or "Penghantaran" in dining_type:
        delivery_address = st.text_input("🏠 Masukkan Alamat Penghantaran Lengkap:")
        st.info("💡 **Nota Penghantaran:** Caj penghantaran akan dibayar kepada runner semasa menerima makanan.")
        if not delivery_address.strip(): is_address_missing = True
    elif "Makan Di Sini" in dining_type:
        table_number = st.text_input("🔢 Nombor Meja Anda:")

total = 0
if not st.session_state.new_cart:
    st.info("Troli anda masih kosong.")
else:
    for food_info, item_data in list(st.session_state.new_cart.items()):
        qty = item_data["qty"]
        item_price = item_data["price"]
        total += item_price * qty
        st.write(f"▪️ **{food_info}** ({CURRENCY} {item_price:.2f} x {qty})")
        if st.button("➖ Kurang", key=f"m_{food_info}_app"):
            st.session_state.new_cart[food_info]["qty"] -= 1
            if st.session_state.new_cart[food_info]["qty"] <= 0: del st.session_state.new_cart[food_info]
            st.rerun()
        if st.button("➕ Tambah", key=f"p_{food_info}_app"):
            st.session_state.new_cart[food_info]["qty"] += 1
            st.rerun()

st.write("---")
order_note = st.text_input("📝 Nota Pesanan (cth: nak garing lebih)")
coupon = st.text_input(" Masukkan Kod Kupon")
final_total = total * 0.9 if coupon == "VIP90" else total
st.markdown(f"###  Jumlah Keseluruhan: **{CURRENCY} {final_total:.2f}**")
st.write("---")

pay_method = st.radio(" Sila pilih kaedah pembayaran:", ["DuitNow (Pindahan Dalam Talian)", "Bayar Tunai Semasa Ambil / Makan"], index=None)

if pay_method and "DuitNow" in pay_method:
    p_text = "Saya bayar melalui DuitNow."
    st.markdown(f'<div style="background-color: #FEF2F2; padding: 15px; border-radius: 12px; color: #111827; border: 1px solid #FCA5A5;"><h4> Arahan Pembayaran DuitNow</h4><p>Sila buat pindahan tunai jumlah keseluruhan ke akaun bos:</p><p style="font-size: 18px; font-weight: bold; color: #DC2626;"> No. DuitNow: 016-2002352</p></div>', unsafe_allow_html=True)

if pay_method and "Tunai" in pay_method:
    p_text = "Saya bayar tunai di kedai."
    st.info("💡 **Nota Pembayaran:** Sila buat pembayaran tunai di kaunter semasa mengambil makanan / makan di kedai.")

if pay_method is None: st.error(" 💳 Sila pilih kaedah pembayaran anda!")

# ==========================================
# WhatsApp Button 
# ==========================================
st.write("---")
items_summary = "\\n".join([f"{i+1}. {k} x{v['qty']}" for i, (k, v) in enumerate(st.session_state.new_cart.items())])
loc = f"No Meja: {table_number}" if dining_type and "Makan Di Sini" in dining_type else (f"Alamat: {delivery_address}" if dining_type and "Delivery" in dining_type else "Takeaway")

whatsapp_message = f"PESANAN BARU ALIS FRIED CHICKEN\n-------------------\nID Pesanan: {st.session_state.order_id}\nCara Makan: {dining_type}\nLokasi: {loc}\n-------------------\nPerincian:\n{items_summary}\n-------------------\nNota: {order_note}\nPembayaran: {pay_method}\nJumlah: {CURRENCY} {final_total:.2f}"

# 🌟 這兩行你最看重的功能代碼，已經用最安全的縮排格式完美嵌入！
encoded_message = urllib.parse.quote(whatsapp_message)
whatsapp_url = f"https://wa.me{MY_PHONE_NUMBER}?text={encoded_message}"

if not st.session_state.new_cart:
    st.warning(" 🛒 Sila tambah makanan ke dalam troli terlebih dahulu!")
    whatsapp_url = "https://wa.me/60162002352"

# 🌟 官方認證大綠色下單按鈕，100% 絕對雷打不動、永久置底現身！
st.link_button("🟢 SAHKAN PESANAN & HANTAR KE WHATSAPP 🟢", whatsapp_url, use_container_width=True)
