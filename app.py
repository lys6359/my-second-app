# -*- coding: utf-8 -*-
import streamlit as st
import urllib.parse
import random
from datetime import datetime, timedelta, timezone

# ==========================================
# ⚙️ KONFIGURASI KEDAI (PENGURUSAN KEDAI AUTOMATIK)
# ==========================================
# 1. Tetapkan zon masa Malaysia (GMT+8)
MY_TZ = timezone(timedelta(hours=8))
now_in_my = datetime.now(MY_TZ)
current_hour = now_in_my.hour
current_minute = now_in_my.minute

# 2. Tukar masa sekarang & waktu operasi kepada jumlah minit
# 11:00 AM Bisnes Mula = 11 * 60 + 0 = 660 minit
# 07:30 PM Bisnes Tamat = 19 * 60 + 30 = 1170 minit
current_total_minutes = (current_hour * 60) + current_minute
OPEN_TIME_MINUTES = (11 * 60) + 0     # 11:00 AM
CLOSE_TIME_MINUTES = (21 * 60) + 8   # 07:30 PM (19:30)

# 3. Logik Semakan Masa Automatik (Menggunakan jumlah minit)
if OPEN_TIME_MINUTES <= current_total_minutes < CLOSE_TIME_MINUTES:
    IS_SHOP_OPEN = True
else:
    IS_SHOP_OPEN = False

# 1. Konfigurasi Halaman & CSS Style (Mengekalkan warna premium kedai)
st.set_page_config(page_title="Sistem Pesanan Makanan ALIS FRIED CHICKEN", page_icon="🍗", layout="wide")


# ==========================================
# Tajuk Utama
# ==========================================
st.title("🍗 Sistem Pesanan Makanan ALIS FRIED CHICKEN")

