import os
import re

def fix_imports(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # regex replace `import { Card, CardHeader... }` with `import Card, { CardHeader... }`
    # or `import { Card }` with `import Card`
    
    # For Card with other named imports
    new_content = re.sub(r'import\s*{\s*Card\s*,\s*(.*?)\s*}\s*from\s*[\'"]@/components/ui/Card[\'"]', 
                         r'import Card, { \1 } from "@/components/ui/Card"', content)
    
    # For just Card
    new_content = re.sub(r'import\s*{\s*Card\s*}\s*from\s*[\'"]@/components/ui/Card[\'"]', 
                         r'import Card from "@/components/ui/Card"', new_content)
                         
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed {filepath}")

for root, _, files in os.walk(r'd:\Hack2Skill\Berunda\apps\web\src'):
    for f in files:
        if f.endswith(('.tsx', '.ts')):
            fix_imports(os.path.join(root, f))
