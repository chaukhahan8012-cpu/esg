import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
import time
import qrcode
import io
from PIL import Image

# 1. Cấu hình giao diện
st.set_page_config(page_title="AgriLoop - MIS Solution", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f9fbfd; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #28a745; color: white; }
    </style>
    """, unsafe_allow_html=True)

# SIDEBAR
st.sidebar.title("🌿 AgriLoop Hub")
st.sidebar.info("Hệ thống quản trị phế phẩm nông nghiệp thông minh")
menu = st.sidebar.radio("CHỨNG MINH GIẢI PHÁP:", 
    ["Sơ đồ vận hành", "Kết nối Cung - Cầu", "Tối ưu Vận chuyển", "Truy xuất nguồn gốc"])

# --- TAB 1: SƠ ĐỒ VẬN HÀNH ---
if menu == "Sơ đồ vận hành":
    st.header("🧠 1. Luồng vận hành hệ thống (Workflow)")
    st.graphviz_chart('''
        digraph {
            rankdir=LR;
            node [shape=box, style=filled, color="#E1F5FE", fontname="Arial"];
            N [label="Nông dân", fillcolor="#C8E6C9"];
            A [label="Hệ thống AgriLoop", fillcolor="#BBDEFB"];
            T [label="Đội ngũ Tài xế", fillcolor="#FFF9C4"];
            M [label="Nhà máy tiêu thụ", fillcolor="#FFCCBC"];
            N -> A [label="Gửi Data"];
            A -> T [label="Lệnh ghép chuyến"];
            T -> M [label="Giao hàng"];
            M -> A [label="Xác thực", style=dotted];
        }
    ''')
    st.write("> **Giá trị:** Tự động hóa quy trình, loại bỏ các bước trung gian thủ công.")

# --- TAB 2: KẾT NỐI CUNG - CẦU ---
elif menu == "Kết nối Cung - Cầu":
    st.header("🤝 2. Thuật toán Khớp lệnh & Pooling")
    c1, c2 = st.columns(2)
    with c1:
        st.write("**📦 Nguồn cung (Nông dân)**")
        df_f = pd.DataFrame({'Tên': ['Hân', 'An', 'Bình'], 'Loại': ['Vỏ trấu', 'Vỏ trấu', 'Rơm rạ'], 'Khối lượng (Tấn)': [5, 8, 10]})
        st.dataframe(df_f, use_container_width=True)
    with c2:
        st.write("**🏭 Nhu cầu (Nhà máy)**")
        st.write("- **Nhà máy X:** Cần 15 Tấn Vỏ trấu")
    
    if st.button("KÍCH HOẠT KHỚP LỆNH TỐI ƯU"):
        with st.spinner('AI đang tính toán...'):
            time.sleep(1)
            st.success("🎉 Đã tìm thấy phương án ghép chuyến!")
            m1, m2 = st.columns(2)
            m1.metric("Khối lượng gom", "13 Tấn", "Vỏ trấu")
            m2.metric("Matching Score", "95%", "Tối ưu")
            st.code("Lệnh điều phối: Xe tải số 05 gom hàng từ Farm Hân & Farm An -> Nhà máy X", language="text")

# --- TAB 3: TỐI ƯU VẬN CHUYỂN ---
elif menu == "Tối ưu Vận chuyển":
    st.header("📍 3. Tối ưu lộ trình bằng bản đồ 3D")
    view_state = pdk.ViewState(latitude=10.7626, longitude=106.6602, zoom=12, pitch=45)
    arc_data = pd.DataFrame({
        's_lon': [106.67, 106.65], 's_lat': [10.77, 10.75],
        't_lon': [106.66, 106.66], 't_lat': [10.76, 10.76]
    })
    layer = pdk.Layer("ArcLayer", arc_data, get_source_position="[s_lon, s_lat]", get_target_position="[t_lon, t_lat]", get_source_color=[40, 167, 69], get_target_color=[220, 53, 69], get_width=5)
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))
    st.write("> **Giá trị:** Giảm quãng đường chạy rỗng, tiết kiệm 20% chi phí xăng xe.")

# --- TAB 4: TRUY XUẤT NGUỒN GỐC ---
elif menu == "Truy xuất nguồn gốc":
    st.header("🆔 4. Số hóa & Truy xuất nguồn gốc (QR)")
    col_a, col_b = st.columns([1, 2])
    with col_a:
        code = st.text_input("Nhập mã lô hàng:", "AL-2026-HUB")
        if st.button("TẠO MÃ QR"):
            qr = qrcode.make(f"AgriLoop Verified: {code} | Quality: Grade A | Farm: HUB-BUH")
            buf = io.BytesIO()
            qr.save(buf, format="PNG")
            st.image(buf, caption=f"Mã QR của {code}", width=250)
    with col_b:
        st.write("**📜 Nhật ký số (Digital Ledger)**")
        history = pd.DataFrame([
            {"Thời gian": "17/04/2026 08:00", "Sự kiện": "Xác nhận thu gom", "Vị trí": "Farm Hân"},
            {"Thời gian": "17/04/2026 14:00", "Sự kiện": "Đang vận chuyển", "Vị trí": "Xe tải 05"},
            {"Thời gian": "17/04/2026 16:30", "Sự kiện": "Đã nhập kho", "Vị trí": "Nhà máy X"}
        ])
        st.table(history)