

import ollama
import re

class AIArtAssistant:
    def __init__(self, model_name="llama3.2:3b"):
        self.model_name = model_name
    
    def extract_search_keywords(self, user_message, language="auto"):
        """
        Извлекает ключевые слова для поиска из описания пользователя
        Поддерживает русский, английский и немецкий
        """
        
        prompt = f"""You are an art museum search assistant. 
Your task is to extract English search keywords from the user's description of a painting.

User's description (in any language): "{user_message}"

Extract and return ONLY 3-5 English keywords that would help find similar artworks in a museum database.
Focus on:
- Style (e.g., impressionism, baroque, modern)
- Subject matter (e.g., landscape, portrait, flowers, sea)
- Mood/atmosphere (e.g., dark, bright, peaceful, dramatic)
- Colors (e.g., blue, red, colorful)
- Artists (if mentioned)

Return ONLY keywords separated by commas, nothing else.
Example output: landscape, peaceful, blue, impressionism

Keywords:"""

        try:
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    "temperature": 0.3,  # Более детерминированные ответы
                    "top_p": 0.9,
                }
            )
            
            # Извлекаем текст ответа
            keywords_text = response['response'].strip()
            
            # Очищаем от лишних символов
            keywords_text = re.sub(r'["\'\n]', '', keywords_text)
            keywords_text = keywords_text.lower()
            
            # Разбиваем на список
            keywords = [kw.strip() for kw in keywords_text.split(',') if kw.strip()]
            
            # Ограничиваем до 5 ключевых слов
            keywords = keywords[:5]
            
            return keywords
            
        except Exception as e:
            print(f"AI Error: {e}")
            # Fallback - простое извлечение слов из сообщения
            return self._simple_keyword_extraction(user_message)
    
    def _simple_keyword_extraction(self, text):
        """Запасной вариант: простое извлечение слов"""
        # Удаляем стоп-слова
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'я', 'хочу', 'покажи', 'найди', 'что-то', 'картину', 'с', 'про',
            'ich', 'möchte', 'zeig', 'mir', 'etwas', 'ein', 'eine', 'der', 'die', 'das'
        }
        
        words = re.findall(r'\w+', text.lower())
        keywords = [w for w in words if w not in stop_words and len(w) > 3]
        
        return keywords[:5]
    
    def generate_response_message(self, user_query, keywords, language="en"):
        """Генерирует дружелюбное сообщение для пользователя"""
        
        if language == "ru":
            return f"🔍 Ищу картины по вашему описанию...\n🏷️ Ключевые слова: {', '.join(keywords)}"
        elif language == "de":
            return f"🔍 Suche nach Kunstwerken...\n🏷️ Schlüsselwörter: {', '.join(keywords)}"
        else:
            return f"🔍 Searching for artworks matching your description...\n🏷️ Keywords: {', '.join(keywords)}"
    
    def detect_language(self, text):
        """Определяет язык текста (упрощенная версия)"""
        # Кириллица = русский
        if re.search(r'[а-яА-Я]', text):
            return "ru"
        # Немецкие умлауты
        elif re.search(r'[äöüÄÖÜß]', text):
            return "de"
        else:
            return "en"