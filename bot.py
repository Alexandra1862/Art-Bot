import os
from typing import Dict
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from met_api import MetMuseumAPI

load_dotenv()

# Initialize API
met = MetMuseumAPI()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command"""
    welcome_message = """🎨 Welcome to Art Museum Bot!

Explore masterpieces from:
🗽 **Metropolitan Museum of Art** (New York)

✨ **Features:**
• 🔍 Search artworks with detailed information
• 🎲 Discover random masterpieces
• 📚 Get comprehensive descriptions including:
  - Artist biography and context
  - Historical period details
  - Technique and materials
  - Cultural significance

**Available commands:**
/start - Show this message
/random - Get a random artwork
/help - Detailed help guide

**Or just describe what you're looking for:**
• Artist name: "Monet", "Van Gogh", "Rembrandt"
• Style/Period: "Impressionism", "Renaissance", "Baroque"
• Subject: "landscape", "portrait", "flowers", "sea"
• Detailed: "Van Gogh sunflowers", "Monet water lilies"

Let's discover art together! 🖼️"""
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command"""
    help_text = """❓ **How to Use Art Museum Bot**

🔍 **SEARCH ARTWORKS:**
Just type what you're looking for!

**Examples:**
• Artist: "Monet", "Van Gogh", "Rembrandt", "Picasso"
• Title: "Starry Night", "Water Lilies", "The Kiss"
• Style: "Impressionism", "Baroque", "Renaissance"
• Subject: "flowers", "landscape", "portrait", "sea"
• Detailed: "Van Gogh sunflowers", "Rembrandt self-portrait"

🎲 **RANDOM ARTWORK:**
Use /random to discover a surprise masterpiece

📚 **DETAILED INFORMATION:**
Each artwork includes:
• 🎨 Title and artist
• 📅 Year created
• 👨‍🎨 Artist biography
• ⏰ Historical period context
• 🖼️ Technical details and style
• 🏛️ Museum information

**Tips for better results:**
✓ Use famous artist names
✓ Mention art periods or styles
✓ Include descriptive words
✓ Try different keywords if no results

Enjoy exploring art history! 🖼️"""
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def random_artwork(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send random artwork with detailed information"""
    await update.message.reply_text("🎲 Finding an amazing artwork for you...")
    
    artwork = met.get_random_artwork()
    
    if artwork and artwork['image_url']:
        # Generate detailed description
        description = generate_detailed_description(artwork)
        
        caption = f"""🎨 **{artwork['title']}**

👨‍🎨 **Artist:** {artwork['artist']}
📅 **Year:** {artwork.get('date', 'Unknown')}
🏛️ **Museum:** Metropolitan Museum of Art

{description}"""
        
        try:
            await update.message.reply_photo(
                photo=artwork['image_url'],
                caption=caption[:1024],
                parse_mode='Markdown'
            )
        except Exception as e:
            print(f"Error sending photo: {e}")
            await update.message.reply_text("❌ Sorry, couldn't display this artwork. Try again!")
    else:
        await update.message.reply_text("❌ Sorry, couldn't find an artwork. Try again!")

