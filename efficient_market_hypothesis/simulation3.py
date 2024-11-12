import agentpy as ap
import random
import matplotlib.pyplot as plt

class FundamentalAgent(ap.Agent):
    def setup(self):
        self.shares = random.randint(10, 100) 
        self.fundamental_value = 100
        self.random_component = random.uniform(-10,10)
        self.belief = self.fundamental_value + self.random_component
        self.cash = 100000  # Cash available for trading
        self.fundamental = True if self.random_component < 20 else False

    def decide_trade(self, market_price):
        if self.belief > market_price and self.cash >= market_price:
            return "buy"
        elif self.belief < market_price and self.shares > 0:
            return "sell"
        else:
            return "hold"

    def execute_trade(self, trade, market_price):
        if trade == "buy":
            self.shares += 1
            self.cash -= market_price
        elif trade == "sell":
            self.shares -= 1
            self.cash += market_price




class StockMarketModel(ap.Model):
    def setup(self):
        self.agents = ap.AgentList(self, 150, FundamentalAgent)
        self.market_price = 100  # Initial market price
        self.price_history = []  # List to store the market price at each step
        self.fundamental_value_history = []

    def step(self):
        buy_val_diffs = []
        sell_val_diffs = []
        buy_count = 0
        sell_count = 0

        # Calculate buy/sell actions and value differences
        total_valuation = 0
        for agent in self.agents:
            total_valuation += agent.belief
            trade = agent.decide_trade(self.market_price)
            if trade == "buy":
                buy_count += 1
                buy_val_diffs.append(agent.belief - self.market_price)
            elif trade == "sell":
                sell_count += 1
                sell_val_diffs.append(self.market_price - agent.belief)

        # Compute the average valuation differences if there are buyers/sellers
        avg_buy_diff = sum(buy_val_diffs) / len(buy_val_diffs) if buy_val_diffs else 0
        avg_sell_diff = sum(sell_val_diffs) / len(sell_val_diffs) if sell_val_diffs else 0


        self.market_price = total_valuation / 150

        # Record market price for analysis
        self.price_history.append(self.market_price)
        self.fundamental_value_history.append(self.agents[0].fundamental_value)
        

        # Execute trades
        for agent in self.agents:
            agent.execute_trade(agent.decide_trade(self.market_price), self.market_price)

        # Increase fundamental value
        fundamental_sum = 0
        fundamental_count = 0
        extrapolative_sum = 0
        extrapolative_count = 0
        for agent in self.agents:
            #jump
            increase = 0
            if self.t in range(10,13):
                increase = 10
            #normal
            else:
                increase = 1

            agent.fundamental_value = agent.fundamental_value + increase #(1.002 ** self.t)
            if agent.fundamental:
                
                agent.belief = agent.fundamental_value + agent.random_component
                fundamental_sum += agent.belief
                fundamental_count += 1
            else:
                if self.t == 1:
                    agent.belief = agent.fundamental_value + agent.random_component
                else:
                    agent.belief = 0.2 * (agent.fundamental_value + agent.random_component) + 0.8 * (agent.belief + (self.price_history[self.t - 1] - self.price_history[self.t - 2]))
                extrapolative_sum += agent.belief
                extrapolative_count += 1
            
        print ("/nfundamental value: " + str(self.agents[0].fundamental_value))
        print ("price: " + str(self.price_history[self.t - 1]))
        print ("avg fundamental belief: " + str(fundamental_sum/fundamental_count))
        #print ("avg extrapolative belief: " + str(extrapolative_sum/extrapolative_count))

    def end(self):
        print(self.price_history)
        print(self.fundamental_value_history)


# Run the model
parameters = {"steps": 50}
market_model = StockMarketModel(parameters)
results = market_model.run()

# Plot the market price over time
plt.figure(figsize=(10, 6))
plt.plot(market_model.price_history, color='blue', linewidth=2)
plt.plot(market_model.fundamental_value_history, color='red', linewidth=2, linestyle='dashed')
plt.title('Market Price Evolution')
plt.xlabel('Step')
plt.ylabel('Market Price')
plt.grid(True)
plt.show()



