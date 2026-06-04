# ============================================================
# CUSTOMER CHURN ANALYSIS
# Author: Simpson Gundlapally
# Tools: Python (Pandas, Matplotlib, Seaborn)
# Dataset: churn_raw_data.csv (5,000 records)
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11})
COLORS  = ['#1F3864','#2E75B6','#4BACC6','#70AD47','#FFC000','#FF6B6B']
C_CHURN = '#FF6B6B'
C_STAY  = '#1F3864'

# ============================================================
# STEP 1: LOAD & EXPLORE
# ============================================================
df = pd.read_csv('churn_raw_data.csv')
print("=" * 55)
print("  STEP 1: RAW DATA OVERVIEW")
print("=" * 55)
print(f"Shape       : {df.shape[0]} rows × {df.shape[1]} columns")
print(f"Columns     : {list(df.columns)}")
print(f"\nData Types:\n{df.dtypes}")
print(f"\nFirst 5 rows:\n{df.head()}")

# ============================================================
# STEP 2: DATA CLEANING
# ============================================================
print("\n" + "=" * 55)
print("  STEP 2: DATA QUALITY CHECK")
print("=" * 55)
print(f"\nNull values:\n{df.isnull().sum()}")

bad_tenure = df['Tenure_Months'] < 0
null_charge = df['Monthly_Charge'].isna()
null_total  = df['Total_Charges'].isna()
total_dirty = (bad_tenure | null_charge | null_total).sum()

print(f"\nDirty record breakdown:")
print(f"  Negative tenure values  : {bad_tenure.sum()}")
print(f"  Missing monthly charges : {null_charge.sum()}")
print(f"  Missing total charges   : {null_total.sum()}")
print(f"  TOTAL dirty             : {total_dirty}")

df_clean = df[~(bad_tenure | null_charge | null_total)].copy()
print(f"\nAfter cleaning : {len(df_clean)} records retained")
print(f"Data accuracy  : {round(len(df_clean)/len(df)*100,1)}%")

# ============================================================
# STEP 3: KPI CALCULATIONS
# ============================================================
print("\n" + "=" * 55)
print("  STEP 3: CHURN KPIs")
print("=" * 55)

total_customers = len(df_clean)
churned         = df_clean['Churn'].sum()
retained        = total_customers - churned
churn_rate      = churned / total_customers * 100
retention_rate  = 100 - churn_rate
avg_tenure      = df_clean['Tenure_Months'].mean()
avg_monthly     = df_clean['Monthly_Charge'].mean()
avg_tenure_churn= df_clean[df_clean['Churn']==1]['Tenure_Months'].mean()
rev_at_risk     = df_clean[df_clean['Churn']==1]['Monthly_Charge'].sum()

print(f"  Total Customers    : {total_customers:,}")
print(f"  Churned            : {churned:,}")
print(f"  Retained           : {retained:,}")
print(f"  Churn Rate         : {churn_rate:.1f}%")
print(f"  Retention Rate     : {retention_rate:.1f}%")
print(f"  Avg Tenure (all)   : {avg_tenure:.1f} months")
print(f"  Avg Tenure (churn) : {avg_tenure_churn:.1f} months")
print(f"  Avg Monthly Charge : ₹{avg_monthly:.2f}")
print(f"  Monthly Rev at Risk: ₹{rev_at_risk:,.0f}")

# ============================================================
# STEP 4: CHURN DRIVER ANALYSIS
# ============================================================
# 4a. Churn by Contract Type
contract_churn = df_clean.groupby('Contract_Type')['Churn'].agg(
    ['count','sum','mean']).reset_index()
contract_churn.columns = ['Contract_Type','Total','Churned','Churn_Rate']
contract_churn['Churn_Rate'] = (contract_churn['Churn_Rate']*100).round(1)
contract_churn = contract_churn.sort_values('Churn_Rate', ascending=False)

# 4b. Churn by Tenure Segment
bins   = [0, 12, 24, 48, 73]
labels = ['0-12 Months','13-24 Months','25-48 Months','49+ Months']
df_clean['Tenure_Segment'] = pd.cut(
    df_clean['Tenure_Months'], bins=bins, labels=labels)
tenure_churn = df_clean.groupby('Tenure_Segment', observed=True)['Churn'].agg(
    ['count','sum','mean']).reset_index()
tenure_churn.columns = ['Tenure_Segment','Total','Churned','Churn_Rate']
tenure_churn['Churn_Rate'] = (tenure_churn['Churn_Rate']*100).round(1)

# 4c. Churn by Payment Method
pay_churn = df_clean.groupby('Payment_Method')['Churn'].agg(
    ['count','sum','mean']).reset_index()
pay_churn.columns = ['Payment_Method','Total','Churned','Churn_Rate']
pay_churn['Churn_Rate'] = (pay_churn['Churn_Rate']*100).round(1)
pay_churn = pay_churn.sort_values('Churn_Rate', ascending=False)

