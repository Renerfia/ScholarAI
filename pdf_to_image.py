

def pdf_to_image(pdf_path):
    import fitz  # PyMuPDF
    import os

    output_folder = f"data\\processed_images" #you can change this to your desired output folder
    os.makedirs(output_folder, exist_ok=True)
    
    doc = fitz.open(pdf_path)

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        output_path = os.path.join(output_folder, f"page_{page_num + 1}.jpg")
        pix.save(output_path)
        print(f"Saved: {output_path}")
    
