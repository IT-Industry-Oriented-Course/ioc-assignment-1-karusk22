# main.py

from agent.agent import run_agent

def main():
    user_input = input("Enter clinical request: ")

    collected_info = user_input

    while True:
        response = run_agent(collected_info)

        # Case 1: Agent refuses
        if response.get("status") == "REFUSED":
            print(response["reason"])
            break

        # Case 2: Agent needs more info → ASK USER
        if response.get("status") == "NEEDS_MORE_INFORMATION":
            for question in response["questions"]:
                answer = input(question + " ")
                collected_info += " " + answer
            continue

        # Case 3: Successful workflow
        print(response)
        break


if __name__ == "__main__":
    main()
