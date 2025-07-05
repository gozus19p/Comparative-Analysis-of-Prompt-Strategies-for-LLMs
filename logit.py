# import torch
# import torch.nn.functional as F
# from transformers import AutoTokenizer, AutoModelForCausalLM
# import numpy as np
# import matplotlib.pyplot as plt
#
#
# class AdvancedConfidenceAnalyzer:
#     def __init__(self, model_name="gpt2"):
#         self.tokenizer = AutoTokenizer.from_pretrained(model_name)
#         self.model = AutoModelForCausalLM.from_pretrained(model_name)
#         self.model.eval()
#
#     def get_confidence_metrics(self, prompt, max_tokens=10):
#         """
#         Calcola multiple metriche di confidence
#         """
#         inputs = self.tokenizer(prompt, return_tensors="pt")
#         input_ids = inputs["input_ids"]
#
#         metrics = {
#             'tokens': [],
#             'logit_gaps': [],
#             'entropy': [],
#             'top1_prob': [],
#             'top3_prob_mass': [],
#             'calibrated_confidence': []
#         }
#
#         with torch.no_grad():
#             for _ in range(max_tokens):
#                 outputs = self.model(input_ids)
#                 logits = outputs.logits[0, -1, :]
#
#                 # Softmax per probabilità
#                 probs = F.softmax(logits, dim=-1)
#
#                 # Top-k logit e probabilità
#                 top_logits, top_indices = torch.topk(logits, k=10)
#                 top_probs = probs[top_indices]
#
#                 # Metriche diverse
#                 # 1. Gap tra top-2 logit
#                 logit_gap = (top_logits[0] - top_logits[1]).item()
#
#                 # 2. Entropy (incertezza)
#                 entropy = -torch.sum(probs * torch.log(probs + 1e-10)).item()
#
#                 # 3. Probabilità del token più probabile
#                 top1_prob = top_probs[0].item()
#
#                 # 4. Massa di probabilità sui top-3
#                 top3_mass = torch.sum(top_probs[:3]).item()
#
#                 # 5. Confidence calibrata (differenza top-2 probabilità)
#                 calibrated_conf = (top_probs[0] - top_probs[1]).item()
#
#                 # Salva metriche
#                 next_token = top_indices[0].item()
#                 token_str = self.tokenizer.decode([next_token])
#
#                 metrics['tokens'].append(token_str)
#                 metrics['logit_gaps'].append(logit_gap)
#                 metrics['entropy'].append(entropy)
#                 metrics['top1_prob'].append(top1_prob)
#                 metrics['top3_prob_mass'].append(top3_mass)
#                 metrics['calibrated_confidence'].append(calibrated_conf)
#
#                 # Aggiorna input per prossimo token
#                 input_ids = torch.cat([input_ids, torch.tensor([[next_token]])], dim=1)
#
#                 if next_token == self.tokenizer.eos_token_id:
#                     break
#
#         return metrics
#
#     def compare_confidence_vs_correctness(self):
#         """
#         Confronta confidence con correttezza su task specifici
#         """
#         # Task con risposta nota
#         test_cases = [
#             # Matematica semplice
#             ("2 + 2 =", " 4", "math"),
#             ("5 * 3 =", " 15", "math"),
#             ("10 - 7 =", " 3", "math"),
#
#             # Fatti geografici
#             ("The capital of France is", " Paris", "geography"),
#             ("The capital of Italy is", " Rome", "geography"),
#             ("The capital of Germany is", " Berlin", "geography"),
#
#             # Completamenti ovvi
#             ("The sun rises in the", " east", "common_knowledge"),
#             ("Ice melts at", " zero", "common_knowledge"),
#             ("There are 24 hours in a", " day", "common_knowledge"),
#         ]
#
#         results = []
#
#         for prompt, expected, category in test_cases:
#             metrics = self.get_confidence_metrics(prompt, max_tokens=3)
#
#             # Controlla se primo token è corretto (VERSIONE CORRETTA)
#             first_token = metrics['tokens'][0] if metrics['tokens'] else ""
#
#             # Confronto esatto (non substring matching)
#             expected_clean = expected.strip().lower()
#             generated_clean = first_token.strip().lower()
#             is_correct = expected_clean == generated_clean
#
#             # Debug: mostra il confronto
#             print(
#                 f"DEBUG: Expected='{expected}' | Generated='{first_token}' | Clean comparison: '{expected_clean}' == '{generated_clean}' → {is_correct}")
#
#             result = {
#                 'prompt': prompt,
#                 'expected': expected,
#                 'generated': first_token,
#                 'correct': is_correct,
#                 'category': category,
#                 'confidence': metrics['calibrated_confidence'][0] if metrics['calibrated_confidence'] else 0,
#                 'entropy': metrics['entropy'][0] if metrics['entropy'] else 0,
#                 'top1_prob': metrics['top1_prob'][0] if metrics['top1_prob'] else 0,
#                 'logit_gap': metrics['logit_gaps'][0] if metrics['logit_gaps'] else 0
#             }
#
#             results.append(result)
#
#             print(f"Prompt: {prompt}")
#             print(f"Expected: {expected} | Generated: {first_token} | Correct: {is_correct}")
#             print(f"Confidence: {result['confidence']:.3f} | Entropy: {result['entropy']:.3f}")
#             print(f"Top1 Prob: {result['top1_prob']:.3f} | Logit Gap: {result['logit_gap']:.3f}")
#             print("-" * 50)
#
#         return results
#
#     def analyze_confidence_patterns(self, results):
#         """
#         Analizza pattern tra confidence e correttezza
#         """
#         correct_results = [r for r in results if r['correct']]
#         incorrect_results = [r for r in results if not r['correct']]
#
#         print("=" * 60)
#         print("ANALISI CONFIDENCE vs CORRETTEZZA (VERSIONE CORRETTA)")
#         print("=" * 60)
#
#         print(f"TOTALE RISPOSTE TESTATE: {len(results)}")
#         print(f"RISPOSTE CORRETTE: {len(correct_results)}")
#         print(f"RISPOSTE SBAGLIATE: {len(incorrect_results)}")
#         print(f"ACCURACY COMPLESSIVA: {len(correct_results) / len(results) * 100:.1f}%")
#         print()
#
#         if correct_results:
#             print(f"RISPOSTE CORRETTE (n={len(correct_results)}):")
#             print(f"  Confidence media: {np.mean([r['confidence'] for r in correct_results]):.3f}")
#             print(f"  Entropy media: {np.mean([r['entropy'] for r in correct_results]):.3f}")
#             print(f"  Top1 Prob media: {np.mean([r['top1_prob'] for r in correct_results]):.3f}")
#
#         if incorrect_results:
#             print(f"RISPOSTE SBAGLIATE (n={len(incorrect_results)}):")
#             print(f"  Confidence media: {np.mean([r['confidence'] for r in incorrect_results]):.3f}")
#             print(f"  Entropy media: {np.mean([r['entropy'] for r in incorrect_results]):.3f}")
#             print(f"  Top1 Prob media: {np.mean([r['top1_prob'] for r in incorrect_results]):.3f}")
#
#         # Analisi per categoria con accuracy dettagliata
#         categories = set(r['category'] for r in results)
#         print(f"ANALISI DETTAGLIATA PER CATEGORIA:")
#         for cat in categories:
#             cat_results = [r for r in results if r['category'] == cat]
#             correct_in_cat = [r for r in cat_results if r['correct']]
#             accuracy = len(correct_in_cat) / len(cat_results) if cat_results else 0
#             avg_confidence = np.mean([r['confidence'] for r in cat_results])
#
#             print(f"  📁 {cat.upper()}:")
#             print(f"     • Accuracy: {accuracy:.2f} ({len(correct_in_cat)}/{len(cat_results)})")
#             print(f"     • Avg Confidence: {avg_confidence:.3f}")
#
#             # Mostra esempi per categoria
#             print(f"     • Esempi:")
#             for r in cat_results[:2]:  # Prime 2 per categoria
#                 status = "✅" if r['correct'] else "❌"
#                 print(f"       {status} '{r['prompt']}' → '{r['generated']}' (conf: {r['confidence']:.3f})")
#             print()
#
#         return {
#             'correct_confidence': [r['confidence'] for r in correct_results],
#             'incorrect_confidence': [r['confidence'] for r in incorrect_results],
#             'correct_entropy': [r['entropy'] for r in correct_results],
#             'incorrect_entropy': [r['entropy'] for r in incorrect_results],
#             'total_accuracy': len(correct_results) / len(results) if results else 0,
#             'overconfidence_score': np.mean([r['confidence'] for r in incorrect_results]) - np.mean(
#                 [r['confidence'] for r in correct_results]) if correct_results and incorrect_results else 0
#         }
#
#
# # Esegui analisi avanzata
# if __name__ == "__main__":
#     analyzer = AdvancedConfidenceAnalyzer()
#
#     # Confronta confidence vs correttezza
#     results = analyzer.compare_confidence_vs_correctness()
#
#     # Analizza pattern
#     patterns = analyzer.analyze_confidence_patterns(results)
#
#     # Stampa summary finale
#     print("🎯 SUMMARY FINALE:")
#     print(f"   • Accuracy totale: {patterns['total_accuracy'] * 100:.1f}%")
#     print(f"   • Overconfidence score: {patterns['overconfidence_score']:.3f}")
#     if patterns['overconfidence_score'] > 0:
#         print("   • ⚠️  MODELLO OVERCONFIDENT: più sicuro quando sbaglia!")
#     else:
#         print("   • ✅ Modello ben calibrato")
#     print()
#
#     # Esempio di analisi dettagliata su un caso specifico
#     print("\n" + "=" * 60)
#     print("ANALISI DETTAGLIATA: '2 + 2 ='")
#     print("=" * 60)
#
#     detailed_metrics = analyzer.get_confidence_metrics("2 + 2 =", max_tokens=5)
#
#     print("Token-by-token breakdown:")
#     for i, (token, conf, entropy, top1, gap) in enumerate(zip(
#             detailed_metrics['tokens'],
#             detailed_metrics['calibrated_confidence'],
#             detailed_metrics['entropy'],
#             detailed_metrics['top1_prob'],
#             detailed_metrics['logit_gaps']
#     )):
#         print(f"Token {i + 1}: '{token}'")
#         print(f"  Confidence: {conf:.3f}")
#         print(f"  Entropy: {entropy:.3f}")
#         print(f"  Top1 Prob: {top1:.3f}")
#         print(f"  Logit Gap: {gap:.3f}")
#         print()

