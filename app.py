import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


st.set_page_config(
    page_title="Saudi Insurance Fraud Analysis",
    ##page_icon="?what do i even use here bro",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    #Fraud correlation data
    fraud_data = {
        'FRAUD_INDICATOR': [0, 1],
        'AVG_PAYMENT_RATIO': [1.0000118113, 1.4797615504],
        'TOTAL': [18006786, 1993214]
    }
    
    #Gender analysis data
    gender_data = {
        'GENDER': ['Female', 'Male'],
        'COUNT': [10002860, 9997140],
        'AVG_CLAIM': [14576.47, 14618.33],
        'AVG_PAID': [15274.41, 15316.03]
    }
    
    #Regional data
    region_data = {
        'REGION': ['Qassim', 'Jazan', 'Tabuk', 'Najran', 'Madinah', 'Hail', 
                  'Eastern Province', 'Al Bahah', 'Asir', 'Makkah', 'Al Jawf', 
                  'Northern Borders', 'Riyadh'],
        'TOTAL_CLAIMS': [1539672, 1538634, 1540058, 1541848, 1536090, 1535090,
                        1536420, 1537662, 1537598, 1538714, 1540722, 1537658, 1539834],
        'FRAUD_CLAIMS': [0] * 13,
        'FRAUD_PERCENTAGE': [0.0] * 13
    }
    
    #Procedure analysis data
    procedure_data = {
        'PROCEDURE': ['Heart Bypass Surgery', 'Knee Replacement', 'Appendectomy', 
                     'Childbirth (C-Section)', 'Cataract Surgery', 'Childbirth (Normal)',
                     'Tonsillectomy', 'Colonoscopy', 'MRI Scan', 'CT Scan',
                     'Emergency Room Visit', 'Prescription Medication', 'Annual Checkup',
                     'Physical Therapy (per session)', 'Dental Cleaning'],
        'TOTAL': [1334078, 1332746, 1332728, 1330344, 1336610, 1331676, 1335894,
                 1337294, 1331902, 1335706, 1331704, 1331856, 1332296, 1333486, 1331680],
        'AVG_PAID': [99050.94, 49514.44, 18568.68, 18565.47, 12380.88, 9906.71,
                    9900.06, 3713.75, 2475.34, 1857.09, 1237.76, 743.04, 618.62, 495.06, 371.37]
    }
    
    return (pd.DataFrame(fraud_data), pd.DataFrame(gender_data), 
            pd.DataFrame(region_data), pd.DataFrame(procedure_data))


fraud_df, gender_df, region_df, procedure_df = load_data()

#creating side bar here
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose Analysis", 
                           ["Overview", "Fraud Analysis", "Gender Analysis", 
                            "Regional Analysis", "Procedure Analysis"])


st.markdown('<h1 class="main-header">Saudi Insurance Fraud Analysis Dashboard</h1>', 
            unsafe_allow_html=True)

if page == "Overview":
    st.markdown("## Executive Summary")
    
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_claims = fraud_df['TOTAL'].sum()
        st.metric("Total Claims", f"{total_claims:,}")
    
    with col2:
        fraud_claims = fraud_df[fraud_df['FRAUD_INDICATOR'] == 1]['TOTAL'].iloc[0]
        fraud_rate = (fraud_claims / total_claims) * 100
        st.metric("Fraud Claims", f"{fraud_claims:,}", f"{fraud_rate:.2f}%")
    
    with col3:
        avg_procedure_cost = procedure_df['AVG_PAID'].mean()
        st.metric("Avg Procedure Cost", f"${avg_procedure_cost:,.2f}")
    
    with col4:
        total_regions = len(region_df)
        st.metric("Regions Analyzed", total_regions)
    
    st.markdown("---")
    
   
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Fraud vs Normal Claims")
        fig_fraud_overview = px.pie(
            fraud_df, 
            values='TOTAL', 
            names=['Normal', 'Fraud'],
            title="Distribution of Claims by Type",
            color_discrete_sequence=['#00cc96', '#ff6b6b']
        )
        st.plotly_chart(fig_fraud_overview, use_container_width=True)
    
    with col2:
        st.subheader("Top 5 Most Expensive Procedures")
        top_procedures = procedure_df.nlargest(5, 'AVG_PAID')
        fig_top_procedures = px.bar(
            top_procedures,
            x='AVG_PAID',
            y='PROCEDURE',
            orientation='h',
            title="Average Cost per Procedure",
            color='AVG_PAID',
            color_continuous_scale='viridis'
        )
        fig_top_procedures.update_layout(showlegend=False)
        st.plotly_chart(fig_top_procedures, use_container_width=True)

