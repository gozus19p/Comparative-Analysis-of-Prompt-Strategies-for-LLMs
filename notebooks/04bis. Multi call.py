#!/usr/bin/env python
# coding: utf-8

# In[1]:



# In[2]:


NER_PROMPT = """Analyze the following review text listing all named entities present in the text, categorizing them by label. Consider only PERSON, ORG, and LOC categories.
Ensure the response is formatted in JSON according to the following schema:

[
  {{
    "label": "<label>",
    "value": "<value>"
  }}
]

Example:

"I recently visited the restaurant 'La Dolce Vita' in Rome and was thrilled with the service and food. The waiter, Marco, was exceptionally friendly and the truffle risotto was simply divine. I can't wait to return and recommend this place to my friends."

[
  {{
    "label": "ORG",
    "value": "La Dolce Vita"
  }},
  {{
    "label": "LOC",
    "value": "Rome"
  }},
  {{
    "label": "PERSON",
    "value": "Marco"
  }}
]

{content}"""

SENTIMENT_PROMPT = """Analyze the following review text indicating whether the sentiment of the review is "positive" or "negative".

Example:

"I recently visited the restaurant 'La Dolce Vita' in Rome and was thrilled with the service and food. The waiter, Marco, was exceptionally friendly and the truffle risotto was simply divine. I can't wait to return and recommend this place to my friends."

"positive"

{content}"""

FORMATTING_OUTPUT = """You are given three informations: sentiment, review and entities. Generate a JSON representation using the following schema. Use just the data you receive:

{{
  "sentiment": "<sentiment>",
  "review": "<review>",
  "entities": [
    {{
      "label": "<label>",
      "value": "<value>"
    }}
  ]
}}

example:

"Sentiment: positive
Review: I recently visited the restaurant 'La Dolce Vita' in Rome and was thrilled with the service and food. The waiter, Marco, was exceptionally friendly and the truffle risotto was simply divine. I can't wait to return and recommend this place to my friends.
Entities: [
    {{
      "label": "ORG",
      "value": "La Dolce Vita"
    }},
    {{
      "label": "LOC",
      "value": "Rome"
    }},
    {{
      "label": "PERSON",
      "value": "Marco"
    }}
  ]"

```json
{{
  "sentiment": "positive",
  "review": "I recently visited the restaurant 'La Dolce Vita' in Rome and was thrilled with the service and food. The waiter, Marco, was exceptionally friendly and the truffle risotto was simply divine. I can't wait to return and recommend this place to my friends.",
  "entities": [
    {{
      "label": "ORG",
      "value": "La Dolce Vita"
    }},
    {{
      "label": "LOC",
      "value": "Rome"
    }},
    {{
      "label": "PERSON",
      "value": "Marco"
    }}
  ]
}}
```


Sentiment: {sentiment}
Review: {review}
Entities: {entities}"""


# In[3]:


import requests

def process_review(review: str, model_name: str) -> str:
    """
    It processes the review text and returns the LLM response as string.
    
    Arguments:
        review (str): The review text.
        
    Return:
        The LLM response as string.
    """
    try:
        sentiment_response: str = requests.post(
            url="http://localhost:11434/api/generate",
            json={
                "model": model_name,
                "prompt": SENTIMENT_PROMPT.format(content=review),
                "stream": False
            }
        ).json()["response"]
    except Exception as e:
        print(f"Error invoking the chain at sentiment stage: {e}")
        return "$$$"

    try:
        ner_response: str = requests.post(
            url="http://localhost:11434/api/generate",
            json={
                "model": model_name,
                "prompt": NER_PROMPT.format(content=review),
                "stream": False
            }
        ).json()["response"]
    except Exception as e:
        print(f"Error invoking the chain at NER stage: {e}")
        return "$$$"
    
    try:
        return requests.post(
            url="http://localhost:11434/api/generate",
            json={
                "model": model_name,
                "prompt": FORMATTING_OUTPUT.format(review=review, sentiment=sentiment_response, entities=ner_response),
                "stream": False
            }
        ).json()["response"]
    except Exception as e:
        print(f"Error invoking the chain at formatting stage: {e}")
        return "$$$"
        
        


# In[4]:


import pandas as pd
from tqdm import tqdm


def call_model_llm(model_name: str, output_file_path: str) -> None:
    """
    It calls the LLM model using Ollama. It returns the sampled dataframe enriched with relevant columns.
    
    Arguments:
        model_name: The name of the model to invoke via Ollama.
    
    Return:
        The enriched dataframe.
    """
    dataframe: pd.DataFrame = pd.read_csv(output_file_path)
    already_done_part: pd.DataFrame = dataframe[~(dataframe.output == "$$$")].copy()
    slice_to_work_on: pd.DataFrame = dataframe[dataframe.output == "$$$"].copy()
    slice_to_work_on.reset_index(inplace=True, drop=True)
    total_rows: int = len(slice_to_work_on)
    for i in tqdm(range(total_rows), total=total_rows):
        row = slice_to_work_on.iloc[i]
        # logging.info(f"Processing row {i + 1} out of {total_rows}")
        result = process_review(row["review"], model_name)
        slice_to_work_on.loc[i, "output"] = result
        updated_df: pd.DataFrame = pd.concat([already_done_part, slice_to_work_on])
        updated_df.to_csv(output_file_path, index=False)


# In[ ]:


import os

# Define the model name to use
MODEL_NAME: str = input("Enter the code of the model: ").strip()

# Define the output path and get the result as csv
base_path: str = os.path.join(os.path.dirname(__file__), "..")
output_file_path: str = f"{base_path}/resources/sampled_reviews_with_output_multicall_{MODEL_NAME.replace(':', '_')}.csv"

exists: bool = os.path.exists(output_file_path)
if not exists:
    sampled: pd.DataFrame = pd.read_csv("../resources/IMDB Dataset Sampled.csv")
    sampled["output"] = sampled.apply(lambda row: "$$$", axis=1)
    sampled.to_csv(output_file_path, index=False)

call_model_llm(model_name=MODEL_NAME, output_file_path=output_file_path)


# In[ ]:




