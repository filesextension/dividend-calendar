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

# Lista de tickers populares conocidos por pagar mensualmente
MONTHLY_PAYERS = {
    "O", "MAIN", "STAG", "AGNC", "PSEC", "LAND", "LTC", "EPR", "GLAD", "GOOD",
    "GAIN", "SLG", "ADC", "SJTR", "GWRS", "PBA", "JEPI", "JEPQ", "DIVO"
}

# Lista curada de Dividend Aristocrats más buscados
ARISTOCRATS = {
    "MMM", "ABBV", "ABT", "ADM", "ADP", "AFL", "APD", "ATO", "BDX", "BEN",
    "BF.B", "BRO", "CAH", "CARR", "CAT", "CB", "CHD", "CHRW", "CINF", "CL",
    "CLX", "CTAS", "CVX", "DOV", "ECL", "ED", "EMR", "ESS", "EXPD", "FRT",
    "GD", "GPC", "GWW", "HRL", "IBM", "ITW", "JNJ", "KMB", "KO", "LEG",
    "LIN", "LOW", "MCD", "MDT", "MKC", "NDSN", "NEE", "NUE", "OTIS", "PEP",
    "PG", "PNR", "PPG", "ROP", "ROST", "SHW", "SPGI", "SWK", "SYY", "T",
    "TGT", "TROW", "VFC", "VZ", "WBA", "WMT", "XOM"
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

def limpiar_yield(yield_str):
    """Extrae el float de yield_pct para comparar números."""
    try:
        limpio = str(yield_str).replace("%", "").replace(",", "").strip()
        return float(limpio)
    except:
        return 0.0

def renderizar_filas(rows):
    if not rows:
        return "<tr><td colspan='6' style='text-align:center; padding: 2rem; color: #8b949e;'>No dividend declarations found for this specific screener.</td></tr>"
    
    filas = ""
    for r in rows:
        ticker = html.escape(str(r.get("symbol", "N/A")))
        name = html.escape(str(r.get("companyName", "N/A")))
        amount = html.escape(str(r.get("dividend_Rate", "N/A")))
        yield_val = html.escape(str(r.get("annual_Yield", "N/A")))
        ex_date = html.escape(str(r.get("dividend_Ex_Date", "N/A")))
        pay_date = html.escape(str(r.get("payment_Date", "N/A")))
        
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

def generar_plantilla(titulo, subtitulo, pestana_activa, contenido_filas, alerta="", fecha_iso="", texto_seo=""):
    nav_links = [
        ("index.html", "Today"),
        ("tomorrow.html", "Tomorrow"),
        ("this-week.html", "This Week"),
        ("next-week.html", "Next Week"),
        ("monthly-dividend-stocks.html", "Monthly Payers"),
        ("high-yield-dividend-stocks.html", "High Yield (>6%)"),
        ("dividend-aristocrats.html", "Aristocrats"),
        ("guide.html", "Guide"),
        ("about.html", "About")
    ]
    
    nav_html = ""
    for url, label in nav_links:
        active_cls = ' class="active"' if pestana_activa == url else ''
        nav_html += f'<a href="{url}"{active_cls}>{label}</a>\n'

    alert_box = f'<div class="callout">{alerta}</div>' if alerta else ""

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
      padding: 1rem 1.5rem;
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
    nav {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.4rem;
    }}
    nav a {{
      color: var(--text-muted);
      text-decoration: none;
      font-size: 0.9rem;
      padding: 0.35rem 0.65rem;
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
    .editorial p, .editorial li {{
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
        Data feed: <a href="https://www.nasdaq.com" target="_blank" rel="noopener noreferrer" style="color: var(--primary); text-decoration: none;">Nasdaq API Live</a>
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
      {texto_seo}
    </section>
  </main>

  <footer>
    <p>&copy; 2026 DividendRadar. Financial market research data updated daily.</p>
    <p>
      <a href="index.html">Today</a> |
      <a href="tomorrow.html">Tomorrow</a> |
      <a href="this-week.html">This Week</a> |
      <a href="next-week.html">Next Week</a> |
      <a href="monthly-dividend-stocks.html">Monthly Payers</a> |
      <a href="high-yield-dividend-stocks.html">High Yield (&gt;6%)</a> |
      <a href="dividend-aristocrats.html">Aristocrats</a> |
      <a href="about.html">About & Methodology</a> |
      <a href="guide.html">Dividend Guide</a> |
      <a href="terms.html">Terms</a> |
      <a href="privacy.html">Privacy</a>
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

# ==========================================
# CÁLCULO DE FECHAS & DESCARGA
# ==========================================
hoy = datetime.date.today()
manana = hoy + datetime.timedelta(days=1)
inicio_semana = hoy - datetime.timedelta(days=hoy.weekday())
dias_esta_semana = [inicio_semana + datetime.timedelta(days=i) for i in range(5)]
inicio_proxima_semana = inicio_semana + datetime.timedelta(days=7)
dias_proxima_semana = [inicio_proxima_semana + datetime.timedelta(days=i) for i in range(5)]

# Descargar datos de 2 semanas completas para nutrir los screeners
pool_total = []
dias_a_descargar = set(dias_esta_semana + dias_proxima_semana + [hoy, manana])
for dia in dias_a_descargar:
    pool_total.extend(obtener_datos_fecha(dia.strftime("%Y-%m-%d")))

# Desduplicar registros por ticker + ex_date
pool_unicos = {}
for item in pool_total:
    clave = f"{item.get('symbol')}_{item.get('dividend_Ex_Date')}"
    pool_unicos[clave] = item
todos_los_registros = list(pool_unicos.values())

print(f"Total registros obtenidos para procesar micronichos: {len(todos_los_registros)}")

# 1. TODAY
datos_hoy = obtener_datos_fecha(hoy.strftime("%Y-%m-%d"))
with open("index.html", "w", encoding="utf-8") as f:
    f.write(generar_plantilla(
        titulo="Today's Ex-Dividend Stocks",
        subtitulo=f"Live list of stocks going ex-dividend today, {hoy.strftime('%B %d, %Y')}.",
        pestana_activa="index.html",
        contenido_filas=renderizar_filas(datos_hoy),
        alerta="<strong>Notice:</strong> Stocks trading ex-dividend today must have been purchased prior to market open to qualify.",
        fecha_iso=hoy.isoformat(),
        texto_seo="<h2>Today's Market Execution</h2><p>Review the exact cutoff declarations for equities trading ex-date today. Positions entered on or after market open will not capture declared disbursements.</p>"
    ))

# 2. TOMORROW
datos_manana = obtener_datos_fecha(manana.strftime("%Y-%m-%d"))
with open("tomorrow.html", "w", encoding="utf-8") as f:
    f.write(generar_plantilla(
        titulo="Stocks Going Ex-Dividend Tomorrow",
        subtitulo=f"Critical cutoff list for tomorrow, {manana.strftime('%B %d, %Y')}. Action required today.",
        pestana_activa="tomorrow.html",
        contenido_filas=renderizar_filas(datos_manana),
        alerta="<strong>Action Required:</strong> To capture these dividends, you must purchase shares before today's market close (4:00 PM EST).",
        fecha_iso=hoy.isoformat(),
        texto_seo="<h2>Immediate Purchase Cutoffs</h2><p>Buying shares today ensures eligibility for tomorrow's scheduled record date settlement. Verify liquidity and spread before placing limit orders.</p>"
    ))

# 3. THIS WEEK
datos_esta_semana = [r for r in todos_los_registros if any(d.strftime("%m/%d/%Y") in str(r.get("dividend_Ex_Date", "")) for d in dias_esta_semana)]
with open("this-week.html", "w", encoding="utf-8") as f:
    f.write(generar_plantilla(
        titulo="Ex-Dividend Stocks This Week",
        subtitulo=f"Complete schedule of all U.S. equities going ex-dividend between {dias_esta_semana[0].strftime('%b %d')} and {dias_esta_semana[-1].strftime('%b %d, %Y')}.",
        pestana_activa="this-week.html",
        contenido_filas=renderizar_filas(datos_esta_semana),
        alerta="<strong>Weekly Outlook:</strong> Plan capital allocations for the current trading week across NYSE and NASDAQ securities.",
        fecha_iso=hoy.isoformat(),
        texto_seo="<h2>Weekly Strategy</h2><p>Plan entry dates for upcoming dividend capture cycles across diversified industrial sectors.</p>"
    ))

# 4. NEXT WEEK
datos_proxima_semana = [r for r in todos_los_registros if any(d.strftime("%m/%d/%Y") in str(r.get("dividend_Ex_Date", "")) for d in dias_proxima_semana)]
with open("next-week.html", "w", encoding="utf-8") as f:
    f.write(generar_plantilla(
        titulo="Ex-Dividend Stocks Next Week",
        subtitulo=f"Early planning radar for upcoming corporate payouts from {dias_proxima_semana[0].strftime('%b %d')} to {dias_proxima_semana[-1].strftime('%b %d, %Y')}.",
        pestana_activa="next-week.html",
        contenido_filas=renderizar_filas(datos_proxima_semana),
        alerta="<strong>Advance Planning:</strong> Upcoming dividend schedule for next week. Verify declared corporate filings.",
        fecha_iso=hoy.isoformat(),
        texto_seo="<h2>Advance Capital Planning</h2><p>Review next week's scheduled dividend cuts to prepare watchlist orders before institutional volume accelerates.</p>"
    ))

# ==========================================
# 5. LONG TAIL: MONTHLY DIVIDEND STOCKS
# ==========================================
datos_monthly = [r for r in todos_los_registros if str(r.get("symbol", "")).upper() in MONTHLY_PAYERS]
with open("monthly-dividend-stocks.html", "w", encoding="utf-8") as f:
    f.write(generar_plantilla(
        titulo="Monthly Dividend Stocks Calendar",
        subtitulo="High-income equities, monthly REITs, and business development companies paying dividends every 30 days.",
        pestana_activa="monthly-dividend-stocks.html",
        contenido_filas=renderizar_filas(datos_monthly),
        alerta="<strong>Passive Cash Flow:</strong> Monthly paying dividend stocks provide 12 distributions per year, accelerating dividend compounding.",
        fecha_iso=hoy.isoformat(),
        texto_seo="""
        <h2>Why Invest in Monthly Dividend Stocks?</h2>
        <p>Unlike traditional quarterly paying stocks, monthly dividend companies disburse income twelve times a year. This structure is favored by retirees and income-focused investors who need predictable cash flow to cover living expenses.</p>
        <h2>Key Monthly Sectors</h2>
        <ul>
            <li><strong>Real Estate Investment Trusts (REITs):</strong> Entities like Realty Income (O) and STAG Industrial (STAG) lease commercial properties and distribute rental income monthly.</li>
            <li><strong>Business Development Companies (BDCs):</strong> Firms like Main Street Capital (MAIN) provide debt capital to private companies, passing through high operational yields.</li>
        </ul>
        """
    ))

# ==========================================
# 6. LONG TAIL: HIGH YIELD DIVIDENDS (>6%)
# ==========================================
datos_high_yield = [r for r in todos_los_registros if limpiar_yield(r.get("annual_Yield")) >= 6.0]
# Ordenar de mayor a menor yield
datos_high_yield.sort(key=lambda x: limpiar_yield(x.get("annual_Yield")), reverse=True)

with open("high-yield-dividend-stocks.html", "w", encoding="utf-8") as f:
    f.write(generar_plantilla(
        titulo="High Yield Dividend Stocks Screener (>6%)",
        subtitulo="Screen U.S. equities with declared annual dividend yields exceeding 6.0% going ex-dividend soon.",
        pestana_activa="high-yield-dividend-stocks.html",
        contenido_filas=renderizar_filas(datos_high_yield),
        alerta="<strong>Yield Caution:</strong> Abnormally high yields (>10%) may signal dividend sustainability risks or declining stock prices.",
        fecha_iso=hoy.isoformat(),
        texto_seo="""
        <h2>Evaluating High Yield Opportunities</h2>
        <p>Stocks yielding above 6% offer substantial cash return, but require thorough fundamental verification. When evaluating high yield opportunities:</p>
        <ul>
            <li><strong>Review Payout Ratio:</strong> Ensure operational free cash flow covers regular payouts without relying on debt issuance.</li>
            <li><strong>Identify Value Traps:</strong> A high dividend yield can be an artifact of a collapsing share price rather than corporate strength.</li>
        </ul>
        """
    ))

# ==========================================
# 7. LONG TAIL: DIVIDEND ARISTOCRATS
# ==========================================
datos_aristocrats = [r for r in todos_los_registros if str(r.get("symbol", "")).upper() in ARISTOCRATS]
with open("dividend-aristocrats.html", "w", encoding="utf-8") as f:
    f.write(generar_plantilla(
        titulo="Dividend Aristocrats Ex-Dividend Radar",
        subtitulo="Upcoming payout schedules for elite S&P 500 companies with 25+ consecutive years of dividend increases.",
        pestana_activa="dividend-aristocrats.html",
        contenido_filas=renderizar_filas(datos_aristocrats),
        alerta="<strong>Elite Quality:</strong> Dividend Aristocrats have increased dividend distributions through recessions, market crashes, and inflationary periods.",
        fecha_iso=hoy.isoformat(),
        texto_seo="""
        <h2>The S&P 500 Dividend Aristocrat Advantage</h2>
        <p>To qualify as a Dividend Aristocrat, a company must belong to the S&P 500 and demonstrate at least 25 consecutive years of increasing its base annual dividend payout.</p>
        <h2>Why Institutional Investors Prefer Aristocrats</h2>
        <p>Consistent dividend growth signals pricing power, strong balance sheet management, and durable competitive moats. Companies such as Coca-Cola (KO), Johnson & Johnson (JNJ), and Procter & Gamble (PG) form the backbone of conservative income portfolios worldwide.</p>
        """
    ))

# ==========================================
# 8. SITEMAP.XML COMPLETO PARA GOOGLE SEARCH CONSOLE
# ==========================================
paginas_sitemap = [
    ("index.html", "1.0", "daily"),
    ("tomorrow.html", "0.9", "daily"),
    ("this-week.html", "0.9", "daily"),
    ("next-week.html", "0.8", "daily"),
    ("monthly-dividend-stocks.html", "0.9", "daily"),
    ("high-yield-dividend-stocks.html", "0.9", "daily"),
    ("dividend-aristocrats.html", "0.8", "daily"),
    ("guide.html", "0.7", "weekly"),
    ("about.html", "0.5", "monthly"),
]

sitemap_items = ""
for url, prio, freq in paginas_sitemap:
    sitemap_items += f"""  <url>
    <loc>https://dividendradar.netlify.app/{url}</loc>
    <lastmod>{hoy.strftime('%Y-%m-%d')}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{prio}</priority>
  </url>\n"""

sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{sitemap_items}</urlset>
"""

with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap_xml)

print("Todas las páginas long tail, micronichos y sitemap.xml generados exitosamente.")
