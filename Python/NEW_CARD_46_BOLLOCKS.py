from PIL import Image, ImageDraw, ImageFont

def draw_spaced_text(draw, position, text, font, fill, letter_spacing=0):
    """Renders text with manual horizontal letter spacing to match AI layout."""
    x, y = position
    # Calculate total width to handle center alignment correctly
    total_width = 0
    for char in text:
        # Get bounding box width of single character
        bbox = draw.textbbox((0, 0), char, font=font)
        total_width += (bbox[2] - bbox[0]) + letter_spacing
    total_width -= letter_spacing  # Remove trailing spacer
    
    start_x = x - (total_width / 2)
    
    current_x = start_x
    for char in text:
        bbox = draw.textbbox((0, 0), char, font=font)
        char_w = bbox[2] - bbox[0]
        # Use 'lm' (left-middle) anchoring to keep vertical alignment locked
        draw.text((current_x, y), char, fill=fill, font=font, anchor="lm")
        current_x += char_w + letter_spacing

# 1. Load your exact 1023x1537 high-res template file
template_filename = "master_template_saudi.png"
base_card = Image.open(template_filename).convert("RGBA")
txt_layer = Image.new("RGBA", base_card.size, (255, 255, 255, 0))
draw = ImageDraw.Draw(txt_layer)

# 2. Color Calibration Profiles
WHITE = (255, 255, 255, 255)
SHADOW_COLOR = (15, 45, 25, 200)   # Soft deep green translucent shadow
FOREST_GREEN = (11, 82, 46, 255)   # Matches your card deck green theme

# 3. Load Balanced Fonts for 1023x1537 Canvas
font_id = ImageFont.truetype("timesbd.ttf", 90)        
font_title = ImageFont.truetype("timesbd.ttf", 72)     # Tuned for spaced layout
font_event = ImageFont.truetype("timesbi.ttf", 42)     
font_actions = ImageFont.truetype("timesbd.ttf", 320)  

center_x = base_card.width / 2

# --- ENTRY 1: TOP ID NUMBER ---
draw.text((center_x, 108), "46", fill=WHITE, font=font_id, anchor="mm")

# --- ENTRY 2: HEADER TITLE (WITH ADVANCED AI BLEND EFFECTS) ---
title_text = "WAR OF ATTRITION"
title_y = 248

# A. Drop Shadow Layer (1px down, 1px right) to match AI depth
draw_spaced_text(draw, (center_x + 1, title_y + 1), title_text, font_title, SHADOW_COLOR, letter_spacing=5)
# B. Primary Crisp White Text Layer
draw_spaced_text(draw, (center_x, title_y), title_text, font_title, WHITE, letter_spacing=5)

# --- ENTRY 3: EVENTS SECTION ---
event_center_y = 669
line_spacing = 58  

line1 = "Flip NORTH-EASTERN Front to DISRUPTED"
line2 = "If already DISRUPTED, flip WESTERN Front instead"

draw.text((center_x, event_center_y - (line_spacing / 2)), line1, fill=FOREST_GREEN, font=font_event, anchor="mm")
draw.text((center_x, event_center_y + (line_spacing / 2)), line2, fill=FOREST_GREEN, font=font_event, anchor="mm")

# --- ENTRY 4: ACTIONS NUMERAL ---
draw.text((center_x, 1174), "2", fill=WHITE, font=font_actions, anchor="mm")

# 4. Composite layout lines cleanly without touching a single background pixel
final_card = Image.alpha_composite(base_card, txt_layer)
final_card.convert("RGB").save("Card_46_Final.png")
print("Card 46 header integration complete with custom letter spacing and drop shadows!")
