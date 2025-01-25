# MotivAI
This project is an ia agent created with langchain in python and which aims to create cover letters by being able to search the internet for information on the company in question and adapt to a template letter, your profile and a job offer if there is one, using the power of an llm of your choice.

 - [Tavily Rrsearch tool](https://app.tavily.com)
 - [Langchain documentation](https://python.langchain.com/docs/tutorials/)

![Chain graph](https://github.com/Gazeux33/CoverLetterWriter/blob/master/assets/graph_chain.png)



## How to use it

### Installing dependencies

```bash
pip install -r requirements.txt
```

### Fill API key
you need to fill the ```.env``` file with your tavily APi Key
```bash 
TAVILY_API_KEY=<your key>
```
### Setup your local llm

To run this project you need a local llm on a local server. For this you can use [LM Studio](https://lmstudio.ai/)
Recommended model : [meta-llama-3.1-8b-instruct](https://huggingface.co/lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF)

### Fill your data

Then your own data in the ```data.json``` 

### Run it

```bash
python main.py -n "Company Name"

# Generate a cover letter in English
python main.py -n "Company Name" -l "en"

# Generate a cover letter with a specific job offer
python main.py -n "Company Name" -l "en" -o "path/to/job_offer.txt"
```





## Acknowledgements

 - https://github.com/Bredda/genai-talk-notebooks

 - https://www.youtube.com/watch?v=yF9kGESAi3M
