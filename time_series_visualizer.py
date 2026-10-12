import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')
df['date'] = pd.to_datetime(df['date'])


# Clean data by removing the lowest and highest 2.5% of page-view values.
df = df[(df['value'] >= df['value'].quantile(0.025))
        & (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot(df: pd.DataFrame = df):
    fig, ax = plt.subplots(figsize = (12, 5))
    ax.plot(df['date'], df['value'], c = 'red')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    
    plt.tight_layout()
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot(df: pd.DataFrame = df):
    
    df_bar = df.copy()
    df_bar['year'] = df_bar['date'].dt.year
    df_bar['month'] = df_bar['date'].dt.strftime('%B')
    
    df_grouped = (
        df_bar.groupby(['year', 'month'])['value'].mean().unstack(level='month')
    )
    month_order = [
      'January',
      'February',
      'March',
      'April',
      'May',
      'June',
      'July',
      'August',
      'September',
      'October',
      'November',
      'December',
    ]
    
    df_grouped = df_grouped.reindex(columns = month_order)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    df_grouped.plot(kind='bar', ax=ax, width=0.8)
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(title = 'Month', loc = 'upper left')
    ax.grid(True, ls = ':')
    
    plt.tight_layout()
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot(df: pd.DataFrame = df):
  # Prepare data for box plots (as provided by boilerplate standards)
  df_box = df.copy()
  df_box['date'] = pd.to_datetime(df_box['date'])
  df_box['year'] = df_box['date'].dt.year
  df_box['month'] = df_box['date'].dt.strftime('%b')  # Abbreviated month names
  df_box['month_num'] = df_box['date'].dt.month

  # Sort by month number so they display chronologically
  df_box = df_box.sort_values('month_num')

  # Set up the matplotlib figure with 2 subplots side by side
  fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 8))

  # 1. Year-wise Box Plot (Trend)
  year_values = [group['value'].to_numpy()
                 for _, group in df_box.groupby('year', sort=True)]
  axes[0].boxplot(
      year_values,
      showfliers=False,
  )
  years = sorted(df_box['year'].unique())
  axes[0].set_xticks(range(1, len(years) + 1), years)
  axes[0].set_title('Year-wise Box Plot (Trend)')
  axes[0].set_xlabel('Year')
  axes[0].set_ylabel('Page Views')
  axes[0].set_ylim(0, 200000)
  axes[0].set_yticks(range(0, 200001, 20000))

  # 2. Month-wise Box Plot (Seasonality)
  month_order = [
      'Jan',
      'Feb',
      'Mar',
      'Apr',
      'May',
      'Jun',
      'Jul',
      'Aug',
      'Sep',
      'Oct',
      'Nov',
      'Dec',
  ]
  month_values = [df_box.loc[df_box['month'] == month, 'value'].to_numpy()
                  for month in month_order]
  axes[1].boxplot(month_values, showfliers=False)
  axes[1].set_xticks(range(1, len(month_order) + 1), month_order)
  axes[1].set_title('Month-wise Box Plot (Seasonality)')
  axes[1].set_xlabel('Month')
  axes[1].set_ylabel('Page Views')
  axes[1].set_ylim(0, 200000)
  axes[1].set_yticks(range(0, 200001, 20000))

  plt.tight_layout()

  # Save image and return fig (Do not modify the next two lines)
  fig.savefig('box_plot.png')
  return fig
