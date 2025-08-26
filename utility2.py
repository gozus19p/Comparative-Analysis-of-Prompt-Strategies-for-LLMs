# import pandas as pd
# from openai import OpenAI
# import time
# import json
# from typing import Dict, Any, List
# import os
# from tqdm import tqdm
# import logging
#
# # Configuration
# INPUT_CSV_PATH = "IMDB Dataset 500 Sampled With Translate Emotion Topic2.csv"
# OUTPUT_CSV_PATH = "resources/IMDB Dataset 500 Sampled With Translate Emotion Topic Updated.csv"
#
# # Add your OpenAI API key here
# # Model settings
# MODEL = "gpt-4"
# MAX_RETRIES = 3
# RETRY_DELAY = 1
# TEMPERATURE = 0.1
#
# # Initialize logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)
#
# # Global client
# client = None
#
# # NER Categories
# NER_CATEGORIES = ["PERSON", "ORG", "LOC"]
#
#
#
# def initialize_openai():
#     """Initialize OpenAI client with API key validation."""
#     global client
#
#     if not OPENAI_API_KEY or OPENAI_API_KEY == "your-api-key-here":
#         raise ValueError("Please set your OPENAI_API_KEY in the script")
#
#     client = OpenAI(api_key=OPENAI_API_KEY)
#     logger.info("OpenAI client initialized successfully")
#
#
# def create_ner_prompt(review_text: str) -> str:
#     """Generate NER prompt for entity extraction."""
#     prompt = f"""
# List all named entities present in the text, categorizing them by label (PERSON, ORG, LOC).
#
# TEXT:
# {review_text}
#
# INSTRUCTIONS:
# - PERSON: Names of people including actors, directors, characters, real people, full names or recognizable single names
# - ORG: Organizations, companies, institutions, brands, titles of movies/shows/books
# - LOC: Geographic locations, places, countries, cities, specific venues
#
# Extract all clear named entities that fit these categories. Include both real and fictional entities.
#
# REQUIRED JSON FORMAT:
# [
#     {{"label": "PERSON", "value": "entity_name"}},
#     {{"label": "ORG", "value": "entity_name"}},
#     {{"label": "LOC", "value": "entity_name"}}
# ]
# """
#     return prompt
#
#
# def extract_entities(review_text: str) -> List[Dict[str, str]]:
#     """Extract named entities from review using OpenAI API."""
#     global client
#
#     prompt = create_ner_prompt(review_text)
#
#     for attempt in range(MAX_RETRIES):
#         try:
#             response = client.chat.completions.create(
#                 model=MODEL,
#                 messages=[
#                     {"role": "system",
#                      "content": "You are an expert named entity recognition system. Respond only with valid JSON array."},
#                     {"role": "user", "content": prompt}
#                 ],
#                 max_tokens=600,
#                 temperature=TEMPERATURE
#             )
#
#             content = response.choices[0].message.content.strip()
#
#             try:
#                 entities = json.loads(content)
#
#                 # Validate and filter entities
#                 valid_entities = []
#                 if isinstance(entities, list):
#                     for entity in entities:
#                         if isinstance(entity, dict) and "label" in entity and "value" in entity:
#                             label = entity["label"].upper().strip()
#                             value = entity["value"].strip()
#
#                             if label in NER_CATEGORIES and len(value) > 0:
#                                 valid_entities.append({"label": label, "value": value})
#
#                 return valid_entities
#
#             except json.JSONDecodeError:
#                 logger.warning(f"JSON parsing error (attempt {attempt + 1}): {content}")
#                 if attempt == MAX_RETRIES - 1:
#                     return []
#
#         except Exception as e:
#             logger.error(f"OpenAI API error (attempt {attempt + 1}): {str(e)}")
#             if attempt == MAX_RETRIES - 1:
#                 return []
#
#         time.sleep(RETRY_DELAY)
#
#     return []
#
#
# def update_json_column(row: pd.Series, new_entities: List[Dict[str, str]]) -> str:
#     """Update the JSON column with new entities."""
#     try:
#         # Try to parse existing JSON
#         if pd.isna(row['json']) or row['json'] == '':
#             json_data = {
#                 "review": row['review'],
#                 "sentiment": row['sentiment'],
#                 "entities": new_entities
#             }
#         else:
#             json_data = json.loads(row['json'])
#             json_data["entities"] = new_entities
#
#         return json.dumps(json_data)
#
#     except json.JSONDecodeError:
#         # If JSON parsing fails, create new JSON
#         json_data = {
#             "review": row['review'],
#             "sentiment": row['sentiment'],
#             "entities": new_entities
#         }
#         return json.dumps(json_data)
#
#
# def reorder_columns(df: pd.DataFrame) -> pd.DataFrame:
#     """Reorder columns to place progressive_index at the end."""
#     columns = df.columns.tolist()
#     if 'progressive_index' in columns:
#         columns.remove('progressive_index')
#         columns.append('progressive_index')
#         return df[columns]
#     return df
#
#
# def process_dataset(input_path: str, output_path: str):
#     """Process the complete dataset with NER extraction."""
#     logger.info(f"Loading dataset from: {input_path}")
#
#     try:
#         df = pd.read_csv(input_path)
#         logger.info(f"Dataset loaded successfully: {len(df)} rows")
#     except FileNotFoundError:
#         logger.error(f"Input file not found: {input_path}")
#         return
#     except Exception as e:
#         logger.error(f"Error loading dataset: {str(e)}")
#         return
#
#     if 'review' not in df.columns:
#         logger.error("Column 'review' not found in dataset")
#         return
#
#     logger.info(f"Starting NER processing")
#     logger.info(f"Model: {MODEL}")
#     logger.info(f"NER categories: {NER_CATEGORIES}")
#
#     total_entities_found = 0
#
#     for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing NER"):
#         review_text = str(row['review'])
#
#         if len(review_text.strip()) < 10:
#             # For very short reviews, set empty entities
#             new_entities = []
#         else:
#             # Extract entities using GPT-4
#             new_entities = extract_entities(review_text)
#             total_entities_found += len(new_entities)
#
#         # Update entities column (as JSON string to match existing format)
#         df.at[index, 'entities'] = json.dumps(new_entities)
#
#         # Update JSON column
#         df.at[index, 'json'] = update_json_column(row, new_entities)
#
#         # Save checkpoint every 10 rows
#         if (index + 1) % 10 == 0:
#             df_temp = reorder_columns(df.copy())
#             df_temp.to_csv(output_path, index=False)
#             logger.info(f"Checkpoint saved: {index + 1}/{len(df)} rows processed")
#
#         # Small delay to avoid rate limits
#         time.sleep(0.5)
#
#     # Final save
#     df = reorder_columns(df)
#     df.to_csv(output_path, index=False)
#     logger.info(f"NER processing complete. Output saved to: {output_path}")
#
#     print("\nFINAL STATISTICS:")
#     print(f"Total entities found: {total_entities_found}")
#     print(f"Average entities per review: {total_entities_found / len(df):.2f}")
#
#     # Count entities by type
#     entity_counts = {"PERSON": 0, "ORG": 0, "LOC": 0}
#     for index, row in df.iterrows():
#         try:
#             entities = json.loads(row['entities'])
#             for entity in entities:
#                 if entity['label'] in entity_counts:
#                     entity_counts[entity['label']] += 1
#         except:
#             continue
#
#     print("\nEntity Distribution:")
#     for label, count in entity_counts.items():
#         print(f"{label}: {count}")
#
#
# def main():
#     """Main execution function."""
#     print("IMDB Dataset NER Processor - OpenAI Integration")
#     print("=" * 50)
#
#     try:
#         initialize_openai()
#
#         if not os.path.exists(INPUT_CSV_PATH):
#             logger.error(f"Input file not found: {INPUT_CSV_PATH}")
#             print(f"Please update INPUT_CSV_PATH variable with correct file path")
#             return
#
#         process_dataset(INPUT_CSV_PATH, OUTPUT_CSV_PATH)
#
#     except Exception as e:
#         logger.error(f"Critical error: {str(e)}")
#
#
# def test_single_review(review_text: str):
#     """Test NER extraction on a single review."""
#     initialize_openai()
#     entities = extract_entities(review_text)
#     print(f"Review: {review_text[:100]}...")
#     print(f"Entities found: {len(entities)}")
#     for entity in entities:
#         print(f"  - {entity['label']}: {entity['value']}")
#
#
# if __name__ == "__main__":
#     main()