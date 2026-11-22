\# FinWise AI – Intelligent Personal Finance Assistant



An AI-powered personal finance management application built with Python, Streamlit, Google Gemini, Retrieval-Augmented Generation (RAG), and function calling.



\## Project Overview



FinWise AI helps users understand and manage their personal finances through intelligent insights, budgeting, expense analysis, financial planning, and AI-powered assistance.



The application combines traditional financial calculations with Generative AI to provide context-aware financial guidance.



\## Key Features



\### Financial Management

\- Budget planning and expense tracking

\- Financial health analysis

\- Credit score insights

\- Debt and loan EMI calculations

\- Emergency fund planning

\- Savings and investment calculators

\- Net worth tracking

\- Financial goal planning and milestones

\- Recurring expense analysis



\### AI-Powered Features

\- AI Spending Insights

\- AI Financial Health Recommendations

\- AI Financial Assistant

\- AI Budget Recommendations

\- AI Monthly Insights

\- AI Forecast Insights

\- AI Savings Goal Advisor



\### Generative AI Implementation



\*\*1. Gemini Integration\*\*

\- Uses Google Gemini for natural-language financial assistance.

\- Generates personalized financial insights and recommendations.



\*\*2. Retrieval-Augmented Generation (RAG)\*\*

\- Uses Sentence Transformers for text embeddings.

\- Uses FAISS for vector similarity search.

\- Retrieves relevant information from a financial knowledge base.

\- Supplies retrieved context to Gemini for grounded responses.



\*\*3. Function Calling\*\*

\- Uses Gemini function calling to invoke Python financial tools.

\- Includes a loan EMI calculation tool.

\- Executes calculations in Python and returns results to Gemini for a natural-language response.



\## Technology Stack



| Component | Technology |

|---|---|

| Programming Language | Python |

| User Interface | Streamlit |

| Generative AI | Google Gemini |

| Embeddings | Sentence Transformers |

| Vector Database | FAISS |

| Data Processing | Pandas, NumPy |

| Visualization | Python visualization libraries |

| Version Control | Git and GitHub |



\## Project Architecture



The application follows a modular architecture:



1\. Streamlit provides the user interface.

2\. Python modules handle financial calculations and analysis.

3\. Gemini generates AI-powered responses.

4\. The RAG engine retrieves relevant financial knowledge.

5\. Gemini function calling invokes Python financial tools.

6\. Results are presented through the Streamlit interface.



See `FinWise\_Architecture.md` for the architecture diagram and additional details.



\## Project Structure



```text

FinWise-AI/

│

├── app.py

├── finance\_tools.py

├── rag\_engine.py

├── loan\_emi.py

│

├── assets/

│   └── style.css

│

├── data/

│   └── knowledge\_base/

│

├── budget\_planner.py

├── credit\_score.py

├── debt\_calculator.py

├── emergency\_fund.py

├── expense\_anomaly.py

├── expense\_forecasting.py

├── financial\_health.py

├── financial\_risk.py

├── investment\_calculator.py

├── net\_worth.py

├── savings\_analyzer.py

├── savings\_planner.py

│

├── FinWise\_Architecture.md

├── .env.example

└── .gitignore

```



\## Installation and Setup



\### 1. Clone the repository



```bash

git clone https://github.com/Parth7544/FinWise-AI.git

cd FinWise-AI

```



\### 2. Create a virtual environment



```bash

python -m venv venv

```



Activate it on Windows:



```bash

venv\\Scripts\\activate

```



\### 3. Install dependencies



pip install -r requirements.txt



\### 4. Configure the Gemini API key



Create a `.env` file in the project root:



```env

GEMINI\_API\_KEY=your\_gemini\_api\_key

```



Get an API key from \[Google AI Studio](https://aistudio.google.com/app/apikey).



\### 5. Run the application



```bash

streamlit run app.py

```



\## Generative AI Demonstration



Example: Loan EMI calculation.



\*\*User Query:\*\*



Calculate EMI for a loan of ₹5,00,000 at 10% annual interest for 5 years.



\*\*AI Result:\*\*

\- Monthly EMI: ₹10,623.52

\- Total Interest: ₹1,37,411.34

\- Total Payment: ₹6,37,411.34



Gemini uses function calling to execute the Python EMI calculator and generate the final response.



\## Project Objectives



\- Simplify personal financial management.

\- Provide intelligent financial insights.

\- Apply Generative AI to a real-world problem.

\- Implement RAG for knowledge-based responses.

\- Demonstrate AI function calling through financial tools.

\- Combine financial analytics with AI assistance.



\## Future Scope



\- Integration with banking APIs.

\- Advanced financial forecasting.

\- Investment portfolio analysis.

\- More AI-powered financial tools.

\- Enhanced financial education and recommendations.



\## Author



\*\*Parth Patil\*\*



B.Tech – Information Technology and Data Science



Ajeenkya DY Patil University



\## Project Guide



\*\*Irshad Ali\*\*



\---



\*\*Project:\*\* FinWise AI  

\*\*Category:\*\* Generative AI / Personal Finance Management

