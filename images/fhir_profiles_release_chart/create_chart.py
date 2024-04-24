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
            ('1.1.0', '2024-01-01', chart_end_date),
            ('1.2.0 BtM-Rezepte', '2025-07-15', chart_end_date)
        ],
        'RU': []
    },
    'de.abda.eRezeptAbgabedaten': {
        'PU': [
            ('1.3', '2024-01-01', '2024-10-31'),
            ('1.4', '2024-11-01', chart_end_date) 
        ],
        'RU': []
    },
    'de.gkvsv.eRezeptAbrechnungsdaten': {
        'PU': [
            ('1.3', '2024-01-01', '2024-10-31'),
            ('1.4', '2024-11-01', chart_end_date) 
        ],
        'RU': []
    },
    'de.abda.eRezeptAbgabedatenPKV': {
        'PU': [
            ('1.3', '2024-01-01', '2024-10-31'),
            ('1.4', '2024-11-01', chart_end_date) 
        ],
        'RU': []
    },
    'de.gematik.erezept-patientenrechnung.r4': {
        'PU': [
            ('1.0', '2024-01-01', '2024-10-31'),
            ('1.0', '2024-11-01', chart_end_date) 
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

# Define the figure and axes for the Gantt charts
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(18, 12))
pos_pu = 0
pos_ru = 0

# Collect all dates for vertical lines
all_dates_pu = set()
all_dates_ru = set()

# Dictionary to keep track of positions for y-ticks labels
y_ticks_pu = {}
y_ticks_ru = {}

# For storing data to put in the table for PU and RU environments
table_data_pu = []
table_data_ru = []

# Iterate through each project profile in the order they are listed in the dictionary
for profile_name in reversed(list(profiles.keys())):
    # Process PU environment with reversed sort order
    versions_pu = profiles[profile_name]['PU']
    versions_pu.sort(key=lambda x: datetime.strptime(x[1], '%Y-%m-%d'), reverse=True) 
    y_ticks_pu[pos_pu] = profile_name  # Position for the package header in PU
    for version, start_date, end_date in versions_pu:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        all_dates_pu.update([start, end])
        axes[0].barh(pos_pu, (end - start).days, left=start, height=0.75, color=colors[pos_pu % len(colors)], edgecolor='black')
        axes[0].text(start + (end - start) * 0.5, pos_pu, version, ha='center', va='center', color='black')
        pos_pu += 1
    axes[0].axhline(y=pos_pu - 0.5, color='black', linewidth=1)

    # Process RU environment
    versions_ru = profiles[profile_name]['RU']
    versions_ru.sort(key=lambda x: datetime.strptime(x[1], '%Y-%m-%d'), reverse=True) 
    y_ticks_ru[pos_ru] = profile_name  # Position for the package header in RU
    for version, start_date, end_date in versions_ru:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        all_dates_ru.update([start, end])
        axes[1].barh(pos_ru, (end - start).days, left=start, height=0.75, color=colors[pos_ru % len(colors)], edgecolor='black')
        axes[1].text(start + (end - start) * 0.5, pos_ru, version, ha='center', va='center', color='black')
        pos_ru += 1
    axes[1].axhline(y=pos_ru - 0.5, color='black', linewidth=1)

# Add vertical lines for each transition date and make sure each has a date label
date_locator = mdates.AutoDateLocator(minticks=len(all_dates_pu), maxticks=len(all_dates_pu) + 5)
for ax in axes:
    for date in sorted(all_dates_pu.union(all_dates_ru)):
        ax.axvline(x=date, color='gray', linestyle=':', linewidth=0.5)
    ax.xaxis.set_major_locator(date_locator)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.set_xticklabels([dt.strftime('%Y-%m-%d') for dt in sorted(all_dates_pu.union(all_dates_ru))], rotation=90)

# Set titles and y-axis labels for packages
axes[0].set_title('Gültigkeit der FHIT Profiles für die PU Umgebung')
axes[0].set_yticks(list(y_ticks_pu.keys()))
axes[0].set_yticklabels(list(y_ticks_pu.values()))

axes[1].set_title('Gültigkeit der FHIT Profiles für die RU Umgebung')
axes[1].set_yticks(list(y_ticks_ru.keys()))
axes[1].set_yticklabels(list(y_ticks_ru.values()))

plt.tight_layout()

# Save the figure
file_path = './FHIR_Profile_Releases_Gantt_Chart.png'
plt.savefig(file_path)
plt.close(fig)  # Close the figure to prevent display


# Erstellen eines DataFrames aus den obigen Daten
data = []
for package, environments in profiles.items():
    for environment, versions in environments.items():
        for version, start_date, end_date in versions:
            data.append({
                "Package": package,
                "Environment": environment,
                "Version": version,
                "Start Date": start_date,
                "End Date": end_date
            })

# Konvertieren der Liste in einen DataFrame
df = pd.DataFrame(data)

# Ausgabe des DataFrame
print(df)