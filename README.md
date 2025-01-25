# Cover Letter Writer
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
you need to in the ```.env``` file with your tavily APi Key
```bash 
TAVILY_API_KEY=<your key>
```
### Setup your local llm

To run this project you need a local llm on a local server. For this you can use [LM Studio](https://lmstudio.ai/)

### Fill your data

Then your own data in the ```profil.json``` et your own template in ```data.json```

### Run it









## Acknowledgements

 - https://github.com/Bredda/genai-talk-notebooks

 - https://www.youtube.com/watch?v=yF9kGESAi3M
