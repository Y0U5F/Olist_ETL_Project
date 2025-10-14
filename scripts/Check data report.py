"""
====================================================================
OLIST E-COMMERCE DATA ANALYSIS WITH PANDAS
تحليل بيانات Olist باستخدام Pandas و Visualization
====================================================================
احفظ هذا الملف باسم: Data_Exploration.ipynb في مجلد notebooks/
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# إعدادات الرسوم البيانية
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ====================================================================
# SECTION 1: تحميل البيانات الخام (Raw Data Loading)
# ====================================================================

print("=" * 70)
print("Loading Raw Data Files...")
print("=" * 70)

# تعديل المسار حسب مكان ملفاتك
data_path = '/mnt/sdb3/ITI/ITI/1-July/Data warehouse and data lake/Menna/The project/Olist_ETL_Project/data/raw_data/'

# تحميل جميع الجداول
try:
    customers_df = pd.read_csv(data_path + 'olist_customers_dataset.csv')
    orders_df = pd.read_csv(data_path + 'olist_orders_dataset.csv')
    order_items_df = pd.read_csv(data_path + 'olist_order_items_dataset.csv')
    products_df = pd.read_csv(data_path + 'olist_products_dataset.csv')
    sellers_df = pd.read_csv(data_path + 'olist_sellers_dataset.csv')
except Exception as e:
    print(f"❌ Error loading data: {e}")
    raise

print(f"✅ Customers: {len(customers_df):,} rows")
print(f"✅ Orders: {len(orders_df):,} rows")
print(f"✅ Order Items: {len(order_items_df):,} rows")
print(f"✅ Products: {len(products_df):,} rows")
print(f"✅ Sellers: {len(sellers_df):,} rows")
print()


# ====================================================================
# SECTION 2: استكشاف القيم المفقودة (Missing Values Analysis)
# ====================================================================

print("=" * 70)
print("ANALYSIS 1: Missing Values Detection")
print("=" * 70)

# تحليل القيم المفقودة في جدول الطلبات
orders_missing = orders_df.isnull().sum()
orders_missing_pct = (orders_missing / len(orders_df)) * 100

print("\nMissing Values in Orders Table:")
print("-" * 50)
if orders_missing[orders_missing > 0].empty:
    print("No missing values found in Orders Table.")
else:
    for col, count in orders_missing[orders_missing > 0].items():
        print(f"{col:40} | {count:6,} ({orders_missing_pct[col]:.2f}%)")

# رسم خريطة حرارية للقيم المفقودة
plt.figure(figsize=(14, 8))
sns.heatmap(orders_df.isnull(), cbar=True, cmap='RdYlGn_r', yticklabels=False)
plt.title('Missing Values Heatmap - Orders Dataset', fontsize=16, fontweight='bold')
plt.xlabel('Columns', fontsize=12)
plt.ylabel('Rows', fontsize=12)
plt.tight_layout()
plt.savefig('output_missing_values_orders.png', dpi=300, bbox_inches='tight')
plt.close()

# رسم بياني شريطي للقيم المفقودة
missing_data = orders_df.isnull().sum().sort_values(ascending=False)
missing_data = missing_data[missing_data > 0]
if not missing_data.empty:
    plt.figure(figsize=(12, 6))
    missing_data.plot(kind='bar', color='coral')
    plt.title('Number of Missing Values per Column - Orders', fontsize=14, fontweight='bold')
    plt.ylabel('Count of Missing Values')
    plt.xlabel('Columns')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('output_missing_values_bar.png', dpi=300, bbox_inches='tight')
    plt.close()


# ====================================================================
# SECTION 3: تحليل الأسعار والقيم المتطرفة (Price Analysis & Outliers)
# ====================================================================

print("\n" + "=" * 70)
print("ANALYSIS 2: Price Distribution & Outliers")
print("=" * 70)

# إحصائيات وصفية للأسعار
print("\nPrice Statistics:")
print("-" * 50)
if 'price' in order_items_df.columns:
    print(order_items_df['price'].describe())
else:
    print("❌ 'price' column not found in order_items_df.")

# رسم توزيع الأسعار - Box Plot
if 'price' in order_items_df.columns:
    plt.figure(figsize=(14, 6))

    plt.subplot(1, 2, 1)
    sns.boxplot(x=order_items_df['price'], color='skyblue')
    plt.title('Price Distribution (Box Plot)', fontsize=14, fontweight='bold')
    plt.xlabel('Price (R$)')

    plt.subplot(1, 2, 2)
    sns.boxplot(x=order_items_df['price'], color='lightcoral')
    plt.xscale('log')  # مقياس لوغاريتمي لرؤية التوزيع بشكل أفضل
    plt.title('Price Distribution (Log Scale)', fontsize=14, fontweight='bold')
    plt.xlabel('Price (R$) - Log Scale')

    plt.tight_layout()
    plt.savefig('output_price_outliers.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Histogram للأسعار
    plt.figure(figsize=(12, 6))
    plt.hist(order_items_df['price'], bins=50, color='mediumseagreen', edgecolor='black', alpha=0.7)
    plt.title('Price Distribution Histogram', fontsize=14, fontweight='bold')
    plt.xlabel('Price (R$)')
    plt.ylabel('Frequency')
    plt.axvline(order_items_df['price'].mean(), color='red', linestyle='--', label=f'Mean: R$ {order_items_df['price'].mean():.2f}')
    plt.axvline(order_items_df['price'].median(), color='blue', linestyle='--', label=f'Median: R$ {order_items_df['price'].median():.2f}')
    plt.legend()
    plt.tight_layout()
    plt.savefig('output_price_histogram.png', dpi=300, bbox_inches='tight')
    plt.close()

    # تحديد القيم المتطرفة
    Q1 = order_items_df['price'].quantile(0.25)
    Q3 = order_items_df['price'].quantile(0.75)
    IQR = Q3 - Q1
    outliers = order_items_df[(order_items_df['price'] < (Q1 - 1.5 * IQR)) | 
                              (order_items_df['price'] > (Q3 + 1.5 * IQR))]

    print(f"\n📊 Total Products: {len(order_items_df):,}")
    print(f"⚠️  Price Outliers Detected: {len(outliers):,} ({len(outliers)/len(order_items_df)*100:.2f}%)")
    print(f"💰 Most Expensive Product: R$ {order_items_df['price'].max():,.2f}")
else:
    print("❌ Skipping price analysis due to missing 'price' column.")


# ====================================================================
# SECTION 4: تحليل التوزيع الجغرافي (Geographic Distribution)
# ====================================================================

print("\n" + "=" * 70)
print("ANALYSIS 3: Geographic Distribution")
print("=" * 70)

# أكثر الولايات مبيعاً
if 'customer_state' in customers_df.columns:
    state_counts = customers_df['customer_state'].value_counts().head(10)
    print("\nTop 10 States by Customer Count:")
    print("-" * 50)
    print(state_counts)

    plt.figure(figsize=(12, 6))
    state_counts.plot(kind='bar', color='teal', edgecolor='black')
    plt.title('Top 10 States by Number of Customers', fontsize=14, fontweight='bold')
    plt.xlabel('State')
    plt.ylabel('Number of Customers')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('output_top_states.png', dpi=300, bbox_inches='tight')
    plt.close()
else:
    print("❌ 'customer_state' column not found in customers_df.")


# ====================================================================
# SECTION 5: تحليل الأوامر حسب الحالة (Order Status Analysis)
# ====================================================================

print("\n" + "=" * 70)
print("ANALYSIS 4: Order Status Distribution")
print("=" * 70)

if 'order_status' in orders_df.columns:
    order_status = orders_df['order_status'].value_counts()
    print("\nOrder Status Breakdown:")
    print("-" * 50)
    print(order_status)

    # Pie Chart
    plt.figure(figsize=(10, 8))
    colors = sns.color_palette('pastel')
    plt.pie(order_status, labels=order_status.index, autopct='%1.1f%%', 
            startangle=90, colors=colors, textprops={'fontsize': 11})
    plt.title('Order Status Distribution', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('output_order_status.png', dpi=300, bbox_inches='tight')
    plt.close()
else:
    print("❌ 'order_status' column not found in orders_df.")


# ====================================================================
# SECTION 6: تحليل الوقت - التواريخ (Time Series Analysis)
# ====================================================================

print("\n" + "=" * 70)
print("ANALYSIS 5: Time Series - Orders Over Time")
print("=" * 70)

if 'order_purchase_timestamp' in orders_df.columns:
    # تحويل التواريخ
    orders_df['order_purchase_timestamp'] = pd.to_datetime(orders_df['order_purchase_timestamp'], errors='coerce')
    orders_df['order_year_month'] = orders_df['order_purchase_timestamp'].dt.to_period('M')

    # عدد الطلبات حسب الشهر
    monthly_orders = orders_df.groupby('order_year_month').size()

    plt.figure(figsize=(14, 6))
    monthly_orders.plot(kind='line', marker='o', color='dodgerblue', linewidth=2)
    plt.title('Number of Orders Over Time (Monthly)', fontsize=14, fontweight='bold')
    plt.xlabel('Month')
    plt.ylabel('Number of Orders')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('output_orders_over_time.png', dpi=300, bbox_inches='tight')
    plt.close()

    min_date = orders_df['order_purchase_timestamp'].min()
    max_date = orders_df['order_purchase_timestamp'].max()
    print(f"\n📅 Date Range: {min_date} to {max_date}")
    if not monthly_orders.empty:
        print(f"📦 Peak Month: {monthly_orders.idxmax()} with {monthly_orders.max():,} orders")
    else:
        print("No monthly orders data available.")
else:
    print("❌ 'order_purchase_timestamp' column not found in orders_df.")


# ====================================================================
# SECTION 7: تحليل وقت التوصيل (Delivery Time Analysis)
# ====================================================================

print("\n" + "=" * 70)
print("ANALYSIS 6: Delivery Time Analysis")
print("=" * 70)

if 'order_delivered_customer_date' in orders_df.columns and 'order_purchase_timestamp' in orders_df.columns:
    # تحويل التواريخ
    orders_df['order_delivered_customer_date'] = pd.to_datetime(orders_df['order_delivered_customer_date'], errors='coerce')
    orders_df['order_estimated_delivery_date'] = pd.to_datetime(orders_df['order_estimated_delivery_date'], errors='coerce')

    # حساب وقت التوصيل
    orders_df['delivery_days'] = (orders_df['order_delivered_customer_date'] - 
                                   orders_df['order_purchase_timestamp']).dt.days

    # فلترة البيانات الصحيحة فقط
    delivery_data = orders_df[orders_df['delivery_days'].notna() & (orders_df['delivery_days'] > 0)]

    print(f"\nDelivery Time Statistics:")
    print("-" * 50)
    print(delivery_data['delivery_days'].describe())

    plt.figure(figsize=(12, 6))
    sns.histplot(delivery_data['delivery_days'], bins=50, kde=True, color='purple', alpha=0.6)
    plt.title('Delivery Time Distribution', fontsize=14, fontweight='bold')
    plt.xlabel('Delivery Time (Days)')
    plt.ylabel('Frequency')
    plt.axvline(delivery_data['delivery_days'].mean(), color='red', linestyle='--', 
                label=f"Mean: {delivery_data['delivery_days'].mean():.1f} days")
    plt.axvline(delivery_data['delivery_days'].median(), color='blue', linestyle='--', 
                label=f"Median: {delivery_data['delivery_days'].median():.1f} days")
    plt.legend()
    plt.tight_layout()
    plt.savefig('output_delivery_time.png', dpi=300, bbox_inches='tight')
    plt.close()
else:
    print("❌ Delivery date columns not found in orders_df.")
    delivery_data = pd.DataFrame()  # fallback for later use


# ====================================================================
# SECTION 8: تحليل المنتجات (Product Analysis)
# ====================================================================

print("\n" + "=" * 70)
print("ANALYSIS 7: Product Category Analysis")
print("=" * 70)

# دمج البيانات
if 'product_id' in order_items_df.columns and 'product_id' in products_df.columns:
    merged_data = order_items_df.merge(products_df, on='product_id', how='left')

    # أكثر الفئات مبيعاً
    if 'product_category_name' in merged_data.columns:
        top_categories = merged_data['product_category_name'].value_counts().head(15)

        plt.figure(figsize=(14, 7))
        top_categories.plot(kind='barh', color='gold', edgecolor='black')
        plt.title('Top 15 Product Categories by Sales Volume', fontsize=14, fontweight='bold')
        plt.xlabel('Number of Items Sold')
        plt.ylabel('Product Category')
        plt.tight_layout()
        plt.savefig('output_top_categories.png', dpi=300, bbox_inches='tight')
        plt.close()

        print("\nTop 5 Product Categories:")
        print("-" * 50)
        print(top_categories.head())
    else:
        print("❌ 'product_category_name' column not found in merged_data.")
        top_categories = pd.Series(dtype=int)
else:
    print("❌ 'product_id' column missing in order_items_df or products_df.")
    merged_data = pd.DataFrame()
    top_categories = pd.Series(dtype=int)


# ====================================================================
# SECTION 9: تحليل الإيرادات (Revenue Analysis)
# ====================================================================

print("\n" + "=" * 70)
print("ANALYSIS 8: Revenue Analysis")
print("=" * 70)

# حساب الإيرادات
if 'price' in order_items_df.columns and 'freight_value' in order_items_df.columns:
    order_items_df['total_value'] = order_items_df['price'] + order_items_df['freight_value']
else:
    print("❌ 'price' or 'freight_value' column missing in order_items_df.")
    order_items_df['total_value'] = np.nan

if 'product_id' in order_items_df.columns and 'product_id' in products_df.columns:
    merged_revenue = order_items_df.merge(products_df, on='product_id', how='left')
    if 'product_category_name' in merged_revenue.columns:
        revenue_by_category = merged_revenue.groupby('product_category_name')['total_value'].sum().sort_values(ascending=False).head(15)

        plt.figure(figsize=(14, 7))
        revenue_by_category.plot(kind='barh', color='seagreen', edgecolor='black')
        plt.title('Top 15 Product Categories by Revenue', fontsize=14, fontweight='bold')
        plt.xlabel('Total Revenue (R$)')
        plt.ylabel('Product Category')
        plt.tight_layout()
        plt.savefig('output_revenue_by_category.png', dpi=300, bbox_inches='tight')
        plt.close()
    else:
        print("❌ 'product_category_name' column not found in merged_revenue.")
        revenue_by_category = pd.Series(dtype=float)
else:
    print("❌ 'product_id' column missing in order_items_df or products_df.")
    merged_revenue = pd.DataFrame()
    revenue_by_category = pd.Series(dtype=float)

if 'total_value' in order_items_df.columns:
    print(f"\n💰 Total Revenue: R$ {order_items_df['total_value'].sum():,.2f}")
    print(f"📦 Total Orders: {len(order_items_df):,}")
    print(f"💵 Average Order Value: R$ {order_items_df['total_value'].mean():.2f}")
else:
    print("❌ 'total_value' column missing in order_items_df.")


# ====================================================================
# SECTION 10: ملخص نهائي (Final Summary Report)
# ====================================================================

print("\n" + "=" * 70)
print("📊 FINAL SUMMARY REPORT")
print("=" * 70)

try:
    avg_delivery_time = (
        delivery_data['delivery_days'].mean()
        if 'delivery_days' in delivery_data.columns and not delivery_data.empty
        else float('nan')
    )
    top_state = (
        customers_df['customer_state'].value_counts().index[0]
        if 'customer_state' in customers_df.columns and not customers_df.empty
        else 'N/A'
    )
    most_sold_category = (
        merged_data['product_category_name'].value_counts().index[0]
        if 'product_category_name' in merged_data.columns and not merged_data.empty
        else 'N/A'
    )
    summary = f"""
