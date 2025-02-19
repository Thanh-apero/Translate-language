from translator_core import escape_xml_string

test_strings = [
    'Enable <b>Full Screen Intent</b> for the best app experience & instant updates.',
    'Continue>>',
    'All',
    '(%1$s Photos)',
    "It's working",
    "Save & Continue"
]

print('\nTesting Android string escaping:\n')
for s in test_strings:
    print(f'Original: {s}')
    print(f'Escaped:  {escape_xml_string(s)}\n') 