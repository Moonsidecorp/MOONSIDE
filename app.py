# ══════════════════════════════════════════════════════════════════════════════
#  MOONSIDE INTELLIGENCE PLATFORM — app.py
#  Version : 1.0.0
#  Author  : Moonside / Market n Mocha (MnM)
#  Stack   : Streamlit · Groq · Gemini · IDX API · yfinance
#  Inspired by: Fincept Terminal architecture (modular, multi-asset, research-first)
#  Enhanced with: SIGMA v87 core engines (IDX pipeline, BSJP, Bandarmologi)
# ══════════════════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────
# PART 1: IMPORTS
# ─────────────────────────────────────────────
import streamlit as st
import streamlit.components.v1 as components
import os, json, time, re, math, random, hashlib, threading
import requests
import sqlite3
from datetime import datetime, timedelta, timezone, date
from typing import Optional
from urllib.parse import urlencode

try:
    import yfinance as yf
    HAS_YF = True
except ImportError:
    HAS_YF = False

try:
    from groq import Groq
    HAS_GROQ = True
except ImportError:
    HAS_GROQ = False

try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

try:
    import fitz
    HAS_FITZ = True
except ImportError:
    HAS_FITZ = False

try:
    import pytz as _pytz
    _WIB = _pytz.timezone("Asia/Jakarta")
except ImportError:
    _pytz = None
    _WIB = timezone(timedelta(hours=7))


# ─────────────────────────────────────────────
# PART 2: PAGE CONFIG — harus sebelum st lain
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="MOONSIDE — Market Intelligence",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": "MOONSIDE Intelligence Platform | by Market n Mocha & KIPM-UP",
    },
)


# ─────────────────────────────────────────────
# PART 3: GLOBAL CONSTANTS & CONFIG
# ─────────────────────────────────────────────

# ── Platform branding ─────────────────────────
PLATFORM_NAME    = "MOONSIDE"
PLATFORM_VERSION = "1.0.0"
PLATFORM_TAGLINE = "Institutional Market Intelligence"
PLATFORM_DESC    = "IDX · Forex · Crypto · AI Research"

# ── Color tokens (mirror landing page) ───────
C = {
    "bg":      "#050507",
    "bg2":     "#08080C",
    "bg3":     "#0D0D12",
    "bg4":     "#111118",
    "surface": "rgba(255,255,255,0.03)",
    "border":  "rgba(255,255,255,0.06)",
    "border2": "rgba(255,255,255,0.1)",
    "accent":  "#7C3AED",
    "accent2": "#A855F7",
    "text":    "#F5F5F7",
    "text2":   "#98989F",
    "text3":   "#3D3D45",
    "green":   "#34C759",
    "red":     "#FF3B30",
    "blue":    "#007AFF",
    "gold":    "#FF9F0A",
    "purple":  "#C4B5FD",
    "mono":    "'SF Mono','IBM Plex Mono','Menlo','Courier New',monospace",
}

# ── TTL config (dari SIGMA v87 CACHE_CONFIG) ──
CACHE_CONFIG = {
    "fundamental":   85 * 86400,
    "price_live":    90,
    "broker_data":   300,
    "news":          1800,
    "market_data":   604800,
    "global_rates":  1800,
    "ff_actuals":    300,
    "ec_high_impact":60,
    "suspended":     21600,
    "ipo_data":      86400,
    "rrg_data":      3600,
    "screener":      180,
}

# ── IDX Trading Calendar 2025-2026 ────────────
_IDX_HOLIDAYS = {
    "2025-01-01","2025-01-27","2025-01-28","2025-01-29","2025-01-30",
    "2025-03-28","2025-03-31","2025-04-14","2025-04-17","2025-04-18",
    "2025-05-01","2025-05-12","2025-05-29","2025-06-01","2025-06-02",
    "2025-06-06","2025-08-17","2025-09-01","2025-09-02","2025-10-06",
    "2025-12-25","2025-12-26",
    "2026-01-01","2026-01-28","2026-01-29","2026-01-30",
    "2026-03-20","2026-03-23","2026-04-02","2026-04-03",
    "2026-05-01","2026-05-14","2026-05-25","2026-08-17","2026-12-25",
}

# ── Free Float DB (IDX-verified, top 100) ─────
_FF_DB = {
    "BBCA":48.0,"BBRI":43.3,"BMRI":40.0,"TLKM":47.7,"ASII":50.1,
    "GOTO":82.0,"BYAN":36.6,"TPIA":14.8,"UNVR":15.0,"KLBF":43.3,
    "ICBP":19.7,"INDF":49.9,"SMMA":9.7,"MDKA":41.8,"MAPI":42.0,
    "HMSP":7.5,"GGRM":24.8,"ITMG":35.2,"ADRO":34.6,"PTBA":34.7,
    "MEDC":33.1,"INCO":20.5,"ANTM":35.0,"TINS":34.9,"ACES":53.2,
    "MNCN":40.6,"BTPS":25.0,"SCMA":49.7,"MYOR":35.0,"CPIN":44.3,
    "JPFA":43.2,"MAIN":24.7,"SIDO":19.8,"ULTJ":33.0,"ROTI":32.5,
    "BRIS":23.7,"BJBR":33.4,"BBNI":40.0,"BJTM":33.0,"NISP":30.0,
    "BBTN":40.0,"PNBN":47.0,"BNLI":40.0,"BDMN":36.0,"MEGA":28.0,
    "WSKT":62.0,"WIKA":66.0,"PTPP":51.0,"ADHI":34.0,"NRCA":25.0,
    "JSMR":30.0,"ISAT":20.0,"EXCL":33.0,"FREN":38.0,"LINK":52.0,
    "TOWR":21.4,"MTEL":28.0,"TBIG":38.0,"HEAL":35.0,"MIKA":26.0,
    "SIDO":19.8,"KAEF":9.1,"KLBF":43.3,"PYFA":40.0,"DVLA":17.4,
    "SMGR":49.4,"INTP":36.1,"TOTO":44.5,"AMRT":18.0,"HERO":56.0,
    "LPPF":42.7,"RALS":33.7,"MAPI":42.0,"ACES":53.2,"MAP":42.0,
    "PGAS":43.2,"AKRA":41.4,"INDR":37.2,"ARNA":38.7,"ALMI":28.0,
    "BSDE":34.8,"CTRA":35.3,"SMRA":40.4,"LPKR":42.5,"PWON":48.3,
    "ASRI":39.6,"DMAS":30.0,"GIAA":50.2,"BIRD":33.4,"TAXI":38.0,
    "UNTR":40.5,"SMSM":40.7,"GJTL":31.2,"AUTO":20.3,"IMAS":21.3,
}


