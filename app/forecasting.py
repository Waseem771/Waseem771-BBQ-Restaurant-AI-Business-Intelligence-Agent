"""
Phase 8 - Sales Forecasting System
Complete Time-Series Forecasting with Multiple Models

This module implements sales forecasting for revenue and order volume.
Beginner-friendly with detailed English comments.

Features:
1. Load historical sales data from database
2. Prepare data for time-series analysis
3. Train multiple forecasting models
4. Evaluate model performance
5. Generate future forecasts
6. Store predictions in database
"""

import os
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Tuple, Dict, List

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error

# Try to import Prophet (Facebook's forecasting library)
try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False
    print("Warning: Prophet not installed. Install with: pip install prophet")

# Import sklearn for simple baseline models
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

print("=" * 80)
print("PHASE 8 - SALES FORECASTING SYSTEM")
print("=" * 80)

# ============================================================================
# STEP 1: Configuration
# ============================================================================

print("\n[1/6] Setting up configuration...")

# Database path
DB_PATH = Path("data/bbq.db")

# Forecasting parameters
FORECAST_DAYS = 30  # Forecast for next 30 days
TRAIN_TEST_SPLIT = 0.8  # Use 80% for training, 20% for testing
EVALUATION_METRICS = ["MAE", "RMSE", "MAPE"]

print(f"  Database: {DB_PATH}")
print(f"  Forecast horizon: {FORECAST_DAYS} days")
print(f"  Train/Test split: {TRAIN_TEST_SPLIT*100:.0f}% / {(1-TRAIN_TEST_SPLIT)*100:.0f}%")

# ============================================================================
# STEP 2: Data Loading Functions
# ============================================================================

print("\n[2/6] Loading historical sales data from database...")

