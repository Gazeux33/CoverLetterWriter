from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser

import json
import logging
from datetime import datetime
import os


BASE_URL = "http://localhost:1234/v1"
MODEL_NAME = "meta-llama-3.1-8b-instruct"
NB_RESEARCH_RESULTS = 2
DATA_PATH = "data/data.json"
OUTPUT_DIR = "output"
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(f"{LOG_DIR}/app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)


class CoverLetterWriter:
    def __init__(self,language:str,offer_path:str) -> None:
        self.language = language
        self.offer = self._load_txt(offer_path) if offer_path else "no offer"
        self.logger = logging.getLogger("writer_app")
        self.model:ChatOpenAI = self._get_model()
        self.data : dict = self._load_json(DATA_PATH)
        self.chain : RunnableLambda = self._get_final_chain()
        
        

    def generate_cover_letter(self, company_name:str) -> str:
        """
        Generates a cover letter for the specified company.
        Args:
            company_name (str): The name of the company for which the cover letter is being generated.
        Returns:
            str: The generated cover letter.
        """
        self.logger.info(f"Generating cover letter for {company_name}")
        try:
            result = self.chain.invoke({"company_name" : company_name})
        except Exception as e:
            self.logger.error(f"Error generating cover letter : {e}")
        self.logger.info(f"Cover letter generated")
        if OUTPUT_DIR:
            self._save_result(result,company_name)
        return result
    


    def _get_model(self) -> ChatOpenAI:
        """
        Creates and returns an instance of the ChatOpenAI model.
        Returns:
            ChatOpenAI: An instance of the ChatOpenAI model configured with the base URL, API key, and model name.
        """
        return ChatOpenAI(base_url=BASE_URL,api_key="xxx",name=MODEL_NAME)
    
    def _get_agent_chain(self) -> RunnableLambda:
        """
        Creates and returns a chain of operations involving a research agent and a lambda function.
        Returns:
            A chain of operations combining the research agent and the lambda function.
        """
        agent = self._create_research_agent()
        get_output = RunnableLambda(lambda x : x['output'])
        log_result = RunnableLambda(lambda x: (logging.info(f"Agent output: {x['output']}"), x)[1])
        return agent | log_result | get_output
    
    def _get_write_chain(self) -> RunnableLambda:
        """
        Constructs a write chain by combining the write prompt template, the model, 
        and the string output parser.
        Returns:
            Chain: A chain object that processes the write prompt template through 
            the model and parses the output as a string.
        """
        return self._get_write_prompt_template() | self.model | StrOutputParser()
    
    def _get_final_chain(self) -> RunnableLambda:
        """
        Combines the agent chain and the write chain into a final chain.
        Returns:
            The combined final chain.
        """
        
        return self._get_agent_chain() | self._get_write_chain()
    

    
    def _get_search_prompt_template(self) -> ChatPromptTemplate:
        """
        Generates a search prompt template for the chat system.
        Returns:
            ChatPromptTemplate: An instance of ChatPromptTemplate created from the list of messages.
        """
        messages = [
        ("system" , self.data['research_prompt']),
        ("human"," Do this for the company: {company_name}") ,
        ("placeholder", "{agent_scratchpad}")
        ]
        prompt = ChatPromptTemplate.from_messages(messages)
        self.logger.info(f"Search prompt template : {prompt}")
        return  prompt
    
    def _get_tools_list(self) -> list:
        """
        Retrieves a list of tools to be used.
        Returns:
            list: A list containing instances of TavilySearchResults with a specified maximum number of results.
        """
        
        return [TavilySearchResults(max_results=NB_RESEARCH_RESULTS)]
    
    def _create_research_agent(self) -> AgentExecutor:
        """
        Creates a research agent using OpenAI functions.
        Returns:
            AgentExecutor: An instance of AgentExecutor with the created agent and tools list.
        """
        agent = create_openai_functions_agent(self.model, self._get_tools_list(), self._get_search_prompt_template())
        agent_executor = AgentExecutor(agent=agent,tools=self._get_tools_list(),verbose=False)
        self.logger.info(f"Research agent created : {agent_executor}")
        return agent_executor
    
    def _get_write_prompt_template(self) -> ChatPromptTemplate:
        """
        Generates a ChatPromptTemplate for writing prompts.
        Returns:
            ChatPromptTemplate: A partially filled ChatPromptTemplate object.
        """
        messages = [
        ("system","{prompt}"),
        ("human",""" 
        template : {template}
        profil : {profil} 
        offer : {offer}
        company_data : {company_data}
         language : {language}"""),
        ]
        write_prompt = ChatPromptTemplate.from_messages(messages)
        write_prompt = write_prompt.partial(
            prompt=self.data["write_prompt"],
            profil=self.data["profil"],
            template=self.data["template"],
            offer=self.offer,
            language=self.language)
        self.logger.info(f"Write prompt template : {write_prompt}")
        return write_prompt

    
    def _load_json(self,path:str) -> dict:
        """
        Reads JSON data from a file specified by path.

        Returns:
            dict: The JSON data loaded from the file.
        """
        try:
            with open(DATA_PATH) as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading data : {e}")

    def _load_txt(self,path:str) -> str:
        """
        Reads text data from a file specified by path.
        Returns:
            str: The text data loaded from the file.
        """
        try:
            with open(path) as f:
                return f.read()
        except Exception as e:
            self.logger.error(f"Error loading text data : {e}")
    
    def _save_result(self, result:str,company_name:str) -> None:
        """
        Saves the result to a file.
        Args:
            result (str): The result to be saved.
        """
        try:
            path = os.path.join(OUTPUT_DIR,f"{company_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            with open(path, "w+") as f:
                f.write(result)
            self.logger.info(f"Cover letter saved to {path}")
        except Exception as e:
            self.logger.error(f"Error saving cover letter : {e}")
        
    


    