# ==========================================
# 🛑 SEMAKAN STATUS KEDAI (LOGIK TUTUP/BUKA KEDAI)
# ==========================================
if not IS_SHOP_OPEN:
    st.markdown("---")
    st.markdown("""
        <div style="background-color: #1F2937; padding: 40px; border-radius: 20px; text-align: center; color: #FFFFFF; border: 4px solid #EF4444;">
            <h1 style="color: #EF4444 !important; font-size: 40px; margin-bottom: 10px;">🛑 MAAF, KEDAI KAMI SUDAH TUTUP</h1>
            <p style="font-size: 18px; color: #F3F4F6;">Terima kasih atas sokongan anda! Kami telah menutup pesanan dalam talian buat masa ini.</p>
            <p style="font-size: 16px; color: #FBBF24; font-weight: bold; margin-top: 15px;">🕒 Waktu Operasi: 11:00 AM - 10:00 PM</p>
            <p style="font-size: 14px; color: #9CA3AF; margin-top: 5px;">Sila kunjungi kami lagi esok hari atau hubungi kami terus untuk sebarang pertanyaan.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    whatsapp_tanya_url = f"https://wa.me"
    st.link_button("💬 Hubungi Bos Melalui WhatsApp", whatsapp_tanya_url)
    st.stop()

# ==========================================
# 🛒 JIKA KEDAI BUKA, TERUSKAN DI BAWAH
# ==========================================
st.write("Selamat datang! Sila pilih hidangan anda di bawah. Selepas selesai, klik butang WhatsApp di bawah untuk hantar pesanan kepada bos!")
st.write("---")

dining_type = st.radio("🥡 Sila pilih cara makan anda:", ["Makan Di Sini", "Bungkus (Takeaway)", "Penghantaran (Delivery)"], horizontal=True, index=None)

# Menu makanan dan gambar
menu = {
    "Ayam Gunting": {"price": 10.00, "image": "images/ayam_gunting.jpg"},
    "Sosej Jumbo": {"price": 6.00, "image": "images/sosej_jumbo.jpg"},
    "Sotong": {"price": 14.00, "image": "images/sotong.jpg"},
    "Chicken Popcorn (7pcs)": {"price": 5.00, "image": "images/popcorn.jpg"},
    "Ayam Tender": {"price": 3.00, "image": "images/tender.jpg"},
    "Satay Ayam": {"price": 3.00, "image": "images/satay.jpg"}
}

CURRENCY = "RM"
MY_PHONE_NUMBER = "60162002352"

if "new_cart" not in st.session_state:
    st.session_state.new_cart = {}

if "order_id" not in st.session_state:
    st.session_state.order_id = f"EP-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"

delivery_address = ""
table_number = ""

col1, col2 = st.columns(2)

with col1:
    st.subheader("【 🍱 Menu Hari Ini 】")
    is_menu_disabled = True if dining_type is None else False
    if dining_type is None:
        st.error("⚠️ Sila pilih 'cara makan' anda di bahagian atas terlebih dahulu!")

    for food, info in menu.items():
        price = info["price"]
        img_path = info["image"]
        
        with st.container():
            img_col, details_col = st.columns([1, 1.3])
            
            with img_col:
                try:
                    st.image(img_path, use_container_width=True)
                except Exception:
                    st.info("🖼️ Gambar belum dimuatkan")
                
            with details_col:
                st.markdown(f"### {food}")
                if "Ayam Gunting" in food:
                    size = st.selectbox("📐 Pilih Saiz", ["Saiz Normal (RM 10.00)", "Saiz Besar (+RM 3.00)"], key="gunting_size")
                    flavor = st.selectbox("🌶️ Pilih Perisa", ["Original", "Pedas"], key="gunting_flavor")
                    actual_price = price + 3.00 if "Saiz Besar" in size else price
                    full_food_name = f"{food} ({size}/{flavor})"
                elif "Ayam Tender" in food:
                    qty_opt = st.selectbox("🔢 Pilih Kuantiti", ["1pcs (RM 3.00)", "3pcs (RM 8.00)", "5pcs (RM 11.00)"], key="tender_qty")
                    flavor = st.selectbox("🌶️ Pilih Perisa", ["Original", "Pedas"], key="tender_flavor")
                    actual_price = 8.00 if "3pcs" in qty_opt else (11.00 if "5pcs" in qty_opt else 3.00)
                    full_food_name = f"{food} ({qty_opt}/{flavor})"
                else:
                    flavor = st.selectbox("🌶️ Pilih Perisa", ["Original", "Pedas"], key=f"{food}_flavor")
                    actual_price = price
                    full_food_name = f"{food} ({flavor})"
                
                st.markdown(f"💰 Harga: **{CURRENCY} {actual_price:.2f}**")
                if st.button(f"➕ Tambah {food}", key=f"btn_{food}", disabled=is_menu_disabled):
                    st.session_state.new_cart[full_food_name] = st.session_state.new_cart.get(full_food_name, {"qty": 0, "price": actual_price})
                    st.session_state.new_cart[full_food_name]["qty"] += 1
                    st.toast("Telah ditambah ke troli!")
                    st.rerun()

with col2:
    st.subheader("【 🛒 Troli Anda 】")
    st.markdown(f"✨ Pilihan: **{dining_type if dining_type else 'Belum Pilih'}** | 🔢 ID Pesanan: **{st.session_state.order_id}**") 
    
    if dining_type:
        if "Delivery" in dining_type or "Penghantaran" in dining_type:
            delivery_address = st.text_input("🏠 Masukkan Alamat Penghantaran Lengkap (Delivery Address):")
            st.info("💡 **Nota Penghantaran:** Sila ambil perhatian, caj penghantaran akan dibayar secara berasingan kepada penghantar (runner) semasa menerima makanan.")
        elif "Makan Di Sini" in dining_type:
            table_number = st.text_input("🔢 Masukkan Nombor Meja Anda (Table Number):")
        
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
        order_note = st.text_input("📝 Nota Pesanan (cth: nak garing lebih)")
        coupon = st.text_input("🏷️ Masukkan Kod Kupon")
        final_total = total * 0.9 if coupon == "VIP90" else total
        if coupon == "VIP90": st.info(f"🎉 Diskaun 10% berjaya digunakan! Dijimatkan {CURRENCY} {total*0.1:.2f}")
            
        st.markdown(f"### 💰 Jumlah Keseluruhan: **{CURRENCY} {final_total:.2f}**")
        st.write("---")
        
        pay_method = st.radio("💳 Sila pilih kaedah pembayaran:", ["DuitNow (Pindahan Dalam Talian)", "Bayar Tunai Semasa Ambil / Makan"], index=None)
        p_text = ""
        
        if pay_method == "DuitNow (Pindahan Dalam Talian)":
            st.markdown(f'<div style="background-color: #1F2937; padding: 15px; border-radius: 12px; color: #FFFFFF;"><h4> Arahan Pembayaran DuitNow</h4><p>Sila buat pindahan tunai jumlah keseluruhan ke akaun bos:</p><p style="font-size: 18px; font-weight: bold; color: #FBBF24;"> No. DuitNow: 016-2002352</p></div>', unsafe_allow_html=True)
            p_text = "Saya telah buat pembayaran melalui DuitNow. Resit akan dihantar sekejap lagi."
        elif pay_method == "Bayar Tunai Semasa Ambil / Makan":
            st.info("💡 Nota: Sila buat pembayaran tunai di kaunter semasa mengambil makanan / makan di kedai.")
            p_text = "Saya memilih untuk bayar tunai di kedai."

        st.write("---")
        items_summary = ""
        for idx, (f_info, i_data) in enumerate(st.session_state.new_cart.items(), 1):
            items_summary += f"{idx}. {f_info} x{i_data['qty']}\n"
            
        loc = f"No Meja: {table_number}" if dining_type and "Makan Di Sini" in dining_type else (f"Alamat: {delivery_address}" if dining_type and "Delivery" in dining_type else "Takeaway")
        
        whatsapp_message = (
            f"🔔 *PESANAN BARU - ALIS FRIED CHICKEN*\n\n"
            f"🆔 *ID Pesanan:* {st.session_state.order_id}\n"
            f"🥡 *Jenis Hidangan:* {dining_type}\n"
            f"📍 *Maklumat Lokasi:* {loc}\n\n"
            f"📋 *Item Pesanan:*\n{items_summary}\n"
            f"📝 *Nota:* {order_note if order_note else 'Tiada'}\n"
            f"🏷️ *Kupon:* {coupon if coupon else 'Tiada'}\n"
            f"💳 *Kaedah Bayar:* {pay_method if pay_method else 'Belum dipilih'}\n"
            f"💬 *Status:* {p_text}\n\n"
            f"💰 *JUMLAH BESAR:* {CURRENCY} {final_total:.2f}\n\n"
            f"Sila sahkan pesanan saya, terima kasih! 🙏"
        ) # <-- 就是這個右括號，舊代碼漏掉了它

        encoded_message = urllib.parse.quote(whatsapp_message)
        whatsapp_url = f"https://wa.me/{MY_PHONE_NUMBER}?text={encoded_message}"
        
        # 精準狀態檢查
        is_address_ok = False if (dining_type and ("Delivery" in dining_type or "Penghantaran" in dining_type) and not delivery_address.strip()) else True
        is_payment_ok = True if pay_method is not None else False
        
        # 💡 原生無干擾按鈕控制：這一次絕對會原汁原味地顯示在畫面上！
        if is_address_ok and is_payment_ok:
            st.success("✅ Semua maklumat lengkap! Klik butang di bawah untuk menghantar pesanan.")
            st.link_button("💬 Hantar Pesanan Ke WhatsApp (Klik Sini)", whatsapp_url, key="btn_wa_enabled")
        else:
            missing_reasons = []
            if not is_address_ok: missing_reasons.append("alamat penghantaran")
            if not is_payment_ok: missing_reasons.append("kaedah pembayaran")
            reasons_text = " dan ".join(missing_reasons)
