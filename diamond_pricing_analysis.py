
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DATA_URL = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/diamonds.csv"
OUTPUT_DIR = "charts"

os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv(DATA_URL)


print("=" * 60)
print("DATA OVERVIEW")
print("=" * 60)
print("Rows before cleaning:", len(df))


df = df[(df['x'] > 0) & (df['y'] > 0) & (df['z'] > 0)]
df = df.drop_duplicates()

print("Rows after cleaning:", len(df))
print()
print(df.head())
print()
print(df.describe())
print()

df['price_per_carat'] = round(df['price'] / df['carat'], 2)


avg_price = round(df['price'].mean(), 2)
median_price = round(df['price'].median(), 2)

print("=" * 60)
print("INSIGHT 1: Overall Price Distribution")
print("=" * 60)
print("Average price: $", avg_price)
print("Median price: $", median_price)
print("The average is notably higher than the median, indicating the")
print("price distribution is skewed by a smaller number of expensive stones.")
print()

plt.figure(figsize=(8, 5))
sns.histplot(df['price'], bins=50, kde=True, color="#4C72B0")
plt.axvline(avg_price, color="red", linestyle="--", label="Mean = $" + str(avg_price))
plt.axvline(median_price, color="green", linestyle="--", label="Median = $" + str(median_price))
plt.title("Distribution of Diamond Prices")
plt.xlabel("Price ($)")
plt.ylabel("Number of Diamonds")
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUT_DIR + "/1_price_distribution.png", dpi=150)
plt.show()


correlations = df[['carat', 'depth', 'table', 'price']].corr()['price'].sort_values(ascending=False)

print("=" * 60)
print("INSIGHT 2: What Correlates Most with Price")
print("=" * 60)
print(correlations)
print()
print("Carat weight is by far the strongest numeric predictor of price.")
print()


cut_order = ["Fair", "Good", "Very Good", "Premium", "Ideal"]
cut_summary = df.groupby('cut', observed=True)['price_per_carat'].agg(
    ['mean', 'median', 'count']
).round(2).reindex(cut_order)

print("=" * 60)
print("INSIGHT 3: Price per Carat by Cut Quality")
print("=" * 60)
print(cut_summary)
print()

plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="cut", y="price_per_carat", order=cut_order, color="#55A868")
plt.title("Price per Carat by Cut Quality")
plt.xlabel("Cut Quality")
plt.ylabel("Price per Carat ($)")
plt.tight_layout()
plt.savefig(OUTPUT_DIR + "/2_price_per_carat_by_cut.png", dpi=150)
plt.show()


color_order = ["J", "I", "H", "G", "F", "E", "D"]
color_summary = df.groupby('color', observed=True)['price_per_carat'].agg(
    ['mean', 'median', 'count']
).round(2).reindex(color_order)

print("=" * 60)
print("INSIGHT 4: Price per Carat by Color Grade (J=worst, D=best)")
print("=" * 60)
print(color_summary)
print()

plt.figure(figsize=(8, 5))
sns.barplot(data=df, x="color", y="price_per_carat", order=color_order, errorbar=None, color="#C44E52")
plt.title("Average Price per Carat by Color Grade")
plt.xlabel("Color Grade (J = worst, D = best)")
plt.ylabel("Average Price per Carat ($)")
plt.tight_layout()
plt.savefig(OUTPUT_DIR + "/3_price_per_carat_by_color.png", dpi=150)
plt.show()


carat_price_corr = round(df['carat'].corr(df['price']), 2)

print("=" * 60)
print("INSIGHT 5: Carat vs Price Relationship")
print("=" * 60)
print("Correlation between carat and price:", carat_price_corr)
print("This confirms carat weight is the dominant driver of price,")
print("though the relationship is not perfectly linear - price accelerates")
print("as carat weight increases.")
print()

plt.figure(figsize=(8, 5))
sample = df.sample(n=3000, random_state=42)  # sample for a readable scatter plot
sns.scatterplot(data=sample, x="carat", y="price", hue="cut", alpha=0.5, hue_order=cut_order)
plt.title("Carat Weight vs Price (correlation = " + str(carat_price_corr) + ")")
plt.xlabel("Carat")
plt.ylabel("Price ($)")
plt.tight_layout()
plt.savefig(OUTPUT_DIR + "/4_carat_vs_price.png", dpi=150)
plt.show()


best_cut = cut_summary['mean'].idxmax()
best_color = color_summary['mean'].idxmax()

print("=" * 60)
print("SUMMARY & RECOMMENDATIONS")
print("=" * 60)
print()
print("1. Diamond prices are right-skewed (mean $" + str(avg_price) + " vs median $" + str(median_price) + "),")
print("   meaning a smaller number of large/high-value stones pull the average up.")
print("   Pricing strategy should reference median, not average, for typical inventory.")
print()
print("2. Carat weight is by far the strongest driver of price (correlation " + str(carat_price_corr) + ").")
print("   Any pricing model should weight carat far above cut, color, or clarity alone.")
print()
print("3. '" + best_cut + "' cut commands the highest average price per carat -")
print("   inventory with this cut grade can likely be priced at a premium.")
print()
print("4. Color grade '" + best_color + "' commands the highest price per carat,")
print("   consistent with color grading standards (D is the highest/rarest grade).")
print("   Stones with lower color grades but strong cut/clarity may be underpriced")
print("   opportunities if customers primarily notice cut quality.")
print()
print("5. Because price accelerates with carat size (not a flat rate), retailers")
print("   should avoid simple per-carat multipliers for larger stones - they")
print("   likely command a premium beyond linear scaling.")
print()
print("Charts saved to the '" + OUTPUT_DIR + "/' folder.")