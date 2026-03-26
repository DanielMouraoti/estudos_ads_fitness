import os
import asyncio
from dotenv import load_dotenv
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from groq import Groq
from fpdf import FPDF
from pypdf import PdfReader

# 1. SEGURANÇA: Carrega a chave do arquivo .env
load_dotenv()
GROQ_API_KEY ="SUA_CHAVE_AQUI"

# 2. CONFIGURAÇÕES DE CAMINHO (Ajuste se necessário no seu Ubuntu)
URL_SITE = "https://www.hevyapp.com/upper-lower-split-complete-guide/"
CAMINHO_DIETA_PDF = "/home/danielmo/Downloads/dieta.pdf"

class PDF(FPDF):
    def header(self):
        self.set_fill_color(30, 41, 59)
        self.rect(0, 0, 210, 30, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font("helvetica", 'B', 15)
        self.cell(0, 10, "CONSULTORIA IA: TREINO & DIETA", align='C', new_x="LMARGIN", new_y="NEXT")
        self.ln(10)

def extrair_texto_pdf(caminho):
    try:
        reader = PdfReader(caminho)
        return "".join([page.extract_text() for page in reader.pages])
    except Exception as e:
        return f"Erro na leitura da dieta: {e}"

async def coletar_dados_web():
    print("[*] Scraper: Coletando base científica...")
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=URL_SITE)
        return result.markdown[:12000]

def gerar_prescricao_ia(conhecimento, perfil):
    print("[*] Groq: Processando inteligência de treino...")
    client = Groq(api_key=GROQ_API_KEY)
    
    prompt = f"""
    Você é um Personal Trainer e Fisiologista de Elite. 
    FONTE TÉCNICA: {conhecimento}
    PERFIL DO ALUNO: {perfil}

    REGRAS DE FORMATAÇÃO PARA GOOGLE DOCS (NÃO USE TABELAS MARKDOWN):
    1. USE TÍTULOS EM CAIXA ALTA PARA OS DIAS.
    2. Liste exercícios assim: [NOME DO EXERCÍCIO EM NEGRITO] - Séries: X | Reps: Y | Descanso: Zs.
    3. CRONOGRAMA OBRIGATÓRIO (NÃO PULE DIAS):
       - SEGUNDA: Superior (Costas/Postura/Hipercifose)
       - TERÇA: Inferior (Pernas Completo)
       - QUARTA: DESCANSO TOTAL E MOBILIDADE TORÁCICA
       - QUINTA: Superior (Peito/Ombros/Tríceps)
       - SEXTA: Inferior (Posterior/Glúteo/Panturrilha)
    4. DIETA: Analise as calorias e proteínas do PDF e ajuste o volume de séries.
    5. IDIOMA: Português (Brasil).
    """
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    return completion.choices[0].message.content

async def main():
    print("\n=== SISTEMA DE CONSULTORIA FITNESS IA ===")
    nome = input("Nome do Aluno: ")
    idade = input("Idade: ")
    limitacoes = input("Lesões/Dores (Ex: Hipercifose): ")
    
    texto_dieta = extrair_texto_pdf(CAMINHO_DIETA_PDF)
    perfil = f"Nome: {nome}, Idade: {idade}, Lesão: {limitacoes}, Dieta: {texto_dieta}"
    
    dados_site = await coletar_dados_web()
    treino_final = gerar_prescricao_ia(dados_site, perfil)
    
    # SALVAR TEXTO LIMPO PARA O GOOGLE DOCS
    with open("texto_limpo_treino.txt", "w", encoding="utf-8") as f:
        f.write(treino_final)
    
    # GERAR PDF DE BACKUP
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("helvetica", size=10)
    texto_pdf = treino_final.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 8, text=texto_pdf)
    pdf.output(f"Treino_{nome}.pdf")
    
    print(f"\n[OK] Processo Finalizado!")
    print(f"-> Texto pronto para o Google Docs em: texto_limpo_treino.txt")
    print(f"-> Use 'cat texto_limpo_treino.txt' para copiar.")

if __name__ == "__main__":
    asyncio.run(main())
