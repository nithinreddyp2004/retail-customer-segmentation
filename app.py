import joblib
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# =============================
# Page config
# =============================
st.set_page_config(
    page_title="Customer Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================
# Custom CSS
# =============================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Poppins:wght@500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #E8E6DF;
    }

    .stApp {
        background: linear-gradient(180deg, #0B0E13 0%, #0D1016 100%);
    }

    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1280px !important;
    }

    [data-testid="stSidebar"] {
        background: #0F1218 !important;
        border-right: 1px solid #1E2230 !important;
    }

    h1, h2, h3 {
        font-family: 'Poppins', sans-serif !important;
        letter-spacing: -0.03em !important;
    }

    h1 {
        font-size: 2.15rem !important;
        font-weight: 800 !important;
        color: #F4F1EA !important;
        margin-bottom: 0.2rem !important;
    }

    h2 {
        font-size: 1.3rem !important;
        color: #D5D1C8 !important;
    }

    .hero {
        background: radial-gradient(circle at top left, rgba(27,140,110,0.16), transparent 38%),
                    linear-gradient(180deg, #11151E 0%, #0F1218 100%);
        border: 1px solid #1E2230;
        border-radius: 22px;
        padding: 1.5rem 1.6rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 10px 35px rgba(0,0,0,0.16);
    }

    .card {
        background: #131824;
        border: 1px solid #1E2230;
        border-radius: 18px;
        padding: 1.2rem 1.3rem;
        box-shadow: 0 8px 28px rgba(0,0,0,0.14);
    }

    .metric-card {
        background: #131824;
        border: 1px solid #1E2230;
        border-radius: 16px;
        padding: 1rem 1.1rem;
    }

    .tag {
        display: inline-block;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        padding: 4px 10px;
        border-radius: 999px;
        border: 1px solid rgba(27,140,110,0.35);
        background: rgba(27,140,110,0.12);
        color: #7ED8BE;
        margin-right: 6px;
        margin-bottom: 6px;
    }

    .subtle {
        font-family: 'JetBrains Mono', monospace;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #5A6174;
        font-size: 0.72rem;
        margin-bottom: 1rem;
    }

    .muted {
        color: #6E7487;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .smalltext {
        color: #A7ADBC;
        font-size: 0.95rem;
        line-height: 1.75;
    }

    .resultbox {
        border-radius: 20px;
        padding: 1.7rem;
        border: 1px solid rgba(27,140,110,0.35);
        background: linear-gradient(180deg, rgba(13,36,32,0.96), rgba(13,18,24,0.96));
        text-align: center;
        box-shadow: 0 10px 35px rgba(0,0,0,0.15);
    }

    [data-testid="stMetric"] {
        background: #131824 !important;
        border: 1px solid #1E2230 !important;
        border-radius: 16px !important;
        padding: 1rem !important;
    }

    [data-testid="stMetricValue"] {
        color: #F1EFE8 !important;
        font-family: 'Poppins', sans-serif !important;
    }

    [data-testid="stMetricLabel"] {
        color: #6B7285 !important;
        font-family: 'JetBrains Mono', monospace !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        font-size: 0.68rem !important;
    }

    .stButton > button {
        background: #1B8C6E !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 0.7rem 1.2rem !important;
        box-shadow: 0 8px 20px rgba(27,140,110,0.18) !important;
    }

    .stButton > button:hover {
        background: #23A882 !important;
    }

    .stDownloadButton > button {
        border-radius: 12px !important;
        border: 1px solid #1B8C6E !important;
        background: transparent !important;
        color: #7ED8BE !important;
        font-family: 'JetBrains Mono', monospace !important;
    }

    [data-testid="stFileUploader"] {
        background: #131824 !important;
        border: 1px dashed #2A3040 !important;
        border-radius: 16px !important;
        padding: 1rem !important;
    }

    hr {
        border-color: #1E2230 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =============================
# Helpers
# =============================
def section_label(text: str):
    st.markdown(f'<div class="subtle">{text}</div>', unsafe_allow_html=True)

def card(title: str, body: str):
    st.markdown(
        f"""
        <div class="card">
            <div class="muted">{title}</div>
            <div class="smalltext" style="margin-top:0.55rem;">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Makes column matching easier:
    Recency, recency, RECENCY, Recency  -> Recency
    frequency_count -> Frequency
    monetary amount -> Monetary
    """
    rename_map = {}
    for col in df.columns:
        clean = str(col).strip().lower().replace(" ", "").replace("_", "")
        if clean == "recency":
            rename_map[col] = "Recency"
        elif clean == "frequency":
            rename_map[col] = "Frequency"
        elif clean == "monetary":
            rename_map[col] = "Monetary"
    return df.rename(columns=rename_map)

def plot_distribution(series: pd.Series, title: str):
    counts = series.value_counts()
    fig, ax = plt.subplots(figsize=(7, 3.5))
    bars = ax.bar(counts.index.astype(str), counts.values, width=0.55)
    ax.set_title(title, fontsize=10)
    ax.set_ylabel("Count")
    ax.grid(axis="y", alpha=0.2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(axis="x", rotation=15)
    for b in bars:
        ax.text(
            b.get_x() + b.get_width() / 2,
            b.get_height(),
            f"{int(b.get_height())}",
            ha="center",
            va="bottom",
            fontsize=8,
        )
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

# =============================
# Load model
# =============================
@st.cache_resource
def load_model():
    data = joblib.load("customer_segmentation_model.pkl")
    return data["scaler"], data["model"], data["cluster_map"]

model_loaded = True
try:
    scaler, model, cluster_map = load_model()
except Exception:
    model_loaded = False
    scaler, model, cluster_map = None, None, {}

# =============================
# Sidebar
# =============================
with st.sidebar:
    st.markdown(
        """
        <div style="padding:0.3rem 0 0.7rem 0;">
            <div style="font-family:Poppins,sans-serif;font-size:1.4rem;font-weight:800;color:#F4F1EA;">◈ Customer</div>
            <div style="font-family:Poppins,sans-serif;font-size:1.4rem;font-weight:800;color:#1B8C6E;">Intelligence</div>
            <div class="subtle" style="margin-top:0.5rem;">RFM · K-Means · Dashboard</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigation",
        ["Overview", "Predict Segment", "Batch Prediction", "About RFM"],
        label_visibility="collapsed",
    )

    st.markdown("<hr>", unsafe_allow_html=True)

    if model_loaded:
        st.success(f"Model loaded. {len(set(cluster_map.values()))} segments ready.")
    else:
        st.error("Model file not found.")
        st.caption("Place `customer_segmentation_model.pkl` in the same folder as app.py")

# =============================
# Prediction function
# =============================
def predict_segment(recency, frequency, monetary):
    df = pd.DataFrame([[recency, frequency, monetary]], columns=["Recency", "Frequency", "Monetary"])
    scaled = scaler.transform(df)
    cluster = int(model.predict(scaled)[0])
    segment = cluster_map.get(cluster, f"Cluster {cluster}")
    return cluster, segment

# =============================
# Overview
# =============================
if page == "Overview":
    st.markdown(
        """
        <div class="hero">
            <h1>Customer Segmentation Dashboard</h1>
            <div class="subtle">Smart customer grouping using RFM and K-Means</div>
            <div style="margin-top:0.9rem;">
                <span class="tag">Unsupervised ML</span>
                <span class="tag">RFM Features</span>
                <span class="tag">Batch Ready</span>
                <span class="tag">Python + Streamlit</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Algorithm", "K-Means")
    c2.metric("Features", "RFM")
    c3.metric("Segments", str(len(set(cluster_map.values()))) if model_loaded else "0")
    c4.metric("Status", "Live" if model_loaded else "Missing Model")

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    left, right = st.columns([1.15, 0.85], gap="large")

    with left:
        section_label("System overview")
        card(
            "What this app does",
            """
            This app takes <b>Recency</b>, <b>Frequency</b>, and <b>Monetary</b> values,
            scales them, and predicts the customer segment using your trained K-Means model.
            You can test one customer or upload a CSV for bulk prediction.
            """,
        )

        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
        st.markdown("### Segment registry")
        if model_loaded:
            seg_df = (
                pd.DataFrame(list(cluster_map.items()), columns=["Cluster", "Segment"])
                .sort_values("Cluster")
                .reset_index(drop=True)
            )
            st.dataframe(seg_df, use_container_width=True, hide_index=True)
        else:
            st.info("Model not loaded yet.")

    with right:
        section_label("RFM meaning")
        card(
            "Recency",
            "How recently the customer purchased. Lower days usually mean stronger engagement.",
        )
        st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
        card(
            "Frequency",
            "How often the customer buys. Higher frequency often means more loyal customers.",
        )
        st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
        card(
            "Monetary",
            "How much total value the customer has spent. Higher values indicate more valuable customers.",
        )

# =============================
# Predict Segment
# =============================
elif page == "Predict Segment":
    st.markdown(
        """
        <div class="hero">
            <h1>Single Customer Prediction</h1>
            <div class="subtle">Enter RFM values and get the predicted segment</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not model_loaded:
        st.error("Model file not found. Please add `customer_segmentation_model.pkl`.")
        st.stop()

    left, right = st.columns([1, 1], gap="large")

    with left:
        section_label("Input features")
        recency = st.number_input("Recency (days)", min_value=0.0, value=30.0, step=1.0)
        frequency = st.number_input("Frequency (count)", min_value=0.0, value=5.0, step=1.0)
        monetary = st.number_input("Monetary (₹)", min_value=0.0, value=1000.0, step=10.0)

        run = st.button("Run Prediction", use_container_width=True)

    with right:
        section_label("Prediction output")
        if run:
            cluster, segment = predict_segment(recency, frequency, monetary)

            st.markdown(
                f"""
                <div class="resultbox">
                    <div class="muted">Predicted Cluster</div>
                    <div style="font-family:Poppins,sans-serif;font-size:3rem;font-weight:800;color:#7ED8BE;line-height:1.1;">
                        {cluster}
                    </div>
                    <div style="height:10px;"></div>
                    <div style="font-family:Poppins,sans-serif;font-size:1.2rem;font-weight:700;color:#E8F8F4;">
                        {segment}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
            st.markdown("### Input summary")
            m1, m2, m3 = st.columns(3)
            m1.metric("Recency", f"{recency:.0f} days")
            m2.metric("Frequency", f"{frequency:.0f}")
            m3.metric("Monetary", f"₹{monetary:,.0f}")
        else:
            st.info("Enter values and click **Run Prediction**.")

# =============================
# Batch Prediction
# =============================
elif page == "Batch Prediction":
    st.markdown(
        """
        <div class="hero">
            <h1>Batch Prediction</h1>
            <div class="subtle">Upload a CSV file with Recency, Frequency, Monetary columns</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not model_loaded:
        st.error("Model file not found. Please add `customer_segmentation_model.pkl`.")
        st.stop()

    st.markdown(
        """
        <div class="card">
            <div class="muted">Required columns</div>
            <div style="margin-top:0.6rem;">
                <span class="tag">Recency</span>
                <span class="tag">Frequency</span>
                <span class="tag">Monetary</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded is not None:
        try:
            batch_df = pd.read_csv(uploaded)
            batch_df = normalize_columns(batch_df)

            st.markdown("### Preview")
            st.dataframe(batch_df.head(10), use_container_width=True, hide_index=True)

            required = ["Recency", "Frequency", "Monetary"]
            missing = [col for col in required if col not in batch_df.columns]

            if missing:
                st.error(
                    "CSV must contain these columns: Recency, Frequency, Monetary. "
                    f"Missing: {', '.join(missing)}"
                )
                st.stop()

            scaled = scaler.transform(batch_df[required])
            clusters = model.predict(scaled)
            batch_df["Cluster"] = clusters
            batch_df["Segment"] = batch_df["Cluster"].map(cluster_map)

            st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
            a, b, c = st.columns(3)
            a.metric("Records Processed", f"{len(batch_df):,}")
            b.metric("Unique Segments", f"{batch_df['Segment'].nunique()}")
            c.metric("Top Segment", batch_df["Segment"].mode()[0])

            st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
            st.markdown("### Segment distribution")
            plot_distribution(batch_df["Segment"], "Customer Segments")

            st.markdown("### Full results")
            st.dataframe(batch_df, use_container_width=True, hide_index=True)

            csv_out = batch_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download predictions CSV",
                data=csv_out,
                file_name="customer_segments.csv",
                mime="text/csv",
                use_container_width=True,
            )
        except Exception as e:
            st.error(f"Error reading file: {e}")
    else:
        st.info("Upload a CSV file to start batch prediction.")

# =============================
# About RFM
# =============================
elif page == "About RFM":
    st.markdown(
        """
        <div class="hero">
            <h1>About RFM</h1>
            <div class="subtle">Recency · Frequency · Monetary framework</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown("### RFM dimensions")
        card(
            "R - Recency",
            "How recently a customer purchased. Lower recency usually means more active customers.",
        )
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
        card(
            "F - Frequency",
            "How many times the customer purchased. Higher frequency often means loyalty.",
        )
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
        card(
            "M - Monetary",
            "How much total value the customer spent. Higher value customers are often more important.",
        )

    with right:
        st.markdown("### Why K-Means?")
        card(
            "Model choice",
            """
            K-Means is used because the goal is to discover natural customer groups.
            There are no labels here, so this is an unsupervised learning problem.
            """,
        )
        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
        st.markdown("### Business actions")
        card(
            "How segments are used",
            """
            High-value customers can get premium offers, loyal customers can get retention campaigns,
            at-risk customers can be re-engaged, and new customers can receive onboarding offers.
            """,
        )