elif page == "Fraud Analysis":
    st.markdown("## Fraud Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(" Fraud Detection Metrics")
        
        #Payment ratio comparison
        fig_payment_ratio = go.Figure()
        fig_payment_ratio.add_trace(go.Bar(
            x=['Normal Claims', 'Fraudulent Claims'],
            y=fraud_df['AVG_PAYMENT_RATIO'],
            marker_color=['#00cc96', '#ff6b6b'],
            text=[f'{x:.4f}' for x in fraud_df['AVG_PAYMENT_RATIO']],
            textposition='auto'
        ))
        fig_payment_ratio.update_layout(
            title="Average Payment Ratio: Normal vs Fraudulent Claims",
            yaxis_title="Payment Ratio",
            xaxis_title="Claim Type"
        )
        st.plotly_chart(fig_payment_ratio, use_container_width=True)
        
        #Key insights
        st.markdown("### Key Insights")
        payment_diff = fraud_df['AVG_PAYMENT_RATIO'].iloc[1] - fraud_df['AVG_PAYMENT_RATIO'].iloc[0]
        st.write(f"• Fraudulent claims have {payment_diff:.2f} higher payment ratio")
        st.write(f"• This represents a {(payment_diff/fraud_df['AVG_PAYMENT_RATIO'].iloc[0])*100:.1f}% increase")
        st.write(f"• {fraud_df['TOTAL'].iloc[1]:,} fraudulent claims detected")
    
    with col2:
        st.subheader("Fraud Impact Analysis")
        
        #Create impact visualization
        fraud_impact = pd.DataFrame({
            'Metric': ['Total Claims', 'Fraudulent Claims', 'Clean Claims'],
            'Count': [fraud_df['TOTAL'].sum(), fraud_df['TOTAL'].iloc[1], fraud_df['TOTAL'].iloc[0]],
            'Percentage': [100, 
                          (fraud_df['TOTAL'].iloc[1]/fraud_df['TOTAL'].sum())*100,
                          (fraud_df['TOTAL'].iloc[0]/fraud_df['TOTAL'].sum())*100]
        })
        
        fig_impact = px.funnel(
            fraud_impact,
            x='Count',
            y='Metric',
            title="Fraud Detection Funnel",
            color='Metric',
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(fig_impact, use_container_width=True)
        
        #Financial impact
        st.markdown("### Financial Impact")
        normal_avg = fraud_df['AVG_PAYMENT_RATIO'].iloc[0]
        fraud_avg = fraud_df['AVG_PAYMENT_RATIO'].iloc[1]
        estimated_loss = fraud_df['TOTAL'].iloc[1] * (fraud_avg - normal_avg) * 1000  
        st.metric("Estimated Excess Payment", f"${estimated_loss:,.2f}")

elif page == "Gender Analysis":
    st.markdown("## Gender-Based Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Claims Distribution by Gender")
        
        
        fig_gender_dist = px.pie(
            gender_df,
            values='COUNT',
            names='GENDER',
            title="Distribution of Claims by Gender",
            color_discrete_sequence=['#ff9999', '#66b3ff']
        )
        st.plotly_chart(fig_gender_dist, use_container_width=True)
        
       
        st.markdown("### Gender Metrics")
        for _, row in gender_df.iterrows():
            st.write(f"**{row['GENDER']}:**")
            st.write(f"  • Total Claims: {row['COUNT']:,}")
            st.write(f"  • Avg Claim: ${row['AVG_CLAIM']:,.2f}")
            st.write(f"  • Avg Paid: ${row['AVG_PAID']:,.2f}")
            st.write("")
    
    with col2:
        st.subheader("Average Amounts by Gender")
        
       
        fig_gender_comparison = go.Figure()
        fig_gender_comparison.add_trace(go.Bar(
            name='Average Claim',
            x=gender_df['GENDER'],
            y=gender_df['AVG_CLAIM'],
            marker_color='lightblue'
        ))
        fig_gender_comparison.add_trace(go.Bar(
            name='Average Paid',
            x=gender_df['GENDER'],
            y=gender_df['AVG_PAID'],
            marker_color='lightcoral'
        ))
        fig_gender_comparison.update_layout(
            title="Average Claim vs Average Paid by Gender",
            yaxis_title="Amount ($)",
            barmode='group'
        )
        st.plotly_chart(fig_gender_comparison, use_container_width=True)
        
        
        st.markdown("### Gender Analysis Insights")
        male_claim_diff = gender_df[gender_df['GENDER'] == 'Male']['AVG_CLAIM'].iloc[0] - gender_df[gender_df['GENDER'] == 'Female']['AVG_CLAIM'].iloc[0]
        male_paid_diff = gender_df[gender_df['GENDER'] == 'Male']['AVG_PAID'].iloc[0] - gender_df[gender_df['GENDER'] == 'Female']['AVG_PAID'].iloc[0]
        
        st.write(f"• Male claims are ${male_claim_diff:.2f} higher on average")
        st.write(f"• Male payments are ${male_paid_diff:.2f} higher on average")
        st.write(f"• Claims distribution is nearly equal between genders")

elif page == "Regional Analysis":
    st.markdown("## Regional Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Claims by Region")
        
        
        region_sorted = region_df.sort_values('TOTAL_CLAIMS', ascending=True)
        
        fig_regional = px.bar(
            region_sorted,
            x='TOTAL_CLAIMS',
            y='REGION',
            orientation='h',
            title="Total Claims by Region",
            color='TOTAL_CLAIMS',
            color_continuous_scale='viridis'
        )
        fig_regional.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig_regional, use_container_width=True)
    
    with col2:
        st.subheader("Regional Insights")
        
        
        max_claims = region_df['TOTAL_CLAIMS'].max()
        min_claims = region_df['TOTAL_CLAIMS'].min()
        avg_claims = region_df['TOTAL_CLAIMS'].mean()
        
        st.metric("Highest Claims", f"{max_claims:,}")
        st.metric("Lowest Claims", f"{min_claims:,}")
        st.metric("Average Claims", f"{avg_claims:,.0f}")
        
        # Top and bottom regions
        st.markdown("### Top 3 Regions")
        top_regions = region_df.nlargest(3, 'TOTAL_CLAIMS')
        for i, (_, row) in enumerate(top_regions.iterrows(), 1):
            st.write(f"{i}. {row['REGION']}: {row['TOTAL_CLAIMS']:,}")
        
        st.markdown("### Bottom 3 Regions")
        bottom_regions = region_df.nsmallest(3, 'TOTAL_CLAIMS')
        for i, (_, row) in enumerate(bottom_regions.iterrows(), 1):
            st.write(f"{i}. {row['REGION']}: {row['TOTAL_CLAIMS']:,}")
    
    
    st.markdown("---")
    st.info("**Note:** All regions currently show 0% fraud rate, indicating either effective fraud prevention or potential gaps in fraud detection systems.")

elif page == "Procedure Analysis":
    st.markdown("## Medical Procedure Analysis")
    
    
    st.sidebar.markdown("### Filter Options")
    cost_range = st.sidebar.slider("Cost Range ($)", 
                                  min_value=0, 
                                  max_value=int(procedure_df['AVG_PAID'].max()),
                                  value=(0, int(procedure_df['AVG_PAID'].max())),
                                  step=1000)
    
    
    filtered_procedures = procedure_df[
        (procedure_df['AVG_PAID'] >= cost_range[0]) & 
        (procedure_df['AVG_PAID'] <= cost_range[1])
    ]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Procedure Costs")
        
       
        fig_cost_dist = px.bar(
            filtered_procedures.sort_values('AVG_PAID', ascending=True),
            x='AVG_PAID',
            y='PROCEDURE',
            orientation='h',
            title="Average Cost per Procedure",
            color='AVG_PAID',
            color_continuous_scale='plasma'
        )
        fig_cost_dist.update_layout(height=600, showlegend=False)
        st.plotly_chart(fig_cost_dist, use_container_width=True)
    
    with col2:
        st.subheader("Procedure Volume")
        
        
        fig_volume = px.bar(
            filtered_procedures.sort_values('TOTAL', ascending=True),
            x='TOTAL',
            y='PROCEDURE',
            orientation='h',
            title="Total Procedures Performed",
            color='TOTAL',
            color_continuous_scale='blues'
        )
        fig_volume.update_layout(height=600, showlegend=False)
        st.plotly_chart(fig_volume, use_container_width=True)
    
    
    st.markdown("---")
    st.markdown("### Procedure Analysis Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Most Expensive")
        expensive = filtered_procedures.nlargest(3, 'AVG_PAID')
        for _, row in expensive.iterrows():
            st.write(f"• {row['PROCEDURE']}: ${row['AVG_PAID']:,.2f}")
    
    with col2:
        st.markdown("#### Most Common")
        common = filtered_procedures.nlargest(3, 'TOTAL')
        for _, row in common.iterrows():
            st.write(f"• {row['PROCEDURE']}: {row['TOTAL']:,}")
    
    with col3:
        st.markdown("#### Cost-Effective")
        affordable = filtered_procedures.nsmallest(3, 'AVG_PAID')
        for _, row in affordable.iterrows():
            st.write(f"• {row['PROCEDURE']}: ${row['AVG_PAID']:,.2f}")

#Footer
st.markdown("---")
st.markdown("**Data Source:** Snowflake Data Analysis Project | **Dashboard Created with:** Streamlit & Plotly")
st.markdown("*Saudi Insurance Fraud Analysis Dashboard - Comprehensive Healthcare Claims Analysis*")