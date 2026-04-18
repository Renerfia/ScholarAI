

def pdf_to_image(pdf_path,password=None):
    import fitz  # PyMuPDF
    import os
    from pathlib import Path

    output_folder = Path("data/processed_images") #you can change this to your desired output folder
    os.makedirs(output_folder, exist_ok=True)
    
    doc = fitz.open(pdf_path)
    

    if doc.is_encrypted:
        
        try:
            doc.authenticate(password)
            print("PDF is encrypted, but authentication succeeded.")
            
        except Exception as e:
            print(f"Failed to authenticate PDF: {e}")
            return

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        output_path = output_folder / f"page_{page_num + 1}.jpg"
        pix.save(output_path)
        print(f"Saved: {output_path}")
    
    doc.close()
    
