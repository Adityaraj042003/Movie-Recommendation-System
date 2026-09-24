import requests
import streamlit as st
from ai_chatbot import get_ai_movie_response

# =============================
# CONFIG
# =============================
API_BASE = "https://movie-recommendation-system-1-r49y.onrender.com"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(
    page_title="CineMatch | Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================================
# THEME 3: BLUE + TEAL (Pixel Match with Bottom-Right Inline Assistant)
# =========================================================================
st.markdown(
    """
<style>
    /* Dark Oceanic Slate Base */
    .stApp {
        background-color: #061024 !important;
        color: #E0F2FE !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    .block-container { 
        padding-top: 1.2rem; 
        padding-bottom: 5rem; 
        max-width: 1440px; 
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    #MainMenu, footer {
        visibility: hidden;
    }

    /* Left Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #081630 !important;
        border-right: 1px solid rgba(20, 136, 166, 0.25) !important;
    }

    .sidebar-brand {
        background: linear-gradient(135deg, #083D91 0%, #0d285c 100%) !important;
        border: 1px solid rgba(94, 234, 212, 0.4) !important;
        border-radius: 10px;
        padding: 14px 16px;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3);
    }
    .sidebar-brand-title {
        color: #ffffff;
        font-weight: 800;
        font-size: 1.2rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .sidebar-section-title {
        color: #ffffff !important;
        font-size: 0.76rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 1.2rem;
        margin-bottom: 0.5rem;
    }

    /* Action Buttons */
    .stButton > button {
        background-color: #1488A6 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 700 !important;
        font-size: 0.85rem !important;
        padding: 0.4rem 0.7rem !important;
        width: 100% !important;
        box-shadow: 0 3px 10px rgba(20, 136, 166, 0.3) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background-color: #5EEAD4 !important;
        color: #061024 !important;
        box-shadow: 0 0 14px rgba(94, 234, 212, 0.5) !important;
    }

    /* Slider: Teal styling */
    div[data-testid="stSlider"] div[data-baseweb="slider"] {
        margin-top: 5px;
    }
    div[data-testid="stSlider"] [role="slider"] {
        background-color: #5EEAD4 !important;
        border: 2px solid #ffffff !important;
        box-shadow: 0 0 8px rgba(94, 234, 212, 0.8) !important;
    }
    div[data-testid="stSlider"] [data-testid="stTickBar"] ~ div div {
        background: #1488A6 !important;
    }

    /* Hero Panel from Photo */
    .hero-panel {
        background: #083D91 !important;
        border-radius: 12px;
        padding: 2rem 2.2rem;
        margin-bottom: 1.4rem;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45);
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0 0 0.3rem 0;
        letter-spacing: -0.4px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .hero-subtitle {
        color: #CBD5E1;
        font-size: 0.95rem;
        margin: 0;
    }

    /* Uniform Movie Cards */
    div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stImage"]) {
        background: #0d1e3d !important;
        border: 1px solid rgba(20, 136, 166, 0.3) !important;
        border-radius: 10px;
        padding: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stImage"]):hover {
        transform: translateY(-4px);
        border-color: #5EEAD4 !important;
    }

    div[data-testid="stImage"] img {
        border-radius: 6px;
        height: 240px !important;
        width: 100% !important;
        object-fit: cover !important;
    }

    .movie-card-title {
        color: #ffffff;
        font-size: 0.82rem;
        font-weight: 600;
        line-height: 1.2rem;
        height: 2.4rem;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        margin: 6px 0 8px 0;
        text-align: center;
    }

    /* ========================================================================= */
    /* EXACT POPOVER STYLING (Pinned to Bottom-Right without stretching)        */
    /* ========================================================================= */
    div[data-testid="stPopover"] {
        position: fixed !important;
        bottom: 18px !important;
        right: 24px !important;
        width: auto !important;
        z-index: 999999 !important;
    }

    div[data-testid="stPopover"] > button {
        background: rgba(13, 30, 61, 0.95) !important;
        color: #ffffff !important;
        border: 1.5px solid #1488A6 !important;
        border-radius: 8px !important;
        padding: 6px 14px !important;
        font-size: 0.84rem !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.6) !important;
        width: auto !important;
    }

    div[data-testid="stPopover"] > button:hover {
        border-color: #5EEAD4 !important;
        background: #083D91 !important;
    }

    /* Floating Card Modal matching the Photo */
    div[data-testid="stPopoverBody"] {
        background: #0d285c !important;
        border: 1.5px solid #1488A6 !important;
        border-radius: 12px !important;
        box-shadow: 0 16px 40px rgba(0, 0, 0, 0.8) !important;
        width: 380px !important;
        max-width: 90vw !important;
        padding: 16px !important;
    }

    /* Forced White Text on both laptops */
    div[data-testid="stChatMessage"] {
        background-color: #081c3d !important;
        border: 1px solid rgba(94, 234, 212, 0.3) !important;
        border-radius: 10px !important;
        padding: 10px 12px !important;
        margin-bottom: 8px !important;
    }

    div[data-testid="stChatMessage"] * {
        color: #ffffff !important;
        line-height: 1.4 !important;
    }

    div[data-testid="stChatMessage"] code {
        background-color: rgba(20, 136, 166, 0.4) !important;
        color: #5EEAD4 !important;
        border: 1px solid rgba(94, 234, 212, 0.4) !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
    }
    /* Fix AI Assistant message text visibility */
div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"],
div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,
div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li,
div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] strong,
div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] span {
    color: #ffffff !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# =============================
# STATE + ROUTING
# =============================
if "view" not in st.session_state:
    st.session_state.view = "home"
if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


def goto_home():
    st.session_state.view = "home"
    st.query_params["view"] = "home"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()


def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))
    st.rerun()


# =============================
# API HELPERS
# =============================
@st.cache_data(ttl=30, show_spinner=False)
def api_get_json(path: str, params: dict | None = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=60)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}: {r.text[:300]}"
        return r.json(), None
    except Exception as e:
        return None, f"Request failed: {e}"


def poster_grid(cards, cols=6, key_prefix="grid"):
    if not cards:
        st.info("No movies to display.")
        return

    rows = (len(cards) + cols - 1) // cols
    idx = 0
    for r in range(rows):
        colset = st.columns(cols, gap="small")
        for c in range(cols):
            if idx >= len(cards):
                break
            m = cards[idx]
            idx += 1

            tmdb_id = m.get("tmdb_id")
            title = m.get("title", "Untitled")
            poster = m.get("poster_url")

            with colset[c]:
                with st.container():
                    if poster:
                        st.image(poster, use_container_width=True)
                    else:
                        st.image(
                            "https://via.placeholder.com/300x450/0d1e3d/1488A6?text=No+Poster",
                            use_container_width=True,
                        )

                    st.markdown(
                        f"<div class='movie-card-title' title='{title}'>{title}</div>",
                        unsafe_allow_html=True,
                    )

                    if st.button("Details", key=f"{key_prefix}_{r}_{c}_{idx}_{tmdb_id}", use_container_width=True):
                        if tmdb_id:
                            goto_details(tmdb_id)


def to_cards_from_tfidf_items(tfidf_items):
    cards = []
    for x in tfidf_items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append(
                {
                    "tmdb_id": tmdb["tmdb_id"],
                    "title": tmdb.get("title") or x.get("title") or "Untitled",
                    "poster_url": tmdb.get("poster_url"),
                }
            )
    return cards


def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 24):
    keyword_l = keyword.strip().lower()
    raw_items = []
    if isinstance(data, dict) and "results" in data:
        for m in data.get("results") or []:
            title = (m.get("title") or "").strip()
            tmdb_id = m.get("id")
            poster_path = m.get("poster_path")
            if title and tmdb_id:
                raw_items.append({
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": f"{TMDB_IMG}{poster_path}" if poster_path else None,
                    "release_date": m.get("release_date", "")
                })

    matched = [x for x in raw_items if keyword_l in x["title"].lower()]
    final_list = matched if matched else raw_items

    suggestions = []
    for x in final_list[:10]:
        year = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))

    cards = [{"tmdb_id": x["tmdb_id"], "title": x["title"], "poster_url": x["poster_url"]} for x in final_list[:limit]]
    return suggestions, cards


# =============================
# LEFT SIDEBAR
# =============================
with st.sidebar:
    st.markdown("""
        <div class="sidebar-brand">
            <div class="sidebar-brand-title">🎬 CineMatch</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-title">Navigation</div>', unsafe_allow_html=True)
    if st.button("Home Catalog", use_container_width=True):
        goto_home()

    st.markdown('<div class="sidebar-section-title">Feed Settings</div>', unsafe_allow_html=True)
    home_category = st.selectbox(
        "Catalog Category",
        ["trending", "popular", "top_rated", "now_playing", "upcoming"],
        index=0,
        format_func=lambda x: {
            "trending": "Trending Now",
            "popular": "Most Popular",
            "top_rated": "Highest Rated",
            "now_playing": "In Theaters",
            "upcoming": "Coming Soon"
        }.get(x, x.title()),
        label_visibility="collapsed"
    )

    st.write("")
    st.markdown('<div class="sidebar-section-title">Display Density</div>', unsafe_allow_html=True)
    grid_cols = st.slider("Columns per row", 4, 8, 6, label_visibility="collapsed")


# ==========================================================
# VIEW: HOME
# ==========================================================
if st.session_state.view == "home":
    st.markdown("""
        <div class="hero-panel">
            <div class="hero-title">🎬 CineMatch</div>
            <p class="hero-subtitle">Explore movies that match the plots you love.</p>
        </div>
    """, unsafe_allow_html=True)

    typed = st.text_input(
        "Search by movie title:",
        placeholder="Type a movie name: Interstellar, Inception, Avengers, Batman...",
    )

    if typed.strip():
        if len(typed.strip()) >= 2:
            with st.spinner("Searching..."):
                data, err = api_get_json("/tmdb/search", params={"query": typed.strip()})
                if not err and data:
                    suggestions, cards = parse_tmdb_search_to_cards(data, typed.strip(), limit=24)
                    if suggestions:
                        labels = ["-- Select direct match --"] + [s[0] for s in suggestions]
                        selected = st.selectbox("Direct Matches", labels, index=0)
                        if selected != "-- Select direct match --":
                            label_to_id = {s[0]: s[1] for s in suggestions}
                            goto_details(label_to_id[selected])
                    st.markdown("### Search Results")
                    poster_grid(cards, cols=grid_cols, key_prefix="search")
        st.stop()

    cat_title = {
        "trending": "Trending Now",
        "popular": "Most Popular",
        "top_rated": "Highest Rated",
        "now_playing": "In Theaters",
        "upcoming": "Coming Soon"
    }.get(home_category, home_category.title())

    st.markdown(f"### <span style='color: #1488A6;'>💧</span> {cat_title}", unsafe_allow_html=True)

    home_cards, err = api_get_json("/home", params={"category": home_category, "limit": 24})
    if err or not home_cards:
        st.error("Backend waking up. Please refresh in a few seconds.")
        st.stop()

    poster_grid(home_cards, cols=grid_cols, key_prefix="feed")

# ==========================================================
# VIEW: DETAILS
# ==========================================================
elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id
    if not tmdb_id:
        goto_home()

    if st.button("← Back to Feed", use_container_width=False):
        goto_home()

    data, err = api_get_json(f"/movie/id/{tmdb_id}")
    if not err and data:
        left, right = st.columns([1, 2.5], gap="large")
        with left:
            st.image(data.get("poster_url") or "", use_container_width=True)
        with right:
            st.markdown(f"## {data.get('title','')}")
            st.write(data.get("overview") or "No synopsis available.")

        st.markdown("---")
        st.subheader("🎯 Recommendations")

        title = (data.get("title") or "").strip()
        if title:
            bundle, err2 = api_get_json(
                "/movie/search",
                params={"query": title, "tfidf_top_n": 12, "genre_limit": 12},
            )

            tab_tfidf, tab_genre = st.tabs(["🧠 Content Matches (TF-IDF Similarity)", "🎭 Genre Suggestions"])

            with tab_tfidf:
                if not err2 and bundle and bundle.get("tfidf_recommendations"):
                    poster_grid(
                        to_cards_from_tfidf_items(bundle.get("tfidf_recommendations")),
                        cols=grid_cols,
                        key_prefix="details_tfidf",
                    )
                else:
                    st.info("No direct TF-IDF matches available for this title.")

            with tab_genre:
                genre_items = bundle.get("genre_recommendations", []) if (not err2 and bundle) else []
                if genre_items:
                    poster_grid(
                        genre_items,
                        cols=grid_cols,
                        key_prefix="details_genre",
                    )
                else:
                    st.info("No genre suggestions available right now.")

# =========================================================
# FLOATING POPOVER (EXACT POSITION FROM PHOTO)
# =========================================================
with st.popover("💬 Ask AI Assistant"):
    st.markdown(
        """
        <div style="margin-bottom: 8px;">
            <span style="background: #1488A6; color: #ffffff; padding: 2px 7px; border-radius: 4px; font-size: 0.7rem; font-weight: 800;">POWERED BY AI</span>
            <h4 style="margin: 6px 0 2px 0; color: #ffffff; font-size: 1.15rem;">💬 AI Movie Assistant</h4>
            <span style="color: #94A3B8; font-size: 0.8rem;">Ask plot breakdowns, similar vibes, or cast trivia</span>
        </div>
        <hr style="border-color: rgba(20, 136, 166, 0.4); margin: 6px 0 10px 0;">
        """,
        unsafe_allow_html=True,
    )

    for role, text in st.session_state.chat_history:
        with st.chat_message(role):
            st.write(text)

    q = st.chat_input("Ask CineMatch AI...")
    if q:
        st.session_state.chat_history.append(("user", q))
        with st.chat_message("user"):
            st.write(q)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                ans = get_ai_movie_response(q)
            st.write(ans)

        st.session_state.chat_history.append(("assistant", ans))
        st.rerun()