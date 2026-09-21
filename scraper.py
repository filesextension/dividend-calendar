import datetime
import html
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": "https://www.nasdaq.com",
    "Referer": "https://www.nasdaq.com/"
}

def obtener_datos_fecha(fecha_str):
    url = f"https://api.nasdaq.com/api/calendar/dividends?date={fecha_str}"
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        if res.status_code == 200:
            data = res.json()
            return data.get("data", {}).get("calendar", {}).get("rows", []) or []
    except Exception as e:
        print(f"Error consultando {fecha_str}: {e}")
    return []

def renderizar_filas(rows):
    if not rows:
        return "<tr><td colspan='6' style='text-align:center; padding: 2rem; color: #8b949e;'>No dividend declarations found for this period.</td></tr>"
    
    filas = ""
    for r in rows:
        ticker = html.escape(str(r.get("symbol", "N/A")))
        name = html.escape(str(r.get("companyName", "N/A")))
        amount = html.escape(str(r.get("dividend_Rate", "N/A")))
        yield_val = html.escape(str(r.get("annual_Yield", "N/A")))
        ex_date = html.escape(str(r.get("dividend_Ex_Date", "N/A")))
        pay_date = html.escape(str(r.get("payment_Date", "N/A")))
        
        # Enlace externo dinámico a Yahoo Finance para aportar E-E-A-T y utilidad
        yahoo_url = f"https://finance.yahoo.com/quote/{ticker}"
        
        filas += f"""
        <tr>
            <td><a href="{yahoo_url}" target="_blank" rel="noopener noreferrer" class="badge" title="Verify {ticker} on Yahoo Finance">{ticker}</a></td>
            <td>{name}</td>
            <td class="num font-bold text-accent">{amount}</td>
            <td class="num">{yield_val}%</td>
            <td>{ex_date}</td>
            <td>{pay_date}</td>
        </tr>
        """
    return filas

