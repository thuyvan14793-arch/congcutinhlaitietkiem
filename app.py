```python
import streamlit as st
import math

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

st.title("💰 TÍNH LÃI TIỀN GỬI TIẾT KIỆM")
st.caption("Tính toán lãi đơn và lãi kép theo kỳ hạn và hình thức nhận lãi")

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def format_money(value):
    return f"{value:,.0f} VNĐ".replace(",", ".")


# =========================
# NHẬP DỮ LIỆU
# =========================
st.subheader("📋 Thông tin khoản tiền gửi")

so_tien = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=100_000_000.0,
    step=1_000_000.0,
    format="%.0f"
)

ky_han = st.number_input(
    "Kỳ hạn (tháng)",
    min_value=1,
    max_value=600,
    value=12,
    step=1
)

loai_lai = st.selectbox(
    "Hình thức tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ]
)

hinh_thuc_lanh_lai = st.selectbox(
    "Hình thức nhận lãi",
    [
        "Lãnh lãi hàng tháng",
        "Lãnh lãi hàng quý",
        "Lãnh lãi cuối kỳ"
    ]
)

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=5.0,
    step=0.1,
    format="%.2f"
)

# =========================
# TÍNH TOÁN
# =========================
if st.button("🧮 TÍNH LÃI", type="primary", use_container_width=True):

    if so_tien <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
        st.stop()

    # Lãi suất theo tháng
    lai_suat_nam = lai_suat / 100
    lai_suat_thang = lai_suat_nam / 12

    # Thời gian gửi theo năm
    so_nam = ky_han / 12

    # ---------------------------------
    # LÃI ĐƠN
    # ---------------------------------
    if loai_lai == "Lãi đơn":

        tong_lai = so_tien * lai_suat_nam * so_nam
        tong_tien = so_tien + tong_lai

        # Tiền lãi định kỳ
        if hinh_thuc_lanh_lai == "Lãnh lãi hàng tháng":
            lai_dinh_ky = so_tien * lai_suat_thang

        elif hinh_thuc_lanh_lai == "Lãnh lãi hàng quý":
            lai_dinh_ky = so_tien * lai_suat_thang * 3

        else:
            lai_dinh_ky = tong_lai

    # ---------------------------------
    # LÃI KÉP
    # ---------------------------------
    else:

        # Với lãi kép:
        # Tiền lãi được nhập vào gốc sau mỗi kỳ.
        #
        # Lãnh lãi hàng tháng:
        # ghép lãi theo tháng.
        #
        # Lãnh lãi hàng quý:
        # ghép lãi theo quý.
        #
        # Lãnh lãi cuối kỳ:
        # ghép lãi theo năm.
        
        if hinh_thuc_lanh_lai == "Lãnh lãi hàng tháng":
            so_ky = ky_han
            lai_suat_ky = lai_suat_nam / 12

        elif hinh_thuc_lanh_lai == "Lãnh lãi hàng quý":
            so_ky = math.ceil(ky_han / 3)
            lai_suat_ky = lai_suat_nam / 4

        else:
            # Nếu kỳ hạn dưới 12 tháng, tính theo tỷ lệ thời gian.
            # Nếu từ 12 tháng trở lên, ghép theo năm.
            so_ky = so_nam
            lai_suat_ky = lai_suat_nam

        tong_tien = so_tien * (1 + lai_suat_ky) ** so_ky
        tong_lai = tong_tien - so_tien

        # Tính lãi của kỳ đầu tiên để hiển thị
        if hinh_thuc_lanh_lai == "Lãnh lãi hàng tháng":
            lai_dinh_ky = so_tien * lai_suat_ky

        elif hinh_thuc_lanh_lai == "Lãnh lãi hàng quý":
            lai_dinh_ky = so_tien * lai_suat_ky

        else:
            lai_dinh_ky = tong_lai

    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================
    st.divider()
    st.subheader("📊 Kết quả tính toán")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Tiền lãi định kỳ",
            format_money(lai_dinh_ky)
        )

        st.metric(
            "Tổng tiền lãi",
            format_money(tong_lai)
        )

    with col2:
        st.metric(
            "Tiền gốc",
            format_money(so_tien)
        )

        st.metric(
            "Tổng gốc + lãi",
            format_money(tong_tien)
        )

    # =========================
    # THÔNG TIN CHI TIẾT
    # =========================
    st.divider()

    st.subheader("📝 Chi tiết khoản gửi")

    st.write(f"**Số tiền gửi:** {format_money(so_tien)}")
    st.write(f"**Kỳ hạn:** {ky_han} tháng")
    st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
    st.write(f"**Hình thức:** {loai_lai}")
    st.write(f"**Nhận lãi:** {hinh_thuc_lanh_lai}")

    # =========================
    # CÔNG THỨC
    # =========================
    with st.expander("📐 Xem công thức tính"):

        if loai_lai == "Lãi đơn":
            st.latex(
                r"I = P \times r \times t"
            )
            st.write(
                "Trong đó: P là tiền gốc, r là lãi suất năm, "
                "t là thời gian gửi tính theo năm."
            )

        else:
            st.latex(
                r"A = P(1+r)^n"
            )
            st.write(
                "Trong đó: P là tiền gốc, r là lãi suất của mỗi kỳ "
                "ghép lãi và n là số kỳ ghép lãi."
            )

    # =========================
    # LƯU Ý
    # =========================
    st.info(
        "💡 Kết quả là phép tính tham khảo theo lãi suất người dùng nhập. "
        "Lãi suất và phương thức tính thực tế của ngân hàng có thể có "
        "quy định riêng theo từng sản phẩm tiền gửi."
    )


# =========================
# FOOTER
# =========================
st.divider()

st.caption(
    "💰 Ứng dụng tính lãi tiết kiệm | Streamlit"
)
```
