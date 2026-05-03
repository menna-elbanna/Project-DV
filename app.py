"""
Person 6 — Line & Area charts + Dash callbacks (FIFA cleaned data).

Large CSVs: only the first MAX_ROWS rows are loaded (chunked read) so the app
stays responsive; widen MAX_ROWS if you need more coverage.
"""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, callback, dcc, html

BASE_DIR = Path(__file__).resolve().parent
DATA_CLEAN = BASE_DIR / "data" / "cleaned_data.csv"
DATA_SAMPLE = BASE_DIR / "data" / "sample_cleaned_data.csv"

USECOLS = ["age", "overall", "club_name", "nationality_name"]
CHUNK_ROWS = 200_000
MAX_ROWS = int(os.environ.get("FIFA_DASH_MAX_ROWS", "500_000"))


def resolve_data_path() -> Path:
    if DATA_CLEAN.exists():
        return DATA_CLEAN
    if DATA_SAMPLE.exists():
        return DATA_SAMPLE
    raise FileNotFoundError(
        "Place data/cleaned_data.csv (or data/sample_cleaned_data.csv) in the project."
    )


def load_data(path: Path) -> pd.DataFrame:
    """Chunked read; cap rows so huge files (multi-million rows) do not exhaust RAM."""
    parts: list[pd.DataFrame] = []
    n = 0
    for chunk in pd.read_csv(
        path,
        usecols=USECOLS,
        chunksize=CHUNK_ROWS,
        low_memory=False,
    ):
        parts.append(chunk)
        n += len(chunk)
        if n >= MAX_ROWS:
            break
    df = pd.concat(parts, ignore_index=True)
    if len(df) > MAX_ROWS:
        df = df.iloc[:MAX_ROWS].copy()
    df = df.dropna(subset=["age", "overall", "club_name", "nationality_name"])
    df["age"] = df["age"].astype(int)
    df["overall"] = df["overall"].astype(int)
    return df


PATH = resolve_data_path()
DF = load_data(PATH)
AGE_MIN = int(DF["age"].min())
AGE_MAX = int(DF["age"].max())

app = Dash(__name__)
app.title = "FIFA — Person 6 (Line & Area)"

app.layout = html.Div(
    [
        html.H1("Person 6 — Line & Area + callbacks", style={"marginBottom": "0.25rem"}),
        html.P(
            [
                f"Data: {PATH.name} — using up to {MAX_ROWS:,} rows loaded for speed. ",
                "No year column: line = mean overall by age; area = players per age. ",
                "Set FIFA_DASH_MAX_ROWS to load more.",
            ],
            style={"maxWidth": "920px", "color": "#444"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Filter by", style={"fontWeight": "600"}),
                        dcc.Dropdown(
                            id="filter-type",
                            options=[
                                {"label": "Club / نادي", "value": "Club"},
                                {"label": "Country / جنسية", "value": "Country"},
                            ],
                            value="Club",
                            clearable=False,
                            style={"minWidth": "200px"},
                        ),
                    ],
                    style={"flex": "0 0 auto"},
                ),
                html.Div(
                    [
                        html.Label("Club or country", style={"fontWeight": "600"}),
                        dcc.Dropdown(
                            id="filter-value",
                            options=[],
                            value=None,
                            clearable=False,
                            style={"minWidth": "280px"},
                        ),
                    ],
                    style={"flex": "1 1 320px"},
                ),
                html.Div(
                    [
                        html.Label("Age range / نطاق العمر", style={"fontWeight": "600"}),
                        dcc.RangeSlider(
                            id="age-range",
                            min=AGE_MIN,
                            max=AGE_MAX,
                            step=1,
                            value=[AGE_MIN, AGE_MAX],
                            marks={i: str(i) for i in range(AGE_MIN, AGE_MAX + 1, 5)},
                            tooltip={"placement": "bottom", "always_visible": False},
                        ),
                    ],
                    style={"flex": "1 1 360px", "paddingTop": "8px"},
                ),
            ],
            style={
                "display": "flex",
                "flexWrap": "wrap",
                "gap": "1.5rem",
                "alignItems": "flex-end",
                "marginBottom": "1.5rem",
                "padding": "1rem",
                "background": "#f6f8fa",
                "borderRadius": "8px",
            },
        ),
        html.Div(
            [
                dcc.Graph(id="line-rating-trend", style={"flex": "1 1 480px"}),
                dcc.Graph(id="area-player-distribution", style={"flex": "1 1 480px"}),
            ],
            style={"display": "flex", "flexWrap": "wrap", "gap": "1rem"},
        ),
    ],
    style={"fontFamily": "system-ui, sans-serif", "padding": "1.25rem 2rem", "maxWidth": "1200px"},
)


def _empty_fig(message: str) -> go.Figure:
    fig = go.Figure()
    fig.update_layout(
        annotations=[
            dict(
                text=message,
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=16, color="#666"),
            )
        ],
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        template="plotly_white",
        height=420,
    )
    return fig


def _apply_filters(
    df: pd.DataFrame,
    filter_type: str,
    filter_value: str | None,
    age_lo: int,
    age_hi: int,
) -> pd.DataFrame:
    out = df[(df["age"] >= age_lo) & (df["age"] <= age_hi)].copy()
    if not filter_value or filter_value == "__ALL__":
        return out
    if filter_type == "Club":
        return out[out["club_name"] == filter_value]
    return out[out["nationality_name"] == filter_value]


@callback(
    Output("filter-value", "options"),
    Output("filter-value", "value"),
    Input("filter-type", "value"),
)
def update_filter_choices(filter_type: str):
    all_opt = {"label": "All / الكل", "value": "__ALL__"}
    if filter_type == "Club":
        vals = sorted(DF["club_name"].dropna().astype(str).unique())
    else:
        vals = sorted(DF["nationality_name"].dropna().astype(str).unique())
    opts = [all_opt] + [{"label": v, "value": v} for v in vals]
    return opts, "__ALL__"


@callback(
    Output("line-rating-trend", "figure"),
    Output("area-player-distribution", "figure"),
    Input("filter-type", "value"),
    Input("filter-value", "value"),
    Input("age-range", "value"),
)
def update_person6_charts(filter_type: str, filter_value: str | None, age_range):
    if age_range is None or len(age_range) != 2:
        age_lo, age_hi = AGE_MIN, AGE_MAX
    else:
        age_lo, age_hi = int(age_range[0]), int(age_range[1])

    sub = _apply_filters(DF, filter_type, filter_value, age_lo, age_hi)
    if sub.empty:
        msg = "No rows after filters — widen age or choose All."
        return _empty_fig(msg), _empty_fig(msg)

    trend = sub.groupby("age", as_index=False)["overall"].mean().sort_values("age")
    line_fig = px.line(
        trend,
        x="age",
        y="overall",
        markers=True,
        title="Mean overall by age (trend — no year column in data)",
    )
    line_fig.update_traces(line=dict(width=3))
    line_fig.update_layout(
        template="plotly_white",
        height=420,
        xaxis_title="Age",
        yaxis_title="Mean overall",
        hovermode="x unified",
    )

    counts = sub.groupby("age").size().reset_index(name="players").sort_values("age")
    area_fig = px.area(
        counts,
        x="age",
        y="players",
        title="Players per age (distribution)",
    )
    area_fig.update_traces(line_color="#636efa", fillcolor="rgba(99,110,250,0.35)")
    area_fig.update_layout(
        template="plotly_white",
        height=420,
        xaxis_title="Age",
        yaxis_title="Player count",
    )

    return line_fig, area_fig


if __name__ == "__main__":
    app.run(debug=True)
