import plotly.express as px
import pandas as pd


def bar_mean_delay(df: pd.DataFrame, by: str):
    return px.bar(df, x=by, y="mean_delay", title=f"Average Arrival Delay by {by}")


def line_delay_by_hour(df: pd.DataFrame):
    g = df.groupby("DEP_HOUR")["ARR_DELAY"].mean(numeric_only=True).reset_index()
    return px.line(
        g, x="DEP_HOUR", y="ARR_DELAY", title="Average Arrival Delay by Departure Hour"
    )


def heatmap_origin_dest(df: pd.DataFrame, top_n=20):
    routes = df.groupby(["ORIGIN", "DEST"])["ARR_DELAY"].mean().reset_index()
    routes = routes.sort_values("ARR_DELAY", ascending=False).head(top_n)
    fig = px.density_heatmap(
        routes,
        x="ORIGIN",
        y="DEST",
        z="ARR_DELAY",
        title=f"Top {top_n} Routes by Mean Arrival Delay",
    )
    return fig
