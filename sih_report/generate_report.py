import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
from content import get_all_content, get_toc_entries

def generate_pdf():
    print("Starting PDF Generation...")
    
    # 1. Setup paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(base_dir, 'templates')
    styles_dir = os.path.join(base_dir, 'styles')
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
    
    # (Optional) Save HTML for debugging
    # with open(os.path.join(output_dir, 'debug_report.html'), 'w', encoding='utf-8') as f:
    #     f.write(rendered_html)
    
    # 4. Generate PDF with WeasyPrint
    print("Converting HTML to PDF with WeasyPrint (this may take a moment)...")
    output_pdf_path = os.path.join(output_dir, 'SIH_26155_NEXUS_Master_Report.pdf')
    
    # WeasyPrint needs the base_url to resolve local relative paths (like images/css)
    HTML(string=rendered_html, base_url=base_dir).write_pdf(
        output_pdf_path,
        stylesheets=[CSS(os.path.join(styles_dir, 'report.css'))]
    )
    
    print(f"\\n✅ SUCCESS! PDF generated at: {output_pdf_path}")
    
    # Print file size to verify
    file_size_mb = os.path.getsize(output_pdf_path) / (1024 * 1024)
    print(f"File Size: {file_size_mb:.2f} MB")

if __name__ == '__main__':
    generate_pdf()
