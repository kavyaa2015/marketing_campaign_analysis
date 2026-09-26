"""Interactive dashboard for the Marketing Campaign Analytics project.

Run: streamlit run app.py
All summaries are recalculated from the sidebar-selected customer audience.
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "processed" / "marketing_cleaned.csv"
PRODUCT_COLUMNS = {"Wine": "MntWines", "Fruits": "MntFruits", "Meat": "MntMeatProducts", "Fish": "MntFishProducts", "Sweets": "MntSweetProducts", "Gold": "MntGoldProds"}
CHANNEL_COLUMNS = {"Web": "NumWebPurchases", "Catalog": "NumCatalogPurchases", "Store": "NumStorePurchases", "Deals": "NumDealsPurchases"}
CAMPAIGN_COLUMNS = {"Campaign 1": "AcceptedCmp1", "Campaign 2": "AcceptedCmp2", "Campaign 3": "AcceptedCmp3", "Campaign 4": "AcceptedCmp4", "Campaign 5": "AcceptedCmp5", "Latest campaign": "Response"}
AGE_ORDER = ["<30", "30–39", "40–49", "50–59", "60–69", "70+"]
INCOME_ORDER = ["Low", "Medium", "High", "Very High"]

st.set_page_config(page_title="Marketing Campaign Intelligence", page_icon="📈", layout="wide")


@st.cache_data(show_spinner="Loading customer data…")
def load_data(path: Path) -> pd.DataFrame:
    """Load data and add non-persistent dashboard features."""
    data = pd.read_csv(path)
    required = {"ID", "Age", "Income", "Response", "Total_Spend", "Total_Purchases"}
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(f"Dataset is missing: {', '.join(sorted(missing))}")
    data["Age_Band"] = pd.cut(data["Age"], [0, 29, 39, 49, 59, 69, float("inf")], labels=AGE_ORDER, ordered=True)
    data["Income_Band"] = pd.cut(data["Income"], [-float("inf"), 30000, 50000, 75000, float("inf")], labels=INCOME_ORDER, ordered=True)
    data["Response_Label"] = data["Response"].map({0: "Did not respond", 1: "Responded"})
    return data


def rate_by(data: pd.DataFrame, column: str, order: list[str] | None = None) -> pd.DataFrame:
    result = data.groupby(column, observed=False).agg(Customers=("ID", "count"), Response_Rate=("Response", "mean"), Average_Spend=("Total_Spend", "mean"), Average_Income=("Income", "mean")).reset_index()
    result["Response_Rate"] *= 100
    if order:
        result[column] = pd.Categorical(result[column], categories=order, ordered=True)
        result = result.sort_values(column)
    return result


def segment_summary(data: pd.DataFrame) -> pd.DataFrame:
    """Overlapping business-rule segments; customers can belong to several."""
    cutoff = data["Total_Spend"].quantile(0.90)
    rules = {"High income": data["Income"] > 75000, "Young customer": data["Age"] < 30, "Campaign responder": data["Response"].eq(1), "High web engagement": data["NumWebVisitsMonth"] > 5, "Family customer": data["Total_Children"] > 0, "High spender (top 10%)": data["Total_Spend"] >= cutoff}
    rows = []
    for name, mask in rules.items():
        group = data.loc[mask]
        rows.append({"Segment": name, "Customers": len(group), "Share of audience": len(group) / len(data) * 100, "Avg. spend": group["Total_Spend"].mean(), "Response rate": group["Response"].mean() * 100})
    return pd.DataFrame(rows).sort_values("Response rate", ascending=False)


data = load_data(DATA_PATH)
with st.sidebar:
    st.header("Explore the audience")
    st.caption("All visuals and KPIs use these filters.")
    selections = {"Country": st.multiselect("Country", sorted(data["Country"].dropna().unique())), "Education": st.multiselect("Education", sorted(data["Education"].dropna().unique())), "Marital_Status": st.multiselect("Marital status", sorted(data["Marital_Status"].dropna().unique())), "Age_Band": st.multiselect("Age band", AGE_ORDER), "Income_Band": st.multiselect("Income band", INCOME_ORDER)}
    outcome = st.radio("Latest campaign outcome", ["All customers", "Responded", "Did not respond"])
    st.divider()
    st.caption("High spender means top 10% of spend in the selected audience.")

filtered = data.copy()
for column, values in selections.items():
    if values:
        filtered = filtered[filtered[column].astype(str).isin(values)]
if outcome != "All customers":
    filtered = filtered[filtered["Response_Label"] == outcome]

st.title("Marketing Campaign Intelligence")
st.caption("Customer value, campaign response, and channel behaviour for campaign-planning decisions.")
if filtered.empty:
    st.warning("No customers match these filters. Adjust one or more selections.")
    st.stop()

overall_rate = data["Response"].mean() * 100
response_rate = filtered["Response"].mean() * 100
tabs = st.tabs(["Executive overview", "Campaign performance", "Customer behaviour", "Targeting", "Data explorer"])

with tabs[0]:
    st.subheader("Audience snapshot")
    metrics = st.columns(5)
    metrics[0].metric("Customers", f"{len(filtered):,}")
    metrics[1].metric("Latest campaign response", f"{response_rate:.1f}%", f"{response_rate - overall_rate:+.1f} pp")
    metrics[2].metric("Average spend", f"₹{filtered['Total_Spend'].mean():,.0f}")
    metrics[3].metric("Average income", f"₹{filtered['Income'].mean():,.0f}")
    metrics[4].metric("Average purchases", f"{filtered['Total_Purchases'].mean():.1f}")
    st.caption("Response delta compares the selected audience with the full customer base. Monetary values use the dataset’s units.")
    left, right = st.columns(2)
    for container, column, order, title, scale in [(left, "Age_Band", AGE_ORDER, "Response by age band", "Tealgrn"), (right, "Income_Band", INCOME_ORDER, "Response by income band", "Blues")]:
        summary = rate_by(filtered, column, order)
        fig = px.bar(summary, x=column, y="Response_Rate", text="Response_Rate", color="Response_Rate", color_continuous_scale=scale, title=title)
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(yaxis_title="Response rate (%)", coloraxis_showscale=False)
        container.plotly_chart(fig, use_container_width=True)
    st.info("Identify groups with above-average response, then check their customer count before making a targeting decision.")

with tabs[1]:
    campaign = pd.DataFrame({"Campaign": list(CAMPAIGN_COLUMNS), "Accepted customers": [int(filtered[c].sum()) for c in CAMPAIGN_COLUMNS.values()], "Acceptance rate": [filtered[c].mean() * 100 for c in CAMPAIGN_COLUMNS.values()]}).sort_values("Acceptance rate", ascending=False)
    left, right = st.columns([3, 2])
    with left:
        fig = px.bar(campaign, x="Campaign", y="Acceptance rate", text="Acceptance rate", color="Acceptance rate", color_continuous_scale="Viridis", title="Acceptance rate across campaigns")
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(yaxis_title="Acceptance rate (%)", coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    with right:
        st.subheader("Campaign scorecard")
        st.dataframe(campaign.style.format({"Acceptance rate": "{:.1f}%"}), hide_index=True, use_container_width=True)
        leader = campaign.iloc[0]
        st.success(f"**{leader['Campaign']}** leads this audience at **{leader['Acceptance rate']:.1f}%**.")
    country = rate_by(filtered, "Country").query("Customers >= 30").sort_values("Response_Rate", ascending=False)
    fig = px.bar(country, x="Country", y="Response_Rate", hover_data=["Customers", "Average_Spend"], color="Response_Rate", color_continuous_scale="Tealgrn", title="Latest-campaign response by country (30+ customers)")
    fig.update_layout(yaxis_title="Response rate (%)", coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

with tabs[2]:
    left, right = st.columns(2)
    product = pd.DataFrame({"Product": list(PRODUCT_COLUMNS), "Total spend": [filtered[c].sum() for c in PRODUCT_COLUMNS.values()]}).sort_values("Total spend")
    fig = px.bar(product, x="Total spend", y="Product", orientation="h", text="Total spend", title="Product-category spending")
    fig.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
    left.plotly_chart(fig, use_container_width=True)
    channel = pd.DataFrame({"Channel": list(CHANNEL_COLUMNS), "Purchases": [filtered[c].sum() for c in CHANNEL_COLUMNS.values()]}).sort_values("Purchases", ascending=False)
    fig = px.bar(channel, x="Channel", y="Purchases", text="Purchases", title="Purchase-channel use")
    fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    right.plotly_chart(fig, use_container_width=True)
    comparison = filtered.groupby("Response_Label")[list(CHANNEL_COLUMNS.values())].mean().rename(columns={v: k for k, v in CHANNEL_COLUMNS.items()}).T.reset_index(names="Channel")
    long = comparison.melt(id_vars="Channel", var_name="Customer outcome", value_name="Average purchases")
    fig = px.bar(long, x="Channel", y="Average purchases", color="Customer outcome", barmode="group", title="Average channel purchases by latest campaign outcome")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("This describes observed behaviour. It does not prove a channel caused the campaign response.")

with tabs[3]:
    segments = segment_summary(filtered)
    fig = px.bar(segments, x="Segment", y="Response rate", color="Avg. spend", hover_data=["Customers", "Share of audience"], title="Segment response rate and average spend")
    fig.update_layout(xaxis_tickangle=-25, yaxis_title="Response rate (%)")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(segments.style.format({"Share of audience": "{:.1f}%", "Avg. spend": "₹{:,.0f}", "Response rate": "{:.1f}%"}), hide_index=True, use_container_width=True)
    st.caption("Segments overlap by design, so a customer may be in multiple segments.")
    left, right = st.columns(2)
    cutoff = filtered["Total_Spend"].quantile(0.90)
    ideal = filtered[(filtered["Total_Spend"] >= cutoff) & filtered["Response"].eq(1)]
    with left:
        st.subheader("Ideal target profile")
        if ideal.empty:
            st.info("No high-value responders match the current filters.")
        else:
            profile = pd.DataFrame({"Measure": ["Customers", "Average age", "Average income", "Average spend", "Average purchases", "Average children"], "Value": [len(ideal), ideal.Age.mean(), ideal.Income.mean(), ideal.Total_Spend.mean(), ideal.Total_Purchases.mean(), ideal.Total_Children.mean()]})
            st.dataframe(profile.style.format({"Value": "{:.1f}"}), hide_index=True, use_container_width=True)
            st.caption("High-value latest-campaign responders: top 10% of spend within selected audience.")
    with right:
        st.subheader("Under-served opportunity")
        underserved = filtered[(filtered.NumWebVisitsMonth > 5) & (filtered.Total_Spend <= filtered.Total_Spend.median()) & filtered.Response.eq(0)]
        st.metric("High-visit, low-spend non-responders", f"{len(underserved):,}", f"{len(underserved) / len(filtered) * 100:.1f}% of selected")
        st.write("Test a tailored web offer or simpler checkout flow for this interested but low-converting audience, then measure incremental response.")

with tabs[4]:
    st.subheader("Filtered customer data")
    st.caption("Download the audience used in every chart for further analysis.")
    columns = ["ID", "Country", "Age", "Education", "Marital_Status", "Income", "Total_Children", "Total_Spend", "Total_Purchases", "NumWebVisitsMonth", "Response"]
    st.dataframe(filtered[columns], hide_index=True, use_container_width=True, height=420)
    st.download_button("Download filtered data (CSV)", filtered.to_csv(index=False).encode("utf-8"), "marketing_campaign_filtered.csv", "text/csv")

st.divider()
st.caption("Marketing Campaign Analytics • Exploratory analysis, not causal inference")
