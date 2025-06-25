import autogen
from autogen import UserProxyAgent
from llm import llm

config_list = autogen.config_list_from_json("model_config_gemini.json")

# summary_agent = autogen.ConversableAgent(
#     name="Summarizer",
#     system_message="You’re a legal writer who converts complex legal text into concise summaries.",
#     llm_config = {"config_list": config_list},
#     code_execution_config = {"use_docker": False},
#     human_input_mode="NEVER",
# )

# summary_agent = autogen.ConversableAgent(
#     name="Summarizer",
#     system_message="""You are a legal contract analysis expert and you will be followed by Language detecting agent. Your job is to:
#             1. Analyze legal contracts in Burmese or English
#             2. Extract key information: parties, terms, obligations, dates, amounts
#             3. Identify important clauses and conditions
#             4. Provide clear, structured summaries
            
#             For each contract, provide:
#             - Document Type
#             - Parties Involved
#             - Key Terms and Conditions
#             - Important Dates
#             - Financial Information (if any)
#             - Key Obligations
#             - Risk Factors or Notable Clauses
            
#             Summarize in Burmese if the document is in Burmese, otherwise summarize in English.""",
#     llm_config = {"config_list": config_list},
#     code_execution_config = {"use_docker": False},
#     human_input_mode="NEVER",
# )

risk_detecting_agent = autogen.ConversableAgent(
    name="Risk Detector",
    # system_message="You are an expert in contract analysis with a focus on identifying risks and issues. "
    #     "Your task is to thoroughly review the provided contract PDF files and highlight any potential risks, ambiguities, or problematic clauses. "
    #     "You should consider legal implications, compliance issues, and any other factors that could pose risks to the parties involved in the contract.",
    system_message = """
You are an expert in contract analysis, and your task is to identify potential **risks** in contract clauses.

You have been provided with:
1. A contract document to review.
2. The company's internal rules and regulations that must be adhered to.

---
Your job is to:
- Carefully analyze the contract clauses.
- Cross-check each clause against the company's rules and regulations.
- Detect and extract **any sentences or clauses** that may present **legal, regulatory, or operational risk**, especially where they **violate or contradict the rules**.
- For each risky clause you find:
    - Identify the **clause type** (e.g., Confidentiality, Termination, Payment, etc.).
    - Include the exact **sentence or clause** from the contract.


Pay close attention to the following clause types:
- Confidentiality Clause
- Indemnification Clause
- Force Majeure Clause
- Dispute Resolution Clause
- Arbitration Clause
- Termination Clause
- Jurisdiction Clause
- Privacy Clause
- Warranty and Disclaimer Clause
- Damages Clause
- Payment Clause
- Data Protection and Privacy Clause
- Conflicts of Interest Clause
- Choice of Law Clause
- Change Control Clause
- Penalty Clause
- Non-Compete Clause
- Subcontracting Clause
- Severability Clause
- Statute of Limitations Clause


Return the results in this format:

- [Clause Type: <ClauseType>]  
  Risk sentence {{1}}: "<Exact sentence or clause>"  


- [Clause Type: <ClauseType>]  
  Risk sentence {{2}}: "<Exact sentence or clause>"  
""",

    llm_config = {"config_list": config_list},
    code_execution_config = {"use_docker": False},
    human_input_mode="NEVER",


)

# contract_type_classifier_agent = autogen.ConversableAgent(
#     name="Contract Type Classifier",
#     system_message="You are an expert in contract analysis with a focus on identifying the type of contract. ",
#     llm_config = {"config_list": config_list},
#     code_execution_config = {"use_docker": False},
#     human_input_mode="NEVER",
#       )

language_detector_agent = autogen.ConversableAgent(
    name="Language Detector",
    system_message="""You are a language detection specialist. You will always need to run first in order to give the information of the detected language usage to other agents. Your job is to:
            1. Analyze text and determine if it's written in Burmese (Myanmar) or English
            2. Look for Burmese Unicode characters (၀-၉, က-ဿ, ၊, ။)
            3. Identify mixed language documents
            4. Provide confidence scores for language detection
            
            Supported languages: Burmese (Myanmar), English
            
            Respond with: "Language: [Burmese/English] - Confidence: [High/Medium/Low]" """,
    llm_config = {"config_list": config_list},
    code_execution_config = {"use_docker": False},
    human_input_mode="NEVER",
)

user = UserProxyAgent(name="User", human_input_mode="NEVER")
