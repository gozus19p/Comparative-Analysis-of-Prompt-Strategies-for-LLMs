# LLM Benchmark

| Modello     | Stato      | Data di ultimo aggiornamento |
|-------------|------------|------------------------------|
| LLama3 8b   | Completato | 4 agosto 2024                |
| Phi3 Medium | In corso   | 1 agosto 2024                |
| Qwen2       | In coda    |                              |
| Gemma2      | In coda    |                              |
| Mistral 7B  | In coda    | 5 agosto 2024                |



---

## Ambiente di sviluppo

### Prerequisiti

> Utilizzare la versione 3.10 di Python.

### Configurazione

Per configurare l'ambiente virutale usiamo `venv` e `pip`, variante molto più semplice di Poetry.

```shell
#!/bin/bash

# Creo l'ambiente virtuale localmente
python -m venv .venv/

# Attivo l'ambiente virtuale (per disattivare, lanciare il comando `deactivate`)
source .venv/bin/activate

# Installo le dipendenze
pip install -r requirements.txt
```

Conseguentemente, configuare l'interprete Python per puntare al binario posto sotto `./venv/bin/python3`.

---

## Stesura dei notebook

### Dichiarazione delle dipendenze

Nella prima cella, riportare per esteso i requisiti da installare con la sintassi seguente:

```jupyter
!pip install requisito1 requisito2 ...
```

Questo garantisce l'interoperabilità e l'atomicità del notebook.

> Il file `requirements.txt` posto sotto la root di progetto deve comunque rimanere allineato, così da mettere a
> disposizione un ambiente virtuale compatibile con tutti i notebook.

### Dataset

I dataset devono risiedere sotto `resources/`, ma essendo parecchio pesanti in termini di byte non vanno committati.

> Fare attenzione alla nomenclatura usata nel .gitignore.
