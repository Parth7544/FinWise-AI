

import streamlit as st
import os
st.set_page_config(
    page_title="FinWise AI",
    page_icon="💰",
    layout="wide"
)
def load_css():
    css_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "assets",
        "style.css"
    )

    with open(css_path, "r", encoding="utf-8") as css_file:
        st.markdown(
            f"<style>{css_file.read()}</style>",
            unsafe_allow_html=True
        )

load_css()
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv
from google import genai
from rag_engine import create_vector_store, retrieve_relevant_documents
from finance_tools import run_finance_agent
# Load API key
load_dotenv(r"C:\Users\User\FinWise-AI\.env")
api_key = os.getenv("GEMINI_API_KEY")

st.title("💰 FinWise AI")
st.caption("Your Personal Finance Intelligence Dashboard")

# Initialize Gemini
if not api_key:
    st.error("Gemini API key not found. Check your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)
# Load and cache the RAG knowledge base
@st.cache_resource
def get_rag_resources():
    return create_vector_store()

# Load transactions
import os

transactions_file = "data/transactions.csv"

if not os.path.exists(transactions_file):
    transactions_file = "data/transactions_sample.csv"

df = pd.read_csv(transactions_file)
df["Date"] = pd.to_datetime(df["Date"])

income = df[df["Type"] == "Income"]["Amount"].sum()
expenses = df[df["Type"] == "Expense"]["Amount"].sum()
savings = income - expenses
savings_rate = (savings / income * 100) if income else 0

expense_df = df[df["Type"] == "Expense"]
category_data = expense_df.groupby("Category")["Amount"].sum()

# Navigation

page = st.sidebar.radio(
    "Navigation",
["Dashboard", "Transactions", "Expense Analysis", "AI Assistant", "Budget Planner", "Monthly Comparison", "Expense Forecasting", "Financial Goals", "Debt Repayment", "Loan EMI", "Credit Score", "Investment Calculator", "SIP Calculator", "Net Worth", "FD Calculator", "RD Calculator"]
)

if page == "Dashboard":
    st.title("💰 FinWise AI Dashboard")

    st.markdown(
    "### Your Personal Financial Overview"
)

    st.caption(
    "Track your income, expenses, savings, and financial health in one place."
)

    st.divider()
    from spending_behavior import analyze_spending_behavior
    from savings_analyzer import analyze_savings_rate
    from financial_risk import analyze_financial_risk
    from emergency_fund import analyze_emergency_fund
    st.subheader("📊 Financial Summary")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "💵 Total Income",
        f"₹{income:,.0f}"
    )

    c2.metric(
        "💸 Total Expenses",
        f"₹{expenses:,.0f}"
    )

    c3.metric(
        "💰 Total Savings",
        f"₹{savings:,.0f}"
    )

    c4.metric(
        "📈 Savings Rate",
        f"{savings_rate:.2f}%"
    )

    st.divider()

    from financial_health import calculate_financial_health

    health_result = calculate_financial_health(
        income,
        expenses,
        savings,
        None
    )

    st.subheader("❤️ Financial Health Score")

    st.metric(
        "Your Financial Health",
        f"{health_result['score']}/100",
        health_result["rating"]
    )

    st.progress(health_result["score"] / 100)
    st.write(
        f"Your savings rate: {health_result['savings_rate']}%"
    )

    st.divider()
    st.subheader("📊 Spending Behavior Analysis")

    spending_result = analyze_spending_behavior(
        income,
        expenses
    )

    st.metric(
        "Expense-to-Income Ratio",
        f"{spending_result['expense_ratio']}%"
    )

    st.write(
        f"Spending Behavior: **{spending_result['behavior']}**"
    )

    st.info(spending_result["recommendation"])
    if st.button("🤖 Generate AI Spending Insights"):

        spending_prompt = f"""
        You are FinWise AI, a personal finance assistant.

        Financial Information:
        Income: ₹{income}
        Expenses: ₹{expenses}
        Savings: ₹{savings}
        Expense Ratio: {spending_result['expense_ratio']}%
        Spending Behavior: {spending_result['behavior']}

        Analyze the user's spending habits.

        Provide:
        1. Spending behavior analysis.
        2. Areas where expenses can be reduced.
        3. Practical saving recommendations.
        4. Three actionable financial improvement tips.

        Use simple language and realistic suggestions.
        Do not invent financial information.
        """

        with st.spinner("Analyzing your spending habits..."):

            try:
                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=spending_prompt
                )

                st.markdown(response.text)

            except Exception as e:
                st.error(f"AI Spending Insights error: {e}")
    st.divider()
    st.subheader("💰 Savings Rate Analysis")

    savings_result = analyze_savings_rate(
        income,
        savings
    )

    st.metric(
        "Savings Rate",
        f"{savings_result['savings_rate']}%",
        savings_result["rating"]
    )

    st.info(savings_result["recommendation"])
    st.divider()
    st.subheader("⚠️ Financial Risk Analysis")

    risk_result = analyze_financial_risk(
        income,
        expenses,
        savings
    )

    st.metric(
        "Financial Risk Level",
        risk_result["risk_level"]
    )

    st.write(
        f"Expense Ratio: {risk_result['expense_ratio']}%"
    )

    st.write(
        f"Savings Ratio: {risk_result['savings_ratio']}%"
    )

    st.write("Recommendations:")

    for recommendation in risk_result["recommendations"]:
        st.info(recommendation)
    st.divider()
    st.subheader("🛡️ Emergency Fund Analyzer")

    emergency_monthly_expenses = st.number_input(
        "Your Essential Monthly Expenses (₹)",
        min_value=1,
        value=10000,
        key="emergency_monthly_expenses"
    )

    emergency_current_fund = st.number_input(
        "Your Current Emergency Fund (₹)",
        min_value=0,
        value=30000,
        key="emergency_current_fund"
    )

    if st.button("Analyze Emergency Fund"):

        emergency_result = analyze_emergency_fund(
            emergency_monthly_expenses,
            emergency_current_fund
        )

        st.metric(
            "Months of Expenses Covered",
            f"{emergency_result['months_covered']} months"
        )

        st.metric(
            "Minimum Emergency Fund",
            f"₹{emergency_result['minimum_target']:,.0f}"
        )

        st.metric(
            "Recommended Emergency Fund",
            f"₹{emergency_result['recommended_target']:,.0f}"
        )

        st.success(
            f"Emergency Fund Status: {emergency_result['status']}"
        )  
    st.subheader("🤖 AI Financial Health Recommendations")

    if st.button("Generate Health Recommendations"):

        health_prompt = f"""
        You are FinWise AI, a personal finance assistant.

        Financial Health Score: {health_result['score']}/100
        Financial Rating: {health_result['rating']}
        Income: ₹{income}
        Expenses: ₹{expenses}
        Savings: ₹{savings}
        Savings Rate: {health_result['savings_rate']}%

        Provide:
        1. An explanation of the financial health score.
        2. Three practical ways to improve financial health.
        3. One realistic monthly savings target.

        Use simple language. Do not invent financial data.
        """

        with st.spinner("Analyzing financial health..."):
            try:
                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=health_prompt
                )
                st.markdown(response.text)
            except Exception as e:
                st.error(f"AI recommendation error: {e}")
    st.subheader("📊 Expense Distribution by Category")

    fig = px.pie(
        values=category_data.values,
        names=category_data.index,
        hole=0.5,
        title="Where Your Money Goes",
        template="plotly_dark"
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hole=0.5
    )

    fig.update_layout(
        title_x=0.5,
        title_font_size=20,
        legend_title="Expense Categories",
        margin=dict(t=60, b=20, l=20, r=20)
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()
elif page == "Transactions":
    st.header("Transaction History")
    st.dataframe(df, use_container_width=True)

elif page == "Expense Analysis":
    from expense_anomaly import detect_expense_anomalies
    from recurring_expenses import detect_recurring_expenses
    st.header("Expense Analysis")

    fig = px.bar(
        x=category_data.index,
        y=category_data.values,
        labels={"x": "Category", "y": "Amount"},
        title="Category-wise Expenses"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.divider()
    st.subheader("🚨 Unusual Expense Detection")

    if st.button("Detect Unusual Expenses"):

        anomalies = detect_expense_anomalies(df)

        if not anomalies.empty:

            st.warning("Unusual expenses detected!")

            st.dataframe(
                anomalies,
                use_container_width=True
            )

        else:
            st.success("No unusual expenses detected!")
    st.divider()
    st.subheader("🔁 Recurring Expense Detection")

    if st.button("Find Recurring Expenses"):

        recurring = detect_recurring_expenses(df)

        if not recurring.empty:

            st.success("Recurring expenses found!")

            st.dataframe(
                recurring,
                use_container_width=True
            )

        else:
            st.info("No recurring expenses found.")

elif page == "AI Assistant":
    st.header("🤖 Chat with FinWise AI")
    st.write("Ask questions about your finances.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask FinWise AI a question...")

    if question:
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)
        # Retrieve relevant information from the knowledge base
        rag_model, rag_index, rag_chunks = get_rag_resources()

        retrieved_docs = retrieve_relevant_documents(
            question,
            rag_model,
            rag_index,
            rag_chunks,
            top_k=3
        )

        rag_context = "\n\n".join(
            [
                f"Source: {doc['source']}\n{doc['content']}"
                for doc in retrieved_docs
            ]
        )
        
        
        financial_context = f"""
        Total Income: ₹{income}
        Total Expenses: ₹{expenses}
        Total Savings: ₹{savings}
        Savings Rate: {savings_rate:.2f}%

        Expense Categories:
        {category_data.to_dict()}
        """

        prompt = f"""
        You are FinWise AI, a helpful personal finance assistant.

        Financial information:
        {financial_context}

        Retrieved knowledge-base information:
        {rag_context}

        User question:
        {question}

        Instructions:
        1. Answer in simple language.
        2. Use the user's financial data when relevant.
        3. Use retrieved knowledge-base information when relevant.
        4. Do not invent financial information.
        5. If the knowledge base does not contain the required information,
           clearly say so instead of pretending it does.
        6. Mention the knowledge-base source filenames when you use them.
        """

        try:
            with st.chat_message("assistant"):
                with st.spinner("FinWise AI is thinking..."):
                    answer = run_finance_agent(
                        client,
                        prompt
                    )                   
                    st.markdown(answer)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as e:
            st.error(f"AI Assistant error: {e}")

elif page == "Budget Planner":
    from budget_planner import create_budget_analysis

    st.header("💰 Monthly Budget Planner")
    st.write("Compare your spending with your planned budget.")

    monthly_budget = {
        "Food": 5000,
        "Shopping": 4000,
        "Bills": 2500,
        "Transport": 2000
    }

    available_months = sorted(
        df["Date"].dt.to_period("M").astype(str).unique(),
        reverse=True
    )

    selected_month = st.selectbox(
        "Select Month",
        available_months
    )

    monthly_df = df[
        df["Date"].dt.to_period("M").astype(str) == selected_month
    ]

    budget_result = create_budget_analysis(
        monthly_df,
        monthly_budget
    )

    st.dataframe(budget_result, use_container_width=True)

    st.subheader("🚨 Budget Alerts")

    over_budget = budget_result[
        budget_result["Status"] == "Over Budget"
    ]

    if not over_budget.empty:
        for _, row in over_budget.iterrows():
            st.error(
                f"{row['Category']}: Over budget by ₹{abs(row['Remaining']):,.0f}"
            )
    else:
        st.success("Great! You are within all your planned budgets.")
   


    st.subheader("🤖 AI Budget Recommendations")

    if st.button("Generate Budget Recommendations"):

        budget_prompt = f"""
        You are FinWise AI, a personal finance assistant.

        Selected month: {selected_month}

        Budget analysis:
        {budget_result.to_string(index=False)}

        Analyze the user's spending.

        Provide:
        1. Categories with high spending.
        2. Areas where expenses can be reduced.
        3. Three practical savings recommendations.

        Use simple language and do not invent information.
        """

        with st.spinner("FinWise AI is analyzing your budget..."):
            try:
                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=budget_prompt
                )
                st.markdown(response.text)
            except Exception as e:
                st.error(f"AI recommendation error: {e}")

    st.subheader("Budget Remaining")

    st.bar_chart(
        budget_result.set_index("Category")["Remaining"]
    )

