from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
import requests
from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline,HuggingFaceEndpoint
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field
load_dotenv()

model=HuggingFacePipeline.from_model_id(
    model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    task="text-generation",
    pipeline_kwargs=dict(
        temperature=0.7,  # temperature controls randomness of language model's output. affects creativity and variability.
       
    )

)

llm=ChatHuggingFace(llm=model)

class ConversionInput(BaseModel):
    first_num:int=Field(...,description="The first value involved in the mathematical operation usually present before a mathematical operator symbol")
    second_num:int=Field(...,description="The second value involved in the mathematical operation usually present after a mathematical operator symbol")
    operator:str=Field(...,description="A mathematical operator like +, -, * or /")

@tool(args_schema=ConversionInput)
def calculator(first_num:int, second_num: int, operator:str) -> float:
    """
    Returns the result of mathematical operation between first number and second number as per the operator provided. Args should be provided as JSON, 
    eg. {"first_num":5, "second_num":7, "operator":"+"}
    """
    if operator=='+':
        return {'result':first_num+second_num}
    elif operator=="-":
        return {'result':first_num-second_num}
    elif operator=="*":
        return {'result':first_num*second_num}
    elif operator=="/":
        return {'result':first_num/second_num}
    else:
        return {'error':'Could not perform mathematical operation on provided query'}


prompt=hub.pull("hwchase17/react")

agent=create_react_agent(
    llm=llm,
    tools=[calculator],
    prompt=prompt
)

agent_executor=AgentExecutor(
    agent=agent,
    tools=[calculator],
    verbose=True,
    handle_parsing_errors=True
)

user_input=input("Type your query")
response=agent_executor.invoke({'input':user_input})
print(response)

