import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

# Set page configuration
st.set_page_config(
    page_title="GRS System Modernization Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS with improved styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
    }
    .metric-card {
        border: 1px solid #e6e6e6;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
    .recommendation {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("Settings & Filters")
    
    # Theme selection
    theme = st.selectbox("Color Theme", ["Light", "Dark"])
    
    # View options
    st.subheader("View Options")
    show_raw_data = st.checkbox("Show Raw Data Tables", True)
    enable_animations = st.checkbox("Enable Chart Animations", True)
    
    # Filters
    st.subheader("Analysis Filters")
    min_score = st.slider("Minimum Score Filter", 0, 10, 0)
    selected_factors = st.multiselect(
        "Factor Focus",
        ['Development Speed', 'Scalability', 'Cost', 'Customizability', 'Security'],
        ['Development Speed', 'Cost']
    )
    
    # Export options
    st.subheader("Export Options")
    if st.button("Export Analysis as PDF"):
        st.info("PDF export functionality will be implemented in the next version")
    
    if st.button("Download Raw Data (CSV)"):
        st.download_button(
            label="Download Data",
            data=df_comparison.to_csv(index=False),
            file_name="comparison_data.csv",
            mime="text/csv"
        )

# Title with improved styling
st.title("🚀 GRS System Modernization Options Comparison")
st.markdown("### Comprehensive Analysis: Microsoft Stack vs Azure Power Apps")

# Create comparison data
comparison_data = {
    'Factor': [
        'Development Speed',
        'Scalability',
        'Initial Cost',
        'Ongoing Cost',
        'Customizability',
        'Maintenance Effort',
        'Time-to-Market',
        'Security Features',
        'Integration Capability',
        'Learning Curve'
    ],
    'Microsoft Stack': [7, 6, 8, 7, 9, 6, 7, 8, 9, 8],
    'Azure Power Apps': [9, 9, 6, 7, 7, 8, 9, 9, 8, 6]
}

df_comparison = pd.DataFrame(comparison_data)

# Timeline data with more detailed breakdown
timeline_data = {
    'Phase': [
        'Environment Setup',
        'Base Implementation',
        'Core Features',
        'Integration',
        'Testing',
        'Deployment'
    ],
    'Microsoft Stack': [30, 45, 60, 45, 30, 15],
    'Azure Power Apps': [15, 30, 45, 30, 30, 15],
    'Risk Level': ['Low', 'Medium', 'High', 'High', 'Medium', 'Low']
}

df_timeline = pd.DataFrame(timeline_data)

# Enhanced cost breakdown data
cost_breakdown = {
    'Category': [
        'Licensing',
        'Infrastructure',
        'Development',
        'Training',
        'Maintenance'
    ],
    'Microsoft Stack': [50000, 30000, 80000, 20000, 25000],
    'Azure Power Apps': [70000, 15000, 60000, 30000, 15000]
}

df_costs = pd.DataFrame(cost_breakdown)

# Create tabs with enhanced styling
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Comparison Matrix",
    "⏱️ Timeline Analysis",
    "💰 Cost Analysis",
    "✨ Feature Comparison",
    "📈 ROI Calculator"
])

with tab1:
    st.header("Comprehensive Comparison Matrix")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Enhanced radar chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=df_comparison['Microsoft Stack'],
            theta=df_comparison['Factor'],
            fill='toself',
            name='Microsoft Stack',
            line_color='#1f77b4'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=df_comparison['Azure Power Apps'],
            theta=df_comparison['Factor'],
            fill='toself',
            name='Azure Power Apps',
            line_color='#ff7f0e'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10],
                    tickfont=dict(size=10)
                )),
            showlegend=True,
            height=600,
            title="Radar Analysis of Key Factors"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Score Summary")
        # Create a summary DataFrame for better presentation
        summary_df = pd.DataFrame({
            'Factor': df_comparison['Factor'],
            'Microsoft Stack': df_comparison['Microsoft Stack'],
            'Azure Power Apps': df_comparison['Azure Power Apps'],
            'Difference': df_comparison['Azure Power Apps'] - df_comparison['Microsoft Stack']
        })
        
        # Format the table with highlighting
        st.dataframe(
            summary_df.style
            .format({
                'Microsoft Stack': '{:.1f}',
                'Azure Power Apps': '{:.1f}',
                'Difference': '{:+.1f}'
            })
            .background_gradient(subset=['Difference'], cmap='RdYlGn', vmin=-5, vmax=5)
            .set_properties(**{'text-align': 'center'})
            .set_table_styles([
                {'selector': 'th', 'props': [('text-align', 'center')]},
                {'selector': 'td', 'props': [('text-align', 'center')]}
            ]),
            use_container_width=True
        )

