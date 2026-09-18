import os
import json
import ast
import pandas as pd
from dotenv import load_dotenv
from google import genai


# =========================================================
# GEMINI SETUP
# =========================================================

load_dotenv()

AI_API_KEY = os.getenv("GEMINI_API_KEY")

if AI_API_KEY:
    ai_client = genai.Client(api_key=AI_API_KEY)
else:
    ai_client = None


# =========================================================
# LOAD DATASET
# =========================================================

DATASET_PATH = "movies_metadata.csv"

try:
    ai_movie_data = pd.read_csv(
        DATASET_PATH,
        low_memory=False
    )
except Exception:
    ai_movie_data = pd.DataFrame()


# =========================================================
# REQUIRED COLUMNS
# =========================================================

AI_COLUMNS = [
    "title",
    "overview",
    "genres",
    "release_date",
    "budget",
    "revenue",
    "runtime",
    "popularity",
    "vote_average",
    "vote_count",
    "original_language"
]

if not ai_movie_data.empty:

    available_columns = [
        col
        for col in AI_COLUMNS
        if col in ai_movie_data.columns
    ]

    ai_movie_data = ai_movie_data[
        available_columns
    ].copy()


# =========================================================
# EXTRACT GENRES
# =========================================================

def extract_genres(value):

    if pd.isna(value):
        return []

    if isinstance(value, list):
        return [
            str(item).strip()
            for item in value
            if item
        ]

    value = str(value).strip()

    if not value:
        return []

    # Try JSON
    try:

        parsed = json.loads(value)

        if isinstance(parsed, list):

            return [
                str(item.get("name", "")).strip()
                for item in parsed
                if isinstance(item, dict)
                and item.get("name")
            ]

    except Exception:
        pass

    # Try Python literal
    try:

        parsed = ast.literal_eval(value)

        if isinstance(parsed, list):

            return [
                str(item.get("name", "")).strip()
                for item in parsed
                if isinstance(item, dict)
                and item.get("name")
            ]

    except Exception:
        pass

    return []


# =========================================================
# CREATE GENRE LIST
# =========================================================

if (
    not ai_movie_data.empty
    and "genres" in ai_movie_data.columns
):

    ai_movie_data["genre_list"] = (
        ai_movie_data["genres"]
        .apply(extract_genres)
    )

else:

    ai_movie_data["genre_list"] = [
        []
        for _ in range(len(ai_movie_data))
    ]


# =========================================================
# SEARCH MOVIES BY GENRE
# =========================================================

def get_movies_by_genre(genre, limit=5):

    if ai_movie_data.empty:
        return pd.DataFrame()

    genre = str(genre).strip().lower()

    matches = ai_movie_data[
        ai_movie_data["genre_list"].apply(
            lambda genre_list:
            genre in [
                str(g).strip().lower()
                for g in genre_list
            ]
        )
    ].copy()

    if matches.empty:
        return pd.DataFrame()

    matches["vote_average"] = pd.to_numeric(
        matches["vote_average"],
        errors="coerce"
    )

    matches["vote_count"] = pd.to_numeric(
        matches["vote_count"],
        errors="coerce"
    )

    matches["popularity"] = pd.to_numeric(
        matches["popularity"],
        errors="coerce"
    )

    matches = matches.dropna(
        subset=["vote_average"]
    )

    # Only movies with reasonable number of votes
    matches = matches[
        matches["vote_count"] >= 100
    ]

    matches = matches.sort_values(
        [
            "vote_average",
            "vote_count"
        ],
        ascending=[
            False,
            False
        ]
    )

    return matches.head(limit)


# =========================================================
# FIND MOVIE FROM QUESTION
# =========================================================

def find_movie_from_question(question):

    if ai_movie_data.empty:
        return pd.DataFrame()

    question_lower = str(question).lower()

    titles = (
        ai_movie_data["title"]
        .fillna("")
        .astype(str)
    )

    # Find the longest matching movie title
    # inside the user's question.
    matched_titles = []

    for title in titles:

        title_clean = title.strip()

        if not title_clean:
            continue

        if len(title_clean) < 2:
            continue

        if title_clean.lower() in question_lower:

            matched_titles.append(title_clean)

    if not matched_titles:
        return pd.DataFrame()

    # Longest title = most specific match
    matched_title = max(
        matched_titles,
        key=len
    )

    result = ai_movie_data[
        ai_movie_data["title"]
        .fillna("")
        .astype(str)
        .str.lower()
        == matched_title.lower()
    ].copy()

    return result.head(5)


# =========================================================
# BUILD MOVIE CONTEXT
# =========================================================

def build_movie_context(movies):

    if movies.empty:
        return None

    context_parts = []

    for _, movie in movies.iterrows():

        context_parts.append(
            f"""
Title: {movie.get("title", "N/A")}
Overview: {movie.get("overview", "N/A")}
Release Date: {movie.get("release_date", "N/A")}
Genres: {movie.get("genres", "N/A")}
Rating: {movie.get("vote_average", "N/A")}
Vote Count: {movie.get("vote_count", "N/A")}
Popularity: {movie.get("popularity", "N/A")}
Runtime: {movie.get("runtime", "N/A")} minutes
Budget: {movie.get("budget", "N/A")}
Revenue: {movie.get("revenue", "N/A")}
Language: {movie.get("original_language", "N/A")}
"""
        )

    return "\n--------------------\n".join(
        context_parts
    )


