# =============================================================================
# INTERFACE GRAPHIQUE "DÉTECTEUR FUITE CLIENTS BCI"
# =============================================================================

# 1. INSTALLATION DES OUTILS - s’exécute auto
!pip install -q gradio pandas matplotlib

import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import gradio as gr

# 2. BASE DE DONNÉES : 20 emails test BCI.
EMAILS_BCI_DEMO = [
  "Bonjour, je veux fermer mon compte BCI. Les taxes sont trop élevées chaque mois.",
  "Péssimo atendimento na agência da 24 de Julho. 3h na fila para nada. Quero fechar.",
  "App BCI não funciona no meu telefone desde atualização. Vou para Millennium.",
  "Tiraram-me 500mt não sei de quê. Taxa fantasma. Encerrem a conta por favor.",
  "Demora muito para ser atendido no balcão. Perco manhã toda. Vou fechar.",
  "Cobram taxa de manutenção e taxa de inactividade. Roubo. Quero sair do BCI.",
  "Atendente foi muito grosso comigo. Falta de respeito. Fechem minha conta.",
  "Aplicativo dá sempre erro quando tento fazer transferência. Cansado.",
  "Fila enorme todos os dias na agência Matola. Não tenho tempo para isso.",
  "Não explicam as taxas. Só vejo dinheiro a sumir. Quero encerrar.",
  "Sistema sempre fora do ar quando preciso. Vou mudar de banco.",
  "Taxa de levantamento no ATM de outro banco é absurda. Fecho conta.",
  "Funcionários não resolvem problema. Empurram de um para outro. Chega.",
  "E-jamii vive com problemas. Não consigo consultar saldo. Desisto.",
  "Cobrança indevida de 200mt. Ninguém sabe explicar. Encerrem.",
  "Tempo de espera no 24443 é 40min. Serviço horrível. Vou sair.",
  "Cada vez que vou agência perco dia trabalho. Não compensa mais.",
  "Descontos que não entendo no extrato. Falta transparência. Adeus BCI.",
  "App não abre no iPhone 11. Já reclamei 3x. Vou fechar.",
  "Muito burocracia para tratar um assunto simples. Outros bancos são melhores."
]

# 3. CERVEAU IA : classifie motif de fuite
MOTIFS = {
  "Taxas elevadas": ["taxa", "taxas", "cobram", "desconto", "tiraram", "roubo", "manutenção", "inactividade", "fantasma", "cobrança"],
  "Mau atendimento": ["fila", "demora", "espera", "atendente", "grosso", "respeito", "funcionários", "burocracia", "balcão"],
  "App/Sistema falha": ["app", "aplicativo", "sistema", "erro", "não funciona", "não abre", "e-jamii", "fora do ar", "transferência"],
  "Falta transparência": ["não explicam", "não sei", "não entendo", "transparência", "sumir"]
}

def classer_email(texte):
  texte = texte.lower()
  for motif, mots_cles in MOTIFS.items():
    if any(palavra in texte for palavra in mots_cles):
      return motif
  return "Outro"

# 4. FONCTION PRINCIPALE : lancée par le bouton
def analisar_fuga_bci(texte_emails):
  # Si utilisateur colle ses emails, on utilise. Sinon on prend démo
  if texte_emails.strip():
    emails = [linha.strip() for linha in texte_emails.split('\n') if linha.strip()]
  else:
    emails = EMAILS_BCI_DEMO

  # Analyse
  resultats = [classer_email(email) for email in emails]
  contagem = Counter(resultats)
  total = len(emails)

  # Création graphique
  fig, ax = plt.subplots(figsize=(6,6))
  ax.pie(contagem.values(), labels=contagem.keys(), autopct='%1.0f%%', startangle=90)
  ax.set_title(f'Porque {total} clientes fogem do BCI')

  # Création rapport texte
  top1 = contagem.most_common(1)[0]
  relatorio = f"""
=== RELATÓRIO FUGA CLIENTES BCI ===
Total emails analisados: {total}

TOP 3 MOTIVOS DE SAÍDA:
"""
  for i, (motif, qtd) in enumerate(contagem.most_common(3), 1):
    percent = (qtd/total)*100
    relatorio += f"{i}. {motif}: {qtd} clientes = {percent:.0f}%\n"

  relatorio += f"\nACÇÃO URGENTE BCI:\n"
  if top1[0] == "Taxas elevadas":
    relatorio += "-> Rever tabela de taxas + comunicar melhor na agência.\n"
  elif top1[0] == "Mau atendimento":
    relatorio += "-> Formar equipa balcão + reduzir filas 24 Julho e Matola.\n"
  elif top1[0] == "App/Sistema falha":
    relatorio += "-> Corrigir bug iPhone + erro transferência. Prioridade TI.\n"

  clientes_salvos = int(total * 0.02 * 30) # 2% sauvés sur 30j
  ganho = clientes_salvos * 4000
  relatorio += f"\nROI: Se salvar só 2% fuga = +{ganho:,} MZN/mês para BCI."
  relatorio += f"\nCusto serviço: 120,000 MZN/mês. Piloto grátis 14 dias."

  return fig, relatorio

# 5. CRÉATION INTERFACE GRAPHIQUE 1 BOUTON
demo = gr.Interface(
  fn=analisar_fuga_bci,
  inputs=gr.Textbox(
    label="Colar emails BCI aqui (1 por linha) ou deixar vazio para usar démo 20 emails",
    lines=8,
    placeholder="Cole aqui os emails 'quero fechar conta'..."
  ),
  outputs=[
    gr.Plot(label="Gráfico para Director BCI"),
    gr.Textbox(label="Relatório + Recomendação + ROI", lines=15)
  ],
  title="BCI - Detector Fuga Clientes",
  description="Clique 'Submit'. IA analisa em 2s e diz porque clientes fogem + quanto BCI perde. 100% tablet.",
  submit_btn="Analisar Agora",
  clear_btn="Limpar"
)

# 6. LANCER INTERFACE
demo.launch(share=True, debug=False)