# ─────────────────────────────────────────────
# PART 4: GLOBAL CSS INJECTION — MOONSIDE UI
# ─────────────────────────────────────────────
def _inject_global_css():
    st.markdown(f"""
<style>
/* ── RESET & FONTS ──────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display',
                 'Helvetica Neue', Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
}}

/* ── STREAMLIT ELEMENT RESETS ───────────────────────────── */
.stApp {{
    background: {C['bg']} !important;
}}
.stApp > header {{ display: none !important; }}
.block-container {{
    padding: 0 !important;
    max-width: 100% !important;
}}

/* ── SIDEBAR KILL ────────────────────────────────────────── */
section[data-testid="stSidebar"] {{ display: none !important; }}
.stDecoration {{ display: none !important; }}

/* ── SCROLLBAR ───────────────────────────────────────────── */
::-webkit-scrollbar {{ width: 3px; height: 3px; }}
::-webkit-scrollbar-track {{ background: {C['bg']}; }}
::-webkit-scrollbar-thumb {{
    background: rgba(124,58,237,0.35);
    border-radius: 2px;
}}

/* ── TAB SYSTEM (Fincept-style) ──────────────────────────── */
.stTabs [data-baseweb="tab-list"] {{
    background: rgba(255,255,255,0.025) !important;
    border-bottom: 1px solid {C['border']} !important;
    padding: 0 20px !important;
    gap: 0 !important;
}}
.stTabs [data-baseweb="tab"] {{
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    color: {C['text3']} !important;
    font-size: 12.5px !important;
    font-weight: 500 !important;
    letter-spacing: 0.03em !important;
    padding: 12px 18px !important;
    border-radius: 0 !important;
    transition: all 0.15s !important;
}}
.stTabs [data-baseweb="tab"]:hover {{
    color: {C['text2']} !important;
    background: rgba(255,255,255,0.03) !important;
}}
.stTabs [aria-selected="true"] {{
    color: {C['text']} !important;
    border-bottom: 2px solid {C['accent']} !important;
    background: transparent !important;
}}
.stTabs [data-baseweb="tab-panel"] {{
    background: transparent !important;
    padding: 0 !important;
}}

/* ── METRICS ─────────────────────────────────────────────── */
[data-testid="stMetric"] {{
    background: rgba(255,255,255,0.022) !important;
    border: 1px solid {C['border']} !important;
    border-radius: 10px !important;
    padding: 14px 16px !important;
}}
[data-testid="stMetricLabel"] {{
    color: {C['text3']} !important;
    font-size: 10px !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    font-family: {C['mono']} !important;
}}
[data-testid="stMetricValue"] {{
    color: {C['text']} !important;
    font-size: 22px !important;
    font-weight: 700 !important;
    letter-spacing: -0.03em !important;
}}
[data-testid="stMetricDelta"] {{
    font-size: 11px !important;
    font-weight: 600 !important;
}}

/* ── BUTTONS ─────────────────────────────────────────────── */
.stButton > button {{
    background: rgba(124,58,237,0.12) !important;
    border: 1px solid rgba(124,58,237,0.28) !important;
    color: #C4B5FD !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    border-radius: 8px !important;
    padding: 8px 18px !important;
    transition: all 0.18s !important;
    font-family: {C['mono']} !important;
    text-transform: uppercase !important;
}}
.stButton > button:hover {{
    background: rgba(124,58,237,0.22) !important;
    border-color: rgba(168,85,247,0.45) !important;
    box-shadow: 0 0 16px rgba(124,58,237,0.18) !important;
    transform: translateY(-1px) !important;
}}
.stButton > button[kind="primary"] {{
    background: linear-gradient(135deg, #7C3AED, #9333EA) !important;
    border-color: transparent !important;
    color: #fff !important;
    box-shadow: 0 4px 14px rgba(124,58,237,0.35) !important;
}}

/* ── INPUTS ──────────────────────────────────────────────── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea {{
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid {C['border2']} !important;
    border-radius: 8px !important;
    color: {C['text']} !important;
    font-family: {C['mono']} !important;
    font-size: 13px !important;
}}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {{
    border-color: {C['accent']} !important;
    box-shadow: 0 0 0 2px rgba(124,58,237,0.12) !important;
}}
.stSelectbox > div > div {{
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid {C['border2']} !important;
    border-radius: 8px !important;
    color: {C['text']} !important;
}}

/* ── DATAFRAME ───────────────────────────────────────────── */
.stDataFrame {{
    border: 1px solid {C['border']} !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}}

/* ── SPINNERS & ALERTS ───────────────────────────────────── */
.stSpinner > div > div {{
    border-top-color: {C['accent']} !important;
}}
.stAlert {{
    border-radius: 8px !important;
    font-size: 13px !important;
}}

/* ── DIVIDER ─────────────────────────────────────────────── */
hr {{
    border: none !important;
    border-top: 1px solid {C['border']} !important;
    margin: 20px 0 !important;
}}

/* ── MOBILE COMPAT ───────────────────────────────────────── */
@media (max-width: 768px) {{
    .stTabs [data-baseweb="tab"] {{
        font-size: 11px !important;
        padding: 10px 12px !important;
    }}
}}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PART 5: TOPBAR — MOONSIDE Header Component
# Inspired by Fincept Terminal's header design
# ─────────────────────────────────────────────
def _render_topbar():
    now_wib = datetime.now(_WIB)
    hour    = now_wib.hour
    is_market_open = (
        now_wib.weekday() < 5
        and now_wib.strftime("%Y-%m-%d") not in _IDX_HOLIDAYS
        and 9 <= hour < 16
    )
    market_label = "MARKET OPEN" if is_market_open else "AFTER HOURS"
    market_color = C['green'] if is_market_open else C['gold']
    time_str     = now_wib.strftime("%d %b %Y · %H:%M WIB")

    st.markdown(f"""
<div style="
    display:flex; align-items:center; justify-content:space-between;
    padding:0 28px; height:52px;
    background:rgba(5,5,7,0.95);
    border-bottom:1px solid {C['border']};
    backdrop-filter:blur(20px);
    position:sticky; top:0; z-index:999;
">
    <!-- Logo -->
    <div style="display:flex;align-items:center;gap:10px;">
        <div style="
            width:28px;height:28px;
            background:linear-gradient(135deg,{C['accent']},{C['accent2']});
            border-radius:8px;display:flex;align-items:center;justify-content:center;
            box-shadow:0 0 12px rgba(124,58,237,0.4);
        ">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                <path d="M7 1.5C3.96 1.5 1.5 3.96 1.5 7S3.96 12.5 7 12.5 12.5 10.04 12.5 7 10.04 1.5 7 1.5zm0 9C5.07 10.5 3.5 8.93 3.5 7S5.07 3.5 7 3.5 10.5 5.07 10.5 7 8.93 10.5 7 10.5z" fill="white" fill-opacity="0.9"/>
                <circle cx="7" cy="7" r="1.8" fill="white"/>
            </svg>
        </div>
        <div>
            <div style="font-size:13px;font-weight:700;letter-spacing:0.1em;color:{C['text']};text-transform:uppercase;">{PLATFORM_NAME}</div>
            <div style="font-size:8.5px;color:{C['text3']};letter-spacing:0.1em;text-transform:uppercase;font-family:{C['mono']};margin-top:-1px;">{PLATFORM_DESC}</div>
        </div>
    </div>

    <!-- Center: Market Status -->
    <div style="display:flex;align-items:center;gap:20px;">
        <div style="display:flex;align-items:center;gap:7px;">
            <div style="width:6px;height:6px;border-radius:50%;background:{market_color};
                box-shadow:0 0 8px {market_color};
                animation:{'blink 2s infinite' if is_market_open else 'none'};"></div>
            <span style="font-size:10px;font-weight:700;color:{market_color};
                letter-spacing:0.1em;font-family:{C['mono']};">{market_label}</span>
        </div>
        <span style="font-size:10px;color:{C['text3']};font-family:{C['mono']};">{time_str}</span>
    </div>

    <!-- Right: Version badge -->
    <div style="display:flex;align-items:center;gap:8px;">
        <div style="
            padding:3px 10px;border-radius:5px;
            background:rgba(124,58,237,0.1);border:1px solid rgba(124,58,237,0.22);
            font-size:9px;font-weight:700;color:#A78BFA;letter-spacing:0.1em;
            font-family:{C['mono']};text-transform:uppercase;
        ">v{PLATFORM_VERSION}</div>
        <div style="
            padding:3px 10px;border-radius:5px;
            background:rgba(255,255,255,0.04);border:1px solid {C['border2']};
            font-size:9px;color:{C['text3']};letter-spacing:0.08em;
            font-family:{C['mono']};
        ">IDX · MNM</div>
    </div>
</div>

<style>
@keyframes blink {{0%,100%{{opacity:1}}50%{{opacity:0.3}}}}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PART 6: ERROR LOGGER
# ─────────────────────────────────────────────
_DEBUG_MODE = False

def _log_err(context: str, err: Exception, extra: str = "") -> None:
    try:
        msg = f"[{context}] {type(err).__name__}: {str(err)[:120]}"
        if extra: msg += f" | {extra}"
        log = st.session_state.setdefault("_err_log", [])
        if len(log) >= 100: log.pop(0)
        log.append({"ts": time.time(), "msg": msg})
        if _DEBUG_MODE: print(f"MOONSIDE ERR: {msg}")
    except Exception:
        pass


# ─────────────────────────────────────────────
# PART 7: SESSION STATE INITIALIZER
# ─────────────────────────────────────────────
def _init_session():
    defaults = {
        "active_module":    "overview",
        "selected_ticker":  "BBCA",
        "ai_messages":      [],
        "plan_cache":       {},
        "broker_cache":     {},
        "price_cache":      {},
        "_err_log":         [],
        "_idxdb_init_done": False,
        "_groq_key_idx":    0,
        "_tab_locks":       {},
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ─────────────────────────────────────────────
# PART 8: SECRETS & API KEY MANAGER
# ─────────────────────────────────────────────
def _get_secret(key: str, fallback=None):
    try:
        return st.secrets[key]
    except Exception:
        return os.environ.get(key, fallback)

def _get_groq_key() -> Optional[str]:
    """Rotasi Groq API key (dukung groq_key_1 ... groq_key_20)."""
    keys = []
    for i in range(1, 21):
        k = _get_secret(f"groq_key_{i}") or _get_secret("groq_api_key")
        if k and k not in keys:
            keys.append(k)
    if not keys:
        return None
    idx = st.session_state.get("_groq_key_idx", 0) % len(keys)
    return keys[idx]

def _rotate_groq_key():
    keys = []
    for i in range(1, 21):
        k = _get_secret(f"groq_key_{i}") or _get_secret("groq_api_key")
        if k and k not in keys:
            keys.append(k)
    if keys:
        st.session_state["_groq_key_idx"] = (
            st.session_state.get("_groq_key_idx", 0) + 1
        ) % len(keys)

def _get_gemini_key() -> Optional[str]:
    for i in range(1, 6):
        k = _get_secret(f"gemini_key_{i}") or _get_secret("gemini_api_key")
        if k: return k
    return None

def _get_fmp_key() -> Optional[str]:
    return _get_secret("fmp_key") or "6ckg4EdDYUqKkkpPK4Weo4b9PbKD6IUK"


# ─────────────────────────────────────────────
# PART 9: IDX DATABASE PIPELINE
# (ported from SIGMA v87 with clean architecture)
# ─────────────────────────────────────────────

_DATA_DIR = os.path.join(os.path.expanduser("~"), ".moonside_data")
os.makedirs(_DATA_DIR, exist_ok=True)
_DB_PATH  = os.path.join(_DATA_DIR, "idx_daily.db")

_IDX_HEADERS = {
    "User-Agent":       "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer":          "https://www.idx.co.id/id/data-pasar/ringkasan-perdagangan/ringkasan-saham/",
    "Accept":           "application/json, text/plain, */*",
    "Accept-Language":  "id-ID,id;q=0.9,en-US;q=0.8",
    "Origin":           "https://www.idx.co.id",
    "X-Requested-With": "XMLHttpRequest",
}
_IDX_SUMMARY_URL = "https://www.idx.co.id/primary/TradingSummary/GetStockSummary"


def _db_connect() -> sqlite3.Connection:
    conn = sqlite3.connect(_DB_PATH, timeout=30, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def _db_init():
    if st.session_state.get("_idxdb_init_done"):
        return
    conn = _db_connect()
    try:
        conn.executescript("""
            PRAGMA journal_mode = WAL;
            PRAGMA synchronous  = NORMAL;
            CREATE TABLE IF NOT EXISTS stock_daily (
                date TEXT NOT NULL, ticker TEXT NOT NULL, name TEXT,
                prev REAL, open REAL, high REAL, low REAL, close REAL,
                change REAL, change_pct REAL, volume INTEGER, value REAL,
                frequency INTEGER, index_individual REAL,
                offer REAL, offer_volume INTEGER, bid REAL, bid_volume INTEGER,
                listed_shares INTEGER, tradeable_shares INTEGER,
                weight_for_index REAL,
                foreign_sell INTEGER, foreign_buy INTEGER, foreign_net INTEGER,
                non_reg_volume INTEGER, non_reg_value REAL, non_reg_frequency INTEGER,
                fetched_at TEXT,
                PRIMARY KEY (date, ticker)
            );
            CREATE INDEX IF NOT EXISTS idx_sd_date   ON stock_daily (date);
            CREATE INDEX IF NOT EXISTS idx_sd_ticker ON stock_daily (date, ticker);
            CREATE TABLE IF NOT EXISTS fetch_log (
                date TEXT PRIMARY KEY, status TEXT, rows_saved INTEGER,
                duration_s REAL, fetched_at TEXT
            );
        """)
        conn.commit()
    finally:
        conn.close()
    st.session_state["_idxdb_init_done"] = True


def _sf(v) -> Optional[float]:
    try:
        if v is None or v in ("", "-", "—"): return None
        return float(str(v).replace(",", "").strip())
    except Exception:
        return None

def _si(v) -> Optional[int]:
    try:
        if v is None or v in ("", "-", "—"): return None
        return int(float(str(v).replace(",", "").strip()))
    except Exception:
        return None


def _parse_idx_row(raw: dict, trade_date: str) -> dict:
    prev  = _sf(raw.get("Prev"))
    close = _sf(raw.get("Close"))
    chg   = _sf(raw.get("Change"))
    chg_pct = round(chg / prev * 100, 2) if (prev and prev != 0 and chg is not None) else None
    fb = _si(raw.get("ForeignBuy"))
    fs = _si(raw.get("ForeignSell"))
    return {
        "date": trade_date, "ticker": str(raw.get("StockCode", "")).strip().upper(),
        "name": str(raw.get("Name", "")).strip(),
        "prev": prev, "open": _sf(raw.get("OpenPrice")),
        "high": _sf(raw.get("High")), "low": _sf(raw.get("Low")),
        "close": close, "change": chg, "change_pct": chg_pct,
        "volume": _si(raw.get("Volume")), "value": _sf(raw.get("Value")),
        "frequency": _si(raw.get("Frequency")),
        "index_individual": _sf(raw.get("IndexIndividual")),
        "offer": _sf(raw.get("Offer")), "offer_volume": _si(raw.get("OfferVolume")),
        "bid": _sf(raw.get("Bid")), "bid_volume": _si(raw.get("BidVolume")),
        "listed_shares": _si(raw.get("ListedShares")),
        "tradeable_shares": _si(raw.get("TradeableShares")),
        "weight_for_index": _sf(raw.get("WeightForIndex")),
        "foreign_sell": fs, "foreign_buy": fb,
        "foreign_net": (fb - fs) if (fb is not None and fs is not None) else None,
        "non_reg_volume": _si(raw.get("NonRegularVolume")),
        "non_reg_value": _sf(raw.get("NonRegularValue")),
        "non_reg_frequency": _si(raw.get("NonRegularFrequency")),
        "fetched_at": datetime.utcnow().isoformat(),
    }


def _is_trading_day(d: date) -> bool:
    return d.weekday() < 5 and d.strftime("%Y-%m-%d") not in _IDX_HOLIDAYS


def db_fetch_date(trade_date: str, force: bool = False) -> dict:
    """Fetch satu tanggal dari IDX API → simpan ke SQLite."""
    if not force:
        conn = _db_connect()
        try:
            row = conn.execute(
                "SELECT rows_saved FROM fetch_log WHERE date=? AND status='ok'",
                (trade_date,)
            ).fetchone()
            if row:
                return {"status": "skip", "rows": row["rows_saved"],
                        "message": f"Cache: {row['rows_saved']} saham"}
        finally:
            conn.close()

    t_start = time.time()
    all_rows, start, length = [], 0, 100

    try:
        while True:
            resp = requests.get(
                _IDX_SUMMARY_URL,
                params={"language": "id", "start": start, "length": length, "date": trade_date},
                headers=_IDX_HEADERS, timeout=15
            )
            resp.raise_for_status()
            data    = resp.json()
            records = data.get("data") or data.get("Data") or []
            if not records: break
            for raw in records:
                parsed = _parse_idx_row(raw, trade_date)
                if parsed["ticker"]: all_rows.append(parsed)
            total = data.get("recordsTotal", 0)
            start += length
            if start >= total: break
            time.sleep(0.25)
    except Exception as e:
        return {"status": "error", "rows": 0, "message": str(e)}

    if not all_rows:
        return {"status": "error", "rows": 0, "message": "Tidak ada data (hari libur?)"}

    conn = _db_connect()
    try:
        conn.executemany("""
            INSERT OR REPLACE INTO stock_daily
            (date,ticker,name,prev,open,high,low,close,change,change_pct,
             volume,value,frequency,index_individual,offer,offer_volume,
             bid,bid_volume,listed_shares,tradeable_shares,weight_for_index,
             foreign_sell,foreign_buy,foreign_net,
             non_reg_volume,non_reg_value,non_reg_frequency,fetched_at)
            VALUES
            (:date,:ticker,:name,:prev,:open,:high,:low,:close,:change,:change_pct,
             :volume,:value,:frequency,:index_individual,:offer,:offer_volume,
             :bid,:bid_volume,:listed_shares,:tradeable_shares,:weight_for_index,
             :foreign_sell,:foreign_buy,:foreign_net,
             :non_reg_volume,:non_reg_value,:non_reg_frequency,:fetched_at)
        """, all_rows)
        conn.execute(
            "INSERT OR REPLACE INTO fetch_log (date,status,rows_saved,duration_s,fetched_at) VALUES (?,?,?,?,?)",
            (trade_date, "ok", len(all_rows), round(time.time()-t_start,2), datetime.utcnow().isoformat())
        )
        conn.commit()
    finally:
        conn.close()

    return {"status": "ok", "rows": len(all_rows),
            "message": f"{len(all_rows)} saham ({round(time.time()-t_start,1)}s)"}


def db_get_latest_date() -> Optional[str]:
    try:
        conn = _db_connect()
        row  = conn.execute("SELECT MAX(date) FROM stock_daily").fetchone()
        conn.close()
        return row[0] if row else None
    except Exception:
        return None


def db_get_snapshot(date_str: str = None, top_n: int = 200) -> list:
    """Ambil snapshot harian semua saham → sorted by value."""
    if not date_str: date_str = db_get_latest_date()
    if not date_str: return []
    try:
        conn = _db_connect()
        rows = conn.execute(
            "SELECT * FROM stock_daily WHERE date=? ORDER BY value DESC LIMIT ?",
            (date_str, top_n)
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception:
        return []


def db_get_ticker_history(ticker: str, days: int = 30) -> list:
    """Ambil historis satu ticker dari SQLite."""
    try:
        conn = _db_connect()
        rows = conn.execute(
            "SELECT * FROM stock_daily WHERE ticker=? ORDER BY date DESC LIMIT ?",
            (ticker.upper(), days)
        ).fetchall()
        conn.close()
        return [dict(r) for r in reversed(rows)]
    except Exception:
        return []


def db_get_foreign_flow(date_str: str = None, top_n: int = 20) -> dict:
    if not date_str: date_str = db_get_latest_date()
    if not date_str: return {"top_buy": [], "top_sell": []}
    try:
        conn = _db_connect()
        top_buy = [dict(r) for r in conn.execute(
            "SELECT ticker,name,close,foreign_net,foreign_buy,foreign_sell FROM stock_daily "
            "WHERE date=? AND foreign_net>0 ORDER BY foreign_net DESC LIMIT ?",
            (date_str, top_n)
        ).fetchall()]
        top_sell = [dict(r) for r in conn.execute(
            "SELECT ticker,name,close,foreign_net,foreign_buy,foreign_sell FROM stock_daily "
            "WHERE date=? AND foreign_net<0 ORDER BY foreign_net ASC LIMIT ?",
            (date_str, top_n)
        ).fetchall()]
        conn.close()
        return {"top_buy": top_buy, "top_sell": top_sell, "date": date_str}
    except Exception:
        return {"top_buy": [], "top_sell": [], "date": date_str}


def db_get_volume_spike(days: int = 5, top_n: int = 30) -> list:
    """Deteksi volume spike hari ini vs rata-rata N hari."""
    try:
        latest = db_get_latest_date()
        if not latest: return []
        conn  = _db_connect()
        tickers = [r[0] for r in conn.execute(
            "SELECT DISTINCT ticker FROM stock_daily ORDER BY ticker"
        ).fetchall()]
        spikes = []
        for tk in tickers[:300]:
            rows = conn.execute(
                "SELECT date,volume,close,change_pct FROM stock_daily "
                "WHERE ticker=? ORDER BY date DESC LIMIT ?",
                (tk, days + 1)
            ).fetchall()
            if len(rows) < 2: continue
            today_vol = rows[0]["volume"] or 0
            avg_vol   = sum(r["volume"] or 0 for r in rows[1:]) / max(len(rows)-1, 1)
            if avg_vol < 50000 or today_vol < 100000: continue
            ratio = today_vol / avg_vol if avg_vol > 0 else 1
            if ratio >= 1.5:
                spikes.append({
                    "ticker": tk, "volume": today_vol, "avg_volume": avg_vol,
                    "spike_ratio": round(ratio, 2),
                    "close": rows[0]["close"], "change_pct": rows[0]["change_pct"],
                })
        conn.close()
        spikes.sort(key=lambda x: x["spike_ratio"], reverse=True)
        return spikes[:top_n]
    except Exception:
        return []


def db_stats() -> dict:
    try:
        conn = _db_connect()
        total_rows = conn.execute("SELECT COUNT(*) FROM stock_daily").fetchone()[0]
        total_days = conn.execute("SELECT COUNT(DISTINCT date) FROM stock_daily").fetchone()[0]
        oldest     = conn.execute("SELECT MIN(date) FROM stock_daily").fetchone()[0]
        newest     = conn.execute("SELECT MAX(date) FROM stock_daily").fetchone()[0]
        db_mb      = round(os.path.getsize(_DB_PATH)/1024/1024, 2) if os.path.exists(_DB_PATH) else 0
        conn.close()
        return {"total_rows": total_rows, "total_days": total_days,
                "oldest": oldest, "newest": newest, "db_mb": db_mb}
    except Exception:
        return {}


def db_auto_fetch_today() -> dict:
    """Fetch hari ini otomatis jika belum ada di DB."""
    today = date.today()
    if not _is_trading_day(today):
        return {"status": "skip", "message": "Hari libur / weekend"}
    return db_fetch_date(today.strftime("%Y-%m-%d"))


# ─────────────────────────────────────────────
# PART 10: PRICE FETCHER — Multi-layer
# yfinance → FMP → IDX API → DB fallback
# ─────────────────────────────────────────────
@st.cache_data(ttl=CACHE_CONFIG["price_live"], show_spinner=False)
def fetch_price(ticker: str) -> dict:
    """Fetch harga live untuk satu ticker IDX."""
    tk = ticker.upper().replace(".JK", "")
    result = {"ticker": tk, "price": None, "prev": None, "chg": None,
              "chg_pct": None, "volume": None, "high": None, "low": None,
              "source": "none"}
    try:
        if HAS_YF:
            yf_tk = tk + ".JK"
            t  = yf.Ticker(yf_tk)
            fi = t.fast_info
            p  = getattr(fi, "last_price", None)
            if p and p > 0:
                prev    = getattr(fi, "previous_close", p)
                chg_pct = round((p - prev) / prev * 100, 2) if prev else 0
                result.update({
                    "price": round(p), "prev": round(prev),
                    "chg": round(p - prev), "chg_pct": chg_pct,
                    "volume": getattr(fi, "three_month_average_volume", None),
                    "high": getattr(fi, "day_high", p),
                    "low":  getattr(fi, "day_low", p),
                    "source": "yfinance",
                })
                return result
    except Exception as e:
        _log_err("fetch_price_yf", e, tk)

    # Fallback: IDX DB snapshot
    try:
        hist = db_get_ticker_history(tk, days=2)
        if hist:
            r = hist[-1]
            prev  = hist[-2]["close"] if len(hist) > 1 else r["prev"]
            price = r["close"]
            result.update({
                "price": round(price) if price else None,
                "prev":  round(prev) if prev else None,
                "chg":   r.get("change"),
                "chg_pct": r.get("change_pct"),
                "volume":  r.get("volume"),
                "high":    r.get("high"),
                "low":     r.get("low"),
                "source":  "idx_db",
            })
    except Exception as e:
        _log_err("fetch_price_db", e, tk)

    return result


@st.cache_data(ttl=CACHE_CONFIG["price_live"], show_spinner=False)
def fetch_prices_batch(tickers: list) -> dict:
    """Batch fetch harga untuk list ticker."""
    results = {}
    if not HAS_YF:
        return results
    try:
        from concurrent.futures import ThreadPoolExecutor, as_completed
        def _fetch_one(tk):
            return tk, fetch_price(tk)
        with ThreadPoolExecutor(max_workers=8) as ex:
            futures = {ex.submit(_fetch_one, tk): tk for tk in tickers}
            for f in as_completed(futures, timeout=20):
                try:
                    tk, data = f.result()
                    results[tk] = data
                except Exception:
                    pass
    except Exception as e:
        _log_err("fetch_prices_batch", e)
    return results


def get_free_float(ticker: str) -> Optional[float]:
    tk = ticker.upper().replace(".JK", "")
    if tk in _FF_DB:
        return _FF_DB[tk]
    try:
        conn = _db_connect()
        row  = conn.execute(
            "SELECT listed_shares, tradeable_shares FROM stock_daily "
            "WHERE ticker=? AND listed_shares>0 ORDER BY date DESC LIMIT 1",
            (tk,)
        ).fetchone()
        conn.close()
        if row and row["listed_shares"] and row["tradeable_shares"]:
            ff = round(row["tradeable_shares"] / row["listed_shares"] * 100, 2)
            if 0 < ff <= 100: return ff
    except Exception:
        pass
    return None


# ─────────────────────────────────────────────
# PART 11: AI ENGINE — Groq + Gemini
# ─────────────────────────────────────────────
_SYSTEM_PROMPT_MNM = """Kamu adalah MOONSIDE AI, asisten analis pasar modal institutional grade.
Kamu menggunakan MnM Strategy+ (Market n Mocha) sebagai framework analisis utama.

FRAMEWORK MnM STRATEGY+:
- IFVG (Imbalance Fair Value Gap): zona harga tidak efisien, target fill
- FVG (Fair Value Gap): gap bullish/bearish, diisi sebelum lanjut
- Order Block (OB): zona akumulasi/distribusi institusi
- Supply & Demand Zone: support/resistance institusional
- EMA: 13 (fast), 21 (pullback), 50 (mid-trend), 100/200 (major trend)
- Confluence: semakin banyak komponen overlap = zona lebih kuat
- IDX = LONG ONLY (tidak ada short selling retail)

BANDARMOLOGI IDX:
- Banyak broker beli, sedikit broker jual = DISTRIBUSI (bandar jual ke retail)
- Sedikit broker beli, banyak broker jual = AKUMULASI (smart money beli)
- Ini counter-intuitive tapi valid untuk IDX

ATURAN RESPON:
- Gunakan Bahasa Indonesia yang profesional
- Berikan analisis konkret: entry, target, stoploss dengan angka spesifik
- Sebutkan sumber data jika relevan
- Format: bullet points untuk data, paragraf untuk analisis
- Selalu tambahkan disclaimer: "Bukan rekomendasi investasi, hanya edukasi"
"""

def _call_ai(prompt: str, system: str = None, max_tokens: int = 1200) -> str:
    """Call AI dengan fallback: Groq primary → Gemini → Groq backup."""
    if system is None:
        system = _SYSTEM_PROMPT_MNM

    # ── Try Groq ──────────────────────────────
    if HAS_GROQ:
        for model in ["llama-3.3-70b-versatile", "llama3-70b-8192"]:
            key = _get_groq_key()
            if not key: break
            try:
                client = Groq(api_key=key)
                resp   = client.chat.completions.create(
                    model=model,
                    messages=[{"role":"system","content":system},
                              {"role":"user","content":prompt}],
                    max_tokens=max_tokens, temperature=0.65,
                )
                return resp.choices[0].message.content or ""
            except Exception as e:
                _log_err("ai_groq", e, model)
                _rotate_groq_key()

    # ── Fallback: Gemini ──────────────────────
    if HAS_GENAI:
        key = _get_gemini_key()
        if key:
            for model in ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]:
                try:
                    genai.configure(api_key=key)
                    m    = genai.GenerativeModel(model, system_instruction=system)
                    resp = m.generate_content(prompt)
                    return resp.text or ""
                except Exception as e:
                    _log_err("ai_gemini", e, model)

    return "⚠️ AI engine tidak tersedia. Periksa konfigurasi API key di Secrets."


# ─────────────────────────────────────────────
# PART 12: HELPER UI COMPONENTS
# ─────────────────────────────────────────────
def _fmt_price(v) -> str:
    try: return f"Rp {int(v):,}".replace(",",".")
    except: return str(v) if v else "—"

def _fmt_num(v, suffix="") -> str:
    try:
        v = float(v)
        if abs(v) >= 1e12: return f"{v/1e12:.1f}T{suffix}"
        if abs(v) >= 1e9:  return f"{v/1e9:.1f}B{suffix}"
        if abs(v) >= 1e6:  return f"{v/1e6:.1f}M{suffix}"
        if abs(v) >= 1e3:  return f"{v/1e3:.1f}K{suffix}"
        return f"{v:.0f}{suffix}"
    except: return "—"

def _fmt_pct(v) -> str:
    try: return f"{float(v):+.2f}%"
    except: return "—"

def _pct_color(v) -> str:
    try:
        return C['green'] if float(v) >= 0 else C['red']
    except:
        return C['text3']

def _badge(label, color=None, bg=None) -> str:
    c  = color or C['text3']
    bg = bg or "rgba(255,255,255,0.05)"
    return (f"<span style='display:inline-block;padding:2px 8px;border-radius:4px;"
            f"background:{bg};color:{c};font-size:9.5px;font-weight:700;"
            f"letter-spacing:0.06em;font-family:{C['mono']};border:1px solid {c}33;'>"
            f"{label}</span>")

def _card_header(title: str, subtitle: str = "", badge: str = "") -> str:
    return f"""
<div style="display:flex;align-items:center;justify-content:space-between;
    margin-bottom:14px;">
    <div>
        <div style="font-size:13px;font-weight:600;color:{C['text']};
            letter-spacing:-0.01em;">{title}</div>
        {f'<div style="font-size:10px;color:{C["text3"]};font-family:{C["mono"]};margin-top:2px;">{subtitle}</div>' if subtitle else ''}
    </div>
    {badge}
</div>"""

def _section_divider(label: str = "") -> None:
    if label:
        st.markdown(f"""
<div style="display:flex;align-items:center;gap:12px;margin:24px 0 16px;">
    <div style="flex:1;height:1px;background:{C['border']};"></div>
    <div style="font-size:9px;letter-spacing:0.14em;text-transform:uppercase;
        color:{C['text3']};font-family:{C['mono']};font-weight:600;">{label}</div>
    <div style="flex:1;height:1px;background:{C['border']};"></div>
</div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"<hr style='border-top:1px solid {C['border']};margin:20px 0;'>",
                    unsafe_allow_html=True)

def _mini_sparkline(values: list, color: str = None, height: int = 40) -> str:
    """Render mini sparkline sebagai inline SVG."""
    if not values or len(values) < 2:
        return ""
    try:
        vs  = [float(v) for v in values if v is not None]
        if not vs or len(vs) < 2: return ""
        mn, mx = min(vs), max(vs)
        rng    = mx - mn or 1
        w, h   = 120, height
        pts    = []
        for i, v in enumerate(vs):
            x = i / (len(vs)-1) * w
            y = h - ((v - mn) / rng * (h-4) + 2)
            pts.append(f"{x:.1f},{y:.1f}")
        col = color or (C['green'] if vs[-1] >= vs[0] else C['red'])
        pts_str = " ".join(pts)
        return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
                f'style="width:100%;height:{h}px;">'
                f'<polyline points="{pts_str}" fill="none" stroke="{col}" '
                f'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'
                f'</svg>')
    except Exception:
        return ""


# ─────────────────────────────────────────────
# PART 13: MARKET OVERVIEW MODULE
# Fincept-style: multi-asset dashboard panel
# ─────────────────────────────────────────────
@st.cache_data(ttl=CACHE_CONFIG["price_live"], show_spinner=False)
def _fetch_market_indices() -> dict:
    """Fetch IHSG, LQ45, dan indeks global."""
    indices = {
        "IHSG":    {"yf": "^JKSE",   "label": "IHSG",       "cat": "IDX"},
        "LQ45":    {"yf": "^JKLQ45", "label": "LQ45",       "cat": "IDX"},
        "S&P500":  {"yf": "^GSPC",   "label": "S&P 500",    "cat": "GLOBAL"},
        "NASDAQ":  {"yf": "^IXIC",   "label": "NASDAQ",     "cat": "GLOBAL"},
        "GOLD":    {"yf": "GC=F",    "label": "Gold (USD)",  "cat": "COMMODITY"},
        "CRUDE":   {"yf": "CL=F",    "label": "Crude Oil",   "cat": "COMMODITY"},
        "USDIDR":  {"yf": "IDR=X",   "label": "USD/IDR",     "cat": "FX"},
        "BTC":     {"yf": "BTC-USD", "label": "Bitcoin",     "cat": "CRYPTO"},
    }
    results = {}
    if not HAS_YF:
        return results
    for key, meta in indices.items():
        try:
            t  = yf.Ticker(meta["yf"])
            fi = t.fast_info
            p  = getattr(fi, "last_price", None)
            if p:
                prev    = getattr(fi, "previous_close", p) or p
                chg_pct = round((p - prev) / prev * 100, 2) if prev else 0
                results[key] = {**meta, "price": p, "chg_pct": chg_pct,
                                "chg": round(p - prev, 2)}
        except Exception:
            pass
    return results


def render_overview():
    """Tab 1: Market Overview — Fincept-style multi-asset dashboard."""
    st.markdown(f"""
<div style="padding:24px 28px 16px;">
    <div style="font-size:22px;font-weight:700;letter-spacing:-0.03em;color:{C['text']};">
        Market Overview
    </div>
    <div style="font-size:12px;color:{C['text3']};font-family:{C['mono']};margin-top:4px;">
        IDX · Global · Forex · Crypto — real-time snapshot
    </div>
</div>
""", unsafe_allow_html=True)

    # ── Fetch indices ─────────────────────────
    with st.spinner("Memuat data pasar..."):
        indices = _fetch_market_indices()

    # ── Market Status Banner ──────────────────
    latest_date = db_get_latest_date()
    snap        = db_get_snapshot(top_n=50) if latest_date else []
    tot_val     = sum(r.get("value", 0) or 0 for r in snap)
    adv         = sum(1 for r in snap if (r.get("change_pct") or 0) > 0)
    dec         = sum(1 for r in snap if (r.get("change_pct") or 0) < 0)

    st.markdown(f"""
<div style="margin:0 28px 20px;padding:16px 20px;
    background:rgba(255,255,255,0.02);border:1px solid {C['border']};
    border-radius:12px;display:flex;gap:32px;flex-wrap:wrap;">
    <div>
        <div style="font-size:9px;letter-spacing:0.12em;text-transform:uppercase;
            color:{C['text3']};font-family:{C['mono']};">Tanggal Data</div>
        <div style="font-size:15px;font-weight:700;color:{C['text']};margin-top:4px;">
            {latest_date or "—"}
        </div>
    </div>
    <div>
        <div style="font-size:9px;letter-spacing:0.12em;text-transform:uppercase;
            color:{C['text3']};font-family:{C['mono']};">Total Nilai (Top 50)</div>
        <div style="font-size:15px;font-weight:700;color:{C['gold']};margin-top:4px;">
            {_fmt_num(tot_val, " IDR")}
        </div>
    </div>
    <div>
        <div style="font-size:9px;letter-spacing:0.12em;text-transform:uppercase;
            color:{C['text3']};font-family:{C['mono']};">Advance / Decline</div>
        <div style="font-size:15px;font-weight:700;margin-top:4px;">
            <span style="color:{C['green']};">{adv}</span>
            <span style="color:{C['text3']};font-size:11px;"> / </span>
            <span style="color:{C['red']};">{dec}</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

    # ── Indices Grid ──────────────────────────
    _section_divider("INDEKS GLOBAL")
    cols = st.columns(4)
    for i, (key, data) in enumerate(indices.items()):
        col = cols[i % 4]
        with col:
            p      = data.get("price", 0) or 0
            pct    = data.get("chg_pct", 0) or 0
            color  = _pct_color(pct)
            cat    = data.get("cat", "")
            cat_color = {"IDX": C['accent2'], "GLOBAL": C['blue'],
                         "FX": C['gold'], "CRYPTO": "#F7931A",
                         "COMMODITY": C['green']}.get(cat, C['text3'])
            st.markdown(f"""
<div style="background:rgba(255,255,255,0.022);border:1px solid {C['border']};
    border-radius:10px;padding:14px 16px;margin-bottom:10px;">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
        <div style="font-size:12px;font-weight:700;color:{C['text']};
            letter-spacing:0.03em;">{data['label']}</div>
        <span style="font-size:8.5px;padding:2px 6px;border-radius:3px;
            background:{cat_color}18;color:{cat_color};font-weight:700;
            font-family:{C['mono']};letter-spacing:0.06em;">{cat}</span>
    </div>
    <div style="font-size:20px;font-weight:700;letter-spacing:-0.03em;
        color:{C['text']};line-height:1;">{p:,.2f}</div>
    <div style="font-size:12px;font-weight:600;color:{color};margin-top:5px;">
        {_fmt_pct(pct)}
    </div>
</div>
""", unsafe_allow_html=True)

    # ── Top Movers from IDX DB ────────────────
    if snap:
        _section_divider("TOP MOVERS IDX")
        col1, col2 = st.columns(2)

        gainers = sorted(
            [r for r in snap if r.get("change_pct") and r.get("close", 0) >= 100],
            key=lambda x: x.get("change_pct", 0), reverse=True
        )[:10]
        losers  = sorted(
            [r for r in snap if r.get("change_pct")],
            key=lambda x: x.get("change_pct", 0)
        )[:10]

        with col1:
            st.markdown(f"<div style='font-size:10px;letter-spacing:0.1em;text-transform:uppercase;"
                        f"color:{C['green']};font-weight:700;font-family:{C['mono']};padding:0 4px 8px;'>"
                        f"▲ TOP GAINERS</div>", unsafe_allow_html=True)
            rows_html = ""
            for r in gainers:
                pct   = r.get("change_pct", 0) or 0
                close = r.get("close", 0) or 0
                val   = r.get("value", 0) or 0
                rows_html += f"""
<div style="display:flex;align-items:center;justify-content:space-between;
    padding:8px 12px;border-bottom:1px solid {C['border']};
    transition:background 0.1s;" onmouseover="this.style.background='rgba(255,255,255,0.02)'"
    onmouseout="this.style.background='transparent'">
    <div>
        <div style="font-size:12px;font-weight:700;color:{C['text']};
            letter-spacing:0.03em;">{r['ticker']}</div>
        <div style="font-size:9px;color:{C['text3']};font-family:{C['mono']};
            margin-top:1px;">{_fmt_num(val)} IDR</div>
    </div>
    <div style="text-align:right;">
        <div style="font-size:12px;font-weight:700;color:{C['text']};">
            {_fmt_price(close)}</div>
        <div style="font-size:10px;font-weight:700;color:{C['green']};margin-top:1px;">
            {_fmt_pct(pct)}</div>
    </div>
</div>"""
            st.markdown(f"""
<div style="background:rgba(255,255,255,0.018);border:1px solid {C['border']};
    border-radius:10px;overflow:hidden;">{rows_html}</div>
""", unsafe_allow_html=True)

        with col2:
            st.markdown(f"<div style='font-size:10px;letter-spacing:0.1em;text-transform:uppercase;"
                        f"color:{C['red']};font-weight:700;font-family:{C['mono']};padding:0 4px 8px;'>"
                        f"▼ TOP LOSERS</div>", unsafe_allow_html=True)
            rows_html = ""
            for r in losers:
                pct   = r.get("change_pct", 0) or 0
                close = r.get("close", 0) or 0
                val   = r.get("value", 0) or 0
                rows_html += f"""
<div style="display:flex;align-items:center;justify-content:space-between;
    padding:8px 12px;border-bottom:1px solid {C['border']};">
    <div>
        <div style="font-size:12px;font-weight:700;color:{C['text']};
            letter-spacing:0.03em;">{r['ticker']}</div>
        <div style="font-size:9px;color:{C['text3']};font-family:{C['mono']};
            margin-top:1px;">{_fmt_num(val)} IDR</div>
    </div>
    <div style="text-align:right;">
        <div style="font-size:12px;font-weight:700;color:{C['text']};">
            {_fmt_price(close)}</div>
        <div style="font-size:10px;font-weight:700;color:{C['red']};margin-top:1px;">
            {_fmt_pct(pct)}</div>
    </div>
</div>"""
            st.markdown(f"""
<div style="background:rgba(255,255,255,0.018);border:1px solid {C['border']};
    border-radius:10px;overflow:hidden;">{rows_html}</div>
""", unsafe_allow_html=True)

    # ── Volume Spike Alert ────────────────────
    _section_divider("VOLUME SPIKE ALERT")
    with st.spinner("Scanning volume..."):
        spikes = db_get_volume_spike(days=5, top_n=15)

    if spikes:
        spike_html = ""
        for s in spikes[:12]:
            ratio    = s.get("spike_ratio", 1)
            pct      = s.get("change_pct") or 0
            pct_col  = _pct_color(pct)
            ratio_c  = C['gold'] if ratio >= 5 else (C['accent2'] if ratio >= 2.5 else C['text2'])
            spike_html += f"""
<div style="display:flex;align-items:center;gap:12px;
    padding:8px 14px;border-bottom:1px solid {C['border']};">
    <div style="width:56px;font-size:12px;font-weight:700;
        color:{C['text']};letter-spacing:0.03em;">{s['ticker']}</div>
    <div style="flex:1;">
        <div style="width:{min(ratio/8*100, 100):.0f}%;height:6px;
            background:{ratio_c};border-radius:3px;opacity:0.7;
            transition:width 0.3s;"></div>
    </div>
    <div style="font-size:11px;font-weight:700;color:{ratio_c};
        font-family:{C['mono']};width:48px;text-align:right;">{ratio:.1f}x</div>
    <div style="font-size:11px;font-weight:700;color:{pct_col};
        width:52px;text-align:right;">{_fmt_pct(pct)}</div>
    <div style="font-size:10px;color:{C['text3']};font-family:{C['mono']};
        width:72px;text-align:right;">{_fmt_price(s.get('close'))}</div>
</div>"""
        st.markdown(f"""
<div style="background:rgba(255,255,255,0.018);border:1px solid {C['border']};
    border-radius:10px;overflow:hidden;">
    <div style="display:flex;gap:12px;padding:8px 14px 6px;
        border-bottom:1px solid {C['border']};">
        <div style="width:56px;font-size:9px;letter-spacing:0.1em;
            text-transform:uppercase;color:{C['text3']};font-family:{C['mono']};
            font-weight:600;">TICKER</div>
        <div style="flex:1;font-size:9px;letter-spacing:0.1em;text-transform:uppercase;
            color:{C['text3']};font-family:{C['mono']};font-weight:600;">SPIKE RATIO</div>
        <div style="width:48px;font-size:9px;letter-spacing:0.1em;text-transform:uppercase;
            color:{C['text3']};font-family:{C['mono']};text-align:right;font-weight:600;">RATIO</div>
        <div style="width:52px;font-size:9px;letter-spacing:0.1em;text-transform:uppercase;
            color:{C['text3']};font-family:{C['mono']};text-align:right;font-weight:600;">CHG%</div>
        <div style="width:72px;font-size:9px;letter-spacing:0.1em;text-transform:uppercase;
            color:{C['text3']};font-family:{C['mono']};text-align:right;font-weight:600;">CLOSE</div>
    </div>
    {spike_html}
</div>
""", unsafe_allow_html=True)
    else:
        st.info("Tidak ada data volume spike. Pastikan database IDX sudah diisi via tab Data Pipeline.")


# ─────────────────────────────────────────────
# PART 14: STOCK INSIGHT MODULE
# Fincept-style: deep-dive single ticker
# ─────────────────────────────────────────────
def render_stock_insight():
    st.markdown(f"""
<div style="padding:24px 28px 16px;">
    <div style="font-size:22px;font-weight:700;letter-spacing:-0.03em;color:{C['text']};">
        Stock Insight
    </div>
    <div style="font-size:12px;color:{C['text3']};font-family:{C['mono']};margin-top:4px;">
        Analisis mendalam per saham — teknikal, fundamental, bandarmologi
    </div>
</div>
""", unsafe_allow_html=True)

    # ── Ticker Input ──────────────────────────
    col_in, col_btn, col_ff = st.columns([2, 1, 2])
    with col_in:
        ticker = st.text_input(
            "Ticker", value=st.session_state.get("selected_ticker", "BBCA"),
            placeholder="BBCA, BBRI, TLKM...",
            key="insight_ticker_input",
            label_visibility="collapsed",
        ).upper().strip()
    with col_btn:
        analyze_clicked = st.button("ANALYZE", key="insight_analyze_btn", type="primary",
                                    use_container_width=True)
    with col_ff:
        ff = get_free_float(ticker)
        st.markdown(f"""
<div style="padding:8px 14px;background:rgba(255,255,255,0.02);border:1px solid {C['border']};
    border-radius:8px;font-family:{C['mono']};font-size:11px;color:{C['text2']};">
    Free Float: <b style="color:{C['accent2']};">{f"{ff:.1f}%" if ff else "—"}</b>
    &nbsp;|&nbsp; Source: {"IDX DB" if ff else "N/A"}
</div>""", unsafe_allow_html=True)

    if analyze_clicked or ticker:
        st.session_state["selected_ticker"] = ticker
        with st.spinner(f"Mengambil data {ticker}..."):
            price_data = fetch_price(ticker)
            hist       = db_get_ticker_history(ticker, days=30)

        p      = price_data.get("price")
        prev   = price_data.get("prev")
        pct    = price_data.get("chg_pct", 0) or 0
        chg    = price_data.get("chg", 0) or 0
        vol    = price_data.get("volume") or 0
        hi     = price_data.get("high")
        lo     = price_data.get("low")

        if p is None and hist:
            last  = hist[-1]
            p     = last.get("close")
            prev  = last.get("prev")
            pct   = last.get("change_pct", 0) or 0
            chg   = last.get("change", 0) or 0
            vol   = last.get("volume", 0) or 0
            hi    = last.get("high")
            lo    = last.get("low")

        # ── Price Header ──────────────────────
        pct_col = _pct_color(pct)
        src_label = price_data.get("source", "db").upper()
        st.markdown(f"""
<div style="margin:0 28px 20px;padding:20px 24px;
    background:rgba(255,255,255,0.022);border:1px solid {C['border']};
    border-radius:12px;">
    <div style="display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:16px;">
        <div>
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
                <div style="font-size:24px;font-weight:700;letter-spacing:0.04em;
                    color:{C['text']};">{ticker}</div>
                {_badge(src_label, C['accent2'])}
            </div>
            <div style="font-size:36px;font-weight:700;letter-spacing:-0.04em;
                color:{C['text']};line-height:1;">
                {_fmt_price(p)}
            </div>
            <div style="font-size:14px;font-weight:600;color:{pct_col};margin-top:6px;">
                {_fmt_pct(pct)} &nbsp; ({_fmt_price(chg)})
            </div>
        </div>
        <div style="display:flex;gap:24px;flex-wrap:wrap;">
            <div>
                <div style="font-size:9px;letter-spacing:0.1em;text-transform:uppercase;
                    color:{C['text3']};font-family:{C['mono']};">HIGH</div>
                <div style="font-size:16px;font-weight:700;color:{C['text']};margin-top:4px;">
                    {_fmt_price(hi)}</div>
            </div>
            <div>
                <div style="font-size:9px;letter-spacing:0.1em;text-transform:uppercase;
                    color:{C['text3']};font-family:{C['mono']};">LOW</div>
                <div style="font-size:16px;font-weight:700;color:{C['text']};margin-top:4px;">
                    {_fmt_price(lo)}</div>
            </div>
            <div>
                <div style="font-size:9px;letter-spacing:0.1em;text-transform:uppercase;
                    color:{C['text3']};font-family:{C['mono']};">FREE FLOAT</div>
                <div style="font-size:16px;font-weight:700;color:{C['accent2']};margin-top:4px;">
                    {f"{ff:.1f}%" if ff else "—"}</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

        # ── History Chart & Data ──────────────
        if hist:
            closes  = [r.get("close") or 0 for r in hist]
            volumes = [r.get("volume") or 0 for r in hist]
            dates   = [r.get("date", "")[-5:] for r in hist]  # MM-DD

            # Simple sparkline area chart
            if len(closes) >= 5:
                mn_c, mx_c = min(closes), max(closes)
                rng        = mx_c - mn_c or 1
                w, h_svg   = 800, 80
                pts = []
                for i, v in enumerate(closes):
                    x = i / (len(closes)-1) * w
                    y = h_svg - ((v - mn_c) / rng * (h_svg - 10) + 5)
                    pts.append(f"{x:.1f},{y:.1f}")
                area_pts = f"0,{h_svg} " + " ".join(pts) + f" {w},{h_svg}"
                line_col = C['green'] if closes[-1] >= closes[0] else C['red']
                line_pts = " ".join(pts)

                st.markdown(f"""
<div style="margin:0 28px 16px;padding:16px 20px;
    background:rgba(255,255,255,0.018);border:1px solid {C['border']};
    border-radius:12px;">
    <div style="font-size:10px;letter-spacing:0.1em;text-transform:uppercase;
        color:{C['text3']};font-family:{C['mono']};margin-bottom:10px;">
        PRICE HISTORY — {len(hist)} HARI TERAKHIR
    </div>
    <svg viewBox="0 0 {w} {h_svg}" xmlns="http://www.w3.org/2000/svg"
        style="width:100%;height:{h_svg}px;">
        <defs>
            <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="{line_col}" stop-opacity="0.18"/>
                <stop offset="100%" stop-color="{line_col}" stop-opacity="0.01"/>
            </linearGradient>
        </defs>
        <polygon points="{area_pts}" fill="url(#areaGrad)"/>
        <polyline points="{line_pts}" fill="none" stroke="{line_col}"
            stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    <div style="display:flex;justify-content:space-between;margin-top:6px;">
        <span style="font-size:9px;color:{C['text3']};font-family:{C['mono']};">{dates[0]}</span>
        <span style="font-size:9px;color:{C['text3']};font-family:{C['mono']};">{dates[-1]}</span>
    </div>
</div>
""", unsafe_allow_html=True)

            # Stats row
            avg_vol  = sum(volumes) / len(volumes) if volumes else 0
            chg_30d  = round((closes[-1] - closes[0]) / closes[0] * 100, 2) if closes[0] else 0
            max_c    = max(closes)
            min_c    = min(closes)

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("30D Change", f"{chg_30d:+.2f}%")
            c2.metric("30D High", _fmt_price(max_c))
            c3.metric("30D Low", _fmt_price(min_c))
            c4.metric("Avg Volume", _fmt_num(avg_vol))

        # ── AI Analysis ──────────────────────
        _section_divider("AI ANALYSIS — MNM STRATEGY+")
        if st.button(f"🤖 Generate AI Analysis untuk {ticker}", key="insight_ai_btn",
                     use_container_width=True):
            prompt = f"""Lakukan analisis lengkap untuk saham {ticker} (IDX/BEI).

Data tersedia:
- Harga terakhir: {_fmt_price(p)}
- Perubahan: {_fmt_pct(pct)}
- Free Float: {f"{ff:.1f}%" if ff else "tidak diketahui"}
- High: {_fmt_price(hi)} | Low: {_fmt_price(lo)}
- Data historis {len(hist)} hari tersedia

Berikan analisis mencakup:
1. Analisis teknikal (EMA, support/resistance, tren)
2. Interpretasi bandarmologi (jika ada sinyal akumulasi/distribusi)
3. Setup MnM Strategy+ yang terlihat (OB, FVG, IFVG)
4. Rekomendasi entry, target (TP1/TP2), dan stoploss
5. Risk/Reward ratio
6. Outlook jangka pendek (1-5 hari)

Tambahkan disclaimer standar di akhir."""

            with st.spinner("MOONSIDE AI menganalisis..."):
                analysis = _call_ai(prompt)
            st.markdown(f"""
<div style="padding:20px 24px;background:rgba(124,58,237,0.06);
    border:1px solid rgba(124,58,237,0.18);border-radius:12px;
    font-size:13.5px;line-height:1.75;color:{C['text2']};">
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:14px;">
        <div style="width:7px;height:7px;border-radius:50%;background:{C['accent']};
            box-shadow:0 0 10px rgba(124,58,237,0.7);animation:blink 2s infinite;"></div>
        <span style="font-size:9px;letter-spacing:0.14em;text-transform:uppercase;
            color:{C['accent2']};font-weight:700;font-family:{C['mono']};">
            MOONSIDE AI · MNM STRATEGY+</span>
    </div>
    {analysis.replace(chr(10), '<br>')}
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PART 15: FOREIGN FLOW MODULE
# ─────────────────────────────────────────────
def render_foreign_flow():
    st.markdown(f"""
<div style="padding:24px 28px 16px;">
    <div style="font-size:22px;font-weight:700;letter-spacing:-0.03em;color:{C['text']};">
        Foreign Flow
    </div>
    <div style="font-size:12px;color:{C['text3']};font-family:{C['mono']};margin-top:4px;">
        Net foreign buy/sell — data real IDX pipeline
    </div>
</div>
""", unsafe_allow_html=True)

    flow_data = db_get_foreign_flow()
    date_str  = flow_data.get("date", "—")

    st.markdown(f"""
<div style="margin:0 28px 20px;padding:10px 18px;
    background:rgba(0,122,255,0.05);border:1px solid rgba(0,122,255,0.18);
    border-radius:8px;font-size:11px;color:{C['blue']};font-family:{C['mono']};">
    📅 Data tanggal: <b>{date_str}</b> &nbsp;|&nbsp; Source: IDX Daily Pipeline
</div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    def _flow_table(data: list, is_buy: bool) -> str:
        color = C['green'] if is_buy else C['red']
        label = "NET FOREIGN BUY" if is_buy else "NET FOREIGN SELL"
        rows  = ""
        for r in data[:15]:
            net   = r.get("foreign_net", 0) or 0
            close = r.get("close", 0) or 0
            rows += f"""
<div style="display:flex;align-items:center;justify-content:space-between;
    padding:7px 14px;border-bottom:1px solid {C['border']};">
    <div style="font-size:12px;font-weight:700;color:{C['text']};
        letter-spacing:0.03em;width:64px;">{r['ticker']}</div>
    <div style="flex:1;margin:0 10px;">
        <div style="width:{min(abs(net)/max(abs(d.get('foreign_net',1)) for d in data)*100, 100):.0f}%;
            height:5px;background:{color};border-radius:3px;opacity:0.65;"></div>
    </div>
    <div style="font-size:11px;font-weight:700;color:{color};
        font-family:{C['mono']};width:80px;text-align:right;">
        {_fmt_num(abs(net))}</div>
    <div style="font-size:10px;color:{C['text3']};font-family:{C['mono']};
        width:68px;text-align:right;">{_fmt_price(close)}</div>
</div>"""
        return f"""
<div style="font-size:10px;letter-spacing:0.1em;text-transform:uppercase;
    color:{color};font-weight:700;font-family:{C['mono']};padding:0 4px 8px;">{label}</div>
<div style="background:rgba(255,255,255,0.018);border:1px solid {C['border']};
    border-radius:10px;overflow:hidden;">{rows if rows else
    f'<div style="padding:20px;text-align:center;color:{C["text3"]};">Tidak ada data</div>'}
</div>"""

    with col1:
        if flow_data.get("top_buy"):
            st.markdown(_flow_table(flow_data["top_buy"], True), unsafe_allow_html=True)
        else:
            st.info("Tidak ada data. Isi database via tab Data Pipeline.")

    with col2:
        if flow_data.get("top_sell"):
            st.markdown(_flow_table(flow_data["top_sell"], False), unsafe_allow_html=True)
        else:
            st.info("Tidak ada data. Isi database via tab Data Pipeline.")

    # ── AI Interpretation ─────────────────────
    _section_divider("AI INTERPRETATION")
    if st.button("🤖 Interpretasi AI Foreign Flow", key="ff_ai_btn", use_container_width=True):
        top_buy  = [r["ticker"] for r in flow_data.get("top_buy", [])[:5]]
        top_sell = [r["ticker"] for r in flow_data.get("top_sell", [])[:5]]
        prompt   = f"""Interpretasi data foreign flow IDX tanggal {date_str}:

Top Net Foreign BUY: {', '.join(top_buy) if top_buy else 'tidak ada data'}
Top Net Foreign SELL: {', '.join(top_sell) if top_sell else 'tidak ada data'}

Berikan analisis:
1. Sentimen asing secara keseluruhan (risk-on/risk-off?)
2. Sektor apa yang diminati vs dijual asing?
3. Saham mana yang paling menarik perhatian dan mengapa?
4. Implikasi untuk pasar IDX ke depan
5. Korelasi dengan kondisi global (USD/IDR, BI Rate, Fed)

Gunakan konteks bandarmologi IDX: net foreign buy bisa jadi tanda distribusi ke retail jika bersamaan dengan broker sell besar."""

        with st.spinner("Menganalisis foreign flow..."):
            analysis = _call_ai(prompt)
        st.markdown(f"""
<div style="padding:20px 24px;background:rgba(0,122,255,0.06);
    border:1px solid rgba(0,122,255,0.2);border-radius:12px;
    font-size:13.5px;line-height:1.75;color:{C['text2']};">
    {analysis.replace(chr(10), '<br>')}
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PART 16: AI RESEARCH CHAT MODULE
# Fincept-style: interactive AI research console
# ─────────────────────────────────────────────
def render_ai_research():
    st.markdown(f"""
<div style="padding:24px 28px 16px;">
    <div style="font-size:22px;font-weight:700;letter-spacing:-0.03em;color:{C['text']};">
        AI Research
    </div>
    <div style="font-size:12px;color:{C['text3']};font-family:{C['mono']};margin-top:4px;">
        MOONSIDE AI · MnM Strategy+ · IDX-focused analysis engine
    </div>
</div>
""", unsafe_allow_html=True)

    # ── Quick Prompts (Fincept-style command palette) ──
    quick_prompts = [
        "Analisis IHSG hari ini dan outlook minggu ini",
        "Jelaskan konsep bandarmologi IDX dan cara membacanya",
        "Apa itu Order Block dan bagaimana cara entry yang benar?",
        "Sektor apa yang menarik di IDX saat ini?",
        "Jelaskan perbedaan IFVG dan FVG dalam MnM Strategy+",
        "Bagaimana membaca volume spike untuk timing entry?",
    ]

    st.markdown(f"""
<div style="margin:0 28px 16px;">
    <div style="font-size:9px;letter-spacing:0.12em;text-transform:uppercase;
        color:{C['text3']};font-family:{C['mono']};margin-bottom:10px;">
        QUICK RESEARCH PROMPTS</div>
    <div style="display:flex;flex-wrap:wrap;gap:6px;">
""" + "".join(f"""
        <div style="padding:5px 12px;background:rgba(124,58,237,0.07);
            border:1px solid rgba(124,58,237,0.18);border-radius:20px;
            font-size:11px;color:#C4B5FD;cursor:pointer;font-weight:500;
            transition:all 0.15s;" onclick="document.querySelector('[data-testid=stTextArea] textarea').value=`{p.replace('`','')}`">
            {p}</div>
""" for p in quick_prompts) + """
    </div>
</div>
""", unsafe_allow_html=True)

    # ── Chat History ──────────────────────────
    msgs = st.session_state.get("ai_messages", [])
    if msgs:
        for msg in msgs[-10:]:
            role  = msg.get("role", "user")
            color = C['accent2'] if role == "assistant" else C['text']
            bg    = "rgba(124,58,237,0.06)" if role == "assistant" else "rgba(255,255,255,0.03)"
            lbl   = "MOONSIDE AI" if role == "assistant" else "YOU"
            st.markdown(f"""
<div style="margin:0 28px 10px;padding:14px 18px;background:{bg};
    border:1px solid {C['border']};border-radius:10px;">
    <div style="font-size:9px;letter-spacing:0.12em;text-transform:uppercase;
        color:{color};font-weight:700;font-family:{C['mono']};margin-bottom:8px;">
        {lbl}</div>
    <div style="font-size:13.5px;line-height:1.7;color:{C['text2']};">
        {msg['content'].replace(chr(10), '<br>')}
    </div>
</div>
""", unsafe_allow_html=True)

    # ── Input Area ────────────────────────────
    st.markdown("<div style='padding:0 28px;'>", unsafe_allow_html=True)
    user_input = st.text_area(
        "Research Query",
        placeholder="Tanyakan analisis pasar, saham, strategi trading, atau ekonomi makro...",
        height=100,
        key="ai_chat_input",
        label_visibility="collapsed",
    )
    col_send, col_clear = st.columns([3, 1])
    with col_send:
        send_clicked = st.button("KIRIM ↑", key="ai_send_btn", type="primary",
                                 use_container_width=True)
    with col_clear:
        if st.button("CLEAR", key="ai_clear_btn", use_container_width=True):
            st.session_state["ai_messages"] = []
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    if send_clicked and user_input.strip():
        msgs = st.session_state.get("ai_messages", [])
        msgs.append({"role": "user", "content": user_input.strip()})

        # Build context dari history (max 6 turns)
        context_msgs = [{"role": "user", "content": _SYSTEM_PROMPT_MNM}]
        for m in msgs[-6:]:
            context_msgs.append(m)

        with st.spinner("MOONSIDE AI memproses..."):
            response = _call_ai(user_input.strip())

        msgs.append({"role": "assistant", "content": response})
        st.session_state["ai_messages"] = msgs
        st.rerun()


# ─────────────────────────────────────────────
# PART 17: SCREENER MODULE
# Fincept-style: filterable stock screener
# ─────────────────────────────────────────────
def render_screener():
    st.markdown(f"""
<div style="padding:24px 28px 16px;">
    <div style="font-size:22px;font-weight:700;letter-spacing:-0.03em;color:{C['text']};">
        Stock Screener
    </div>
    <div style="font-size:12px;color:{C['text3']};font-family:{C['mono']};margin-top:4px;">
        Filter saham IDX berdasarkan volume, nilai, perubahan harga, dan foreign flow
    </div>
</div>
""", unsafe_allow_html=True)

    # ── Filter Controls ───────────────────────
    with st.expander("⚙️ Filter Screener", expanded=True):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            min_val = st.number_input("Min Nilai (Miliar)", min_value=0.0,
                                      max_value=1000.0, value=1.0, step=0.5,
                                      key="scr_min_val")
        with c2:
            min_freq = st.number_input("Min Frekuensi", min_value=0,
                                       max_value=100000, value=100, step=50,
                                       key="scr_min_freq")
        with c3:
            min_chg = st.number_input("Min Chg% (hari ini)", min_value=-20.0,
                                      max_value=20.0, value=0.0, step=0.5,
                                      key="scr_min_chg")
        with c4:
            foreign_net_only = st.checkbox("Foreign Net Buy (+)", value=False,
                                           key="scr_foreign")

    if st.button("🔍 SCREEN SAHAM", key="scr_run_btn", type="primary", use_container_width=True):
        latest_date = db_get_latest_date()
        if not latest_date:
            st.error("Database IDX kosong. Gunakan tab Data Pipeline untuk mengisi data.")
            return

        try:
            conn = _db_connect()
            filters = ["date = ?"]
            params  = [latest_date]
            if min_val > 0:
                filters.append("value >= ?")
                params.append(min_val * 1e9)
            if min_freq > 0:
                filters.append("frequency >= ?")
                params.append(min_freq)
            if min_chg != 0:
                filters.append("change_pct >= ?")
                params.append(min_chg)
            if foreign_net_only:
                filters.append("foreign_net > 0")

            where = " AND ".join(filters)
            rows  = conn.execute(
                f"SELECT * FROM stock_daily WHERE {where} ORDER BY value DESC LIMIT 100",
                params
            ).fetchall()
            conn.close()

            results = [dict(r) for r in rows]
        except Exception as e:
            st.error(f"Error screener: {e}")
            return

        st.markdown(f"""
<div style="padding:8px 14px;background:rgba(52,199,89,0.06);
    border:1px solid rgba(52,199,89,0.18);border-radius:8px;
    font-size:11px;color:{C['green']};font-family:{C['mono']};margin-bottom:14px;">
    ✅ Ditemukan <b>{len(results)}</b> saham memenuhi kriteria · Tanggal: {latest_date}
</div>
""", unsafe_allow_html=True)

        if results:
            # ── Render table ──────────────────
            tbl_rows = ""
            for i, r in enumerate(results):
                pct   = r.get("change_pct", 0) or 0
                close = r.get("close", 0) or 0
                val   = r.get("value", 0) or 0
                freq  = r.get("frequency", 0) or 0
                fn    = r.get("foreign_net", 0) or 0
                fn_col= C['green'] if fn > 0 else (C['red'] if fn < 0 else C['text3'])
                row_bg= "rgba(255,255,255,0.01)" if i % 2 == 0 else "transparent"
                tbl_rows += f"""
<tr style="background:{row_bg};">
    <td style="padding:8px 12px;font-size:12px;font-weight:700;
        color:{C['text']};border-bottom:1px solid {C['border']};">{r['ticker']}</td>
    <td style="padding:8px 12px;font-size:11px;color:{C['text3']};
        border-bottom:1px solid {C['border']};font-family:{C['mono']};">
        {(r.get('name') or '')[:18]}</td>
    <td style="padding:8px 12px;font-size:12px;font-weight:600;color:{C['text']};
        text-align:right;border-bottom:1px solid {C['border']};
        font-family:{C['mono']};">{_fmt_price(close)}</td>
    <td style="padding:8px 12px;font-size:12px;font-weight:700;color:{_pct_color(pct)};
        text-align:right;border-bottom:1px solid {C['border']};
        font-family:{C['mono']};">{_fmt_pct(pct)}</td>
    <td style="padding:8px 12px;font-size:11px;color:{C['gold']};
        text-align:right;border-bottom:1px solid {C['border']};
        font-family:{C['mono']};">{_fmt_num(val)}</td>
    <td style="padding:8px 12px;font-size:11px;color:{C['text2']};
        text-align:right;border-bottom:1px solid {C['border']};
        font-family:{C['mono']};">{freq:,}</td>
    <td style="padding:8px 12px;font-size:11px;font-weight:600;color:{fn_col};
        text-align:right;border-bottom:1px solid {C['border']};
        font-family:{C['mono']};">{_fmt_num(fn)}</td>
</tr>"""

            header_style = (f"padding:8px 12px;font-size:9px;letter-spacing:0.1em;"
                            f"text-transform:uppercase;color:{C['text3']};font-family:{C['mono']};"
                            f"font-weight:600;border-bottom:1px solid {C['border']};text-align:right;")
            st.markdown(f"""
<div style="overflow-x:auto;">
<table style="width:100%;border-collapse:collapse;background:rgba(255,255,255,0.018);
    border:1px solid {C['border']};border-radius:10px;overflow:hidden;">
    <thead>
        <tr>
            <th style="{header_style}text-align:left;">TICKER</th>
            <th style="{header_style}text-align:left;">NAMA</th>
            <th style="{header_style}">CLOSE</th>
            <th style="{header_style}">CHG%</th>
            <th style="{header_style}">NILAI</th>
            <th style="{header_style}">FREQ</th>
            <th style="{header_style}">FOREIGN NET</th>
        </tr>
    </thead>
    <tbody>{tbl_rows}</tbody>
</table>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PART 18: DATA PIPELINE MODULE
# Admin panel untuk IDX database management
# ─────────────────────────────────────────────
def render_data_pipeline():
    st.markdown(f"""
<div style="padding:24px 28px 16px;">
    <div style="font-size:22px;font-weight:700;letter-spacing:-0.03em;color:{C['text']};">
        Data Pipeline
    </div>
    <div style="font-size:12px;color:{C['text3']};font-family:{C['mono']};margin-top:4px;">
        IDX daily data management · SQLite pipeline · Backfill engine
    </div>
</div>
""", unsafe_allow_html=True)

    # ── DB Stats ──────────────────────────────
    stats = db_stats()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Rows",    f"{stats.get('total_rows',0):,}")
    c2.metric("Hari Tersimpan", f"{stats.get('total_days',0)}")
    c3.metric("Data Terlama",   stats.get("oldest", "—"))
    c4.metric("Data Terbaru",   stats.get("newest", "—"))

    st.caption(f"📦 DB size: {stats.get('db_mb', 0)} MB  |  Path: `{_DB_PATH}`")
    _section_divider()

    # ── Auto fetch ────────────────────────────
    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.markdown(f"""
<div style="padding:12px 16px;background:rgba(255,255,255,0.02);
    border:1px solid {C['border']};border-radius:8px;
    font-size:12px;color:{C['text2']};font-family:{C['mono']};">
    💡 Auto-fetch: data hari bursa akan diambil otomatis saat startup. Jika kosong, gunakan tombol di bawah.
</div>""", unsafe_allow_html=True)
    with col_b:
        if st.button("FETCH HARI INI", key="dp_fetch_today", type="primary",
                     use_container_width=True):
            with st.spinner("Fetching..."):
                res = db_auto_fetch_today()
            if res["status"] == "ok":
                st.success(f"✅ {res['message']}")
            elif res["status"] == "skip":
                st.info(f"⏭️ {res['message']}")
            else:
                st.error(f"❌ {res['message']}")
            st.rerun()

    _section_divider("BACKFILL HISTORIS")

    months = st.slider("Bulan ke belakang", 1, 6, 3, key="dp_months_slider")
    if st.button("🔄 MULAI BACKFILL", key="dp_backfill_btn", type="primary",
                 use_container_width=True):
        # Generate date range
        today      = date.today()
        start_date = today - timedelta(days=months*30)
        trading_days = []
        cur = start_date
        while cur <= today:
            if _is_trading_day(cur):
                trading_days.append(cur.strftime("%Y-%m-%d"))
            cur += timedelta(days=1)

        progress_bar = st.progress(0.0)
        status_text  = st.empty()
        results      = {"ok": 0, "skip": 0, "error": 0}

        for i, d_str in enumerate(trading_days):
            res  = db_fetch_date(d_str)
            stat = res["status"]
            results[stat] = results.get(stat, 0) + 1
            icon = "✅" if stat == "ok" else ("⏭️" if stat == "skip" else "❌")
            progress_bar.progress((i+1)/len(trading_days))
            status_text.markdown(
                f"`[{i+1}/{len(trading_days)}]` {icon} **{d_str}** — {res['message']}"
            )

        status_text.markdown(
            f"**Selesai** — ✅ {results['ok']} baru | ⏭️ {results['skip']} skip | ❌ {results['error']} error"
        )
        st.rerun()

    _section_divider("FETCH TANGGAL SPESIFIK")
    col_date, col_fetch = st.columns([3, 1])
    with col_date:
        fetch_dt = st.date_input("Tanggal", value=date.today()-timedelta(days=1),
                                 key="dp_fetch_date")
    with col_fetch:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("FETCH", key="dp_fetch_single", use_container_width=True):
            with st.spinner("Fetching..."):
                res = db_fetch_date(fetch_dt.strftime("%Y-%m-%d"), force=True)
            if res["status"] == "ok":
                st.success(f"✅ {res['message']}")
            else:
                st.error(f"❌ {res['message']}")
            st.rerun()


# ─────────────────────────────────────────────
# PART 19: TAB PERSISTENCE SCRIPT
# (ported from SIGMA v87)
# ─────────────────────────────────────────────
def _inject_tab_persist():
    components.html("""
<script>
(function() {
    if (window.__moonsideTabPersist) return;
    window.__moonsideTabPersist = true;
    var pd = window.parent.document;
    var KEY = '_moonside_tabs_v1';

    function saveTabs() {
        try {
            var active = [];
            pd.querySelectorAll('button[role="tab"][aria-selected="true"]').forEach(function(t) {
                var txt = (t.textContent || '').trim();
                if (txt) active.push(txt);
            });
            if (active.length > 0) sessionStorage.setItem(KEY, JSON.stringify(active));
        } catch(e) {}
    }

    function restoreTabs() {
        try {
            var saved = JSON.parse(sessionStorage.getItem(KEY) || '[]');
            if (!saved.length) return;
            function restoreLevel(idx) {
                if (idx >= saved.length) return;
                pd.querySelectorAll('button[role="tab"]').forEach(function(t) {
                    if ((t.textContent || '').trim() === saved[idx]
                        && t.getAttribute('aria-selected') !== 'true') {
                        t.click();
                    }
                });
                if (idx + 1 < saved.length)
                    setTimeout(function() { restoreLevel(idx + 1); }, 150);
            }
            restoreLevel(0);
        } catch(e) {}
    }

    var _attempts = 0;
    function smartRestore() {
        _attempts++;
        if (_attempts > 20) return;
        var tabs = pd.querySelectorAll('button[role="tab"]');
        if (tabs.length === 0) { setTimeout(smartRestore, 200); return; }
        restoreTabs();
    }

    pd.addEventListener('click', function(e) {
        var el = e.target;
        while (el && el !== pd.body) {
            if (el.getAttribute && el.getAttribute('role') === 'tab') {
                setTimeout(saveTabs, 150); break;
            }
            el = el.parentElement;
        }
    }, true);

    _attempts = 0;
    setTimeout(smartRestore, 400);
})();
</script>
""", height=0)


# ─────────────────────────────────────────────
# PART 20: MAIN APP ENTRY POINT
# Fincept-style modular tab navigation
# ─────────────────────────────────────────────
def main():
    # ── Init ─────────────────────────────────
    _init_session()
    _inject_global_css()
    _render_topbar()

    # ── DB init + auto-fetch background ──────
    _db_init()
    if not st.session_state.get("_auto_fetched_today"):
        st.session_state["_auto_fetched_today"] = True
        threading.Thread(target=db_auto_fetch_today, daemon=True).start()

    # ── Content padding wrapper ───────────────
    st.markdown(f"""
<style>
/* Tab content padding */
.stTabs [data-baseweb="tab-panel"] > div {{
    padding: 0 !important;
}}
</style>
""", unsafe_allow_html=True)

    # ── Main Navigation Tabs ──────────────────
    # Inspired by Fincept Terminal's module-based navigation
    tabs = st.tabs([
        "◆ Overview",
        "⬡ Stock Insight",
        "⊕ Foreign Flow",
        "✦ AI Research",
        "◎ Screener",
        "🗄 Data Pipeline",
    ])

    with tabs[0]:
        render_overview()

    with tabs[1]:
        render_stock_insight()

    with tabs[2]:
        render_foreign_flow()

    with tabs[3]:
        render_ai_research()

    with tabs[4]:
        render_screener()

    with tabs[5]:
        render_data_pipeline()

    # ── Tab Persistence ───────────────────────
    _inject_tab_persist()

    # ── Footer ────────────────────────────────
    st.markdown(f"""
<div style="padding:24px 28px;border-top:1px solid {C['border']};
    display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">
    <div>
        <div style="font-size:12px;font-weight:700;letter-spacing:0.1em;
            color:{C['text']};text-transform:uppercase;">{PLATFORM_NAME}</div>
        <div style="font-size:10px;color:{C['text3']};font-family:{C['mono']};margin-top:2px;">
            {PLATFORM_TAGLINE} · v{PLATFORM_VERSION} · by Market n Mocha & KIPM-UP
        </div>
    </div>
    <div style="font-size:10px;color:{C['text3']};font-family:{C['mono']};">
        ⚠️ Bukan rekomendasi investasi. Hanya untuk edukasi dan riset.
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
if __name__ == "__main__":
    main()
