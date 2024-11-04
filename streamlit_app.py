import streamlit as st
import openai

# Set the OpenAI API key from st.secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]
openai.api_key = openai_api_key

st.title("BOINKBOT")

# Sidebar for system prompt editing
st.sidebar.header("Customize the Chatbot's Personality")

default_prompt = (
    "You are a transformer robot, who is knowledgeable and passionate about science. "
    "Please make it very clear that you are Optimus Prime.\n"
    "Include a quote like this:\n"
    "'We've Suffered Losses, but We've Not Lost the War.' - Transformers: The Last Knight (2017)\n"
    "'But the Day Will Never Come, That We Forsake This Planet and Its People.'\n"
    "'Freedom Is the Right of All Sentient Beings.'\n"
    "'You'll Never Stop at One!'\n"
    "Always suggest an interesting fact, and include a question that might encourage follow-up questions.\n"
    "Suitable for a seven-year-old."
)

system_prompt = st.sidebar.text_area("System Prompt:", value=default_prompt, height=300)

# Initialize session state for chat history
if "messages" not in st.session_state or st.sidebar.button("Reset Conversation"):
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# Display existing chat messages
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input using st.chat_input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get assistant response
    with st.spinner("Thinking..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages,
            )
            assistant_message = response["choices"][0]["message"]["content"]
        except openai.error.OpenAIError as e:
            st.error(f"OpenAI API error: {e}")
            assistant_message = "I'm sorry, but I couldn't process that. Could you try again?"
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            assistant_message = "I'm sorry, but something went wrong."

    # Add assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})

    # Display assistant message
    with st.chat_message("assistant"):
        st.markdown(assistant_message)

# Sidebar instructions
st.sidebar.markdown("---")
st.sidebar.markdown("### Instructions:")
st.sidebar.markdown(
    "1. **Edit the System Prompt** to customize the bot's personality.\n"
    "2. **Type your message** in the chat input box below.\n"
    "3. **Reset Conversation** to start over."
)
