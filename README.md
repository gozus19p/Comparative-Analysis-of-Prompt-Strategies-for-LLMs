# Comparative-Analysis-of-Prompt-Strategies-for-LLMs
## v2.0.0

## SCOPO:
In questa nuova versione, ci proponiamo di migliorare significativamente il nostro precedente lavoro, approfondendo l'analisi delle performance dei Large Language Models in contesti single-task e multi-task.
L'obiettivo principale è comprendere e documentare le ragioni fondamentali per cui determinati modelli di grandi dimensioni possano eccellere in uno scenario piuttosto che nell'altro, manterremo l'approccio metodologico della versione precedente utilizzando Ollama come framework di riferimento, ma espanderemo l'analisi includendo un confronto sistematico tra diverse famiglie architetturali di modelli, questo ci permetterà di valutare l'impatto dell'architettura sottostante sulle performance nei diversi contesti operativi.
Per quanto riguarda il dataset utilizzeremo sempre lo stesso (IMDB), ampliando però il ventaglio di task NLP con l'introduzione di un quarto compito (ancora da decidere)

## AS IS
- modelli analizzati: LLama 3.1 8B, Qwen2 7B, Mistral 7B, Phi3 Medium, Gemma2 9B
- Task NLP attuali: sentiment analysis, named entity recognition (NER), formattazione JSON
- Metodologia di valutazione: combinazione di metriche (F1 per NER, exact match per sentiment, BLEU per review)
- Risultati: non esiste una regola definitiva che favorisca i prompt single-task rispetto ai multi-task

## TO DO:
- strutturato DATASET con 500 osservazioni
- implementare un sistema di valutazione per definire se le distribuzioni non sono statisticamente diverse tra il dataset con 1000 osservazioni e quello con 500
- Definire cluster per famiglia di modelli, mantenendo focus sulle versioni più recenti:
    - 🦙 Meta – llama3.1:8b-instruct-q3_K_L -> Transformer decoder-only
    - 🧠 DeepSeek - deepseek-r1:8b -> Mixture-of-Experts (MoE)
    - 🧠 DeepSeek - deepseek-r1:7b -> Mixture-of-Experts (MoE)
    - 🔍 Google - Gemma 3 4B ->  Transformer decoder-only
    - 🐉 Alibaba – Qwen3:4B-Instruct → Transformer decoder-only
- Aggiungere un quarto task NLP (traduzione)
- calcolare quanto variano i risultati aggiungendo task NLP


# NOTE:
- Il file per la generazione della traduzione è stato testato su un'altra repo, (se necessario costruire chiave API per TEST), dataset generato e inserito in resources


---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# V2
## Validazione dei Dati

- **Completare la validazione** dei dati sul **campione di 500** elementi.
- Attenzione: l'aggiunta del **task di traduzione** può causare una **degradazione della qualità dell'output**.
- Valutare l’impatto della traduzione sulle performance generali.

## Output per Famiglie

- Strutturare l’**output finale** per **famiglie di dati o categorie**.
- Organizzazione logica dei risultati per una migliore leggibilità e analisi.


----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Distribuzione con Top-p e Temperatura

- Se **non si considera solo il token più probabile**, ma si imposta:
  - `top-p = 1`
  - `temperatura = 0`
- Si ottiene una **distribuzione di probabilità molto concentrata** sui token più probabili.
- In questo scenario, la **differenza tra il primo e il secondo token** diventa **poco significativa**.

## Calcolo Escludendo il Primo Token

- Se si sceglie di **non calcolare il logit sul primo token**:
  - Escludere il primo token dalla sequenza.
  - Analizzare i **tre token successivi**.
  - Calcolare la **differenza media dei logit** sui token successivi.
  - Considerare la **media complementare a 1**:
    - `1 - media`

## Distribuzione Ponderata

- Assegnare al **primo token** un **peso del 80%**.
- Sottrarre questo valore dal totale (100%).
- Redistribuire il restante 20% tra gli altri token.
- **Scalare i logit** dei token successivi in modo proporzionale.

## Obiettivo

- Ottenere una **distribuzione di probabilità coerente**, utile per analizzare la **qualità dei token generati**.
