from .analyzer import SEOReport
from datetime import datetime


class HTMLReportGenerator:
    """Generate beautiful HTML reports"""
    
    @staticmethod
    def generate(report: SEOReport, output_path: str = "seo_report.html") -> str:
        """Generate an HTML report and save it to a file"""
        
        # Determine score color
        if report.seo_score >= 80:
            score_color = "#10b981"  # Green
            score_status = "Excellent"
        elif report.seo_score >= 60:
            score_color = "#f59e0b"  # Yellow
            score_status = "Good"
        elif report.seo_score >= 40:
            score_color = "#f97316"  # Orange
            score_status = "Needs Improvement"
        else:
            score_color = "#ef4444"  # Red
            score_status = "Poor"
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEO Report - {report.url}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2em;
            margin-bottom: 10px;
        }}
        
        .header .url {{
            font-size: 1.1em;
            opacity: 0.9;
            word-break: break-all;
        }}
        
        .score-section {{
            text-align: center;
            padding: 40px;
            background: #f8f9fa;
        }}
        
        .score-circle {{
            width: 180px;
            height: 180px;
            border-radius: 50%;
            background: {score_color};
            color: white;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 0 auto 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }}
        
        .score-number {{
            font-size: 3.5em;
            font-weight: bold;
            line-height: 1;
        }}
        
        .score-label {{
            font-size: 1em;
            margin-top: 5px;
            opacity: 0.9;
        }}
        
        .score-status {{
            font-size: 1.5em;
            font-weight: 600;
            color: {score_color};
            margin-top: 10px;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 35px;
        }}
        
        .section-title {{
            font-size: 1.3em;
            font-weight: 600;
            color: #667eea;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e5e7eb;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
        }}
        
        .info-item {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }}
        
        .info-label {{
            font-size: 0.85em;
            color: #6b7280;
            margin-bottom: 5px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .info-value {{
            font-size: 1.1em;
            font-weight: 600;
            color: #1f2937;
            word-break: break-word;
        }}
        
        .status-good {{
            color: #10b981;
        }}
        
        .status-bad {{
            color: #ef4444;
        }}
        
        .status-warning {{
            color: #f59e0b;
        }}
        
        .summary-list {{
            list-style: none;
        }}
        
        .summary-list li {{
            padding: 12px 15px;
            margin-bottom: 8px;
            border-radius: 8px;
            display: flex;
            align-items: flex-start;
            gap: 10px;
        }}
        
        .summary-list li.issue {{
            background: #fee2e2;
            border-left: 4px solid #ef4444;
        }}
        
        .summary-list li.warning {{
            background: #fef3c7;
            border-left: 4px solid #f59e0b;
        }}
        
        .summary-list li.passed {{
            background: #d1fae5;
            border-left: 4px solid #10b981;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #6b7280;
            font-size: 0.9em;
            border-top: 1px solid #e5e7eb;
        }}
        
        @media (max-width: 600px) {{
            .header h1 {{
                font-size: 1.5em;
            }}
            
            .score-circle {{
                width: 140px;
                height: 140px;
            }}
            
            .score-number {{
                font-size: 2.5em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 SEO Analysis Report</h1>
            <div class="url">{report.url}</div>
            <div style="margin-top: 10px; font-size: 0.9em; opacity: 0.8;">
                Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </div>
        </div>
        
        <div class="score-section">
            <div class="score-circle">
                <div class="score-number">{report.seo_score}</div>
                <div class="score-label">/ 100</div>
            </div>
            <div class="score-status">{score_status}</div>
        </div>
        
        <div class="content">
            <!-- Basic SEO -->
            <div class="section">
                <div class="section-title">📌 Basic SEO</div>
                <div class="info-grid">
                    <div class="info-item">
                        <div class="info-label">Title</div>
                        <div class="info-value">
                            {report.title if report.title else '<span class="status-bad">❌ Missing</span>'}
                        </div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Title Length</div>
                        <div class="info-value">
                            {report.title_length} chars
                            {'✅' if 30 <= report.title_length <= 60 else '⚠️'}
                        </div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Meta Description</div>
                        <div class="info-value">
                            {report.meta_description[:100] + '...' if report.meta_description and len(report.meta_description) > 100 else (report.meta_description if report.meta_description else '<span class="status-bad">❌ Missing</span>')}
                        </div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Description Length</div>
                        <div class="info-value">
                            {report.meta_description_length} chars
                            {'✅' if 120 <= report.meta_description_length <= 160 else '⚠️'}
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Headings -->
            <div class="section">
                <div class="section-title">📌 Headings Structure</div>
                <div class="info-grid">
                    <div class="info-item">
                        <div class="info-label">H1 Tags</div>
                        <div class="info-value {'status-good' if report.h1_count == 1 else 'status-warning'}">{report.h1_count}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">H2 Tags</div>
                        <div class="info-value">{report.h2_count}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">H3 Tags</div>
                        <div class="info-value">{report.h3_count}</div>
                    </div>
                </div>
            </div>
            
            <!-- Links -->
            <div class="section">
                <div class="section-title">📌 Links Analysis</div>
                <div class="info-grid">
                    <div class="info-item">
                        <div class="info-label">Total Links</div>
                        <div class="info-value">{report.total_links}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Internal Links</div>
                        <div class="info-value">{report.internal_links}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">External Links</div>
                        <div class="info-value">{report.external_links}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Nofollow Links</div>
                        <div class="info-value">{report.nofollow_links}</div>
                    </div>
                </div>
            </div>
            
            <!-- Images -->
            <div class="section">
                <div class="section-title">📌 Images</div>
                <div class="info-grid">
                    <div class="info-item">
                        <div class="info-label">Total Images</div>
                        <div class="info-value">{report.total_images}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">With Alt Text</div>
                        <div class="info-value status-good">{report.images_with_alt} ✅</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Without Alt Text</div>
                        <div class="info-value {'status-bad' if report.images_without_alt > 0 else 'status-good'}">{report.images_without_alt} {'❌' if report.images_without_alt > 0 else '✅'}</div>
                    </div>
                </div>
            </div>
            
            <!-- Content -->
            <div class="section">
                <div class="section-title">📌 Content Analysis</div>
                <div class="info-grid">
                    <div class="info-item">
                        <div class="info-label">Word Count</div>
                        <div class="info-value {'status-good' if report.word_count >= 300 else 'status-warning'}">{report.word_count} words</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Paragraphs</div>
                        <div class="info-value">{report.paragraph_count}</div>
                    </div>
                </div>
            </div>
            
            <!-- Technical -->
            <div class="section">
                <div class="section-title">📌 Technical SEO</div>
                <div class="info-grid">
                    <div class="info-item">
                        <div class="info-label">HTTPS</div>
                        <div class="info-value {'status-good' if report.is_https else 'status-bad'}">{'✅ Yes' if report.is_https else '❌ No'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Page Size</div>
                        <div class="info-value {'status-warning' if report.page_size_kb > 500 else 'status-good'}">{report.page_size_kb:.2f} KB</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Viewport (Mobile)</div>
                        <div class="info-value {'status-good' if report.has_viewport else 'status-bad'}">{'✅ Yes' if report.has_viewport else '❌ No'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Canonical URL</div>
                        <div class="info-value {'status-good' if report.has_canonical else 'status-warning'}">{'✅ ' + report.canonical_url if report.has_canonical else '❌ Not set'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Language</div>
                        <div class="info-value {'status-good' if report.language else 'status-warning'}">{report.language if report.language else '❌ Not set'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Favicon</div>
                        <div class="info-value {'status-good' if report.has_favicon else 'status-warning'}">{'✅ Yes' if report.has_favicon else '❌ No'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Indexable</div>
                        <div class="info-value {'status-good' if report.is_indexable else 'status-bad'}">{'✅ Yes' if report.is_indexable else '❌ No (noindex)'}</div>
                                            <div class="info-item">
                        <div class="info-label">Load Time</div>
                        <div class="info-value {'status-warning' if report.load_time_seconds > 3 else 'status-good'}">{report.load_time_seconds:.2f}s</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">TTFB</div>
                        <div class="info-value">{report.ttfb_seconds:.2f}s</div>
                    </div>
             <!-- Security -->
            <div class="section">
                <div class="section-title">📌 Security Headers</div>
                <div class="info-grid">
                    <div class="info-item">
                        <div class="info-label">HSTS</div>
                        <div class="info-value {'status-good' if report.has_strict_transport else 'status-warning'}">{'✅ Yes' if report.has_strict_transport else '❌ No'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Content Security Policy</div>
                        <div class="info-value {'status-good' if report.has_content_security else 'status-warning'}">{'✅ Yes' if report.has_content_security else '❌ No'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">X-Frame-Options</div>
                        <div class="info-value {'status-good' if report.has_x_frame_options else 'status-warning'}">{'✅ Yes' if report.has_x_frame_options else '❌ No'}</div>
                    </div>
                </div>
            </div>
                    
                    </div>
                </div>
            </div>
            
            <!-- Social Media -->
            <div class="section">
                <div class="section-title">📌 Social Media Optimization</div>
                <div class="info-grid">
                    <div class="info-item">
                        <div class="info-label">Open Graph Tags</div>
                        <div class="info-value {'status-good' if report.has_og_tags else 'status-warning'}">{'✅ Yes' if report.has_og_tags else '❌ No'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Twitter Card</div>
                        <div class="info-value {'status-good' if report.has_twitter_card else 'status-warning'}">{'✅ Yes' if report.has_twitter_card else '❌ No'}</div>
                    </div>
                </div>
            </div>
            
            <!-- Structured Data -->
            <div class="section">
                <div class="section-title">📌 Structured Data</div>
                <div class="info-grid">
                    <div class="info-item">
                        <div class="info-label">Schema.org Markup</div>
                        <div class="info-value {'status-good' if report.has_schema else 'status-warning'}">
                            {'✅ ' + ', '.join(report.schema_types) if report.has_schema else '❌ Not found'}
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Summary -->
            <div class="section">
                <div class="section-title">📌 Summary & Recommendations</div>
                
                {'<h4 style="color: #ef4444; margin: 15px 0 10px;">❌ Critical Issues</h4><ul class="summary-list">' + ''.join([f'<li class="issue">{issue}</li>' for issue in report.issues]) + '</ul>' if report.issues else ''}
                
                {'<h4 style="color: #f59e0b; margin: 15px 0 10px;">⚠️ Warnings</h4><ul class="summary-list">' + ''.join([f'<li class="warning">{warning}</li>' for warning in report.warnings]) + '</ul>' if report.warnings else ''}
                
                {'<h4 style="color: #10b981; margin: 15px 0 10px;">✅ Passed Checks</h4><ul class="summary-list">' + ''.join([f'<li class="passed">{passed}</li>' for passed in report.passed]) + '</ul>' if report.passed else ''}
            </div>
        </div>
        
        <div class="footer">
            Generated by SEO Analyzer | Powered by Python 🐍
        </div>
    </div>
</body>
</html>"""
        
        # Save to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return output_path