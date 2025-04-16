import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Currency configuration
CURRENCIES = {
    'USD': {'symbol': '$', 'name': 'US Dollar', 'icon': '💵'},
    'EUR': {'symbol': '€', 'name': 'Euro', 'icon': '💶'},
    'SEK': {'symbol': 'kr', 'name': 'Swedish Krona', 'icon': '🇸🇪'},
    'INR': {'symbol': '₹', 'name': 'Indian Rupee', 'icon': '🇮🇳'}
}

# Set page config
st.set_page_config(
    page_title="Trade Risk Calculator",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    .stButton>button {
        background-color: #3498db;
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
    }
    .stButton>button:hover {
        background-color: #2980b9;
    }
    .card {
        background-color: #2c3e50;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .success-alert {
        border-left: 4px solid #2ecc71;
        padding-left: 1rem;
        margin-bottom: 1rem;
    }
    .exit-strategy {
        background-color: #2c3e50;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def generate_risk_reward_table(entry_price, base_target, risk_per_share, n_steps=5):
    """Generate a table showing risk-to-reward ratios for different target prices."""
    base_reward = base_target - entry_price
    if base_reward <= 0:
        return pd.DataFrame()
    
    multipliers = np.linspace(0.8, 1.2, n_steps)
    target_prices = entry_price + base_reward * multipliers
    
    data = {
        'Target Price': target_prices,
        'Reward per Share': target_prices - entry_price,
        'Risk-to-Reward Ratio': risk_per_share / (target_prices - entry_price),
        'Reward-to-Risk Ratio': (target_prices - entry_price) / risk_per_share
    }
    
    return pd.DataFrame(data)

def calculate_exit_strategy(entry_price, target_price, number_of_shares):
    """Calculate the 3-part exit strategy."""
    target1 = target_price
    target2 = entry_price + 2 * (target_price - entry_price)
    target3 = entry_price + 3 * (target_price - entry_price)
    
    shares_per_target = number_of_shares / 3
    profit1 = shares_per_target * (target1 - entry_price)
    profit2 = shares_per_target * (target2 - entry_price)
    profit3 = shares_per_target * (target3 - entry_price)
    total_profit = profit1 + profit2 + profit3
    
    return {
        'targets': [target1, target2, target3],
        'profits': [profit1, profit2, profit3],
        'total_profit': total_profit,
        'shares_per_target': shares_per_target
    }

def calculate_standard_risk(account_size, risk_percentage, number_of_shares, entry_price, target_price):
    """Calculate standard risk metrics."""
    risk_fraction = risk_percentage / 100.0
    total_risk = account_size * risk_fraction
    risk_per_share = total_risk / number_of_shares
    recommended_stop_loss = entry_price - risk_per_share
    capital_required = number_of_shares * entry_price
    reward_per_share = target_price - entry_price
    
    exit_strategy = calculate_exit_strategy(entry_price, target_price, number_of_shares)
    
    return {
        'total_risk': total_risk,
        'risk_per_share': risk_per_share,
        'recommended_stop_loss': recommended_stop_loss,
        'capital_required': capital_required,
        'reward_per_share': reward_per_share,
        'exit_strategy': exit_strategy
    }

def calculate_position_size(account_size, risk_percentage, entry_price, technical_stoploss, target_price):
    """Calculate position size based on technical analysis."""
    risk_fraction = risk_percentage / 100.0
    total_risk = account_size * risk_fraction
    risk_per_share_tech = entry_price - technical_stoploss
    adjusted_shares = total_risk / risk_per_share_tech
    adjusted_shares_div3 = round(adjusted_shares / 3) * 3
    capital_required = adjusted_shares_div3 * entry_price
    
    exit_strategy = calculate_exit_strategy(entry_price, target_price, adjusted_shares_div3)
    
    return {
        'adjusted_shares': adjusted_shares,
        'adjusted_shares_div3': adjusted_shares_div3,
        'capital_required': capital_required,
        'risk_per_share_tech': risk_per_share_tech,
        'exit_strategy': exit_strategy
    }

def format_currency(value, currency='USD'):
    """Format a number as currency with the appropriate symbol."""
    symbol = CURRENCIES[currency]['symbol']
    return f"{value:,.2f} ({currency})"

def display_exit_strategy(exit_strategy, currency='USD'):
    """Display the exit strategy in a formatted way."""
    st.markdown("#### Exit Strategy")
    st.markdown('<div class="exit-strategy">', unsafe_allow_html=True)
    
    for i, (target, profit) in enumerate(zip(exit_strategy['targets'], exit_strategy['profits']), 1):
        st.markdown(f"""
        **Target {i}**
        - Price: {format_currency(target, currency)}
        - Shares: {exit_strategy['shares_per_target']:.0f}
        - Profit: {format_currency(profit, currency)}
        - Action: {'Sell 1/3 position, move stop to entry' if i == 1 else 
                  'Sell 1/3 position, move stop to Target 1' if i == 2 else 
                  'Sell remaining position'}
        """)
    
    st.markdown(f"""
    **Total Potential Profit**: {format_currency(exit_strategy['total_profit'], currency)}
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# Main app
st.title("Trade Risk Calculator")
st.markdown("Calculate optimal position sizes and manage risk effectively")

# Initialize session state for currency if not exists
if 'selected_currency' not in st.session_state:
    st.session_state.selected_currency = 'USD'

# Currency selector with icons
st.markdown("### Select Currency")
currency_cols = st.columns(len(CURRENCIES))
for i, (currency_code, currency_info) in enumerate(CURRENCIES.items()):
    with currency_cols[i]:
        if st.button(
            f"{currency_info['icon']} {currency_code}",
            key=f"currency_{currency_code}",
            use_container_width=True,
            type="primary" if st.session_state.selected_currency == currency_code else "secondary"
        ):
            st.session_state.selected_currency = currency_code

# Info box
with st.expander("ℹ️ Important Information", expanded=True):
    st.info("""
    - Use the Standard Calculator for basic risk assessment
    - Fine-tune with the Position Size Calculator
    - All calculations assume a 3-part exit strategy for optimal risk management
    """)

# Create two columns for the calculators
col1, col2 = st.columns(2)

# Standard Risk Calculator
with col1:
    st.subheader("Standard Risk Calculator")
    with st.form("standard_calculator"):
        account_size_1 = st.number_input(f"Account Size ({CURRENCIES[st.session_state.selected_currency]['symbol']})", value=5000.0, min_value=1.0, step=100.0)
        risk_percentage_1 = st.number_input("Risk Percentage", value=1.0, min_value=0.1, max_value=5.0, step=0.1)
        number_of_shares_1 = st.number_input("Number of Shares", value=45.0, min_value=1.0, step=1.0)
        entry_price_1 = st.number_input(f"Entry Price per Share ({CURRENCIES[st.session_state.selected_currency]['symbol']})", value=10.0, min_value=0.01, step=0.01)
        target_price_1 = st.number_input(f"Target Price per Share ({CURRENCIES[st.session_state.selected_currency]['symbol']})", value=12.50, min_value=0.01, step=0.01)
        
        if st.form_submit_button("Calculate Risk"):
            results = calculate_standard_risk(
                account_size_1, risk_percentage_1, number_of_shares_1,
                entry_price_1, target_price_1
            )
            
            st.markdown("### Trade Analysis")
            st.markdown("#### Capital Requirements")
            st.write(f"Total Capital: {format_currency(results['capital_required'], st.session_state.selected_currency)}")
            st.write(f"Risk per Trade: {format_currency(results['total_risk'], st.session_state.selected_currency)}")
            st.write(f"Risk per Share: {format_currency(results['risk_per_share'], st.session_state.selected_currency)}")
            
            st.markdown("#### Risk Metrics")
            st.write(f"Stop Loss: {format_currency(results['recommended_stop_loss'], st.session_state.selected_currency)}")
            st.write(f"Reward per Share: {format_currency(results['reward_per_share'], st.session_state.selected_currency)}")
            
            # Risk-to-Reward Matrix
            st.markdown("#### Risk-to-Reward Matrix")
            matrix = generate_risk_reward_table(
                entry_price_1, target_price_1, results['risk_per_share']
            )
            st.dataframe(matrix.style.format({
                'Target Price': lambda x: format_currency(x, st.session_state.selected_currency),
                'Reward per Share': lambda x: format_currency(x, st.session_state.selected_currency),
                'Risk-to-Reward Ratio': '{:.2f}',
                'Reward-to-Risk Ratio': '{:.2f}:1'
            }))
            
            # Display Exit Strategy
            display_exit_strategy(results['exit_strategy'], st.session_state.selected_currency)

# Position Size Calculator
with col2:
    st.subheader("Position Size Calculator")
    with st.form("position_calculator"):
        account_size_2 = st.number_input(f"Account Size ({CURRENCIES[st.session_state.selected_currency]['symbol']})", value=5000.0, min_value=1.0, step=100.0, key="account_size_2")
        risk_percentage_2 = st.number_input("Risk Percentage", value=1.0, min_value=0.1, max_value=5.0, step=0.1, key="risk_percentage_2")
        entry_price_2 = st.number_input(f"Entry Price per Share ({CURRENCIES[st.session_state.selected_currency]['symbol']})", value=10.0, min_value=0.01, step=0.01, key="entry_price_2")
        technical_stoploss = st.number_input(f"Technical Stop Loss Price ({CURRENCIES[st.session_state.selected_currency]['symbol']})", value=8.89, min_value=0.01, step=0.01)
        target_price_2 = st.number_input(f"Target Price per Share ({CURRENCIES[st.session_state.selected_currency]['symbol']})", value=12.50, min_value=0.01, step=0.01, key="target_price_2")
        
        if st.form_submit_button("Calculate Position Size"):
            results = calculate_position_size(
                account_size_2, risk_percentage_2, entry_price_2,
                technical_stoploss, target_price_2
            )
            
            st.markdown("### Trade Analysis")
            st.markdown("#### Position Details")
            st.write(f"Adjusted Position Size: {results['adjusted_shares']:.2f} shares")
            st.write(f"Rounded Position Size: {results['adjusted_shares_div3']} shares")
            st.write(f"Total Capital Required: {format_currency(results['capital_required'], st.session_state.selected_currency)}")
            st.write(f"Technical Risk per Share: {format_currency(results['risk_per_share_tech'], st.session_state.selected_currency)}")
            
            # Risk-to-Reward Matrix
            st.markdown("#### Risk-to-Reward Matrix")
            matrix = generate_risk_reward_table(
                entry_price_2, target_price_2, results['risk_per_share_tech']
            )
            st.dataframe(matrix.style.format({
                'Target Price': lambda x: format_currency(x, st.session_state.selected_currency),
                'Reward per Share': lambda x: format_currency(x, st.session_state.selected_currency),
                'Risk-to-Reward Ratio': '{:.2f}',
                'Reward-to-Risk Ratio': '{:.2f}:1'
            }))
            
            # Display Exit Strategy
            display_exit_strategy(results['exit_strategy'], st.session_state.selected_currency)

# Risk Management Tips
st.markdown("### Risk Management Tips")
tips = [
    "Never risk more than 2% of your account on a single trade",
    "Use stop-loss orders to protect your capital",
    "Consider scaling out of positions to lock in profits",
    "Regularly review and adjust your risk parameters"
]

for tip in tips:
    st.markdown(f"✅ {tip}")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by JS") 