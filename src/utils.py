import pandas as pd

from typing import Set, Tuple, Dict, Any

def add_missing_recurring(
    budget: pd.DataFrame,
    purchase_name: str,
    target_months: Set[Tuple[int, int]],
    default_values: Dict[str, Any]
) -> pd.DataFrame:
    """
    Add missing recurring payment entries to the budget DataFrame.

    Parameters:
        budget (pd.DataFrame): The main budget DataFrame.
        purchase_name (str): Name of the recurring purchase (e.g., 'gas').
        target_months (set of (int, int)): Set of (year, month) tuples that should be present.
        default_values (dict): Default values for the new row (excluding id, year, month, date).

    Returns:
        pd.DataFrame: Updated budget DataFrame with missing entries added.
    """
    existing_months = set(
        zip(
            budget.loc[budget["purchase_name"] == purchase_name, "purchase_year"],
            budget.loc[budget["purchase_name"] == purchase_name, "purchase_month"]
        )
    )
    missing_months = target_months - existing_months
    if missing_months:
        df_to_add = pd.DataFrame(columns=budget.columns)
        for i, (year, month) in enumerate(sorted(missing_months)):
            row = default_values.copy()
            row.update({
                "id": budget["id"].max() + 1 + i,
                "purchase_year": year,
                "purchase_month": month,
                "purchase_date": pd.Timestamp(f"{year}-{month:02d}-02 21:00:00+00:00")
            })
            df_to_add.loc[len(df_to_add)] = row
        budget = pd.concat([budget, df_to_add], ignore_index=True)
    return budget
