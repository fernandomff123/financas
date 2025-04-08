import QuantLib as ql
from enum import Enum

# Definindo um Enum para os tipos de opção
class OptionType(Enum):
    CALL = "call"
    PUT = "put"

class Option:
    def __init__(self, strike, expiry_date, option_type: OptionType):
        self.strike = strike  # Preço de exercício da opção
        self.expiry_date = expiry_date  # Data de expiração
        self.option_type = option_type  # Tipo de opção (call ou put)

        # Criação da opção com QuantLib
        self.option = self._create_option()

    def _create_option(self):
        """Cria a opção com QuantLib"""
        payoff = ql.PlainVanillaPayoff(
            ql.Option.Call if self.option_type == OptionType.CALL else ql.Option.Put, 
            self.strike
        )
        exercise = ql.EuropeanExercise(self.expiry_date)
        return ql.VanillaOption(payoff, exercise)

    def _create_black_scholes_process(self, spot_price, risk_free_rate, dividend_yield=0, volatility=0):
        """Cria o processo Black-Scholes com base nos parâmetros fornecidos"""
        day_count = ql.Actual365Fixed()
        calendar = ql.NullCalendar()
        today = ql.Date.todaysDate()
        ql.Settings.instance().evaluationDate = today

        spot_handle = ql.QuoteHandle(ql.SimpleQuote(spot_price))
        rate_handle = ql.YieldTermStructureHandle(ql.FlatForward(today, risk_free_rate, day_count))
        dividend_handle = ql.YieldTermStructureHandle(ql.FlatForward(today, dividend_yield, day_count))
        vol_handle = ql.BlackVolTermStructureHandle(
            ql.BlackConstantVol(today, calendar, ql.QuoteHandle(ql.SimpleQuote(volatility)), day_count)
        )

        return ql.GeneralizedBlackScholesProcess(
            spot_handle, rate_handle, dividend_handle, vol_handle
        )

    def update_spot_price(self, new_spot_price):
        """Atualiza o preço do ativo subjacente para a opção"""
        self.spot_price = new_spot_price
        spot_handle = ql.QuoteHandle(ql.SimpleQuote(self.spot_price))

        # Atualiza o processo Black-Scholes
        process = self._create_black_scholes_process(self.spot_price, 0.05)  # Usando taxa livre de risco padrão para exemplo
        self.option.setPricingEngine(ql.AnalyticEuropeanEngine(process))

    def price(self, spot_price, risk_free_rate, volatility, dividend_yield=0):
        """Calcula o preço da opção usando o modelo de Black-Scholes"""
        process = self._create_black_scholes_process(spot_price, risk_free_rate, dividend_yield, volatility)
        self.option.setPricingEngine(ql.AnalyticEuropeanEngine(process))
        return self.option.NPV()  # Retorna o valor presente líquido da opção
