# Diagnose Knowledge Check Quiz - Interactive Single Question Format

import streamlit as st

def main():
    st.set_page_config(
        page_title="Diagnose Knowledge Check",
        page_icon="🧠",
        layout="centered"
    )
    
    # Compact CSS styling
    st.markdown("""
    <style>
    .quiz-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    .question-card {
        background: #f8fafc;
        padding: 1.2rem;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .correct-feedback {
        background: #dcfce7;
        border: 1px solid #16a34a;
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
        border-left: 4px solid #16a34a;
    }
    
    .incorrect-feedback {
        background: #fee2e2;
        border: 1px solid #dc2626;
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
        border-left: 4px solid #dc2626;
    }
    
    .progress-bar {
        background: #e5e7eb;
        height: 8px;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    .progress-fill {
        background: #3b82f6;
        height: 100%;
        border-radius: 4px;
        transition: width 0.3s ease;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 1
        st.session_state.score = 0
        st.session_state.answers = {}
        st.session_state.show_feedback = False
        st.session_state.current_page = "quiz"
    
    # Page routing
    if st.session_state.current_page == "quiz":
        show_quiz_page()
    elif st.session_state.current_page == "exercise":
        show_exercise_page()

def show_quiz_page():
    # Header
    st.markdown("""
    <div class="quiz-header">
        <h3>Diagnose Step Knowledge Check</h3>
        <p>Interactive quiz on systematic AI validation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress indicator - only show for active questions
    if st.session_state.current_question <= 5:
        progress = (st.session_state.current_question - 1) / 5
        st.markdown(f"""
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress * 100}%"></div>
        </div>
        <p style="text-align: center; font-size: 0.9rem; color: #6b7280;">
            Question {st.session_state.current_question} of 5
        </p>
        """, unsafe_allow_html=True)
        
        display_current_question()
    else:
        show_final_results()

def show_exercise_page():
    # Back to quiz button
    if st.button("← Back to Quiz Results"):
        st.session_state.current_page = "quiz"
        st.rerun()
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 1.5rem; border-radius: 10px; color: white; text-align: center; margin: 1rem 0;">
        <h3>Practical Exercise: AI Customer Service Chatbot</h3>
        <p>Apply the Diagnose framework to a new scenario</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Two tabs for exercise
    exercise_tab1, exercise_tab2 = st.tabs(["📋 Scenario & Instructions", "✍️ Your Response"])
    
    with exercise_tab1:
        show_exercise_scenario()
    
    with exercise_tab2:
        show_exercise_response()

def display_current_question():
    questions = get_questions()
    current_q = st.session_state.current_question
    
    if current_q <= 5:
        question_data = questions[current_q - 1]
        
        # Question card
        st.markdown(f"""
        <div class="question-card">
            <h4>{question_data['question']}</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Answer options
        answer = st.radio(
            "Select your answer:",
            question_data['options'],
            key=f"q{current_q}_answer"
        )
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("Submit Answer", type="primary"):
                st.session_state.answers[current_q] = answer
                st.session_state.show_feedback = True
                st.rerun()
        
        # Show feedback if answer submitted
        if st.session_state.show_feedback:
            is_correct = answer == question_data['correct']
            
            if is_correct:
                st.session_state.score += 1
                st.markdown(f"""
                <div class="correct-feedback">
                    <strong>Correct! ✅</strong><br>
                    {question_data['explanation']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="incorrect-feedback">
                    <strong>Incorrect ❌</strong><br>
                    <strong>Correct answer:</strong> {question_data['correct']}<br>
                    <strong>Explanation:</strong> {question_data['explanation']}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("Next Question", type="secondary"):
                    st.session_state.current_question += 1
                    st.session_state.show_feedback = False
                    st.rerun()
    
    else:
        # Quiz completed - show results and practical exercise
        show_final_results()

def show_final_results():
    percentage = (st.session_state.score / 5) * 100
    
    st.markdown(f"""
    <div class="quiz-header">
        <h3>Quiz Complete!</h3>
        <h2>Final Score: {st.session_state.score}/5 ({percentage:.0f}%)</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if percentage >= 80:
        st.success("Excellent understanding of the Diagnose concept! You've demonstrated mastery of systematic AI validation principles.")
    elif percentage >= 60:
        st.warning("Good foundation with room for improvement. Consider reviewing the philosophical connections and practical applications.")
    else:
        st.error("Additional study recommended. Focus on understanding how philosophical principles translate into practical AI validation methods.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Restart Quiz", key="restart_quiz"):
            st.session_state.current_question = 1
            st.session_state.score = 0
            st.session_state.answers = {}
            st.session_state.show_feedback = False
            if 'show_exercise' in st.session_state:
                del st.session_state.show_exercise
            st.rerun()
    
    with col2:
        if st.button("Continue to Exercise", type="primary", key="continue_exercise"):
            st.session_state.current_page = "exercise"
            st.rerun()
    
    # Don't show exercise here anymore - it will be on separate page

def show_practical_exercise():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 1.5rem; border-radius: 10px; color: white; text-align: center; margin: 1rem 0;">
        <h3>Practical Exercise: AI Customer Service Chatbot</h3>
        <p>Apply the Diagnose framework to a new scenario</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Two tabs for exercise
    exercise_tab1, exercise_tab2 = st.tabs(["📋 Scenario & Instructions", "✍️ Your Response"])
    
    with exercise_tab1:
        show_exercise_scenario()
    
    with exercise_tab2:
        show_exercise_response()

def show_exercise_scenario():
    # Scenario card
    st.markdown("""
    <div class="question-card">
        <h4>🤖 The Scenario</h4>
        <p>Your company has deployed an AI chatbot to handle customer service inquiries. The chatbot automatically resolves simple issues and escalates complex ones to human agents. Recent customer complaints suggest the AI may be failing to escalate urgent issues appropriately.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Task description
    st.markdown("""
    <div class="question-card">
        <h4>🎯 Your Mission</h4>
        <p>Apply the Diagnose step to evaluate this AI system using the systematic validation framework you've learned.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Instructions in clean format
    st.subheader("Step-by-Step Instructions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Step 1: Define Standards**
        What should good chatbot performance look like? Consider:
        - Response accuracy
        - Escalation decisions  
        - Customer satisfaction
        
        **Step 2: Design Tests**
        Create tests for:
        - Accuracy validation
        - Human oversight points
        - Bias detection methods
        """)
    
    with col2:
        st.markdown("""
        **Step 3: Implementation Plan**
        How will you test without disrupting service?
        - Sampling strategy
        - Review process
        - Monitoring approach
        
        **Success Criteria:**
        - Clear performance standards
        - Realistic human oversight plan  
        - Addresses potential bias
        - Practical implementation
        """)

def show_exercise_response():
    st.subheader("Your Diagnostic Plan")
    
    # Response form with professional styling
    st.markdown("**Performance Standards**")
    standards = st.text_area(
        "What standards should the chatbot meet?",
        placeholder="Define accuracy, response time, escalation criteria...",
        height=100,
        key="standards"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Accuracy Testing**")
        accuracy_test = st.text_area(
            "How will you test accuracy?",
            placeholder="Describe your testing approach...",
            height=80,
            key="accuracy"
        )
    
    with col2:
        st.markdown("**Bias Detection**") 
        bias_test = st.text_area(
            "How will you check for bias?",
            placeholder="What fairness tests will you run...",
            height=80,
            key="bias"
        )
    
    st.markdown("**Human Oversight Plan**")
    human_plan = st.text_area(
        "What role should humans play in validation?",
        placeholder="When and how should humans validate AI decisions...",
        height=100,
        key="human_plan"
    )
    
    # Reflection questions
    st.subheader("Quick Reflection")
    
    col1, col2 = st.columns(2)
    
    with col1:
        reflection1 = st.text_area(
            "How did you apply systematic doubt?",
            height=60,
            key="reflection1"
        )
    
    with col2:
        reflection2 = st.text_area(
            "What could go wrong without diagnosis?",
            height=60,
            key="reflection2"
        )
    
    # Submit button
    if st.button("Submit Exercise", type="primary", use_container_width=True):
        if standards and accuracy_test and human_plan:
            st.balloons()
            st.success("Exercise completed successfully!")
            
            st.markdown("""
            <div class="correct-feedback">
                <strong>Well Done!</strong><br>
                You've successfully applied the Diagnose framework to a new scenario, demonstrating understanding of systematic validation, human oversight, and evidence-based decision making.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Please complete the main sections (Standards, Accuracy Testing, Human Oversight) before submitting.")

def get_questions():
    return [
        {
            'question': 'What is the primary purpose of the Diagnose step in the Botspeak Loop?',
            'options': [
                'A) To improve AI system speed and efficiency',
                'B) To apply systematic skepticism to AI outputs before acceptance',
                'C) To replace human decision-making with automated processes',
                'D) To reduce the cost of AI implementation'
            ],
            'correct': 'B) To apply systematic skepticism to AI outputs before acceptance',
            'explanation': 'The Diagnose step implements systematic skepticism through structured testing and validation before trusting AI outputs.'
        },
        {
            'question': 'A hospital implements AI for patient triage without validation testing. After 6 months, they discover the AI underestimates severity for elderly patients. Which philosophical principle was violated?',
            'options': [
                'A) Cartesian systematic doubt - they accepted AI claims without rigorous testing',
                'B) Humean empiricism - they assumed training performance would continue', 
                'C) Popperian falsifiability - they never tested for potential AI failures',
                'D) All of the above'
            ],
            'correct': 'D) All of the above',
            'explanation': 'All three principles were violated - no systematic testing, assumption of continued performance, and no attempt to find failure modes.'
        },
        {
            'question': 'In an AI resume screening system, human reviewers disagree with AI decisions 60% of the time. What does this suggest?',
            'options': [
                'A) The AI system is well-calibrated and ready for deployment',
                'B) Human reviewers need additional training',
                'C) The AI system requires significant improvement or increased human oversight',
                'D) The sample size is too small for meaningful analysis'
            ],
            'correct': 'C) The AI system requires significant improvement or increased human oversight',
            'explanation': '60% disagreement indicates poor AI-human alignment, suggesting the system needs improvement or cannot operate autonomously.'
        },
        {
            'question': 'Which of the following is NOT a core component of the Diagnose step?',
            'options': [
                'A) Acceptance testing against predefined criteria',
                'B) Uncertainty assessment and confidence calibration',
                'C) Automated deployment without human review',
                'D) Bias detection across demographic groups'
            ],
            'correct': 'C) Automated deployment without human review',
            'explanation': 'Automated deployment without human review contradicts the fundamental principle of systematic validation in the Diagnose step.'
        },
        {
            'question': 'An AI system shows 85% accuracy but has a bimodal score distribution (peaks at 20 and 95 points). What diagnostic concern does this raise?',
            'options': [
                'A) The system accuracy is too low for deployment',
                'B) The system may oversimplify complex decisions into binary categories',
                'C) The system is perfectly calibrated',
                'D) No concerns - high accuracy indicates good performance'
            ],
            'correct': 'B) The system may oversimplify complex decisions into binary categories',
            'explanation': 'Bimodal distribution suggests the AI polarizes decisions rather than handling nuanced cases, requiring human oversight for complex scenarios.'
        }
    ]

if __name__ == "__main__":
    main()