from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser

import json


BASE_URL = "http://localhost:1234/v1"
MODEL_NAME = "meta-llama-3.1-8b-instruct"

NB_RESEARCH_RESULTS = 10

DATA_PATH = "data.json"

#TODO : Compete json file
#TODO : Add logger
#TODO : refactor code
#TODO : Add Documentation
#TODO : Add offer


class CoverLetterWriter:
    def __init__(self):
        self.model = self._get_model()
        self.data = self._get_data()
        self.chain = self._get_final_chain()

    def generate_cover_letter(self, company_name):
        return self.chain.invoke({"company_name" : company_name})


    def _get_model(self):
        return ChatOpenAI(base_url=BASE_URL,api_key="xxx",name=MODEL_NAME)
    
    def _get_agent_chain(self):
        agent = self._create_research_agent()
        get_output = RunnableLambda(lambda x : x['output'])
        return agent | get_output
    
    def _get_write_chain(self):
        return self._get_write_prompt_template() | self.model | StrOutputParser()
    
    def _get_final_chain(self):
        return self._get_agent_chain() | self._get_write_chain()
    

    
    def _get_search_prompt_template(self):
        messages = [
        ("system" , self.data['research_prompt']),
        ("human"," Do this for the company: {company_name}") ,
        ("placeholder", "{agent_scratchpad}")
        ]
        return ChatPromptTemplate.from_messages(messages)
    
    def _get_tools_list(self):
        return [TavilySearchResults(max_results=NB_RESEARCH_RESULTS)]
    
    def _create_research_agent(self):
        agent = create_openai_functions_agent(self.model, self._get_tools_list, self._get_search_prompt_template)
        return AgentExecutor(agent=agent,tools=self._get_tools_list(),verbose=False)
    
    def _get_write_prompt_template(self):
        messages = [
        ("system","{prompt}"),
        ("human",""" 
        template : {template}
        profil : {profil} 
        company_data : {company_data}"""),
        ]
        write_prompt = ChatPromptTemplate.from_messages(messages)
        write_prompt = write_prompt.partial(
            prompt=self.data["write_prompt"],
            profil=self.data["profil"],
            template=self.data["template"])
        return write_prompt

    
    def _get_data(self):
        with open(DATA_PATH) as f:
            return json.load(f)
    

if __name__ == "__main__":
    writer = CoverLetterWriter()
    print(writer.generate_cover_letter("Google"))
    