import torch
from matplotlib import pyplot as plt
from transformers import AutoTokenizer, AutoModelForCausalLM

# MODELLO DI BASE (puoi cambiarlo in 'EleutherAI/gpt-neo-1.3B', 'gpt2-xl', ecc.)
model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
model.eval()

# Aggiungi padding token se non presente
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token


def compute_token_confidence(logits, top_k=3):
    """
    Calcola la differenza media tra il primo logit e i successivi top-k
    Restituisce anche i top-k token con i loro logits
    """
    # Ordina i logit in ordine decrescente
    top_logits, top_indices = torch.topk(logits, top_k, dim=-1)
    diffs = top_logits[:, 0].unsqueeze(1) - top_logits[:, 1:]
    mean_diff = diffs.mean(dim=-1)

    # Normalizzazione opzionale: sigmoid per portarlo tra 0 e 1
    confidence_score = torch.sigmoid(mean_diff)

    return confidence_score, top_logits, top_indices


def generate_with_confidence(prompt, max_new_tokens=20):
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    generated_ids = input_ids.clone()
    all_confidences = []
    all_top_tokens = []  # Lista per salvare i top-k token di ogni step

    for _ in range(max_new_tokens):
        with torch.no_grad():
            outputs = model(generated_ids)
            logits = outputs.logits[:, -1, :]  # Solo ultimi logit (token corrente)
            confidence, top_logits, top_indices = compute_token_confidence(logits)

            all_confidences.append(confidence.item())

            # Salva i top-k token con i loro logits
            top_tokens_info = []
            for i in range(top_logits.shape[1]):
                token_id = top_indices[0, i].item()
                token_text = tokenizer.decode(token_id)
                logit_value = top_logits[0, i].item()
                top_tokens_info.append({
                    'token': token_text,
                    'logit': logit_value,
                    'token_id': token_id
                })
            all_top_tokens.append(top_tokens_info)

            # Forzare greedy decoding
            next_token = torch.argmax(logits, dim=-1)
            generated_ids = torch.cat([generated_ids, next_token.unsqueeze(-1)], dim=-1)

    generated_text = tokenizer.decode(generated_ids[0])
    return generated_text, all_confidences, all_top_tokens


