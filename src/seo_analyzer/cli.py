import argparse
import json
from dataclasses import asdict
from pathlib import Path
from datetime import datetime
from .analyzer import SEOAnalyzer
from .report_generator import HTMLReportGenerator


def analyze_single_url(url: str, output_dir: Path = None, generate_html: bool = False) -> dict:
    """Analyze a single URL and optionally save reports"""
    analyzer = SEOAnalyzer(url)
    report = analyzer.analyze()
    
    if not report:
        return {"url": url, "status": "failed", "error": "Could not analyze URL"}
    
    result = {
        "url": url,
        "status": "success",
        "score": report.seo_score,
        "report": asdict(report)
    }
    
    # Save reports if output directory is specified
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename from URL and timestamp
        domain = url.split('//')[-1].split('/')[0].replace('.', '_')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_filename = f"{domain}_{timestamp}"
        
        # Save JSON report
        json_path = output_dir / f"{base_filename}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(report), f, indent=2, ensure_ascii=False)
        result["json_file"] = str(json_path)
        
        # Save HTML report if requested
        if generate_html:
            html_path = output_dir / f"{base_filename}.html"
            HTMLReportGenerator.generate(report, str(html_path))
            result["html_file"] = str(html_path)
    
    return result


def main():
    """Main entry point for the CLI"""
    parser = argparse.ArgumentParser(
        description="🔍 SEO Analyzer - Analyze SEO metrics of web pages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single URL analysis
  seo-analyze https://example.com
  
  # Single URL with JSON output
  seo-analyze https://example.com --json
  
  # Single URL with HTML report
  seo-analyze https://example.com --html
  
  # Multiple URLs from file
  seo-analyze --file urls.txt --output-dir reports/
  
  # Multiple URLs with HTML reports
  seo-analyze --file urls.txt --output-dir reports/ --html
  
  # Multiple URLs from command line
  seo-analyze https://example.com https://google.com --output-dir reports/
        """
    )
    
    # Single URL or multiple URLs
    parser.add_argument(
        "urls", 
        nargs="*",
        help="One or more URLs to analyze"
    )
    parser.add_argument(
        "--file", 
        "-f",
        help="Path to a text file containing URLs (one per line)"
    )
    
    # Output options
    parser.add_argument(
        "--json", 
        action="store_true", 
        help="Output the report in JSON format (single URL only)"
    )
    parser.add_argument(
        "--html", 
        action="store_true", 
        help="Generate HTML report file(s)"
    )
    parser.add_argument(
        "--output-dir", 
        "-o",
        help="Directory to save reports (auto-creates if doesn't exist)"
    )
    
    args = parser.parse_args()
    
    # Collect URLs
    urls_to_analyze = []
    
    if args.file:
        # Read URLs from file
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"❌ File not found: {args.file}")
            exit(1)
        
        with open(file_path, 'r') as f:
            urls_to_analyze = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        print(f"📄 Loaded {len(urls_to_analyze)} URLs from {args.file}\n")
    
    if args.urls:
        urls_to_analyze.extend(args.urls)
    
    if not urls_to_analyze:
        parser.print_help()
        exit(1)
    
    # Single URL mode
    if len(urls_to_analyze) == 1 and not args.output_dir:
        url = urls_to_analyze[0]
        analyzer = SEOAnalyzer(url)
        report = analyzer.analyze()
        
        if report:
            if args.html:
                output_path = HTMLReportGenerator.generate(report, "seo_report.html")
                print(f"\n✅ HTML report generated successfully!")
                print(f"📄 Saved to: {output_path}\n")
            elif args.json:
                print(json.dumps(asdict(report), indent=2, ensure_ascii=False))
            else:
                analyzer.print_report(report)
        else:
            print("❌ Analysis failed. Please check the URL and try again.")
            exit(1)
    
    # Batch mode (multiple URLs or output directory specified)
    else:
        output_dir = Path(args.output_dir) if args.output_dir else Path("reports")
        
        print(f"🚀 Starting batch analysis of {len(urls_to_analyze)} URLs...")
        print(f"📁 Reports will be saved to: {output_dir}/\n")
        
        results = []
        for i, url in enumerate(urls_to_analyze, 1):
            print(f"[{i}/{len(urls_to_analyze)}] Analyzing: {url}")
            result = analyze_single_url(url, output_dir, args.html)
            results.append(result)
            
            if result["status"] == "success":
                print(f"   ✅ Score: {result['score']}/100")
                if args.html:
                    print(f"   📄 HTML: {result.get('html_file', 'N/A')}")
            else:
                print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
            print()
        
        # Generate summary
        successful = [r for r in results if r["status"] == "success"]
        failed = [r for r in results if r["status"] == "failed"]
        
        print("=" * 70)
        print("📊 BATCH ANALYSIS SUMMARY")
        print("=" * 70)
        print(f"✅ Successful: {len(successful)}")
        print(f"❌ Failed: {len(failed)}")
        
        if successful:
            avg_score = sum(r["score"] for r in successful) / len(successful)
            print(f"📈 Average Score: {avg_score:.1f}/100")
            
            # Show top and bottom performers
            sorted_results = sorted(successful, key=lambda x: x["score"], reverse=True)
            print(f"\n🏆 Best: {sorted_results[0]['url']} ({sorted_results[0]['score']}/100)")
            print(f"⚠️  Worst: {sorted_results[-1]['url']} ({sorted_results[-1]['score']}/100)")
        
        # Save summary JSON
        summary_path = output_dir / f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "total_urls": len(urls_to_analyze),
                "successful": len(successful),
                "failed": len(failed),
                "average_score": sum(r["score"] for r in successful) / len(successful) if successful else 0,
                "results": results
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Summary saved to: {summary_path}")
        print("=" * 70)


if __name__ == "__main__":
    main()