import QuantLib as ql
import numpy as npp
import matplotlib 
matplotlib.use('TkAgg')  # Definir o backend para interatividade
import matplotlib.pyplot as plt  # Agora importe o pyplot como de costume

import QuantLib as ql
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Classe que representa uma Opção
class Option:
    def __init__(self, strike, expiry_date, option_type, spot_price, volatility):
        self.strike = strike  # Preço de exercício da opção
        self.expiry_date = expiry_date  # Data de expiração
        self.option_type = option_type  # Tipo de opção (call ou put)
        self.spot_price = spot_price  # Preço do ativo subjacente
        self.volatility = volatility  # Volatilidade da opção

        # Criação da opção com QuantLib
        self.option = self._create_option()

    def _create_option(self):
        # Define o payoff de acordo com o tipo da opção (Call ou Put)
        payoff = ql.PlainVanillaPayoff(
            ql.Option.Call if self.option_type == 'call' else ql.Option.Put, 
            self.strike
        )
        # Exercício europeu
        exercise = ql.EuropeanExercise(self.expiry_date)
        return ql.VanillaOption(payoff, exercise)

    def update_spot_price(self, new_spot_price):
        """ Atualiza o preço do ativo subjacente para a opção """
        self.spot_price = new_spot_price
        spot_handle = ql.QuoteHandle(ql.SimpleQuote(self.spot_price))
        
        # Criando o processo Black-Scholes
        day_count = ql.Actual365Fixed()
        calendar = ql.NullCalendar()
        today = ql.Date.todaysDate()
        ql.Settings.instance().evaluationDate = today
        rate_handle = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, day_count))
        vol_handle = ql.BlackVolTermStructureHandle(
            ql.BlackConstantVol(today, calendar, ql.QuoteHandle(ql.SimpleQuote(self.volatility)), day_count)
        )  # Certifique-se de que todos os parênteses estejam fechados corretamente
        
        # Criando o processo Black-Scholes
        process = ql.GeneralizedBlackScholesProcess(
            spot_handle, rate_handle, rate_handle, vol_handle)  # Alteração feita aqui
        
        # Usando o processo correto no modelo
        self.option.setPricingEngine(ql.AnalyticEuropeanEngine(process))

    def price(self, risk_free_rate, dividend_yield=0):
        # Modelo de precificação (Black-Scholes)
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
        )  # Cert