def plot_confidence(text, confidences, tokenizer):
    # Tokenizza solo la parte generata (escludendo il prompt originale)
    tokens = tokenizer.tokenize(text)

    # Assicurati che il numero di token corrisponda al numero di confidenze
    if len(tokens) > len(confidences):
        # Prendi solo i token generati (gli ultimi len(confidences) token)
        tokens = tokens[-len(confidences):]
    elif len(confidences) > len(tokens):
        # Tronca le confidenze se sono troppe
        confidences = confidences[:len(tokens)]

    plt.figure(figsize=(12, 4))
    plt.plot(confidences, marker='o')
    plt.xticks(range(len(tokens)), tokens, rotation=45, ha='right')
    plt.ylim(0, 1.05)
    plt.ylabel("Confidence")
    plt.title("Confidence per token generato")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def analyze_prompt_confidence(prompt, max_new_tokens=20, show_plot=True, show_alternatives=True):
    """
    Funzione principale per analizzare la confidence di un prompt
    """
    print(f"🔹 Prompt: {prompt}")
    text, confidences, top_tokens = generate_with_confidence(prompt, max_new_tokens)

    # Estrai solo la parte generata (dopo il prompt)
    generated_part = text[len(prompt):]

    print(f"📝 Output generato: {generated_part}")
    print(f"✅ Confidence media: {sum(confidences) / len(confidences):.3f}")
    print(f"📊 Confidence min/max: {min(confidences):.3f} / {max(confidences):.3f}")

    if show_alternatives:
        print("\n🔄 Top-3 alternative per ogni token:")
        print("=" * 80)
        for i, (conf, alternatives) in enumerate(zip(confidences, top_tokens)):
            chosen = alternatives[0]['token']
            alt1 = alternatives[1]['token'] if len(alternatives) > 1 else "N/A"
            alt2 = alternatives[2]['token'] if len(alternatives) > 2 else "N/A"

            print(f"Step {i + 1:2d} | Conf: {conf:.3f} | "
                  f"Scelto: '{chosen}' ({alternatives[0]['logit']:.2f}) | "
                  f"Alt1: '{alt1}' ({alternatives[1]['logit']:.2f}) | "
                  f"Alt2: '{alt2}' ({alternatives[2]['logit']:.2f})")

    if show_plot:
        plot_confidence(generated_part, confidences, tokenizer)

    print("-" * 80)
    return text, confidences, top_tokens


# ESEMPIO DI UTILIZZO
if __name__ == "__main__":
    prompts = [
        "The meaning of life is",
        "Explain quantum mechanics in simple terms.",
        "What is the capital of France?",
        "Write a Python function to sort a list."
    ]

    # Mostra i dettagli completi per tutti i prompt
    for i, prompt in enumerate(prompts):
        print(f"\n{'=' * 80}")
        print(f"PROMPT {i + 1}/{len(prompts)}")
        print(f"{'=' * 80}")
        analyze_prompt_confidence(prompt, max_new_tokens=15, show_plot=False, show_alternatives=True)

    # Esempio aggiuntivo con grafico
    print(f"\n{'=' * 80}")
    print("ESEMPIO AGGIUNTIVO CON GRAFICO:")
    print(f"{'=' * 80}")
    analyze_prompt_confidence("The weather today is", max_new_tokens=8, show_plot=True, show_alternatives=True)



