import requests

url = "http://localhost:11434/api/generate"

# Simulated vector DB result
retrieved_context = [
    "An Assignment represents the seller's obligation to fulfill the terms of the contract by either selling or buying the underlying security at the exercise price."
    "This obligation is triggered when the buyer of an option contract exercises their right to buy or sell the underlying security."
    "Based on an external file from the custodian, an event is raised for every row of the file by Tibco and published on the servicebus. With help of the replicated option and portfolio data, a market instrument and CLIENT portfolio can be determined, For this portfolio the settlement currency and the fee amount are also determined."
    "This data is used while creating a single booking instruction for TRAN. Transactions on the NOSTRO side are created based on the default custody rules. This page describes the process of creating a booking instruction for a cash settlement in case of an Assignment."
]

# Combine context into a single string
context_text = "\n".join(retrieved_context)

# Build a prompt with context
prompt = f"""
You are an AI assistant specialized in financing and banking. Use the context below to answer the user.

Context:
{context_text}

User question:
What is an assignment?
"""

payload = {
    "model": "llama3",
    "prompt": prompt,
    "stream": False
}

response = requests.post(url, json=payload)

data = response.json()

if "response" in data:
    print(data["response"])
else:
    print("Error:", data)
