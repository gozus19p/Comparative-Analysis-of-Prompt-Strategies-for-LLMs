# import pandas as pd
# from openai import OpenAI
# import time
# import json
# from typing import Dict, Any
# import os
# from tqdm import tqdm
# import logging
#
# # Configuration
# INPUT_CSV_PATH = "IMDB Dataset 500 Sampled With Translate.csv"
# OUTPUT_CSV_PATH = "IMDB Dataset 500 Sampled With Translate Emotion Topic.csv"

#
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
# # Deterministic categories
# EMOTION_CATEGORIES = [
#     "joy",
#     "anger",
#     "sadness",
#     "disgust",
#     "neutral"
# ]
#
# TOPIC_CATEGORIES = [
#     "action",
#     "comedy",
#     "drama",
#     "horror",
#     "thriller",
#     "romance",
#     "sci-fi",
#     "fantasy",
#     "documentary",
#     "other"
# ]
#
#
# def initialize_openai():
#     """Initialize OpenAI client with API key validation."""
#     global client
#
#     if not OPENAI_API_KEY:
#         raise ValueError("OPENAI_API_KEY environment variable not found")
#
#     client = OpenAI(api_key=OPENAI_API_KEY)
#     logger.info("OpenAI client initialized successfully")
#
#
# def create_classification_prompt(review_text: str) -> str:
#     """Generate classification prompt with strict category enforcement."""
#     emotions_str = ", ".join(EMOTION_CATEGORIES)
#     topics_str = ", ".join(TOPIC_CATEGORIES)
#
#     prompt = f"""
# Analyze the following movie review and provide mandatory classification for emotions and genre.
#
# REVIEW:
# {review_text}
#
# STRICT INSTRUCTIONS:
# 1. EMOTION CLASSIFICATION: Choose EXACTLY ONE from: {emotions_str}
# 2. TOPIC CLASSIFICATION: Choose EXACTLY ONE from: {topics_str}
#
# DETERMINISTIC RULES:
# - No custom categories allowed
# - No synonyms or variations permitted
# - Must select a category even if uncertain
# - Use "other" for unclear genre, "neutral" for unclear emotion
#
# REQUIRED JSON FORMAT:
# {{
#     "emotion": "EXACT_EMOTION_CATEGORY",
#     "topic": "EXACT_TOPIC_CATEGORY"
# }}
# """
#     return prompt
#
#
# def classify_review(review_text: str) -> Dict[str, str]:
#     """Classify a single review using OpenAI API with error handling."""
#     global client
#
#     prompt = create_classification_prompt(review_text)
#
#     for attempt in range(MAX_RETRIES):
#         try:
#             response = client.chat.completions.create(
#                 model=MODEL,
#                 messages=[
#                     {"role": "system",
#                      "content": "You are an expert movie review analyst. Respond only with valid JSON."},
#                     {"role": "user", "content": prompt}
#                 ],
#                 max_tokens=100,
#                 temperature=TEMPERATURE
#             )
#
#             content = response.choices[0].message.content.strip()
#
#             try:
#                 result = json.loads(content)
#
#                 emotion = result.get("emotion", "").lower().strip()
#                 topic = result.get("topic", "").lower().strip()
#
#                 if emotion not in EMOTION_CATEGORIES:
#                     logger.warning(f"Invalid emotion '{emotion}', defaulting to 'neutral'")
#                     emotion = "neutral"
#                 if topic not in TOPIC_CATEGORIES:
#                     logger.warning(f"Invalid topic '{topic}', defaulting to 'other'")
#                     topic = "other"
#
#                 return {"emotion": emotion, "topic": topic}
#
#             except json.JSONDecodeError:
#                 logger.warning(f"JSON parsing error (attempt {attempt + 1}): {content}")
#                 if attempt == MAX_RETRIES - 1:
#                     return {"emotion": "neutral", "topic": "other"}
#
#         except Exception as e:
#             logger.error(f"OpenAI API error (attempt {attempt + 1}): {str(e)}")
#             if attempt == MAX_RETRIES - 1:
#                 return {"emotion": "neutral", "topic": "other"}
#
#         time.sleep(RETRY_DELAY)
#
#     return {"emotion": "neutral", "topic": "other"}
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
#     """Process the complete dataset with OpenAI classification."""
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
#     df['emotion_classification'] = ''
#     df['topic_classification'] = ''
#
#     logger.info(f"Starting classification process")
#     logger.info(f"Model: {MODEL}")
#     logger.info(f"Emotion categories: {len(EMOTION_CATEGORIES)}")
#     logger.info(f"Topic categories: {len(TOPIC_CATEGORIES)}")
#
#     for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing reviews"):
#         review_text = str(row['review'])
#
#         if len(review_text.strip()) < 10:
#             df.at[index, 'emotion_classification'] = 'neutral'
#             df.at[index, 'topic_classification'] = 'other'
#         else:
#             classification = classify_review(review_text)
#             df.at[index, 'emotion_classification'] = classification['emotion']
#             df.at[index, 'topic_classification'] = classification['topic']
#
#         if (index + 1) % 10 == 0:
#             df_temp = reorder_columns(df.copy())
#             df_temp.to_csv(output_path, index=False)
#             logger.info(f"Checkpoint saved: {index + 1}/{len(df)} rows processed")
#
#         time.sleep(0.5)
#
#     df = reorder_columns(df)
#     df.to_csv(output_path, index=False)
#     logger.info(f"Classification complete. Output saved to: {output_path}")
#
#     print("\nFINAL STATISTICS:")
#     print("Emotion Distribution:")
#     print(df['emotion_classification'].value_counts())
#     print("\nTopic Distribution:")
#     print(df['topic_classification'].value_counts())
#
#
# def main():
#     """Main execution function."""
#     print("Movie Review Classifier - OpenAI Integration")
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
#     """Test classification on a single review."""
#     initialize_openai()
#     result = classify_review(review_text)
#     print(f"Review: {review_text[:100]}...")
#     print(f"Emotion: {result['emotion']}")
#     print(f"Topic: {result['topic']}")
#
#
# if __name__ == "__main__":
#     main()