elif page == "Monthly Comparison":

    from monthly_comparison import compare_monthly_expenses

    st.header("📊 Monthly Expense Comparison")
    st.write("Compare your expenses across two different months.")

    available_months = sorted(
        df["Date"].dt.to_period("M").astype(str).unique()
    )

    if len(available_months) >= 2:

        month1 = st.selectbox("Select First Month", available_months, index=0)
        month2 = st.selectbox("Select Second Month", available_months, index=1)

        comparison_result = compare_monthly_expenses(
            df, month1, month2
        )

        st.subheader("Expense Comparison")
        st.dataframe(comparison_result, use_container_width=True)
        st.subheader("🤖 AI Monthly Insights")
        
        if st.button("Generate Monthly Insights"):

            comparison_prompt = f"""
            You are FinWise AI, a personal finance assistant.

            First month: {month1}
            Second month: {month2}

            Monthly expense comparison:
            {comparison_result.to_string(index=False)}

            Analyze the comparison and explain:
            1. Which categories increased the most.
            2. Which categories decreased.
            3. Important spending patterns.
            4. Three practical ways to save money.

            Use simple language.
            Do not invent information.
            """

            with st.spinner("Analyzing monthly expenses..."):
                try:
                    response = client.models.generate_content(
                        model="gemini-3.5-flash-lite",
                        contents=comparison_prompt
                    )

                    st.markdown(response.text)

                except Exception as e:
                    st.error(f"AI insights error: {e}")

      
        

    else:
        st.warning("At least two months of data are required.")


