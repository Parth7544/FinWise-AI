
from loan_emi import calculate_loan_emi
from google.genai import types
import time

def calculate_loan_emi_tool(
    principal,
    annual_interest_rate,
    years
):
    """Calculate loan EMI and total interest."""

    return calculate_loan_emi(
        principal,
        annual_interest_rate,
        years
    )


loan_emi_declaration = types.FunctionDeclaration(
    name="calculate_loan_emi",
    description=(
        "Calculate the monthly EMI, total loan payment, "
        "and total interest for a loan."
    ),
    parameters={
        "type": "OBJECT",
        "properties": {
            "principal": {
                "type": "NUMBER",
                "description": "Loan principal amount in Indian rupees."
            },
            "annual_interest_rate": {
                "type": "NUMBER",
                "description": "Annual interest rate in percentage."
            },
            "years": {
                "type": "NUMBER",
                "description": "Loan repayment period in years."
            }
        },
        "required": [
            "principal",
            "annual_interest_rate",
            "years"
        ]
    }
)


finance_tools = [
    types.Tool(
        function_declarations=[loan_emi_declaration]
    )
]

def execute_finance_tool(function_name, arguments):

    if function_name == "calculate_loan_emi":

        return calculate_loan_emi_tool(
            principal=arguments["principal"],
            annual_interest_rate=arguments["annual_interest_rate"],
            years=arguments["years"]
        )

    return {
        "status": "Unknown Tool",
        "message": f"Tool '{function_name}' is not available."
    }
def generate_with_retry(client, contents, config, max_retries=3):

    for attempt in range(max_retries):

        try:
            return client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=contents,
                config=config
            )

        except Exception as e:

            error_message = str(e)

            if "503" in error_message or "UNAVAILABLE" in error_message:

                if attempt < max_retries - 1:
                    time.sleep(5 * (attempt + 1))
                else:
                    raise

            else:
                raise

def run_finance_agent(client, prompt):

    from google.genai import types

    contents = [prompt]

    config = types.GenerateContentConfig(
        tools=finance_tools
    )

    # Ask Gemini to process the user's question
    response = generate_with_retry(
        client,
        contents,
        config
    )

    # Allow up to 5 tool-calling rounds
    for _ in range(5):

        candidate = response.candidates[0]
        model_content = candidate.content

        function_calls = [
            part.function_call
            for part in model_content.parts
            if part.function_call
        ]

        # No more tool calls: return Gemini's answer
        if not function_calls:
            return response.text

        # Preserve Gemini's function-call message
        contents.append(model_content)

        function_response_parts = []

        # Execute every requested function
        for function_call in function_calls:

            result = execute_finance_tool(
                function_call.name,
                dict(function_call.args or {})
            )

            function_response_parts.append(
                types.Part.from_function_response(
                    name=function_call.name,
                    response=result
                )
            )

        # Send Python's results back to Gemini
        contents.append(
            types.Content(
                role="user",
                parts=function_response_parts
            )
        )

        # Ask Gemini to generate the final answer
        response = generate_with_retry(
            client,
            contents,
            config
        )

    return "Maximum tool-calling rounds reached. Please try again."
