from autogen import GroupChat, GroupChatManager
from agents import risk_detecting_agent, language_detector_agent,user
import streamlit as st
import fitz
import io
import contextlib
import time

st.title("Risk Detection with AutoGen")

contract_file = st.file_uploader("Upload Contract PDF", type=["pdf"])
rules_file = st.file_uploader("Upload Rules/Policy PDF", type=["pdf"])

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(stream=pdf_path.read(), filetype="pdf")
    return "\n".join(page.get_text() for page in doc)

def chunk_text(text, max_chars=3000):
    return [text[i:i+max_chars] for i in range(0, len(text), max_chars)]


def filter_risk_output(output):
    """Filter the output to show only risk-related content"""
    lines = output.split('\n')
    filtered_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Skip lines that contain agent names or system messages
        if any(agent_name in line for agent_name in ['User (to chat_manager)', 'Language Detector (to chat_manager)', 'Risk Detector (to chat_manager)']):
            continue
            
        # Skip lines that repeat the full documents
        if any(keyword in line.lower() for keyword in [
            'the following is the contract document:',
            'the following are the company rules',
            'please analyze the previously provided contract'
        ]):
            continue
            
        # Keep lines that contain risk analysis
        if any(keyword in line.lower() for keyword in [
            'clause type:', 'risk sentence', '[clause type:', 'language:', 'confidence:'
        ]) or line.startswith('- [') or 'risk' in line.lower():
            filtered_lines.append(line)
    
    return '\n'.join(filtered_lines) if filtered_lines else "No risks detected in the analysis."

if st.button("Analyze Risks"):
    if contract_file and rules_file:
        with st.spinner("Analyzing contract for risks..."):
            contract_text = extract_text_from_pdf(contract_file)
            rules_text = extract_text_from_pdf(rules_file)

            contract_chunks = chunk_text(contract_text, max_chars=3000)

            all_outputs = []

            for i, chunk in enumerate(contract_chunks):
                # Setup new GroupChat and Manager each time (isolated)
                group_chat = GroupChat(
                    agents=[user, language_detector_agent, risk_detecting_agent],
                    messages=[],
                    max_round=4
                )
                chat_manager = GroupChatManager(
                    groupchat=group_chat,
                    llm_config={"config_list": risk_detecting_agent.llm_config["config_list"]},
                )

                result_buffer = io.StringIO()
                with contextlib.redirect_stdout(result_buffer):
                    user.initiate_chat(
                        chat_manager,
                        message=f"""
Please analyze the following contract section for risks based on the company policies.

CONTRACT CHUNK {i+1}:
{chunk}

COMPANY RULES:
{rules_text}

List all risky clauses only.
""",
                        summary_method="last_msg"
                    )
                all_outputs.append(result_buffer.getvalue())
                time.sleep(2)  # prevent API overload on Streamlit Cloud

            combined_output = "\n".join(all_outputs)
            filtered_output = filter_risk_output(combined_output)

            st.subheader("Detected Risks")
            st.markdown(filtered_output)




# if st.button("Analyze Risks"):
#     if contract_file and rules_file:
#         with st.spinner("Analyzing contract for risks..."):
#         # Extract text from uploaded PDFs
#             contract_text = extract_text_from_pdf(contract_file)
#             rules_text = extract_text_from_pdf(rules_file)

#             contract_chunks = chunk_text(contract_text)
#             rules_chunks = chunk_text(rules_text)

#             all_outputs = []

#             # Setup group chat
#             group_chat = GroupChat(
#                 agents=[user, language_detector_agent, risk_detecting_agent],
#                 messages=[],
#                 max_round=4
#             )

#             chat_manager = GroupChatManager(
#                 groupchat=group_chat,
#                 llm_config={"config_list": risk_detecting_agent.llm_config["config_list"]},
#             )

            # Capture the printed output by redirecting stdout
            # import io
            # import contextlib

            # result_buffer = io.StringIO()
            # with contextlib.redirect_stdout(result_buffer):

            #     user.initiate_chat(
            #         chat_manager,
            #         message=f"""Please analyze this contract for risks against the provided rules.

            #                 CONTRACT DOCUMENT:
            #                 {contract_text}

            #                 COMPANY RULES AND POLICIES:
            #                 {rules_text}

            #                 Please identify risky clauses with the help of risk detection agent.""",
            #         summary_method="last_msg",
            #     )

            # Iterate through all combinations of chunks (can be adjusted if needed)
           


    # Get the output and display it
    # chat_output = result_buffer.getvalue()
    # combined_output = "\n".join(all_outputs)
    # filtered_output = filter_risk_output(combined_output)
    # st.subheader("Detected Risks")
    # st.markdown(filtered_output)