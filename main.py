from autogen import GroupChat, GroupChatManager
from agents import risk_detecting_agent, language_detector_agent,user
import streamlit as st
import fitz
#For token counting
import tiktoken


st.title("Risk Detection with AutoGen")

contract_file = st.file_uploader("Upload Contract PDF", type=["pdf"])
rules_file = st.file_uploader("Upload Rules/Policy PDF", type=["pdf"])

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(stream=pdf_path.read(), filetype="pdf")
    return "\n".join(page.get_text() for page in doc)

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

#Function for token counting
def count_tokens(text):
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


if st.button("Analyze Risks"):
    if contract_file and rules_file:
        with st.spinner("Analyzing contract for risks..."):
        # Extract text from uploaded PDFs
            contract_text = extract_text_from_pdf(contract_file)
            rules_text = extract_text_from_pdf(rules_file)

            #Input
            user_message = f"""Please analyze this contract for risks against the provided rules.

                            CONTRACT DOCUMENT:
                            {contract_text}

                            COMPANY RULES AND POLICIES:
                            {rules_text}

                            Please identify risky clauses with the help of risk detection agent.""",
            
            input_tokens = count_tokens(user_message)

            # Setup group chat
            group_chat = GroupChat(
                agents=[user, language_detector_agent, risk_detecting_agent],
                messages=[],
                max_round=4
            )

            chat_manager = GroupChatManager(
                groupchat=group_chat,
                llm_config={"config_list": risk_detecting_agent.llm_config["config_list"]},
            )

            # Capture the printed output by redirecting stdout
            import io
            import contextlib

            result_buffer = io.StringIO()
            with contextlib.redirect_stdout(result_buffer):

                user.initiate_chat(
                    chat_manager,
                    message=user_message,
                    summary_method="last_msg"
                )

                

    # Get the output and display it
    chat_output = result_buffer.getvalue()
    output_tokens = count_tokens(chat_output)

    #Filter the output to show only risk-related content
    filtered_output = filter_risk_output(chat_output)

    #Show the results
    st.subheader("Detected Risks")
    st.markdown(filtered_output)

    #Show the token counts
    st.subheader("Token Counts")
    st.markdown(f"Input Tokens: {input_tokens}")
    st.markdown(f"Output Tokens: {output_tokens}")

