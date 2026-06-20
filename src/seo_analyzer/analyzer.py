import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from dataclasses import dataclass, field
from typing import Optional, List
import re
import time
import json


@dataclass
class SEOReport:
    url: str
    status_code: int
    
    # Basic SEO
    title: Optional[str] = None
    title_length: int = 0
    meta_description: Optional[str] = None
    meta_description_length: int = 0
    
    # Headings
    h1_count: int = 0
    h2_count: int = 0
    h3_count: int = 0
    
    # Links
    total_links: int = 0
    internal_links: int = 0
    external_links: int = 0
    nofollow_links: int = 0
    broken_links: List[str] = field(default_factory=list)
    
    # Images
    total_images: int = 0
    images_with_alt: int = 0
    images_without_alt: int = 0
    
    # Technical
    page_size_kb: float = 0.0
    has_canonical: bool = False
    canonical_url: Optional[str] = None
    has_viewport: bool = False
    has_charset: bool = False
    language: Optional[str] = None
    has_favicon: bool = False
    is_https: bool = False
    
    # Performance
    load_time_seconds: float = 0.0
    ttfb_seconds: float = 0.0  # Time to First Byte
    
    # Content
    word_count: int = 0
    paragraph_count: int = 0
    
    # Security Headers
    security_headers: dict = field(default_factory=dict)
    has_strict_transport: bool = False
    has_content_security: bool = False
    has_x_frame_options: bool = False
    
    # Social Media
    has_og_tags: bool = False
    og_title: Optional[str] = None
    og_description: Optional[str] = None
    og_image: Optional[str] = None
    has_twitter_card: bool = False
    
    # Robots
    robots_meta: Optional[str] = None
    is_indexable: bool = True
    
    # Schema
    has_schema: bool = False
    schema_types: List[str] = field(default_factory=list)
    
    # Score
    seo_score: int = 0
    issues: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    passed: List[str] = field(default_factory=list)


