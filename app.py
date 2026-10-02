# -*- coding: utf-8 -*-
import streamlit as st
import urllib.parse
import random
import os
from datetime import datetime

# 1. Halaman & Visual CSS - Reka Bentuk Telefon App
st.set_page_config(page_title="Sistem Pesanan Makanan ALIS FRIED CHICKEN", page_icon="🍗", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #111827; color: #F9FAFB !important; }
    h1, h2, h3 { color: #FBBF24 !important; font-weight: 800 !important; }
    [data-testid="stContainer"] {
        background-color: #1F2937 !important; border-radius: 16px !important; padding: 15px !important;
        border: 1px solid #374151 !important; margin-bottom: 12px !important;
    }
    .stSelectbox label p { color: #9CA3AF !important; }
    [data-testid="stContainer"] button {
        background-color: #FBBF24 !important; color: #111827 !important; font-weight: bold !important;
        border-radius: 20px !important; border: none !important; width: 100% !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🍔 Tajuk Utama
# ==========================================
st.title("🍗 ALIS FRIED CHICKEN")
st.write("Made fresh everyday • Sajian panas dan ranggup setiap hari!")
st.write("---")

dining_type = st.radio("🥡 Sila pilih cara makan anda:", ["Makan Di Sini", "Bungkus (Takeaway)", "Penghantaran (Delivery)"], horizontal=True, index=None)
st.write("---")

menu_data = {
    "Ayam Gunting": {"price": 10.00, "img": "ayam_gunting.jpg", "desc": "Ayam gunting ranggup bersaiz besar dengan rempah istimewa."},
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
pay_method = None
p_text = ""
final_total = 0.0

tab1, tab2 = st.tabs(["🔥 Popular", "🍗 Semua Menu (Semua)"])

def paparkan_menu(senarai_makanan):
    is_menu_disabled = True if dining_type is None else False
    if dining_type is None:
        st.error("⚠️ Sila pilih 'cara makan' anda di bahagian atas terlebih dahulu sebelum memesan!")
        
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
                    st.markdown(f'<div style="background-color: #374151; width: 100%; aspect-ratio: 1; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #9CA3AF;">📷 {food}</div>', unsafe_allow_html=True)
            
            with info_col:
                st.markdown(f"### {food}")
                st.markdown(f"<small style='color: #9CA3AF;'>{desc_text}</small>", unsafe_allow_html=True)
                
                if "Ayam Gunting" in food:
                    size = st.selectbox("Saiz", ["Saiz Normal (RM 10.00)", "Saiz Besar (+RM 3.00)"], key=f"{food}_sz")
                    flavor = st.selectbox("Perisa", ["Original", "Pedas"], key=f"{food}_flv")
                    actual_price = price + 3.00 if "Saiz Besar" in size else price
                    full_food_name = f"{food} ({size}/{flavor})"
                elif "Ayam Tender" in food:
                    qty_opt = st.selectbox("Kuantiti", ["1pcs (RM 3.00)", "3pcs (RM 8.00)", "5pcs (RM 11.00)"], key=f"{food}_qt")
                    flavor = st.selectbox("Perisa", ["Original", "Pedas"], key=f"{food}_flv")
                    actual_price = 8.00 if "3pcs" in qty_opt else (11.00 if "5pcs" in qty_opt else 3.00)
                    full_food_name = f"{food} ({qty_opt}/{flavor})"
                else:
                    flavor = st.selectbox("Perisa", ["Original", "Pedas"], key=f"{food}_flv")
                    actual_price = price
                    full_food_name = f"{food} ({flavor})"
                
                st.markdown(f"**{CURRENCY} {actual_price:.2f}**")
                if st.button(f"➕ Tambah", key=f"btn_{food}_tab", disabled=is_menu_disabled):
                    if full_food_name in st.session_state.new_cart:
                        st.session_state.new_cart[full_food_name]["qty"] += 1
                    else:
                        st.session_state.new_cart[full_food_name] = {"qty": 1, "price": actual_price}
                    st.toast("Telah ditambah ke troli!")
                    st.rerun()

with tab1: paparkan_menu(["Ayam Gunting", "Sotong", "Chicken Popcorn (7pcs)"])
with tab2: paparkan_menu(list(menu_data.keys()))

# ==========================================
# 🛒 Bahagian Troli & Pesanan Anda
# ==========================================
st.write("---")
st.header("🛒 Troli & Pesanan Anda")

if dining_type:
    if "Delivery" in dining_type or "Penghantaran" in dining_type:
        delivery_address = st.text_input("🏠 Masukkan Alamat Penghantaran Lengkap (Delivery Address):")
        st.info("💡 **Nota Penghantaran:** Sila ambil perhatian, caj penghantaran akan dibayar secara berasingan kepada penghantar (runner) semasa menerima makanan.")
        if not delivery_address.strip():
            is_address_missing = True
            st.error("⚠️ Sila masukkan alamat penghantaran anda terlebih dahulu!")
    elif "Makan Di Sini" in dining_type:
        table_number = st.text_input("🔢 Masukkan Nombor Meja Anda (Table Number):")

if not st.session_state.new_cart:
    st.info("Troli anda masih kosong. Sila klik butang ➕ Tambah pada menu di atas untuk mula memesan.")
else:
    total = 0
    for food_info, item_data in list(st.session_state.new_cart.items()):
        qty = item_data["qty"]
        item_price = item_data["price"]
        total += item_price * qty
        
        cart_col1, cart_col2 = st.columns(2)
        with cart_col1: st.write(f"▪️ **{food_info}** \n({CURRENCY} {item_price:.2f} x {qty})")
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
    order_note = st.text_input("📝 Nota Pesanan (cth: nak garing lebih, pedas lebih)")
    coupon = st.text_input("🏷️ Masukkan Kod Kupon")
    final_total = total * 0.9 if coupon == "VIP90" else total
    if coupon == "VIP90": st.info(f"🎉 Diskaun 10% berjaya digunakan! Dijimatkan {CURRENCY} {total*0.1:.2f}")
        
    st.markdown(f"### 💰 Jumlah Keseluruhan: **{CURRENCY} {final_total:.2f}**")
    st.write("---")
    
    pay_method = st.radio("💳 Sila pilih kaedah pembayaran:", ["DuitNow (Pindahan Dalam Talian)", "Bayar Tunai Semasa Ambil / Makan"], index=None)
    if pay_method == "DuitNow (Pindahan Dalam Talian)":
        st.markdown(f'<div style="background-color: #1F2937; padding: 15px; border-radius: 12px; color: #FFFFFF; border: 1px solid #FBBF24;"><h4> Arahan Pembayaran DuitNow</h4><p>Sila buat pindahan tunai jumlah keseluruhan ke akaun bos:</p><p style="font-size: 18px; font-weight: bold; color: #FBBF24;"> No. DuitNow: 016-2002352</p></div>', unsafe_allow_html=True)
        p_text = "Saya telah buat pembayaran melalui DuitNow. Resit akan dihantar sekejap lagi."
    elif pay_method == "Bayar Tunai Semasa Ambil / Makan":
        st.info("💡 Nota: Sila buat pembayaran tunai di kaunter semasa mengambil makanan / makan di kedai.")
        p_text = "Saya memilih untuk bayar tunai di kedai."
    else:
        is_payment_missing = True
        st.error("⚠️ Sila pilih kaedah pembayaran anda!")

    # ==========================================
    # 🌟 WhatsApp Button 安全單行重寫區域
    # ==========================================
    st.write("---")
    items_summary = ""
    for idx, (f_info, i_data) in enumerate(st.session_state.new_cart.items(), 1):
        items_summary += f"{idx}. {f_info} x{i_data['qty']} | "
        
    loc = f"No Meja: {table_number}" if dining_type and "Makan Di Sini" in dining_type else (f"Alamat: {delivery_address}" if dining_type and "Delivery" in dining_type else "Takeaway")
    
    # 🌟 改為完全安全的單行字串，100% 杜絕括號不閉合的錯誤 Bug！
    whatsapp_message = f"PESANAN BARU ALIS FRIED CHICKEN\\n-------------------\\nID Pesanan: {st.session_state.order_id}\\nCara Makan: {dining_type}\\nLokasi: {loc}\\n-------------------\\nPerincian: {items_summary}\\n-------------------\\nNota: {order_note if order_note else 'Tiada'}\\nPembayaran: {pay_method if pay_method else 'Belum Pilih'}\\nJumlah: {CURRENCY} {final_total:.2f}\\nMesej: {p_text}"
    
    whatsapp_url = f"https://wa.me/{MY_PHONE_NUMBER}?text={urllib.parse.quote(whatsapp_message)}"
    is_btn_disabled = is_address_missing or is_payment_missing
