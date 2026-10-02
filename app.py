import streamlit as st
st.set_page_config(page_title="Tính lãi tiền gửi tiết kiệm", page_icon="💰"
import math

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

st.title("💰 Máy tính lãi tiền gửi tiết kiệm")
st.caption("Tính lãi theo phương pháp lãi đơn hoặc lãi kép")

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def format_money(value):
    return f"{value:,.0f} VNĐ"


# =========================
# NHẬP DỮ LIỆU
# =========================
st.subheader("📋 Thông tin khoản tiền gửi")

amount = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=100_000_000.0,
    step=1_000_000.0,
    format="%.0f"
)

term_months = st.number_input(
    "Kỳ hạn (tháng)",
    min_value=1,
    max_value=600,
    value=12,
    step=1
)

interest_type = st.radio(
    "Phương pháp tính lãi",
    ["Lãi đơn", "Lãi kép"],
    horizontal=True
)

payout_type = st.selectbox(
    "Hình thức lãnh lãi",
    [
        "Lãnh lãi hàng tháng",
        "Lãnh lãi hàng quý",
        "Lãnh lãi cuối kỳ"
    ]
)

interest_rate = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=6.0,
    step=0.01,
    format="%.2f"
)

# =========================
# TÍNH TOÁN
# =========================
if st.button("🧮 Tính lãi", type="primary", use_container_width=True):

    principal = amount
    annual_rate = interest_rate / 100
    months = term_months
    years = months / 12

    # ---------------------------------
    # LÃI ĐƠN
    # ---------------------------------
    if interest_type == "Lãi đơn":

        total_interest = principal * annual_rate * years
        total_amount = principal + total_interest

        # Lãi định kỳ
        monthly_interest = principal * annual_rate / 12
        quarterly_interest = principal * annual_rate / 4

        if payout_type == "Lãnh lãi hàng tháng":
            periodic_interest = monthly_interest
            periods = months

        elif payout_type == "Lãnh lãi hàng quý":
            periodic_interest = quarterly_interest
            periods = months / 3

        else:
            periodic_interest = total_interest
            periods = 1

    # ---------------------------------
    # LÃI KÉP
    # ---------------------------------
    else:

        # Lãi kép được tính theo chu kỳ nhận lãi.
        if payout_type == "Lãnh lãi hàng tháng":
            periods = months
            periodic_rate = annual_rate / 12

            total_amount = principal * (
                (1 + periodic_rate) ** periods
            )

            total_interest = total_amount - principal

            # Lãi phát sinh ở kỳ đầu tiên
            periodic_interest = principal * periodic_rate

        elif payout_type == "Lãnh lãi hàng quý":
            periods = months / 3
            periodic_rate = annual_rate / 4

            total_amount = principal * (
                (1 + periodic_rate) ** periods
            )

            total_interest = total_amount - principal

            # Lãi phát sinh ở quý đầu tiên
            periodic_interest = principal * periodic_rate

        else:
            # Lãi kép cuối kỳ: quy đổi theo tháng
            periods = months
            monthly_rate = annual_rate / 12

            total_amount = principal * (
                (1 + monthly_rate) ** periods
            )

            total_interest = total_amount - principal

            periodic_interest = total_interest

    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================
    st.divider()
    st.subheader("📊 Kết quả")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "💵 Tiền lãi định kỳ",
            format_money(periodic_interest)
        )

        st.metric(
            "📈 Tổng tiền lãi",
            format_money(total_interest)
        )

    with col2:
        st.metric(
            "🏦 Tiền gốc",
            format_money(principal)
        )

        st.metric(
            "💰 Tổng gốc + lãi",
            format_money(total_amount)
        )

    # =========================
    # THÔNG TIN CHI TIẾT
    # =========================
    st.divider()

    st.subheader("📝 Chi tiết khoản gửi")

    details = {
        "Số tiền gửi": format_money(principal),
        "Kỳ hạn": f"{months} tháng",
        "Phương pháp tính": interest_type,
        "Hình thức lãnh lãi": payout_type,
        "Lãi suất": f"{interest_rate:.2f}%/năm",
        "Tiền lãi định kỳ": format_money(periodic_interest),
        "Tổng tiền lãi": format_money(total_interest),
        "Tổng tiền nhận được": format_money(total_amount),
    }

    for key, value in details.items():
        col1, col2 = st.columns([1, 2])
        with col1:
            st.write(f"**{key}**")
        with col2:
            st.write(value)

    # =========================
    # LƯU Ý
    # =========================
    st.info(
        "💡 Lưu ý: Đây là công cụ mô phỏng theo công thức lãi suất nhập vào. "
        "Lãi suất thực tế của ngân hàng có thể áp dụng quy định riêng về "
        "ngày tính lãi, số ngày trong kỳ, phương thức nhập lãi vào gốc "
        "và làm tròn số tiền."
    )
