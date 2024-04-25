#
# Created by Omer F. Keles (ORCID: 0000-0002-3004-1191)
#

# Import necessary modules
import pandas as pd
import matplotlib.pyplot as plt
from colour import Color
import squarify

# Set "debris_objects" to the result of using pd.read_csv() to read local debris objects file
debris_objects = pd.read_csv("debris_objects.csv")

# Set the default DPI for plots to 300 and style to Dominik Haitz's freely available "Pitaya Smoothie dark" theme
plt.rcParams["figure.dpi"] = 300
plt.style.use("https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle")

# Create new dataframe "debris_objects_knownyear" that keeps only records with a known origin year
# Remove the decimal points for values in the "Year" column by converting the column to a datetime format, converting the values under "Year" to a string, and then showing the first four characters ("YYYY" vs. "YYYY-MM-DD 00:00:00")
debris_objects_knownyear = debris_objects.dropna(subset = ["Year"])
debris_objects_knownyear["Year"] = pd.to_datetime(debris_objects["Year"], format = "%Y").astype(str).str[:4]

# Create a stacked bar plot of the number of debris object records associated with each year
# Each bar is further disaggregated by the "objectClass" variable, which is the classification of the object (whether it's a rocket body, payload, etc.)
# Count the number of records for each combination of "Year" and "objectClass" using .size(), and then unstack the data to create a 2D dataframe (with "Year" as the rows and "objectClass" as the columns)
# Add labels of total records by year above each stacked bar, shifted 40 units above where label text is placed by default (for better spacing) and rotated 90 degrees
fig1, ax1 = plt.subplots(figsize = (15, 9))

objectClass_by_year = debris_objects_knownyear.groupby(["Year", "objectClass"]).size().unstack()
objectClass_by_year.plot(kind = "bar", stacked = True, ax = ax1)

for n, total_records in enumerate(objectClass_by_year.sum(axis = 1)):
    ax1.text(n, total_records + 40, int(total_records), ha = "center", va = "bottom", rotation = 90)

ax1.set_title("Debris Object Records by Known Origin Year")
ax1.set_xlabel("Year")
ax1.set_ylabel("Number of Debris Objects")
ax1.legend(title = "Debris Object Classification", loc = "upper left")
ax1.set_xticklabels(ax1.get_xticklabels(), rotation = 45)
plt.tight_layout()
plt.savefig("debris_objects_by_year.png")

# Create a bar plot broadly categorizing the missions associated with documented debris objects ("Civil", "Commercial", "Defense", "Amateur", "Unknown")
# Fill empty values under "mission" column with "Unknown"
# Define function "categorize_mission" that takes an argument (a "mission" string) and returns a category based on the presence of one of the aforementioned keywords in the rows under "mission"
# Create new column "mission_category" that applies the "categorize_mission" function, and then use "mission_category_counts" to count the number of debris object records by mission category
debris_objects["mission"] = debris_objects["mission"].fillna("Unknown")

def categorize_mission(mission:str):
    if "Civil" in mission:
        return "Civil"
    elif "Commercial" in mission:
        return "Commercial"
    elif "Defense" in mission:
        return "Defense"
    elif "Amateur" in mission:
        return "Amateur"
    else:
        return "Unknown"

debris_objects["mission_category"] = debris_objects["mission"].apply(categorize_mission)
mission_category_counts = debris_objects["mission_category"].value_counts()

fig2, ax2 = plt.subplots(figsize = (10, 9))
plot2 = mission_category_counts.plot(kind = "bar", ax = ax2, width = 0.8, color = ["#1F77B4", "#FF6600", "#2CA02C", "#E60000", "#9467BD"])
plot2.bar_label(plot2.containers[0], label_type = "edge", padding = 4)
ax2.set_title("Categories of Missions Associated with Debris Objects")
ax2.set_xlabel("Mission Categories")
ax2.set_ylabel("Number of Debris Objects")
ax2.set_xticklabels(ax2.get_xticklabels(), rotation = 0)
plt.tight_layout()
plt.savefig("debris_objects_by_mission_category.png")

