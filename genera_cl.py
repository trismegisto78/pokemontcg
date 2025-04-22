import json
import re
import os

# Paths to the deck JSON files
deck_paths = ['deck1.json', 'deck2.json']

# Accumulatore per carte uniche (key: tupla con nome, tipo, subtypes, hp)
unique_cards = {}
for path in deck_paths:
    with open(path, 'r', encoding='utf-8') as f:
        deck = json.load(f)
    for card in deck:
        key = (card['name'], card['cardType'], tuple(card.get('subtypes', [])), card.get('hp', None))
        unique_cards[key] = card  # sovrascrive duplicati, lasciando uno solo

# Preparo il contenuto del file delle classi
lines = []
lines.append("from core.card import PokemonBaseCard, PokemonStage1Card, PokemonStage2Card, TrainerCard, EnergyCard")
lines.append("from core.utils import mprint")
lines.append("")
for card in unique_cards.values():
    # Genera un nome di classe pulito
    cls = re.sub(r'\\W+', '', card['name'].title().replace(' ', '')) + "Card"
    # Determina la classe base
    if card['cardType'] == 'Pokemon':
        subs = card.get('subtypes', [])
        if 'Basic' in subs:
            base = 'PokemonBaseCard'
        elif any(s.lower().startswith('stage 1') for s in subs):
            base = 'PokemonStage1Card'
        elif any(s.lower().startswith('stage 2') for s in subs):
            base = 'PokemonStage2Card'
        else:
            base = 'PokemonBaseCard'
    elif card['cardType'] == 'Trainer':
        base = 'TrainerCard'
    else:
        base = 'EnergyCard'
    # Inizio definizione classe
    lines.append(f"class {cls}({base}):")
    lines.append("    def __init__(self, index):")
    # Super call con placeholder
    if base.startswith('Pokemon'):
        lines.append(f"        super().__init__(index, 'XXX', '{card['name']}', 'TYPE', {card.get('hp', 0)}, retreat_cost=0)")
    elif base == 'TrainerCard':
        lines.append(f"        super().__init__(index, 'XXX', '{card['name']}', 'Item')")
    else:  # EnergyCard
        etype = card.get('energyType', 'Basic')
        lines.append(f"        super().__init__(index, 'XXX', '{card['name']}', '{etype}')")
    lines.append("        # TODO: implement abilities and attacks according to JSON definition")
    lines.append("")

# Scrivo il file in core/pokemons_custom.py
output_path = './core/pokemons_custom.py'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

# Stampo un'anteprima delle prime 20 righe
print("\n".join(lines[:20]))

