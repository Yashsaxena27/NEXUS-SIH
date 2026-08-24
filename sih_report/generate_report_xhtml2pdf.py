import os
from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa
from content import get_all_content, get_toc_entries

def generate_pdf():
    print("Starting PDF Generation with xhtml2pdf...")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(base_dir, 'templates')
    output_dir = os.path.join(base_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    content_html = get_all_content()
    toc = get_toc_entries()
    
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template('report_template.html')
    
    rendered_html = template.render(
        content=content_html,
        toc_entries=toc
    )
    
    html_path = os.path.join(output_dir, 'temp_report.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(rendered_html)
    
    output_pdf_path = os.path.join(output_dir, 'SIH_26155_NEXUS_Master_Report.pdf')
    
    with open(output_pdf_path, "w+b") as result_file:
        # xhtml2pdf needs a link callback to resolve local paths
        def link_callback(uri, rel):
            # use absolute path
            if uri.startswith('../'):
                return os.path.join(base_dir, uri[3:])
            return uri
            
        pisa_status = pisa.CreatePDF(
            rendered_html,
            dest=result_file,
            link_callback=link_callback
        )
    
    if pisa_status.err:
        print("❌ Error generating PDF with xhtml2pdf")
    else:
        print(f"\\n✅ SUCCESS! PDF generated at: {output_pdf_path}")
        file_size_mb = os.path.getsize(output_pdf_path) / (1024 * 1024)
        print(f"File Size: {file_size_mb:.2f} MB")

if __name__ == '__main__':
    generate_pdf()