# =========================================================
# ANALYZE DATASET
# =========================================================

def analyze_movie_dataset(question):

    if ai_movie_data.empty:
        return None

    data = ai_movie_data.copy()

    # Convert numeric columns
    numeric_columns = [
        "budget",
        "revenue",
        "runtime",
        "popularity",
        "vote_average",
        "vote_count"
    ]

    for col in numeric_columns:

        if col in data.columns:

            data[col] = pd.to_numeric(
                data[col],
                errors="coerce"
            )

    question_lower = str(question).lower()


    # =====================================================
    # GENRE DETECTION
    # =====================================================

    genres = [
        "science fiction",
        "action",
        "adventure",
        "animation",
        "comedy",
        "crime",
        "documentary",
        "drama",
        "family",
        "fantasy",
        "history",
        "horror",
        "music",
        "mystery",
        "romance",
        "thriller",
        "war",
        "western"
    ]

    requested_genre = None

    for genre in genres:

        if genre in question_lower:

            requested_genre = genre

            break


    # =====================================================
    # GENRE RESULT
    # =====================================================

    if requested_genre:

        result = get_movies_by_genre(
            requested_genre,
            limit=5
        )

        if result.empty:
            return None

        return {
            "type": "genre",
            "genre": requested_genre,
            "data": result[
                [
                    "title",
                    "vote_average",
                    "vote_count",
                    "popularity"
                ]
            ].to_string(
                index=False
            )
        }


    # =====================================================
    # TOP RATED
    # =====================================================

    if (
        "highest rated" in question_lower
        or "top rated" in question_lower
    ):

        result = data.dropna(
            subset=["vote_average"]
        )

        result = result[
            result["vote_count"] >= 100
        ]

        result = result.sort_values(
            "vote_average",
            ascending=False
        ).head(10)

        if result.empty:
            return None

        return {
            "type": "ranking",
            "data": result[
                [
                    "title",
                    "vote_average",
                    "vote_count"
                ]
            ].to_string(
                index=False
            )
        }


    # =====================================================
    # HIGHEST REVENUE
    # =====================================================

    if (
        "highest revenue" in question_lower
        or "top revenue" in question_lower
    ):

        result = data.dropna(
            subset=["revenue"]
        )

        result = result[
            result["revenue"] > 0
        ]

        result = result.sort_values(
            "revenue",
            ascending=False
        ).head(10)

        if result.empty:
            return None

        return {
            "type": "revenue",
            "data": result[
                [
                    "title",
                    "revenue"
                ]
            ].to_string(
                index=False
            )
        }


    # =====================================================
    # MOST POPULAR
    # =====================================================

    if (
        "most popular" in question_lower
        or "top popular" in question_lower
    ):

        result = data.dropna(
            subset=["popularity"]
        )

        result = result.sort_values(
            "popularity",
            ascending=False
        ).head(10)

        if result.empty:
            return None

        return {
            "type": "popularity",
            "data": result[
                [
                    "title",
                    "popularity"
                ]
            ].to_string(
                index=False
            )
        }


    return None


# =========================================================
# GEMINI RESPONSE
# =========================================================

def get_ai_movie_response(question):

    question = str(question).strip()

    if not question:
        return "Question is not valid for this model."


    if ai_movie_data.empty:
        return "Question is not valid for this model."


    # =====================================================
    # STEP 1: DATASET ANALYSIS
    # =====================================================

    analysis = analyze_movie_dataset(
        question
    )


    # =====================================================
    # STEP 2: IF DATASET ANALYSIS FOUND RESULT
    # =====================================================

    if analysis:

        dataset_context = analysis["data"]

        if analysis["type"] == "genre":

            dataset_context = f"""
Genre requested by user:
{analysis["genre"].title()}

Movies found in the user's dataset:

{analysis["data"]}
"""


    # =====================================================
    # STEP 3: SPECIFIC MOVIE QUESTION
    # =====================================================

    else:

        movies = find_movie_from_question(
            question
        )

        if movies.empty:

            return (
                "Question is not valid for this model."
            )

        dataset_context = build_movie_context(
            movies
        )

        if not dataset_context:

            return (
                "Question is not valid for this model."
            )


    # =====================================================
    # STEP 4: GEMINI API CHECK
    # =====================================================

    if ai_client is None:

        return (
            "Question is not valid for this model."
        )


    # =====================================================
    # STEP 5: GEMINI PROMPT
    # =====================================================

    prompt = f"""
You are an AI Movie Assistant.

USER QUESTION:
{question}

MOVIE DATA FROM THE USER'S DATASET:
{dataset_context}

Instructions:

- Answer the user's question naturally.
- Use the movie data above as your factual source.
- You may explain, summarize, compare, and interpret the
  provided movie information in your own words.
- Do not introduce movies that are not present in the data.
- Do not change numerical values from the dataset.
- Do not invent missing movie information.
- Keep the answer relevant to the user's question.
- If the provided data does not contain the information
  needed to answer the question, say:
  "This information is not available in the dataset."
"""


    # =====================================================
    # STEP 6: GEMINI CALL
    # =====================================================

    try:

        response = ai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if response and response.text:

            return response.text.strip()

        return (
            "Question is not valid for this model."
        )

    except Exception:

        # Dataset result is still useful if Gemini
        # temporarily fails.

        if analysis:

            return analysis["data"]

        return (
            "Question is not valid for this model."
        )