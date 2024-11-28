from typing import Any


class IndicadoresExplicacao:
    #Metodo construtor para iniciar os atributos de minha classe
    def __init__(self):
        self.pl = """P/L: O índice representa uma proporção entre o preço da ação e o lucro da empresa.
        Quanto menor for esse índice, melhor para um investidor."""
        self.psr = """PSR: Price to Sales Ratio. Esse indicador serve para avaliar o crescimento da ação, e também medir seu risco.
        Quanto maior for o PSR, maior é o risco de investir nessa empresa. 
        PSR acima de 1.5 indica um alto grau de risco."""
        self.p_vp = """P/VP:O índice representa uma proporção entreo o preço da ação e valor patromonial da empresa.
         Quanto menor for o índice, melhor para o investidor.  """
        self.dy = """Dividend yield: Representa uma relação, em %, entre o a quantidade de dividendos pagos e o preço da ação.
        Quanto for esse índice, melhor para o investidor, pois indica que ela está pagando bons dividendos"""
        self.margem_liquida = """Margem Líquida: Representa a proporção entre o lucro líquido  e a receita líquida da empresa.
        Quanto maior for a margem liquida, melhor para o investidor."""
        self.margem_ebit = """Margem EBIT: É um índice que revela a taxa de lucratividade de uma empresa, antes de juros e impostos.
        Quanto maior for a margem EBIT, melhor para o investidor"""
        self.roe = """Return On Equity: Medida que demonstra a capacidade da empresa gerar lucro a partir do capital investido nela pelos acionistas.
        Quanto maior for o ROE, melhor para o investidor."""
        self.marge_bruta = """Margem bruta: Indica a rentabilidade da empresa, sem levar em consideração qualquer cuso de operação.
        Quanto maior for o índice, melhor para o investidor, mas não necessariamente uma grande margem bruta significa algo positivo para o investidor,
        pois se os custos operacionais forem grandes, o retorno ao investidor não serão tão bons."""
        self.p_ebit = """P/EBIT: Relaciona o preço da ação """
        self.roa = """Return on assets: Indica o quão eficiente é a empresa ao utilizar seus recursos para gerar lucro.
        Quanto maior for o índice, melhor para o investidor.
        """

        self.rsi = """Índice de força relativa: Representa o quão rápido o preço de um ativo vai se alterando.
        Quanto maior o rsi, maior é a variação de preço da ação."""
    

    def get_pl(self) -> str:
        return self.pl
    
    def get_psr(self) -> str:
        return self.psr
    
    def get_p_vp(self):
        return self.p_vp

    def get_dy(self):
        return self.dy

    def get_margem_liquida(self):
        return self.margem_liquida
    
    def get_roe(self):
        return self.roe

    def get_margem_bruta(self):
        return self.marge_bruta

    def get_p_ebit(self):
        return self.p_ebit
    
    def get_roa(self):
        return self.roa