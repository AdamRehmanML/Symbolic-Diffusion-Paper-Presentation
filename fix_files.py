import os
import glob
import re

def fix_yellow():
    for f in glob.glob("*.py"):
        with open(f, 'r') as file:
            content = file.read()
        
        # Replace ORANGE with ORANGE exactly
        new_content = re.sub(r'\bYELLOW\b', 'ORANGE', content)
        
        if content != new_content:
            with open(f, 'w') as file:
                file.write(new_content)
            print(f"Replaced ORANGE with ORANGE in {f}")

def remove_last_fadeout(filename):
    if not os.path.exists(filename):
        return
    with open(filename, 'r') as file:
        lines = file.readlines()
        
    for i in range(len(lines) - 1, -1, -1):
        if 'self.play(*[FadeOut(m) for m in self.mobjects])' in lines[i]:
            lines[i] = lines[i].replace('self.play(*[FadeOut(m) for m in self.mobjects])', '# self.play(*[FadeOut(m) for m in self.mobjects])')
            print(f"Commented out last FadeOut in {filename}")
            break
            
    with open(filename, 'w') as file:
        file.writelines(lines)

if __name__ == "__main__":
    fix_yellow()
    remove_last_fadeout("scene_03_diffusion_basics.py")
    remove_last_fadeout("scene_05_architecture.py")
    remove_last_fadeout("scene_08_results.py")
