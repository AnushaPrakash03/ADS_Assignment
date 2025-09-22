# TechCorp Resume Screening Diagnostic System
# Real-world HR diagnostic tool for AI resume screening validation

import streamlit as st
import pandas as pd
import re
import io
from typing import Dict, List, Tuple

# Job requirements and constraints
JOB_REQUIREMENTS = {
    "data_engineer": {
        "title": "Senior Data Engineer",
        "department": "Engineering", 
        "min_experience": 3,
        "required_skills": ["python", "sql", "etl", "data pipeline", "spark", "airflow"],
        "preferred_skills": ["aws", "docker", "kubernetes", "kafka", "hadoop"],
        "education_required": ["bachelor", "master", "computer science", "engineering"]
    },
    "data_analyst": {
        "title": "Data Analyst",
        "department": "Analytics",
        "min_experience": 2, 
        "required_skills": ["sql", "excel", "tableau", "power bi", "statistics", "python"],
        "preferred_skills": ["r", "looker", "data visualization", "business intelligence"],
        "education_required": ["bachelor", "master", "statistics", "mathematics", "business"]
    }
}

def main():
    st.set_page_config(
        page_title="TechCorp HR Screening System",
        page_icon="🏢", 
        layout="wide"
    )
    
    # Professional CSS styling
    st.markdown("""
    <style>
    /* Global typography improvements */
    .main .block-container {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
        line-height: 1.6;
        color: #1f2937;
    }
    
    /* Main header styling */
    .main-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        font-size: 2.2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        font-size: 1rem;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Professional diagnostic section */
    .diagnostic-section {
        background: linear-gradient(135deg, #fef3c7, #fde68a);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #f59e0b;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .diagnostic-section h3 {
        color: #92400e;
        font-size: 1.3rem;
        font-weight: 600;
        margin-top: 0;
        margin-bottom: 0.5rem;
    }
    
    .diagnostic-section p {
        color: #78350f;
        font-size: 0.95rem;
        margin: 0;
    }
    
    /* Candidate cards with professional styling */
    .candidate-card {
        background: #ffffff;
        padding: 1.2rem;
        border-radius: 8px;
        border-left: 3px solid #3b82f6;
        margin: 0.5rem 0;
        font-size: 0.9rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid #e5e7eb;
    }
    
    /* Professional metric styling */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    div[data-testid="metric-container"] > label {
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        color: #6b7280 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    div[data-testid="metric-container"] > div {
        font-size: 1.6rem !important;
        font-weight: 600 !important;
        color: #111827 !important;
    }
    
    /* Typography hierarchy */
    h1 {
        font-size: 2rem !important;
        font-weight: 600 !important;
        color: #111827 !important;
        margin-bottom: 1rem !important;
    }
    
    h2 {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        color: #1f2937 !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }
    
    h3 {
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        color: #374151 !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.75rem !important;
    }
    
    h4 {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #4b5563 !important;
        margin-top: 1.25rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Professional text sizing */
    p, li {
        font-size: 0.9rem !important;
        line-height: 1.6 !important;
        color: #374151 !important;
    }
    
    /* Enhanced button styling */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-size: 0.9rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(59,130,246,0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8, #1e40af);
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(59,130,246,0.4);
    }
    
    /* Form element styling */
    .stCheckbox > label, .stSelectbox > label, .stSlider > label {
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        color: #374151 !important;
    }
    
    /* Small text styling */
    small {
        font-size: 0.75rem !important;
        color: #6b7280 !important;
        line-height: 1.4 !important;
    }
    
    /* Alert and info box styling */
    .stAlert {
        border-radius: 8px;
        font-size: 0.85rem !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>TechCorp HR Resume Screening System</h1>
        <p>Internal AI Diagnostic Tool for Hiring Managers</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📝 Resume Screening", 
        "🔍 AI Diagnostic Review", 
        "📊 System Analytics",
        "📋 Resources & Templates",
        "⚖️ Approach Comparison"
    ])
    
    with tab1:
        show_resume_screening()
    
    with tab2:
        show_diagnostic_review()
        
    with tab3:
        show_system_analytics()
        
    with tab4:
        show_resources_templates()
        
    with tab5:
        show_approach_comparison()

def show_resume_screening():
    st.header("Resume Screening Interface")
    st.write("*Internal tool for HR team to process incoming applications*")
    
    # Job selection
    col1, col2 = st.columns([1, 2])
    
    with col1:
        job_type = st.selectbox(
            "Select Position:",
            ["data_engineer", "data_analyst"],
            format_func=lambda x: JOB_REQUIREMENTS[x]["title"]
        )
    
    # Resume upload
    st.subheader("Process Applications")
    uploaded_files = st.file_uploader(
        "Upload candidate resumes for batch processing",
        type=['txt', 'pdf'],
        accept_multiple_files=True,
        help="Upload multiple resume files for AI screening"
    )
    
    if uploaded_files:
        st.subheader("AI Screening Results - For HR Review Only")
        
        screening_results = []
        
        for i, file in enumerate(uploaded_files):
            # Read file with encoding handling
            if file.type == "text/plain":
                try:
                    resume_text = str(file.read(), "utf-8")
                except UnicodeDecodeError:
                    file.seek(0)
                    try:
                        resume_text = str(file.read(), "latin-1")
                    except UnicodeDecodeError:
                        file.seek(0)
                        resume_text = str(file.read(), "cp1252")
            else:
                # Simulate PDF parsing
                resume_text = "Sample resume with data engineering experience, Python, SQL skills, 4 years experience..."
            
            # AI screening
            screening_result = screen_resume(resume_text, job_type)
            candidate_name = f"Candidate_{i+1}"
            
            screening_results.append({
                'name': candidate_name,
                'filename': file.name,
                'result': screening_result,
                'resume_text': resume_text[:200]
            })
            
            # Display result in HR format
            st.markdown(f"""
            <div class="candidate-card">
                <strong>{candidate_name}</strong> ({file.name})<br>
                AI Decision: <strong>{screening_result['decision']}</strong> | 
                Score: <strong>{screening_result['total_score']}/100</strong> | 
                Experience: <strong>{screening_result['experience_assessment']}</strong>
            </div>
            """, unsafe_allow_html=True)
        
        # Store for diagnostic review
        st.session_state.screening_results = screening_results
        
        # Summary metrics
        if screening_results:
            total_apps = len(screening_results)
            accepted = len([r for r in screening_results if r['result']['decision'] == 'Accept'])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Applications Processed", total_apps)
            with col2:
                st.metric("AI Recommendations", f"{accepted} Accept, {total_apps-accepted} Reject")
            with col3:
                st.metric("Acceptance Rate", f"{accepted/total_apps*100:.1f}%")
            
            st.warning("⚠️ **HR Notice**: These are AI recommendations only. Human review required before any hiring decisions.")

def show_diagnostic_review():
    st.header("AI System Diagnostic Review")
    
    if 'screening_results' not in st.session_state or not st.session_state.screening_results:
        st.info("No screening results available. Please process resumes in the Resume Screening tab first.")
        return
    
    st.markdown("""
    <div class="diagnostic-section">
        <h3>🔍 Systematic AI Validation Process</h3>
        <p>Apply diagnostic methodology to ensure AI hiring recommendations are accurate, fair, and reliable before making hiring decisions.</p>
    </div>
    """, unsafe_allow_html=True)
    
    results = st.session_state.screening_results
    
    # Diagnostic configuration
    st.markdown("### Configure Diagnostic Review")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Diagnostic Tests to Perform**")
        test_accuracy = st.checkbox("Human-AI Decision Validation", value=True, help="Compare AI decisions with human expert judgment")
        test_consistency = st.checkbox("Decision Consistency Analysis", value=True, help="Check for consistent application of criteria")
        test_bias = st.checkbox("Bias Detection Screening", value=False, help="Analyze for demographic or systemic biases")
        test_edge_cases = st.checkbox("Edge Case Performance", value=False, help="Test AI performance on unusual resumes")
    
    with col2:
        st.write("**Review Parameters**")
        reviewer_type = st.selectbox("Human Reviewer Role", ["Senior HR Manager", "Technical Hiring Manager", "Department Head"])
        review_threshold = st.slider("Human Override Threshold", 0, 100, 70, help="Score below which human review is mandatory")
        # Handle slider edge case when only one result exists
        max_sample = max(len(results), 2)
        default_sample = min(5, len(results))
        sample_size = st.slider("Sample Size for Review", 1, max_sample, default_sample)
    
    if st.button("Conduct Diagnostic Review", type="primary"):
        conduct_systematic_diagnosis(
            results[:sample_size], 
            {
                'accuracy': test_accuracy,
                'consistency': test_consistency, 
                'bias': test_bias,
                'edge_cases': test_edge_cases
            },
            reviewer_type,
            review_threshold
        )

def conduct_systematic_diagnosis(results, tests, reviewer_type, threshold):
    st.markdown("### Diagnostic Analysis Results")
    
    if tests['accuracy']:
        st.markdown("#### Human-AI Decision Validation")
        
        st.write("**Manual Review Process:**")
        st.write(f"Reviewer: {reviewer_type}")
        
        human_ai_comparison = []
        
        for i, candidate in enumerate(results):
            ai_decision = candidate['result']['decision']
            ai_score = candidate['result']['total_score']
            
            st.markdown(f"**{candidate['name']}** - AI Score: {ai_score}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**AI Recommendation:** {ai_decision}")
                st.write(f"**AI Reasoning:**")
                st.write(f"- Skills: {candidate['result']['skills_score']}/100")
                st.write(f"- Experience: {candidate['result']['experience_score']}/100") 
                st.write(f"- Education: {candidate['result']['education_score']}/100")
            
            with col2:
                human_decision = st.selectbox(
                    f"Human Decision ({reviewer_type}):",
                    ["Accept", "Reject", "Interview", "Further Review"],
                    key=f"human_{i}"
                )
                
                human_confidence = st.slider(
                    "Reviewer Confidence",
                    1, 10, 7,
                    key=f"conf_{i}"
                )
                
                human_notes = st.text_area(
                    "Review Notes:",
                    placeholder="Context, concerns, additional factors...",
                    key=f"notes_{i}",
                    height=80
                )
            
            # Store comparison
            agreement = (ai_decision.lower() == human_decision.lower())
            human_ai_comparison.append({
                'candidate': candidate['name'],
                'ai_decision': ai_decision,
                'human_decision': human_decision,
                'agreement': agreement,
                'ai_score': ai_score,
                'human_confidence': human_confidence,
                'notes': human_notes
            })
            
            if agreement:
                st.success("✅ Human-AI Agreement")
            else:
                st.warning("⚠️ Human Override Required")
                
            st.markdown("---")
        
        # Summary analysis
        if human_ai_comparison:
            agreement_rate = sum(1 for c in human_ai_comparison if c['agreement']) / len(human_ai_comparison)
            
            st.markdown("#### Human-AI Validation Summary")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Agreement Rate", f"{agreement_rate:.1%}")
            with col2:
                overrides = len([c for c in human_ai_comparison if not c['agreement']])
                st.metric("Human Overrides", overrides)
            with col3:
                avg_confidence = sum(c['human_confidence'] for c in human_ai_comparison) / len(human_ai_comparison)
                st.metric("Avg Human Confidence", f"{avg_confidence:.1f}/10")
            
            # Analysis insights
            if agreement_rate >= 0.8:
                st.success("🎯 High AI-Human Agreement: AI system appears well-calibrated")
            elif agreement_rate >= 0.6:
                st.warning("⚠️ Moderate Agreement: Some AI decisions require human correction")
            else:
                st.error("🚨 Low Agreement: AI system needs significant improvement or human oversight")
    
    if tests['consistency']:
        st.markdown("#### Decision Consistency Analysis")
        
        scores = [r['result']['total_score'] for r in results]
        score_series = pd.Series(scores)
        score_std = score_series.std()
        score_mean = score_series.mean()
        
        # Handle edge case where all scores are identical
        if pd.isna(score_std) or len(set(scores)) == 1:
            score_std = 0.0
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Score Standard Deviation", f"{score_std:.1f}")
        with col2:
            st.metric("Average Score", f"{score_mean:.1f}")
        
        # Updated logic for identical scores
        if score_std == 0:
            st.warning("⚠️ All candidates received identical scores - this may indicate system malfunction")
            st.write("**Diagnostic Alert**: Identical scoring patterns suggest the AI may not be processing resume content properly")
        elif score_std <= 20:
            st.success("✅ Consistent scoring patterns")
        else:
            st.warning("⚠️ High score variance - may indicate inconsistent criteria application")
    
    if tests['bias']:
        st.markdown("#### Bias Detection Analysis")
        
        st.info("""
        **Systematic Bias Review:**
        - Name-based discrimination analysis
        - Educational background preferences  
        - Experience pathway biases
        - Keyword dependency patterns
        
        *In production: Analyze patterns across hundreds of applications*
        """)
        
        acceptance_rate = len([r for r in results if r['result']['decision'] == 'Accept']) / len(results)
        
        if acceptance_rate < 0.05:
            st.warning("Very low acceptance rate - potential over-filtering")
        elif acceptance_rate > 0.5:
            st.warning("Very high acceptance rate - potential under-filtering")
        else:
            st.success("Reasonable acceptance rate observed")

def show_system_analytics():
    st.header("System Performance Analytics")
    
    if 'screening_results' not in st.session_state:
        st.info("No data available. Process some applications first.")
        return
    
    results = st.session_state.screening_results
    
    # Performance metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total = len(results)
        st.metric("Total Applications", total)
    
    with col2:
        accepted = len([r for r in results if r['result']['decision'] == 'Accept'])
        st.metric("AI Recommendations", f"{accepted} Accept")
    
    with col3:
        avg_score = sum(r['result']['total_score'] for r in results) / len(results)
        st.metric("Average AI Score", f"{avg_score:.1f}")
    
    with col4:
        high_confidence = len([r for r in results if r['result']['total_score'] >= 80])
        st.metric("High Confidence Cases", high_confidence)
    
    # Score distribution
    st.subheader("AI Score Distribution")
    scores = [r['result']['total_score'] for r in results]
    score_df = pd.DataFrame({'scores': scores})
    
    import plotly.express as px
    fig = px.histogram(score_df, x='scores', nbins=10, title="Distribution of AI Screening Scores")
    st.plotly_chart(fig, width="stretch")
    
    st.subheader("Key Insights")
    st.info("""
    **System Diagnostics Summary:**
    - This tool demonstrates how HR teams should validate AI hiring systems
    - Human review remains essential for fair and accurate hiring decisions
    - Systematic diagnosis prevents biased or inaccurate AI recommendations from affecting candidates
    - The diagnostic process ensures responsible AI deployment in human-centered applications
    """)

def show_resources_templates():
    st.header("Diagnostic Resources & Templates")
    st.write("Downloadable templates and frameworks for AI system validation")
    
    # Diagnostic Checklist
    st.markdown("#### 1. AI Diagnostic Checklist")
    
    checklist_content = """# AI Resume Screening Diagnostic Checklist

## Pre-Diagnostic Setup
- [ ] Define clear acceptance criteria and thresholds
- [ ] Identify stakeholders and decision makers  
- [ ] Establish time constraints and resource limits
- [ ] Set up documentation and audit trail systems

## Risk Stratification Process
- [ ] Categorize applications by risk level
- [ ] Calculate required sample sizes for statistical confidence
- [ ] Assign appropriate review resources to each category

## Acceptance Testing Protocol
- [ ] Run AI system against validation dataset
- [ ] Compare AI decisions to ground truth outcomes
- [ ] Calculate accuracy, precision, recall metrics
- [ ] Verify performance meets minimum thresholds

## Human Validation Process
- [ ] Select representative sample for human review
- [ ] Assign qualified reviewers
- [ ] Conduct blind review of AI recommendations
- [ ] Record human decisions and confidence levels
- [ ] Calculate human-AI agreement rates

## Bias Detection Analysis
- [ ] Analyze acceptance rates across demographic groups
- [ ] Test for statistical significance of differences
- [ ] Review for systematic biases
- [ ] Document any bias patterns discovered

## Final Decision and Documentation
- [ ] Compile diagnostic findings into summary report
- [ ] Make go/no-go decision on AI system deployment
- [ ] Document all overrides and justifications
- [ ] Create monitoring plan for ongoing validation"""
    
    st.download_button(
        label="Download Diagnostic Checklist",
        data=checklist_content,
        file_name="ai_diagnostic_checklist.md",
        mime="text/markdown"
    )
    
    with st.expander("Preview Diagnostic Checklist"):
        st.markdown(checklist_content)
    
    # Human Override Template
    st.markdown("#### 2. Human Override Documentation Template")
    
    override_template = """# Human Override Documentation Form

**Application Details**
- Candidate ID: _______________
- Position: ___________________
- AI Decision: ________________
- AI Score: ___________________
- Human Reviewer: ____________

**Override Decision**
- Human Decision: [ ] Accept [ ] Reject [ ] Interview [ ] Further Review
- Reviewer Confidence (1-10): _______

**Justification**
- Primary reason for override: _________________________________
- Additional factors considered: ______________________________
- Potential AI system limitations identified: ___________________

**Follow-up Actions**
- [ ] Flag for system improvement
- [ ] Include in bias analysis  
- [ ] Update training data
- [ ] Escalate to senior review"""
    
    st.download_button(
        label="Download Override Template",
        data=override_template,
        file_name="human_override_template.md",
        mime="text/markdown"
    )
    
    # Risk Assessment Framework
    st.markdown("#### 3. Risk Assessment Framework")
    
    risk_framework = """# Risk Assessment Framework for AI Resume Screening

## Application Classification Criteria

### High-Risk (100% Human Review)
- AI scores between 65-75 points
- Applications from protected demographic groups
- Executive or senior-level positions  
- Applications with unusual backgrounds or career gaps
- Any technical errors or incomplete AI processing

### Medium-Risk (Statistical Sampling)
- AI scores between 40-65 or 75-85 points
- Standard professional backgrounds
- Mid-level positions
- Complete AI processing with normal confidence levels

### Low-Risk (Automated with Monitoring)
- AI scores below 40 or above 85 points
- Clear qualification matches or mismatches
- Standard entry to mid-level positions
- High AI processing confidence

## Resource Allocation Guidelines
- High-risk: Immediate manual review by senior staff
- Medium-risk: Sample-based review using statistical methods  
- Low-risk: Automated processing with pattern monitoring
- Alert triggers: Unusual acceptance rates, score clustering, demographic disparities

## Statistical Sampling Calculator
- Population size (total applications): N = ______
- Desired confidence level: [ ] 90% [ ] 95% [ ] 99%
- Margin of error: [ ] ±3% [ ] ±5% [ ] ±10%
- Required sample size: n = (Z² × p × (1-p)) / E²"""
    
    st.download_button(
        label="Download Risk Framework",
        data=risk_framework,
        file_name="risk_assessment_framework.md", 
        mime="text/markdown"
    )
    
    with st.expander("Preview Risk Assessment Framework"):
        st.markdown(risk_framework)
    
    # Generic AI Diagnostic Framework
    st.markdown("#### 4. Generic AI Diagnostic Framework")
    
    generic_framework = """# Reusable AI Diagnostic Framework

This framework can be adapted for any AI decision-making system requiring validation.

## Step 1: System Definition
- Define AI system purpose and scope
- Identify decision stakeholders and affected parties
- Establish success criteria and risk tolerance  
- Document regulatory and ethical requirements

## Step 2: Risk Stratification
- Categorize decisions by impact and uncertainty
- Allocate human oversight resources appropriately
- Design sampling strategies for validation
- Set up monitoring for automated decisions

## Step 3: Diagnostic Testing
- **Acceptance testing**: Verify basic performance requirements
- **Calibration checks**: Ensure confidence scores match accuracy
- **Bias detection**: Analyze fairness across relevant groups
- **Edge case testing**: Identify system limitations

## Step 4: Human Integration  
- Design human oversight workflows
- Train reviewers on diagnostic procedures
- Establish override protocols and documentation
- Create feedback loops for system improvement

## Step 5: Ongoing Monitoring
- Implement automated performance tracking
- Schedule regular diagnostic reviews
- Monitor for distribution drift and bias emergence
- Plan for model updates and retraining

## Customization Guidelines
- Adapt risk categories to your specific domain
- Modify diagnostic tests based on system requirements
- Adjust sampling methods for your scale and resources
- Customize documentation for regulatory compliance

## Application Areas
- Healthcare AI diagnostics
- Financial decision systems
- Educational assessment tools
- Content moderation systems
- Autonomous vehicle systems
- Any AI system affecting human decisions"""
    
    st.download_button(
        label="Download Generic Framework",
        data=generic_framework,
        file_name="generic_ai_diagnostic_framework.md",
        mime="text/markdown"
    )
    
    with st.expander("Preview Generic AI Framework"):
        st.markdown(generic_framework)

def show_approach_comparison():
    st.header("Why Systematic Diagnosis Matters")
    st.write("A visual comparison of two different approaches to AI deployment")
    
    # Create tabs for different comparison views
    comparison_tab1, comparison_tab2, comparison_tab3 = st.tabs([
        "📈 Outcomes Comparison", 
        "⏱️ Timeline Comparison", 
        "💡 Key Takeaways"
    ])
    
    with comparison_tab1:
        st.markdown("#### What Happens With Each Approach")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="background: #fee2e2; padding: 1.2rem; border-radius: 10px; border-left: 5px solid #dc2626; margin-bottom: 1rem;">
                <h4 style="color: #dc2626; margin-top: 0; font-size: 1rem; font-weight: 600;">❌ Without Diagnosis</h4>
                <p style="font-size: 0.8rem; margin-bottom: 0; color: #7f1d1d;">Deploy AI directly to make hiring decisions</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Metrics cards
            col1a, col1b = st.columns(2)
            with col1a:
                st.metric("Legal Cost", "$2M", delta="Settlement")
                st.metric("Time to Failure", "12 months", delta="Complete shutdown")
            with col1b:
                st.metric("Reputation Impact", "Severe", delta="Media crisis")  
                st.metric("Regulatory Status", "Under Investigation", delta="Sanctions")
            
            st.markdown('<div style="margin-top: 1rem;">', unsafe_allow_html=True)
            st.error("**What Goes Wrong:**")
            st.markdown("""
            <ul style="font-size: 0.8rem; margin: 0.5rem 0; padding-left: 1rem; color: #374151;">
                <li>Hidden bias affects real candidates</li>
                <li>Legal complaints pile up</li>
                <li>Media exposes discrimination</li>
                <li>System must be shut down</li>
            </ul>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: #dcfce7; padding: 1.2rem; border-radius: 10px; border-left: 5px solid #16a34a; margin-bottom: 1rem;">
                <h4 style="color: #16a34a; margin-top: 0; font-size: 1rem; font-weight: 600;">✅ With Systematic Diagnosis</h4>
                <p style="font-size: 0.8rem; margin-bottom: 0; color: #14532d;">Validate AI before making any decisions</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Metrics cards
            col2a, col2b = st.columns(2)
            with col2a:
                st.metric("Legal Protection", "Strong", delta="Proactive compliance")
                st.metric("System Reliability", "High", delta="Continuous improvement")
            with col2b:
                st.metric("Candidate Trust", "High", delta="Fair process")
                st.metric("Regulatory Status", "Compliant", delta="Transparent audit trails")
            
            st.markdown('<div style="margin-top: 1rem;">', unsafe_allow_html=True)
            st.success("**What Works Well:**")
            st.markdown("""
            <ul style="font-size: 0.8rem; margin: 0.5rem 0; padding-left: 1rem; color: #374151;">
                <li>Bias caught before harm occurs</li>
                <li>Legal compliance demonstrated</li>
                <li>Quality hiring maintained</li>
                <li>System improves over time</li>
            </ul>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with comparison_tab2:
        st.markdown("#### 12-Month Timeline Comparison")
        
        # Timeline visualization with professional styling
        timeline_data = {
            'Month': [1, 3, 6, 9, 12],
            'Without Diagnosis': [
                'System launched', 
                'Problems hidden', 
                'Lawsuits filed',
                'Media investigation',
                '$2M settlement'
            ],
            'With Diagnosis': [
                'Testing phase',
                'Bias detected & fixed',
                'Safe deployment', 
                'Continuous monitoring',
                'Successful operation'
            ]
        }
        
        import plotly.graph_objects as go
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=timeline_data['Month'],
            y=[1]*5,
            mode='markers+text',
            name='Without Diagnosis',
            text=timeline_data['Without Diagnosis'],
            textposition="top center",
            marker=dict(size=10, color='#dc2626'),
            textfont=dict(color='#dc2626', size=9)
        ))
        
        fig.add_trace(go.Scatter(
            x=timeline_data['Month'],
            y=[2]*5,
            mode='markers+text', 
            name='With Diagnosis',
            text=timeline_data['With Diagnosis'],
            textposition="bottom center",
            marker=dict(size=10, color='#16a34a'),
            textfont=dict(color='#16a34a', size=9)
        ))
        
        fig.update_layout(
            title=dict(text="Timeline: Two Different Approaches", font=dict(size=14)),
            xaxis_title="Months After Implementation",
            yaxis=dict(showticklabels=False, range=[0.5, 2.5]),
            height=300,
            showlegend=True,
            font=dict(size=11)
        )
        
        st.plotly_chart(fig, width="stretch")
        
        # Professional comparison table
        st.markdown("#### Side-by-Side Results")
        
        results_data = {
            'Outcome Area': ['Legal Risk', 'Candidate Impact', 'Business Result', 'Time Investment'],
            'Without Diagnosis': ['$2M lawsuit', 'Discrimination', 'System shutdown', '0 months prep'],
            'With Diagnosis': ['Protected', 'Fair treatment', 'Continuous success', '2 months prep']
        }
        
        results_df = pd.DataFrame(results_data)
        st.dataframe(results_df, hide_index=True, width="stretch")
    
    with comparison_tab3:
        st.markdown("#### Key Learning Points")
        
        # Three professional insight cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background: #fef3c7; padding: 1rem; border-radius: 8px; text-align: center; height: 160px; border: 1px solid #fde047;">
                <h5 style="color: #92400e; margin-top: 0; font-size: 0.9rem; font-weight: 600;">🏛️ Philosophical Foundation</h5>
                <p style="font-size: 0.75rem; margin: 0.3rem 0; color: #78350f;"><strong>Cartesian Doubt:</strong> Question AI claims systematically</p>
                <p style="font-size: 0.75rem; margin: 0.3rem 0; color: #78350f;"><strong>Humean Skepticism:</strong> Don't assume past performance continues</p>
                <p style="font-size: 0.75rem; margin: 0.3rem 0; color: #78350f;"><strong>Popperian Testing:</strong> Actively seek system failures</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: #dbeafe; padding: 1rem; border-radius: 8px; text-align: center; height: 160px; border: 1px solid #93c5fd;">
                <h5 style="color: #1d4ed8; margin-top: 0; font-size: 0.9rem; font-weight: 600;">💰 Business Impact</h5>
                <p style="font-size: 0.75rem; margin: 0.3rem 0; color: #1e40af;"><strong>Cost of Failure:</strong> $2M+ in legal settlements</p>
                <p style="font-size: 0.75rem; margin: 0.3rem 0; color: #1e40af;"><strong>Cost of Prevention:</strong> 2 months of validation work</p>
                <p style="font-size: 0.75rem; margin: 0.3rem 0; color: #1e40af;"><strong>ROI:</strong> Massive savings through prevention</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: #f3e8ff; padding: 1rem; border-radius: 8px; text-align: center; height: 160px; border: 1px solid #c084fc;">
                <h5 style="color: #7c3aed; margin-top: 0; font-size: 0.9rem; font-weight: 600;">👥 Human Impact</h5>
                <p style="font-size: 0.75rem; margin: 0.3rem 0; color: #6d28d9;"><strong>Without Diagnosis:</strong> Real people face discrimination</p>
                <p style="font-size: 0.75rem; margin: 0.3rem 0; color: #6d28d9;"><strong>With Diagnosis:</strong> Fair treatment for all candidates</p>
                <p style="font-size: 0.75rem; margin: 0.3rem 0; color: #6d28d9;"><strong>Benefit:</strong> Trust and fairness maintained</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Professional final insight
        st.markdown("""
        <div style="background: #f0f9ff; padding: 1.2rem; border-radius: 10px; border-left: 4px solid #0ea5e9; margin: 1rem 0;">
            <h5 style="color: #0c4a6e; margin-top: 0; font-size: 0.95rem; font-weight: 600;">💡 The Bottom Line</h5>
            <p style="font-size: 0.85rem; color: #0c4a6e; margin: 0; line-height: 1.5;">
                Systematic diagnosis isn't just good practice—it's essential protection for both people and organizations. 
                The small upfront investment in validation prevents catastrophic failures that can destroy trust, 
                cost millions, and harm real people.
            </p>
        </div>
        """, unsafe_allow_html=True)

def screen_resume(resume_text: str, job_type: str) -> Dict:
    """Simulate AI resume screening"""
    
    requirements = JOB_REQUIREMENTS[job_type]
    resume_lower = resume_text.lower()
    
    # Skills analysis
    found_required = [skill for skill in requirements['required_skills'] if skill.lower() in resume_lower]
    found_preferred = [skill for skill in requirements['preferred_skills'] if skill.lower() in resume_lower]
    
    # Experience extraction
    experience_years = extract_experience(resume_text)
    experience_score = min(experience_years / requirements['min_experience'] * 100, 100)
    
    # Skills scoring
    required_match = len(found_required) / len(requirements['required_skills'])
    preferred_match = len(found_preferred) / len(requirements['preferred_skills']) 
    skills_score = (required_match * 70 + preferred_match * 30)
    
    # Education assessment
    education_score = 50
    for edu in requirements['education_required']:
        if edu.lower() in resume_lower:
            education_score = 100
            break
    
    # Final calculation
    total_score = int((skills_score * 0.5 + experience_score * 0.3 + education_score * 0.2))
    decision = 'Accept' if total_score >= 70 else 'Reject'
    
    return {
        'decision': decision,
        'total_score': total_score,
        'skills_score': int(skills_score),
        'experience_score': int(experience_score),
        'education_score': int(education_score),
        'found_skills': found_required + found_preferred,
        'experience_assessment': f"{experience_years} years"
    }

def extract_experience(resume_text: str) -> int:
    """Extract years of experience"""
    patterns = [
        r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
        r'experience.*?(\d+)\+?\s*years?'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, resume_text.lower())
        if matches:
            return max([int(match) for match in matches])
    
    # Estimate from keywords
    if any(word in resume_text.lower() for word in ['senior', 'lead']):
        return 5
    elif any(word in resume_text.lower() for word in ['junior', 'entry']):
        return 1
    return 2

if __name__ == "__main__":
    main()