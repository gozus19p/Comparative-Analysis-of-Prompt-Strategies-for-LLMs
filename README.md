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
- Definire cluster per famiglia di modelli, mantenendo focus sulle versioni più recenti:
    - 🦙 Meta – llama3.1:8b-instruct-q3_K_L -> Transformer decoder-only
    - 🧠 DeepSeek - deepseek-r1:8b -> Mixture-of-Experts (MoE)
    - 🔍 Google - Gemma 3 4B ->  Transformer decoder-only
    - 🐉 Alibaba – Qwen3:7B-Instruct → Transformer decoder-only
- Aggiungere un quarto task NLP (traduzione)
- calcolare quanto variano i risultati aggiungendo task NLP


# NOTE:
- Il file per la generazione della traduzione è stato testato su un'altra repo, (se necessario costruire chiave API per TEST), dataset generato e inserito in resources
