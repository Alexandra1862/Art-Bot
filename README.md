# 🎨 Art Museum Telegram Bot
## t.me/art_museum_serch_bot
## (yes, there is an error in the username, i know :)  i created a beta test version at the beginning and i can not use the same username with the "search" ord in it. still, as my bot is not that perfect, the bot is anso not perfect.

## 📋 Project Description

A multilingual Telegram bot that allows users to explore masterpieces from the Metropolitan Museum of Art. The bot uses AI (Ollama with LLaMA) to understand natural language queries in English, Russian, and German, and provides detailed artwork information including artist biographies, historical context, and technical details.

## ✨ Features

- 🌍 **Multilingual Support**: English, Russian, German
- 🔍 **Smart Search**: AI-powered natural language understanding
- 🎨 **Search by Artist**: Quick access to works by famous artists (Van Gogh, Monet, Rembrandt, etc.)
- ⏰ **Search by Period**: Browse by artistic movements (Renaissance, Baroque, Impressionism, etc.)
- 🎲 **Random Discovery**: Get surprise masterpieces
- 📚 **Detailed Information**: Comprehensive artwork descriptions with:
  - Artist biographies (15+ famous artists)
  - Historical context
  - Artistic period information (10+ periods)
  - Technical details and materials
  - Style and composition analysis

## 🚀 How It Works

### Architecture

```
User Query → Telegram Bot → AI Helper (Ollama) → Met Museum API → Formatted Response
```

### Workflow

1. **User sends query** (in any supported language)
   - Text: "Show me Van Gogh's sunflowers"
   - Button: Select artist/period from menu

2. **AI Processing** (if text query)
   - Language detection (EN/RU/DE)
   - Keyword extraction using LLaMA 3.2
   - Translation to English (Met Museum API requirement)

3. **Museum API Search**
   - Query Met Museum's collection
   - Filter results with images
   - Retrieve artwork metadata

4. **Response Generation**
   - Create detailed descriptions in user's language
   - Add artist biography
   - Include period information
   - Format with technical details

5. **Display to User**
   - Send artwork image
   - Display formatted caption
   - Provide interactive buttons

## 📦 Installation

### Prerequisites

- Python 3.8+
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- Ollama installed locally

### Step 1: Install Ollama

1. **Download Ollama for Windows:**
   - Visit https://ollama.com/download
   - Download Windows version
   - Install (standard installation)

2. **Verify installation:**
   ```bash
   # Open Command Prompt (Win + R → cmd)
   ollama --version
   ```
   You should see version information (e.g., `ollama version is 0.1.26`)

3. **Download AI model** (~5-10 minutes, ~2GB):
   ```bash
   ollama pull llama3.2:3b
   ```
   This lightweight model provides excellent multilingual support for English, Russian, and German.

### Step 2: Install Python Dependencies

```bash
pip install python-telegram-bot requests python-dotenv ollama
```

### Step 3: Clone Repository

```bash
git clone https://github.com/yourusername/art-museum-bot.git
cd art-museum-bot
```

### Step 4: Configure Environment

1. Create `.env` file in project root:
   ```env
   TELEGRAM_TOKEN=your_bot_token_here
   ```

2. Get your bot token:
   - Message [@BotFather](https://t.me/botfather) on Telegram
   - Send `/newbot`
   - Follow instructions
   - Copy the token to `.env` file

### Step 5: Run the Bot

```bash
python bot_ai.py
```

You should see:
```
🧠 Testing Ollama...
✅ Ollama connected!
🤖 🎨 Art Museum Bot is running...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Languages: 🇬🇧 English | 🇷🇺 Русский | 🇩🇪 Deutsch
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 📁 Project Structure

```
Art Museum Bot/
├── __pycache__/
├── .env
├── ai_helper.py
├── bot.py
├── bot_ai.py
├── met_api.py
├── Museum_API/
├── ollama_test.py
├── test_api.py
├── test_ollama_connection.py

```

## 🔧 Core Components

### 1. **met_api.py** - Museum API Integration
- Connects to Metropolitan Museum of Art API
- Searches artworks by keywords
- Retrieves random artworks
- Extracts metadata (artist, date, culture, medium)

### 2. **ai_helper.py** - AI Language Processing
- Language detection (EN/RU/DE)
- Keyword extraction from natural language
- Uses Ollama with LLaMA 3.2 model
- Generates response messages

### 3. **bot_ai.py** - Main Bot Logic
- Telegram bot handlers
- Multilingual text management
- User interface (buttons, menus)
- Artwork description generation
- Artist biographies (15+ artists)
- Period information (10+ periods)

## 💬 Usage Examples

### Search in English:
```
"Show me Van Gogh's sunflowers"
"Impressionist paintings with water"
"Dark mysterious portraits"
```

### Search in Russian:
```
"Покажи картины Ван Гога с подсолнухами"
"Импрессионистские картины с водой"
"Тёмные таинственные портреты"
```

### Search in German:
```
"Zeig mir Van Goghs Sonnenblumen"
"Impressionistische Gemälde mit Wasser"
"Dunkle mysteriöse Porträts"
```

### Button Navigation:
- 🔍 Search Artworks
- 🎨 Search by Artist
- ⏰ Search by Period
- 🎲 Random Artwork
- ❓ Help

## 🌐 Supported Artists

Van Gogh, Monet, Rembrandt, Leonardo da Vinci, Picasso, Degas, Michelangelo, Caravaggio, Raphael, Rubens, Vermeer, Turner, Cézanne, Matisse, Goya

## 🎨 Supported Art Periods

Medieval, Renaissance, Baroque, Rococo, 18th Century, Romanticism, Impressionism, Post-Impressionism, Modern Art, Contemporary

## 🛠️ Troubleshooting

**No search results:**
- Try different keywords
- Use famous artist names
- Try broader art periods

## 📊 Technical Details

- **Language**: Python 3.8+
- **AI Model**: LLaMA 3.2 (3B parameters)
- **Museum API**: Metropolitan Museum of Art Collection API
- **Bot Framework**: python-telegram-bot
- **AI Framework**: Ollama

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 👥 Author

Alexandra Zakharova, BA ; for the course 2025W 136031-1 GenAI for Humanists

## 🙏 Acknowledgments

- Metropolitan Museum of Art for their open API
- Ollama team for the AI framework
- Meta for the LLaMA model
- Eugen - für alles! 😘
- Renato - for the possibility to make something interesting in the WS 2025/26! Thank you! 
---

**Enjoy exploring art! 🎨🖼️**
