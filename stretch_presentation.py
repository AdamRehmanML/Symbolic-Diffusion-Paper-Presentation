import glob
import re
import os

def scale_wait(match):
    w = float(match.group(1))
    
    if w < 0.5:
        new_w = round(w * 2.0, 1)
    elif w <= 1.5:
        new_w = round(w * 4.4, 1)
    else:
        new_w = round(w * 7.5, 1)
        
    return f"self.wait({new_w})"

if __name__ == "__main__":
    files = glob.glob('scene_*.py') + ['main.py']
    
    for f in files:
        with open(f, 'r') as file:
            content = file.read()
            
        new_content = re.sub(r'self\.wait\(([\d\.]+)\)', scale_wait, content)
        
        if content != new_content:
            with open(f, 'w') as file:
                file.write(new_content)
            print(f"Stretched presentation times in {f}")

