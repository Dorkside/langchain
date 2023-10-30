import os
CHOICES = {}
for filename in os.listdir('prompts/'):
    with open(os.path.join('prompts/', filename), 'r') as f:
        CHOICES[filename] = f.read()