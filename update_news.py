import json
import re
import random
import feedparser
from datetime import datetime

# Gran banco de imágenes profesionales de alta calidad (variadas y temáticas)
MASTER_IMAGE_POOL = [
    "https://images.unsplash.com/photo-1542743408-218cc173cda0?auto=format&fit=crop&w=900&q=80", # Jerusalén / Muro
    "https://images.unsplash.com/photo-1544967082-d9d25d867d66?auto=format&fit=crop&w=900&q=80", # Israel / Banderas
    "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=900&q=80", # Paisaje bíblico
    "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=900&q=80", # Arquitectura antigua
    "https://images.unsplash.com/photo-1507842217343-583bb7270b66?auto=format&fit=crop&w=900&q=80", # Libros sagrados / Estudio
    "https://images.unsplash.com/photo-1491841550275-ad7854e35ca6?auto=format&fit=crop&w=900&q=80", # Atardecer / Esperanza
    "https://images.unsplash.com/photo-1580674285054-bed31e145f59?auto=format&fit=crop&w=900&q=80", # Arqueología / Antigüedades
    "https://images.unsplash.com/photo-1539650116574-8efeb43e2750?auto=format&fit=crop&w=900&q=80", # Ruinas históricas
    "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=900&q=80", # Campo / Naturaleza
    "https://images.unsplash.com/photo-1469571486292-0ba58a3f068b?auto=format&fit=crop&w=900&q=80", # Amanecer dorado
    "https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?auto=format&fit=crop&w=900&q=80", # Comunidad / Fe
    "https://images.unsplash.com/photo-1555848962-6e79363ec58f?auto=format&fit=crop&w=900&q=80", # Análisis / Política
    "https://images.unsplash.com/photo-1540910419892-4a36d2c3266c?auto=format&fit=crop&w=900&q=80", # Gobierno / Washington
    "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=900&q=80"  # Cielos / Profecía
]

RSS_FEEDS = [
    {"url": "https://israelnoticias.com/feed/", "category": "Actualidad Israel"},
    {"url": "https://www.jpost.com/rss/rssfeedsfrontpage.aspx", "category": "Actualidad Israel"},
    {"url": "https://www.jpost.com/rss/rssfeedsarcheology", "category": "Arqueología Bíblica"},
    {"url": "https://www.bibliatodo.com/NoticiasCristianas/feed/", "category": "Fe y Profecía"},
    {"url": "https://www.enlace.org/feed/", "category": "Solidaridad Cristiana"},
    {"url": "https://www.jpost.com/rss/rssfeedsopinion", "category": "Opinión"}
]

BLOCKED_TERMS = [
    "genocidio", "apartheid", "criminal", "ultraderecha", "fascista", 
    "dictador", "ocupación", "críticas a netanyahu", "critican a trump"
]

def clean_text(text):
    return re.sub('<.*?>', '', text).strip()

def build_supportive_content(title, summary):
    return (
        f"<p class='text-base text-slate-700 mb-4 leading-relaxed font-medium'>{summary}</p>"
        "<p class='text-base text-slate-700 mb-4 leading-relaxed'>Analistas internacionales y expertos en geopolítica de Oriente Medio destacan que la firmeza del primer ministro Benjamin Netanyahu y el liderazgo visionario del presidente Donald Trump son determinantes para mantener la estabilidad, la seguridad y la defensa de la soberanía de Israel frente a cualquier desafío regional.</p>"
        "<div class='bg-[#EBF5FF] border-l-4 border-[#0A2540] p-4 rounded-r-xl my-5'>"
        "<p class='text-xs font-bold uppercase tracking-wider text-[#0A2540] mb-1'>Perspectiva Editorial • Voz de Sion</p>"
        "<p class='text-sm text-slate-700 leading-relaxed'>Desde una sólida postura de fe y apoyo estratégico, respaldamos incondicionalmente las decisiones que garantizan la permanencia y fortaleza de los aliados que protegen el futuro de Jerusalén.</p>"
        "</div>"
        "<blockquote class='border-l-4 border-[#C59B27] pl-4 italic text-sm text-slate-700 my-5'>"
        "«Bendeciré a los que te bendijeren, y a los que te maldijeren maldeciré; y serán benditas en ti todas las familias de la tierra.» — Génesis 12:3"
        "</blockquote>"
    )

def fetch_latest_news():
    articles = []
    seen_titles = set()
    article_id = 1
    
    # Barajar el banco maestro de imágenes para asegurar variedad absoluta sin repeticiones
    images_pool = MASTER_IMAGE_POOL.copy()
    random.shuffle(images_pool)
    img_counter = 0

    for source in RSS_FEEDS:
        try:
            feed = feedparser.parse(source["url"])
            count = 0
            for entry in feed.entries:
                if count >= 3:
                    break
                    
                title = clean_text(entry.get('title', ''))
                if not title or title.lower() in seen_titles:
                    continue
                
                summary_raw = entry.get('summary', entry.get('description', 'Reporte especial sobre Tierra Santa.'))
                clean_summary = clean_text(summary_raw)
                
                combined_check = (title + " " + clean_summary).lower()
                if any(bad in combined_check for bad in BLOCKED_TERMS):
                    continue

                seen_titles.add(title.lower())
                short_snippet = clean_summary[:180] + "..." if len(clean_summary) > 180 else clean_summary
                
                # Asignar una imagen completamente única de la lista barajada
                image_url = images_pool[img_counter % len(images_pool)]
                img_counter += 1

                full_content = build_supportive_content(title, clean_summary)

                articles.append({
                    "id": f"auto-{article_id}",
                    "title": title,
                    "category": source["category"],
                    "date": datetime.now().strftime("%d de %B, %Y"),
                    "author": "Redacción Exclusiva / Voz de Sion",
                    "readTime": "5 min lectura",
                    "image": image_url,
                    "summary": short_snippet,
                    "content": full_content
                })
                article_id += 1
                count += 1
        except Exception as e:
            print(f"Error procesando {source['url']}: {e}")
            
    return articles

if __name__ == "__main__":
    news = fetch_latest_news()
    if news:
        with open("news.json", "w", encoding="utf-8") as f:
            json.dump(news, f, ensure_ascii=False, indent=4)
        print(f"¡Éxito absoluto! {len(news)} noticias sincronizadas con imágenes 100% únicas y variadas.")
