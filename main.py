# main.py

from agent.agent import run_agent

if __name__ == "__main__":
    query = input("Enter clinical request: ")
    response = run_agent(query)
    print(response)
