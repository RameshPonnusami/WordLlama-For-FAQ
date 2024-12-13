import os
import json
import traceback
from wordllama import WordLlama, WordLlamaConfig
import sqlite3
from typing import List, Tuple

class FAQSystem:
    def __init__(self, weights_path='' , 
                        config_path='', db_path='faq_database.db'):
        """
        Initialize the FAQ system with a SQLite database
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_path = db_path
        self.weights_path = weights_path
        self.config_path = config_path
        self.wl = self.detailed_wordllama_load()
        self._create_table()
        self._load_sample_data()

    def detailed_wordllama_load(self, config_name: str = 'l2_supercat'
    ):
        """
        Comprehensive WordLlama model loading with detailed diagnostics
        """
        print("===== WordLlama Model Loading Diagnostics =====")
        weights_path = self.weights_path
        config_path = self.config_path
        # Verify file existence
        print(f"Weights file path: {weights_path}")
        print(f"Config file path: {config_path}")
        
        if not os.path.exists(weights_path):
            raise FileNotFoundError(f"Weights file not found: {weights_path}")
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        # Read and print config file contents
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            print("\nConfig File Contents:")
           # print(json.dumps(config_data, indent=2))
        except Exception as e:
            print(f"Error reading config file: {e}")
            traceback.print_exc()
            return None
        
        # Attempt model loading with different strategies
        try:
            print("\nAttempting to load model...")
            
            # Strategy 1: Direct load with config name
            try:
                model = WordLlama.load(config_name)
                print("Model loaded successfully using config name")
                return model
            except Exception as e:
                print(f"Config name load failed: {e}")
            
            # Strategy 2: Create and register custom config
            try:
                custom_config = WordLlamaConfig(
                    name=config_name,
                    **config_data
                )
                
                # Register the configuration
                WordLlamaConfig.register(custom_config)
                
                # Try loading again
                model = WordLlama.load(config_name)
                print("Model loaded successfully after custom config registration")
                return model
            except Exception as e:
                print(f"Custom config load failed: {e}")
                traceback.print_exc()
            
            # Strategy 3: Explicit weight loading attempt
            raise ValueError("Unable to load model using standard methods")
        
        except Exception as e:
            print(f"Final model loading error: {e}")
            traceback.print_exc()
            return None
            
    def _load_sample_data(self):
        """
        Load sample FAQ data into the database
        """
        sample_faqs = [
            ("How do I reset my password?", "You can reset your password by clicking 'Forgot Password' on the login page."),
            ("What are the shipping costs?", "Shipping is free for orders over $50, otherwise a flat rate of $5 applies."),
            ("Can I return an item?", "Yes, items can be returned within 30 days of purchase with original packaging."),
            ("How long does shipping take?", "Standard shipping takes 3-5 business days."),
            ("Do you offer international shipping?", "We currently ship to the US, Canada, and Mexico."),
            ("What payment methods do you accept?", "We accept Visa, MasterCard, American Express, and PayPal."),
            ("How can I track my order?", "You can track your order using the tracking number sent in your confirmation email."),
            ("Are there any discounts available?", "We offer student and military discounts. Check our website for current promotions."),
            ("What is your privacy policy?", "We do not sell personal data and use encryption to protect your information."),
            ("How do I contact customer support?", "You can reach our support team via email at support@example.com or call 1-800-SUPPORT.")
        ]

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Clear existing data to avoid duplicates
            cursor.execute('DELETE FROM faqs')
            
            # Insert sample FAQs
            cursor.executemany(
                'INSERT INTO faqs (question, answer) VALUES (?, ?)', 
                sample_faqs
            )
            conn.commit()
    def _create_table(self):
        """
        Create FAQ table if it doesn't exist
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS faqs (
                    id INTEGER PRIMARY KEY,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL
                )
            ''')
            conn.commit()
    def search_faqs(self, query: str, top_k: int = 10) -> List[Tuple[str, str, float]]:
        """
        Search FAQs using semantic similarity with WordLlama
        
        Args:
            query (str): Search query
            top_k (int): Number of top results to return
        
        Returns:
            List of tuples containing (question, answer, similarity_score)
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT question, answer FROM faqs')
            #If you have large db, you can filter out only relative data like below 
            #SELECT * FROM faqs WHERE question LIKE '%password%' OR question LIKE '%reset%' LIMIT 100; 
            all_faqs = cursor.fetchall()

        # Calculate similarities and rank
        ranked_faqs = [
        {"question": question, "answer": answer, "similarity_score": self.wl.similarity(query, question)} 
        for question, answer in all_faqs
    ]
    
        # Sort by similarity score in descending order
        ranked_faqs.sort(key=lambda x: x["similarity_score"], reverse=True)
        
        return ranked_faqs[:top_k]
def main(queries):        
    model_dir = 'wordlama_models'
    
    # Construct full paths
    weights_path = os.path.join(model_dir, 'l2_supercat_256.safetensors')
    config_path = os.path.join(model_dir, 'l2_supercat_tokenizer_config.json')
    faq_system = FAQSystem(
        weights_path=weights_path, 
        config_path=config_path,
      
    )
    
    
    # Demonstrate search functionality

    print(f"\nSearch Results for: '{queries}'")
    results = faq_system.search_faqs(queries)
    print(results)

queries="password reset"
main(queries)  
#----------------------------------------   
