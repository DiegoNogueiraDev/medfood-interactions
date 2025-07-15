from unstructured.partition.pdf import partition_pdf
import json

def detailed_transcription_analysis(pdf_path):
    blocks = partition_pdf(pdf_path, strategy="hi_res")
    
    analysis = {
        "total_blocks": len(blocks),
        "blocks_by_category": {},
        "text_blocks": 0,
        "total_characters": 0,
        "empty_blocks": 0,
        "sample_texts": []
    }
    
    for i, block in enumerate(blocks):
        category = block.category if hasattr(block, 'category') else 'unknown'
        
        if category not in analysis["blocks_by_category"]:
            analysis["blocks_by_category"][category] = 0
        analysis["blocks_by_category"][category] += 1
        
        if hasattr(block, 'text') and block.text:
            text = block.text.strip()
            if text:
                analysis["text_blocks"] += 1
                analysis["total_characters"] += len(text)
                
                if len(analysis["sample_texts"]) < 10:
                    analysis["sample_texts"].append({
                        "block_index": i,
                        "category": category,
                        "text_preview": text[:200] + "..." if len(text) > 200 else text,
                        "text_length": len(text)
                    })
            else:
                analysis["empty_blocks"] += 1
        else:
            analysis["empty_blocks"] += 1
    
    # Verificar tipos de conteúdo
    print("=== ANÁLISE DETALHADA DA TRANSCRIÇÃO ===")
    print(f"Total de blocos extraídos: {analysis['total_blocks']}")
    print(f"Blocos com texto: {analysis['text_blocks']}")
    print(f"Blocos vazios: {analysis['empty_blocks']}")
    print(f"Total de caracteres: {analysis['total_characters']}")
    print()
    
    print("Distribuição por categoria:")
    for category, count in analysis["blocks_by_category"].items():
        print(f"  {category}: {count} blocos")
    print()
    
    print("Amostras de texto extraído:")
    for sample in analysis["sample_texts"]:
        print(f"  Bloco {sample['block_index']} ({sample['category']}) - {sample['text_length']} chars:")
        print(f"    {sample['text_preview']}")
        print()
    
    # Verificar se capturou estruturas específicas
    all_text = ""
    for block in blocks:
        if hasattr(block, 'text') and block.text:
            all_text += block.text + " "
    
    print("=== VERIFICAÇÃO DE COMPLETUDE ===")
    keywords = ["DrugBank", "ANVISA", "interações", "medicamentos", "alimentos", 
                "álcool", "cafeína", "toranja", "grapefruit", "vitamina K"]
    
    found_keywords = []
    for keyword in keywords:
        if keyword.lower() in all_text.lower():
            found_keywords.append(keyword)
    
    print(f"Palavras-chave encontradas: {found_keywords}")
    print(f"Coverage: {len(found_keywords)}/{len(keywords)} ({len(found_keywords)/len(keywords)*100:.1f}%)")
    
    return analysis, all_text

if __name__ == "__main__":
    analysis, full_text = detailed_transcription_analysis("bula.pdf")
    
    # Salvar análise detalhada
    with open("transcription_analysis.json", "w", encoding="utf-8") as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    
    print(f"\nAnálise salva em transcription_analysis.json")
    print(f"Qualidade estimada: {'Alta' if analysis['total_characters'] > 25000 else 'Média' if analysis['total_characters'] > 15000 else 'Baixa'}")