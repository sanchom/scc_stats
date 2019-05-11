#!/bin/python3

from selenium import webdriver

import logging
import os
import pickle
import random
import re
import time

def is_number(x):
    return re.fullmatch(r"[0-9]+", x)

class CachedSCC:
    def __init__(self, cache_path=None):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('no-sandbox')
        options.add_argument('disable-gpu')
        self.driver = webdriver.Chrome(chrome_options=options)

        self.cache_path = cache_path
        if (cache_path and os.path.exists(cache_path)):
            self.cache = pickle.load(open(cache_path, 'rb'))
        else:
            self.cache = {'cases_from_year': {}}

    def get_detailed_case_info(self, decision_url):
        self.driver.implicitly_wait(10) # Will wait up to 10 seconds if the requested element is not found.
        if ('detailed_case_info' in self.cache and
            decision_url in self.cache['detailed_case_info']):
            return self.cache['detailed_case_info'][decision_url]
        else:
            time.sleep(random.uniform(1.0, 2.0))
            docket_no = None
            on_appeal_from = None
            criminal_or_civil = None
            type_of_appeal = None
            self.driver.get('{}?iframe=true'.format(decision_url))
            metadata = self.driver.find_element_by_class_name('metadata')
            fields = metadata.find_elements_by_xpath('.//table/tbody/tr')
            for f in fields:
                if f.find_element_by_class_name('label').get_attribute('innerText') == 'Case number':
                    docket_no = f.find_element_by_class_name('metadata').get_attribute('innerText')
                    if ',' in docket_no:
                        docket_no = [d.strip() for d in docket_no.split(',')]
                    else:
                        docket_no = [docket_no]
                if f.find_element_by_class_name('label').get_attribute('innerText') == 'On appeal from':
                    on_appeal_from = f.find_element_by_class_name('metadata').get_attribute('innerText')
            if not docket_no:
                # For some reason, we didn't find the "Case number" field. Looking for the Notes field instead.
                for f in fields:
                    if f.find_element_by_class_name('label').get_attribute('innerText') == 'Notes':
                        d_field = f.find_element_by_class_name('metadata').get_attribute('innerText')
                        docket_no = re.findall(r'[0-9]{5}', d_field)

            interveners = []
            assert(len(docket_no) >= 1)
            for d in docket_no:
                self.driver.get('https://www.scc-csc.ca/case-dossier/info/parties-eng.aspx?cas={}'.format(d))
                source_crim_leave = self.driver.find_element_by_xpath('//div[@id="wb-main-in"]/p[2]').get_attribute('innerText')
                matches = re.findall(r'\(.+?\)', source_crim_leave)
                source = matches[0][1:-1]
                criminal_or_civil = matches[1][1:-1]
                type_of_appeal = matches[2][1:-1]
                self.driver.implicitly_wait(0) # No waiting. We have the whole document.
                party_rows = self.driver.find_element_by_xpath('//div[@id="wb-main-in"]').find_element_by_class_name('wet-boew-zebra').find_elements_by_xpath('.//tbody/tr')
                for r in party_rows:
                    if r.find_elements_by_xpath('.//td') and r.find_element_by_xpath('.//td[2]').get_attribute('innerText') == 'Intervener':
                        interveners.append(r.find_element_by_xpath('.//td[1]').get_attribute('innerText'))
            detailed_info = {'docket_no': docket_no,
                             'on_appeal_from': on_appeal_from,
                             'criminal': criminal_or_civil == 'Criminal',
                             'as_of_right': type_of_appeal != 'By Leave',
                             'interveners': interveners}
            if (self.cache_path):
                if 'detailed_case_info' not in self.cache:
                    self.cache['detailed_case_info'] = {}
                self.cache['detailed_case_info'][decision_url] = detailed_info
                pickle.dump(self.cache, open(self.cache_path, 'wb'))
            return detailed_info

    def get_cases_from_year(self, year):
        self.driver.implicitly_wait(10) # Will wait up to 10 seconds if the requested element is not found.
        if (year in self.cache['cases_from_year']):
            logging.info('Getting cases from year from cache: {}.'.format(year))
            return self.cache['cases_from_year'][year]
        else:
            logging.info('Getting cases from year from SCC: {}.'.format(year))
            page_id = 1
            done = False
            judgements = []
            while not done:
                url = 'https://scc-csc.lexum.com/scc-csc/scc-csc/en/{}/nav_neu.do?page={}&iframe=true'.format(year, page_id)
                self.driver.get(url)
                for j in self.driver.find_elements_by_class_name('info'):
                    document_node = j.find_element_by_class_name('documents')
                    title = None; citation = None; published = None; pdf_link = None;
                    title = j.find_element_by_class_name('title').get_attribute('innerText')
                    case_link = j.find_element_by_xpath('.//a').get_attribute('href')
                    citation = j.find_element_by_class_name('citation').get_attribute('innerText')
                    published = j.find_element_by_class_name('publicationDate').get_attribute('innerText')
                    pdf_link = document_node.find_element_by_xpath('.//a[@title="Download the PDF version"]').get_attribute('href')
                    judgements.append({'title': title, 'citation': citation, 'published': published, 'case_link': case_link, 'pdf': pdf_link})

                pager = self.driver.find_element_by_class_name('pager')
                pages = sorted([int(p.text) for p in pager.find_elements_by_class_name('active') if is_number(p.text)])
                done = (page_id == pages[-1])
                page_id += 1
                time.sleep(random.uniform(1.0, 2.0))

            if (self.cache_path):
                self.cache['cases_from_year'][year] = judgements
                pickle.dump(self.cache, open(self.cache_path, 'wb'))
            
            return judgements
