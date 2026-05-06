import streamlit as st
import numpy as np
from PIL import Image
import io

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Fake Signature Detector",
    page_icon="✍️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap');

/* ── Root Variables ── */
:root {
    --bg: #0a0a0f;
    --surface: #12121a;
    --surface2: #1a1a28;
    --border: rgba(255,255,255,0.07);
    --accent: #7c6af7;
    --accent2: #a78bfa;
    --real: #22c55e;
    --fake: #ef4444;
    --text: #e2e8f0;
    --muted: #64748b;
}

/* ── Base ── */
html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Syne', sans-serif !important;
}

.stApp {
    background: var(--bg) !important;
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(124,106,247,0.15), transparent),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(167,139,250,0.08), transparent);
}

/* ── Hide Streamlit Chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
.block-container { padding: 2.5rem 1.5rem 4rem !important; max-width: 780px !important; }

/* ── Hero Header ── */
.hero {
    text-align: center;
    padding: 3rem 0 2rem;
}

.hero-badge {
    display: inline-block;
    background: rgba(124,106,247,0.15);
    border: 1px solid rgba(124,106,247,0.3);
    color: var(--accent2);
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    padding: 0.35rem 1rem;
    border-radius: 100px;
    margin-bottom: 1.2rem;
    text-transform: uppercase;
}

.hero h1 {
    font-size: clamp(2rem, 5vw, 3rem) !important;
    font-weight: 800 !important;
    letter-spacing: -0.03em;
    line-height: 1.1;
    background: linear-gradient(135deg, #fff 30%, var(--accent2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.75rem !important;
}

.hero p {
    color: var(--muted);
    font-size: 1rem;
    font-weight: 400;
    max-width: 440px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ── Upload Zone ── */
.upload-zone {
    background: var(--surface);
    border: 1.5px dashed rgba(124,106,247,0.35);
    border-radius: 16px;
    padding: 2rem;
    margin: 2rem 0;
    transition: border-color 0.3s;
    position: relative;
    overflow: hidden;
}

.upload-zone::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse 60% 40% at 50% 0%, rgba(124,106,247,0.06), transparent);
    pointer-events: none;
}

/* Streamlit file uploader overrides */
[data-testid="stFileUploader"] {
    background: transparent !important;
}

[data-testid="stFileUploader"] > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
}

[data-testid="stFileUploader"] label {
    color: var(--muted) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
}

[data-testid="stFileUploader"] button {
    background: rgba(124,106,247,0.15) !important;
    border: 1px solid rgba(124,106,247,0.4) !important;
    color: var(--accent2) !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
}

[data-testid="stFileUploader"] button:hover {
    background: rgba(124,106,247,0.3) !important;
}

/* ── Analyze Button ── */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #7c6af7, #a78bfa) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.85rem 2rem !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.02em;
    cursor: pointer !important;
    transition: all 0.25s !important;
    box-shadow: 0 4px 24px rgba(124,106,247,0.3) !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 32px rgba(124,106,247,0.45) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Result Cards ── */
.result-card {
    border-radius: 16px;
    padding: 2rem;
    margin: 1.5rem 0;
    border: 1.5px solid;
    position: relative;
    overflow: hidden;
}

.result-real {
    background: rgba(34,197,94,0.07);
    border-color: rgba(34,197,94,0.3);
}

.result-fake {
    background: rgba(239,68,68,0.07);
    border-color: rgba(239,68,68,0.3);
}

.result-real::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse 80% 60% at 50% 0%, rgba(34,197,94,0.1), transparent);
    pointer-events: none;
}

.result-fake::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse 80% 60% at 50% 0%, rgba(239,68,68,0.1), transparent);
    pointer-events: none;
}

.result-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

.result-real .result-label { color: var(--real); }
.result-fake .result-label { color: var(--fake); }

.result-verdict {
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin-bottom: 0.4rem;
    position: relative;
    z-index: 1;
}

