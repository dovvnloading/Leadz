# -*- coding: utf-8 -*-
import json
import re 
import ollama
import requests
from bs4 import BeautifulSoup
from ddgs import DDGS

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from PySide6.QtCore import QThread, Signal

from config import (LLM_MODEL, EMBEDDING_MODEL, SEARCH_RESULTS_COUNT, 
                    TOP_N_PAGES_TO_ANALYZE, SIMILARITY_THRESHOLD)

class JobSearchWorker(QThread):
    status_update = Signal(str)
    job_found = Signal(dict)
    finished = Signal()

    def __init__(self, query):
        super().__init__()
        self.query = query
        self.is_running = True
        try:
            self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        except Exception as e:
            print(f"ERROR: Could not load embedding model: {e}")
            self.status_update.emit(f"Error loading embedding model: {e}")
            self.is_running = False

    def run(self):
        if not self.is_running:
            self.finished.emit()
            return
            
        max_attempts = 2
        jobs_found_count = 0
        attempt = 1
        MINIMUM_JOBS_THRESHOLD = 3

        try:
            while attempt <= max_attempts:
                is_retry = (attempt > 1)

                if is_retry:
                    self.status_update.emit("Initial search yielded few results. Retrying with a more targeted approach...")
                    print("\n" + "-"*50)
                    print("RETRYING SEARCH: Using more targeted queries.")
                    print("-"*50)
                else:
                    print("\n" + "="*50)
                    print(f"Starting search for: '{self.query}'")
                    print("="*50)

                self.status_update.emit("Step 1/5: Generating intelligent search queries...")
                search_queries = self._generate_intelligent_search_queries(is_retry=is_retry)
                if not search_queries:
                    self.status_update.emit("Error: Could not generate search queries from your request.")
                    break 
                print(f"Step 1 complete: Generated {len(search_queries)} intelligent queries.")

                self.status_update.emit("Step 2/5: Searching the web...")
                search_results = self._conduct_web_search(search_queries)
                if not search_results:
                    self.status_update.emit("Error: Web search found no results.")
                    attempt += 1
                    continue
                print(f"Step 2 complete: Found {len(search_results)} unique URLs.")

                self.status_update.emit("Step 3/5: Fetching pages...")
                cleaned_pages = self._retrieve_and_clean_pages(search_results)
                if not cleaned_pages:
                    self.status_update.emit("Error: Failed to fetch content from websites.")
                    attempt += 1
                    continue
                print(f"Step 3 complete: Cleaned {len(cleaned_pages)} pages.")

                self.status_update.emit("Step 4/5: Ranking & filtering pages...")
                top_pages = self._rank_retrieved_data(cleaned_pages)
                if not top_pages:
                    self.status_update.emit("Could not find relevant pages after filtering.")
                    attempt += 1
                    continue
                print(f"Step 4 complete: Selected top {len(top_pages)} relevant pages.")

                self.status_update.emit("Step 5/5: Analyzing job listings for relevance...")
                found_jobs = self._extract_structured_data(top_pages)
                for job in found_jobs:
                    self.job_found.emit(job)
                    jobs_found_count += 1
                print("Step 5 complete.")

                if jobs_found_count >= MINIMUM_JOBS_THRESHOLD or attempt == max_attempts:
                    break
                
                attempt += 1

        except Exception as e:
            print(f"ERROR: {e}")
            self.status_update.emit(f"An unexpected error occurred: {e}")
        finally:
            self.status_update.emit("Search complete!")
            self.finished.emit()
            print("="*50)

    def _clean_and_parse_json(self, raw_json_string):
        match = re.search(r'```json\s*(\{.*?\})\s*```', raw_json_string, re.DOTALL)
        if match:
            clean_json = match.group(1)
        else:
            curly_brace_start = raw_json_string.find('{')
            curly_brace_end = raw_json_string.rfind('}')
            if curly_brace_start != -1 and curly_brace_end != -1:
                clean_json = raw_json_string[curly_brace_start:curly_brace_end+1]
            else:
                raise ValueError("No JSON found")
        return json.loads(clean_json)

    def _generate_intelligent_search_queries(self, is_retry=False):
        if is_retry:
            retry_prompt_addon = """
            The previous broad search attempt yielded insufficient results. 
            Generate a new set of queries that are more specific. 
            Focus on constructing queries that explicitly target known job boards and career pages by using the 'site:' operator (e.g., site:linkedin.com, site:greenhouse.io, site:lever.co).
            Ensure every generated query includes a 'site:' restriction.
            """
        else:
            retry_prompt_addon = """
            The queries should be suitable for a general web search, like Google or DuckDuckGo.
            Include synonyms, related technologies, and variations in job titles. Add terms like "careers", "jobs", or "hiring" to improve results.
            """

        prompt = f"""
        You are an expert technical recruiter and search specialist.
        Analyze the following user query and generate a JSON list of 3-5 diverse, high-quality search engine queries to find relevant job postings online.
        Infer the job title, key skills, location, and experience level from the user's query.
        {retry_prompt_addon}

        User's query: "{self.query}"

        Example output for a query like "Senior Python Developer, Remote, New York":
        {{
            "queries": [
                "senior python developer remote jobs new york",
                "python backend engineer careers nyc remote",
                "lead software developer python django hiring remote",
                "remote senior backend developer jobs (python or django) united states"
            ]
        }}

        Respond ONLY with the JSON object containing the "queries" list.
        """
        try:
            response = ollama.chat(model=LLM_MODEL, messages=[{'role': 'user', 'content': prompt}], format="json")
            data = self._clean_and_parse_json(response['message']['content'])
            return data.get("queries", [])
        except Exception as e:
            print(f"Error generating intelligent queries: {e}")
            return []

    def _conduct_web_search(self, search_queries):
        all_results = []
        seen_urls = set()
        site_restriction = "(site:linkedin.com OR site:indeed.com OR site:glassdoor.com OR site:greenhouse.io OR site:lever.co OR site:wellfound.com)"
        
        num_queries_to_run = 0
        for q in search_queries:
            num_queries_to_run += 1
            if "site:" not in q:
                num_queries_to_run +=1

        results_per_search = max(1, SEARCH_RESULTS_COUNT // num_queries_to_run if num_queries_to_run > 0 else SEARCH_RESULTS_COUNT)

        def perform_search(query):
            try:
                with DDGS() as ddgs:
                    print(f"Searching with: '{query}'")
                    results = list(ddgs.text(query, max_results=results_per_search))
                    for r in results:
                        if 'href' in r and r['href'] not in seen_urls:
                            all_results.append({'href': r['href']})
                            seen_urls.add(r['href'])
            except Exception as e:
                print(f"DDGS search for query '{query}' failed: {e}")

        print("\n--- Starting Hybrid Search ---")
        for query in search_queries:
            perform_search(query)
            if "site:" not in query:
                final_query = f"{query} {site_restriction}"
                perform_search(final_query)
        
        return all_results

    def _retrieve_and_clean_pages(self, search_results):
        pages = []
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        for result in search_results:
            url = result['href']
            try:
                response = requests.get(url, headers=headers, timeout=7)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
                    tag.extract()
                text = soup.get_text(separator=' ', strip=True)
                if len(text) > 300:
                    pages.append({'url': url, 'text': text})
            except:
                pass 
        return pages

    def _rank_retrieved_data(self, pages):
        if not pages: 
            return []
        page_texts = [page['text'] for page in pages]
        query_embedding = self.embedding_model.encode([self.query])
        page_embeddings = self.embedding_model.encode(page_texts)
        similarities = cosine_similarity(query_embedding, page_embeddings)[0]
        
        ranked_pages = sorted(zip(pages, similarities), key=lambda x: x[1], reverse=True)
        
        relevant_pages = []
        for page, score in ranked_pages:
            if score >= SIMILARITY_THRESHOLD:
                relevant_pages.append(page)

        return relevant_pages[:TOP_N_PAGES_TO_ANALYZE]

    def _extract_structured_data(self, top_pages):
        found_jobs = []
        for i, page in enumerate(top_pages):
            self.status_update.emit(f"Step 5/5: Analyzing job {i+1}/{len(top_pages)} for relevance...")
            
            prompt = f"""
            The user is searching for a job with this query: "{self.query}"

            Analyze the text below. First, determine if it contains a job posting highly relevant to the user's query.
            - If NO relevant job is found, respond ONLY with the JSON: {{"is_relevant": false}}
            - If a relevant job IS found, extract its details into the following JSON structure. 
            - Use "N/A" for any missing fields.
            - The 'skills' field should be a list of 3-5 key technologies or qualifications.
            - The 'summary' field should be 2-3 sentences.

            {{
                "is_relevant": true,
                "jobTitle": "...",
                "company": "...",
                "location": "...",
                "salary": "...",
                "job_type": "Full-time | Part-time | Contract | N/A",
                "experience": "Entry-level | Mid-level | Senior | N/A",
                "skills": ["...", "...", "..."],
                "summary": "..."
            }}

            Respond ONLY with the JSON object.

            Text: ---
            {page['text'][:4000]}
            ---
            """
            try:
                response = ollama.chat(model=LLM_MODEL, messages=[{'role': 'user', 'content': prompt}], format="json")
                job_data = self._clean_and_parse_json(response['message']['content'])

                if job_data.get('is_relevant'):
                    job_data['url'] = page['url']
                    found_jobs.append(job_data)
                    print(f"  -> Found relevant job: {job_data.get('jobTitle')}")
                else:
                    print(f"  -> Skipping irrelevant content on {page['url']}")

            except Exception as e:
                print(f"Error extracting data from {page['url']}: {e}")
        return found_jobs