def generar_plantilla(titulo, subtitulo, pestana_activa, contenido_filas, alerta="", fecha_iso=""):
    nav_links = [
        ("index.html", "Today"),
        ("tomorrow.html", "Tomorrow"),
        ("this-week.html", "This Week"),
        ("next-week.html", "Next Week"),
        ("guide.html", "Dividend Guide"),
        ("about.html", "About")
    ]
    
    nav_html = ""
    for url, label in nav_links:
        active_cls = ' class="active"' if pestana_activa == url else ''
        nav_html += f'<a href="{url}"{active_cls}>{label}</a>\n'

    alert_box = f'<div class="callout">{alerta}</div>' if alerta else ""

    # Schema markup dinámico por página
    schema_markup = f"""
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "WebPage",
    "name": "{titulo}",
    "description": "{subtitulo}",
    "dateModified": "{fecha_iso}",
    "publisher": {{
      "@type": "Organization",
      "name": "DividendRadar"
    }}
  }}
  </script>
    """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{titulo} - DividendRadar</title>
  <meta name="description" content="{subtitulo}">
  {schema_markup}
  <style>
    :root {{
      --bg: #0d1117;
      --card: #161b22;
      --border: #30363d;
      --text: #c9d1d9;
      --text-muted: #8b949e;
      --primary: #58a6ff;
      --accent: #2ea043;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      background-color: var(--bg);
      color: var(--text);
      margin: 0;
      padding: 0;
      line-height: 1.6;
    }}
    header {{
      background-color: var(--card);
      border-bottom: 1px solid var(--border);
      padding: 1.2rem 2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1rem;
    }}
    header a.brand {{
      color: #fff;
      font-size: 1.3rem;
      font-weight: bold;
      text-decoration: none;
    }}
    nav a {{
      color: var(--text-muted);
      text-decoration: none;
      margin-left: 1.2rem;
      font-size: 0.95rem;
      padding: 0.3rem 0.6rem;
      border-radius: 4px;
      transition: all 0.2s;
    }}
    nav a:hover {{
      color: var(--primary);
    }}
    nav a.active {{
      color: #fff;
      background: #21262d;
      border: 1px solid var(--border);
    }}
    main {{
      max-width: 1100px;
      margin: 2rem auto;
      padding: 0 1.5rem;
    }}
    .hero {{
      text-align: center;
      margin-bottom: 2rem;
    }}
    .hero h1 {{
      font-size: 2.2rem;
      color: #fff;
      margin-bottom: 0.5rem;
    }}
    .hero p {{
      color: var(--text-muted);
      font-size: 1.05rem;
      max-width: 750px;
      margin: 0 auto;
    }}
    .callout {{
      background-color: rgba(88, 166, 255, 0.1);
      border-left: 4px solid var(--primary);
      padding: 1rem 1.2rem;
      margin: 1.5rem 0;
      border-radius: 0 6px 6px 0;
      color: #c9d1d9;
    }}
    .search-box {{
      margin: 1.5rem 0;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1rem;
    }}
    .search-box input {{
      background-color: var(--card);
      border: 1px solid var(--border);
      color: #fff;
      padding: 0.75rem 1rem;
      border-radius: 6px;
      font-size: 0.95rem;
      width: 100%;
      max-width: 380px;
      outline: none;
    }}
    .search-box input:focus {{
      border-color: var(--primary);
    }}
    .table-container {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 8px;
      overflow-x: auto;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      text-align: left;
    }}
    th, td {{
      padding: 0.9rem 1.2rem;
      border-bottom: 1px solid var(--border);
    }}
    th {{
      background-color: rgba(255, 255, 255, 0.03);
      color: #fff;
      font-weight: 600;
      font-size: 0.85rem;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    tr:last-child td {{
      border-bottom: none;
    }}
    tr:hover td {{
      background-color: rgba(255, 255, 255, 0.02);
    }}
    a.badge {{
      background-color: #21262d;
      border: 1px solid var(--border);
      color: var(--primary);
      padding: 0.2rem 0.5rem;
      border-radius: 4px;
      font-weight: bold;
      font-size: 0.85rem;
      text-decoration: none;
      display: inline-block;
    }}
    a.badge:hover {{
      background-color: var(--primary);
      color: #fff;
    }}
    .text-accent {{ color: var(--accent); }}
    .font-bold {{ font-weight: bold; }}
    .num {{ text-align: right; }}
    th.num {{ text-align: right; }}
    .editorial {{
      margin-top: 3rem;
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 2rem;
    }}
    .editorial h2 {{
      color: #fff;
      font-size: 1.35rem;
      margin-top: 1.5rem;
      border-bottom: 1px solid var(--border);
      padding-bottom: 0.5rem;
    }}
    .editorial h2:first-child {{
      margin-top: 0;
    }}
    .editorial p {{
      color: var(--text-muted);
    }}
    footer {{
      text-align: center;
      padding: 2.5rem 1.5rem;
      border-top: 1px solid var(--border);
      color: var(--text-muted);
      font-size: 0.85rem;
      margin-top: 4rem;
    }}
    footer a {{
      color: var(--primary);
      text-decoration: none;
      margin: 0 0.5rem;
    }}
    footer a:hover {{
      text-decoration: underline;
    }}
  </style>
</head>
<body>
  <header>
    <a href="index.html" class="brand">📈 DividendRadar</a>
    <nav>
      {nav_html}
    </nav>
  </header>

  <main>
    <div class="hero">
      <h1>{titulo}</h1>
      <p>{subtitulo}</p>
    </div>

    {alert_box}

    <div class="search-box">
      <input type="text" id="filtro" placeholder="Search by ticker or company name..." onkeyup="filtrarTabla()">
      <span style="font-size: 0.85rem; color: var(--text-muted);">
        Data dynamically sourced from <a href="https://www.nasdaq.com" target="_blank" rel="noopener noreferrer" style="color: var(--primary); text-decoration: none;">Nasdaq API</a>.
      </span>
    </div>

    <div class="table-container">
      <table id="tabla-dividendos">
        <thead>
          <tr>
            <th>Symbol</th>
            <th>Company Name</th>
            <th class="num">Cash Amount</th>
            <th class="num">Yield (%)</th>
            <th>Ex-Dividend Date</th>
            <th>Pay Date</th>
          </tr>
        </thead>
        <tbody>
          {contenido_filas}
        </tbody>
      </table>
    </div>

    <section class="editorial">
      <h2>Trading Strategy & Settlement Rules</h2>
      <p>Remember that corporate dividends require trades to settle before the official record date. To capture a distribution, you must acquire the stock at least one trading session before its scheduled ex-dividend date, in accordance with <a href="https://www.investor.gov/" target="_blank" rel="noopener noreferrer" style="color: var(--primary); text-decoration: none;">SEC settlement guidelines</a>.</p>
      
      <h2>Risk Management Considerations</h2>
      <p>Click on any ticker symbol in the table above to verify real-time financials and payout sustainability on Yahoo Finance. Explore complete breakdown guides in our <a href="guide.html" style="color: var(--primary);">Ex-Dividend Strategy Guide</a>.</p>
    </section>
  </main>

  <footer>
    <p>&copy; 2026 DividendRadar. Financial data provided for informational and research purposes only.</p>
    <p>
      <a href="index.html">Today</a> |
      <a href="tomorrow.html">Tomorrow</a> |
      <a href="this-week.html">This Week</a> |
      <a href="next-week.html">Next Week</a> |
      <a href="about.html">About & Methodology</a> |
      <a href="guide.html">Dividend Strategy Guide</a> |
      <a href="terms.html">Terms of Service</a> |
      <a href="privacy.html">Privacy Policy</a>
    </p>
    <p style="margin-top: 1rem; color: #58a6ff;">Contact: support@dividendradar.com</p>
  </footer>

  <script>
    function filtrarTabla() {{
      const input = document.getElementById("filtro");
      const filtro = input.value.toUpperCase();
      const tr = document.getElementById("tabla-dividendos").getElementsByTagName("tr");
      for (let i = 1; i < tr.length; i++) {{
        const tdSimbolo = tr[i].getElementsByTagName("td")[0];
        const tdNombre = tr[i].getElementsByTagName("td")[1];
        if (tdSimbolo || tdNombre) {{
          const txtSimbolo = tdSimbolo.textContent || tdSimbolo.innerText;
          const txtNombre = tdNombre.textContent || tdNombre.innerText;
          if (txtSimbolo.toUpperCase().indexOf(filtro) > -1 || txtNombre.toUpperCase().indexOf(filtro) > -1) {{
            tr[i].style.display = "";
          }} else {{
            tr[i].style.display = "none";
          }}
        }}
      }}
    }}
  </script>
</body>
</html>
"""

hoy = datetime.date.today()
manana = hoy + datetime.timedelta(days=1)
inicio_semana = hoy - datetime.timedelta(days=hoy.weekday())
dias_esta_semana = [inicio_semana + datetime.timedelta(days=i) for i in range(5)]
inicio_proxima_semana = inicio_semana + datetime.timedelta(days=7)
dias_proxima_semana = [inicio_proxima_semana + datetime.timedelta(days=i) for i in range(5)]

print(f"Generando calendario para Hoy: {hoy.strftime('%Y-%m-%d')}")

# 1. TODAY
datos_hoy = obtener_datos_fecha(hoy.strftime("%Y-%m-%d"))
html_today = generar_plantilla(
    titulo="Today's Ex-Dividend Stocks",
    subtitulo=f"Live list of stocks going ex-dividend today, {hoy.strftime('%B %d, %Y')}.",
    pestana_activa="index.html",
    contenido_filas=renderizar_filas(datos_hoy),
    alerta="<strong>Notice:</strong> Stocks listed here are trading ex-dividend today. Shares purchased today will not qualify for the upcoming payout.",
    fecha_iso=hoy.isoformat()
)
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_today)

# 2. TOMORROW
datos_manana = obtener_datos_fecha(manana.strftime("%Y-%m-%d"))
html_tomorrow = generar_plantilla(
    titulo="Stocks Going Ex-Dividend Tomorrow",
    subtitulo=f"Critical cutoff list for tomorrow, {manana.strftime('%B %d, %Y')}. Action required before market close today.",
    pestana_activa="tomorrow.html",
    contenido_filas=renderizar_filas(datos_manana),
    alerta="<strong>Action Required:</strong> To receive these dividends, you must purchase qualifying shares before today's market closing bell (4:00 PM EST).",
    fecha_iso=hoy.isoformat()
)
with open("tomorrow.html", "w", encoding="utf-8") as f:
    f.write(html_tomorrow)

# 3. THIS WEEK
datos_esta_semana = []
for d in dias_esta_semana:
    datos_esta_semana.extend(obtener_datos_fecha(d.strftime("%Y-%m-%d")))

html_this_week = generar_plantilla(
    titulo="Ex-Dividend Stocks This Week",
    subtitulo=f"Complete schedule of all U.S. equities going ex-dividend between {dias_esta_semana[0].strftime('%b %d')} and {dias_esta_semana[-1].strftime('%b %d, %Y')}.",
    pestana_activa="this-week.html",
    contenido_filas=renderizar_filas(datos_esta_semana),
    alerta="<strong>Weekly Outlook:</strong> Plan your capital allocation for the entire current trading week across NYSE and NASDAQ securities.",
    fecha_iso=hoy.isoformat()
)
with open("this-week.html", "w", encoding="utf-8") as f:
    f.write(html_this_week)

# 4. NEXT WEEK
datos_proxima_semana = []
for d in dias_proxima_semana:
    datos_proxima_semana.extend(obtener_datos_fecha(d.strftime("%Y-%m-%d")))

html_next_week = generar_plantilla(
    titulo="Ex-Dividend Stocks Next Week",
    subtitulo=f"Early planning radar for upcoming corporate payouts from {dias_proxima_semana[0].strftime('%b %d')} to {dias_proxima_semana[-1].strftime('%b %d, %Y')}.",
    pestana_activa="next-week.html",
    contenido_filas=renderizar_filas(datos_proxima_semana),
    alerta="<strong>Advance Planning:</strong> Upcoming dividend schedule for next week. Verify declared corporate announcements prior to trade execution.",
    fecha_iso=hoy.isoformat()
)
with open("next-week.html", "w", encoding="utf-8") as f:
    f.write(html_next_week)

# 5. SITEMAP
sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://dividendradar.netlify.app/index.html</loc>
    <lastmod>{hoy.strftime('%Y-%m-%d')}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://dividendradar.netlify.app/tomorrow.html</loc>
    <lastmod>{hoy.strftime('%Y-%m-%d')}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://dividendradar.netlify.app/this-week.html</loc>
    <lastmod>{hoy.strftime('%Y-%m-%d')}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://dividendradar.netlify.app/next-week.html</loc>
    <lastmod>{hoy.strftime('%Y-%m-%d')}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://dividendradar.netlify.app/guide.html</loc>
    <lastmod>{hoy.strftime('%Y-%m-%d')}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>
  <url>
    <loc>https://dividendradar.netlify.app/about.html</loc>
    <lastmod>{hoy.strftime('%Y-%m-%d')}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>
</urlset>
"""

with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap_xml)
