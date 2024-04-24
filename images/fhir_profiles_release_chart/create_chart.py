import pandas as pd  # Import pandas to use DateOffset
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

adjustmenttime = 3  # Months
chart_end_date = '2026-10-14'

profiles = {
    'de.gematik.erezept-workflow.r4': {
        'PU': [
            ('1.2', '2024-01-01', '2025-04-15'),
            ('1.3 $dispense & Digas & ePA', '2025-01-15', '2025-09-30'),
            ('1.4 BtM-Rezepte', '2025-07-15', chart_end_date)
        ],
        'RU': []
    },
    'kbv.ita.erp': {
        'PU': [
            ('1.1.0', '2024-01-01', '2026-01-14'),
            ('2.0.0 BtM-Rezepte', '2025-07-15', chart_end_date)
        ],
        'RU': []
    },
    'de.abda.eRezeptAbgabedaten': {
        'PU': [
            ('1.3', '2024-01-01', '2024-10-31'),
            ('1.4', '2024-11-01', '2025-07-14'), 
            ('1.5 BtM-Rezepte', '2025-07-15', chart_end_date) 
        ],
        'RU': []
    },
    'de.gkvsv.eRezeptAbrechnungsdaten': {
        'PU': [
            ('1.3', '2024-01-01', '2024-10-31'),
            ('1.4', '2024-11-01', '2025-07-14'), 
            ('1.5 BtM-Rezepte', '2025-07-15', chart_end_date) 
        ],
        'RU': []
    },
    'de.abda.eRezeptAbgabedatenPKV': {
        'PU': [
            ('1.3', '2024-01-01', '2024-10-31'),
            ('1.4', '2024-11-01', '2025-07-14'), 
            ('1.5 BtM-Rezepte', '2025-07-15', chart_end_date) 
        ],
        'RU': []
    },
    'de.gematik.erezept-patientenrechnung.r4': {
        'PU': [
            ('1.0', '2024-01-01', '2024-10-31'),
            ('1.0', '2024-11-01', '2025-07-14'),
            ('1.1 BtM-Rezepte', '2025-07-15', chart_end_date) 
        ],
        'RU': []
    }
}

# Adjusting the profiles dictionary to generate RU data correctly from PU data
for profile, environments in profiles.items():
    pu_versions = environments['PU']
    ru_versions = []
    for version, start_date, end_date in pu_versions:
        start_date_pu = datetime.strptime(start_date, '%Y-%m-%d')
        start_date_ru = (start_date_pu - pd.DateOffset(months=adjustmenttime)).strftime('%Y-%m-%d')
        ru_versions.append((version, start_date_ru, end_date))
    environments['RU'] = ru_versions

# Variables for colors and the position of bars
colors = [
    '#ffb3ba', '#ffdfba', '#ffffba', '#baffc9', '#bae1ff',
    '#ffadad', '#ffd6a5', '#fdffb6', '#caffbf', '#9bf6ff',
    '#a0c4ff', '#bdb2ff', '#ffc6ff', '#ffcccc', '#ffafcc',
    '#ffcad4', '#f3c4fb', '#ecbcfd', '#e2afff', '#deaaff',
    '#b28dff', '#c5a3ff', '#d5aaff', '#f2c0ff', '#ffd3e8',
    '#fde4cf', '#d6e0f0', '#f9c6c9', '#d5e4c3', '#c9d6df',
    '#e7c6ff', '#e6eecf', '#deffcc', '#e0f9ff', '#fbcffc',
    '#fcefee', '#c9c6ff', '#c3fdfd', '#b5d8cc', '#fbdcc4'
]

# Define the figure and axes for the Gantt charts and tables
fig = plt.figure(constrained_layout=True, figsize=(20, 12))
gs = fig.add_gridspec(2, 2, width_ratios=[3, 1])  # Grid specification for two charts and two tables

axes = [fig.add_subplot(gs[i, 0]) for i in range(2)]
table_axes = [fig.add_subplot(gs[i, 1]) for i in range(2)]  # Axes for tables

# Collect all dates for vertical lines
all_dates_pu = set()
all_dates_ru = set()

# Iterate through each project profile in the order they are listed in the dictionary
for i, environment in enumerate(['PU', 'RU']):
    pos = 0
    table_data = []  # Initialize table data for each environment
    y_ticks = {}
    for profile_name, versions in profiles.items():
        # Sort versions in reverse order for consistency across environments
        versions_sorted = sorted(versions[environment], key=lambda x: datetime.strptime(x[1], '%Y-%m-%d'), reverse=True)
        y_ticks[pos+1] = profile_name  # Position for the package header
        for version, start_date, end_date in versions_sorted:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            if environment == 'PU':
                all_dates_pu.update([start, end])
            else:
                all_dates_ru.update([start, end])
            axes[i].barh(pos, (end - start).days, left=start, height=0.75, color=colors[pos % len(colors)], edgecolor='black')
            axes[i].text(start + (end - start) * 0.5, pos, version, ha='center', va='center', color='black')
            # Collect data for the table
            table_data.insert(0, [profile_name, version, start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')])
            pos += 1
        axes[i].axhline(y=pos - 0.5, color='black', linewidth=1)

    # Create table showing profile validity
    table = table_axes[i].table(cellText=table_data, colLabels=['Profil', 'Version', 'Start Date', 'End Date'], loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 2)
    table_axes[i].axis('off')

# Set common properties and save the figure
for ax, environment, all_dates in zip(axes, ['PU', 'RU'], [all_dates_pu, all_dates_ru]):
    ax.set_yticks(list(y_ticks.keys()))
    ax.set_yticklabels(list(y_ticks.values()))
    ax.set_title(f'Gültigkeit der FHIR Profiles für die {environment} Umgebung')
    date_locator = mdates.AutoDateLocator(minticks=len(all_dates), maxticks=len(all_dates) + 5)
    ax.xaxis.set_major_locator(date_locator)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.set_xticklabels([dt.strftime('%Y-%m-%d') for dt in sorted(all_dates)], rotation=90)

plt.tight_layout()
file_path = './FHIR_Profile_Releases_Gantt_Chart_with_Tables.png'
plt.savefig(file_path)
plt.close(fig)