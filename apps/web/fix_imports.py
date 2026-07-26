import os

def fix_imports(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    replacements = {
        "import { Button } from '@/components/ui/Button'": "import Button from '@/components/ui/Button'",
        "import { Button } from '@/components/ui/Button';": "import Button from '@/components/ui/Button';",
        "import { Badge } from '@/components/ui/Badge'": "import Badge from '@/components/ui/Badge'",
        "import { Badge } from '@/components/ui/Badge';": "import Badge from '@/components/ui/Badge';",
        "import { Input } from '@/components/ui/Input'": "import Input from '@/components/ui/Input'",
        "import { Input } from '@/components/ui/Input';": "import Input from '@/components/ui/Input';",
    }
    
    new_content = content
    for old, new in replacements.items():
        new_content = new_content.replace(old, new)
        
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed {filepath}")

for root, _, files in os.walk(r'd:\Hack2Skill\Berunda\apps\web\src'):
    for f in files:
        if f.endswith(('.tsx', '.ts')):
            fix_imports(os.path.join(root, f))
