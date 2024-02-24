import random


class RansomNegotiationAI:
    def __init__(self, victim_name, initial_demand):
        self.victim_name = victim_name
        self.initial_demand = initial_demand
        self.current_demand = initial_demand
        self.negotiation_rounds = 0
        self.negotiation_history = []

    def process_input(self, user_input):
        return user_input.lower().strip()

    def generate_response(self, user_input):
        user_input = self.process_input(user_input)
        response = ""

        if "demand" in user_input:
            response = f"The current demand is ${self.current_demand}."
        elif "negotiate" in user_input:
            response = self.negotiate()
        elif "pay" in user_input:
            response = self.pay_ransom()
        elif "info" in user_input:
            response = self.get_ransom_info()
        elif "reset" in user_input:
            response = self.reset_negotiation()
        elif "history" in user_input:
            response = self.get_negotiation_history()
        elif "quit" in user_input:
            response = "Thank you for using the ransom negotiation AI. Goodbye!"
        else:
            response = "I'm sorry, I didn't understand that. Please try again."

        return response

    def negotiate(self):
        self.negotiation_rounds += 1
        reduction_factor = 0.1 * self.negotiation_rounds
        new_demand = max(0, int(self.current_demand * (1 - reduction_factor)) + random.randint(-500, 1000))
        self.current_demand = new_demand
        self.negotiation_history.append((self.negotiation_rounds, self.current_demand))
        return f"The new demand after negotiation round {self.negotiation_rounds} is ${self.current_demand}. Would you like to pay now?"

    def pay_ransom(self):
        return f"Thank you for your cooperation. The transaction is being processed."

    def get_ransom_info(self):
        info = f"Victim: {self.victim_name}\nInitial Demand: ${self.initial_demand}\nCurrent Demand: ${self.current_demand}\nNegotiation Rounds: {self.negotiation_rounds}"
        return info

    def reset_negotiation(self):
        self.current_demand = self.initial_demand
        self.negotiation_rounds = 0
        self.negotiation_history = []
        return "Negotiation process has been reset. The initial demand has been restored."

    def get_negotiation_history(self):
        history_str = "Negotiation History:\n"
        for round_num, demand in self.negotiation_history:
            history_str += f"Round {round_num}: ${demand}\n"
        return history_str


# Testing the class if executed directly
if __name__ == "__main__":
    victim_name = "John Doe"
    initial_demand = 10000
    ransom_ai = RansomNegotiationAI(victim_name, initial_demand)

    while True:
        user_input = input("You: ")
        response = ransom_ai.generate_response(user_input)
        print("AI:", response)
        if "transaction" in response or "quit" in response:
            break