async def search_artwork(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Search artworks by user query with detailed descriptions"""
    query = update.message.text
    
    await update.message.reply_text(f"🔍 Searching for: '{query}'...")
    
    # Search artworks
    artworks = met.search_artworks(query, max_results=3)
    
    if not artworks:
        await update.message.reply_text(
            "❌ No artworks found for your search.\n\n"
            "**Try:**\n"
            "• Different spelling or keywords\n"
            "• Famous artist names (Monet, Van Gogh, Rembrandt)\n"
            "• Art periods (Impressionism, Renaissance, Baroque)\n"
            "• General themes (landscape, portrait, flowers)\n"
            "• Use /help for more search examples",
            parse_mode='Markdown'
        )
        return
    
    # Send results
    await update.message.reply_text(f"✅ Found {len(artworks)} artwork(s):")
    
    for artwork in artworks:
        if artwork['image_url']:
            # Generate detailed description
            description = generate_detailed_description(artwork)
            
            caption = f"""🎨 **{artwork['title']}**

👨‍🎨 **Artist:** {artwork['artist']}
📅 **Year:** {artwork.get('date', 'Unknown')}
🏛️ **Museum:** Metropolitan Museum of Art

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

def generate_detailed_description(artwork: Dict) -> str:
    """Generate comprehensive artwork description with historical context"""
    title = artwork.get('title', 'Unknown')
    artist = artwork.get('artist', 'Unknown Artist')
    date = artwork.get('date', 'Unknown period')
    culture = artwork.get('culture', '')
    department = artwork.get('department', '')
    medium = artwork.get('medium', '')
    
    description = ""
    
    # Historical Context
    description += "📖 **Historical Context:**\n"
    
    if culture:
        description += f"This masterpiece originates from {culture} culture. "
    
    description += f"Created by {artist}"
    
    if date and date != 'Unknown':
        description += f" in {date}"
    
    description += ".\n\n"
    
    # Artist Information
    description += "👨‍🎨 **About the Artist:**\n"
    artist_context = get_artist_context(artist)
    description += f"{artist_context}\n\n"
    
    # Period Information
    period = determine_period(date)
    if period:
        description += f"⏰ **Artistic Period:**\n"
        period_info = get_period_information(period)
        description += f"{period_info}\n\n"
    
    # Technical Details
    description += "🎨 **Technical Details:**\n"
    
    if medium:
        description += f"Medium: {medium}\n"
    
    if department:
        description += f"Department: {department}\n"
    
    # Artistic characteristics
    characteristics = get_artistic_characteristics(artist, period, title.lower())
    if characteristics:
        description += f"Style: {characteristics}\n"
    
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

def get_artist_context(artist: str) -> str:
    """Get biographical context about the artist"""
    artist_lower = artist.lower()
    
    contexts = {
        'van gogh': "Vincent van Gogh (1853-1890) was a Dutch Post-Impressionist painter whose work profoundly influenced 20th-century art. Known for bold colors, dramatic brushwork, and emotional honesty.",
        'monet': "Claude Monet (1840-1926) was a founder of French Impressionism. Famous for his series paintings capturing light and atmosphere, including water lilies, haystacks, and the Rouen Cathedral.",
        'rembrandt': "Rembrandt van Rijn (1606-1669) was a Dutch Golden Age painter, considered one of the greatest visual artists in history. Master of light and shadow (chiaroscuro).",
        'leonardo': "Leonardo da Vinci (1452-1519) was an Italian Renaissance polymath - painter, inventor, scientist. Creator of the Mona Lisa and The Last Supper.",
        'picasso': "Pablo Picasso (1881-1973) was a Spanish painter and co-founder of Cubism. One of the most influential artists of the 20th century.",
        'degas': "Edgar Degas (1834-1917) was a French Impressionist artist famous for his paintings of ballet dancers, capturing movement and light in innovative ways.",
        'michelangelo': "Michelangelo (1475-1564) was an Italian Renaissance sculptor, painter, and architect. Creator of the Sistine Chapel ceiling and the statue of David.",
        'caravaggio': "Caravaggio (1571-1610) was an Italian Baroque master known for dramatic use of light and shadow (tenebrism) and realistic depiction of religious scenes.",
        'raphael': "Raphael (1483-1520) was an Italian High Renaissance painter known for harmonious compositions and graceful figures.",
        'rubens': "Peter Paul Rubens (1577-1640) was a Flemish Baroque painter known for dynamic compositions, vibrant colors, and sensuous figures.",
        'vermeer': "Johannes Vermeer (1632-1675) was a Dutch Baroque painter who specialized in domestic interior scenes. Master of light.",
        'cezanne': "Paul Cézanne (1839-1906) was a French Post-Impressionist painter whose work laid foundations for the transition to Cubism.",
        'matisse': "Henri Matisse (1869-1954) was a French artist known for revolutionary use of color. Leader of the Fauvism movement.",
        'goya': "Francisco Goya (1746-1828) was a Spanish Romantic painter considered the last of the Old Masters and first of the moderns."
    }
    
    for key, context in contexts.items():
        if key in artist_lower:
            return context
    
    return f"{artist} was a significant artist whose work contributed to art history."

def get_period_information(period: str) -> str:
    """Get information about the artistic period"""
    periods = {
        'Medieval': "The Medieval period (5th-15th century) featured religious art, illuminated manuscripts, and Gothic architecture.",
        'Renaissance': "The Renaissance (14th-17th century) marked a cultural rebirth emphasizing humanism, realism, and classical inspiration. Artists mastered perspective and anatomy.",
        'Baroque': "The Baroque period (1600-1750) featured dramatic expression, rich colors, intense light and shadow contrasts, and grandeur.",
        '18th Century': "The 18th century saw Neoclassicism reviving classical styles, emphasizing order, symmetry, and moral virtue.",
        'Romanticism': "Romanticism (1800-1850) emphasized emotion, individualism, and nature's sublime power. Artists focused on dramatic subjects and expressive techniques.",
        'Impressionism': "Impressionism (1860-1890) revolutionized art with visible brushstrokes, emphasis on light effects, and scenes from everyday life.",
        'Post-Impressionism': "Post-Impressionism (1886-1905) extended Impressionism while emphasizing symbolic content and formal structure.",
        'Modern Art': "Modern Art (1900-1950) broke from traditional techniques, embracing abstraction, experimentation, and diverse movements.",
        'Contemporary': "Contemporary Art (1950-present) encompasses diverse styles, media, and concepts, characterized by pluralism and conceptual approaches."
    }
    
    return periods.get(period, f"This work belongs to the {period} period.")

def get_artistic_characteristics(artist: str, period: str, title: str) -> str:
    """Determine artistic characteristics"""
    characteristics = []
    
    artist_lower = artist.lower()
    
    # Artist-specific
    if 'van gogh' in artist_lower:
        characteristics.append("bold brushstrokes and vibrant colors")
    elif 'monet' in artist_lower:
        characteristics.append("impressionist light effects and soft palette")
    elif 'rembrandt' in artist_lower:
        characteristics.append("dramatic chiaroscuro and psychological depth")
    elif 'degas' in artist_lower:
        characteristics.append("innovative compositions and movement")
    
    # Period-specific
    if period:
        if 'Impressionism' in period:
            characteristics.append("loose brushwork capturing light")
        elif 'Baroque' in period:
            characteristics.append("dramatic composition and rich colors")
        elif 'Renaissance' in period:
            characteristics.append("realistic perspective and balance")
    
    # Subject-based
    if 'portrait' in title:
        characteristics.append("human expression focus")
    elif 'landscape' in title:
        characteristics.append("natural scenery emphasis")
    
    if characteristics:
        return ", ".join(characteristics)
    return "distinctive artistic vision"

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    print(f"Error: {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "❌ An error occurred. Please try again or use /help for assistance."
        )

def main():
    """Start the bot"""
    # Get token
    token = os.getenv('TELEGRAM_TOKEN')
    
    if not token:
        print("❌ Error: TELEGRAM_TOKEN not found in .env file!")
        return
    
    # Create application
    app = Application.builder().token(token).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("random", random_artwork))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_artwork))
    
    # Error handler
    app.add_error_handler(error_handler)
    
    # Start bot
    print("🤖 🎨 Art Museum Bot is running...")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("Features:")
    print("✅ Search artworks with detailed descriptions")
    print("✅ Artist biographies (14+ famous artists)")
    print("✅ Historical period information (9 periods)")
    print("✅ Technical details and artistic characteristics")
    print("✅ Random artwork discovery")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    import asyncio
    import nest_asyncio
    nest_asyncio.apply()
    
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()