with tab2:
    st.header("Implementation Timeline Analysis")
    
    # Enhanced Gantt-like chart
    fig = go.Figure()
    
    colors = {'Low': 'green', 'Medium': 'orange', 'High': 'red'}
    
    for platform in ['Microsoft Stack', 'Azure Power Apps']:
        for i, phase in enumerate(df_timeline['Phase']):
            fig.add_trace(go.Bar(
                name=f"{platform} - {phase}",
                y=[platform],
                x=[df_timeline.loc[i, platform]],
                orientation='h',
                marker_color=colors[df_timeline.loc[i, 'Risk Level']],
                customdata=[[phase, df_timeline.loc[i, 'Risk Level']]],
                hovertemplate="<b>%{customdata[0]}</b><br>" +
                            "Duration: %{x} days<br>" +
                            "Risk Level: %{customdata[1]}<extra></extra>"
            ))
    
    fig.update_layout(
        barmode='stack',
        height=200,
        xaxis_title="Days",
        yaxis_title="Platform",
        showlegend=False,
        title="Implementation Timeline with Risk Levels"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Risk level legend
    st.markdown("### Risk Levels")
    cols = st.columns(3)
    cols[0].markdown("🟢 Low Risk")
    cols[1].markdown("🟡 Medium Risk")
    cols[2].markdown("🔴 High Risk")

with tab3:
    st.header("Detailed Cost Analysis")
    
    # Enhanced cost visualization
    fig = go.Figure()
    
    # Add bars for Microsoft Stack
    fig.add_trace(go.Bar(
        name='Microsoft Stack',
        x=df_costs['Category'],
        y=df_costs['Microsoft Stack'],
        marker_color='#1f77b4',
        text=df_costs['Microsoft Stack'].apply(lambda x: f'${x:,.0f}'),
        textposition='auto',
    ))
    
    # Add bars for Azure Power Apps
    fig.add_trace(go.Bar(
        name='Azure Power Apps',
        x=df_costs['Category'],
        y=df_costs['Azure Power Apps'],
        marker_color='#ff7f0e',
        text=df_costs['Azure Power Apps'].apply(lambda x: f'${x:,.0f}'),
        textposition='auto',
    ))
    
    fig.update_layout(
        barmode='group',
        height=500,
        yaxis_title="Cost (USD)",
        xaxis_title="Category",
        title="Cost Comparison by Category"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Total cost comparison
    col1, col2 = st.columns(2)
    
    with col1:
        ms_total = df_costs['Microsoft Stack'].sum()
        st.metric(
            "Total Microsoft Stack Cost",
            f"${ms_total:,.2f}",
            delta=f"${ms_total - df_costs['Azure Power Apps'].sum():,.2f}"
        )
    
    with col2:
        pa_total = df_costs['Azure Power Apps'].sum()
        st.metric(
            "Total Azure Power Apps Cost",
            f"${pa_total:,.2f}",
            delta=f"${df_costs['Azure Power Apps'].sum() - ms_total:,.2f}"
        )

with tab4:
    st.header("Feature Comparison")
    
    features = {
        'Feature': [
            'Built-in Security',
            'Compliance Tools',
            'Mobile Support',
            'Custom Development',
            'Third-party Integration',
            'Automated Testing',
            'Version Control',
            'Deployment Automation',
            'Performance Monitoring',
            'Disaster Recovery'
        ],
        'Microsoft Stack': ['✅', '✅', '⚠️', '✅', '✅', '✅', '✅', '✅', '✅', '✅'],
        'Azure Power Apps': ['✅', '✅', '✅', '⚠️', '✅', '✅', '✅', '✅', '✅', '✅'],
        'Notes': [
            'Both platforms offer enterprise-grade security',
            'Built-in compliance features in both',
            'Native in Power Apps, requires custom dev in MS Stack',
            'Full control in MS Stack, limited in Power Apps',
            'Extensive integration capabilities in both',
            'Built-in testing tools available',
            'Standard source control integration',
            'CI/CD pipeline support',
            'Comprehensive monitoring tools',
            'Built-in DR capabilities'
        ]
    }
    
    df_features = pd.DataFrame(features)
    
    # Display feature comparison as a styled table
    st.dataframe(
        df_features.style
        .set_properties(**{
            'background-color': 'white',
            'color': 'black',
            'border-color': '#d3d3d3',
            'padding': '10px'
        })
        .set_table_styles([
            {'selector': 'th', 'props': [
                ('background-color', '#f0f2f6'),
                ('color', 'black'),
                ('font-weight', 'bold'),
                ('text-align', 'left'),
                ('padding', '10px')
            ]},
            {'selector': 'td', 'props': [
                ('text-align', 'left'),
                ('padding', '10px')
            ]}
        ])
        .apply(lambda x: ['background-color: #f8f9fa' if i % 2 == 0 else '' for i in range(len(x))], axis=0),
        use_container_width=True,
        height=400
    )
    
    # Add legend for symbols
    st.markdown("---")
    st.markdown("### Legend")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("✅ - Full Support")
    with col2:
        st.markdown("⚠️ - Partial/Limited Support")
    with col3:
        st.markdown("❌ - Not Supported")

with tab5:
    st.header("ROI Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Input Parameters")
        num_users = st.slider("Number of Users", 10, 1000, 50)
        project_months = st.slider("Project Duration (Months)", 6, 36, 12)
        complexity = st.selectbox("Project Complexity", ["Low", "Medium", "High"])
        expected_roi = st.slider("Expected ROI (%)", 0, 200, 100)

    # Calculate estimated costs and ROI
    def calculate_costs_and_roi(users, months, complexity, roi_percentage):
        complexity_factor = {"Low": 0.8, "Medium": 1.0, "High": 1.3}
        factor = complexity_factor[complexity]
        
        ms_stack_cost = (users * 100 * months + 50000) * factor
        power_apps_cost = (users * 40 * months + 30000) * factor
        
        ms_roi = (ms_stack_cost * (1 + roi_percentage/100)) - ms_stack_cost
        pa_roi = (power_apps_cost * (1 + roi_percentage/100)) - power_apps_cost
        
        return ms_stack_cost, power_apps_cost, ms_roi, pa_roi

    ms_cost, pa_cost, ms_roi, pa_roi = calculate_costs_and_roi(
        num_users, project_months, complexity, expected_roi
    )

    with col2:
        st.subheader("ROI Analysis")
        
        # Cost metrics
        st.metric("Microsoft Stack Total Cost", f"${ms_cost:,.2f}")
        st.metric("Azure Power Apps Total Cost", f"${pa_cost:,.2f}")
        
        # ROI metrics
        st.metric("Microsoft Stack Expected ROI", f"${ms_roi:,.2f}")
        st.metric("Azure Power Apps Expected ROI", f"${pa_roi:,.2f}")

# Enhanced recommendations section
st.markdown("---")
st.header("📋 Analysis Summary & Recommendations")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### Key Findings
    
    1. 🚀 **Development Speed**
       - Azure Power Apps shows significant advantages in rapid development
       - Faster time-to-market by approximately 30%
    
    2. 💰 **Cost Structure**
       - Initial costs vary by implementation scope
       - Long-term TCO generally favors Azure Power Apps
    
    3. 📈 **Scalability**
       - Azure Power Apps provides better built-in scalability
       - Lower infrastructure management overhead
    
    4. 🛠️ **Customization**
       - Traditional Microsoft Stack offers more flexibility
       - Better suited for complex custom requirements
    """)

with col2:
    st.markdown("""
    ### Recommended Approach
    
    #### Azure Power Apps Focus:
    - Standard workflows
    - User interfaces
    - Basic business processes
    - Mobile access requirements
    - Rapid prototyping needs
    
    #### Traditional Microsoft Stack Focus:
    - Complex calculations
    - Custom integrations
    - Performance-critical operations
    - Legacy system interfaces
    - Specialized security requirements
    """)

# Add export functionality
st.markdown("---")
st.subheader("Export Options")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Export Full Report"):
        st.info("Full report export will be available in the next version")

with col2:
    if st.button("Export Comparison Data"):
        st.download_button(
            label="Download Comparison CSV",
            data=df_comparison.to_csv(index=False),
            file_name="comparison_data.csv",
            mime="text/csv"
        )

with col3:
    if st.button("Export Cost Analysis"):
        st.download_button(
            label="Download Cost Analysis CSV",
            data=df_costs.to_csv(index=False),
            file_name="cost_analysis.csv",
            mime="text/csv"
        )