import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Market Making Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# TITLE & INTRO
# -------------------------------
st.title("💃 Market Making Dance Revolution")
st.subheader("Understanding Risk, Not Chasing Profit")

st.write(
    "This dashboard helps users understand **why market makers lose money** "
    "during risky conditions and how decisions change with uncertainty."
)

# -------------------------------
# SIDEBAR SETTINGS
# -------------------------------
st.sidebar.header("⚙️ Market Settings")
st.sidebar.caption("Change values to simulate calm vs risky markets.")

TIME_STEPS = st.sidebar.slider("Time Steps", 200, 1000, 500)
BASE_SPREAD = st.sidebar.slider("Base Spread", 0.1, 1.0, 0.2)
NEWS_IMPACT = st.sidebar.slider("News Impact", 1, 10, 3)

# -------------------------------
# TOP METRICS (PREMIUM LOOK)
# -------------------------------
col1, col2, col3 = st.columns(3)

col1.metric("📦 Inventory Risk", "Dynamic")
col2.metric("⚠️ Market Risk", "High during news")
col3.metric("🎯 Goal", "Survival > Profit")

st.markdown("---")

# -------------------------------
# HOW TO USE
# -------------------------------
st.info(
    "👈 Adjust market settings on the left, then click **Run Simulation**. "
    "Watch how risk, profit, and inventory change — and read the suggestions below."
)

# -------------------------------
# MARKET SIMULATION FUNCTION
# -------------------------------
def simulate_market():
    prices = [100]
    inventory = 0
    cash = 0
    pnl = []
    inventory_hist = []

    for t in range(TIME_STEPS):
        price = prices[-1] + np.random.normal(0, 0.01)
        prices.append(price)

        spread = BASE_SPREAD + abs(inventory) * 0.01
        bid = price - spread / 2
        ask = price + spread / 2

        # Informed traders after mid-point
        if t > TIME_STEPS // 2:
            action = "buy"
        else:
            action = np.random.choice(["buy", "sell"])

        if action == "buy":
            inventory -= 1
            cash += ask
        else:
            inventory += 1
            cash -= bid

        inventory_hist.append(inventory)
        pnl.append(cash + inventory * price)

    return prices, pnl, inventory_hist

# -------------------------------
# RUN BUTTON
# -------------------------------
if st.button("▶️ Run Simulation"):

    prices, pnl, inventory_hist = simulate_market()

    # -------------------------------
    # CHART 1: PRICE
    # -------------------------------
    st.subheader("📈 Market Price Movement")
    st.caption("Sudden movements represent uncertainty and news-driven risk.")

    fig, ax = plt.subplots()
    ax.plot(prices)
    ax.set_xlabel("Time")
    ax.set_ylabel("Price")
    st.pyplot(fig)

    # -------------------------------
    # CHART 2: P&L
    # -------------------------------
    st.subheader("💰 Profit & Loss Over Time")
    st.caption("Losses after risky periods indicate adverse selection.")

    fig, ax = plt.subplots()
    ax.plot(pnl)
    ax.set_xlabel("Time")
    ax.set_ylabel("P&L")
    st.pyplot(fig)

    # -------------------------------
    # CHART 3: INVENTORY
    # -------------------------------
    st.subheader("📦 Inventory Exposure")
    st.caption("High inventory imbalance increases downside risk.")

    fig, ax = plt.subplots()
    ax.plot(inventory_hist)
    ax.set_xlabel("Time")
    ax.set_ylabel("Inventory")
    st.pyplot(fig)

    st.markdown("---")

    # -------------------------------
    # SMART DECISION SUGGESTIONS (WORLD-CLASS)
    # -------------------------------
    st.subheader("🧠 Decision Support & Suggestions")

    avg_inventory = np.mean(np.abs(inventory_hist))
    final_pnl = pnl[-1]

    if NEWS_IMPACT >= 7 and BASE_SPREAD < 0.3:
        st.warning(
            "⚠️ High news impact with low spread detected.\n\n"
            "Suggestion: **Increase spread** to protect against informed traders."
        )

    elif avg_inventory > 50:
        st.warning(
            "📦 Inventory risk is building up.\n\n"
            "Suggestion: **Slow down trading or rebalance positions**."
        )

    elif final_pnl < 0:
        st.info(
            "💡 Losses observed.\n\n"
            "Insight: Losses are due to uncertainty, not bad decisions. "
            "Risk control matters more than profit."
        )

    else:
        st.success(
            "✅ Market conditions look stable.\n\n"
            "Strategy is surviving current risk levels."
        )

    # -------------------------------
    # FINAL TAKEAWAY
    # -------------------------------
    st.markdown("---")
    st.success(
        "Final takeaway: **Market making is about managing uncertainty, "
        "not maximizing short-term profit.**"
    )
