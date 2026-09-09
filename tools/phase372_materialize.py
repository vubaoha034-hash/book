from pathlib import Path
import base64, zlib, json

ROOT = Path(__file__).resolve().parents[1]
parts = [
    (ROOT / 'tools/.phase372_payload_0').read_text(encoding='utf-8').strip(),
    (ROOT / 'tools/.phase372_payload_1').read_text(encoding='utf-8').strip(),
    (ROOT / 'tools/.phase372_payload_2').read_text(encoding='utf-8').strip(),
]
parts.extend((ROOT / f'tools/.phase372_payload_3_{i}').read_text(encoding='utf-8').strip() for i in range(8))
parts.append((ROOT / 'tools/.phase372_payload_4').read_text(encoding='utf-8').strip())
payload = ''.join(parts)
files = json.loads(zlib.decompress(base64.b64decode(payload)).decode('utf-8'))

required = {
    'state/calibration/PHASE372_BOOK01_READER_EXPERIENCE_CARDS_V1.jsonl': 30,
    'state/calibration/PHASE372_BOOK02_READER_EXPERIENCE_CARDS_V1.jsonl': 30,
    'state/calibration/PHASE372_BOOK03_READER_EXPERIENCE_CARDS_V1.jsonl': 30,
}
required_fields = {
    'book_id','source_anchor','scene_identity','reader_question_or_expectation_before',
    'immediate_character_objective','pressure_or_uncertainty_source','what_information_is_visible_now',
    'what_information_is_withheld','why_withholding_is_not_confusion','state_change_per_beat',
    'voice_or_prose_surface_signal','reader_reward_or_new_question','exit_energy','dimension_tags',
    'failure_boundary','portable_mechanism_candidate'
}
for rel, content in files.items():
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding='utf-8')

for rel, expected in required.items():
    rows = [json.loads(x) for x in (ROOT / rel).read_text(encoding='utf-8').splitlines() if x.strip()]
    assert len(rows) == expected, (rel, len(rows))
    for row in rows:
        assert required_fields.issubset(row), (rel, row.get('card_id'))
        assert all(row.get(k) not in ('', None, []) for k in required_fields)
print('PHASE372_MATERIALIZED_OK')
