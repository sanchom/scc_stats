from cached_scc import CachedSCC

import datetime
import logging
import time
import random
import sys

logging.basicConfig(level=logging.INFO)

def render_docket_links(docket_nos):
    url_base = 'https://www.scc-csc.ca/case-dossier/info/parties-eng.aspx?cas={}'
    link_text = ''
    for i, docket_no in enumerate(docket_nos, start=1):
        url = url_base.format(docket_no)
        link_text += ' [[{}]]({})'.format(i, url)
    return link_text

def render_docket_links_for_pollen(docket_nos):
    url_base = 'https://www.scc-csc.ca/case-dossier/info/parties-eng.aspx?cas={}'
    link_text = ''
    for i, docket_no in enumerate(docket_nos, start=1):
        url = url_base.format(docket_no)
        link_text += ' [◊a[#:href "{}"]{{{}}}]'.format(url, i)
    return link_text

def render_interveners(interveners):
    x = '<ul>'
    for i in interveners:
        x += '<li>{}</li>'.format(i)
    x += '</ul>'
    return x

def render_interveners_for_pollen(interveners, docket_nos):
    x = '◊ul{'
    for i in interveners:
        x += '◊li{{{}}}'.format(i)
    x += '}'
    x += '◊p[\'((class "small-screens-only"))]{{Details: {}}}'.format(render_docket_links_for_pollen(docket_nos))
    return x

def render_from(loc):
    if not loc:
        return 'None'
    parts = loc.split(',')
    translated_parts = []
    for p in parts:
        p = p.strip()
        if p == 'Federal Court of Appeal':
            translated_parts.append('FCA')
        elif p == 'Quebec':
            translated_parts.append('QC')
        elif p == 'Ontario':
            translated_parts.append('ON')
        elif p == 'Manitoba':
            translated_parts.append('MB')
        elif p == 'Nova Scotia':
            translated_parts.append('NS')
        elif p == 'British Columbia':
            translated_parts.append('BC')
        elif p == 'Saskatchewan':
            translated_parts.append('SK')
        elif p == 'Alberta':
            translated_parts.append('AB')
        elif p == 'Northwest Territories':
            translated_parts.append('NWT')
        elif p == 'Prince Edward Island':
            translated_parts.append('PE')
        elif p == 'Yukon':
            translated_parts.append('Y')
        elif p == 'Nunavut':
            translated_parts.append('NT')
        elif p == 'Newfoundland and Labrador':
            translated_parts.append('NL')
        elif p == 'Canada':
            translated_parts.append('Can')
        elif p == 'New Brunswick':
            translated_parts.append('NB')
        elif p == 'Court Martial Appeal Court of Canada':
            translated_parts.append('Ct Martial App Ct')
        else:
            raise Exception('unrecognized location: {}'.format(p))
    return ', '.join(translated_parts)

def print_pollen(decisions):
    for year in range(2009,2019):
        print('◊heading{{{}}}'.format(year))
        num_cases = len([key for (key, val) in decisions.items() if val['publication_date'].year == year])
        with_interventions = len([key for (key, val) in decisions.items() if val['publication_date'].year == year and val['interveners']])
        as_of_right_appeals = len([key for (key, val) in decisions.items() if val['publication_date'].year == year and val['as_of_right']])

        as_of_right_appeals_with_interventions = len([key for (key, val)
                                                      in decisions.items() if val['publication_date'].year == year and
                                                      val['as_of_right'] and val['interveners']])

        print('◊div[\'((class "full-width"))]{')
        print('◊table[\'((class "scc-stats full-width"))]{')
        print('◊tr{')
        print('◊th{Appeals decided}◊th{Appeals with interveners}◊th{Appeals as of right}◊th{Appeals as of right with interventions}')
        print('}')
        print('◊tr{')
        print('◊td{{{}}}◊td{{{}}}◊td{{{}}}◊td{{{}}}'.format(num_cases, with_interventions, as_of_right_appeals, as_of_right_appeals_with_interventions))
        print('}')
        print('}')
        print('}')

        print('◊div[\'((class "full-width"))]{')
        print('◊table[\'((class "scc-stats full-width"))]{')
        print('◊tr{')
        print('◊th{Citation}◊th{Criminal?}◊th[\'((class "as-of-right-column"))]{A.o.R.?' +
              '}◊th{Interveners}◊th[\'((class "no-print drop-on-small-screens"))]{Details}')
        print('}')
        for key, v in [(key, val) for (key, val) in decisions.items() if val['publication_date'].year == year]:
            print('◊tr{')
            print('◊td{{◊em{{◊a[#:href "{}"]{{{}}}}}, {}}}◊td{{{}}}◊td[\'((class "as-of-right-column"))]{{{}}}◊td[\'((class "intervener-cell"))]{{{}}}◊td[\'((class "no-print drop-on-small-screens"))]{{{}}}'.format(
                v['decision_url'], v['title'], key,
                'crim.' if v['criminal'] else '',
                'a.o.r.' if v['as_of_right'] else '',
                render_interveners_for_pollen(v['interveners'], v['docket_no']) if len(v['interveners']) else '',
                render_docket_links_for_pollen(v['docket_no'])))
            print('}')
        print('}')
        print('}')

