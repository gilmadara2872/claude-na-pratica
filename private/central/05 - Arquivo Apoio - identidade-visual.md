# Identidade visual · Central de Pessoas · Kora Foods

A Central mostra pessoas, não planilhas. Cada pessoa é um círculo com as iniciais, na cor da sua área.
A interface é escura, com a cor da Kora como destaque, para os números e os alertas brilharem.
Ela deve parecer um produto de verdade: viva, com movimento suave, e nunca poluída.

## Estrutura
- Menu lateral à esquerda, um tom acima do fundo, com um ícone de traço em cada item.
  Só aparecem as telas que o sistema já tem. O item atual fica com um traço laranja à esquerda e o texto claro.
  O menu pode ser recolhido para mostrar só os ícones.
- Barra no topo: busca de pessoas à esquerda; data da planilha e o nome de quem entrou à direita.
- Conteúdo em cartões de cantos bem arredondados (20 px), um tom acima do fundo, com uma borda fina.
- Números do topo em cartões: um círculo com ícone, a frase do que o número significa e o número bem grande.

## Cores
| Nome | Hex | Uso |
| --- | --- | --- |
| Noite | #101521 | fundo das páginas |
| Cartão | #171D2B | cartões e menu |
| Cartão alto | #1F2738 | o que fica por cima: ficha, menus abertos, dicas |
| Linha | #2A3346 | bordas e divisórias |
| Texto | #F1F4FA | texto principal |
| Texto suave | #A4AEC2 | textos de apoio |
| Kora | #FF8A3D | a cor da marca: botões principais, item atual, destaques |
| Verde | #3DDC97 | crescimento, sucesso, confirmação |
| Vermelho | #FF5470 | o que já venceu ou custa dinheiro |
| Âmbar | #FFC23D | o que vence em breve |
| Azul | #5B8CFF | quem está parado (sem promoção) |

Cores por área: Operações #2EC4B6, Logística #4CC9F0, Comercial #C084FC, Financeiro #818CF8,
Marketing #F472B6, TI #A3E635, RH #86EFAC, Qualidade #CBD5E1.
Vermelho e âmbar são só para alertas, nunca para decoração. O laranja da Kora é só para ação e destaque.

## Efeitos de acabamento
O movimento serve para mostrar o que importa, nunca para enfeitar. Tudo rápido (entre 0,2 e 0,6 segundo).
- **Números que contam:** ao abrir a tela, os números grandes sobem de zero até o valor.
- **Mapa que acende:** os círculos entram em sequência, área por área. Quem tem alerta ganha um anel
  que pulsa devagar, com um brilho suave da cor do alerta.
- **Passar o mouse:** o círculo cresce um pouco e mostra nome e cargo numa dica; cartões ganham um brilho leve na borda.
- **Ficha:** desliza por cima da tela, com o fundo escurecido e desfocado.
- **Gravou:** a confirmação aparece em verde, e o que mudou na tela pisca uma vez para mostrar onde mudou.
- **Trocar de aba ou de filtro:** o conteúdo troca com um esmaecer rápido; os pontos do gráfico se movem até a nova posição.
- Quem pediu ao computador menos movimento vê tudo sem animação.

## Tipografia
- A fonte do próprio sistema em tudo ("Segoe UI" no Windows, com system-ui e sans-serif de reserva).
  Não baixe nem instale nenhuma fonte: tem que funcionar em qualquer computador, sem internet.
- Títulos com peso forte; números grandes bem pesados e em algarismos tabulares.
- Corpo em 16 px e textos de gráfico em 14 px no mínimo: a tela vai ser vista numa transmissão ao vivo.
- Frases em caixa normal. Nada de rótulo em caixa alta.

## Princípios
- O elemento marcante é o mapa de pessoas na tela inicial. Nenhum outro elemento compete com ele.
- Nas análises, o título do cartão já é a conclusão; o gráfico à esquerda e a leitura à direita, com o número grande e o que fazer.
- Números grandes só para o que pede ação. Ao lado de cada número, uma frase que diga o que ele significa.
- Listas longas mostram as primeiras linhas e um botão "Mostrar todas".
- Filtros em pílulas; a escolhida fica laranja. Abas em controle segmentado.
- Sem dependência de internet: nada de fonte ou biblioteca de CDN. Ícones e gráficos em SVG no próprio código.
- Textos curtos, em português, do ponto de vista de quem usa ("Registrar promoção", não "Enviar").
- Não mude nenhuma regra nem nenhum número: a identidade é só a aparência.
