# AI-Pharmacy-Agent
An implementation of an AI-powered pharmacist assistant

# Project Overview
In this project I built a real-time conversational AI pharmacy agent, using OpenAI API. 
The agent has database of 5 medications and 10 users. The agent can answer questions regarding prescription 
management, inventory control, and customer service. 
both in hebrew and english.

# Architecture
Backend language - Python
Backend framework - FastAPI
LLM - OpenAI
Database - json files - medications, users
The UI is a simple browser-based interface served by fastAPI.
the UI ables to interact with the agent and display real time responses
users can type random questions, and streaming answers are displayed from the agent.
Agent logic - once getting a text from the user, it detects an intent, if a user asks for dosage, usage, stock availability, to see his prescription etc.
if there is an intent for internal information, then it uses its tools, and databases to reply the correct answer.
according to each intent the agent extracts the data it needs from the text, whether its a name of a medicine or a users name.
This deterministic logic runs before calling the LLM, ensuring controlled and predictable behavior.
Tools are implemented as Python functions, each tools has a single responsibility.
then in pharmancy_tools.py it provides the relevant data from the database and return the correct answer.
The agent injects tool results into the model prompt, ensuring that the language model uses verified data rather than generating information freely.
in order to generate natural language responses I integrated the agent with OpenAI.
A system prompt defines its behaviour.
tool outputs are injected as a system messages.
The LLM never accesses the database directly.






