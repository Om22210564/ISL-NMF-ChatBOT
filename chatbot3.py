import json
from typing import List, Dict, Any
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from apisecrets import GROQ_API_KEY

class ISLChatbot:
    def __init__(self, data_path: str = "ISL_Complete.json"):
        self.isl_data = self._load_data(data_path)
        self.llm = ChatGroq(
            api_key=GROQ_API_KEY,
            model_name="llama3-70b-8192",
            temperature=0.2,
            max_tokens=2048,
        )
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=self._create_system_prompt()),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        self.base_chain = self.prompt | self.llm
        self.message_history = []

    def _load_data(self, path: str) -> Dict[str, Any]:
        try:
            with open(path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Warning: Could not find ISL data file at {path}. Using embedded data.")
            return self._get_embedded_data()

    def _get_embedded_data(self) -> Dict[str, Any]:
        return {
            "title": "Indian Sign Language (ISL) Guide",
            "introduction": {
                "overview": "ISL combines manual signs with non-manual features.",
                "purpose": "This provides mapping of manual signs and NMFs."
            }
        }
        
    def _create_system_prompt(self) -> str:
        return "You are an expert assistant for Indian Sign Language (ISL), specializing in non-manual features (NMFs)."

    def chat(self, user_input: str) -> str:
        if user_input.lower().startswith('link '):
            sign = user_input[5:].strip()
            link = self.get_youtube_link(sign)
            if link:
                return f"YouTube link for '{sign}': {link}"
            else:
                return f"No YouTube link found for '{sign}'."

        self.message_history.append({"role": "user", "content": user_input})
        response = self.base_chain.invoke({"input": user_input, "history": self.message_history})
        self.message_history.append({"role": "assistant", "content": response.content})
        return response.content

    def search_signs(self, query: str) -> List[Dict[str, Any]]:
        results = []
        query = query.lower()
        for sign in self.isl_data.get("components", {}).get("manual_signs", []):
            if query in sign["sign"].lower():
                results.append(sign)
        for link_data in self.isl_data.get("youtube_links", []):
            if query in link_data.get("Word", "").lower():
                results.append(link_data)
        return results
    
    def get_nmf_combinations(self, expression: str) -> List[Dict[str, Any]]:
        """Get sign descriptions that involve specific NMF expressions."""
        results = []
        expression = expression.lower()
        
        for desc in self.isl_data.get("sign_descriptions", []):
            if expression in desc.get("Action Combination", "").lower():
                results.append(desc)
                
        return results
    
    def get_youtube_link(self, sign: str) -> str:
        sign = sign.lower()
        for link_data in self.isl_data.get("youtube_links", []):
            if sign == link_data.get("Word", "").lower():
                return link_data.get("Youtube Link", "")
        return ""

if __name__ == "__main__":
    print("Indian Sign Language (ISL) Chatbot")
    chatbot = ISLChatbot()
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        elif user_input.lower().startswith('search '):
            query = user_input[7:].strip()
            results = chatbot.search_signs(query)
            for result in results:
                if "sign" in result:
                    print(f"Sign: {result['sign']}")
                if "Youtube Link" in result:
                    print(f"Link: {result['Youtube Link']}")
        else:
            response = chatbot.chat(user_input)
            print(f"Chatbot: {response}")
