請幫我將目前的 app.py 程式碼進行大改造，替換成全新的「ALIS FRIED CHICKEN」炸雞點餐系統！請嚴格按照以下規則重寫：

1. 更新菜單資料與基礎價格（CURRENCY 保持 "RM"）：
   - Ayam Gunting (炸雞排)：基礎價格 RM 10.00
   - Sosej Jumbo (巨無霸香腸)：基礎價格 RM 6.00
   - Sotong (炸魷魚)：基礎價格 RM 14.00
   - Chicken Popcorn (7pcs) (爆米花雞)：基礎價格 RM 5.00
   - Ayam Tender (雞柳)：基礎價格 RM 3.00
   - Satay Ayam (沙爹雞肉串)：基礎價格 RM 3.00

2. 為每道餐點設計客製化選項與加價邏輯（請使用 st.selectbox）：
   - Ayam Gunting：
     * 選擇份量：Saiz Normal (RM 10.00)、Saiz Besar (+RM 3.00)
     * 選擇辣度：不辣、微辣、大辣
   - Sosej Jumbo：
     * 選擇醬料：辣椒醬、番茄醬、美乃滋、不需要醬料
   - Sotong：
     * 選擇辣度：不辣、辣椒粉、招牌胡椒鹽
   - Chicken Popcorn：
     * 選擇口味：原味、椒鹽味、起司粉 (+RM 1.00)
   - Ayam Tender：
     * 選擇數量：1pcs (RM 3.00)、3pcs (+RM 5.00，總共8)、5pcs (+RM 8.00，總共11)
   - Satay Ayam：
     * 選擇數量：1串 (RM 3.00)、5串 (+RM 12.00)、10串 (+RM 24.00)

3. 網頁基本設定調整：
   - 網頁大標題改為：「🍗 ALIS FRIED CHICKEN 網頁點餐系統」
   - 老闆電話 MY_PHONE_NUMBER 改為："60162002352"（根據菜單上的 016-200 2352）
   - CSS 樣式保持原有的明亮黃與深灰色調。

4. 徹底修復與補全結帳及 WhatsApp 跳轉邏輯：
   - 補全末尾斷掉的代碼，當用戶選擇「DuitNow 線上轉賬」時，完成 payment_closing_text 變數，並顯示轉賬號碼 016-200 2352。
   - 用戶選擇「到店支付現金」時，設定對應的 payment_closing_text。
   - 在購物車最下方添加一個藍色或醒目的「🟢 確認下單並發送 WhatsApp」按鈕。
   - 點擊按鈕時，將訂單單號、用餐方式（桌號/外送地址）、點餐明細（品項、客製化選項、數量、總價）、備註、總金額、付款方式全部整合，使用 urllib.parse.quote() 進行網址編碼。
   - 最後使用 st.link_button() 引導顧客跳轉至 https://wa.me... 發送訂單。

請給我修改後完整且無錯誤的 app.py 程式碼。
