import os
import asyncio
from jinja2 import Environment, FileSystemLoader
from playwright.async_api import async_playwright
from content import get_all_content, get_toc_entries

async def generate_pdf():
    print("Starting PDF Generation with Playwright...")
    
    # 1. Setup paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(base_dir, 'templates')
    output_dir = os.path.join(base_dir, 'output')
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 2. Get content and TOC
    print("Loading content...")
    content_html = get_all_content()
    toc = get_toc_entries()
    
    # 3. Render HTML with Jinja2
    print("Rendering HTML template...")
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template('report_template.html')
    
    rendered_html = template.render(
        content=content_html,
        toc_entries=toc
    )
    
    html_path = os.path.join(output_dir, 'temp_report.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(rendered_html)
    
    # 4. Generate PDF with Playwright
    print("Converting HTML to PDF with Playwright...")
    output_pdf_path = os.path.join(output_dir, 'SIH_26155_NEXUS_Master_Report.pdf')
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        file_uri = f"file:///{html_path.replace('\\\\', '/')}"
        await page.goto(file_uri, wait_until="networkidle")
        
        await page.pdf(
            path=output_pdf_path,
            format="A4",
            print_background=True,
            display_header_footer=True,
            header_template="<div style='font-size: 8px; color: #888; padding-left: 2cm;'>SIH 26155 -- NEXUS Master Report</div>",
            footer_template="<div style='font-size: 8px; color: #888; width: 100%; display: flex; justify-content: space-between; padding-left: 2cm; padding-right: 2cm;'><span>Page <span class='pageNumber'></span> of <span class='totalPages'></span></span><span>Confidential -- Team NEXUS</span></div>",
            margin={"top": "2.5cm", "right": "2cm", "bottom": "2.5cm", "left": "2cm"}
        )
        await browser.close()
    
    print(f"\\nSUCCESS! PDF generated at: {output_pdf_path}")
    file_size_mb = os.path.getsize(output_pdf_path) / (1024 * 1024)
    print(f"File Size: {file_size_mb:.2f} MB")

if __name__ == '__main__':
    asyncio.run(generate_pdf())
