#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera todos os carrosseis de conteudo da Abdalla Tech."""
from carousel_engine import build

import os
_HERE = os.path.dirname(os.path.abspath(__file__))
BASE = _HERE

SPECS = [
    # 1) POSICIONAMENTO — reparo nivel componente
    {
        "slug": "reparo-componente", "item_label": "PONTO",
        "footer_left": "REPARO NÍVEL COMPONENTE · FRANCA / SP",
        "cover": {"title": ["A GENTE CONSERTA", "O QUE OS OUTROS", "MANDAM TROCAR"],
                  "subtitle": "Reparo nível componente: consertamos a peça, não trocamos tudo."},
        "tips": [
            {"icon": "chip", "kicker": "O reparo de verdade", "title": ["REPARO NÍVEL", "COMPONENTE"],
             "body": "Em vez de trocar a placa inteira, a gente localiza e substitui só o componente com defeito: um capacitor, um chip, uma trilha. Conserto na raiz."},
            {"icon": "swap_x", "kicker": "A saída fácil deles", "title": ["POR QUE MANDAM", "VOCÊ TROCAR"],
             "body": "Muita loja não tem equipamento nem conhecimento pra reparo em placa. Aí a saída fácil é trocar tudo e te cobrar caro por isso."},
            {"icon": "money", "kicker": "Seu bolso agradece", "title": ["VOCÊ ECONOMIZA", "MUITO MAIS"],
             "body": "Consertar o componente costuma custar uma fração do valor de uma peça nova. Você resolve o problema gastando bem menos."},
            {"icon": "board", "kicker": "No nível de chip e solda", "title": ["O QUE A GENTE", "REPARA"],
             "body": "Placa-mãe, placa de vídeo (GPU), notebook, fonte, monitor e mais. Reparo em nível de chip, solda e trilha."},
            {"icon": "check_badge", "kicker": "Sem enrolação", "title": ["DIAGNÓSTICO", "HONESTO"],
             "body": "Se não valer a pena consertar, a gente te fala na hora. Sem enrolação e sem conserto desnecessário."},
            {"icon": "microscope", "kicker": "Precisão de verdade", "title": ["EQUIPAMENTO", "PROFISSIONAL"],
             "body": "Estação de solda, microscópio e instrumentos de medição. É reparo feito com precisão, não no chute."},
        ],
        "cta": {"kicker": "ANTES DE TROCAR, PERGUNTE", "headline": ["SUA PEÇA", "TEM", "CONSERTO"],
                "items": ["Placa-mãe que não liga", "GPU com artefato ou sem vídeo",
                          "Notebook 'morto'", "Fonte queimada"],
                "caption": "Manda uma foto da peça no WhatsApp. Diagnóstico honesto e orçamento sem compromisso."},
    },
    # 2) EDUCATIVO — sinais de que o PC vai dar problema
    {
        "slug": "sinais-pc", "item_label": "SINAL",
        "footer_left": "FRANCA / SP · MANUTENÇÃO DE PC",
        "cover": {"title": ["5 SINAIS DE QUE", "SEU PC VAI", "DAR PROBLEMA"],
                  "subtitle": "Fique de olho antes que vire dor de cabeça (e conta alta)."},
        "tips": [
            {"icon": "restart", "kicker": "Do nada, sem motivo", "title": ["TRAVA E", "REINICIA SOZINHO"],
             "body": "Travamentos e reinícios do nada podem ser fonte fraca, superaquecimento ou memória com defeito."},
            {"icon": "monitor", "kicker": "A imagem denuncia", "title": ["TELA AZUL", "OU ARTEFATOS"],
             "body": "Tela azul frequente ou 'quadradinhos' e riscos na imagem indicam problema de memória ou placa de vídeo."},
            {"icon": "thermometer", "kicker": "Calor é inimigo", "title": ["ESQUENTA E", "DESLIGA SOZINHO"],
             "body": "Se desliga sozinho sob carga, provável poeira acumulada, cooler parado ou pasta térmica ressecada."},
            {"icon": "sound", "kicker": "Ouça a máquina", "title": ["BARULHO", "ESTRANHO"],
             "body": "Clique no HD, chiado agudo (coil whine) ou cooler barulhento são avisos claros de desgaste."},
            {"icon": "power", "kicker": "Custa a acordar", "title": ["DEMORA OU", "NEM LIGA"],
             "body": "Liga só na segunda ou terceira tentativa, ou nem acende: fonte ou placa pedindo socorro."},
        ],
        "cta": {"kicker": "PERCEBEU ALGUM SINAL?", "headline": ["NÃO ESPERE", "PARAR DE", "FUNCIONAR"],
                "items": ["PC travando ou reiniciando", "Superaquecimento", "Não liga ou não dá vídeo",
                          "Barulho estranho"],
                "caption": "Quanto antes olhar, mais barato resolver. Chama no WhatsApp e descreve o sintoma."},
    },
    # 3) EDUCATIVO — notebook esquentando
    {
        "slug": "notebook-esquentando", "item_label": "CAUSA",
        "footer_left": "FRANCA / SP · REPARO DE NOTEBOOK",
        "cover": {"title": ["NOTEBOOK", "ESQUENTANDO", "MUITO?"],
                  "subtitle": "As causas mais comuns e o que fazer pra não queimar a placa."},
        "tips": [
            {"icon": "dust", "kicker": "A vilã número 1", "title": ["POEIRA NO", "COOLER"],
             "body": "Poeira acumulada trava a saída de ar quente. Uma limpeza interna resolve boa parte dos casos."},
            {"icon": "syringe", "kicker": "Ela seca com o tempo", "title": ["PASTA TÉRMICA", "RESSECADA"],
             "body": "Com o tempo a pasta seca e para de transferir calor. Trocar a pasta derruba a temperatura na hora."},
            {"icon": "bed", "kicker": "Tapa a ventilação", "title": ["USO NA CAMA", "OU SOFÁ"],
             "body": "Superfície mole tampa as entradas de ar. Use em base firme e, se puder, um suporte com ventilação."},
            {"icon": "fan", "kicker": "Coração da refrigeração", "title": ["COOLER COM", "DEFEITO"],
             "body": "Se o cooler faz barulho ou nem gira, precisa de manutenção ou troca antes que a máquina superaqueça."},
        ],
        "cta": {"kicker": "NOTEBOOK VIVENDO QUENTE?", "headline": ["RESOLVA", "ANTES DE", "QUEIMAR"],
                "items": ["Limpeza interna completa", "Troca de pasta térmica", "Reparo ou troca de cooler",
                          "Notebook desligando sozinho"],
                "caption": "Calor constante mata a placa. Chama no WhatsApp e agende uma manutenção."},
    },
    # 4) EDUCATIVO — cuidados com a fonte
    {
        "slug": "cuidados-fonte", "item_label": "DICA",
        "footer_left": "FRANCA / SP · PC GAMER",
        "cover": {"title": ["CUIDADOS COM A", "FONTE DO SEU", "PC GAMER"],
                  "subtitle": "A fonte protege (ou destrói) o resto do PC. Trate ela bem."},
        "tips": [
            {"icon": "shield_bolt", "kicker": "Não é lugar de economizar", "title": ["NÃO ECONOMIZE", "NA FONTE"],
             "body": "Fonte genérica sem selo é a maior causa de queima de placa. Invista numa fonte de qualidade e certificada."},
            {"icon": "gauge", "kicker": "Nem pouca, nem no limite", "title": ["POTÊNCIA", "CERTA"],
             "body": "Fonte subdimensionada vive no limite e falha. Some o consumo das peças e deixe uma boa folga."},
            {"icon": "plug_bolt", "kicker": "Energia suja mata fonte", "title": ["PROTEJA DA", "ENERGIA"],
             "body": "Picos e quedas de energia danificam a fonte. Um bom estabilizador ou nobreak protege o PC inteiro."},
            {"icon": "fan", "kicker": "Ela precisa de ar", "title": ["DEIXE A FONTE", "RESPIRAR"],
             "body": "Não bloqueie a ventoinha da fonte nem cole o gabinete na parede. Ar livre é fonte mais fria e durável."},
            {"icon": "brush", "kicker": "Manutenção simples", "title": ["LIMPE A", "POEIRA"],
             "body": "Poeira acumulada esquenta e desgasta a fonte. Uma limpeza periódica aumenta bastante a vida útil."},
        ],
        "cta": {"kicker": "SUSPEITA DA SUA FONTE?", "headline": ["FONTE BOA", "PROTEGE O", "PC TODO"],
                "items": ["PC desligando sob carga", "Cheiro de queimado", "Não liga depois de um pico",
                          "Indicação da fonte ideal"],
                "caption": "Antes que a fonte leve a placa junto, chama no WhatsApp pra um diagnóstico."},
    },
    # 5) EDUCATIVO — como limpar o PC por dentro
    {
        "slug": "limpar-pc", "item_label": "PASSO",
        "footer_left": "FRANCA / SP · MANUTENÇÃO DE PC",
        "cover": {"title": ["LIMPE SEU PC", "POR DENTRO SEM", "ESTRAGAR NADA"],
                  "subtitle": "O jeito certo de tirar a poeira sem danificar as peças."},
        "tips": [
            {"icon": "power", "kicker": "Segurança primeiro", "title": ["DESLIGUE E", "TIRE DA TOMADA"],
             "body": "Antes de tudo: PC desligado, cabo fora e, de preferência, uma pulseira antiestática na mão."},
            {"icon": "printer", "kicker": "Sem umidade", "title": ["AR COMPRIMIDO,", "NÃO A BOCA"],
             "body": "Use ar comprimido ou soprador pra tirar a poeira. Soprar com a boca joga saliva e umidade nas peças."},
            {"icon": "fan", "kicker": "Protege o motor", "title": ["SEGURE AS", "VENTOINHAS"],
             "body": "Trave a hélice do cooler com o dedo ao soprar. Girar em excesso pode danificar o motor da ventoinha."},
            {"icon": "brush", "kicker": "Delicadeza nos cantos", "title": ["PINCEL MACIO", "NOS CANTOS"],
             "body": "Pincel de cerdas macias solta a poeira presa em dissipadores e placas. Sem força e sem pressa."},
            {"icon": "no_water", "kicker": "Jamais", "title": ["NADA DE ÁGUA", "OU PRODUTO"],
             "body": "Não use água nem limpa-vidros. Se precisar de líquido, só álcool isopropílico e nas mãos certas."},
        ],
        "cta": {"kicker": "PREFERE DEIXAR COM QUEM ENTENDE?", "headline": ["LIMPEZA", "FEITA DO", "JEITO CERTO"],
                "items": ["Limpeza interna completa", "Troca de pasta térmica", "Revisão de coolers",
                          "PC esquentando ou barulhento"],
                "caption": "Faço a limpeza completa com segurança. Chama no WhatsApp pra agendar."},
    },
    # 6) COMPARATIVO — trocar ou consertar
    {
        "slug": "trocar-ou-consertar", "item_label": "PERGUNTA",
        "footer_left": "FRANCA / SP · REPARO ELETRÔNICO",
        "cover": {"title": ["TROCAR OU", "CONSERTAR?", "COMO DECIDIR"],
                  "subtitle": "4 perguntas que mostram se vale a pena consertar."},
        "tips": [
            {"icon": "scale", "kicker": "A conta principal", "title": ["CUSTA MENOS", "QUE UM NOVO?"],
             "body": "Se o reparo sai por uma fração do valor de um equipamento novo, consertar quase sempre compensa."},
            {"icon": "clock", "kicker": "Idade do equipamento", "title": ["A PEÇA É BOA", "E RECENTE?"],
             "body": "Equipamento bom e atual vale a pena manter. Muito antigo e fraco, às vezes é hora de trocar mesmo."},
            {"icon": "magnifier", "kicker": "Sem chute", "title": ["QUAL O", "DEFEITO REAL?"],
             "body": "Muita coisa que parece 'morta' é um componente barato queimado. Só o diagnóstico revela a verdade."},
            {"icon": "wrench", "kicker": "Faz toda a diferença", "title": ["QUEM VAI", "CONSERTAR?"],
             "body": "Com reparo nível componente, muito 'sem conserto' vira conserto. Peça um diagnóstico antes de trocar."},
        ],
        "cta": {"kicker": "NA DÚVIDA, DIAGNOSTICA", "headline": ["NÃO TROQUE", "SEM ANTES", "PERGUNTAR"],
                "items": ["Diagnóstico do defeito real", "Orçamento do conserto", "Comparação com o valor novo",
                          "Opinião honesta"],
                "caption": "Antes de gastar com um novo, manda uma foto no WhatsApp. Pode ter conserto barato."},
    },
    # 7) EDUCATIVO — mitos x verdades
    {
        "slug": "mitos-manutencao", "item_label": "MITO",
        "footer_left": "FRANCA / SP · MANUTENÇÃO DE PC",
        "cover": {"title": ["MITOS & VERDADES", "DA MANUTENÇÃO", "DO SEU PC"],
                  "subtitle": "Pare de acreditar nessas — seu bolso agradece."},
        "tips": [
            {"icon": "refresh", "kicker": "Verdade: nem sempre", "title": ["FORMATAR", "RESOLVE TUDO"],
             "body": "MITO. Formatar resolve só problema de software. Se é hardware (fonte, memória, calor), o defeito volta na hora."},
            {"icon": "drop_warn", "kicker": "Verdade: o barato sai caro", "title": ["GENÉRICO É", "TUDO IGUAL"],
             "body": "MITO. Peça ou tinta genérica duvidosa entope, esquenta e queima. Nem tudo genérico é ruim, mas o barato demais custa caro."},
            {"icon": "bug", "kicker": "Verdade: nem sempre é vírus", "title": ["PC LENTO", "É VÍRUS"],
             "body": "NEM SEMPRE. Muitas vezes é HD velho, pouca memória RAM ou superaquecimento. Vírus é só uma das causas."},
            {"icon": "dust", "kicker": "Verdade: poeira é inimiga", "title": ["NÃO PRECISA", "LIMPAR POR DENTRO"],
             "body": "MITO. Poeira é a maior inimiga do PC: esquenta, trava e desgasta as peças. Limpeza periódica é essencial."},
            {"icon": "power", "kicker": "Verdade: ligar não é estar 100%", "title": ["SE LIGA,", "TÁ TUDO BEM"],
             "body": "MITO. Dá pra ligar com fonte falhando, memória com erro ou temperatura alta. Perceber cedo evita prejuízo."},
        ],
        "cta": {"kicker": "FICOU NA DÚVIDA?", "headline": ["PERGUNTE A", "QUEM", "ENTENDE"],
                "items": ["PC lento ou travando", "Suspeita de superaquecimento", "Peça genérica dando problema",
                          "Diagnóstico de verdade"],
                "caption": "Nada de achismo. Chama no WhatsApp e descubra o que seu PC realmente tem."},
    },
]

if __name__ == "__main__":
    for spec in SPECS:
        build(spec, f"{BASE}/{spec['slug']}")
    print("TODOS GERADOS")
