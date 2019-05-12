from cached_scc import CachedSCC

import datetime
import logging
import time
import random

logging.basicConfig(level=logging.INFO)

def render_docket_links(docket_nos):
    url_base = 'https://www.scc-csc.ca/case-dossier/info/parties-eng.aspx?cas={}'
    link_text = ''
    for i, docket_no in enumerate(docket_nos, start=1):
        url = url_base.format(docket_no)
        link_text += ' [[{}]]({})'.format(i, url)
    return link_text

def render_interveners(interveners):
    x = '<ul>'
    for i in interveners:
        x += '<li>{}</li>'.format(i)
    x += '</ul>'
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


def print_markdown(decisions):
    for year in range(2009, 2019):
        print('# {}'.format(year))
        num_cases = len([key for (key, val) in decisions.items() if val['publication_date'].year == year])
        with_interventions = len([key for (key, val) in decisions.items() if val['publication_date'].year == year and val['interveners']])
        as_of_right_appeals = len([key for (key, val) in decisions.items() if val['publication_date'].year == year and val['as_of_right']])

        as_of_right_appeals_with_interventions = len([key for (key, val)
                                                      in decisions.items() if val['publication_date'].year == year and
                                                      val['as_of_right'] and val['interveners']])

        print('|Total decisions|Decisions with interventions|Appeals as of right|Appeals as of right with interventions|')
        print('|---------------|----------------------------|-------------------|--------------------------------------|')
        print('| {} | {} ({:.2f}%) | {} | {} ({:.2f}%) |'.format(num_cases,
                                                       with_interventions,
                                                       100 * with_interventions / num_cases, as_of_right_appeals,
                                                       as_of_right_appeals_with_interventions,
                                                       100 * as_of_right_appeals_with_interventions / as_of_right_appeals))
        print()
        print('|Citation|From|Criminal?|As of right?|Interveners|Dockets|')
        print('|---------|----|---------|------------|-----------|-------|')
        for key, v in [(key, val) for (key, val) in decisions.items() if val['publication_date'].year == year]:
            print('| _[{}]({})_, {} | {} | {} | {} | {} | {} |'.format(
                v['title'], v['decision_url'], key, render_from(v['appeal_from']),
                'criminal' if v['criminal'] else '', 'as of right' if v['as_of_right'] else '',
                render_interveners(v['interveners']) if len(v['interveners']) else '',
                render_docket_links(v['docket_no'])))
        print()
        print()

def print_tsv(decisions):
    for key, v in decisions.items():
        print('{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(
            key, v['title'], v['decision_url'], v['appeal_from'],
            'criminal' if v['criminal'] else '', 'as of right' if v['as_of_right'] else '',
            len(v['interveners']) if len(v['interveners']) else ''))


scc = CachedSCC('scc-cache.pkl')
decisions = {}
case_list = []
for year in range(2009, 2019):
    case_list.extend(scc.get_cases_from_year(year))

for c in case_list:
    d = scc.get_detailed_case_info(c['case_link'])
    decisions[c['citation']] = {'title':c['title'],
                                'neutral_citation':c['citation'],
                                'publication_date':datetime.date.fromisoformat(c['published']),
                                'decision_pdf':c['pdf'],
                                'decision_url':c['case_link'],
                                'docket_no': d['docket_no'],
                                'appeal_from': d['on_appeal_from'],
                                'criminal': d['criminal'],
                                'as_of_right': d['as_of_right'],
                                'interveners': list(set(d['interveners']))}

print_markdown(decisions)
