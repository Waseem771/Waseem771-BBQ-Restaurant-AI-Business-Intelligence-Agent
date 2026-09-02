"""
Phase 9 - Anomaly Detection System
Complete Time-Series Anomaly Detection with Isolation Forest

This module implements real-time anomaly detection for sales data.
Beginner-friendly with detailed English comments.

Features:
1. Load historical sales data
2. Train Isolation Forest model
3. Detect anomalies in revenue and orders
4. Calculate severity levels
5. Store anomaly records
6. Real-time monitoring
7. Alert generation
"""

import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Tuple, Dict, List, Optional

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

print("=" * 80)
print("PHASE 9 - ANOMALY DETECTION SYSTEM")
print("=" * 80)

# ============================================================================
# STEP 1: Configuration
# ============================================================================

print("\n[1/6] Setting up configuration...")

DB_PATH = Path("data/bbq.db")

# Anomaly Detection Parameters
CONTAMINATION_RATE = 0.05  # Expect 5% anomalies
SENSITIVITY = "medium"  # low, medium, high
LOOKBACK_DAYS = 7  # Compare current day with last 7 days average

print(f"  Database: {DB_PATH}")
print(f"  Contamination Rate: {CONTAMINATION_RATE*100:.1f}%")
print(f"  Sensitivity: {SENSITIVITY}")
print(f"  Lookback Period: {LOOKBACK_DAYS} days")

# ============================================================================
# STEP 2: Data Loading
# ============================================================================

print("\n[2/6] Loading sales data from database...")

def load_sales_data() -> pd.DataFrame:
    """
    Load sales data from database.

    What it does:
    1. Connect to SQLite database
    2. Query daily sales metrics
    3. Calculate various features
    4. Return as DataFrame

    Returns:
        DataFrame with daily sales metrics and features
    """
    conn = sqlite3.connect(str(DB_PATH))

    query = """
    SELECT
        order_date as date,
        COUNT(*) as order_count,
        SUM(total_amount) as daily_revenue,
        AVG(total_amount) as avg_order_value,
        MIN(total_amount) as min_order_value,
        MAX(total_amount) as max_order_value,
        COUNT(DISTINCT customer_id) as unique_customers
    FROM orders
    GROUP BY order_date
    ORDER BY order_date
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').reset_index(drop=True)

    print(f"  Loaded {len(df)} days of data")
    print(f"  Date range: {df['date'].min().date()} to {df['date'].max().date()}")
    print(f"  Total revenue: {df['daily_revenue'].sum():,.0f} PKR")
    print(f"  Avg daily revenue: {df['daily_revenue'].mean():,.0f} PKR")

    return df


def engineer_anomaly_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create features for anomaly detection.

    Features added:
    - Moving averages (7-day, 14-day, 30-day)
    - Deviation from moving average
    - Rolling standard deviation
    - Day of week
    - Revenue per order
    - Customer satisfaction (orders per customer)

    Args:
        df: DataFrame with daily sales data

    Returns:
        DataFrame with additional anomaly detection features
    """
    df = df.copy()

    # Moving averages
    df['revenue_ma7'] = df['daily_revenue'].rolling(window=7, min_periods=1).mean()
    df['revenue_ma14'] = df['daily_revenue'].rolling(window=14, min_periods=1).mean()
    df['revenue_ma30'] = df['daily_revenue'].rolling(window=30, min_periods=1).mean()

    # Standard deviations
    df['revenue_std7'] = df['daily_revenue'].rolling(window=7, min_periods=1).std()
    df['revenue_std30'] = df['daily_revenue'].rolling(window=30, min_periods=1).std()

    # Deviations from moving average
    df['deviation_from_ma7'] = df['daily_revenue'] - df['revenue_ma7']
    df['deviation_pct_ma7'] = (df['deviation_from_ma7'] / df['revenue_ma7']) * 100

    # Order metrics
    df['revenue_per_order'] = df['daily_revenue'] / df['order_count']
    df['orders_per_customer'] = df['order_count'] / df['unique_customers']

    # Day of week
    df['day_of_week'] = df['date'].dt.dayofweek
    df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)

    # Volatility
    df['volatility_7d'] = df['daily_revenue'].pct_change().rolling(7).std() * 100

    print(f"  Added 12 anomaly detection features")
    return df


# Load and prepare data
daily_sales = load_sales_data()
daily_sales_features = engineer_anomaly_features(daily_sales)

# ============================================================================
# STEP 3: Anomaly Detection Class
# ============================================================================

