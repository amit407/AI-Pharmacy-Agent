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

UI is a simple browser-based interface served by fastAPI.

This UI ables to interact with the agent and display real time responses
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

# Functions Documentations
tool - get_stock

retrieve the current stock availability for a given medication.

input - med_name. type - str. (English or hebrew)

output Schema - {"name": "Paracetamol", "stock": 25}

Error handling - if the med is not found in the database returns: {"error": "medication 'X' not found. please check spelling or ask a pharmacist."}

Fallback behavior - if med not in DB, the agent will respond using general knowledge without using tools.


tool - get_dosage

returns dosage instructions for a given medication.

input - med_name. type - str. (English or hebrew)

output Schema - {"name": "Paracetamol", "dosage": "200mg every 8 hours"}

Error handling - if the med is not found in the database returns: {"error": "medication 'X' not found. please check spelling or ask a pharmacist."}

Fallback behavior - if dosage is missing, returns "N/A" and the agent clarifies limitations.


tool - get_active_ingridient

return the active ingridient of a given medication.

input - med_name. type - str. (English or hebrew)

output Schema -    {"name": "Cough Syrup", "active_ingredient": "Dextromethorphan"}

Error handling - error response

Fallback behavior - if med not in DB, the agent will respond using general knowledge without using tools.


tool get_user_prescription

Return the prescription list for a verified user.

output schema - input - user_name. type - str. (English or hebrew)

output schema -{"name": "Dana Katz", "prescription": ["Cough syrup", "Paracetamol"]}

Error handling - if user not found in DB, error message requsting correct and full name.

Fallback behavior - No fallback to AI-generated prescriptions, safety decision.


# How to run
build docker image - docker build -t ai-agent .

run docker - docker run -p 8000:8000 ai-agent

open browser - http://127.0.0.1:8000


# Multi step flows
Flow 1 - medication Availability 

1. user asks a free text question
2. agent detects intention - 'stock'
3. agent extracts med name
4. agent calls get_stock()
5. tool returns with the stock availability
6. agent responds using only the output of the tool


Flow 2 - Presciption lookup (user wants to see their prescription) 

1. user provides their name
2. agent verifies user exist in the DB
3. agent detects intention - 'prescription'
4. agent calls get_user_prescription
5. tool returns with the user's prescription


Flow 3 - Medication Dosage

1. users asks about dosage of a med
2. agent detects intent - 'dosage'
3. aget extracts medication name
4. agent calls tool 'get_dosage'
5. tool returns the dosage of the medication
6. agent responds in the user's language


# Evidence

<img width="855" height="715" alt="Screenshot 2026-01-03 182503" src="https://github.com/user-attachments/assets/2a2a1193-8625-4d4c-88a1-64fe4ce77c16" />


<img width="967" height="708" alt="Screenshot 2026-01-03 183519" src="https://github.com/user-attachments/assets/5be4d770-63e3-4519-bcbb-b1debd30e848" />


# Evaluation

each flow should is tested-

to verify tools outputs match the DB values. (to ensure no made up values are displayed)

to confirm correct intent detection, and correct tool invocation, and ensure logic.

test both hebrew and english

test unknown medications, test incorrect user names - check error responses

test that no medical advice is given

ensure tools are preffered but if didnt find intention and tools are not needed - confirm AI generated responses



