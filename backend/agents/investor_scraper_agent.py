#!/usr/bin/env python3
"""
Investor Scraper Agent for Daena AI VP System
Scrapes investor emails from various sources and scores them
"""

import requests
import json
import re
import time
import logging
from typing import List, Dict, Any
from datetime import datetime
from urllib.parse import urljoin, urlparse
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InvestorScraperAgent:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Scoring weights
        self.scoring_weights = {
            'location_match': 0.3,  # Toronto, Canada
            'domain_fit': 0.4,      # AI, SaaS, Tech
            'contact_quality': 0.2,  # Email presence, contact page
            'source_reliability': 0.1 # Source credibility
        }
        
        # Target sources
        self.sources = {
            'cvca': {
                'base_url': 'https://cvca.ca',
                'search_paths': ['/members', '/investors', '/venture-capital'],
                'reliability': 0.9
            },
            'marsdd': {
                'base_url': 'https://marsdd.com',
                'search_paths': ['/ventures', '/investors', '/partners'],
                'reliability': 0.8
            },
            'angel': {
                'base_url': 'https://angel.co',
                'search_paths': ['/investors', '/toronto', '/ai'],
                'reliability': 0.7
            },
            'crunchbase': {
                'base_url': 'https://crunchbase.com',
                'search_paths': ['/organizations', '/investors', '/toronto'],
                'reliability': 0.8
            }
        }
        
        # Keywords for scoring
        self.location_keywords = ['toronto', 'canada', 'ontario', 'gta']
        self.domain_keywords = ['ai', 'artificial intelligence', 'machine learning', 'saas', 'software', 'tech', 'technology', 'startup', 'venture']
        
    def scrape_investors(self, max_results: int = 50) -> List[Dict[str, Any]]:
        """Main method to scrape investors from all sources"""
        logger.info("🕵️ Starting investor scraping process...")
        
        all_investors = []
        
        for source_name, source_config in self.sources.items():
            try:
                logger.info(f"Scraping from {source_name}...")
                investors = self._scrape_source(source_name, source_config, max_results // len(self.sources))
                all_investors.extend(investors)
                time.sleep(1)  # Be respectful to servers
            except Exception as e:
                logger.error(f"Error scraping {source_name}: {str(e)}")
                continue
        
        # Score and sort investors
        scored_investors = self._score_investors(all_investors)
        scored_investors.sort(key=lambda x: x['score'], reverse=True)
        
        # Limit results
        final_investors = scored_investors[:max_results]
        
        logger.info(f"✅ Scraped {len(final_investors)} investors with scores")
        return final_investors
    
    def _scrape_source(self, source_name: str, source_config: Dict, max_per_source: int) -> List[Dict[str, Any]]:
        """Scrape investors from a specific source"""
        investors = []
        
        for path in source_config['search_paths']:
            try:
                url = urljoin(source_config['base_url'], path)
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                
                # Extract investor information from page
                page_investors = self._extract_investors_from_page(
                    response.text, 
                    source_name, 
                    source_config['base_url'],
                    source_config['reliability']
                )
                
                investors.extend(page_investors)
                
                if len(investors) >= max_per_source:
                    break
                    
            except Exception as e:
                logger.warning(f"Error scraping {url}: {str(e)}")
                continue
        
        return investors[:max_per_source]
    
    def _extract_investors_from_page(self, html_content: str, source: str, base_url: str, reliability: float) -> List[Dict[str, Any]]:
        """Extract investor information from HTML content"""
        investors = []
        
        # Email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        # Name patterns (various formats)
        name_patterns = [
            r'<h[1-6][^>]*>([^<]+(?:investor|partner|principal|managing)[^<]*)</h[1-6]>',
            r'<div[^>]*class="[^"]*(?:name|title)[^"]*"[^>]*>([^<]+)</div>',
            r'<span[^>]*class="[^"]*(?:name|title)[^"]*"[^>]*>([^<]+)</span>'
        ]
        
        # Find emails
        emails = re.findall(email_pattern, html_content)
        
        # Find potential names near emails
        for email in emails:
            # Look for names near the email
            email_index = html_content.find(email)
            if email_index == -1:
                continue
                
            # Extract surrounding text
            start = max(0, email_index - 200)
            end = min(len(html_content), email_index + 200)
            surrounding_text = html_content[start:end]
            
            # Try to find a name
            name = self._extract_name_from_text(surrounding_text, email)
            
            if name and email:
                investor = {
                    'name': name,
                    'email': email,
                    'source': source,
                    'source_url': base_url,
                    'reliability': reliability,
                    'raw_text': surrounding_text[:100] + '...',
                    'scraped_at': datetime.now().isoformat()
                }
                investors.append(investor)
        
        # Also look for investor listings without emails
        for pattern in name_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            for match in matches:
                # Clean up the match
                name = re.sub(r'<[^>]+>', '', match).strip()
                if len(name) > 3 and len(name) < 100:
                    investor = {
                        'name': name,
                        'email': '',  # No email found
                        'source': source,
                        'source_url': base_url,
                        'reliability': reliability,
                        'raw_text': match[:100] + '...',
                        'scraped_at': datetime.now().isoformat()
                    }
                    investors.append(investor)
        
        return investors
    
    def _extract_name_from_text(self, text: str, email: str) -> str:
        """Extract a name from text near an email"""
        # Remove HTML tags
        clean_text = re.sub(r'<[^>]+>', ' ', text)
        
        # Look for patterns like "Name <email>" or "email (Name)"
        patterns = [
            rf'([A-Z][a-z]+ [A-Z][a-z]+)\s*[<\[{email}[>\]]',
            rf'[<\[{email}[>\]]\s*\(([A-Z][a-z]+ [A-Z][a-z]+)\)',
            rf'([A-Z][a-z]+ [A-Z][a-z]+)\s+{email}',
            rf'{email}\s+([A-Z][a-z]+ [A-Z][a-z]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, clean_text)
            if match:
                return match.group(1).strip()
        
        # Fallback: look for capitalized words near email
        words = clean_text.split()
        email_index = -1
        for i, word in enumerate(words):
            if email in word:
                email_index = i
                break
        
        if email_index >= 0:
            # Look for capitalized words before email
            for i in range(max(0, email_index - 3), email_index):
                if i < len(words) and words[i] and words[i][0].isupper():
                    if i + 1 < len(words) and words[i + 1] and words[i + 1][0].isupper():
                        return f"{words[i]} {words[i + 1]}"
                    return words[i]
        
        return "Unknown Investor"
    
    def _score_investors(self, investors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Score investors based on various criteria"""
        scored_investors = []
        
        for investor in investors:
            score = 0
            notes = []
            
            # Location scoring
            location_score = self._calculate_location_score(investor)
            score += location_score * self.scoring_weights['location_match']
            if location_score > 0:
                notes.append("Location match")
            
            # Domain fit scoring
            domain_score = self._calculate_domain_score(investor)
            score += domain_score * self.scoring_weights['domain_fit']
            if domain_score > 0:
                notes.append("Domain fit")
            
            # Contact quality scoring
            contact_score = self._calculate_contact_score(investor)
            score += contact_score * self.scoring_weights['contact_quality']
            if contact_score > 0:
                notes.append("Good contact info")
            
            # Source reliability
            source_score = investor.get('reliability', 0.5)
            score += source_score * self.scoring_weights['source_reliability']
            notes.append(f"Source: {investor.get('source', 'unknown')}")
            
            # Add score and notes to investor
            investor['score'] = round(score, 2)
            investor['notes'] = ', '.join(notes)
            investor['status'] = 'scraped'
            
            scored_investors.append(investor)
        
        return scored_investors
    
    def _calculate_location_score(self, investor: Dict[str, Any]) -> float:
        """Calculate location match score"""
        text = f"{investor.get('name', '')} {investor.get('raw_text', '')}".lower()
        
        for keyword in self.location_keywords:
            if keyword in text:
                return 1.0
        
        return 0.0
    
    def _calculate_domain_score(self, investor: Dict[str, Any]) -> float:
        """Calculate domain fit score"""
        text = f"{investor.get('name', '')} {investor.get('raw_text', '')}".lower()
        
        matches = 0
        for keyword in self.domain_keywords:
            if keyword in text:
                matches += 1
        
        return min(matches / len(self.domain_keywords), 1.0)
    
    def _calculate_contact_score(self, investor: Dict[str, Any]) -> float:
        """Calculate contact quality score"""
        score = 0.0
        
        # Email presence
        if investor.get('email'):
            score += 0.8
        
        # Contact page or other contact info
        if 'contact' in investor.get('raw_text', '').lower():
            score += 0.2
        
        return min(score, 1.0)
    
    def save_results(self, investors: List[Dict[str, Any]], filename: str = None) -> str:
        """Save scraped results to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"logs/scraped_investors_{timestamp}.json"
        
        # Ensure logs directory exists
        os.makedirs("logs", exist_ok=True)
        
        results = {
            'scraped_at': datetime.now().isoformat(),
            'total_investors': len(investors),
            'sources_used': list(self.sources.keys()),
            'investors': investors
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Saved {len(investors)} investors to {filename}")
        return filename
    
    def get_mock_investors(self) -> List[Dict[str, Any]]:
        """Get mock investors for testing/demo purposes"""
        mock_investors = [
            {
                'name': 'Sarah Chen',
                'email': 'sarah.chen@torontovc.com',
                'source': 'cvca',
                'source_url': 'https://cvca.ca',
                'reliability': 0.9,
                'score': 0.85,
                'notes': 'Location match, Domain fit, Good contact info, Source: cvca',
                'status': 'scraped',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'name': 'Michael Rodriguez',
                'email': 'm.rodriguez@aiaccelerator.ca',
                'source': 'marsdd',
                'source_url': 'https://marsdd.com',
                'reliability': 0.8,
                'score': 0.92,
                'notes': 'Location match, Domain fit, Good contact info, Source: marsdd',
                'status': 'scraped',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'name': 'Jennifer Kim',
                'email': 'jennifer@techfund.ca',
                'source': 'angel',
                'source_url': 'https://angel.co',
                'reliability': 0.7,
                'score': 0.78,
                'notes': 'Location match, Domain fit, Good contact info, Source: angel',
                'status': 'scraped',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'name': 'David Thompson',
                'email': 'david@saasventures.com',
                'source': 'crunchbase',
                'source_url': 'https://crunchbase.com',
                'reliability': 0.8,
                'score': 0.88,
                'notes': 'Location match, Domain fit, Good contact info, Source: crunchbase',
                'status': 'scraped',
                'scraped_at': datetime.now().isoformat()
            }
        ]
        
        return mock_investors

# Global instance
investor_scraper = InvestorScraperAgent()

def run_scraper(max_results: int = 20, use_mock: bool = True) -> Dict[str, Any]:
    """Main function to run the investor scraper"""
    try:
        if use_mock:
            logger.info("🕵️ Using mock investor data for demo")
            investors = investor_scraper.get_mock_investors()
        else:
            logger.info("🕵️ Starting real investor scraping...")
            investors = investor_scraper.scrape_investors(max_results)
        
        # Save results
        filename = investor_scraper.save_results(investors)
        
        return {
            'status': 'success',
            'message': f'Successfully scraped {len(investors)} investors',
            'investors': investors,
            'filename': filename,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in investor scraper: {str(e)}")
        return {
            'status': 'error',
            'message': f'Error scraping investors: {str(e)}',
            'investors': [],
            'timestamp': datetime.now().isoformat()
        }

if __name__ == "__main__":
    # Test the scraper
    result = run_scraper(use_mock=True)
    print(json.dumps(result, indent=2)) 