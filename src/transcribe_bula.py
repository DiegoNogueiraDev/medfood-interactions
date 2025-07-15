from unstructured.partition.pdf import partition_pdf

def transcribe_bula(pdf_path):
    blocks = partition_pdf(pdf_path, strategy="hi_res")
    
    transcribed_text = []
    for block in blocks:
        if hasattr(block, 'text') and block.text.strip():
            transcribed_text.append(block.text)
    
    return '\n'.join(transcribed_text)

if __name__ == "__main__":
    pdf_file = "bula.pdf"
    transcribed_content = transcribe_bula(pdf_file)
    
    with open("bula_transcribed.txt", "w", encoding="utf-8") as f:
        f.write(transcribed_content)
    
    print(f"Transcrição salva em bula_transcribed.txt")
    print(f"Total de caracteres: {len(transcribed_content)}")