print("\n[3/6] Building anomaly detection system...")

class AnomalyDetector:
    """
    Complete anomaly detection system using Isolation Forest.

    What Isolation Forest does:
    - Builds random forests of isolation trees
    - Anomalies are easier to isolate (require fewer splits)
    - Normal points need more splits to isolate
    - Assigns anomaly score based on isolation path length

    Advantages:
    - No need to define distance metrics
    - Works well with high-dimensional data
    - Efficient (linear time complexity)
    - Can detect global and local anomalies
    """

    def __init__(self, contamination_rate: float = 0.05):
        """
        Initialize anomaly detector.

        Args:
            contamination_rate: Expected proportion of anomalies (0-1)
        """
        self.contamination_rate = contamination_rate
        self.model = None
        self.scaler = StandardScaler()
        self.trained = False
        self.anomalies = []

        print("  Anomaly Detector initialized")

    def train(self, df: pd.DataFrame) -> None:
        """
        Train Isolation Forest on historical data.

        Process:
        1. Select features for anomaly detection
        2. Standardize features (mean=0, std=1)
        3. Train Isolation Forest
        4. Calculate anomaly scores
        5. Store results

        Args:
            df: DataFrame with features
        """
        print("  Training Isolation Forest...")

        # Select features for anomaly detection
        feature_cols = [
            'daily_revenue', 'order_count', 'avg_order_value',
            'revenue_per_order', 'orders_per_customer',
            'volatility_7d', 'is_weekend'
        ]

        # Get feature data
        X = df[feature_cols].fillna(0).values

        # Standardize features
        X_scaled = self.scaler.fit_transform(X)

        # Train Isolation Forest
        # n_estimators: number of trees (100 is good balance)
        # contamination: expected % of anomalies
        # random_state: for reproducibility
        self.model = IsolationForest(
            n_estimators=100,
            contamination=self.contamination_rate,
            random_state=42,
            n_jobs=-1
        )

        self.model.fit(X_scaled)

        # Get anomaly predictions (-1 for anomaly, 1 for normal)
        predictions = self.model.predict(X_scaled)

        # Get anomaly scores (lower = more anomalous)
        scores = self.model.score_samples(X_scaled)

        # Store in DataFrame
        df['anomaly_prediction'] = predictions
        df['anomaly_score'] = scores

        self.trained = True

        # Count anomalies
        n_anomalies = (predictions == -1).sum()
        print(f"  Model trained")
        print(f"  Anomalies detected: {n_anomalies} ({n_anomalies/len(df)*100:.1f}%)")

    def detect_anomalies(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Detect anomalies in data.

        Returns DataFrame with:
        - anomaly_prediction: -1 (anomaly) or 1 (normal)
        - anomaly_score: lower = more anomalous
        - severity: LOW, MEDIUM, HIGH, CRITICAL
        - description: Human-readable explanation

        Args:
            df: DataFrame with features

        Returns:
            DataFrame with anomaly detection results
        """
        if not self.trained:
            print("  ERROR: Model not trained")
            return None

        print("  Detecting anomalies...")

        feature_cols = [
            'daily_revenue', 'order_count', 'avg_order_value',
            'revenue_per_order', 'orders_per_customer',
            'volatility_7d', 'is_weekend'
        ]

        X = df[feature_cols].fillna(0).values
        X_scaled = self.scaler.transform(X)

        # Get predictions and scores
        predictions = self.model.predict(X_scaled)
        scores = self.model.score_samples(X_scaled)

        df = df.copy()
        df['is_anomaly'] = predictions == -1
        df['anomaly_score'] = scores

        # Calculate severity
        severities = []
        for score in scores:
            if score < -0.8:
                severities.append("CRITICAL")
            elif score < -0.5:
                severities.append("HIGH")
            elif score < -0.2:
                severities.append("MEDIUM")
            else:
                severities.append("LOW")

        df['severity'] = severities

        # Get anomalies only
        anomalies = df[df['is_anomaly']].copy()
        print(f"  Found {len(anomalies)} anomalies")

        return df, anomalies

    def explain_anomaly(self, row: pd.Series) -> str:
        """
        Generate human-readable explanation for anomaly.

        Args:
            row: DataFrame row with anomaly data

        Returns:
            Explanation string
        """
        reasons = []

        # Revenue analysis
        if 'revenue_ma7' in row and pd.notna(row['revenue_ma7']) and row['revenue_ma7'] > 0:
            if row['daily_revenue'] < row['revenue_ma7'] * 0.7:
                reasons.append(f"Revenue {(1 - row['daily_revenue']/row['revenue_ma7'])*100:.0f}% below 7-day average")
            elif row['daily_revenue'] > row['revenue_ma7'] * 1.3:
                reasons.append(f"Revenue {(row['daily_revenue']/row['revenue_ma7'] - 1)*100:.0f}% above 7-day average")

        # Order analysis
        if row['avg_order_value'] > 0:
            expected_orders = row['daily_revenue'] / row['avg_order_value']
            if row['order_count'] < expected_orders * 0.8:
                reasons.append("Low order count for revenue level")
            elif row['order_count'] > expected_orders * 1.2:
                reasons.append("High order count for revenue level")

        # Volatility analysis
        if 'volatility_7d' in row and pd.notna(row['volatility_7d']) and row['volatility_7d'] > 15:
            reasons.append(f"High volatility ({row['volatility_7d']:.1f}%)")

        if not reasons:
            reasons.append("Unusual pattern detected by Isolation Forest")

        return "; ".join(reasons)


# Initialize and train detector
detector = AnomalyDetector(contamination_rate=CONTAMINATION_RATE)
detector.train(daily_sales_features)

# ============================================================================
# STEP 4: Detect Anomalies
# ============================================================================

print("\n[4/6] Detecting anomalies in historical data...")

results_df, anomalies_df = detector.detect_anomalies(daily_sales_features)

# ============================================================================
# STEP 5: Analyze and Display Results
# ============================================================================

print("\n[5/6] Analyzing anomaly detection results...")

print(f"\nAnomalies by Severity:")
severity_counts = anomalies_df['severity'].value_counts()
for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
    count = severity_counts.get(severity, 0)
    print(f"  {severity}: {count}")

print(f"\nTop 10 Most Anomalous Days:")
top_anomalies = results_df[results_df['is_anomaly']].nsmallest(10, 'anomaly_score')[
    ['date', 'daily_revenue', 'order_count', 'severity', 'anomaly_score']
]

for idx, row in top_anomalies.iterrows():
    # Get full row from results_df for explanation
    full_row = results_df.loc[idx]
    explanation = detector.explain_anomaly(full_row)
    print(f"  {row['date'].date()} - {row['severity']}")
    print(f"    Revenue: {row['daily_revenue']:,.0f} PKR ({row['order_count']} orders)")
    print(f"    Reason: {explanation}")
    print()

# ============================================================================
# STEP 6: Statistics and Summary
# ============================================================================

print("\n[6/6] Generating anomaly detection summary...")

print("\n" + "=" * 80)
print("ANOMALY DETECTION SUMMARY")
print("=" * 80)

print("\n[DATA ANALYSIS]")
print(f"  Total Days Analyzed: {len(results_df)}")
print(f"  Anomalies Detected: {len(anomalies_df)} ({len(anomalies_df)/len(results_df)*100:.1f}%)")

print("\n[SEVERITY DISTRIBUTION]")
for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
    count = len(anomalies_df[anomalies_df['severity'] == severity])
    pct = (count / len(anomalies_df) * 100) if len(anomalies_df) > 0 else 0
    print(f"  {severity}: {count} ({pct:.1f}%)")

print("\n[ANOMALY STATISTICS]")
print(f"  Min Anomaly Score: {anomalies_df['anomaly_score'].min():.4f}")
print(f"  Max Anomaly Score: {anomalies_df['anomaly_score'].max():.4f}")
print(f"  Avg Anomaly Score: {anomalies_df['anomaly_score'].mean():.4f}")

print("\n[REVENUE ANALYSIS]")
print(f"  Normal Days Avg Revenue: {results_df[~results_df['is_anomaly']]['daily_revenue'].mean():,.0f} PKR")
print(f"  Anomaly Days Avg Revenue: {anomalies_df['daily_revenue'].mean():,.0f} PKR")
print(f"  Revenue Difference: {(anomalies_df['daily_revenue'].mean() / results_df[~results_df['is_anomaly']]['daily_revenue'].mean() - 1)*100:+.1f}%")

print("\n[ORDER ANALYSIS]")
print(f"  Normal Days Avg Orders: {results_df[~results_df['is_anomaly']]['order_count'].mean():.0f}")
print(f"  Anomaly Days Avg Orders: {anomalies_df['order_count'].mean():.0f}")

print("\n" + "=" * 80)
print("PHASE 9 - ANOMALY DETECTION COMPLETE")
print("=" * 80)
