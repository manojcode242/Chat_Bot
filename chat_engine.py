from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
#from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage

class ChatBot:
    AVAILABLE_MODELS = {  # add models as per your Groq account
        # DOC : https://console.groq.com/docs/models (note models change over time)
        "groq/compound-mini": "groq/compound-mini",
        "qwen/qwen3-32b": "qwen/qwen3-32b",
        "groq/compound": "groq/compound",
        "llama-3.1-8b-instant": "llama-3.1-8b-instant"
    }

    def __init__(self, groq_api_key: str, model_name: str = "qwen/qwen3-32b"):
        self.groq_api_key = groq_api_key
        self.model_name = model_name
        self.llm = self._setup_llm()
        self.app = self._setup_workflow()

    def _setup_llm(self):
        return ChatGroq(
            temperature=0.1,
            groq_api_key=self.groq_api_key,
            model_name=self.model_name
        )

    def _setup_workflow(self):
        workflow = StateGraph(state_schema=MessagesState)
        
        def call_model(state: MessagesState):
            #sys_msg = SystemMessage(content="You are a helpful assistant ")
            response = self.llm.invoke(state["messages"])
            return {"messages": response}

        workflow.add_edge(START, "model")
        workflow.add_node("model", call_model)
        
        return workflow.compile(checkpointer=MemorySaver())

    def chat(self, message: str, thread_id: str):
        return self.app.invoke(
            {"messages": [{"role": "user", "content": message}]},
            {"configurable": {"thread_id": thread_id}}
        )

    def update_model(self, model_name: str):
        self.model_name = model_name
        self.llm = self._setup_llm()
        self.app = self._setup_workflow()
