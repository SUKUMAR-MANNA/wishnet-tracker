import streamlit as st
import pandas as pd
from datetime import date
import plotly.express as px
import os

# ⚙️ Page config
st.set_page_config(page_title="WishNet Tracker", layout="wide")

# 🎯 Title
st.title("📊 WishNet Tracker")
st.caption(f"Last updated: {date.today()}")

# 🔄 Auto refresh (optional)
refresh = st.checkbox("🔄 Auto Refresh (every 10s)")
if refresh:
    st.rerun()

# 🔢 Input
used = st.number_input("Enter your usage (GB)", min_value=0.0)

# 📊 Metrics
total_limit = 3300
remaining = max(total_limit - used, 0)  # prevent negative
progress = used / total_limit if total_limit > 0 else 0

col1, col2 = st.columns(2)

with col1:
    st.metric("📥 Used", f"{used:.2f} GB")

with col2:
    st.metric("📦 Remaining", f"{remaining:.2f} GB")

# 🔥 Progress bar
st.write(f"📊 {min(progress*100, 100):.1f}% used")
st.progress(min(progress, 1.0))

# 🚦 Smart status
if progress >= 1:
    st.error("🚨 Limit exceeded! Stop usage NOW")
elif progress >= 0.95:
    st.error("🚨 Almost finished! Stop usage NOW")
elif progress > 0.8:
    st.warning("⚠️ You are close to limit!")
elif progress < 0.3:
    st.success("🟢 You can use more data")
else:
    st.info("🟡 Balanced usage")

# 💾 File path
file = "usage.csv"

col_save, col_reset = st.columns(2)

# 💾 Save data
with col_save:
    if st.button("💾 Save Today’s Usage"):
        if os.path.exists(file):
            data = pd.read_csv(file)
        else:
            data = pd.DataFrame(columns=["date", "usage"])

        today_str = date.today().strftime("%Y-%m-%d")

        # Remove today's old entry
        data = data[data["date"] != today_str]

        new = pd.DataFrame({
            "date": [today_str],
            "usage": [used]
        })

        data = pd.concat([data, new])
        data.to_csv(file, index=False)

        st.success("✅ Saved successfully!")

# 🗑 Reset data
with col_reset:
    if st.button("🗑 Reset Data"):
        if os.path.exists(file):
            os.remove(file)
            st.warning("⚠️ All data deleted!")

# 📊 Show graph
if os.path.exists(file):
    data = pd.read_csv(file)

    if not data.empty:
        # Fix date
        data["date"] = pd.to_datetime(data["date"])

        # Sort
        data = data.sort_values("date")

        # Format for display
        data["date_str"] = data["date"].dt.strftime("%d %b")

        fig = px.bar(
            data,
            x="date_str",
            y="usage",
            title="📊 Daily Usage",
            text="usage"
        )

        fig.update_layout(
            template="plotly_dark",
            xaxis_title="Date",
            yaxis_title="Usage (GB)"
        )

        fig.update_traces(
            marker_color="#00C853",
            textposition="outside"
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("📭 No data yet. Save your first entry 🚀")

else:
    st.info("📭 No data yet. Save your first entry 🚀")