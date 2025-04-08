import QuantLib as ql
import matplotlib.pyplot as plt
import numpy as np

class Option:
    def __init__(self, strike, expiry_date, option_type, spot_price, volatility):
        self.strike = strike  # Preço de exercício da opção
        self.expiry_date = expiry_date  # Data de expiração
        self.option_type = option_type  # Tipo de opção (call ou put)
        self.spot_price = spot_price  # Preço do ativo subjacente
        self.volatility = volatility  # Volatilidade da opção

    def option_price(self, risk_free_rate, dividend_yield=0):
        """Calcula o preço da opção usando o modelo de Black-Scholes"""
        day_count = ql.Actual365Fixed()
        calendar = ql.NullCalendar()
        today = ql.Date.todaysDate()
        ql.Settings.instance().evaluationDate = today

        # Definindo os parâmetros financeiros (spot, taxa de juros, volatilidade)
        spot_handle = ql.QuoteHandle(ql.SimpleQuote(self.spot_price))
        rate_handle = ql.YieldTermStructureHandle(ql.FlatForward(today, risk_free_rate, day_count))
        dividend_handle = ql.YieldTermStructureHandle(ql.FlatForward(today, dividend_yield, day_count))
        vol_handle = ql.BlackVolTermStructureHandle(
            ql.BlackConstantVol(today, calendar, ql.QuoteHandle(ql.SimpleQuote(self.volatility)), day_count)
        )

        # Calculando o preço da opção usando Black-Scholes
        process = ql.GeneralizedBlackScholesProcess(
            spot_handle, rate_handle, rate_handle, vol_handle)
        engine = ql.AnalyticEuropeanEngine(process)
        option = ql.VanillaOption(ql.PlainVanillaPayoff(
            ql.Option.Call if self.option_type == 'call' else ql.Option.Put, self.strike), 
            ql.EuropeanExercise(self.expiry_date))
        option.setPricingEngine(engine)
        return option.NPV()  # Preço da opção (prêmio)

    def payoff(self, spot_price):
        """Calcula o payoff na expiração da opção"""
        if self.option_type == 'call':
            return max(0, spot_price - self.strike)
        else:
            return max(0, self.strike - spot_price)

# Parâmetros ajustados da opção
strike = 95  # Preço de exercício mais próximo do preço spot
option_type = 'call'  # Tipo de opção ('call' ou 'put')
initial_spot_price = 100  # Preço inicial do ativo subjacente
volatility = 0.2  # Volatilidade anual
risk_free_rate = 0.05  # Taxa de juros livre de risco

# Definindo o prêmio da opção (calculado com o modelo de Black-Scholes)
expiry_date = ql.Date(31, 12, 2025)  # Data de expiração

# Lista de preços do ativo subjacente para simulação
spot_prices = np.linspace(80, 120, 100)  # Preços de 80 a 120 para um comportamento mais realista
option_prices = []
payoff_values = []

# Calculando o preço da opção (Black-Scholes) e o payoff para cada preço do ativo subjacente
for spot_price in spot_prices:
    option = Option(strike, expiry_date, option_type, spot_price, volatility)
    option_price = option.option_price(risk_free_rate)  # Calculando o preço da opção
    payoff_value = option.payoff(spot_price)  # Calculando o payoff da opção
    option_prices.append(option_price)
    payoff_values.append(payoff_value)

# Plotando o gráfico do valor da opção em função do preço do ativo subjacente
plt.figure(figsize=(10, 6))

# Plotando a evolução do preço da opção (Black-Scholes)
plt.plot(spot_prices, option_prices, label=f"Preço da Opção ({option_type.capitalize()})", color='orange')

# Plotando o payoff da opção na expiração
plt.plot(spot_prices, payoff_values, label=f"Payoff na Expiração ({option_type.capitalize()})", color='green')

# Ajustando o gráfico
plt.title(f'Valor da Opção e Payoff na Expiração ({option_type.capitalize()})')
plt.xlabel('Preço do Ativo Subjacente (Spot Price)')
plt.ylabel('Valor da Opção / Payoff')
plt.legend()
plt.grid(True)

# Exibindo o gráfico
plt.tight_layout()  # Para evitar problemas de sobreposição no gráfico
plt.show()