class SEOAnalyzer:
    def __init__(self, url: str):
        self.url = url
        self.domain = urlparse(url).netloc
        self.soup: Optional[BeautifulSoup] = None
        self.response: Optional[requests.Response] = None
        
    def fetch_page(self) -> bool:
        """Fetch the web page with performance metrics"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        try:
            start_time = time.time()
            self.response = requests.get(self.url, headers=headers, timeout=15, allow_redirects=True)
            end_time = time.time()
            
            self.response.raise_for_status()
            self.soup = BeautifulSoup(self.response.text, 'html.parser')
            
            # Calculate performance metrics
            if hasattr(self.response, 'elapsed'):
                self.ttfb = self.response.elapsed.total_seconds()
            self.load_time = end_time - start_time
            
            return True
        except requests.exceptions.Timeout:
            print(f"❌ Timeout: The request took too long")
            return False
        except requests.exceptions.ConnectionError:
            print(f"❌ Connection Error: Could not connect to {self.url}")
            return False
        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP Error: {e}")
            return False
        except Exception as e:
            print(f"❌ Error fetching page: {e}")
            return False
    
    def _analyze_title(self, report: SEOReport):
        """Analyze title tag"""
        title_tag = self.soup.find('title')
        if title_tag and title_tag.string:
            report.title = title_tag.string.strip()
            report.title_length = len(report.title)
            
            if report.title_length == 0:
                report.issues.append("Title tag is empty")
            elif report.title_length < 30:
                report.warnings.append(f"Title is too short ({report.title_length} chars, recommended: 30-60)")
            elif report.title_length > 60:
                report.warnings.append(f"Title is too long ({report.title_length} chars, recommended: 30-60)")
            else:
                report.passed.append(f"Title length is optimal ({report.title_length} chars)")
        else:
            report.issues.append("Missing title tag")
    
    def _analyze_meta_description(self, report: SEOReport):
        """Analyze meta description"""
        meta = self.soup.find('meta', attrs={'name': 'description'})
        if meta and meta.get('content'):
            report.meta_description = meta['content'].strip()
            report.meta_description_length = len(report.meta_description)
            
            if report.meta_description_length < 120:
                report.warnings.append(f"Meta description is too short ({report.meta_description_length} chars, recommended: 120-160)")
            elif report.meta_description_length > 160:
                report.warnings.append(f"Meta description is too long ({report.meta_description_length} chars, recommended: 120-160)")
            else:
                report.passed.append(f"Meta description length is optimal ({report.meta_description_length} chars)")
        else:
            report.issues.append("Missing meta description")
    
    def _analyze_headings(self, report: SEOReport):
        """Analyze heading structure"""
        report.h1_count = len(self.soup.find_all('h1'))
        report.h2_count = len(self.soup.find_all('h2'))
        report.h3_count = len(self.soup.find_all('h3'))
        
        if report.h1_count == 0:
            report.issues.append("Missing H1 tag")
        elif report.h1_count > 1:
            report.warnings.append(f"Multiple H1 tags found ({report.h1_count}), recommended: 1")
        else:
            report.passed.append("H1 tag structure is correct")
    
    def _analyze_links(self, report: SEOReport):
        """Analyze links and check for broken links"""
        all_links = self.soup.find_all('a', href=True)
        report.total_links = len(all_links)
        
        # Check first 10 links for broken links (to save time)
        links_to_check = all_links[:10]
        
        for link in all_links:
            href = link['href']
            full_url = urljoin(self.url, href)
            
            if urlparse(full_url).netloc == self.domain:
                report.internal_links += 1
            else:
                report.external_links += 1
            
            if link.get('rel') and 'nofollow' in link.get('rel'):
                report.nofollow_links += 1
        
        # Check for broken links (sample)
        for link in links_to_check:
            href = link['href']
            if href.startswith(('http://', 'https://')):
                try:
                    response = requests.head(href, timeout=5, allow_redirects=True)
                    if response.status_code >= 400:
                        report.broken_links.append(href)
                except:
                    pass
        
        if report.broken_links:
            report.warnings.append(f"Found {len(report.broken_links)} broken links (sample of 10)")
    
    def _analyze_images(self, report: SEOReport):
        """Analyze images"""
        images = self.soup.find_all('img')
        report.total_images = len(images)
        report.images_with_alt = len([img for img in images if img.get('alt') and img['alt'].strip()])
        report.images_without_alt = report.total_images - report.images_with_alt
        
        if report.images_without_alt > 0:
            report.warnings.append(f"{report.images_without_alt} images missing alt text")
        elif report.total_images > 0:
            report.passed.append("All images have alt text")
    
    def _analyze_technical(self, report: SEOReport):
        """Analyze technical SEO elements"""
        report.page_size_kb = len(self.response.content) / 1024
        report.is_https = self.url.startswith('https://')
        report.load_time_seconds = self.load_time
        report.ttfb_seconds = self.ttfb
        
        # Canonical
        canonical = self.soup.find('link', rel='canonical')
        if canonical:
            report.has_canonical = True
            report.canonical_url = canonical.get('href')
            report.passed.append("Canonical URL is set")
        
        # Viewport
        viewport = self.soup.find('meta', attrs={'name': 'viewport'})
        if viewport:
            report.has_viewport = True
            report.passed.append("Viewport meta tag is set (mobile-friendly)")
        else:
            report.issues.append("Missing viewport meta tag (not mobile-friendly)")
        
        # Charset
        charset = self.soup.find('meta', attrs={'charset': True})
        if charset:
            report.has_charset = True
        
        # Language
        html_tag = self.soup.find('html')
        if html_tag and html_tag.get('lang'):
            report.language = html_tag['lang']
            report.passed.append(f"Language attribute is set ({report.language})")
        else:
            report.warnings.append("Missing language attribute in <html> tag")
        
        # Favicon
        favicon = self.soup.find('link', rel=lambda x: x and 'icon' in x)
        if favicon:
            report.has_favicon = True
            report.passed.append("Favicon is set")
        else:
            report.warnings.append("Missing favicon")
    
    def _analyze_content(self, report: SEOReport):
        """Analyze content"""
        # Word count
        text = self.soup.get_text()
        words = text.split()
        report.word_count = len(words)
        
        # Paragraph count
        report.paragraph_count = len(self.soup.find_all('p'))
        
        if report.word_count < 300:
            report.warnings.append(f"Low word count ({report.word_count} words, recommended: 300+)")
        elif report.word_count > 0:
            report.passed.append(f"Good content length ({report.word_count} words)")
    
    def _analyze_security(self, report: SEOReport):
        """Analyze security headers"""
        headers = self.response.headers
        
        # Strict-Transport-Security
        if 'strict-transport-security' in headers:
            report.has_strict_transport = True
            report.security_headers['strict-transport-security'] = headers['strict-transport-security']
        
        # Content-Security-Policy
        if 'content-security-policy' in headers:
            report.has_content_security = True
            report.security_headers['content-security-policy'] = headers['content-security-policy']
        
        # X-Frame-Options
        if 'x-frame-options' in headers:
            report.has_x_frame_options = True
            report.security_headers['x-frame-options'] = headers['x-frame-options']
        
        if report.has_strict_transport:
            report.passed.append("HSTS header is set")
        else:
            report.warnings.append("Missing HSTS header")
    
    def _analyze_social(self, report: SEOReport):
        """Analyze social media tags"""
        # Open Graph
        og_tags = self.soup.find_all('meta', attrs={'property': re.compile(r'^og:')})
        if og_tags:
            report.has_og_tags = True
            for tag in og_tags:
                prop = tag.get('property')
                if prop == 'og:title':
                    report.og_title = tag.get('content')
                elif prop == 'og:description':
                    report.og_description = tag.get('content')
                elif prop == 'og:image':
                    report.og_image = tag.get('content')
            report.passed.append("Open Graph tags are set")
        else:
            report.warnings.append("Missing Open Graph tags (for social media)")
        
        # Twitter Card
        twitter_tags = self.soup.find_all('meta', attrs={'name': re.compile(r'^twitter:')})
        if twitter_tags:
            report.has_twitter_card = True
            report.passed.append("Twitter Card tags are set")
        else:
            report.warnings.append("Missing Twitter Card tags")
    
    def _analyze_robots(self, report: SEOReport):
        """Analyze robots meta"""
        robots = self.soup.find('meta', attrs={'name': 'robots'})
        if robots and robots.get('content'):
            report.robots_meta = robots['content']
            if 'noindex' in report.robots_meta.lower():
                report.is_indexable = False
                report.issues.append("Page is set to noindex (not indexable)")
            else:
                report.passed.append("Page is indexable")
        else:
            report.passed.append("Page is indexable (no robots meta restrictions)")
    
    def _analyze_schema(self, report: SEOReport):
        """Analyze Schema.org markup"""
        schema_scripts = self.soup.find_all('script', type='application/ld+json')
        if schema_scripts:
            report.has_schema = True
            for script in schema_scripts:
                try:
                    data = json.loads(script.string)
                    if isinstance(data, dict) and '@type' in data:
                        report.schema_types.append(data['@type'])
                except:
                    pass
            report.passed.append(f"Schema markup found: {', '.join(report.schema_types)}")
        else:
            report.warnings.append("No Schema.org markup found")
    
    def _calculate_score(self, report: SEOReport):
        """Calculate SEO score (0-100)"""
        score = 0
        
        # Title (15 points)
        if report.title and 30 <= report.title_length <= 60:
            score += 15
        elif report.title:
            score += 8
        
        # Meta Description (15 points)
        if report.meta_description and 120 <= report.meta_description_length <= 160:
            score += 15
        elif report.meta_description:
            score += 8
        
        # H1 (10 points)
        if report.h1_count == 1:
            score += 10
        elif report.h1_count > 0:
            score += 5
        
        # HTTPS (10 points)
        if report.is_https:
            score += 10
        
        # Viewport (10 points)
        if report.has_viewport:
            score += 10
        
        # Images with alt (10 points)
        if report.total_images > 0 and report.images_without_alt == 0:
            score += 10
        elif report.total_images == 0:
            score += 10
        
        # Canonical (5 points)
        if report.has_canonical:
            score += 5
        
        # Language (5 points)
        if report.language:
            score += 5
        
        # Open Graph (5 points)
        if report.has_og_tags:
            score += 5
        
        # Schema (5 points)
        if report.has_schema:
            score += 5
        
        # Indexable (10 points)
        if report.is_indexable:
            score += 10
        
        report.seo_score = score
    
    def analyze(self) -> Optional[SEOReport]:
        """Analyze the page completely"""
        if not self.fetch_page():
            return None
        
        report = SEOReport(
            url=self.url,
            status_code=self.response.status_code
        )
        
        # Run all analyses
        self._analyze_title(report)
        self._analyze_meta_description(report)
        self._analyze_headings(report)
        self._analyze_links(report)
        self._analyze_images(report)
        self._analyze_technical(report)
        self._analyze_content(report)
        self._analyze_security(report)
        self._analyze_social(report)
        self._analyze_robots(report)
        self._analyze_schema(report)
        
        # Calculate score
        self._calculate_score(report)
        
        return report
    
    def print_report(self, report: SEOReport):
        """Print the complete SEO report"""
        print(f"\n{'='*70}")
        print(f"📊 SEO Report for: {report.url}")
        print(f"{'='*70}\n")
        
        # SEO Score
        if report.seo_score >= 80:
            score_emoji = "🟢"
        elif report.seo_score >= 50:
            score_emoji = "🟡"
        else:
            score_emoji = "🔴"
        
        print(f"{score_emoji} SEO SCORE: {report.seo_score}/100")
        print(f"{'─'*70}\n")
        
        # Basic SEO
        print("📌 BASIC SEO")
        print(f"{'─'*70}")
        print(f"  Title: {report.title or '❌ Missing'}")
        if report.title:
            print(f"  Title Length: {report.title_length} chars", end="")
            if 30 <= report.title_length <= 60:
                print(" ✅")
            else:
                print(" ⚠️")
        
        print(f"  Meta Description: {report.meta_description[:80] + '...' if report.meta_description and len(report.meta_description) > 80 else (report.meta_description or '❌ Missing')}")
        if report.meta_description:
            print(f"  Description Length: {report.meta_description_length} chars", end="")
            if 120 <= report.meta_description_length <= 160:
                print(" ✅")
            else:
                print(" ⚠️")
        
        # Headings
        print(f"\n📌 HEADINGS")
        print(f"{'─'*70}")
        print(f"  H1: {report.h1_count}  |  H2: {report.h2_count}  |  H3: {report.h3_count}")
        
        # Links
        print(f"\n📌 LINKS")
        print(f"{'─'*70}")
        print(f"  Total: {report.total_links}  |  Internal: {report.internal_links}  |  External: {report.external_links}  |  Nofollow: {report.nofollow_links}")
        if report.broken_links:
            print(f"  ❌ Broken Links: {len(report.broken_links)}")
        
        # Images
        print(f"\n📌 IMAGES")
        print(f"{'─'*70}")
        print(f"  Total: {report.total_images}  |  With Alt: {report.images_with_alt} ✅  |  Without Alt: {report.images_without_alt} ❌")
        
        # Content
        print(f"\n📌 CONTENT")
        print(f"{'─'*70}")
        print(f"  Word Count: {report.word_count}")
        print(f"  Paragraphs: {report.paragraph_count}")
        
        # Technical
        print(f"\n📌 TECHNICAL")
        print(f"{'─'*70}")
        print(f"  HTTPS: {'✅ Yes' if report.is_https else '❌ No'}")
        print(f"  Page Size: {report.page_size_kb:.2f} KB", end="")
        if report.page_size_kb > 500:
            print(" ⚠️")
        else:
            print(" ✅")
        print(f"  Load Time: {report.load_time_seconds:.2f}s  |  TTFB: {report.ttfb_seconds:.2f}s")
        print(f"  Viewport: {'✅ Yes' if report.has_viewport else '❌ No'}")
        print(f"  Canonical: {'✅ ' + report.canonical_url if report.has_canonical else '❌ No'}")
        print(f"  Language: {report.language or '❌ Not set'}")
        print(f"  Favicon: {'✅ Yes' if report.has_favicon else '❌ No'}")
        print(f"  Indexable: {'✅ Yes' if report.is_indexable else '❌ No (noindex)'}")
        
        # Security
        print(f"\n📌 SECURITY")
        print(f"{'─'*70}")
        print(f"  HSTS: {'✅ Yes' if report.has_strict_transport else '❌ No'}")
        print(f"  CSP: {'✅ Yes' if report.has_content_security else '❌ No'}")
        print(f"  X-Frame-Options: {'✅ Yes' if report.has_x_frame_options else '❌ No'}")
        
        # Social Media
        print(f"\n📌 SOCIAL MEDIA")
        print(f"{'─'*70}")
        print(f"  Open Graph: {'✅ Yes' if report.has_og_tags else '❌ No'}")
        print(f"  Twitter Card: {'✅ Yes' if report.has_twitter_card else '❌ No'}")
        
        # Schema
        print(f"\n📌 STRUCTURED DATA")
        print(f"{'─'*70}")
        if report.has_schema:
            print(f"  Schema Types: {', '.join(report.schema_types)}")
        else:
            print(f"  ❌ No Schema.org markup found")
        
        # Summary
        print(f"\n📌 SUMMARY")
        print(f"{'─'*70}")
        if report.issues:
            print(f"  ❌ Issues ({len(report.issues)}):")
            for issue in report.issues:
                print(f"     • {issue}")
        
        if report.warnings:
            print(f"  ⚠️  Warnings ({len(report.warnings)}):")
            for warning in report.warnings:
                print(f"     • {warning}")
        
        if report.passed:
            print(f"  ✅ Passed ({len(report.passed)}):")
            for passed in report.passed:
                print(f"     • {passed}")
        
        print(f"\n{'='*70}\n")