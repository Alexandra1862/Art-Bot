import os
from typing import Dict, List
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from met_api import MetMuseumAPI
from ai_helper import AIArtAssistant

load_dotenv()

# Initialize APIs
met = MetMuseumAPI()
ai_assistant = AIArtAssistant()

# ==================== MULTILINGUAL TEXTS ====================
TEXTS = {
    'en': {
        'welcome': """🎨 Welcome to Art Museum Bot!

🌍 Languages: English | Русский | Deutsch

Explore masterpieces from:
🗽 **Metropolitan Museum of Art** (New York)

✨ **Features:**
• 🔍 Advanced search with detailed information
• 🎨 Search by famous artists
• ⏰ Browse by artistic period
• 🎲 Discover random masterpieces
• 📚 Comprehensive artwork descriptions

Select your language:""",
        'language_set': '✅ Language set to: English',
        'main_menu': '🎨 Main Menu',
        'search': '🔍 Search Artworks',
        'artist': '🎨 Search by Artist',
        'period': '⏰ Search by Period',
        'random': '🎲 Random Artwork',
        'help': '❓ Help',
        'searching': '🔍 Searching the Metropolitan Museum collection...',
        'finding_random': '🎲 Finding an amazing artwork for you...',
        'found_artworks': '✅ Found {count} artwork(s):',
        'no_artworks': """❌ No artworks found for your search.

**Try:**
• Different spelling or keywords
• Famous artist names (Monet, Van Gogh, Rembrandt)
• Art periods (Impressionism, Renaissance, Baroque)
• General themes (landscape, portrait, flowers)
• Use /help for more search examples""",
        'search_prompt': """🔍 **Advanced Artwork Search**

Tell me what you're looking for. Be as detailed as you want!

**Examples:**
• "Show me Van Gogh's starry night paintings"
• "Impressionist garden scenes with flowers"
• "Rembrandt portraits with dramatic lighting"
• "Renaissance religious paintings with angels"
• "Modern abstract art with bold colors"

I'll search the Metropolitan Museum's vast collection for you! 🗽""",
        'help_text': """❓ **How to Use Art Museum Bot**

🔍 **SEARCH ARTWORKS:**
Just type what you're looking for!

**Examples:**
• Artist: "Monet", "Van Gogh", "Rembrandt", "Picasso"
• Title: "Starry Night", "Water Lilies"
• Style: "Impressionism", "Baroque", "Renaissance"
• Subject: "flowers", "landscape", "portrait", "sea"

🎨 **SEARCH BY ARTIST:**
Quick access to works by famous artists

⏰ **SEARCH BY PERIOD:**
Explore specific art movements

🎲 **RANDOM ARTWORK:**
Discover surprise masterpieces

📚 **DETAILED INFORMATION:**
Each artwork includes artist biography, historical context, period details, and technical information.

Use /start to return to main menu!""",
        'select_artist': '🎨 **Select Artist:**',
        'select_period': '⏰ **Select Artistic Period:**',
        'artist_name': 'Artist',
        'year': 'Year',
        'museum': 'Museum',
        'historical_context': '📖 **Historical Context:**',
        'about_artist': '👨‍🎨 **About the Artist:**',
        'artistic_period': '⏰ **Artistic Period:**',
        'technical_details': '🎨 **Technical Details:**',
        'medium': 'Medium',
        'department': 'Department',
        'style': 'Style',
        'error_display': '❌ Sorry, couldn\'t display this artwork. Please try again!',
        'error_find': '❌ Sorry, couldn\'t find an artwork. Please try again!',
        'error_general': '❌ An error occurred. Please try again or use /help for assistance.'
    },
    'ru': {
        'welcome': """🎨 Добро пожаловать в Бот Художественного Музея!

🌍 Языки: English | Русский | Deutsch

Исследуйте шедевры из:
🗽 **Метрополитен-музея** (Нью-Йорк)

✨ **Возможности:**
• 🔍 Расширенный поиск с подробной информацией
• 🎨 Поиск по известным художникам
• ⏰ Просмотр по художественным периодам
• 🎲 Открытие случайных шедевров
• 📚 Подробные описания произведений

Выберите ваш язык:""",
        'language_set': '✅ Язык установлен: Русский',
        'main_menu': '🎨 Главное меню',
        'search': '🔍 Поиск картин',
        'artist': '🎨 Поиск по художнику',
        'period': '⏰ Поиск по периоду',
        'random': '🎲 Случайная картина',
        'help': '❓ Помощь',
        'searching': '🔍 Ищу в коллекции Метрополитен-музея...',
        'finding_random': '🎲 Ищу удивительную картину для вас...',
        'found_artworks': '✅ Найдено {count} картин(ы):',
        'no_artworks': """❌ Картины по вашему запросу не найдены.

**Попробуйте:**
• Другие ключевые слова
• Имена известных художников (Моне, Ван Гог, Рембрандт)
• Художественные периоды (Импрессионизм, Ренессанс, Барокко)
• Общие темы (пейзаж, портрет, цветы)
• Используйте /help для примеров поиска""",
        'search_prompt': """🔍 **Расширенный поиск картин**

Опишите, что вы ищете. Будьте максимально подробны!

**Примеры:**
• "Покажи картины Ван Гога со звёздным небом"
• "Импрессионистские сады с цветами"
• "Портреты Рембрандта с драматическим освещением"
• "Религиозные картины эпохи Возрождения с ангелами"
• "Современное абстрактное искусство с яркими цветами"

Я поищу в огромной коллекции Метрополитен-музея! 🗽""",
        'help_text': """❓ **Как использовать Бот Художественного Музея**

🔍 **ПОИСК КАРТИН:**
Просто напишите, что вы ищете!

**Примеры:**
• Художник: "Моне", "Ван Гог", "Рембрандт", "Пикассо"
• Название: "Звёздная ночь", "Кувшинки"
• Стиль: "Импрессионизм", "Барокко", "Ренессанс"
• Тема: "цветы", "пейзаж", "портрет", "море"

🎨 **ПОИСК ПО ХУДОЖНИКУ:**
Быстрый доступ к работам известных художников

⏰ **ПОИСК ПО ПЕРИОДУ:**
Изучайте определённые художественные движения

🎲 **СЛУЧАЙНАЯ КАРТИНА:**
Откройте для себя неожиданные шедевры

📚 **ПОДРОБНАЯ ИНФОРМАЦИЯ:**
Каждая картина включает биографию художника, исторический контекст, период и технические детали.

Используйте /start для возврата в главное меню!""",
        'select_artist': '🎨 **Выберите художника:**',
        'select_period': '⏰ **Выберите художественный период:**',
        'artist_name': 'Художник',
        'year': 'Год',
        'museum': 'Музей',
        'historical_context': '📖 **Исторический контекст:**',
        'about_artist': '👨‍🎨 **О художнике:**',
        'artistic_period': '⏰ **Художественный период:**',
        'technical_details': '🎨 **Технические детали:**',
        'medium': 'Материал',
        'department': 'Отдел',
        'style': 'Стиль',
        'error_display': '❌ Извините, не удалось показать эту картину. Попробуйте снова!',
        'error_find': '❌ Извините, не удалось найти картину. Попробуйте снова!',
        'error_general': '❌ Произошла ошибка. Попробуйте снова или используйте /help для помощи.'
    },
    'de': {
        'welcome': """🎨 Willkommen beim Kunstmuseum-Bot!

🌍 Sprachen: English | Русский | Deutsch

Entdecken Sie Meisterwerke aus:
🗽 **Metropolitan Museum of Art** (New York)

✨ **Funktionen:**
• 🔍 Erweiterte Suche mit detaillierten Informationen
• 🎨 Suche nach berühmten Künstlern
• ⏰ Durchsuchen nach Kunstperioden
• 🎲 Zufällige Meisterwerke entdecken
• 📚 Umfassende Kunstwerkbeschreibungen

Wählen Sie Ihre Sprache:""",
        'language_set': '✅ Sprache eingestellt: Deutsch',
        'main_menu': '🎨 Hauptmenü',
        'search': '🔍 Kunstwerke suchen',
        'artist': '🎨 Nach Künstler suchen',
        'period': '⏰ Nach Periode suchen',
        'random': '🎲 Zufälliges Kunstwerk',
        'help': '❓ Hilfe',
        'searching': '🔍 Durchsuche die Metropolitan Museum Sammlung...',
        'finding_random': '🎲 Finde ein erstaunliches Kunstwerk für Sie...',
        'found_artworks': '✅ {count} Kunstwerk(e) gefunden:',
        'no_artworks': """❌ Keine Kunstwerke für Ihre Suche gefunden.

**Versuchen Sie:**
• Andere Schreibweise oder Schlüsselwörter
• Berühmte Künstlernamen (Monet, Van Gogh, Rembrandt)
• Kunstperioden (Impressionismus, Renaissance, Barock)
• Allgemeine Themen (Landschaft, Porträt, Blumen)
• Verwenden Sie /help für weitere Suchbeispiele""",
        'search_prompt': """🔍 **Erweiterte Kunstwerksuche**

Sagen Sie mir, wonach Sie suchen. Seien Sie so detailliert wie Sie möchten!

**Beispiele:**
• "Zeig mir Van Goghs Sternennacht-Gemälde"
• "Impressionistische Gartenszenen mit Blumen"
• "Rembrandt-Porträts mit dramatischer Beleuchtung"
• "Renaissance religiöse Gemälde mit Engeln"
• "Moderne abstrakte Kunst mit kräftigen Farben"

Ich durchsuche die riesige Sammlung des Metropolitan Museum für Sie! 🗽""",
        'help_text': """❓ **Wie man den Kunstmuseum-Bot benutzt**

🔍 **KUNSTWERKE SUCHEN:**
Schreiben Sie einfach, wonach Sie suchen!

**Beispiele:**
• Künstler: "Monet", "Van Gogh", "Rembrandt", "Picasso"
• Titel: "Sternennacht", "Seerosen"
• Stil: "Impressionismus", "Barock", "Renaissance"
• Thema: "Blumen", "Landschaft", "Porträt", "Meer"

🎨 **NACH KÜNSTLER SUCHEN:**
Schneller Zugriff auf Werke berühmter Künstler

⏰ **NACH PERIODE SUCHEN:**
Erkunden Sie bestimmte Kunstbewegungen

🎲 **ZUFÄLLIGES KUNSTWERK:**
Entdecken Sie überraschende Meisterwerke

📚 **DETAILLIERTE INFORMATIONEN:**
Jedes Kunstwerk enthält Künstlerbiografie, historischen Kontext, Periodendetails und technische Informationen.

Verwenden Sie /start, um zum Hauptmenü zurückzukehren!""",
        'select_artist': '🎨 **Künstler wählen:**',
        'select_period': '⏰ **Kunstperiode wählen:**',
        'artist_name': 'Künstler',
        'year': 'Jahr',
        'museum': 'Museum',
        'historical_context': '📖 **Historischer Kontext:**',
        'about_artist': '👨‍🎨 **Über den Künstler:**',
        'artistic_period': '⏰ **Kunstperiode:**',
        'technical_details': '🎨 **Technische Details:**',
        'medium': 'Medium',
        'department': 'Abteilung',
        'style': 'Stil',
        'error_display': '❌ Entschuldigung, konnte dieses Kunstwerk nicht anzeigen. Bitte versuchen Sie es erneut!',
        'error_find': '❌ Entschuldigung, konnte kein Kunstwerk finden. Bitte versuchen Sie es erneut!',
        'error_general': '❌ Ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut oder verwenden Sie /help für Hilfe.'
    }
}