elif page == "Expense Forecasting":

    from expense_forecasting import forecast_monthly_expenses

    st.header("🔮 Expense Forecasting")
    st.write("Estimate next month's expenses using historical spending.")

    forecast_result = forecast_monthly_expenses(df)

    st.subheader("Predicted Monthly Expenses")

    st.dataframe(forecast_result, use_container_width=True)

    total_forecast = forecast_result["Predicted Expenses"].sum()

    st.metric(
        "Estimated Total Monthly Expenses",
        f"₹{total_forecast:,.2f}"
    )

    st.subheader("Expense Forecast Chart")

    st.bar_chart(
        forecast_result.set_index("Category")["Predicted Expenses"]
    )
    st.subheader("🤖 AI Forecast Insights")

    if st.button("Generate Forecast Insights"):

        forecast_prompt = f"""
        You are FinWise AI, a personal finance assistant.

        Predicted monthly expenses:
        {forecast_result.to_string(index=False)}

        Total predicted expenses:
        ₹{total_forecast:,.2f}

        Analyze this forecast and provide:
        1. The highest predicted expense category.
        2. Categories where spending can be reduced.
        3. Three practical savings recommendations.
        4. A short conclusion about the forecast.

        Use simple language.
        Do not invent financial information.
        """

        with st.spinner("FinWise AI is analyzing your forecast..."):

            try:
                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=forecast_prompt
                )

                st.markdown(response.text)

            except Exception as e:
                st.error(f"AI forecast error: {e}")

