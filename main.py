import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('churn_data.csv')

# Convert TotalCharges to numeric
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')


def calculate_churn_rate(series):
    """Calculate the churn rate of a Series."""
    series = series.dropna()

    if len(series) == 0:
        return 0

    return (series == 'Yes').mean() * 100


def plot_churn_by_category(df, column, title):
    """Plot churn rate for each category of a column."""

    churn_by_group = (
        df.groupby(column)['Churn']
        .apply(calculate_churn_rate)
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.barh(churn_by_group.index, churn_by_group.values)

    ax.set_xlabel('Churn Rate (%)')
    ax.set_ylabel(column)
    ax.set_title(title)

    plt.tight_layout()
    plt.show()


def plot_churn_by_scatter(df, x_column, y_column, title):
    """Plot a scatter plot between two numerical variables."""

    churn_numeric = (df['Churn'] == 'Yes').astype(int)

    fig, ax = plt.subplots(figsize=(10, 6))

    scatter = ax.scatter(
        df[x_column],
        df[y_column],
        c=churn_numeric,
        cmap='coolwarm',
        alpha=0.5
    )

    ax.set_xlabel(x_column)
    ax.set_ylabel(y_column)
    ax.set_title(title)

    fig.colorbar(scatter, ax=ax, label='Churn (1 = Yes, 0 = No)')

    plt.tight_layout()
    plt.show()


def plot_churn_by_range(df, column, step, title, xlabel):
    """Plot churn rate across numerical ranges."""

    max_value = df[column].max()
    bins = range(0, int(max_value) + step, step)

    df = df.copy()

    df['Range'] = pd.cut(
        df[column],
        bins=bins,
        right=False
    )

    churn_by_range = (
        df.groupby('Range', observed=False)['Churn']
        .apply(calculate_churn_rate)
    )

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(
        range(len(churn_by_range)),
        churn_by_range.values
    )

    ax.set_xlabel(xlabel)
    ax.set_ylabel('Churn Rate (%)')
    ax.set_title(title)

    ax.set_xticks(range(len(churn_by_range)))
    ax.set_xticklabels(
        [str(interval) for interval in churn_by_range.index],
        rotation=45,
        ha='right'
    )

    plt.tight_layout()
    plt.show()

plot_churn_by_scatter(df, 'Tenure', 'MonthlyCharges', 'Churn Rate by Tenure and Monthly Charges')