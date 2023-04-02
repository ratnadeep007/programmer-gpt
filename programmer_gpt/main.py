import os
import streamlit as st
from dotenv import load_dotenv
from streamlit_chat import message
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import SimpleSequentialChain, LLMChain
from langchain.chains.conversation.memory import ConversationBufferMemory

load_dotenv()

if 'convo_type' not in st.session_state:
    st.session_state.convo_type = 'new'
    st.session_state.question = None

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(temperature=.4) # type: ignore
template = """You are a logical problem solver who uses programming. You understand the
question then write proper {language} code for that problem code in markdown format
annonate code block with proper programming languaage and 
then execute given code and give answer in markdown quotes.
Question: {question}
Code:
Answer:
"""

prompt_template = PromptTemplate(input_variables=["question", "language"], template=template)
# memory = ConversationBufferMemory(memory_key="chat_history")

llm_chain = LLMChain(
    llm=llm,
    prompt=prompt_template,
    verbose=True,
)

st.title("Programmer GPT")
st.markdown("A GPT-4 powered programmer that tries to solve logical problem using programming")
st.markdown("Example: \nJohn has 15 apple, he distributed apples equally 3 people and Jessie has 3 mangos and she also distributed those equally. How many fruits does each one have now?")

print(st.session_state)

question = st.session_state.question
is_clear = False

# if st.session_state.convo_type == 'new':
language_selectbox = st.empty()
language = language_selectbox.selectbox(
    "Which Programming lanugage?",
    ("Javascript", "Python", "Typescript", "Golang", "Rust"),
)

placeholder = st.empty()

with placeholder.container():
    col1, col2 = st.columns([9,1])
    question_input = st.empty()
    question = col1.text_area("dsadasdas", placeholder="Problem Statement", max_chars=200, height=50, label_visibility="collapsed")
    print(question)
    if question == "":
        col2.markdown("###")
    is_clear = col2.button("Clear")
    if is_clear:
        question = ""
    if question != "":
        question_input.empty()
        with placeholder.container():
            col1, col2 = st.columns([9,1])
            col1.write(question)
        answer = llm_chain.predict(question=question, language=language)
        st.markdown(answer)
st.session_state.question = question
st.session_state.convo_type = 'continue'

# def parse_answer(text: str):