def get_text(lang: str, key: str, **kwargs) -> str:
    """Get text in user's language with formatting"""
    text = TEXTS.get(lang, TEXTS['en']).get(key, TEXTS['en'].get(key, ''))
    if kwargs:
        text = text.format(**kwargs)
    return text

# ==================== KEYBOARDS ====================
def get_language_keyboard():
    """Language selection keyboard"""
    keyboard = [
        [InlineKeyboardButton("🇬🇧 English", callback_data='lang_en')],
        [InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru')],
        [InlineKeyboardButton("🇩🇪 Deutsch", callback_data='lang_de')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_main_menu_keyboard(lang: str):
    """Main menu keyboard"""
    keyboard = [
        [KeyboardButton(get_text(lang, 'search')), KeyboardButton(get_text(lang, 'random'))],
        [KeyboardButton(get_text(lang, 'artist')), KeyboardButton(get_text(lang, 'period'))],
        [KeyboardButton(get_text(lang, 'help'))]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_period_selection_keyboard(lang: str):
    """Period selection keyboard"""
    periods = {
        'en': [
            "🏛️ Renaissance (1400-1600)",
            "👑 Baroque (1600-1750)",
            "🎭 Romanticism (1800-1850)",
            "🌅 Impressionism (1860-1890)",
            "🎨 Modern (1900+)"
        ],
        'ru': [
            "🏛️ Ренессанс (1400-1600)",
            "👑 Барокко (1600-1750)",
            "🎭 Романтизм (1800-1850)",
            "🌅 Импрессионизм (1860-1890)",
            "🎨 Модерн (1900+)"
        ],
        'de': [
            "🏛️ Renaissance (1400-1600)",
            "👑 Barock (1600-1750)",
            "🎭 Romantik (1800-1850)",
            "🌅 Impressionismus (1860-1890)",
            "🎨 Moderne (1900+)"
        ]
    }
    
    keyboard = []
    for idx, period_text in enumerate(periods.get(lang, periods['en'])):
        period_keys = ['renaissance', 'baroque', 'romanticism', 'impressionism', 'modern']
        keyboard.append([InlineKeyboardButton(period_text, callback_data=f'period_{period_keys[idx]}')])
    
    return InlineKeyboardMarkup(keyboard)

def get_artist_selection_keyboard():
    """Famous artists keyboard"""
    keyboard = [
        [InlineKeyboardButton("Vincent van Gogh", callback_data="artist_van gogh")],
        [InlineKeyboardButton("Claude Monet", callback_data="artist_monet")],
        [InlineKeyboardButton("Rembrandt", callback_data="artist_rembrandt")],
        [InlineKeyboardButton("Leonardo da Vinci", callback_data="artist_da vinci")],
        [InlineKeyboardButton("Pablo Picasso", callback_data="artist_picasso")],
        [InlineKeyboardButton("Edgar Degas", callback_data="artist_degas")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ==================== COMMAND HANDLERS ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command with language selection"""
    user = update.effective_user
    
    # Check if language is already set
    if 'language' not in context.user_data:
        await update.message.reply_text(
            TEXTS['en']['welcome'],
            reply_markup=get_language_keyboard(),
            parse_mode='Markdown'
        )
    else:
        lang = context.user_data['language']
        await update.message.reply_text(
            get_text(lang, 'welcome'),
            reply_markup=get_main_menu_keyboard(lang),
            parse_mode='Markdown'
        )

async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle language selection"""
    query = update.callback_query
    await query.answer()
    
    language = query.data.split('_')[1]
    context.user_data['language'] = language
    
    await query.edit_message_text(
        get_text(language, 'language_set'),
        parse_mode='Markdown'
    )
    
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=get_text(language, 'main_menu'),
        reply_markup=get_main_menu_keyboard(language)
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command"""
    lang = context.user_data.get('language', 'en')
    await update.message.reply_text(
        get_text(lang, 'help_text'),
        parse_mode='Markdown'
    )

async def search_by_period(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Search by artistic period"""
    lang = context.user_data.get('language', 'en')
    await update.message.reply_text(
        get_text(lang, 'select_period'),
        reply_markup=get_period_selection_keyboard(lang),
        parse_mode='Markdown'
    )

async def search_by_artist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Search by famous artist"""
    lang = context.user_data.get('language', 'en')
    await update.message.reply_text(
        get_text(lang, 'select_artist'),
        reply_markup=get_artist_selection_keyboard(),
        parse_mode='Markdown'
    )

async def random_artwork(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get random artwork"""
    lang = context.user_data.get('language', 'en')
    await update.message.reply_text(get_text(lang, 'finding_random'))
    
    artwork = met.get_random_artwork()
    
    if artwork and artwork.get('image_url'):
        description = generate_detailed_description(artwork, lang)
        
        caption = f"""🎨 **{artwork['title']}**

👨‍🎨 **{get_text(lang, 'artist_name')}:** {artwork['artist']}
📅 **{get_text(lang, 'year')}:** {artwork.get('date', 'Unknown')}
🏛️ **{get_text(lang, 'museum')}:** Metropolitan Museum of Art

{description}"""
        
        try:
            await update.message.reply_photo(
                photo=artwork['image_url'],
                caption=caption[:1024],
                parse_mode='Markdown'
            )
        except Exception as e:
            print(f"Error sending photo: {e}")
            await update.message.reply_text(get_text(lang, 'error_display'))
    else:
        await update.message.reply_text(get_text(lang, 'error_find'))

async def advanced_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Advanced search"""
    lang = context.user_data.get('language', 'en')
    user_message = update.message.text
    
    # Handle menu buttons
    if user_message == get_text(lang, 'search'):
        await update.message.reply_text(
            get_text(lang, 'search_prompt'),
            parse_mode='Markdown'
        )
        return
    
    if user_message == get_text(lang, 'random'):
        await random_artwork(update, context)
        return
    
    if user_message == get_text(lang, 'artist'):
        await search_by_artist(update, context)
        return
    
    if user_message == get_text(lang, 'period'):
        await search_by_period(update, context)
        return
    
    if user_message == get_text(lang, 'help'):
        await help_command(update, context)
        return
    
    # Perform search
    await update.message.reply_text(get_text(lang, 'searching'))
    
    # Extract keywords using AI
    language_detected = ai_assistant.detect_language(user_message)
    keywords = ai_assistant.extract_search_keywords(user_message, language_detected)
    
    if not keywords:
        await update.message.reply_text(
            get_text(lang, 'no_artworks'),
            parse_mode='Markdown'
        )
        return
    
    # Search
    search_query = " ".join(keywords)
    artworks = met.search_artworks(search_query, max_results=5)
    
    if not artworks and len(keywords) > 2:
        search_query = " ".join(keywords[:2])
        artworks = met.search_artworks(search_query, max_results=5)
    
    if not artworks and len(keywords) > 0:
        search_query = keywords[0]
        artworks = met.search_artworks(search_query, max_results=5)
    
    if not artworks:
        await update.message.reply_text(
            get_text(lang, 'no_artworks'),
            parse_mode='Markdown'
        )
        return
    
    # Send results
    await update.message.reply_text(
        get_text(lang, 'found_artworks', count=len(artworks)),
        parse_mode='Markdown'
    )
    
    for artwork in artworks:
        if artwork.get('image_url'):
            description = generate_detailed_description(artwork, lang)
            
            caption = f"""🗽 **{artwork['title']}**

👨‍🎨 **{get_text(lang, 'artist_name')}:** {artwork['artist']}
📅 **{get_text(lang, 'year')}:** {artwork.get('date', 'Unknown')}
🏛️ **{get_text(lang, 'museum')}:** Metropolitan Museum of Art

{description}"""
            
            try:
                await update.message.reply_photo(
                    photo=artwork['image_url'],
                    caption=caption[:1024],
                    parse_mode='Markdown'
                )
            except Exception as e:
                print(f"Error sending artwork: {e}")
                continue

def generate_detailed_description(artwork: Dict, lang: str) -> str:
    """Generate detailed description in user's language"""
    title = artwork.get('title', 'Unknown')
    artist = artwork.get('artist', 'Unknown Artist')
    date = artwork.get('date', 'Unknown period')
    culture = artwork.get('culture', '')
    department = artwork.get('department', '')
    medium = artwork.get('medium', '')
    
    description = ""
    
    # Historical Context
    description += get_text(lang, 'historical_context') + "\n"
    
    if culture:
        if lang == 'ru':
            description += f"Этот шедевр происходит из культуры {culture}. "
        elif lang == 'de':
            description += f"Dieses Meisterwerk stammt aus der {culture} Kultur. "
        else:
            description += f"This masterpiece originates from {culture} culture. "
    
    if lang == 'ru':
        description += f"Создано {artist}"
    elif lang == 'de':
        description += f"Geschaffen von {artist}"
    else:
        description += f"Created by {artist}"
    
    if date and date != 'Unknown':
        if lang == 'ru':
            description += f" в {date}"
        elif lang == 'de':
            description += f" im Jahr {date}"
        else:
            description += f" in {date}"
    
    description += ".\n\n"
    
    # Artist Information
    description += get_text(lang, 'about_artist') + "\n"
    artist_context = get_artist_context(artist, lang)
    description += f"{artist_context}\n\n"
    
    # Period Information
    period = determine_period(date)
    if period:
        description += get_text(lang, 'artistic_period') + "\n"
        period_info = get_period_information(period, lang)
        description += f"{period_info}\n\n"
    
    # Technical Details
    description += get_text(lang, 'technical_details') + "\n"
    
    if medium:
        description += f"{get_text(lang, 'medium')}: {medium}\n"
    
    if department:
        description += f"{get_text(lang, 'department')}: {department}\n"
    
    # Artistic characteristics
    characteristics = get_artistic_characteristics(artist, period, title.lower(), lang)
    if characteristics:
        description += f"{get_text(lang, 'style')}: {characteristics}\n"
    
    return description

def determine_period(date_str: str) -> str:
    """Determine artistic period from date"""
    try:
        year = int(''.join(filter(str.isdigit, date_str))[:4])
        
        if year < 1400:
            return 'Medieval'
        elif year < 1600:
            return 'Renaissance'
        elif year < 1700:
            return 'Baroque'
        elif year < 1800:
            return '18th Century'
        elif year < 1850:
            return 'Romanticism'
        elif year < 1890:
            return 'Impressionism'
        elif year < 1910:
            return 'Post-Impressionism'
        elif year < 1950:
            return 'Modern Art'
        else:
            return 'Contemporary'
    except:
        return ''

def get_artist_context(artist: str, lang: str) -> str:
    """Get artist biography in user's language"""
    artist_lower = artist.lower()
    
    contexts = {
        'van gogh': {
            'en': "Vincent van Gogh (1853-1890) was a Dutch Post-Impressionist painter whose work profoundly influenced 20th-century art. Known for bold colors and emotional honesty.",
            'ru': "Винсент ван Гог (1853-1890) был голландским постимпрессионистом, чьи работы глубоко повлияли на искусство XX века. Известен яркими цветами и эмоциональной честностью.",
            'de': "Vincent van Gogh (1853-1890) war ein niederländischer postimpressionistischer Maler, dessen Werk die Kunst des 20. Jahrhunderts tiefgreifend beeinflusste. Bekannt für kräftige Farben und emotionale Ehrlichkeit."
        },
        'monet': {
            'en': "Claude Monet (1840-1926) was a founder of French Impressionism. Famous for his series paintings capturing light and atmosphere.",
            'ru': "Клод Моне (1840-1926) был основателем французского импрессионизма. Знаменит серийными картинами, запечатлевающими свет и атмосферу.",
            'de': "Claude Monet (1840-1926) war ein Begründer des französischen Impressionismus. Berühmt für seine Serienbilder, die Licht und Atmosphäre einfangen."
        },
        'rembrandt': {
            'en': "Rembrandt van Rijn (1606-1669) was a Dutch Golden Age painter, master of light and shadow (chiaroscuro).",
            'ru': "Рембрандт ван Рейн (1606-1669) был художником Золотого века Нидерландов, мастером света и тени (кьяроскуро).",
            'de': "Rembrandt van Rijn (1606-1669) war ein niederländischer Maler des Goldenen Zeitalters, Meister von Licht und Schatten (Chiaroscuro)."
        },
        'leonardo': {
            'en': "Leonardo da Vinci (1452-1519) was an Italian Renaissance polymath - painter, inventor, scientist.",
            'ru': "Леонардо да Винчи (1452-1519) был итальянским универсалом эпохи Возрождения - художником, изобретателем, учёным.",
            'de': "Leonardo da Vinci (1452-1519) war ein italienischer Renaissance-Universalgelehrter - Maler, Erfinder, Wissenschaftler."
        },
        'picasso': {
            'en': "Pablo Picasso (1881-1973) was a Spanish painter and co-founder of Cubism.",
            'ru': "Пабло Пикассо (1881-1973) был испанским художником и соосно вателем кубизма.",
            'de': "Pablo Picasso (1881-1973) war ein spanischer Maler und Mitbegründer des Kubismus."
        }
    }
    
    for key, context_dict in contexts.items():
        if key in artist_lower:
            return context_dict.get(lang, context_dict['en'])
    
    if lang == 'ru':
        return f"{artist} был значимым художником, внёсшим вклад в историю искусства."
    elif lang == 'de':
        return f"{artist} war ein bedeutender Künstler, der zur Kunstgeschichte beitrug."
    else:
        return f"{artist} was a significant artist who contributed to art history."

def get_period_information(period: str, lang: str) -> str:
    """Get period information in user's language"""
    periods = {
        'Renaissance': {
            'en': "The Renaissance (14th-17th century) marked a cultural rebirth emphasizing humanism, realism, and classical inspiration.",
            'ru': "Ренессанс (14-17 века) ознаменовал культурное возрождение с акцентом на гуманизм, реализм и классическое вдохновение.",
            'de': "Die Renaissance (14.-17. Jahrhundert) markierte eine kulturelle Wiedergeburt mit Betonung auf Humanismus, Realismus und klassischer Inspiration."
        },
        'Baroque': {
            'en': "The Baroque period (1600-1750) featured dramatic expression, rich colors, and intense light and shadow contrasts.",
            'ru': "Период барокко (1600-1750) характеризовался драматическим выражением, насыщенными цветами и интенсивными контрастами света и тени.",
            'de': "Die Barockzeit (1600-1750) zeichnete sich durch dramatischen Ausdruck, reiche Farben und intensive Hell-Dunkel-Kontraste aus."
        },
        'Impressionism': {
            'en': "Impressionism (1860-1890) revolutionized art with visible brushstrokes and emphasis on light effects.",
            'ru': "Импрессионизм (1860-1890) революционизировал искусство видимыми мазками кисти и акцентом на световых эффектах.",
            'de': "Der Impressionismus (1860-1890) revolutionierte die Kunst mit sichtbaren Pinselstrichen und Betonung auf Lichteffekten."
        }
    }
    
    if period in periods:
        return periods[period].get(lang, periods[period]['en'])
    
    if lang == 'ru':
        return f"Это произведение принадлежит к периоду {period}."
    elif lang == 'de':
        return f"Dieses Werk gehört zur Periode {period}."
    else:
        return f"This work belongs to the {period} period."

def get_artistic_characteristics(artist: str, period: str, title: str, lang: str) -> str:
    """Get artistic characteristics in user's language"""
    characteristics = []
    artist_lower = artist.lower()
    
    if 'van gogh' in artist_lower:
        if lang == 'ru':
            characteristics.append("смелые мазки и яркие цвета")
        elif lang == 'de':
            characteristics.append("kühne Pinselstriche und lebendige Farben")
        else:
            characteristics.append("bold brushstrokes and vibrant colors")
    elif 'monet' in artist_lower:
        if lang == 'ru':
            characteristics.append("импрессионистские световые эффекты")
        elif lang == 'de':
            characteristics.append("impressionistische Lichteffekte")
        else:
            characteristics.append("impressionist light effects")
    
    if characteristics:
        return ", ".join(characteristics)
    
    if lang == 'ru':
        return "уникальное художественное видение"
    elif lang == 'de':
        return "einzigartige künstlerische Vision"
    else:
        return "distinctive artistic vision"

# ==================== CALLBACK HANDLERS ====================
async def period_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle period selection"""
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get('language', 'en')
    
    period = query.data.split('_')[1]
    period_queries = {'renaissance': 'Renaissance', 'baroque': 'Baroque', 
                     'romanticism': 'Romanticism', 'impressionism': 'Impressionism', 
                     'modern': 'Modern'}
    
    await query.edit_message_text(f"🔍 {get_text(lang, 'searching')}")
    
    artworks = met.search_artworks(period_queries[period], max_results=3)
    
    if not artworks:
        await query.message.reply_text(get_text(lang, 'no_artworks'), parse_mode='Markdown')
        return
    
    await query.message.reply_text(get_text(lang, 'found_artworks', count=len(artworks)), parse_mode='Markdown')
    
    for artwork in artworks:
        if artwork.get('image_url'):
            description = generate_detailed_description(artwork, lang)
            caption = f"""🗽 **{artwork['title']}**

👨‍🎨 **{get_text(lang, 'artist_name')}:** {artwork['artist']}
📅 **{get_text(lang, 'year')}:** {artwork.get('date', 'Unknown')}

{description}"""
            
            try:
                await query.message.reply_photo(photo=artwork['image_url'], caption=caption[:1024], parse_mode='Markdown')
            except Exception as e:
                print(f"Error: {e}")

async def artist_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle artist selection"""
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get('language', 'en')
    
    artist = query.data.split('_', 1)[1]
    await query.edit_message_text(f"🔍 {get_text(lang, 'searching')}")
    
    artworks = met.search_artworks(artist, max_results=3)
    
    if not artworks:
        await query.message.reply_text(get_text(lang, 'no_artworks'), parse_mode='Markdown')
        return
    
    await query.message.reply_text(get_text(lang, 'found_artworks', count=len(artworks)), parse_mode='Markdown')
    
    for artwork in artworks:
        if artwork.get('image_url'):
            description = generate_detailed_description(artwork, lang)
            caption = f"""🗽 **{artwork['title']}**

👨‍🎨 **{get_text(lang, 'artist_name')}:** {artwork['artist']}
📅 **{get_text(lang, 'year')}:** {artwork.get('date', 'Unknown')}

{description}"""
            
            try:
                await query.message.reply_photo(photo=artwork['image_url'], caption=caption[:1024], parse_mode='Markdown')
            except Exception as e:
                print(f"Error: {e}")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    print(f"Error: {context.error}")
    if update and update.effective_message:
        lang = context.user_data.get('language', 'en')
        await update.effective_message.reply_text(get_text(lang, 'error_general'))

# ==================== MAIN ====================
def main():
    """Start the bot"""
    token = os.getenv('TELEGRAM_TOKEN')
    
    if not token:
        print("❌ Error: TELEGRAM_TOKEN not found!")
        return
    
    print("🧠 Testing Ollama...")
    try:
        import ollama
        ollama.list()
        print("✅ Ollama connected!")
    except Exception as e:
        print(f"⚠️ Ollama not available: {e}")
    
    app = Application.builder().token(token).build()
    
    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("random", random_artwork))
    app.add_handler(CallbackQueryHandler(language_callback, pattern='^lang_'))
    app.add_handler(CallbackQueryHandler(period_callback, pattern='^period_'))
    app.add_handler(CallbackQueryHandler(artist_callback, pattern='^artist_'))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, advanced_search))
    
    # Error handler (use add_error_handler, not add_handler)
    app.add_error_handler(error_handler)
    
    print("🤖 🎨 Multilingual Art Museum Bot is running...")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("Languages: 🇬🇧 English | 🇷🇺 Русский | 🇩🇪 Deutsch")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    import nest_asyncio
    nest_asyncio.apply()
    
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()