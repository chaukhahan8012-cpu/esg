import streamlit as st
import pandas as pd
import qrcode
import io
from PIL import Image

# Cấu hình giao diện
st.set_page_config(page_title="AgriLoop Traceability", layout="centered")

st.title("🛡️ AgriLoop: Hệ Thống Truy Xuất Nguồn Gốc")
st.markdown("---")

# Phần 1: Tạo mã định danh cho lô hàng
st.subheader("1. Khởi tạo 'Hộ chiếu số' cho lô hàng")
col1, col2 = st.columns([2, 1])

with col1:
    batch_id = st.text_input("Nhập mã lô hàng (Batch ID):", "AL-HUB-2026-001")
    farm_name = st.selectbox("Nguồn gốc trang trại:", ["Trang trại Hân (Lâm Đồng)", "Hợp tác xã An (Long An)", "Farm Bình (Tiền Giang)"])
    product_type = st.text_input("Loại phế phẩm:", "Vỏ trấu chất lượng cao")

with col2:
    if st.button("Tạo Mã QR"):
        # Dữ liệu mã hóa trong QR
        qr_content = f"ID: {batch_id}\nFarm: {farm_name}\nType: {product_type}\nVerified by AgriLoop"
        qr = qrcode.make(qr_content)
        
        # Chuyển đổi để hiển thị
        img_buf = io.BytesIO()
        qr.save(img_buf, format="PNG")
        st.image(img_buf, caption="Mã QR định danh", width=200)

st.markdown("---")

# Phần 2: Giả lập Quét mã và Hiện kết quả
st.subheader("2. Kết quả truy xuất khi khách hàng quét mã")

# Giả lập database lịch sử lô hàng
trace_data = {
    "AL-HUB-2026-001": [
        {"Thời gian": "17/04/2026 08:00", "Sự kiện": "Thu gom & Kiểm định tại nguồn", "Trạng thái": "✅ Đạt chuẩn A"},
        {"Thời gian": "17/04/2026 13:00", "Sự kiện": "Đóng gói & Ghép chuyến vận chuyển", "Trạng thái": "🚚 Đang vận chuyển"},
        {"Thời gian": "17/04/2026 17:00", "Sự kiện": "Giao hàng thành công tại Nhà máy X", "Trạng thái": "🏁 Hoàn thành"}
    ]
}

search_id = st.text_input("Quét mã QR hoặc Nhập mã để tra cứu:", "AL-HUB-2026-001")

if search_id in trace_data:
    st.success(f"Tìm thấy thông tin lô hàng: {search_id}")
    df_history = pd.DataFrame(trace_data[search_id])
    st.table(df_history)
    
    # Thêm biểu đồ tiến trình cho Pro
    st.info("💡 Lô hàng này đã giúp giảm 2.5kg khí thải CO2 ra môi trường.")
else:
    st.error("Không tìm thấy dữ liệu cho mã này.")
