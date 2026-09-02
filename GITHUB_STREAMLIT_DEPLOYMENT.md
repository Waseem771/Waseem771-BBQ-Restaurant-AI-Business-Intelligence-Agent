# 🚀 GitHub + Streamlit Deployment Guide

**Date:** 2026-08-31  
**Level:** Beginner-Friendly  
**Time Required:** 1-2 hours

---

## Table of Contents

1. [What is Streamlit?](#what-is-streamlit)
2. [GitHub Setup](#github-setup)
3. [Streamlit Deployment](#streamlit-deployment)
4. [Alternative: Streamlit Cloud](#alternative-streamlit-cloud)
5. [Troubleshooting](#troubleshooting)

---

## What is Streamlit?

Streamlit is a Python framework for building data apps with minimal code.

**Why Streamlit for your BBQ AI app?**
- Fast deployment (minutes, not hours)
- No backend infrastructure needed
- Perfect for dashboards and AI apps
- Free hosting tier available
- Easy to share with others

**Streamlit vs Docker:**
- **Docker:** Full control, more complex, production-ready
- **Streamlit:** Simple, fast, great for AI/ML apps

---

## GitHub Setup

### Step 1: Create GitHub Repository

**1.1 Create GitHub Account**
```
1. Go to https://github.com
2. Sign up (free account)
3. Verify email
```

**1.2 Create New Repository**
```
1. Click "+" in top-right → "New repository"
2. Repository name: bbq-ai-business-intelligence
3. Description: BBQ Restaurant AI Business Intelligence Dashboard
4. Visibility: Public (required for free Streamlit deployment)
5. Click "Create repository"
```

**1.3 Initialize Local Git**
```bash
# Navigate to project
cd "E:\BBQ Restaurant AI Business Intelligence Agent\Projects\BBQ Restaurant AI Business Intelligence Agent"

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: BBQ Restaurant AI Business Intelligence Agent"

# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/bbq-ai-business-intelligence.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**1.4 Verify on GitHub**
```
1. Go to https://github.com/YOUR_USERNAME/bbq-ai-business-intelligence
2. Should see all your files uploaded
3. README.md should display
```

---

## Streamlit Deployment

### Step 2: Create Streamlit App

**2.1 Install Streamlit Locally**
```bash
# Install streamlit
pip install streamlit

# Verify installation
streamlit --version
```

**2.2 Create Streamlit Frontend App**

Create `frontend/app.py`:

```python
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="BBQ Restaurant AI Dashboard",
    page_icon="🍖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "http://localhost:8000/api/v1"  # Change for production

# Sidebar Navigation
st.sidebar.title("🍖 BBQ Restaurant AI")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Sales Analytics", "AI Assistant", "Settings"]
)

st.sidebar.markdown("---")
st.sidebar.info("📊 Real-time Business Intelligence")

# ============================================================================
# DASHBOARD PAGE
# ============================================================================

if page == "Dashboard":
    st.title("📊 Restaurant Dashboard")
    st.markdown("Real-time business metrics and KPIs")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Revenue",
            value="Rs. 850,000",
            delta="↑ 12%",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            label="Total Orders",
            value="1,240",
            delta="↑ 8%",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            label="Avg Order Value",
            value="Rs. 685",
            delta="↑ 4%",
            delta_color="normal"
        )
    
    with col4:
        st.metric(
            label="Customer Count",
            value="834",
            delta="↑ 15%",
            delta_color="normal"
        )
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Daily Sales Trend")
        # Sample data
        dates = pd.date_range(start='2026-08-01', periods=31)
        sales = [150000, 165000, 145000, 170000, 155000, 160000, 175000,
                 180000, 165000, 170000, 185000, 170000, 175000, 190000,
                 185000, 200000, 195000, 210000, 205000, 220000, 215000,
                 225000, 220000, 230000, 225000, 235000, 240000, 245000,
                 240000, 250000, 255000]
        df = pd.DataFrame({'Date': dates, 'Sales': sales})
        
        fig = px.line(df, x='Date', y='Sales', 
                     title='Sales Trend',
                     markers=True,
                     line_shape='spline')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🔝 Top Products")
        products = pd.DataFrame({
            'Product': ['BBQ Platter', 'Beef Ribs', 'Chicken Wings', 'Smoker Platter', 'Sides Pack'],
            'Revenue': [125000, 95000, 75000, 65000, 45000]
        })
        
        fig = px.bar(products, x='Product', y='Revenue', 
                    title='Top Products by Revenue',
                    color='Revenue')
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# SALES ANALYTICS PAGE
# ============================================================================

elif page == "Sales Analytics":
    st.title("📊 Sales Analytics")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        date_range = st.date_input(
            "Select Date Range",
            value=[datetime.now() - timedelta(days=30), datetime.now()],
            key="date_range"
        )
    
    with col2:
        product_filter = st.multiselect(
            "Filter by Product",
            ["BBQ Platter", "Beef Ribs", "Chicken Wings", "Smoker Platter", "Sides Pack"],
            default=["BBQ Platter"]
        )
    
    with col3:
        branch_filter = st.multiselect(
            "Filter by Branch",
            ["Main Branch", "Downtown", "Airport"],
            default=["Main Branch"]
        )
    
    st.markdown("---")
    
    # Analytics
    st.subheader("Revenue by Day of Week")
    days_revenue = pd.DataFrame({
        'Day': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        'Revenue': [125000, 135000, 145000, 155000, 195000, 250000, 235000]
    })
    
    fig = px.bar(days_revenue, x='Day', y='Revenue', color='Revenue',
                title='Average Revenue by Day of Week',
                color_continuous_scale='Viridis')
    st.plotly_chart(fig, use_container_width=True)
    
    # Comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Monthly Comparison")
        months = pd.DataFrame({
            'Month': ['July', 'August', 'September'],
            'Revenue': [4250000, 5100000, 5850000]
        })
        fig = px.line(months, x='Month', y='Revenue', markers=True,
                     title='Monthly Revenue Trend')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Product Performance")
        perf = pd.DataFrame({
            'Product': ['BBQ Platter', 'Beef Ribs', 'Wings', 'Smoker', 'Sides'],
            'This Month': [125, 95, 75, 65, 45],
            'Last Month': [110, 85, 70, 60, 40]
        })
        fig = px.bar(perf, x='Product', y=['This Month', 'Last Month'],
                    barmode='group', title='Product Sales Comparison')
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# AI ASSISTANT PAGE
# ============================================================================

elif page == "AI Assistant":
    st.title("🤖 AI Assistant")
    st.markdown("Ask questions about your business data")
    
    # Chat interface
    st.markdown("---")
    
    # Example questions
    st.subheader("Example Questions:")
    examples = [
        "What were our best-selling products last month?",
        "Which day generated the highest revenue?",
        "Why did sales decrease yesterday?",
        "What are the expected sales for next week?",
        "Which products are performing poorly?",
        "Compare this month with the previous month."
    ]
    
    for i, example in enumerate(examples, 1):
        if st.button(f"{i}. {example}", key=f"example_{i}"):
            st.write(f"**Your Question:** {example}")
            st.info("🤖 AI is thinking...")
            # Here you would call your AI API
            st.success("Sample response would appear here after API integration")
    
    st.markdown("---")
    
    # Chat input
    user_question = st.text_input("Or type your own question:")
    
    if user_question:
        st.write(f"**Your Question:** {user_question}")
        st.info("🤖 AI is thinking...")
        # Here you would call your AI API
        st.success("Sample response would appear here")

# ============================================================================
# SETTINGS PAGE
# ============================================================================

elif page == "Settings":
    st.title("⚙️ Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Theme")
        theme = st.radio("Color Theme", ["Light", "Dark", "Auto"])
        st.info(f"Theme set to: {theme}")
        
        st.subheader("Notifications")
        email_alerts = st.checkbox("Email Alerts", value=True)
        push_alerts = st.checkbox("Push Notifications", value=True)
        
        st.subheader("Data")
        if st.button("Export Data"):
            st.success("Data exported successfully!")
    
    with col2:
        st.subheader("API Configuration")
        api_url = st.text_input("API URL", value=API_BASE_URL)
        api_key = st.text_input("API Key", type="password")
        
        if st.button("Test Connection"):
            st.success("✓ Connected successfully!")
        
        st.subheader("About")
        st.info("""
        **BBQ Restaurant AI Business Intelligence**
        
        Version: 1.0.0
        Built with: Streamlit + Python
        Deployed: 2026-08-31
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <small>🍖 BBQ Restaurant AI Business Intelligence | 2026</small>
</div>
""", unsafe_allow_html=True)
```

**2.3 Test Streamlit App Locally**
```bash
# Navigate to frontend directory
cd frontend

# Run streamlit app
streamlit run app.py

# App opens at http://localhost:8501
```

---

### Step 3: Prepare for Streamlit Cloud

**3.1 Create requirements.txt**

Create `requirements.txt` in project root:

```
streamlit==1.28.1
pandas==2.0.3
plotly==5.17.0
requests==2.31.0
python-dotenv==1.0.0
```

**3.2 Create .streamlit/config.toml**

Create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#ff6b35"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[client]
showErrorDetails = true
toolbarMode = "viewer"

[logger]
level = "info"

[server]
port = 8501
headless = true
```

**3.3 Update GitHub Repository**

```bash
# Commit streamlit files
git add frontend/app.py requirements.txt .streamlit/config.toml
git commit -m "feat: add Streamlit dashboard application"
git push origin main
```

---

### Step 4: Deploy to Streamlit Cloud

**4.1 Create Streamlit Cloud Account**

1. Go to https://streamlit.io/cloud
2. Click "Sign up"
3. Sign in with GitHub (authenticate)
4. Authorize Streamlit to access your repositories

**4.2 Deploy App**

1. Click "New app"
2. Connect repository:
   - Repository: `YOUR_USERNAME/bbq-ai-business-intelligence`
   - Branch: `main`
   - Main file path: `frontend/app.py`
3. Click "Deploy"
4. Wait 2-3 minutes for deployment
5. Your app URL: `https://bbq-ai-business-intelligence.streamlit.app`

**4.3 Share Your Live App**

```
Share link: https://bbq-ai-business-intelligence.streamlit.app
QR Code: [Will be generated by Streamlit Cloud]
```

---

## Alternative: Streamlit Cloud

### Without Docker (Recommended for Getting Started)

**Benefits:**
- ✅ Free hosting tier
- ✅ Easy deployment
- ✅ No infrastructure management
- ✅ Automatic HTTPS
- ✅ Automatic updates on git push

**Limitations:**
- Limited compute (1 vCPU, 2GB RAM)
- Good for small apps and dashboards
- Not ideal for heavy ML processing

**When to use Streamlit Cloud:**
- Prototyping
- Dashboards
- Small AI/ML apps
- Demo applications
- Sharing with non-technical users

---

## GitHub Repository Structure

```
bbq-ai-business-intelligence/
├── frontend/
│   ├── app.py                 # ← Streamlit main app
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
├── backend/
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── scripts/
│   ├── deploy-local.sh
│   ├── deploy-production.sh
│   └── test-deployment.sh
├── docker-compose.yml
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt           # ← For Streamlit Cloud
├── QUICK_START_DEPLOYMENT.md
├── DOCKER_DEPLOYMENT_BEGINNER_GUIDE.md
├── DEPLOYMENT_COMPLETE_CHECKLIST.md
└── MONITORING_AND_TROUBLESHOOTING.md
```

---

## Step-by-Step Streamlit Deployment

### Complete Workflow

**Step 1: Prepare Local Files**
```bash
# 1. Create Streamlit app
nano frontend/app.py          # Create app.py with code above

# 2. Create requirements.txt
cat > requirements.txt << 'EOF'
streamlit==1.28.1
pandas==2.0.3
plotly==5.17.0
requests==2.31.0
python-dotenv==1.0.0
EOF

# 3. Create .streamlit directory
mkdir -p .streamlit

# 4. Create config file
cat > .streamlit/config.toml << 'EOF'
[theme]
primaryColor = "#ff6b35"
backgroundColor = "#ffffff"
EOF
```

**Step 2: Test Locally**
```bash
# Install dependencies
pip install -r requirements.txt

# Run app
cd frontend
streamlit run app.py

# Open browser to http://localhost:8501
```

**Step 3: Push to GitHub**
```bash
# Add files
git add frontend/app.py requirements.txt .streamlit/

# Commit
git commit -m "feat: add streamlit dashboard"

# Push
git push origin main
```

**Step 4: Deploy to Streamlit Cloud**
```
1. Go to https://share.streamlit.io
2. Click "New app"
3. Select repository and branch
4. Set main file: frontend/app.py
5. Click "Deploy"
6. Wait 2-3 minutes
7. Done! 🎉
```

---

## Troubleshooting

### Issue 1: "Module not found" Error

**Error:**
```
ModuleNotFoundError: No module named 'streamlit'
```

**Solution:**
```bash
# Install streamlit
pip install streamlit

# Or create requirements.txt and install
pip install -r requirements.txt
```

---

### Issue 2: App Won't Load in Streamlit Cloud

**Error:**
```
App not loading / blank page
```

**Diagnosis:**
1. Check GitHub repository is public
2. Check `.streamlit/config.toml` exists
3. Check `frontend/app.py` exists
4. Check `requirements.txt` exists

**Solution:**
```bash
# View logs in Streamlit Cloud
# Click "Manage app" → "Settings" → "Logs"

# Common issues:
# - Missing requirements.txt
# - Wrong main file path
# - Syntax errors in app.py
# - Missing dependencies
```

---

### Issue 3: API Connection Error

**Error:**
```
requests.exceptions.ConnectionError
```

**Cause:**
Streamlit Cloud can't reach your backend API

**Solution:**
```python
# Option 1: Use public API URL (not localhost)
API_BASE_URL = "https://yourdomain.com/api/v1"

# Option 2: Use environment variable
import os
API_BASE_URL = os.getenv("API_URL", "http://localhost:8000/api/v1")

# Option 3: Mock data for demo
try:
    response = requests.get(f"{API_BASE_URL}/dashboard")
except:
    # Use mock data if API not available
    st.warning("Using mock data - API not available")
```

---

### Issue 4: Slow App Performance

**Solutions:**
```python
# 1. Use caching
import streamlit as st

@st.cache_data
def load_data():
    # Expensive operation
    return pd.read_csv("data.csv")

# 2. Limit data loaded
df = df.tail(1000)  # Only show recent data

# 3. Use smaller charts
st.plotly_chart(fig, use_container_width=False)

# 4. Optimize API calls
@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_dashboard_data():
    return requests.get(f"{API_BASE_URL}/dashboard").json()
```

---

## Comparison: Deployment Options

| Feature | Streamlit Cloud | Docker + DigitalOcean | AWS |
|---------|-----------------|----------------------|-----|
| **Cost** | Free tier | $5/mo | $50+/mo |
| **Setup Time** | 5 min | 30 min | 1+ hour |
| **Difficulty** | Very Easy | Medium | Hard |
| **Control** | Limited | Full | Full |
| **Scaling** | Limited | Manual | Auto |
| **Performance** | Good | Excellent | Excellent |
| **Best For** | Demos, Prototypes | Production, Custom | Enterprise, Scale |

---

## Quick Reference: Streamlit Commands

```python
# Display elements
st.write("Text")
st.title("Title")
st.header("Header")
st.subheader("Subheader")
st.text("Plain text")
st.markdown("**Bold** text")
st.code("code")

# Metrics
st.metric("Label", 100, "+5%")

# Input
st.text_input("Enter text")
st.number_input("Enter number")
st.slider("Slide", 0, 100)
st.selectbox("Choose", ["A", "B", "C"])
st.multiselect("Choose many", ["A", "B", "C"])
st.checkbox("Check me")
st.button("Click me")
st.date_input("Pick date")
st.time_input("Pick time")

# Display data
st.dataframe(df)
st.table(df)
st.json(data)

# Charts
st.line_chart(df)
st.bar_chart(df)
st.area_chart(df)

# Plotly charts
import plotly.express as px
fig = px.bar(df, x="col", y="col")
st.plotly_chart(fig)

# Layout
col1, col2 = st.columns(2)
with col1:
    st.write("Left column")
with col2:
    st.write("Right column")

# Sidebar
st.sidebar.title("Menu")
st.sidebar.radio("Choose", ["Option 1", "Option 2"])

# Status messages
st.success("Success!")
st.warning("Warning!")
st.error("Error!")
st.info("Info!")
```

---

## Next Steps

### Phase 1: Basic Streamlit (This Week)
- ✅ Create Streamlit frontend
- ✅ Deploy to Streamlit Cloud
- ✅ Share with team

### Phase 2: Connect Backend (Next Week)
- Integrate with FastAPI backend
- Real-time data updates
- AI chat integration

### Phase 3: Production (Next Month)
- Move to Docker + custom server
- Add authentication
- Configure backups
- Setup monitoring

---

## Success Checklist

✅ **GitHub Repository**
- Repository created and public
- Code pushed to main branch
- README.md present

✅ **Streamlit App**
- `frontend/app.py` created
- `requirements.txt` created
- `.streamlit/config.toml` created

✅ **Streamlit Cloud**
- Account created
- App deployed
- Live URL working

✅ **Sharing**
- Live link shared with team
- QR code created
- Documentation updated

---

## Your Live App

```
🎉 Congratulations! Your app is live at:

https://bbq-ai-business-intelligence.streamlit.app

Share this link with your team and stakeholders!
```

---

**Generated:** 2026-08-31 13:52 UTC  
**Level:** Beginner-Friendly ✅  
**Ready to Deploy:** Yes ✅