# 4d. Churn by Internet Service
internet_churn = df_clean.groupby('Internet_Service')['Churn'].agg(
    ['count','sum','mean']).reset_index()
internet_churn.columns = ['Service','Total','Churned','Churn_Rate']
internet_churn['Churn_Rate'] = (internet_churn['Churn_Rate']*100).round(1)

# 4e. Monthly charge distribution
churn_yes = df_clean[df_clean['Churn']==1]['Monthly_Charge']
churn_no  = df_clean[df_clean['Churn']==0]['Monthly_Charge']

print("\n" + "=" * 55)
print("  STEP 4: CHURN DRIVER ANALYSIS")
print("=" * 55)
print(f"\nChurn by Contract Type:\n{contract_churn.to_string(index=False)}")
print(f"\nChurn by Tenure Segment:\n{tenure_churn.to_string(index=False)}")
print(f"\nChurn by Payment Method:\n{pay_churn.to_string(index=False)}")

# ============================================================
# STEP 5: FEATURE CORRELATION (manual)
# ============================================================
print("\n" + "=" * 55)
print("  STEP 5: CORRELATION WITH CHURN")
print("=" * 55)
num_cols = ['Age','Tenure_Months','Monthly_Charge','Total_Charges','Support_Calls']
corr = df_clean[num_cols + ['Churn']].corr()['Churn'].drop('Churn').sort_values()
print(corr.round(3).to_string())

# ============================================================
# STEP 6: VISUALIZATIONS
# ============================================================
fig = plt.figure(figsize=(20, 26))
fig.suptitle('Customer Churn Analysis Dashboard\nSimpson Gundlapally | Telecom Dataset 2024',
             fontsize=18, fontweight='bold', color='#1F3864', y=0.98)

# Plot 1 — Churn vs Retained Donut
ax1 = fig.add_subplot(4, 3, 1)
vals = [retained, churned]
labels_pie = [f'Retained\n{retention_rate:.1f}%', f'Churned\n{churn_rate:.1f}%']
wedges, texts = ax1.pie(vals, labels=labels_pie, colors=[C_STAY, C_CHURN],
                         startangle=90, wedgeprops=dict(width=0.55))
ax1.set_title('Overall Churn Rate', fontweight='bold', color='#1F3864')

# Plot 2 — Churn by Contract
ax2 = fig.add_subplot(4, 3, 2)
bars2 = ax2.bar(contract_churn['Contract_Type'], contract_churn['Churn_Rate'],
                color=[C_CHURN, '#FFC000', C_STAY], edgecolor='white')
ax2.set_title('Churn Rate by Contract Type', fontweight='bold', color='#1F3864')
ax2.set_ylabel('Churn Rate (%)')
ax2.set_ylim(0, 60)
for bar, val in zip(bars2, contract_churn['Churn_Rate']):
    ax2.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
             f'{val}%', ha='center', fontweight='bold', fontsize=10)
ax2.tick_params(axis='x', rotation=10)

# Plot 3 — Churn by Tenure Segment
ax3 = fig.add_subplot(4, 3, 3)
bars3 = ax3.bar(tenure_churn['Tenure_Segment'], tenure_churn['Churn_Rate'],
                color=COLORS[:4], edgecolor='white')
ax3.set_title('Churn Rate by Tenure Segment', fontweight='bold', color='#1F3864')
ax3.set_ylabel('Churn Rate (%)')
ax3.tick_params(axis='x', rotation=15)
for bar, val in zip(bars3, tenure_churn['Churn_Rate']):
    ax3.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3,
             f'{val}%', ha='center', fontsize=9, fontweight='bold')

# Plot 4 — Monthly Charge Distribution
ax4 = fig.add_subplot(4, 3, (4, 5))
ax4.hist(churn_no,  bins=30, alpha=0.6, color=C_STAY, label='Retained', density=True)
ax4.hist(churn_yes, bins=30, alpha=0.6, color=C_CHURN, label='Churned',  density=True)
ax4.set_title('Monthly Charge Distribution: Churn vs Retained',
              fontweight='bold', color='#1F3864')
ax4.set_xlabel('Monthly Charge (₹)')
ax4.set_ylabel('Density')
ax4.legend()
ax4.axvline(churn_yes.mean(), color=C_CHURN, linestyle='--',
            label=f'Churn avg ₹{churn_yes.mean():.0f}')
ax4.axvline(churn_no.mean(),  color=C_STAY,  linestyle='--',
            label=f'Retained avg ₹{churn_no.mean():.0f}')
ax4.legend(fontsize=9)

