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
# EXACT THEME 3: BLUE + TEAL (Fresh & Calm)
# Palette: Deep Navy (#083D91), Vibrant Teal (#1488A6), Mint Teal (#5EEAD4), Light (#E0F2FE)
# =========================================================================
st.markdown(
    """
<style>
    /* Exact Navy Blue Base from Pic 3 (Clean, vibrant, not pitch-black) */
    .stApp {
        background-color: #081e42 !important;
        color: #E0F2FE !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    .block-container { 
        padding-top: 1.5rem; 
        padding-bottom: 5.5rem; 
        max-width: 1480px; 
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    #MainMenu, footer {
        visibility: hidden;
    }

    /* Left Sidebar: Navy Foundation */
    section[data-testid="stSidebar"] {
        background-color: #0b2654 !important;
        border-right: 1.5px solid rgba(94, 234, 212, 0.25) !important;
    }

    /* Sidebar Brand Card: Navy to Teal Gradient */
    .sidebar-brand {
        background: linear-gradient(135deg, #083D91 0%, #1488A6 100%) !important;
        border: 1.5px solid #5EEAD4 !important;
        border-radius: 12px;
        padding: 14px 16px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 18px rgba(20, 136, 166, 0.4);
    }
    .sidebar-brand-title {
        color: #ffffff;
        font-weight: 800;
        font-size: 1.25rem;
        letter-spacing: -0.3px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* White Sidebar Headings */
    .sidebar-section-title {
        color: #ffffff !important;
        font-size: 0.78rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 1.4rem;
        margin-bottom: 0.6rem;
    }

    /* Navigation & Action Buttons: Solid Vibrant Teal */
    .stButton > button {
        background-color: #1488A6 !important;
        color: #ffffff !important;
        border: 1px solid #5EEAD4 !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 0.86rem !important;
        padding: 0.4rem 0.7rem !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background-color: #5EEAD4 !important;
        color: #081e42 !important;
        border-color: #5EEAD4 !important;
        box-shadow: 0 0 16px rgba(94, 234, 212, 0.6) !important;
    }

    /* Slider styling: Teal bar and mint handle */
    div[data-testid="stSlider"] div[data-baseweb="slider"] div {
        background-color: transparent !important;
    }
    div[data-testid="stSlider"] [role="slider"] {
        background-color: #5EEAD4 !important;
        border: 2px solid #ffffff !important;
        box-shadow: 0 0 10px rgba(94, 234, 212, 0.8) !important;
    }
    div[data-testid="stSlider"] div[data-testid="stTickBar"] ~ div {
        background: linear-gradient(90deg, #1488A6 0%, #5EEAD4 100%) !important;
    }

    /* Movie Cards: Soft Navy Blue Box Framing from Pic 3 */
    div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stImage"]) {
        background: #0f2d5e !important;
        border: 1.5px solid rgba(20, 136, 166, 0.5) !important;
        border-radius: 12px;
        padding: 10px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.35);
        transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    }

    div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stImage"]):hover {
        transform: translateY(-5px);
        border-color: #5EEAD4 !important;
        box-shadow: 0 8px 24px rgba(94, 234, 212, 0.4) !important;
    }

    /* Uniform Poster Dimensions */
    div[data-testid="stImage"] img {
        border-radius: 8px;
        height: 255px !important;
        width: 100% !important;
        object-fit: cover !important;
    }

    /* Card Titles */
    .movie-card-title {
        color: #ffffff;
        font-size: 0.86rem;
        font-weight: 700;
        line-height: 1.25rem;
        height: 2.5rem;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        margin-top: 8px;
        margin-bottom: 8px;
        text-align: center;
    }

    /* Detail Page Glass Box */
    .glass-card {
        background: rgba(15, 45, 94, 0.9);
        border: 1px solid rgba(20, 136, 166, 0.45);
        border-radius: 14px;
        padding: 22px;
        box-shadow: 0 8px 26px rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(8px);
    }

    /* Tag Pills */
    .pill-badge {
        display: inline-block;
        border-radius: 9999px;
        padding: 3px 12px;
        font-size: 0.8rem;
        font-weight: 700;
        margin-right: 8px;
        margin-bottom: 6px;
    }

    /* Search Input Field */
    div[data-baseweb="input"] {
        background-color: #0f2d5e !important;
        border: 1.5px solid rgba(20, 136, 166, 0.6) !important;
        border-radius: 10px !important;
    }
    div[data-baseweb="input"]:focus-within {
        border-color: #5EEAD4 !important;
        box-shadow: 0 0 12px rgba(94, 234, 212, 0.5) !important;
    }
    div[data-baseweb="input"] input {
        color: #ffffff !important;
    }

    /* ================================================= */
    /* FLOATING PILL BUTTON FOR AI ASSISTANT             */
    /* ================================================= */
    div[data-testid="stPopover"] {
        position: fixed !important;
        bottom: 24px !important;
        right: 28px !important;
        width: auto !important;
        max-width: fit-content !important;
        z-index: 999999 !important;
    }

    div[data-testid="stPopover"] > button {
        background: linear-gradient(135deg, #1488A6 0%, #083D91 100%) !important;
        color: #ffffff !important;
        border: 2px solid #5EEAD4 !important;
        border-radius: 50px !important;
        padding: 10px 22px !important;
        font-size: 0.92rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.3px !important;
        box-shadow: 0 8px 24px rgba(20, 136, 166, 0.6) !important;
        display: inline-flex !important;
        align-items: center !important;
        gap: 8px !important;
        width: auto !important;
        transition: all 0.25s ease !important;
    }

    div[data-testid="stPopover"] > button:hover {
        transform: translateY(-4px) scale(1.04) !important;
        box-shadow: 0 12px 28px rgba(94, 234, 212, 0.7) !important;
    }

    div[data-testid="stPopoverBody"] {
        background: linear-gradient(160deg, #0b2654 0%, #081e42 100%) !important;
        border: 2px solid #1488A6 !important;
        border-radius: 20px !important;
        box-shadow: 0 20px 45px rgba(0, 0, 0, 0.85) !important;
        width: 390px !important;
        max-width: 90vw !important;
        max-height: 540px !important;
        padding: 18px !important;
    }

    div[data-testid="stChatMessage"] {
        background-color: #0f2d5e !important;
        border: 1px solid rgba(94, 234, 212, 0.25) !important;
        border-radius: 12px !important;
        padding: 10px 14px !important;
        margin-bottom: 8px !important;
        font-size: 0.9rem !important;
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

qp_view = st.query_params.get("view")
qp_id = st.query_params.get("id")
if qp_view in ("home", "details"):
    st.session_state.view = qp_view
if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except Exception:
        pass


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
# API HELPERS (60s timeout)
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
                            "https://via.placeholder.com/300x450/0f2d5e/1488A6?text=No+Poster",
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

    if isinstance(data, dict) and "results" in data:
        raw = data.get("results") or []
        raw_items = []
        for m in raw:
            title = (m.get("title") or "").strip()
            tmdb_id = m.get("id")
            poster_path = m.get("poster_path")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": f"{TMDB_IMG}{poster_path}" if poster_path else None,
                    "release_date": m.get("release_date", ""),
                }
            )
    elif isinstance(data, list):
        raw_items = []
        for m in data:
            tmdb_id = m.get("tmdb_id") or m.get("id")
            title = (m.get("title") or "").strip()
            poster_url = m.get("poster_url")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": poster_url,
                    "release_date": m.get("release_date", ""),
                }
            )
    else:
        return [], []

    matched = [x for x in raw_items if keyword_l in x["title"].lower()]
    final_list = matched if matched else raw_items

    suggestions = []
    for x in final_list[:10]:
        year = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))

    cards = [
        {"tmdb_id": x["tmdb_id"], "title": x["title"], "poster_url": x["poster_url"]}
        for x in final_list[:limit]
    ]
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
    st.caption(f"Currently showing: **{grid_cols} columns**")


# ==========================================================
# VIEW: HOME
# ==========================================================
if st.session_state.view == "home":
    # EXACT SHADING FROM PIC 3: Deep Royal Blue (#083D91) smoothly blending to Vibrant Teal (#1488A6) with Mint (#5EEAD4) Border
    st.markdown("""
        <div style="
            background: linear-gradient(110deg, #083D91 0%, #0d5c8a 55%, #1488A6 100%);
            border-radius: 14px;
            padding: 2.2rem 2.2rem;
            margin-bottom: 1.8rem;
            border: 1.5px solid #5EEAD4;
            box-shadow: 0 8px 25px rgba(20, 136, 166, 0.35);
        ">
            <h1 style="font-size: 2.5rem; font-weight: 800; color: #ffffff; margin: 0 0 0.4rem 0; letter-spacing: -0.5px;">🎬 CineMatch</h1>
            <p style="color: #E0F2FE; font-size: 1rem; max-width: 640px; margin: 0; opacity: 0.95;">
                Explore movies that match the plots you love.
            </p>
        </div>
    """, unsafe_allow_html=True)

    typed = st.text_input(
        "Search by movie title:",
        placeholder="Search by movie title, genre, actor...",
    )

    # SEARCH MODE
    if typed.strip():
        if len(typed.strip()) < 2:
            st.caption("Type at least 2 characters for search suggestions.")
        else:
            with st.spinner("🔎 Querying database..."):
                data, err = api_get_json("/tmdb/search", params={"query": typed.strip()})
                if err or data is None:
                    st.error(f"Search failed: {err}")
                else:
                    suggestions, cards = parse_tmdb_search_to_cards(
                        data, typed.strip(), limit=24
                    )

                    if suggestions:
                        labels = ["-- Select from suggestions --"] + [s[0] for s in suggestions]
                        selected = st.selectbox("Direct Matches", labels, index=0)

                        if selected != "-- Select from suggestions --":
                            label_to_id = {s[0]: s[1] for s in suggestions}
                            goto_details(label_to_id[selected])
                    else:
                        st.info("No suggestions found.")

                    st.markdown("### Search Results")
                    poster_grid(cards, cols=grid_cols, key_prefix="search_results")

        st.stop()

    # HOME FEED MODE
    cat_title = {
        "trending": "Trending Now",
        "popular": "Most Popular",
        "top_rated": "Highest Rated",
        "now_playing": "In Theaters",
        "upcoming": "Coming Soon"
    }.get(home_category, home_category.title())

    # Teal droplet matching Pic 3
    st.markdown(f"### <span style='color: #5EEAD4; font-size: 1.2rem; vertical-align: middle;'>💧</span> {cat_title}", unsafe_allow_html=True)

    home_cards, err = api_get_json(
        "/home", params={"category": home_category, "limit": 24}
    )
    if err or not home_cards:
        st.error(f"Home feed failed: {err or 'Unknown error'}")
        st.stop()

    poster_grid(home_cards, cols=grid_cols, key_prefix="home_feed")

# ==========================================================
# VIEW: DETAILS
# ==========================================================
elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id
    if not tmdb_id:
        st.warning("No movie selected.")
        if st.button("← Back to Feed"):
            goto_home()
        st.stop()

    col_nav_left, col_nav_right = st.columns([4, 1])
    with col_nav_left:
        st.markdown("### Movie Details & Intelligence")
    with col_nav_right:
        if st.button("← Back to Feed", use_container_width=True):
            goto_home()

    data, err = api_get_json(f"/movie/id/{tmdb_id}")
    if err or not data:
        st.error(f"Could not load details: {err or 'Unknown error'}")
        st.stop()

    if data.get("backdrop_url"):
        st.markdown(f"""
        <div style="
            background-image: linear-gradient(to bottom, rgba(8, 30, 66, 0.2), #081e42), url('{data["backdrop_url"]}');
            background-size: cover;
            background-position: center;
            height: 250px;
            border-radius: 14px;
            margin-bottom: 1.5rem;
            border: 1.5px solid rgba(20, 136, 166, 0.35);
        "></div>
        """, unsafe_allow_html=True)

    left, right = st.columns([1, 2.2], gap="large")

    with left:
        poster_src = data.get("poster_url") or "https://via.placeholder.com/500x750/0f2d5e/1488A6?text=No+Poster"
        st.image(poster_src, use_container_width=True)

    with right:
        st.markdown(f"## {data.get('title','')}")
        
        release = data.get("release_date") or "N/A"
        vote_avg = data.get("vote_average")
        rating_str = f"⭐ {vote_avg:.1f}/10" if vote_avg else "⭐ Unrated"
        
        st.markdown(
            f"""
            <div style="margin-bottom: 1rem;">
                <span class="pill-badge" style="background: rgba(224, 242, 254, 0.15); color: #E0F2FE; border: 1px solid rgba(224, 242, 254, 0.3);">{release[:4] if release != 'N/A' else 'N/A'}</span>
                <span class="pill-badge" style="background: rgba(234, 179, 8, 0.25); color: #facc15; border: 1px solid rgba(234, 179, 8, 0.5);">{rating_str}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        genres = [g["name"] for g in data.get("genres", [])]
        if genres:
            genre_html = "".join([f'<span class="pill-badge" style="background: rgba(20, 136, 166, 0.35); color: #5EEAD4; border: 1px solid rgba(94, 234, 212, 0.4);">{g}</span>' for g in genres])
            st.markdown(f"<div style='margin-bottom: 1.2rem;'>{genre_html}</div>", unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="glass-card">
                <h4 style="margin-top: 0; color: #5EEAD4;">Synopsis</h4>
                <p style="color: #E0F2FE; line-height: 1.6; margin-bottom: 0;">{data.get("overview") or "No overview provided."}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

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
                genre_only, err3 = api_get_json(
                    "/recommend/genre", params={"tmdb_id": tmdb_id, "limit": 18}
                )
                if not err3 and genre_only:
                    poster_grid(
                        genre_only, cols=grid_cols, key_prefix="details_genre_fallback"
                    )
                else:
                    st.info("No genre suggestions available right now.")
    else:
        st.warning("No title available to compute recommendations.")

# =========================================================
# TEAL FLOATING POP-UP AI ASSISTANT
# =========================================================
with st.popover("💬 Ask AI Assistant"):
    st.markdown(
        """
        <div style="margin-bottom: 10px;">
            <span style="background: #1488A6; color: #ffffff; padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; font-weight: 800; border: 1px solid rgba(94, 234, 212, 0.4);">POWERED BY AI</span>
            <h3 style="margin: 6px 0 2px 0; color: #E0F2FE; font-size: 1.25rem;">💬 AI Movie Assistant</h3>
            <span style="color: #5EEAD4; font-size: 0.8rem;">Ask plot breakdowns, similar vibes, or cast trivia</span>
        </div>
        <hr style="border-color: rgba(20, 136, 166, 0.4); margin: 6px 0 12px 0;">
        """,
        unsafe_allow_html=True,
    )

    for role, text in st.session_state.chat_history:
        with st.chat_message(role):
            st.write(text)

    chat_question = st.chat_input("Ask CineMatch AI...")

    if chat_question:
        st.session_state.chat_history.append(("user", chat_question))
        with st.chat_message("user"):
            st.write(chat_question)

        with st.chat_message("assistant"):
            with st.spinner("💬 Thinking..."):
                answer = get_ai_movie_response(chat_question)
            st.write(answer)
        st.session_state.chat_history.append(("assistant", answer))
        st.rerun()