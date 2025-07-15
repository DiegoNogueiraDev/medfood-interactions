from unstructured.partition.pdf import partition_pdf
from unstructured.chunking.title import chunk_by_title
import json

def enhanced_transcription(pdf_path):
    # Extrair com diferentes estratégias para maximizar captura
    elements = partition_pdf(
        pdf_path, 
        strategy="hi_res",
        infer_table_structure=True,
        extract_images_in_pdf=False,
        chunking_strategy="by_title"
    )
    
    # Organizar por seções
    structured_content = {
        "metadata": {
            "total_elements": len(elements),
            "extraction_method": "unstructured hi_res with table inference"
        },
        "sections": {},
        "full_text": "",
        "tables": [],
        "lists": []
    }
    
    current_section = "introduction"
    section_content = []
    
    for element in elements:
        text = element.text.strip() if hasattr(element, 'text') and element.text else ""
        if not text:
            continue
            
        category = element.category if hasattr(element, 'category') else 'unknown'
        
        # Identificar novas seções por títulos
        if category == "Title" and len(text) > 10:
            # Salvar seção anterior
            if section_content:
                structured_content["sections"][current_section] = {
                    "content": "\n".join(section_content),
                    "word_count": len(" ".join(section_content).split())
                }
            
            # Nova seção
            current_section = text.lower().replace(" ", "_").replace(":", "")[:50]
            section_content = [text]
        else:
            section_content.append(text)
        
        # Capturar listas e tabelas separadamente
        if category == "Table":
            structured_content["tables"].append(text)
        elif category == "ListItem":
            structured_content["lists"].append(text)
        
        structured_content["full_text"] += text + "\n"
    
    # Salvar última seção
    if section_content:
        structured_content["sections"][current_section] = {
            "content": "\n".join(section_content),
            "word_count": len(" ".join(section_content).split())
        }
    
    return structured_content

def compare_transcriptions():
    # Comparar método original vs enhanced
    print("=== COMPARAÇÃO DE MÉTODOS DE TRANSCRIÇÃO ===")
    
    # Método original
    original_elements = partition_pdf("bula.pdf", strategy="hi_res")
    original_text = "\n".join([elem.text for elem in original_elements if hasattr(elem, 'text') and elem.text])
    
    # Método enhanced
    enhanced_data = enhanced_transcription("bula.pdf")
    enhanced_text = enhanced_data["full_text"]
    
    print(f"Método original:")
    print(f"  - Caracteres: {len(original_text)}")
    print(f"  - Palavras: {len(original_text.split())}")
    print(f"  - Elementos: {len(original_elements)}")
    
    print(f"\nMétodo enhanced:")
    print(f"  - Caracteres: {len(enhanced_text)}")
    print(f"  - Palavras: {len(enhanced_text.split())}")
    print(f"  - Elementos: {enhanced_data['metadata']['total_elements']}")
    print(f"  - Seções identificadas: {len(enhanced_data['sections'])}")
    print(f"  - Tabelas: {len(enhanced_data['tables'])}")
    print(f"  - Listas: {len(enhanced_data['lists'])}")
    
    # Verificar se enhanced capturou mais conteúdo
    improvement = len(enhanced_text) - len(original_text)
    print(f"\nMelhoria: {improvement} caracteres ({improvement/len(original_text)*100:.1f}%)")
    
    return enhanced_data

if __name__ == "__main__":
    enhanced_data = compare_transcriptions()
    
    # Salvar transcrição estruturada
    with open("bula_enhanced_transcription.json", "w", encoding="utf-8") as f:
        json.dump(enhanced_data, f, ensure_ascii=False, indent=2)
    
    # Salvar texto completo melhorado
    with open("bula_enhanced.txt", "w", encoding="utf-8") as f:
        f.write(enhanced_data["full_text"])
    
    print("\n=== SEÇÕES IDENTIFICADAS ===")
    for section, data in enhanced_data["sections"].items():
        print(f"{section}: {data['word_count']} palavras")
    
    print(f"\nArquivos salvos: bula_enhanced_transcription.json e bula_enhanced.txt")