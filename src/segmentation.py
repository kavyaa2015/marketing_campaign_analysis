"""
segmentation.py

Purpose:
    Create rule-based customer segments
    required by the marketing analytics project.
"""

import pandas as pd


DATA_PATH = "data/processed/marketing_cleaned.csv"


def load_data():

    return pd.read_csv(DATA_PATH)


def create_segments(df):

    # --------------------------------------------------------
    # 1. HIGH INCOME
    # Income > 75,000
    # --------------------------------------------------------

    df["High_Income"] = (
        df["Income"] > 75000
    )

    # --------------------------------------------------------
    # 2. YOUNG CUSTOMER
    # Age < 30
    # --------------------------------------------------------

    df["Young_Customer"] = (
        df["Age"] < 30
    )

    # --------------------------------------------------------
    # 3. CAMPAIGN RESPONDER
    # Response = 1
    # --------------------------------------------------------

    df["Campaign_Responder"] = (
        df["Response"] == 1
    )

    # --------------------------------------------------------
    # 4. HIGH WEB ENGAGEMENT
    # Website visits > 5
    # --------------------------------------------------------

    df["High_Web_Engagement"] = (
        df["NumWebVisitsMonth"] > 5
    )

    # --------------------------------------------------------
    # 5. FAMILY CUSTOMER
    # Children > 0
    # --------------------------------------------------------

    df["Family_Customer"] = (
        df["Total_Children"] > 0
    )

    # --------------------------------------------------------
    # 6. HIGH SPENDER
    # Above 90th percentile
    # --------------------------------------------------------

    spend_threshold = (
        df["Total_Spend"].quantile(0.90)
    )

    print(
        f"High spender threshold: "
        f"{spend_threshold:.2f}"
    )

    df["High_Spender"] = (
        df["Total_Spend"] > spend_threshold
    )

    return df


def create_segment_summary(df):

    segments = {
        "High Income": df["High_Income"],
        "Young Customer": df["Young_Customer"],
        "Campaign Responder": df["Campaign_Responder"],
        "High Web Engagement": df["High_Web_Engagement"],
        "Family Customer": df["Family_Customer"],
        "High Spender": df["High_Spender"]
    }

    results = []

    for segment_name, condition in segments.items():

        segment_data = df[condition]

        results.append({
            "Segment": segment_name,
            "Customers": len(segment_data),
            "Percentage": (
                len(segment_data) /
                len(df) *
                100
            ),
            "Average_Spend": (
                segment_data["Total_Spend"].mean()
            ),
            "Average_Income": (
                segment_data["Income"].mean()
            ),
            "Response_Rate": (
                segment_data["Response"].mean() * 100
            )
        })

    summary = pd.DataFrame(results)

    return summary


def main():

    print("=" * 60)
    print("CUSTOMER SEGMENTATION")
    print("=" * 60)

    df = load_data()

    df = create_segments(df)

    summary = create_segment_summary(df)

    print("\nSegment Summary:")
    print(summary.to_string(index=False))

    # Save final dataset
    df.to_csv(
        DATA_PATH,
        index=False
    )

    print("\nSegmentation completed.")


if __name__ == "__main__":
    main()