def load_daily_sales() -> pd.DataFrame:
    """
    Load daily sales data from SQLite database.

    What it does:
    1. Connect to database
    2. Query order data grouped by date
    3. Calculate daily metrics (revenue, order count, average order value)
    4. Return as DataFrame

    Returns:
        DataFrame with columns: date, daily_revenue, order_count, avg_order_value
    """
    conn = sqlite3.connect(str(DB_PATH))

    # SQL query to get daily sales metrics
    query = """
    SELECT
        order_date as date,
        COUNT(*) as order_count,
        SUM(total_amount) as daily_revenue,
        AVG(total_amount) as avg_order_value
    FROM orders
    GROUP BY order_date
    ORDER BY order_date
    """

    # Execute query and load into DataFrame
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Convert date column to datetime format
    df['date'] = pd.to_datetime(df['date'])

    # Sort by date
    df = df.sort_values('date').reset_index(drop=True)

    print(f"  Loaded {len(df)} days of data")
    print(f"  Date range: {df['date'].min().date()} to {df['date'].max().date()}")
    print(f"  Total revenue: {df['daily_revenue'].sum():,.0f} PKR")
    print(f"  Avg daily revenue: {df['daily_revenue'].mean():,.0f} PKR")

    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add time-based features to the data.

    Why add features?
    - Models need to understand temporal patterns
    - Day of week affects sales (weekends vs weekdays)
    - Month affects sales (seasons, holidays)
    - These features help the model learn patterns

    Features added:
    - day_of_week: 0=Monday, 6=Sunday
    - month: 1-12
    - quarter: 1-4
    - day_of_month: 1-31
    - week_of_year: 1-52
    - is_weekend: 0 or 1

    Args:
        df: DataFrame with 'date' column

    Returns:
        DataFrame with additional feature columns
    """
    df = df.copy()

    # Extract temporal features
    df['day_of_week'] = df['date'].dt.dayofweek  # 0=Mon, 6=Sun
    df['month'] = df['date'].dt.month
    df['quarter'] = df['date'].dt.quarter
    df['day_of_month'] = df['date'].dt.day
    df['week_of_year'] = df['date'].dt.isocalendar().week
    df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)  # 1 if Sat/Sun, 0 otherwise

    # Add rolling averages (smoothed trends)
    # 7-day moving average
    df['revenue_ma7'] = df['daily_revenue'].rolling(window=7, min_periods=1).mean()
    # 30-day moving average
    df['revenue_ma30'] = df['daily_revenue'].rolling(window=30, min_periods=1).mean()

    print(f"  Added {len(df.columns) - 5} features (time + rolling averages)")

    return df


# Load and prepare data
daily_sales = load_daily_sales()
daily_sales_with_features = engineer_features(daily_sales)

# ============================================================================
# STEP 3: Train-Test Split
# ============================================================================

print("\n[3/6] Splitting data into training and testing sets...")

# Calculate split point
split_index = int(len(daily_sales_with_features) * TRAIN_TEST_SPLIT)
split_date = daily_sales_with_features.iloc[split_index]['date']

# Split data
train_df = daily_sales_with_features.iloc[:split_index].copy()
test_df = daily_sales_with_features.iloc[split_index:].copy()

print(f"  Training set: {len(train_df)} days ({train_df['date'].min().date()} to {train_df['date'].max().date()})")
print(f"  Testing set: {len(test_df)} days ({test_df['date'].min().date()} to {test_df['date'].max().date()})")
print(f"  Split date: {split_date.date()}")

# ============================================================================
# STEP 4: Model Training Class
# ============================================================================

print("\n[4/6] Building forecasting models...")

class SalesForecaster:
    """
    Complete forecasting system with multiple models.

    Supports:
    1. Prophet - Facebook's time-series model (if available)
    2. Linear Regression - Simple baseline
    3. Random Forest - Non-linear patterns

    Each model is trained separately and evaluated.
    """

    def __init__(self, train_df: pd.DataFrame, test_df: pd.DataFrame):
        """
        Initialize forecaster.

        Args:
            train_df: Training data with features
            test_df: Testing data for evaluation
        """
        self.train_df = train_df
        self.test_df = test_df
        self.models = {}
        self.predictions = {}
        self.metrics = {}

        print("  Forecaster initialized")

    def train_prophet(self) -> None:
        """
        Train Facebook Prophet model.

        What Prophet does:
        - Decomposes time series into trend, seasonality, holidays
        - Handles missing data and outliers automatically
        - Good for data with strong seasonal patterns
        - Provides uncertainty intervals

        Why Prophet is good:
        - Easy to use
        - Handles multiple seasonalities (daily, weekly, yearly)
        - Good for business data
        - Provides confidence intervals
        """
        if not PROPHET_AVAILABLE:
            print("  Prophet: SKIPPED (not installed)")
            return

        print("  Training Prophet model...")

        try:
            # Prepare data for Prophet
            # Prophet expects columns: ds (date) and y (target)
            prophet_df = pd.DataFrame({
                'ds': self.train_df['date'],
                'y': self.train_df['daily_revenue']
            })

            # Initialize and train Prophet
            model = Prophet(yearly_seasonality=True, daily_seasonality=False)
            model.fit(prophet_df)

            # Test set predictions
            test_forecast_df = pd.DataFrame({'ds': self.test_df['date']})
            test_forecast = model.predict(test_forecast_df)

            # Store model and predictions
            self.models['prophet'] = model
            self.predictions['prophet'] = test_forecast['yhat'].values

            print("    Prophet model trained successfully")

        except Exception as e:
            print(f"    Prophet training failed: {e}")

    def train_linear_regression(self) -> None:
        """
        Train Linear Regression model.

        What Linear Regression does:
        - Finds best-fit line through data
        - Formula: y = mx + b
        - Fast and simple baseline

        Why Linear Regression:
        - Good baseline to compare against
        - Fast training
        - Interpretable results
        - Works well if trend is linear
        """
        print("  Training Linear Regression model...")

        # Prepare features
        # Select columns: day_of_week, month, is_weekend, etc.
        feature_cols = ['day_of_week', 'month', 'quarter', 'is_weekend', 'revenue_ma7']
        X_train = self.train_df[feature_cols].values
        y_train = self.train_df['daily_revenue'].values
        X_test = self.test_df[feature_cols].values

        # Train model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Make predictions
        predictions = model.predict(X_test)

        # Store
        self.models['linear_regression'] = model
        self.predictions['linear_regression'] = predictions

        print("    Linear Regression trained")

    def train_random_forest(self) -> None:
        """
        Train Random Forest model.

        What Random Forest does:
        - Creates many decision trees
        - Averages their predictions
        - Captures non-linear patterns

        Why Random Forest:
        - Handles non-linear relationships
        - Captures complex patterns
        - Less prone to overfitting than single tree
        - Good for business data
        """
        print("  Training Random Forest model...")

        try:
            # Prepare features (same as Linear Regression)
            feature_cols = ['day_of_week', 'month', 'quarter', 'is_weekend', 'revenue_ma7']
            X_train = self.train_df[feature_cols].values
            y_train = self.train_df['daily_revenue'].values
            X_test = self.test_df[feature_cols].values

            # Train Random Forest
            # n_estimators = number of trees (100 is good balance)
            # random_state = for reproducibility
            model = RandomForestRegressor(
                n_estimators=100,
                max_depth=15,
                random_state=42,
                n_jobs=-1  # Use all CPU cores
            )
            model.fit(X_train, y_train)

            # Make predictions
            predictions = model.predict(X_test)

            # Store
            self.models['random_forest'] = model
            self.predictions['random_forest'] = predictions

            print("    Random Forest trained")

        except Exception as e:
            print(f"    Random Forest training failed: {e}")

    def evaluate_models(self) -> Dict[str, Dict[str, float]]:
        """
        Evaluate all trained models on test set.

        Metrics calculated:
        - MAE: Mean Absolute Error (average absolute difference)
        - RMSE: Root Mean Squared Error (penalizes large errors more)
        - MAPE: Mean Absolute Percentage Error (percentage error)

        Returns:
            Dictionary: {model_name: {metric_name: value}}
        """
        print("  Evaluating models on test set...")

        # Actual test values
        y_test = self.test_df['daily_revenue'].values

        # Calculate metrics for each model
        for model_name, predictions in self.predictions.items():
            mae = mean_absolute_error(y_test, predictions)
            rmse = np.sqrt(mean_squared_error(y_test, predictions))
            mape = mean_absolute_percentage_error(y_test, predictions)

            self.metrics[model_name] = {
                'MAE': mae,
                'RMSE': rmse,
                'MAPE': mape
            }

            print(f"    {model_name}:")
            print(f"      MAE:  {mae:,.0f} PKR")
            print(f"      RMSE: {rmse:,.0f} PKR")
            print(f"      MAPE: {mape:.2%}")

        return self.metrics

    def get_best_model(self) -> str:
        """
        Find model with lowest MAE (Mean Absolute Error).

        Why MAE?
        - Easy to interpret (in PKR)
        - Not overly sensitive to outliers
        - Good for business purposes

        Returns:
            Name of best model
        """
        if not self.metrics:
            return None

        best_model = min(self.metrics.keys(),
                        key=lambda m: self.metrics[m]['MAE'])
        best_mae = self.metrics[best_model]['MAE']

        print(f"\n  BEST MODEL: {best_model} (MAE: {best_mae:,.0f} PKR)")
        return best_model

    def forecast_future(self, days: int = FORECAST_DAYS) -> pd.DataFrame:
        """
        Generate forecasts for future dates.

        Process:
        1. Get best model
        2. Create future dates
        3. Generate features for future dates
        4. Make predictions
        5. Return as DataFrame

        Args:
            days: Number of days to forecast

        Returns:
            DataFrame with forecast dates and predictions
        """
        print(f"\n  Generating {days}-day forecast...")

        # Get best model
        best_model_name = self.get_best_model()
        if best_model_name is None:
            print("    ERROR: No models trained")
            return None

        # Get last date from training data
        last_date = self.train_df['date'].max()

        # Generate future dates
        future_dates = [last_date + timedelta(days=i+1) for i in range(days)]

        # Create future DataFrame with features
        future_df = pd.DataFrame({'date': future_dates})
        future_df['day_of_week'] = future_df['date'].dt.dayofweek
        future_df['month'] = future_df['date'].dt.month
        future_df['quarter'] = future_df['date'].dt.quarter
        future_df['is_weekend'] = (future_df['day_of_week'] >= 5).astype(int)

        # For rolling averages, use last known value
        last_ma7 = self.train_df['revenue_ma7'].iloc[-1]
        future_df['revenue_ma7'] = last_ma7

        # Make predictions with best model
        if best_model_name in ['linear_regression', 'random_forest']:
            feature_cols = ['day_of_week', 'month', 'quarter', 'is_weekend', 'revenue_ma7']
            X_future = future_df[feature_cols].values
            predictions = self.models[best_model_name].predict(X_future)
            future_df['forecast'] = predictions

        elif best_model_name == 'prophet':
            # Prophet forecasting
            future_prophet_df = pd.DataFrame({'ds': future_dates})
            forecast = self.models[best_model_name].predict(future_prophet_df)
            future_df['forecast'] = forecast['yhat'].values

        print(f"    Forecast generated for {len(future_df)} future dates")
        print(f"    Average predicted daily revenue: {future_df['forecast'].mean():,.0f} PKR")

        return future_df


# ============================================================================
# STEP 5: Train All Models
# ============================================================================

print("\n[5/6] Training forecasting models...")

# Initialize forecaster
forecaster = SalesForecaster(train_df, test_df)

# Train all models
forecaster.train_prophet()
forecaster.train_linear_regression()
forecaster.train_random_forest()

# Evaluate models
metrics = forecaster.evaluate_models()

# ============================================================================
# STEP 6: Generate Forecasts and Save
# ============================================================================

print("\n[6/6] Generating future forecasts...")

# Generate 30-day forecast
forecast_df = forecaster.forecast_future(days=FORECAST_DAYS)

if forecast_df is not None:
    print(f"\nForecast Results:")
    print(f"  Start date: {forecast_df['date'].min().date()}")
    print(f"  End date: {forecast_df['date'].max().date()}")
    print(f"\nTop 5 Predicted Days:")
    top_days = forecast_df.nlargest(5, 'forecast')[['date', 'forecast']]
    for idx, row in top_days.iterrows():
        print(f"  {row['date'].date()}: {row['forecast']:,.0f} PKR")

    print(f"\nBottom 5 Predicted Days:")
    bottom_days = forecast_df.nsmallest(5, 'forecast')[['date', 'forecast']]
    for idx, row in bottom_days.iterrows():
        print(f"  {row['date'].date()}: {row['forecast']:,.0f} PKR")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "=" * 80)
print("FORECASTING SUMMARY")
print("=" * 80)

print("\n[TRAINING DATA]")
print(f"  Period: {train_df['date'].min().date()} to {train_df['date'].max().date()}")
print(f"  Days: {len(train_df)}")
print(f"  Total Revenue: {train_df['daily_revenue'].sum():,.0f} PKR")
print(f"  Daily Avg: {train_df['daily_revenue'].mean():,.0f} PKR")

print("\n[TESTING DATA]")
print(f"  Period: {test_df['date'].min().date()} to {test_df['date'].max().date()}")
print(f"  Days: {len(test_df)}")
print(f"  Total Revenue: {test_df['daily_revenue'].sum():,.0f} PKR")
print(f"  Daily Avg: {test_df['daily_revenue'].mean():,.0f} PKR")

print("\n[MODELS TRAINED]")
for model_name in forecaster.models.keys():
    print(f"  - {model_name}: TRAINED")

print("\n[MODEL PERFORMANCE]")
for model_name, scores in forecaster.metrics.items():
    print(f"  {model_name}:")
    print(f"    MAE:  {scores['MAE']:,.0f} PKR")
    print(f"    RMSE: {scores['RMSE']:,.0f} PKR")
    print(f"    MAPE: {scores['MAPE']:.2%}")

print("\n[FORECAST GENERATED]")
if forecast_df is not None:
    print(f"  Days: {len(forecast_df)}")
    print(f"  Period: {forecast_df['date'].min().date()} to {forecast_df['date'].max().date()}")
    print(f"  Average Predicted Revenue: {forecast_df['forecast'].mean():,.0f} PKR")
    print(f"  Min Predicted: {forecast_df['forecast'].min():,.0f} PKR")
    print(f"  Max Predicted: {forecast_df['forecast'].max():,.0f} PKR")

print("\n" + "=" * 80)
print("PHASE 8 - SALES FORECASTING COMPLETE")
print("=" * 80)
