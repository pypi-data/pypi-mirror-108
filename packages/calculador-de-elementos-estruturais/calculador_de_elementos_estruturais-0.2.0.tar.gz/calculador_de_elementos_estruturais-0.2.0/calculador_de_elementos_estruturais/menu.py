from .viga_de_madeira import VigaDeMadeira
from .pilar_de_madeira import PilarDeMadeira
from .enunciado_pv import Enunciado
from .ligacao_corte_duplo import LigacaoCorteDuplo

'''from viga_de_madeira import VigaDeMadeira
from pilar_de_madeira import PilarDeMadeira
from enunciado_pv import Enunciado
from ligacao_corte_duplo import LigacaoCorteDuplo'''

class MenuPrincipal:

    def __init__(self):
        print('\n\nBem vindo ao Calculador de Estruturas do 4º TE. A seguir, um pequeno tutorial de uso.\n\n')
        print('Se tudo der certo, você só deve copiar e colar o enunciado. Mas caso não dê:\n')
        print('Quando aparecer um seletor, por exemplo: \n (1) Opção 1 \n (2) Opção 2')
        print('Digite somente o número que está dentro dos parênteses. Por exemplo, se sua a opção desejada for a 2,')
        print('digite apenas "2" (sem as aspas).\n')
        print('Não é necessário digitar as unidades dos valores, apenas o número é necessário.')
        print('Caso a unidade seja digitada, erros ocorrerão.\n')
        print('Caso seja necessário digitar algum valor decimal, separe as casas decimais por ponto, e não por vírgula.')
        print('Exemplo: O valor decimal é "1,2", você deve digitar "1.2"\n\n')

        while True:
            
            enunciado = Enunciado.pega_enunciado()
            
            if enunciado != ' ':
                if 'PILAR' in enunciado:
                    PilarDeMadeira(enunciado)
                elif 'VIGA' in enunciado:
                    VigaDeMadeira(enunciado)
                elif 'CORTE DUPLO' in enunciado:
                    LigacaoCorteDuplo(enunciado)
                else:
                    raise ValueError('Digite um valor válido.')
            else:
                mensagem = '''Qual elemento estrutural irá ser calculado?
        
                (1) Pilar
                (2) Viga
                (3) Ligação Corte Duplo
            
                 '''
                elemento = int(input(mensagem))

                if elemento == 1:
                    PilarDeMadeira(None)
                elif elemento == 2:
                    VigaDeMadeira(None)
                elif elemento == 3:
                    LigacaoCorteDuplo(None)
                else:
                    raise ValueError('Digite um valor válido.')