Data Quality Summary:
{'=' * 50}
✅ Total Customers: {len(customers_df):,}
✅ Total Orders: {len(orders_df):,}
✅ Total Products Sold: {len(order_items_df):,}
✅ Unique Products: {products_df['product_id'].nunique():,}
✅ Active Sellers: {sellers_df['seller_id'].nunique():,}

Missing Data Issues:
{'=' * 50}
⚠️  Orders with missing delivery dates: {orders_df['order_delivered_customer_date'].isnull().sum():,}
⚠️  Orders with missing approval: {orders_df['order_approved_at'].isnull().sum():,}

Business Insights:
{'=' * 50}
💰 Total Revenue: R$ {order_items_df['total_value'].sum():,.2f}
📊 Average Order Value: R$ {order_items_df['total_value'].mean():.2f}
⏱️  Average Delivery Time: {avg_delivery_time:.1f} days
🏆 Top State: {top_state}
🎯 Most Sold Category: {most_sold_category}
"""
except Exception as e:
    summary = f"❌ Error generating summary: {e}"

print(summary)

# حفظ التقرير
try:
    with open('output_analysis_summary.txt', 'w', encoding='utf-8') as f:
        f.write(summary)
except Exception as e:
    print(f"❌ Error saving summary: {e}")

print("\n✅ Analysis Complete! All charts saved successfully.")
print("=" * 70)