# Create horizontal bar plots to further disaggregate the purposes of each of the mission categories
# Create separate filtered dataframes and count the number of debris object records for each mission category
# Limit to the top 5 purposes for consistency, as a significant dropoff in unique purposes occurs afterwards for commercial/amateur missions
# Generate gradient bars using the PyPI colour package
civil_purposes = debris_objects[debris_objects["mission"].str.contains("Civil")]
civil_mission_counts = civil_purposes["mission"].value_counts()
civil_mission_counts = civil_mission_counts[:5].sort_values(ascending = True)
fig3, ax3 = plt.subplots(figsize = (10, 9))
colors = list(Color("#E60000").range_to(Color("#FF2C2C"), 5))
colors = [color.rgb for color in colors]
plot3 = civil_mission_counts.plot(kind = "barh", ax = ax3, color = colors)
plot3.bar_label(plot3.containers[0], label_type = "edge", padding = 4)
ax3.set_title("Debris Objects by Purpose of Civil Missions (Top 5)")
ax3.set_xlabel("Number of Debris Objects")
ax3.set_ylabel("Purpose of Civil Mission")
plt.tight_layout()
plt.savefig("debris_objects_by_civil.png")

commercial_purposes = debris_objects[debris_objects["mission"].str.contains("Commercial")]
commercial_mission_counts = commercial_purposes["mission"].value_counts()
commercial_mission_counts = commercial_mission_counts[:5].sort_values(ascending = True)
fig4, ax4 = plt.subplots(figsize = (10, 9))
colors = list(Color("#FF6600").range_to(Color("#FCAE1E"), 5))
colors = [color.rgb for color in colors]
plot4 = commercial_mission_counts.plot(kind = "barh", ax = ax4, width = 0.8, color = colors)
plot4.bar_label(plot4.containers[0], label_type = "edge", padding = 4)
ax4.set_title("Debris Objects by Purpose of Commercial Missions (Top 5)")
ax4.set_xlabel("Number of Debris Objects")
ax4.set_ylabel("Purpose of Commercial Mission")
plt.tight_layout()
plt.savefig("debris_objects_by_commercial.png")

defense_purposes = debris_objects[debris_objects["mission"].str.contains("Defense")]
defense_mission_counts = defense_purposes["mission"].value_counts()
defense_mission_counts = defense_mission_counts[:5].sort_values(ascending = True)
fig5, ax5 = plt.subplots(figsize = (10, 9))
colors = list(Color("#2CA02C").range_to(Color("#90EE90"), 5))
colors = [color.rgb for color in colors]
plot5 = defense_mission_counts.plot(kind = "barh", ax = ax5, color = colors)
plot5.bar_label(plot5.containers[0], label_type = "edge", padding = 4)
ax5.set_title("Debris Objects by Purpose of Defense Missions (Top 5)")
ax5.set_xlabel("Number of Debris Objects")
ax5.set_ylabel("Purpose of Defense Mission")
plt.tight_layout()
plt.savefig("debris_objects_by_defense.png")

amateur_purposes = debris_objects[debris_objects["mission"].str.contains("Amateur")]
amateur_mission_counts = amateur_purposes["mission"].value_counts()
amateur_mission_counts = amateur_mission_counts[:5].sort_values(ascending = True)
fig6, ax6 = plt.subplots(figsize = (10, 9))
colors = list(Color("#9467BD").range_to(Color("#CBC3E3"), 5))
colors = [color.rgb for color in colors]
plot6 = amateur_mission_counts.plot(kind = "barh", ax = ax6, width = 0.8, color = colors)
plot6.bar_label(plot6.containers[0], label_type = "edge", padding = 4)
ax6.set_title("Debris Objects by Purpose of Amateur Missions (Top 5)")
ax6.set_xlabel("Number of Debris Objects")
ax6.set_ylabel("Purpose of Amateur Mission")
plt.tight_layout()
plt.savefig("debris_objects_by_amateur.png")

# Create a treemap (using the Squarify library) of the top 10 most frequently occurring names for debris object ownership
# Add wrapped labels consisting of debris ownership name and the number of debris objects associated with a given source 
debris_object_ownership = debris_objects["name"].value_counts()
debris_object_ownership = debris_object_ownership[:10]
fig7, ax7 = plt.subplots(figsize = (10, 9))
colors = list(Color("#1F77B4").range_to(Color("#00008B"), 10))
colors = [color.rgb for color in colors]
squarify.plot(sizes = debris_object_ownership.values, label = [f"{name}\n({count} debris objects)" for name, count in debris_object_ownership.items()], color = colors, ax = ax7, text_kwargs = {"wrap": True, "fontsize":8})
ax7.set_title("Most Frequently Documented Names for Debris Ownership (Top 10)")
plt.tight_layout()
plt.savefig("debris_objects_by_ownership.png")