.result-real .result-verdict { color: #fff; }
.result-fake .result-verdict { color: #fff; }

.result-confidence {
    font-size: 0.9rem;
    color: var(--muted);
    position: relative;
    z-index: 1;
}

/* ── Progress Bar ── */
.confidence-bar {
    height: 6px;
    border-radius: 100px;
    margin: 1rem 0;
    position: relative;
    background: rgba(255,255,255,0.08);
    overflow: hidden;
}

.confidence-fill-real {
    height: 100%;
    border-radius: 100px;
    background: linear-gradient(90deg, #16a34a, #22c55e);
    transition: width 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.confidence-fill-fake {
    height: 100%;
    border-radius: 100px;
    background: linear-gradient(90deg, #dc2626, #ef4444);
    transition: width 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* ── Image Preview ── */
.img-preview {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid var(--border);
    background: var(--surface2);
}

/* ── Info Cards ── */
.info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin: 1.5rem 0;
}

.info-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem;
}

.info-card-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.4rem;
}

.info-card-value {
    font-size: 1rem;
    font-weight: 700;
    color: var(--text);
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 2rem 0;
}

/* ── Footer ── */
.footer {
    text-align: center;
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: var(--muted);
    margin-top: 3rem;
    letter-spacing: 0.05em;
}

/* ── Spinner ── */
.stSpinner > div {
    border-color: var(--accent) transparent transparent !important;
}

/* ── Streamlit image ── */
[data-testid="stImage"] img {
    border-radius: 12px;
    border: 1px solid var(--border);
}
</style>
""", unsafe_allow_html=True)


# ─── Load Model ─────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    try:
        import tensorflow as tf
        model = tf.keras.models.load_model("best_model.h5")
        return model, None
    except Exception as e:
        return None, str(e)


# ─── Preprocess Image ────────────────────────────────────────────────────────
def preprocess_image(image: Image.Image) -> np.ndarray:
    img = image.convert("RGB")
    img = img.resize((224, 224))
    arr = np.array(img) / 255.0
    return np.expand_dims(arr, axis=0)


# ─── Hero Section ────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">🔬 VGG16 Transfer Learning</div>
    <h1>Signature Authenticator</h1>
    <p>Upload a signature image and let the AI determine whether it's genuine or forged in seconds.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ─── Load Model ─────────────────────────────────────────────────────────────
model, model_error = load_model()

if model_error:
    st.error(f"⚠️ Could not load model: `{model_error}`\n\nMake sure `best_model.h5` is in the same folder as `app.py`.")
    st.stop()

# ─── Upload Section ──────────────────────────────────────────────────────────
st.markdown('<div class="upload-zone">', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "Drop your signature image here",
    type=["jpg", "jpeg", "png", "bmp", "tiff"],
    label_visibility="visible",
    help="Supported formats: JPG, JPEG, PNG, BMP, TIFF"
)
st.markdown('</div>', unsafe_allow_html=True)

# ─── Main Logic ──────────────────────────────────────────────────────────────
if uploaded_file:
    image = Image.open(io.BytesIO(uploaded_file.read()))
    w, h = image.size
    file_size_kb = uploaded_file.size / 1024

    # Two-column layout: image + metadata
    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.image(image, caption="Uploaded Signature", use_container_width=True)

    with col2:
        st.markdown(f"""
        <div class="info-grid" style="margin-top:0;">
            <div class="info-card">
                <div class="info-card-label">Width</div>
                <div class="info-card-value">{w}px</div>
            </div>
            <div class="info-card">
                <div class="info-card-label">Height</div>
                <div class="info-card-value">{h}px</div>
            </div>
            <div class="info-card">
                <div class="info-card-label">File Size</div>
                <div class="info-card-value">{file_size_kb:.1f} KB</div>
            </div>
            <div class="info-card">
                <div class="info-card-label">Format</div>
                <div class="info-card-value">{uploaded_file.type.split("/")[-1].upper()}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── Analyze Button ──
    if st.button("✦ Analyze Signature", use_container_width=True):
        with st.spinner("Analyzing..."):
            import time
            time.sleep(0.5)  # slight pause for UX feel

            input_arr = preprocess_image(image)
            prediction = model.predict(input_arr, verbose=0)[0][0]

            # VGG16 in this notebook: 1 = Fake, 0 = Real
            is_fake = prediction > 0.5
            confidence = float(prediction) if is_fake else float(1 - prediction)
            conf_pct = confidence * 100

        # ── Result Card ──
        if is_fake:
            st.markdown(f"""
            <div class="result-card result-fake">
                <div class="result-label">⚠ Detection Result</div>
                <div class="result-verdict">FORGED SIGNATURE</div>
                <div class="result-confidence">Confidence: {conf_pct:.1f}%</div>
                <div class="confidence-bar">
                    <div class="confidence-fill-fake" style="width:{conf_pct}%"></div>
                </div>
                <div style="font-size:0.82rem;color:#94a3b8;margin-top:0.5rem;">
                    The model has detected signs of forgery in this signature.
                    This result is for reference only — always verify with a human expert.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-card result-real">
                <div class="result-label">✓ Detection Result</div>
                <div class="result-verdict">AUTHENTIC SIGNATURE</div>
                <div class="result-confidence">Confidence: {conf_pct:.1f}%</div>
                <div class="confidence-bar">
                    <div class="confidence-fill-real" style="width:{conf_pct}%"></div>
                </div>
                <div style="font-size:0.82rem;color:#94a3b8;margin-top:0.5rem;">
                    The model classifies this signature as genuine.
                    This result is for reference only — always verify with a human expert.
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ── Raw Score Info ──
        st.markdown(f"""
        <div class="info-card" style="margin-top:1rem;">
            <div class="info-card-label">Raw Model Output Score</div>
            <div class="info-card-value" style="font-family:'DM Mono',monospace; font-size:1.3rem;">
                {prediction:.6f}
            </div>
            <div style="font-size:0.75rem;color:var(--muted);margin-top:0.3rem;">
                Threshold: 0.5 — values above = Fake, below = Real
            </div>
        </div>
        """, unsafe_allow_html=True)

else:
    # ── Placeholder when nothing is uploaded ──
    st.markdown("""
    <div style="
        text-align:center;
        padding: 3rem 1rem;
        background: var(--surface);
        border-radius: 16px;
        border: 1px solid var(--border);
        color: var(--muted);
    ">
        <div style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.4;">✍️</div>
        <div style="font-size: 0.9rem; font-family: 'DM Mono', monospace; letter-spacing: 0.05em;">
            No signature uploaded yet
        </div>
        <div style="font-size: 0.8rem; margin-top: 0.5rem; opacity: 0.7;">
            Upload an image above to get started
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="divider"></div>
<div class="footer">
    Fake Signature Detector · VGG16 Transfer Learning · Built with Streamlit
</div>
""", unsafe_allow_html=True)