elif page == "Financial Goals":
    from financial_goals import calculate_goal_progress
    from goal_storage import save_goals, load_goals
    from goal_priority import analyze_goal_priority
    from savings_planner import calculate_monthly_savings
    from goal_timeline import calculate_goal_timeline
    from goal_milestones import calculate_goal_milestones

    st.header("🎯 Financial Goals Tracker")
    st.write("Create and track multiple savings goals.")

    if "financial_goals" not in st.session_state:
        st.session_state.financial_goals = load_goals()

    goal_name = st.text_input(
        "Goal Name",
        placeholder="Example: Emergency Fund"
    )

    goal_amount = st.number_input(
        "Target Amount (₹)",
        min_value=1,
        value=50000
    )

    current_savings = st.number_input(
        "Current Savings (₹)",
        min_value=0,
        value=0
    )

    if st.button("Add Savings Goal"):
        if goal_name.strip():
            st.session_state.financial_goals.append({
                "name": goal_name,
                "target": goal_amount,
                "saved": current_savings
            })

            save_goals(st.session_state.financial_goals)

            st.success("Savings goal saved permanently!")
        else:
            st.warning("Please enter a goal name.")

    st.divider()
    st.subheader("📊 Goals Summary")

    total_goals = len(st.session_state.financial_goals)

    total_target = sum(
        goal["target"]
        for goal in st.session_state.financial_goals
    )

    total_saved = sum(
        goal["saved"]
        for goal in st.session_state.financial_goals
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Active Goals", total_goals)

    col2.metric(
        "Total Target",
        f"₹{total_target:,.0f}"
    )

    col3.metric(
        "Total Saved",
        f"₹{total_saved:,.0f}"
    )

    st.divider()   
    st.subheader("Your Savings Goals")
    st.subheader("📈 Overall Savings Progress")

    if total_target > 0:

        remaining_amount = max(total_target - total_saved, 0)

        overall_progress = min(
            (total_saved / total_target) * 100,
            100
        )

        progress_data = pd.DataFrame({
            "Status": ["Saved", "Remaining"],
            "Amount": [min(total_saved, total_target), remaining_amount]
        })

        fig = px.pie(
            progress_data,
            values="Amount",
            names="Status",
            hole=0.5,
            title=f"Overall Goal Completion: {overall_progress:.1f}%"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.progress(overall_progress / 100)

    else:
        st.info("Add a savings goal to view overall progress.")
    for goal in st.session_state.financial_goals:
        result = calculate_goal_progress(
            goal["target"],
            goal["saved"]
        )

        st.write(f"### {goal['name']}")
        st.progress(result["progress"] / 100)
        st.write(f"Progress: {result['progress']}%")
        st.write(f"Target: ₹{goal['target']:,.0f}")
        st.write(f"Saved: ₹{goal['saved']:,.0f}")
        st.write(f"Remaining: ₹{result['remaining']:,.0f}")
        st.write(f"Status: {result['status']}")
        milestones = calculate_goal_milestones(
            goal["target"],
            goal["saved"]
        )

        st.write("🏆 Goal Milestones")

        for milestone in milestones:

            if milestone["achieved"]:
                st.success(
                    f"{milestone['milestone']}% Milestone Achieved"
                )
            else:
                st.info(
                    f"{milestone['milestone']}% Milestone - "
                    f"₹{milestone['required_amount']:,.0f} required"
                )
        st.divider()

    st.subheader("✏️ Update Existing Goal")

    if st.session_state.financial_goals:

        goal_names = [
            goal["name"]
            for goal in st.session_state.financial_goals
        ]

        selected_goal = st.selectbox(
            "Select Goal",
            goal_names
        )

        selected_index = goal_names.index(selected_goal)

        updated_savings = st.number_input(
            "Updated Savings Amount (₹)",
            min_value=0,
            value=int(
                st.session_state.financial_goals[selected_index]["saved"]
            ),
            key="updated_savings_input"
        )

        if st.button("Update Savings"):

            st.session_state.financial_goals[selected_index]["saved"] = updated_savings

            save_goals(st.session_state.financial_goals)

            st.success("Savings updated successfully!")

            st.rerun()

    else:
        st.info("Add a savings goal first.")


    st.divider()
    st.subheader("🗑️ Delete Savings Goal")

    if st.session_state.financial_goals:

        delete_goal = st.selectbox(
            "Select goal to delete",
            [
                goal["name"]
                for goal in st.session_state.financial_goals
            ],
            key="delete_goal_select"
        )

        if st.button("Delete Goal"):
            st.session_state.financial_goals = [
                goal
                for goal in st.session_state.financial_goals
                if goal["name"] != delete_goal
            ]

            save_goals(st.session_state.financial_goals)

            st.success("Goal deleted successfully!")
            st.rerun()


    st.divider()
    st.divider()
    st.subheader("🎯 Goal Priority Analyzer")

    if st.button("Analyze Goal Priority"):

        priority_result = analyze_goal_priority(
            st.session_state.financial_goals
        )

        if priority_result["priority_goal"]:

            st.success(
                f"Recommended Priority: {priority_result['priority_goal']}"
            )

            st.metric(
                "Current Progress",
                f"{priority_result['progress']}%"
            )

            st.metric(
                "Remaining Amount",
                f"₹{priority_result['remaining']:,.0f}"
            )

            st.info(priority_result["reason"])

        else:
            st.info(priority_result["reason"])
    st.subheader("🤖 AI Savings Goal Advisor")

    if st.button("Generate AI Goal Recommendations"):

        goals_prompt = f"""
        You are FinWise AI, a personal finance assistant.

        User's savings goals:
        {st.session_state.financial_goals}

        Total target: ₹{total_target}
        Total saved: ₹{total_saved}

        Analyze the goals and provide:
        1. Which goal should be prioritized.
        2. How much more money is needed.
        3. Practical monthly savings suggestions.
        4. Three ways to reach these goals faster.

        Use simple language.
        Do not invent financial information.
        """

        with st.spinner("FinWise AI is analyzing your goals..."):
            try:
                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=goals_prompt
                )

                st.markdown(response.text)

            except Exception as e:
                st.error(f"AI Goal Advisor error: {e}")


    st.divider()
    st.subheader("📅 Monthly Savings Planner")

    if st.session_state.financial_goals:

        planner_goal_names = [
            goal["name"]
            for goal in st.session_state.financial_goals
        ]

        planner_goal = st.selectbox(
            "Choose a savings goal",
            planner_goal_names,
            key="planner_goal_select"
        )

        planner_index = planner_goal_names.index(planner_goal)
        selected_goal_data = st.session_state.financial_goals[planner_index]

        months = st.number_input(
            "Months to achieve your goal",
            min_value=1,
            value=6,
            step=1
        )

        if st.button("Calculate Monthly Savings"):

            plan = calculate_monthly_savings(
                selected_goal_data["target"],
                selected_goal_data["saved"],
                months
            )

            st.metric(
                "Required Monthly Savings",
                f"₹{plan['monthly_savings']:,.2f}"
            )

            st.metric(
                "Remaining Amount",
                f"₹{plan['remaining_amount']:,.2f}"
            )

            st.success(plan["status"])

    else:
        st.info("Add a savings goal first.")


    st.divider()
    st.subheader("⏳ Goal Completion Time Estimator")

    if st.session_state.financial_goals:

        timeline_goal_names = [
            goal["name"]
            for goal in st.session_state.financial_goals
        ]

        timeline_goal = st.selectbox(
            "Select a goal",
            timeline_goal_names,
            key="timeline_goal_select"
        )

        timeline_index = timeline_goal_names.index(timeline_goal)
        timeline_data = st.session_state.financial_goals[timeline_index]

        monthly_contribution = st.number_input(
            "How much can you save monthly? (₹)",
            min_value=1,
            value=5000,
            key="timeline_monthly_savings"
        )

        if st.button("Estimate Completion Time"):

            timeline_result = calculate_goal_timeline(
                timeline_data["target"],
                timeline_data["saved"],
                monthly_contribution
            )

            if timeline_result["status"] == "Goal Already Achieved":
                st.success("Congratulations! Your goal is already achieved.")

            elif timeline_result["status"] == "Goal In Progress":
                st.metric(
                    "Estimated Time",
                    f"{timeline_result['months_required']} months"
                )

                st.success("Your estimated completion timeline is ready!")

            else:
                st.error("Please enter valid values.")

    else:
        st.info("Add a savings goal first.")

elif page == "Debt Repayment":

    from debt_calculator import calculate_debt_repayment

    st.header("💳 Debt Repayment Calculator")
    st.write("Calculate how long it may take to repay your debt.")

    debt_amount = st.number_input(
        "Total Debt Amount (₹)",
        min_value=0.0,
        value=100000.0
    )

    annual_interest_rate = st.number_input(
        "Annual Interest Rate (%)",
        min_value=0.0,
        value=12.0
    )

    monthly_payment = st.number_input(
        "Monthly Payment (₹)",
        min_value=0.0,
        value=10000.0
    )

    if st.button("Calculate Debt Repayment"):

        debt_result = calculate_debt_repayment(
            debt_amount,
            monthly_payment,
            annual_interest_rate
        )

        st.subheader("Repayment Analysis")

        if debt_result["status"] == "Debt Repayment Plan Calculated":

            st.metric("Months Required", debt_result["months_required"])
            st.metric("Total Payment", f"₹{debt_result['total_payment']:,.2f}")
            st.metric("Total Interest", f"₹{debt_result['total_interest']:,.2f}")

            st.success(debt_result["status"])

        else:
            st.warning(debt_result["status"])
elif page == "Loan EMI":

    from loan_emi import calculate_loan_emi

    st.header("🏦 Loan EMI Calculator")
    st.write("Calculate your monthly loan EMI and total interest.")

    principal = st.number_input(
        "Loan Amount (₹)",
        min_value=0.0,
        value=500000.0
    )

    annual_interest_rate = st.number_input(
        "Annual Interest Rate (%)",
        min_value=0.0,
        value=10.0
    )

    years = st.number_input(
        "Loan Duration (Years)",
        min_value=1,
        value=5
    )

    if st.button("Calculate EMI"):

        emi_result = calculate_loan_emi(
            principal,
            annual_interest_rate,
            years
        )

        st.subheader("Loan EMI Analysis")

        if emi_result["status"] == "EMI Calculated Successfully":

            st.metric(
                "Monthly EMI",
                f"₹{emi_result['monthly_emi']:,.2f}"
            )

            st.metric(
                "Total Payment",
                f"₹{emi_result['total_payment']:,.2f}"
            )

            st.metric(
                "Total Interest",
                f"₹{emi_result['total_interest']:,.2f}"
            )

            st.success(emi_result["status"])

        else:
            st.warning(emi_result["status"])
elif page == "Credit Score":

    from credit_score import analyze_credit_score

    st.header("📊 Credit Score Analyzer")
    st.write("Analyze your credit score and get improvement recommendations.")

    credit_score = st.number_input(
        "Enter Your Credit Score",
        min_value=300,
        max_value=900,
        value=750,
        step=1
    )

    if st.button("Analyze Credit Score"):

        credit_result = analyze_credit_score(credit_score)

        st.subheader("Credit Score Analysis")

        st.metric("Your Credit Score", credit_score)

        st.write(
            f"**Credit Rating:** {credit_result['rating']}"
        )

        st.info(credit_result["recommendation"])
elif page == "Investment Calculator":

    from investment_calculator import calculate_investment_return

    st.header("📈 Investment Return Calculator")
    st.write("Estimate your investment growth using compound returns.")

    principal = st.number_input(
        "Initial Investment (₹)",
        min_value=0.0,
        value=100000.0
    )

    annual_return_rate = st.number_input(
        "Expected Annual Return (%)",
        min_value=0.0,
        value=12.0
    )

    years = st.number_input(
        "Investment Duration (Years)",
        min_value=1,
        value=5
    )

    if st.button("Calculate Investment Return"):

        investment_result = calculate_investment_return(
            principal,
            annual_return_rate,
            years
        )

        st.subheader("Investment Analysis")

        if investment_result["status"] == "Investment Calculation Successful":

            st.metric(
                "Initial Investment",
                f"₹{principal:,.2f}"
            )

            st.metric(
                "Final Investment Value",
                f"₹{investment_result['final_value']:,.2f}"
            )

            st.metric(
                "Total Profit",
                f"₹{investment_result['total_profit']:,.2f}"
            )

            st.success(investment_result["status"])

        else:
            st.warning(investment_result["status"])
elif page == "SIP Calculator":

    from sip_calculator import calculate_sip

    st.header("📈 SIP Calculator")
    st.write("Estimate your wealth creation through monthly investments.")

    monthly_investment = st.number_input(
        "Monthly Investment (₹)",
        min_value=0.0,
        value=5000.0
    )

    annual_return_rate = st.number_input(
        "Expected Annual Return (%)",
        min_value=0.0,
        value=12.0
    )

    years = st.number_input(
        "Investment Duration (Years)",
        min_value=1,
        value=10
    )

    if st.button("Calculate SIP"):

        sip_result = calculate_sip(
            monthly_investment,
            annual_return_rate,
            years
        )

        st.subheader("SIP Investment Analysis")

        if sip_result["status"] == "SIP Calculation Successful":

            st.metric(
                "Total Invested",
                f"₹{sip_result['total_invested']:,.2f}"
            )

            st.metric(
                "Estimated Maturity Value",
                f"₹{sip_result['maturity_value']:,.2f}"
            )

            st.metric(
                "Estimated Wealth Gained",
                f"₹{sip_result['wealth_gained']:,.2f}"
            )

            st.success(sip_result["status"])

        else:
            st.warning(sip_result["status"])
elif page == "Net Worth":

    from net_worth import calculate_net_worth

    st.header("💰 Net Worth Calculator")
    st.write("Calculate your total assets, liabilities, and net worth.")

    st.subheader("Your Assets")

    cash = st.number_input("Cash (₹)", min_value=0.0, value=20000.0)
    savings = st.number_input("Savings (₹)", min_value=0.0, value=50000.0)
    investments = st.number_input("Investments (₹)", min_value=0.0, value=100000.0)
    property = st.number_input("Property Value (₹)", min_value=0.0, value=500000.0)
    other_assets = st.number_input("Other Assets (₹)", min_value=0.0, value=10000.0)

    st.subheader("Your Liabilities")

    loans = st.number_input("Outstanding Loans (₹)", min_value=0.0, value=150000.0)
    credit_card_debt = st.number_input("Credit Card Debt (₹)", min_value=0.0, value=10000.0)
    other_liabilities = st.number_input("Other Liabilities (₹)", min_value=0.0, value=5000.0)

    if st.button("Calculate Net Worth"):

        net_result = calculate_net_worth(
            cash,
            savings,
            investments,
            property,
            other_assets,
            loans,
            credit_card_debt,
            other_liabilities
        )

        st.subheader("Net Worth Analysis")

        st.metric("Total Assets", f"₹{net_result['total_assets']:,.2f}")
        st.metric("Total Liabilities", f"₹{net_result['total_liabilities']:,.2f}")
        st.metric("Net Worth", f"₹{net_result['net_worth']:,.2f}")

        if net_result["status"] == "Positive Net Worth":
            st.success(net_result["status"])
        elif net_result["status"] == "Negative Net Worth":
            st.warning(net_result["status"])
        else:
            st.info(net_result["status"])
elif page == "FD Calculator":

    from fd_calculator import calculate_fd

    st.header("🏦 Fixed Deposit Calculator")
    st.write("Calculate your FD maturity amount and interest earned.")

    principal = st.number_input(
        "Deposit Amount (₹)",
        min_value=0.0,
        value=100000.0
    )

    annual_interest_rate = st.number_input(
        "Annual Interest Rate (%)",
        min_value=0.0,
        value=7.0
    )

    years = st.number_input(
        "Investment Duration (Years)",
        min_value=1,
        value=5
    )

    if st.button("Calculate FD"):

        fd_result = calculate_fd(
            principal,
            annual_interest_rate,
            years
        )

        st.subheader("Fixed Deposit Analysis")

        if fd_result["status"] == "FD Calculation Successful":

            st.metric(
                "Principal Amount",
                f"₹{principal:,.2f}"
            )

            st.metric(
                "Maturity Amount",
                f"₹{fd_result['maturity_amount']:,.2f}"
            )

            st.metric(
                "Total Interest",
                f"₹{fd_result['total_interest']:,.2f}"
            )

            st.success(fd_result["status"])

        else:
            st.warning(fd_result["status"])
elif page == "RD Calculator":

    from rd_calculator import calculate_rd

    st.header("🏦 Recurring Deposit Calculator")
    st.write("Estimate your RD maturity amount and interest earned.")

    monthly_deposit = st.number_input(
        "Monthly Deposit (₹)",
        min_value=0.0,
        value=5000.0
    )

    annual_interest_rate = st.number_input(
        "Annual Interest Rate (%)",
        min_value=0.0,
        value=7.0
    )

    years = st.number_input(
        "Deposit Duration (Years)",
        min_value=1,
        value=5
    )

    if st.button("Calculate RD"):

        rd_result = calculate_rd(
            monthly_deposit,
            annual_interest_rate,
            years
        )

        st.subheader("Recurring Deposit Analysis")

        if rd_result["status"] == "RD Calculation Successful":

            st.metric(
                "Total Invested",
                f"₹{rd_result['total_invested']:,.2f}"
            )

            st.metric(
                "Maturity Amount",
                f"₹{rd_result['maturity_amount']:,.2f}"
            )

            st.metric(
                "Total Interest",
                f"₹{rd_result['total_interest']:,.2f}"
            )

            st.success(rd_result["status"])

        else:
            st.warning(rd_result["status"])
from report_generator import generate_financial_report

st.sidebar.divider()
st.sidebar.subheader("📄 Financial Report")

if st.sidebar.button("Generate PDF Report"):
    pdf_path = generate_financial_report(
        income,
        expenses,
        savings,
        savings_rate,
        category_data.to_dict()
    )

    with open(pdf_path, "rb") as pdf_file:
        st.sidebar.download_button(
            label="Download PDF",
            data=pdf_file,
            file_name="FinWise_Financial_Report.pdf",
            mime="application/pdf"
        )

st.sidebar.success("FinWise AI is active")
