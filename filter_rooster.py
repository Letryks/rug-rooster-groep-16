from pathlib import Path
from urllib.request import urlopen
import re

SOURCE = 'https://rooster.rug.nl/maat/api/2026-2027/schedule/fad329c2-0913-4eb4-b2d6-0fdb7b807aa2'
raw = urlopen(SOURCE, timeout=60).read().decode().replace('\r\n', '\n')
end = raw.index('END:VTIMEZONE\n') + len('END:VTIMEZONE\n')
output, pos = [raw[:end]], end
while True:
    start = raw.find('BEGIN:VEVENT\n', pos)
    if start < 0: break
    finish = raw.find('END:VEVENT\n', start) + len('END:VEVENT\n')
    event, pos = raw[start:finish], finish
    text = re.sub(r'\n[ \t]', '', event)
    match = re.search(r'^DESCRIPTION:(.*)$', text, re.MULTILINE)
    description = match.group(1) if match else ''
    grouped = re.search(r'(?:\bgr\.|\bgroep)\s*\d+', description, re.I)
    selected = re.search(r'(?:\bgr\.|\bgroep)\s*16\b', description, re.I) or re.search(r'(?:\bgr\.|\bgroep)\s*(?:0?1[0-6]|16)\s*-\s*(?:1[6-8]|[2-9]\d)\b', description, re.I)
    if not grouped or selected: output.append(event)
Path('rooster-groep-16.ics').write_text(''.join(output) + 'END:VCALENDAR\n')
