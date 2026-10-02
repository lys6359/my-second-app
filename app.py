# 初始狀態設為 False（假設沒有漏填）
is_address_missing = False 

if dining_type:
    if dining_type in ["Bungkus (Takeaway)", "Penghantaran (Delivery)"]:
        delivery_address = st.text_input("🏠 Masukkan Alamat Lengkap Sila (Address Required):")
        
        # 🚨 關鍵防呆：如果顧客選擇了 Delivery，但輸入框是空的（或只有空格）
        if not delivery_address.strip():
            is_address_missing = True  # 標記為「漏填地址」
            st.markdown("<p style='color:red; font-weight:bold;'>⚠️ Sila masukkan alamat anda terlebih dahulu!</p>", unsafe_allow_html=True)

# ... 中間計算購物車金額 ...

# 🛒 只有在「沒有漏填地址」的情況下，is_ready_to_order 才會是 True
is_ready_to_order = not is_address_missing and dining_type is not None

if is_ready_to_order:
    # 🟢 顧客有填地址，才會渲染並顯示漂亮的 WhatsApp 按鈕
    st.link_button("🟢 Hantar Pesanan via WhatsApp", whatsapp_url)
else:
    # 🔒 如果沒填地址，按鈕會被隱藏，並顯示警告字句
    st.warning("🔒 Sila lengkapkan maklumat Cara Makan dan Alamat/Meja di atas untuk mengaktifkan butang pesanan.")
