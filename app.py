import streamlit as st
import urllib.parse
import random
from datetime import datetime

# 1. Konfigurasi Halaman (簡化基本設定)
st.set_page_config(page_title="ALIS FRIED CHICKEN", page_icon="🍗", layout="wide")

# 2. Tajuk Utama
st.title("🍗 Sistem Pesanan Makanan ALIS FRIED CHICKEN")
st.write("Sila pilih hidangan anda. Selepas selesai, klik pautan WhatsApp di bawah untuk hantar pesanan!")
st.write("---")

dining_type = st.radio("Pilih cara makan anda:", ["Makan Di Sini", "Bungkus (Takeaway)", "Penghantaran (Delivery)"], horizontal=True, index=None)

menu = {
    "Ayam Gunting": 10.00,
    "Sosej Jumbo": 6.00,
    "Sotong": 14.00,
    "Chicken Popcorn (7pcs)": 5.00,
    "Ayam Tender": 3.00,
    "Satay Ayam": 3.00
}

CURRENCY = "RM"
MY_PHONE_NUMBER = "60162002352"

if "new_cart" not in st.session_state:
    st.session_state.new_cart = {}

if "order_id" not in st.session_state:
    st.session_state.order_id = f"ALIS-{random.randint(1000, 9999)}"

col1, col2 = st.columns(2)

with col1:
    st.subheader("【 Menu Hari Ini 】")
    is_menu_disabled = True if dining_type is None else False
    if dining_type is None:
        st.error("⚠️ Sila pilih 'cara makan' anda di atas terlebih dahulu!")

    for food, price in menu.items():
        with st.container():
            st.markdown(f"### {food}")
            if "Ayam Gunting" in food:
                size = st.selectbox("Saiz", ["Saiz Normal (RM 10.00)", "Saiz Besar (+RM 3.00)"], key="gunting_size")
                spicy = st.selectbox("Kepedasan", ["Kurang Pedas", "Pedas Biasa", "Sangat Pedas"], key="gunting_spicy")
                actual_price = price + 3.00 if "Saiz Besar" in size else price
                full_food_name = f"{food} ({size}/{spicy})"
            elif "Sosej Jumbo" in food:
                sauce = st.selectbox("Sos", ["Sos Cili", "Sos Tomato", "Mayonis", "Tanpa Sos"], key="sosej_sauce")
                actual_price = price
                full_food_name = f"{food} ({sauce})"
            elif "Sotong" in food:
                spicy = st.selectbox("Perisa", ["Original", "Serbuk Cili", "Serbuk Lada Hitam"], key="sotong_spicy")
                actual_price = price
                full_food_name = f"{food} ({spicy})"
            elif "Chicken Popcorn" in food:
                flavor = st.selectbox("Perisa", ["Original", "Serbuk Keju (+RM 1.00)"], key="popcorn_flavor")
                actual_price = price + 1.00 if "Keju" in flavor else price
                full_food_name = f"{food} ({flavor})"
            elif "Ayam Tender" in food:
                qty_opt = st.selectbox("Kuantiti", ["1pcs (RM 3.00)", "3pcs (RM 8.00)", "5pcs (RM 11.00)"], key="tender_qty")
                actual_price = 8.00 if "3pcs" in qty_opt else (11.00 if "5pcs" in qty_opt else 3.00)
                full_food_name = f"{food} ({qty_opt})"
            else:
                satay_opt = st.selectbox("Kuantiti", ["1 Cucuk (RM 3.00)", "5 Cucuk (RM 15.00)", "10 Cucuk (RM 30.00)"], key="satay_qty")
                actual_price = 15.00 if "5 Cucuk" in satay_opt else (30.00 if "10 Cucuk" in satay_opt else 3.00)
                full_food_name = f"{food} ({satay_opt})"
            
            st.write(f"Harga: {CURRENCY} {actual_price:.2f}")
            if st.button(f"➕ Tambah {food}", key=f"btn_{food}", disabled=is_menu_disabled):
                if full_food_name in st.session_state.new_cart:
                    st.session_state.new_cart[full_food_name]["qty"] += 1
                else:
                    st.session_state.new_cart[full_food_name] = {"qty": 1, "price": actual_price}
                st.toast("Ditambah ke troli!")
                st.rerun()

with col2:
    st.subheader("【 Troli Anda 】")
    st.write(f"Cara Makan: {dining_type if dining_type else 'Belum Pilih'} | ID: {st.session_state.order_id}")
    
    delivery_address = st.text_input("Alamat Penghantaran Lengkap:") if dining_type == "Penghantaran (Delivery)" else ""
    table_number = st.text_input("Nombor Meja Anda:") if dining_type == "Makan Di Sini" else ""
        
    if not st.session_state.new_cart:
        st.write("Troli kosong. Sila tambah makanan dari menu.")
    else:
        total = 0
        st.write("---")
        for food_info, item_data in list(st.session_state.new_cart.items()):
            qty = item_data["qty"]
            item_price = item_data["price"]
            total += item_price * qty
            
            c1, c2, c3 = st.columns(3)
            with c1: st.write(f"- {food_info} (x{qty})")
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
        order_note = st.text_input("Nota Pesanan (cth: nak pedas lebih)")
        coupon = st.text_input("Kod Kupon")
        final_total = total * 0.9 if coupon == "VIP90" else total
            
        st.markdown(f"### Jumlah: **{CURRENCY} {final_total:.2f}**")
        st.write("---")
        
        pay_method = st.radio("Kaedah Pembayaran:", ["DuitNow", "Tunai Di Kedai"])
        p_text = "Saya telah bayar melalui DuitNow." if pay_method == "DuitNow" else "Saya akan bayar tunai."
        if pay_method == "DuitNow":
            st.info("📞 No. DuitNow Bos: 016-2002352")
            
        st.write("---")
        
        items_summary = ""
        for idx, (f_info, i_data) in enumerate(st.session_state.new_cart.items(), 1):
            items_summary += f"{idx}. {f_info} x{i_data['qty']}\n"
            
        loc = f"No Meja: {table_number}" if dining_type == "Makan Di Sini" else (f"Alamat: {delivery_address}" if dining_type == "Penghantaran (Delivery)" else "Takeaway")
        
        # 🌟 採用保證絕不報錯、100% 支援所有裝置的純文字訊息格式，杜絕任何問號方塊
        whatsapp_message = (
            f"* PESANAN BARU ALIS FRIED CHICKEN *\n"
            f"-----------------------------------\n"
            f"ID Pesanan: {st.session_state.order_id}\n"
            f"Cara Makan: {dining_type}\n"
            f"Lokasi: {loc}\n"
            f"-----------------------------------\n"
            f"明細 Perincian:\n{items_summary}"
            f"-----------------------------------\n"
            f"Nota: {order_note if order_note else 'Tiada'}\n"
            f"Pembayaran: {pay_method}\n"
            f"Jumlah: {CURRENCY} {final_total:.2f}\n"
            f"-----------------------------------\n"
            f"Mesej: {p_text}"
        )
        
        encoded_message = urllib.parse.quote(whatsapp_message)
        whatsapp_url = f"https://wa.me/{MY_PHONE_NUMBER}?text={encoded_message}"
        
        # 🌟 終極大絕招：直接用 Streamlit 絕對不會出錯、最安全的純文字大超連結連結！
        st.markdown(f"### 🔗 [👉 KLIK DI SINI UNTUK HANTAR PESANAN KE WHATSAPP]({whatsapp_url})")