def print_tsv(decisions):
    for key, v in decisions.items():
        print('{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(
            key, v['title'], v['decision_url'], v['appeal_from'],
            'criminal' if v['criminal'] else '', 'as of right' if v['as_of_right'] else '',
            len(v['interveners']) if len(v['interveners']) else ''))

def print_tsv_interveners(decisions):
    for key, v in decisions.items():
        if not v['interveners']:
            print('{}\t{}'.format(key, v['title']))
        else:
            for i in v['interveners']:
                print('{}\t{}\t{}'.format(key, v['title'], i))

def clean_up_intervener(intervener, intervener_to_class, equivalence_classes):
    results = []
    for (query, class_id) in intervener_to_class:
        if query in intervener:
            results.append(equivalence_classes[class_id][0])
            intervener = intervener.replace(query, '')
    intervener = intervener.strip(' ,/')
    if intervener.startswith('and'):
        intervener = intervener.replace('and', '')
    intervener = intervener.strip(' ,/')
    if intervener.startswith('et'):
        intervener = intervener.replace('et', '')
    if intervener.startswith('the'):
        intervener = intervener.replace('the', '')
    intervener = intervener.strip(' ,/')
    if len(intervener) > 0:
        results.append(intervener)
    return results

def clean_up_interveners(original_interveners, equivalence_classes):
    intervener_to_class = []
    for i, c in enumerate(equivalence_classes):
        for e in c:
            intervener_to_class.append((e, i))
    # Sorting these largest to smallest
    intervener_to_class = sorted(intervener_to_class, key=lambda e: len(e[0]), reverse=True)

    cleaned_up = []
    for i in original_interveners:
        cleaned_up.extend(clean_up_intervener(i, intervener_to_class, equivalence_classes))

    return cleaned_up

assert len(sys.argv) == 2, 'Failed to provide path to equivalence classes.'
equivalence_path = sys.argv[1]
f = open(equivalence_path, 'r')
data = f.read()
f.close()
equivalence_classes = []
this_group = []
for line in data.splitlines():
    if len(line) == 0:
        if (this_group):
            equivalence_classes.append(this_group)
        this_group = []
    else:
        this_group.append(line)
equivalence_classes = sorted(equivalence_classes, key=lambda group: group[0])

scc = CachedSCC('scc-cache.pkl')
decisions = {}
case_list = []
for year in range(2009, 2019):
    case_list.extend(scc.get_cases_from_year(year))

for c in case_list:
    d = scc.get_detailed_case_info(c['case_link'])
    interveners = clean_up_interveners(list(set(d['interveners'])), equivalence_classes)
    decisions[c['citation']] = {'title':c['title'],
                                'neutral_citation':c['citation'],
                                'publication_date':datetime.date.fromisoformat(c['published']),
                                'decision_pdf':c['pdf'],
                                'decision_url':c['case_link'],
                                'docket_no': d['docket_no'],
                                'appeal_from': d['on_appeal_from'],
                                'criminal': d['criminal'],
                                'as_of_right': d['as_of_right'],
                                'interveners': sorted(list(set(interveners)))}

print_tsv_interveners(decisions)
