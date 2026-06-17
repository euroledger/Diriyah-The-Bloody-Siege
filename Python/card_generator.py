import os
import platform
import urllib.request
from PIL import Image, ImageDraw, ImageFont

def guarantee_local_fonts():
    """Automatically downloads authentic Times New Roman font files if missing from the folder."""
    fonts = {
        "timesbd.ttf": "https://githubusercontent.com",
        "timesi.ttf": "https://githubusercontent.com"
    }
    
    for font_name, url in fonts.items():
        if not os.path.exists(font_name):
            print(f"Font file '{font_name}' not found locally. Downloading from repository...")
            try:
                # Disguise user-agent to bypass basic server blocking rules
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as response, open(font_name, 'wb') as out_file:
                    out_file.write(response.read())
                print(f"Successfully installed local asset: {font_name}")
            except Exception as e:
                print(f"Warning: Automatic download failed for {font_name}. Error: {e}")

def get_times_font(font_type, size):
    """Retrieves the clean local font asset with perfect sizing capabilities."""
    filename = "timesi.ttf" if font_type == "italic" else "timesbd.ttf"
    
    if os.path.exists(filename):
        return ImageFont.truetype(filename, size)
    
    # Absolute system pathways if the download fails
    system = platform.system()
    paths = []
    if system == "Windows":
        paths = [rf"C:\Windows\Fonts\{filename}", rf"C:\Windows\Fonts\{filename.upper()}"]
    elif system == "Darwin":
        paths = [f"/Library/Fonts/Times New Roman {'Italic' if font_type=='italic' else 'Bold'}.ttf"]
        
    for path in paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
            
    print(f"CRITICAL FALLBACK: Using basic font engine for {filename}. Scale will be degraded.")
    return ImageFont.load_default()

def generate_single_card(card_id, title, event_text, advance_marker, action_points, card_type):
    # Ensure our true typography files are present before drawing anything
    guarantee_local_fonts()
    
    # 1. DYNAMIC TEMPLATE SELECTION
    template_file = "master_template_saudi.png" if card_type.upper() == "SAUDI" else "master_template_turkish.png"
    
    if os.path.exists(template_file):
        card = Image.open(template_file).convert("RGBA")
    else:
        print(f"Error: Template file '{template_file}' not found in your directory!")
        return
        
    draw = ImageDraw.Draw(card)
    img_w, img_h = card.size
    center_x = img_w // 2  # 512 pixels
    
    # 2. SCALED HIGH-RES FONTS SETUP (Bound directly to true vector files)
    id_str = str(card_id)
    font_size_id = 90 if len(id_str) > 1 else 125  
    
    font_title = get_times_font("bold", 64)   
    font_id = get_times_font("bold", font_size_id)      
    font_event = get_times_font("italic", 32)    
    font_advance = get_times_font("bold", 110) 
    font_actions = get_times_font("bold", 110) 

    # -------------------------------------------------------------
    # TOP HEADER AXIS (LOCKED TO YOUR VERIFIED NUDGE COORDINATES)
    # -------------------------------------------------------------
    circle_x, circle_y = 512, 112
    final_id_x = circle_x + 5
    final_id_y = circle_y - 2 if len(id_str) == 1 else circle_y - 12 
    
    draw.text((final_id_x, final_id_y), id_str, fill="white", font=font_id, anchor="mm")
    draw.text((center_x, 255), title.upper(), fill="white", font=font_title, anchor="mm")

    # -------------------------------------------------------------
    # ZONE 1: EVENTS ZONE TEXT
    # -------------------------------------------------------------
    words = event_text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line + " " + word) < 42:
            current_line += " " + word if current_line else word
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    
    y_offset = 520 if len(lines) == 1 else 495
    for line in lines:
        draw.text((center_x, y_offset), line, fill="black", font=font_event, anchor="mm")
        y_offset += 45

    # -------------------------------------------------------------
    # ZONE 2: ADVANCE ZONE
    # -------------------------------------------------------------
    clean_advance = advance_marker.strip().upper()
    
    if clean_advance in ["", "NONE", "NO FRONTS ADVANCE"]:
        draw.text((center_x, 1060), "No Fronts Advance", fill="black", font=font_event, anchor="mm")
    else:
        advance_color = (139, 0, 0, 255) 
        charcoal_border = (50, 50, 50, 255) 
        
        markers = [m.strip() for m in advance_marker.split(",") if m.strip()]
        num_boxes = len(markers)
        
        box_w, box_h = 180, 180
        gap = 35
        y_center = 1060  
        
        total_width = (num_boxes * box_w) + ((num_boxes - 1) * gap)
        start_x = center_x - (total_width // 2)
        
        for i, marker in enumerate(markers):
            box_left = start_x + (i * (box_w + gap))
            box_right = box_left + box_w
            box_top = y_center - (box_h // 2)
            box_bottom = y_center + (box_h // 2)
            
            # Render a heavy, clean border frame
            draw.rectangle([box_left, box_top, box_right, box_bottom], outline=charcoal_border, width=5)
            box_center_x = box_left + (box_w // 2)
            
            if len(marker) > 1 and marker[-1].isdigit():
                base_letter = marker[:-1]
                num = marker[-1]
                draw.text((box_center_x - 18, y_center), base_letter, fill=advance_color, font=font_advance, anchor="mm")
                font_super = get_times_font("bold", 55)
                draw.text((box_center_x + 35, y_center - 35), num, fill=advance_color, font=font_super, anchor="mm")
            else:
                font_current = get_times_font("bold", 90) if len(marker) > 1 else font_advance
                draw.text((box_center_x, y_center), marker, fill=advance_color, font=font_current, anchor="mm")

    # -------------------------------------------------------------
    # ZONE 3: ACTIONS ZONE
    # -------------------------------------------------------------
    y_actions_center = 1380  
    box_size = 90  
    green_left = center_x - box_size
    green_right = center_x + box_size
    green_top = y_actions_center - box_size
    green_bottom = y_actions_center + box_size
    
    draw.rectangle([green_left, green_top, green_right, green_bottom], fill=(0, 100, 8, 255), outline="white", width=4)
    draw.text((center_x, 1375), str(action_points), fill="white", font=font_actions, anchor="mm")

    output_filename = f"card_{card_id}_{title.lower().replace(' ', '_').strip()}.png"
    card.save(output_filename)
    print(f"Success! Compiled pristine asset: {output_filename}")
