import os
import requests
import json
from typing import List, Dict, Any
from urllib.parse import quote

class ResearchService:
    def __init__(self):
        """Инициализация сервиса поиска исследований"""
        self.pubmed_base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        self.clinical_trials_base_url = "https://clinicaltrials.gov/api/query"
        self.fda_base_url = "https://api.fda.gov"
    
    def search_pubmed(self, drug_name: str, condition: str = "") -> List[Dict[str, Any]]:
        """Поиск исследований в PubMed"""
        try:
            # Формируем поисковый запрос
            if condition:
                search_term = f'"{drug_name}"[Title/Abstract] AND "{condition}"[MeSH Terms] AND ("randomized controlled trial"[Publication Type] OR "meta-analysis"[Publication Type] OR "systematic review"[Publication Type])'
            else:
                search_term = f'"{drug_name}"[Title/Abstract] AND ("randomized controlled trial"[Publication Type] OR "meta-analysis"[Publication Type] OR "systematic review"[Publication Type])'
            
            # Поиск статей
            search_url = f"{self.pubmed_base_url}/esearch.fcgi"
            search_params = {
                'db': 'pubmed',
                'term': search_term,
                'retmax': 5,
                'retmode': 'json'
            }
            
            response = requests.get(search_url, params=search_params, timeout=10)
            if not response.ok:
                return []
            
            search_data = response.json()
            pmids = search_data.get('esearchresult', {}).get('idlist', [])
            
            if not pmids:
                return []
            
            # Получаем детали статей
            summary_url = f"{self.pubmed_base_url}/esummary.fcgi"
            summary_params = {
                'db': 'pubmed',
                'id': ','.join(pmids),
                'retmode': 'json'
            }
            
            response = requests.get(summary_url, params=summary_params, timeout=10)
            if not response.ok:
                return []
            
            summary_data = response.json()
            articles = []
            
            for pmid in pmids:
                if pmid in summary_data.get('result', {}):
                    article_data = summary_data['result'][pmid]
                    articles.append({
                        'pmid': pmid,
                        'title': article_data.get('title', ''),
                        'authors': ', '.join([author.get('name', '') for author in article_data.get('authors', [])[:3]]),
                        'journal': article_data.get('fulljournalname', ''),
                        'year': article_data.get('pubdate', '').split()[0] if article_data.get('pubdate') else '',
                        'type': self._determine_study_type(article_data.get('title', '')),
                        'url': f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                    })
            
            return articles
        
        except Exception as e:
            print(f"Ошибка при поиске в PubMed: {str(e)}")
            return []
    
    def search_clinical_trials(self, drug_name: str, condition: str = "") -> List[Dict[str, Any]]:
        """Поиск клинических исследований"""
        try:
            # Формируем поисковый запрос
            search_terms = [drug_name]
            if condition:
                search_terms.append(condition)
            
            search_url = f"{self.clinical_trials_base_url}/study_fields"
            params = {
                'expr': ' AND '.join(search_terms),
                'fields': 'NCTId,BriefTitle,OverallStatus,Phase,Condition,InterventionName',
                'min_rnk': 1,
                'max_rnk': 5,
                'fmt': 'json'
            }
            
            response = requests.get(search_url, params=params, timeout=10)
            if not response.ok:
                return []
            
            data = response.json()
            studies = []
            
            for study in data.get('StudyFieldsResponse', {}).get('StudyFields', []):
                nct_id = study.get('NCTId', [''])[0]
                title = study.get('BriefTitle', [''])[0]
                status = study.get('OverallStatus', [''])[0]
                phase = study.get('Phase', [''])[0]
                
                studies.append({
                    'nctId': nct_id,
                    'title': title,
                    'status': status,
                    'phase': phase,
                    'url': f"https://clinicaltrials.gov/ct2/show/{nct_id}"
                })
            
            return studies
        
        except Exception as e:
            print(f"Ошибка при поиске клинических исследований: {str(e)}")
            return []
    
    def search_fda(self, drug_name: str) -> List[Dict[str, Any]]:
        """Поиск информации в базе FDA"""
        try:
            search_url = f"{self.fda_base_url}/drug/drugsfda.json"
            params = {
                'search': f'products.active_ingredients.name:"{drug_name}"',
                'limit': 3
            }
            
            response = requests.get(search_url, params=params, timeout=10)
            if not response.ok:
                return []
            
            data = response.json()
            results = []
            
            for result in data.get('results', []):
                application_number = result.get('application_number', '')
                sponsor_name = result.get('sponsor_name', '')
                
                results.append({
                    'applicationNumber': application_number,
                    'sponsorName': sponsor_name,
                    'url': f"https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm?event=overview.process&ApplNo={application_number}"
                })
            
            return results
        
        except Exception as e:
            print(f"Ошибка при поиске в FDA: {str(e)}")
            return []
    
    def _determine_study_type(self, title: str) -> str:
        """Определение типа исследования по заголовку"""
        title_lower = title.lower()
        
        if 'meta-analysis' in title_lower or 'meta analysis' in title_lower:
            return 'Meta-analysis'
        elif 'systematic review' in title_lower:
            return 'Systematic Review'
        elif 'randomized controlled trial' in title_lower or 'rct' in title_lower:
            return 'RCT'
        elif 'clinical trial' in title_lower:
            return 'Clinical Trial'
        else:
            return 'Study'