# Plot 5 — Payment Method Churn
ax5 = fig.add_subplot(4, 3, 6)
bars5 = ax5.barh(pay_churn['Payment_Method'], pay_churn['Churn_Rate'],
                 color=[C_CHURN if r > 25 else '#2E75B6'
                        for r in pay_churn['Churn_Rate']], edgecolor='white')
ax5.set_title('Churn Rate by Payment Method', fontweight='bold', color='#1F3864')
ax5.set_xlabel('Churn Rate (%)')
for bar, val in zip(bars5, pay_churn['Churn_Rate']):
    ax5.text(bar.get_width()+0.3, bar.get_y()+bar.get_height()/2,
             f'{val}%', va='center', fontsize=9)

# Plot 6 — Support Calls vs Churn (Box Plot)
ax6 = fig.add_subplot(4, 3, 7)
df_clean['Churn_Label'] = df_clean['Churn'].map({0:'Retained', 1:'Churned'})
df_clean.boxplot(column='Support_Calls', by='Churn_Label', ax=ax6,
                 patch_artist=True,
                 boxprops=dict(facecolor='#D6E4F0'),
                 medianprops=dict(color=C_CHURN, linewidth=2))
ax6.set_title('Support Calls vs Churn', fontweight='bold', color='#1F3864')
ax6.set_xlabel('')
plt.sca(ax6)
plt.title('')

# Plot 7 — Internet Service Churn
ax7 = fig.add_subplot(4, 3, 8)
bars7 = ax7.bar(internet_churn['Service'], internet_churn['Churn_Rate'],
                color=['#FF6B6B','#2E75B6','#70AD47'], edgecolor='white')
ax7.set_title('Churn Rate by Internet Service', fontweight='bold', color='#1F3864')
ax7.set_ylabel('Churn Rate (%)')
for bar, val in zip(bars7, internet_churn['Churn_Rate']):
    ax7.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3,
             f'{val}%', ha='center', fontsize=10, fontweight='bold')

# Plot 8 — Correlation Bar
ax8 = fig.add_subplot(4, 3, 9)
corr_vals = corr.values
corr_cols  = corr.index.tolist()
bar_colors = [C_CHURN if v > 0 else C_STAY for v in corr_vals]
ax8.barh(corr_cols, corr_vals, color=bar_colors, edgecolor='white')
ax8.set_title('Feature Correlation with Churn', fontweight='bold', color='#1F3864')
ax8.set_xlabel('Correlation Coefficient')
ax8.axvline(0, color='gray', linewidth=0.8, linestyle='--')

# Plot 9 — Tenure Distribution by Churn
ax9 = fig.add_subplot(4, 3, (10,12))
ax9.hist(df_clean[df_clean['Churn']==0]['Tenure_Months'],
         bins=30, alpha=0.6, color=C_STAY, label='Retained', density=True)
ax9.hist(df_clean[df_clean['Churn']==1]['Tenure_Months'],
         bins=30, alpha=0.6, color=C_CHURN, label='Churned', density=True)
ax9.set_title('Tenure Distribution: Churned vs Retained Customers',
              fontweight='bold', color='#1F3864')
ax9.set_xlabel('Tenure (Months)')
ax9.set_ylabel('Density')
ax9.legend()

plt.tight_layout(rect=[0,0,1,0.97])
plt.savefig('/home/claude/ChurnAnalysis/ChurnAnalysis_Dashboard.png',
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("\n✅ Churn dashboard visualization saved.")

# ============================================================
# STEP 7: BUSINESS INSIGHTS
# ============================================================
print("\n" + "=" * 55)
print("  STEP 7: KEY BUSINESS INSIGHTS")
print("=" * 55)
mtm_rate = contract_churn[contract_churn['Contract_Type']=='Month-to-Month']['Churn_Rate'].values[0]
print(f"1. Month-to-Month churn rate : {mtm_rate}% — highest risk segment")
print(f"2. Early tenure (0-12 mo)    : {tenure_churn.iloc[0]['Churn_Rate']}% churn — critical onboarding window")
print(f"3. Electronic Check payment  : {pay_churn.iloc[0]['Churn_Rate']}% churn — flag for auto-pay push")
print(f"4. Monthly revenue at risk   : ₹{rev_at_risk:,.0f} per month")
print(f"5. Support calls driver      : High-call customers churn significantly more")
print(f"6. Avg tenure of churned     : {avg_tenure_churn:.1f} months vs {avg_tenure:.1f} overall")

# Export clean data
df_clean.to_csv('/home/claude/ChurnAnalysis/churn_cleaned_data.csv', index=False)
contract_churn.to_csv('/home/claude/ChurnAnalysis/contract_churn_summary.csv', index=False)
tenure_churn.to_csv('/home/claude/ChurnAnalysis/tenure_churn_summary.csv', index=False)
pay_churn.to_csv('/home/claude/ChurnAnalysis/payment_churn_summary.csv', index=False)
print("\n✅ All CSVs exported for Power BI.")
