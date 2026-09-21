import datetime
import html
import json
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": "https://www.nasdaq.com",
    "Referer": "https://www.nasdaq.com/"
}

MONTHLY_PAYERS = {
    "O", "MAIN", "STAG", "AGNC", "PSEC", "LAND", "LTC", "EPR", "GLAD", "GOOD",
    "GAIN", "SLG", "ADC", "SJTR", "GWRS", "PBA", "JEPI", "JEPQ", "DIVO"
}

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
    try:
        limpio = str(yield_str).replace("%", "").replace(",", "").strip()
        return float(limpio)
    except:
        return 0.0

def renderizar_filas(rows):
    if not rows:
        return "<tr><td colspan='6' style='text-align:center; padding: 2rem; color: #8b949e;'>No dividend declarations found for this specific period or screener criteria.</td></tr>"
    
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

CALCULADORA_HTML = """
<div class="calc-card">
  <div class="calc-header">
    <h3>🧮 Interactive Dividend Yield & Cash Flow Calculator</h3>
    <p>Estimate your passive income, distribution paychecks, and long-term compound growth.</p>
  </div>
  <div class="calc-grid">
    <div class="calc-input">
      <label for="inv-amount">Total Investment ($):</label>
      <input type="number" id="inv-amount" value="5000" step="500" oninput="calcularDividendos()">
    </div>
    <div class="calc-input">
      <label for="inv-yield">Annual Dividend Yield (%):</label>
      <input type="number" id="inv-yield" value="4.5" step="0.1" oninput="calcularDividendos()">
    </div>
    <div class="calc-input">
      <label for="inv-frequency">Payout Frequency:</label>
      <select id="inv-frequency" onchange="calcularDividendos()">
        <option value="4">Quarterly (4x/year)</option>
        <option value="12">Monthly (12x/year)</option>
        <option value="2">Semi-Annual (2x/year)</option>
        <option value="1">Annual (1x/year)</option>
      </select>
    </div>
  </div>
  <div class="calc-results">
    <div class="result-box">
      <span class="label">Annual Passive Income:</span>
      <span class="value text-accent" id="res-annual">$225.00</span>
    </div>
    <div class="result-box">
      <span class="label">Per Distribution Payout:</span>
      <span class="value" id="res-payout">$56.25</span>
    </div>
    <div class="result-box">
      <span class="label">10-Year DRIP Forecast:</span>
      <span class="value text-primary" id="res-drip">$7,764.85</span>
    </div>
  </div>
</div>
"""

CALCULADORA_JS = """
<script>
function calcularDividendos() {
  const capital = parseFloat(document.getElementById('inv-amount').value) || 0;
  const yieldPct = parseFloat(document.getElementById('inv-yield').value) || 0;
  const frequency = parseInt(document.getElementById('inv-frequency').value) || 4;

  const annualIncome = capital * (yieldPct / 100);
  const perPayout = annualIncome / frequency;

  const rate = yieldPct / 100;
  const drip10Years = capital * Math.pow((1 + rate / frequency), frequency * 10);

  document.getElementById('res-annual').innerText = '$' + annualIncome.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
  document.getElementById('res-payout').innerText = '$' + perPayout.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
  document.getElementById('res-drip').innerText = '$' + drip10Years.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
}
window.addEventListener('DOMContentLoaded', calcularDividendos);
</script>
"""

def generar_faqs_html(faqs_list):
    if not faqs_list:
        return "", ""
    
    faq_html = '<div class="faq-container"><h2>Frequently Asked Questions</h2>'
    faq_schema_entities = []

    for item in faqs_list:
        q = html.escape(item["q"])
        a = item["a"] # Puede contener enlaces limpios
        
        faq_html += f"""
        <details class="faq-item">
          <summary><strong>{q}</strong></summary>
          <div class="faq-answer"><p>{a}</p></div>
        </details>
        """
        faq_schema_entities.append({
            "@type": "Question",
            "name": item["q"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": item["a_plana"]
            }
        })
    faq_html += '</div>'

    schema_faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faq_schema_entities
    }
    schema_faq_tag = f'<script type="application/ld+json">{json.dumps(schema_faq)}</script>'

    return faq_html, schema_faq_tag

def generar_plantilla(titulo, subtitulo, pestana_activa, contenido_filas, alerta="", fecha_iso="", guia_html="", faqs_list=None, con_calculadora=True):
    nav_links = [
        ("index.html", "Today"),
        ("tomorrow.html", "Tomorrow"),
        ("this-week.html", "This Week"),
        ("next-week.html", "Next Week"),
        ("monthly-dividend-stocks.html", "Monthly"),
        ("high-yield-dividend-stocks.html", "High Yield"),
        ("dividend-aristocrats.html", "Aristocrats"),
        ("best-dividend-etfs.html", "ETFs"),
        ("reit-bdc-dividend-guide.html", "REITs & BDCs"),
        ("dividend-growth-investing.html", "DGI Strategy"),
        ("drip-calculator-guide.html", "DRIP"),
        ("payout-ratio-safety.html", "Safety"),
        ("qualified-vs-ordinary-dividends.html", "Taxes")
    ]
    
    nav_html = ""
    for url, label in nav_links:
        active_cls = ' class="active"' if pestana_activa == url else ''
        nav_html += f'<a href="{url}"{active_cls}>{label}</a>\n'

    alert_box = f'<div class="callout">{alerta}</div>' if alerta else ""
    widget_calc = CALCULADORA_HTML if con_calculadora else ""
    faq_rendered_html, faq_schema_tag = generar_faqs_html(faqs_list or [])

    schema_webpage = f"""
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
  {schema_webpage}
  {faq_schema_tag}
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
      gap: 0.35rem;
    }}
    nav a {{
      color: var(--text-muted);
      text-decoration: none;
      font-size: 0.85rem;
      padding: 0.3rem 0.55rem;
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
    .calc-card {{
      background: #1c2128;
      border: 1px solid #444c56;
      border-radius: 8px;
      padding: 1.5rem;
      margin-bottom: 2rem;
    }}
    .calc-header h3 {{
      color: #fff;
      margin-top: 0;
      font-size: 1.25rem;
      margin-bottom: 0.3rem;
    }}
    .calc-header p {{
      color: var(--text-muted);
      font-size: 0.9rem;
      margin-top: 0;
      margin-bottom: 1.2rem;
    }}
    .calc-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 1rem;
      margin-bottom: 1.2rem;
    }}
    .calc-input label {{
      display: block;
      color: var(--text);
      font-size: 0.85rem;
      font-weight: 600;
      margin-bottom: 0.4rem;
    }}
    .calc-input input, .calc-input select {{
      width: 100%;
      background: var(--card);
      border: 1px solid var(--border);
      color: #fff;
      padding: 0.6rem 0.8rem;
      border-radius: 6px;
      font-size: 0.95rem;
      outline: none;
    }}
    .calc-input input:focus, .calc-input select:focus {{
      border-color: var(--primary);
    }}
    .calc-results {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 1rem;
      padding-top: 1rem;
      border-top: 1px solid var(--border);
    }}
    .result-box {{
      background: rgba(0,0,0,0.2);
      padding: 0.8rem 1rem;
      border-radius: 6px;
      border: 1px solid rgba(255,255,255,0.05);
    }}
    .result-box .label {{
      display: block;
      font-size: 0.8rem;
      color: var(--text-muted);
      margin-bottom: 0.2rem;
    }}
    .result-box .value {{
      font-size: 1.3rem;
      font-weight: bold;
      color: #fff;
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
    .text-primary {{ color: var(--primary); }}
    .font-bold {{ font-weight: bold; }}
    .num {{ text-align: right; }}
    th.num {{ text-align: right; }}
    .editorial {{
      margin-top: 3rem;
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 2.2rem;
    }}
    .editorial h2 {{
      color: #fff;
      font-size: 1.4rem;
      margin-top: 1.8rem;
      border-bottom: 1px solid var(--border);
      padding-bottom: 0.5rem;
    }}
    .editorial h2:first-child {{
      margin-top: 0;
    }}
    .editorial h3 {{
      color: var(--primary);
      font-size: 1.15rem;
      margin-top: 1.4rem;
    }}
    .editorial p, .editorial li {{
      color: var(--text-muted);
      line-height: 1.7;
    }}
    .editorial ul, .editorial ol {{
      padding-left: 1.5rem;
    }}
    .editorial li {{
      margin-bottom: 0.5rem;
    }}
    .editorial a {{
      color: var(--primary);
      text-decoration: none;
    }}
    .editorial a:hover {{
      text-decoration: underline;
    }}
    /* FAQS ACCORDION */
    .faq-container {{
      margin-top: 2.5rem;
      border-top: 1px solid var(--border);
      padding-top: 1.5rem;
    }}
    .faq-item {{
      background: #1c2128;
      border: 1px solid var(--border);
      border-radius: 6px;
      margin-bottom: 0.8rem;
      padding: 0.9rem 1.2rem;
    }}
    .faq-item summary {{
      cursor: pointer;
      color: #fff;
      font-size: 1rem;
      outline: none;
    }}
    .faq-item summary:hover {{
      color: var(--primary);
    }}
    .faq-answer {{
      margin-top: 0.8rem;
      padding-top: 0.8rem;
      border-top: 1px solid rgba(255,255,255,0.05);
    }}
    .faq-answer p {{
      margin: 0;
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
    {widget_calc}

    {'<div class="search-box"><input type="text" id="filtro" placeholder="Search by ticker or company name..." onkeyup="filtrarTabla()"><span style="font-size: 0.85rem; color: var(--text-muted);">Data feed: <a href="https://www.nasdaq.com" target="_blank" rel="noopener noreferrer" style="color: var(--primary); text-decoration: none;">Nasdaq API Live</a></span></div><div class="table-container"><table id="tabla-dividendos"><thead><tr><th>Symbol</th><th>Company Name</th><th class="num">Cash Amount</th><th class="num">Yield (%)</th><th>Ex-Dividend Date</th><th>Pay Date</th></tr></thead><tbody>' + contenido_filas + '</tbody></table></div>' if contenido_filas else ''}

    <section class="editorial">
      {guia_html}
      {faq_rendered_html}
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
      <a href="best-dividend-etfs.html">Dividend ETFs</a> |
      <a href="reit-bdc-dividend-guide.html">REITs & BDCs</a> |
      <a href="dividend-growth-investing.html">DGI Guide</a> |
      <a href="special-dividends-explained.html">Special Dividends</a> |
      <a href="drip-calculator-guide.html">DRIP</a> |
      <a href="payout-ratio-safety.html">Safety</a> |
      <a href="qualified-vs-ordinary-dividends.html">Taxes</a> |
      <a href="about.html">About</a> |
      <a href="terms.html">Terms</a> |
      <a href="privacy.html">Privacy</a>
    </p>
    <p style="margin-top: 1rem; color: #58a6ff;">Contact: support@dividendradar.com</p>
  </footer>

  {CALCULADORA_JS if con_calculadora else ''}
  <script>
    function filtrarTabla() {{
      const input = document.getElementById("filtro");
      if(!input) return;
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

pool_total = []
dias_a_descargar = set(dias_esta_semana + dias_proxima_semana + [hoy, manana])
for dia in dias_a_descargar:
    pool_total.extend(obtener_datos_fecha(dia.strftime("%Y-%m-%d")))

pool_unicos = {}
for item in pool_total:
    clave = f"{item.get('symbol')}_{item.get('dividend_Ex_Date')}"
    pool_unicos[clave] = item
todos_los_registros = list(pool_unicos.values())

print(f"Total registros únicos procesados: {len(todos_los_registros)}")

# ==============================================================================
# 1. TODAY'S EX-DIVIDEND STOCKS (index.html)
# ==============================================================================
guia_today = """
<h2>Understanding Today's Ex-Dividend Trading Session</h2>
<p>When an equity trades <strong>ex-dividend today</strong>, it has reached its official regulatory cutoff point. Under U.S. Securities and Exchange Commission (SEC) settlement regulations, trading ex-dividend means the right to the upcoming dividend has officially detached from the stock certificate.</p>

<h3>What Happens to the Stock Price Today?</h3>
<p>On the morning of the ex-date, the opening share price is automatically adjusted downward by the exchange by approximately the exact declared dividend cash amount. Because the company will disburse capital from its treasury to shareholders, the enterprise value of the firm contracts by that precise cash sum. If external broader market momentum is neutral, an equity trading at $50 that declared a $1.00 dividend will open around $49.00.</p>

<h3>Can You Buy Today and Receive the Dividend?</h3>
<p><strong>No.</strong> Purchasing shares on or after the ex-dividend date disqualifies you from the declared payment. The cash disbursement will be routed to the previous shareholder who owned the shares prior to this morning's market open. To receive upcoming payments, plan your orders ahead using our <a href="tomorrow.html">Tomorrow Ex-Dividend Calendar</a>.</p>
"""

faqs_today = [
    {
        "q": "If I buy a stock on its ex-dividend date today, do I get the dividend?",
        "a": "No. You must purchase shares at least one full business day before the ex-dividend date. If you buy today, the dividend belongs to the previous owner.",
        "a_plana": "No. You must purchase shares at least one full business day before the ex-dividend date. If you buy today, the dividend belongs to the previous owner."
    },
    {
        "q": "Why did the stock open lower today despite no bad earnings news?",
        "a": "Stock exchanges automatically adjust opening prices down by the approximate declared dividend cash amount to reflect corporate cash leaving the company balance sheet.",
        "a_plana": "Stock exchanges automatically adjust opening prices down by the approximate declared dividend cash amount to reflect corporate cash leaving the company balance sheet."
    },
    {
        "q": "Can I sell my stock today and still receive the payout?",
        "a": "Yes! If you held the stock before today's market opening bell and sell at any time on or after the ex-dividend date, you remain fully entitled to receive the dividend on the payment date.",
        "a_plana": "Yes! If you held the stock before today's market opening bell and sell at any time on or after the ex-dividend date, you remain fully entitled to receive the dividend on the payment date."
    }
]

datos_hoy = obtener_datos_fecha(hoy.strftime("%Y-%m-%d"))
with open("index.html", "w", encoding="utf-8") as f:
    f.write(generar_plantilla(
        titulo="Today's Ex-Dividend Stocks Calendar",
        subtitulo=f"Real-time U.S. equities trading ex-dividend today, {hoy.strftime('%B %d, %Y')}.",
        pestana_activa="index.html",
        contenido_filas=renderizar_filas(datos_hoy),
        alerta="<strong>Notice:</strong> Equities listed below are trading ex-dividend today. Purchasing shares today will NOT qualify for the current declared distribution.",
        fecha_iso=hoy.isoformat(),
        guia_html=guia_today,
        faqs_list=faqs_today
    ))

# ==============================================================================
# 2. TOMORROW'S EX-DIVIDEND STOCKS (tomorrow.html)
# ==============================================================================
guia_tomorrow = """
<h2>Immediate Action Radar: Stocks Going Ex-Dividend Tomorrow</h2>
<p>This is the most critical actionable page for income investors and dividend capture strategists. The securities listed below will cross their ex-dividend threshold tomorrow morning. <strong>Today represents your final trading window to acquire these positions</strong> if you wish to receive the declared dividend payment.</p>

<h3>The Execution Deadline: 4:00 PM EST</h3>
<p>To lock in eligibility, your buy order must execute before the regular New York market closing bell today (4:00 PM Eastern Standard Time). After-hours trades executed after 4:00 PM often have delayed settlement status depending on your brokerage platform, which can forfeit your entitlement to the dividend.</p>

<h3>Tactical Checklist Before Entering Today:</h3>
<ul>
  <li><strong>Check Trading Volume and Liquidity:</strong> Ensure the equity has sufficient daily volume and a tight bid-ask spread to avoid slippage on execution.</li>
  <li><strong>Inspect Payout Ratio Sustainability:</strong> Verify whether the company generates genuine cash flow or is funding payouts through debt by reviewing our <a href="payout-ratio-safety.html">Payout Ratio Safety Guide</a>.</li>
  <li><strong>Tax Bracket Considerations:</strong> Buying right before ex-date results in short-term holding periods, qualifying distributions for ordinary income tax instead of lower capital gains brackets. See our <a href="qualified-vs-ordinary-dividends.html">Qualified Dividend Tax Guide</a>.</li>
</ul>
"""

faqs_tomorrow = [
    {
        "q": "What is the exact deadline to buy a stock going ex-dividend tomorrow?",
        "a": "You must buy shares before today's standard market close (4:00 PM Eastern Time). Executing today guarantees your trade settles on time to establish shareholder of record status.",
        "a_plana": "You must buy shares before today's standard market close (4:00 PM Eastern Time). Executing today guarantees your trade settles on time to establish shareholder of record status."
    },
    {
        "q": "What is the Dividend Capture Strategy?",
        "a": "It is an active trading methodology where an investor buys an equity right before the ex-date, captures the dividend distribution rights, and attempts to sell the shares once the price recovers post-cutoff.",
        "a_plana": "It is an active trading methodology where an investor buys an equity right before the ex-date, captures the dividend distribution rights, and attempts to sell the shares once the price recovers post-cutoff."
    },
    {
        "q": "When will the cash dividend actually arrive in my brokerage account?",
        "a": "The money arrives on the scheduled 'Payment Date' listed in the final column of our table, which is typically 2 to 4 weeks after the ex-dividend date.",
        "a_plana": "The money arrives on the scheduled 'Payment Date' listed in the final column of our table, which is typically 2 to 4 weeks after the ex-dividend date."
    }
]

datos_manana = obtener_datos_fecha(manana.strftime("%Y-%m-%d"))
with open("tomorrow.html", "w", encoding="utf-8") as f:
    f.write(generar_plantilla(
        titulo="Stocks Going Ex-Dividend Tomorrow",
        subtitulo=f"Critical cutoff calendar for tomorrow, {manana.strftime('%B %d, %Y')}. Action required before today's market close.",
        pestana_activa="tomorrow.html",
        contenido_filas=renderizar_filas(datos_manana),
        alerta="<strong>Action Required:</strong> To receive these declared payouts, you must purchase qualifying shares before today's closing bell (4:00 PM EST).",
        fecha_iso=hoy.isoformat(),
        guia_html=guia_tomorrow,
        faqs_list=faqs_tomorrow
    ))

# ==============================================================================
# 3. THIS WEEK (this-week.html)
# ==============================================================================
guia_this_week = """
<h2>Weekly Dividend Income Outlook & Capital Allocation</h2>
<p>Tracking the weekly schedule enables portfolio managers and retail investors to stage capital across various sectors without concentrating ex-date risk on a single trading session. Corporate distributions across NYSE, NASDAQ, and AMEX occur continuously throughout the five-day trading week.</p>

<h3>Building a Weekly Dividend Income Ladder</h3>
<p>Investors can systematically diversify their monthly passive cash flow by staggering positions across companies with differing ex-dates and payment cycles. By combining defensive blue chips, high-yielding Real Estate Investment Trusts, and monthly payers, you can generate regular cash flow distributed evenly throughout the quarter.</p>

<h3>Key Variables to Screen Every Week:</h3>
<ol>
  <li><strong>Yield on Cost Potential:</strong> Prioritize companies that regularly grow distributions over static high-yield traps. Review our <a href="dividend-growth-investing.html">Dividend Growth Guide</a>.</li>
  <li><strong>Ex-Date vs. Record Date:</strong> Remember that exchange ex-dates always precede the corporate record date to account for settlement clearing times.</li>
  <li><strong>Reinvestment Compounding:</strong> Run our interactive calculator above to see how automatic reinvestment (DRIP) amplifies weekly declared dividends over a multi-year horizon.</li>
</ol>
"""

faqs_this_week = [
    {
        "q": "How often is this weekly ex-dividend calendar updated?",
        "a": "Our automated market scraper queries official Nasdaq data feeds daily before the New York opening bell to ensure all declared corporate corporate actions are current.",
        "a_plana": "Our automated market scraper queries official Nasdaq data feeds daily before the New York opening bell to ensure all declared corporate corporate actions are current."
    },
    {
        "q": "Why do ex-dividend dates rarely fall on weekends or market holidays?",
        "a": "Ex-dividend dates are tied directly to active exchange trading sessions. If markets are closed, clearing and settlement mechanisms do not operate.",
        "a_plana": "Ex-dividend dates are tied directly to active exchange trading sessions. If markets are closed, clearing and settlement mechanisms do not operate."
    },
    {
        "q": "How can I filter this weekly table for specific high-yield stocks?",
        "a": "Use the real-time search box above the table to search by company ticker, name, or inspect our pre-screened <a href='high-yield-dividend-stocks.html'>High Yield Screener (>6%)</a>.",
        "a_plana": "Use the real-time search box above the table to search by company ticker, name, or inspect our pre-screened High Yield Screener (>6%)."
    }
]

datos_esta_semana = [r for r in todos_los_registros if any(d.strftime("%m/%d/%Y") in str(r.get("dividend_Ex_Date", "")) for d in dias_esta_semana)]
with open("this-week.html", "w", encoding="utf-8") as f:
    f.write(generar_plantilla(
        titulo="Ex-Dividend Stocks This Week",
        subtitulo=f"Complete schedule of U.S. equities going ex-dividend between {dias_esta_semana[0].strftime('%b %d')} and {dias_esta_semana[-1].strftime('%b %d, %Y')}.",
        pestana_activa="this-week.html",
        contenido_filas=renderizar_filas(datos_esta_semana),
        alerta="<strong>Weekly Outlook:</strong> Plan your capital allocation for the entire current trading week across NYSE and NASDAQ securities.",
        fecha_iso=hoy.isoformat(),
        guia_html=guia_this_week,
        faqs_list=faqs_this_week
    ))

# ==============================================================================
# 4. NEXT WEEK (next-week.html)
# ==============================================================================
guia_next_week = """
<h2>Advance Planning: Ex-Dividend Equities for Next Week</h2>
<p>High-performing income investors don't scramble at the last minute; they formulate watchlists well in advance. Reviewing the upcoming week's dividend announcements allows you to perform thorough fundamental research, analyze quarterly financial statements, and place disciplined limit buy orders ahead of institutional price moves.</p>

<h3>Benefits of Planning One Week Ahead:</h3>
<ul>
  <li><strong>Avoiding Emotional Chasing:</strong> Entering orders during market spikes immediately before ex-dates often erodes your return through higher share acquisition prices.</li>
  <li><strong>Detailed Balance Sheet Due Diligence:</strong> Evaluate company debt ratios, free cash flow conversion, and payout sustainability without time pressure. Check our <a href="payout-ratio-safety.html">Safety Framework</a>.</li>
  <li><strong>Monitoring Pre-Ex-Date Price Rallies:</strong> High-yield stocks frequently appreciate several days prior to their ex-date as retail dividend capture traders accumulate shares.</li>
</ul>
"""

faqs_next_week = [
    {
        "q": "Can companies cancel or alter next week's dividend before the ex-date?",
        "a": "While rare, a company's board of directors can legally revise or cancel a declared dividend in instances of severe financial distress or bankruptcy before settlement.",
        "a_plana": "While rare, a company's board of directors can legally revise or cancel a declared dividend in instances of severe financial distress or bankruptcy before settlement."
    },
    {
        "q": "Is it better to buy shares next week or wait until the stock trades ex-dividend?",
        "a": "It depends on your strategy. If you buy before ex-date, you collect the cash dividend but absorb the price markdown. If you buy after ex-date, you acquire shares at a lower base price without receiving the current distribution.",
        "a_plana": "It depends on your strategy. If you buy before ex-date, you collect the cash dividend but absorb the price markdown. If you buy after ex-date, you acquire shares at a lower base price without receiving the current distribution."
    }
]

datos_proxima_semana = [r for r in todos_los_registros if any(d.strftime("%m/%d/%Y") in str(r.get("dividend_Ex_Date", "")) for d in dias_proxima_semana)]
with open("next-week.html", "w", encoding="utf-8") as f:
    f.write(generar_plantilla(
        titulo="Ex-Dividend Stocks Next Week",
        subtitulo=f"Advance radar for upcoming corporate payouts from {dias_proxima_semana[0].strftime('%b %d')} to {dias_proxima_semana[-1].strftime('%b %d, %Y')}.",
        pestana_activa="next-week.html",
        contenido_filas=renderizar_filas(datos_proxima_semana),
        alerta="<strong>Advance Planning:</strong> Upcoming dividend schedule for next week. Conduct due diligence prior to establishing positions.",
        fecha_iso=hoy.isoformat(),
        guia_html=guia_next_week,
        faqs_list=faqs_next_week
    ))

# ==============================================================================
# 5. MONTHLY DIVIDEND STOCKS (monthly-dividend-stocks.html)
# ==============================================================================
guia_monthly = """
<h2>Why Investors Prioritize Monthly Dividend Paying Stocks</h2>
<p>The vast majority of public U.S. corporations distribute dividends on a quarterly schedule (every three months). However, income-focused retirees and living-off-dividends investors often prefer companies that distribute payments <strong>twelve times per year</strong> to align with recurring household bills and mortgage liabilities.</p>

<h3>Key Vehicles Delivering Monthly Payouts:</h3>
<ul>
  <li><strong>Real Estate Investment Trusts (REITs):</strong> Commercial and industrial REITs like Realty Income (O) and STAG Industrial (STAG) lease physical properties and distribute monthly rental income to shareholders.</li>
  <li><strong>Business Development Companies (BDCs):</strong> Companies like Main Street Capital (MAIN) provide debt capital to middle-market businesses, generating high loan interest yields disbursed monthly.</li>
  <li><strong>Covered Call ETFs:</strong> Derivative-enhanced funds like JEPI and JEPQ write call options on equity portfolios to deliver substantial monthly yield payouts. See our <a href="best-dividend-etfs.html">Dividend ETF Guide</a>.</li>
</ul>

<h3>The Compounding Advantage of Monthly Reinvestment</h3>
<p>Because payouts occur 12 times a year instead of 4, automated dividend reinvestment (DRIP) compounds your invested capital faster. Each monthly disbursement buys fractional shares that immediately begin generating their own income the very next month.</p>
"""

faqs_monthly = [
    {
        "q": "Are monthly dividend stocks safer than quarterly stocks?",
        "a": "Not inherently. A monthly payout frequency is simply a corporate scheduling choice. Dividend safety depends strictly on business cash flow, debt leverage, and payout ratios, not payout frequency.",
        "a_plana": "Not inherently. A monthly payout frequency is simply a corporate scheduling choice. Dividend safety depends strictly on business cash flow, debt leverage, and payout ratios, not payout frequency."
    },
    {
        "q": "How are monthly REIT dividends taxed by the IRS?",
        "a": "Because REITs do not pay federal corporate tax, their dividends are typically classified as ordinary income rather than lower-taxed qualified dividends. Learn more in our <a href='qualified-vs-ordinary-dividends.html'>Tax Guide</a>.",
        "a_plana": "Because REITs do not pay federal corporate tax, their dividends are typically classified as ordinary income rather than lower-taxed qualified dividends."
    }
]

datos_monthly = [r for r in todos_los_registros if str(r.get("symbol", "")).upper() in MONTHLY_PAYERS]
with open("monthly-dividend-stocks.html", "w", encoding="utf-8") as f:
    f.write(generar_plantilla(
        titulo="Monthly Dividend Stocks Calendar",
        subtitulo="High-income equities, monthly REITs, and business development companies distributing cash flow every 30 days.",
        pestana_activa="monthly-dividend-stocks.html",
        contenido_filas=renderizar_filas(datos_monthly),
        alerta="<strong>Predictable Cash Flow:</strong> Monthly paying dividend stocks distribute income 12 times a year, accelerating portfolio compounding.",
        fecha_iso=hoy.isoformat(),
        guia_html=guia_monthly,
        faqs_list=faqs_monthly
    ))

# ==============================================================================
# 6. HIGH YIELD (>6%) (high-yield-dividend-stocks.html)
# ==============================================================================
guia_high_yield = """
<h2>High Yield Screener: Navigating Equities Yielding Over 6.0%</h2>
<p>An annual dividend yield exceeding 6% offers immediate cash return, but it demands strict fundamental skepticism. In financial markets, yield is inversely proportional to share price: <em>Dividend Yield = Annual Dividend / Stock Price</em>. When a stock price collapses due to deteriorating business conditions, its nominal yield spikes to artificial double-digit levels, creating a <strong>Value Trap</strong>.</p>

<h3>How to Distinguish Real High Yield from Dangerous Traps:</h3>
<ol>
  <li><strong>Check Free Cash Flow Coverage:</strong> Net income can be manipulated by accounting adjustments, but cash flow cannot. Ensure Free Cash Flow comfortably exceeds declared dividends.</li>
  <li><strong>Beware of Special Dividends:</strong> Sometimes a massive yield is caused by a one-time windfall distribution that will not repeat. Read our <a href="special-dividends-explained.html">Special Dividends Breakdown</a>.</li>
  <li><strong>Examine Debt Maturity Profiles:</strong> In higher interest rate regimes, highly levered companies may be forced to slash dividends to refinance maturing bonds.</li>
</ol>
"""

faqs_high_yield = [
    {
        "q": "Is an 8% or 10% dividend yield sustainable long-term?",
        "a": "In capital-intensive sectors or standard corporations, yields above 8% often signal severe market distress and risk of an upcoming dividend cut. However, specialized pass-through structures like BDCs, Master Limited Partnerships (MLPs), and Covered Call ETFs can legitimately sustain higher yields.",
        "a_plana": "In capital-intensive sectors or standard corporations, yields above 8% often signal severe market distress and risk of an upcoming dividend cut. However, specialized pass-through structures like BDCs, Master Limited Partnerships (MLPs), and Covered Call ETFs can legitimately sustain higher yields."
    },
    {
        "q": "What happens to a stock's price when its dividend is cut?",
        "a": "Historically, when a high-yield company announces a dividend reduction or suspension, its stock price drops sharply (often 10% to 25% in a single trading session) as income funds dump shares.",
        "a_plana": "Historically, when a high-yield company announces a dividend reduction or suspension, its stock price drops sharply (often 10% to 25% in a single trading session) as income funds dump shares."
    }
]

datos_high_yield = [r for r in todos_los_registros if limpiar_yield(r.get("annual_Yield")) >= 6.0]
datos_high_yield.sort(key=lambda x: limpiar_yield(x.get("annual_Yield")), reverse=True)
with open("high-yield-dividend-stocks.html", "w", encoding="utf-8") as f:
    f.write(generar_plantilla(
        titulo="High Yield Dividend Stocks Screener (>6%)",
        subtitulo="Screen U.S. equities with declared annual dividend yields exceeding 6.0% going ex-dividend soon.",
        pestana_activa="high-yield-dividend-stocks.html",
        contenido_filas=renderizar_filas(datos_high_yield),
        alerta="<strong>Yield Caution:</strong> Abnormally high yields (>10%) may signal dividend cut risks or declining underlying stock prices.",
        fecha_iso=hoy.isoformat(),
        guia_html=guia_high_yield,
        faqs_list=faqs_high_yield
    ))

# ==============================================================================
# 7. DIVIDEND ARISTOCRATS (dividend-aristocrats.html)
# ==============================================================================
guia_aristocrats = """
<h2>The Elite S&P 500 Dividend Aristocrats</h2>
<p>To qualify as an official <strong>S&P 500 Dividend Aristocrat</strong>, an enterprise must satisfy stringent regulatory and performance criteria: it must belong to the S&P 500, maintain a minimum market capitalization of $3 billion, and crucially, <strong>increase its base annual dividend per share for at least 25 consecutive years</strong>.</p>

<h3>Why Aristocrats Deliver Superior Risk-Adjusted Returns:</h3>
<ul>
  <li><strong>Durable Economic Moats:</strong> Increasing dividends across oil shocks, recessions, the 2008 financial crisis, and global pandemics requires unshakeable competitive pricing power.</li>
  <li><strong>Prudent Capital Allocation:</strong> Management teams that commit to uninterrupted dividend growth avoid destructive speculative acquisitions and keep balance sheet leverage disciplined.</li>
  <li><strong>Inflation Hedge:</strong> Aristocrats increase their cash distributions annually, keeping pace with or outpacing real inflation rates. Learn more in our <a href="dividend-growth-investing.html">Dividend Growth Investing Guide</a>.</li>
</ul>
"""

faqs_aristocrats = [
    {
        "q": "What is the difference between a Dividend Aristocrat and a Dividend King?",
        "a": "A Dividend Aristocrat has increased its dividend payout for at least 25 consecutive years and belongs to the S&P 500. A Dividend King has increased payouts for at least 50 consecutive years, regardless of index membership.",
        "a_plana": "What is the difference between a Dividend Aristocrat and a Dividend King? A Dividend Aristocrat has increased its dividend payout for at least 25 consecutive years and belongs to the S&P 500. A Dividend King has increased payouts for at least 50 consecutive years, regardless of index membership."
    },
    {
        "q": "What happens if a Dividend Aristocrat freezes or cuts its payout?",
        "a": "It is immediately ejected from the official S&P 500 Dividend Aristocrats index at the next quarterly rebalancing, forcing institutional index funds to divest holdings.",
        "a_plana": "It is immediately ejected from the official S&P 500 Dividend Aristocrats index at the next quarterly rebalancing, forcing institutional index funds to divest holdings."
    }
]

datos_aristocrats = [r for r in todos_los_registros if str(r.get("symbol", "")).upper() in ARISTOCRATS]
with open("dividend-aristocrats.html", "w", encoding="utf-8") as f:
    f.write(generar_plantilla(
        titulo="Dividend Aristocrats Ex-Dividend Radar",
        subtitulo="Upcoming payout schedules for elite S&P 500 companies with 25+ consecutive years of annual dividend increases.",
        pestana_activa="dividend-aristocrats.html",
        contenido_filas=renderizar_filas(datos_aristocrats),
        alerta="<strong>Elite Quality:</strong> Dividend Aristocrats have increased dividend payouts through recessions, market crashes, and inflationary periods.",
        fecha_iso=hoy.isoformat(),
        guia_html=guia_aristocrats,
        faqs_list=faqs_aristocrats
    ))

# ==============================================================================
# 8-14. GUÍAS EDITORIALES DE AUTORIDAD TÓPICA (Sin tablas de Nasdaq)
# ==============================================================================

# 8. DRIP GUIDE
with open("drip-calculator-guide.html", "w", encoding="utf-8") as f:
    f.write(generar_plantilla(
        titulo="Dividend Reinvestment Plan (DRIP) Compounding Guide",
        subtitulo="How automated dividend reinvestment accelerates wealth accumulation through exponential compound interest.",
        pestana_activa="drip-calculator-guide.html",
        contenido_filas="",
        con_calculadora=True,
        fecha_iso=hoy.isoformat(),
        guia_html="""
        <h2>What is a DRIP (Dividend Reinvestment Plan)?</h2>
        <p>A Dividend Reinvestment Plan (DRIP) is an automated financial arrangement that directs your brokerage to immediately use cash dividend distributions to purchase additional whole or fractional shares of the dividend-paying entity, typically with zero transaction commissions.</p>
        
        <h2>The Mathematical Impact of DRIP Compounding</h2>
        <p>When you reinvest dividends instead of taking cash payouts, two compounding forces work in tandem:</p>
        <ol>
          <li><strong>Share Count Expansion:</strong> Every distribution increases your total share ownership without out-of-pocket capital injections.</li>
          <li><strong>Increased Future Dividends:</strong> The next dividend payout is calculated on a larger base of shares, creating an exponential "snowball effect."</li>
        </ol>
        <p>Over a 20-year horizon, historical S&P 500 data demonstrates that total returns with reinvested dividends outperform price-appreciation-only returns by more than 200%. Check our <a href="dividend-growth-investing.html">DGI Strategy Guide</a>.</p>
        """,
        faqs_list=[
            {
                "q": "Do I have to pay taxes on dividends that are automatically reinvested via DRIP?",
                "a": "Yes. The IRS treats reinvested dividends as cash income received during that tax year, even though you never transferred the money into your checking account.",
                "a_plana": "Yes. The IRS treats reinvested dividends as cash income received during that tax year, even though you never transferred the money into your checking account."
            },
            {
                "q": "Does DRIP adjust my cost basis for capital gains taxes?",
                "a": "Yes. Each DRIP share purchase creates a new tax lot with its own cost basis equal to the market price paid at the time of reinvestment.",
                "a_plana": "Yes. Does DRIP adjust my cost basis for capital gains taxes? Yes. Each DRIP share purchase creates a new tax lot with its own cost basis equal to the market price paid at the time of reinvestment."
            }
        ]
    ))

# 9. PAYOUT RATIO SAFETY
with open("payout-ratio-safety.html", "w", encoding="utf-8") as f:
    f.write(generar_plantilla(
        titulo="Dividend Safety: How to Analyze the Payout Ratio",
        subtitulo="Detecting impending dividend cuts, value traps, and evaluating free cash flow dividend sustainability.",
        pestana_activa="payout-ratio-safety.html",
        contenido_filas="",
        con_calculadora=False,
        fecha_iso=hoy.isoformat(),
        guia_html="""
        <h2>Understanding the Dividend Payout Ratio</h2>
        <p>The Dividend Payout Ratio measures the percentage of net earnings paid to shareholders as dividends. It acts as the primary indicator of dividend safety.</p>
        <div class="callout"><strong>Formula:</strong> Payout Ratio = (Total Annual Dividends / Net Income) &times; 100</div>
        
        <h2>Warning Thresholds Across Sectors:</h2>
        <ul>
          <li><strong>0% - 50%:</strong> Healthy coverage with abundant cushion for reinvestment and capital expenditure.</li>
          <li><strong>51% - 75%:</strong> Moderate safety typical for mature consumer staples and regulated utilities.</li>
          <li><strong>76% - 95%:</strong> Thin margin of safety. Highly vulnerable during macroeconomic recessions.</li>
          <li><strong>Over 100%:</strong> Critical alert. The firm is distributing more capital than it generates in GAAP earnings.</li>
        </ul>
        <p>For Real Estate entities, net income is distorted by depreciation. Learn how to evaluate REITs using AFFO in our <a href="reit-bdc-dividend-guide.html">REIT & BDC Dividend Guide</a>.</p>
        """,
        faqs_list=[
            {
                "q": "Why is Free Cash Flow payout ratio better than Net Income payout ratio?",
                "a": "Net income includes non-cash accounting items like depreciation and goodwill write-downs. Free cash flow measures actual cash in the bank, providing an accurate view of dividend affordability.",
                "a_plana": "Net income includes non-cash accounting items like depreciation and goodwill write-downs. Free cash flow measures actual cash in the bank, providing an accurate view of dividend affordability."
            }
        ]
    ))

# 10. TAXES (QUALIFIED VS ORDINARY)
with open("qualified-vs-ordinary-dividends.html", "w", encoding="utf-8") as f:
    f.write(generar_plantilla(
        titulo="Qualified vs. Ordinary Dividends: Complete IRS Tax Guide",
        subtitulo="Understand preferential capital gains rates, IRS holding period requirements, and tax-efficient portfolio management.",
        pestana_activa="qualified-vs-ordinary-dividends.html",
        contenido_filas="",
        con_calculadora=False,
        fecha_iso=hoy.isoformat(),
        guia_html="""
        <h2>Ordinary vs. Qualified Dividend Tax Rates</h2>
        <p>How dividends are taxed depends on IRS classification:</p>
        <ul>
          <li><strong>Ordinary Dividends:</strong> Taxed as regular income (up to 37%). Typical for REITs, BDCs, and short-term holdings.</li>
          <li><strong>Qualified Dividends:</strong> Taxed at favorable long-term capital gains rates (0%, 15%, or 20% depending on taxable income).</li>
        </ul>
        <h2>The Crucial 60-Day Holding Period Rule</h2>
        <p>To qualify for lower capital gains rates, shares must be held unhedged for at least 61 days during a 121-day period centered on the ex-dividend date. Short-term dividend capture traders rarely meet this requirement.</p>
        """,
        faqs_list=[
            {
                "q": "Are foreign stock dividends qualified for U.S. investors?",
                "a": "Foreign companies eligible for benefits of a comprehensive U.S. tax treaty or whose ADRs trade readily on established U.S. securities exchanges can qualify for preferential rates.",
                "a_plana": "Foreign companies eligible for benefits of a comprehensive U.S. tax treaty or whose ADRs trade readily on established U.S. securities exchanges can qualify for preferential rates."
            }
        ]
    ))

# 11. BEST DIVIDEND ETFS
with open("best-dividend-etfs.html", "w", encoding="utf-8") as f:
    f.write(generar_plantilla(
        titulo="Best Dividend ETFs for Passive Income (SCHD, VYM, JEPI)",
        subtitulo="Comparing low-cost index dividend funds, dividend growth ETFs, and high-yield covered call strategies.",
        pestana_activa="best-dividend-etfs.html",
        contenido_filas="",
        con_calculadora=True,
        fecha_iso=hoy.isoformat(),
        guia_html="""
        <h2>Why Many Investors Prefer Dividend ETFs</h2>
        <p>Exchange-Traded Funds (ETFs) eliminate single-stock dividend cut risk through broad diversification. Instead of analyzing individual balance sheets, an ETF automatically rebalances holdings according to index rules.</p>
        
        <h2>Top Tier Dividend ETFs Compared:</h2>
        <ul>
          <li><strong>Schwab U.S. Dividend Equity ETF (SCHD):</strong> The gold standard for dividend growth, screening for cash flow to total debt, return on equity, and 10 consecutive years of dividend increases.</li>
          <li><strong>Vanguard High Dividend Yield ETF (VYM):</strong> Broad market exposure tracking higher-yielding U.S. companies with an ultra-low expense ratio.</li>
          <li><strong>JPMorgan Equity Premium Income ETF (JEPI):</strong> An actively managed covered-call ETF distributing high monthly income through options premium.</li>
        </ul>
        <p>Explore monthly-paying vehicles on our <a href="monthly-dividend-stocks.html">Monthly Dividend Calendar</a>.</p>
        """,
        faqs_list=[
            {
                "q": "Is SCHD better than individual dividend stocks?",
                "a": "For passive investors, yes. SCHD provides instant exposure to over 100 financially vetted dividend-growing businesses, shielding you from individual bankruptcy risks.",
                "a_plana": "For passive investors, yes. SCHD provides instant exposure to over 100 financially vetted dividend-growing businesses, shielding you from individual bankruptcy risks."
            }
        ]
    ))

# 12. REITS & BDCS DIVIDEND GUIDE
with open("reit-bdc-dividend-guide.html", "w", encoding="utf-8") as f:
    f.write(generar_plantilla(
        titulo="REITs & BDCs High-Yield Guide: FFO, AFFO & Debt Safety",
        subtitulo="Mastering real estate investment trusts and business development companies for maximum monthly income.",
        pestana_activa="reit-bdc-dividend-guide.html",
        contenido_filas="",
        con_calculadora=False,
        fecha_iso=hoy.isoformat(),
        guia_html="""
        <h2>The Special Regulatory Structure of REITs & BDCs</h2>
        <p>Real Estate Investment Trusts (REITs) and Business Development Companies (BDCs) are legally mandated by Congress to pay out at least <strong>90% of their taxable income</strong> to shareholders as dividends in exchange for paying zero corporate income taxes.</p>
        
        <h2>Why Traditional P/E Ratios Fail for REITs</h2>
        <p>Real estate properties carry heavy GAAP depreciation write-offs, which artificially depress net earnings while physical properties often appreciate in value. Smart investors measure performance using:</p>
        <ul>
          <li><strong>Funds From Operations (FFO):</strong> Net income plus depreciation and amortization, minus property sales gains.</li>
          <li><strong>Adjusted Funds From Operations (AFFO):</strong> FFO minus recurring maintenance capital expenditures; the truest metric of dividend safety.</li>
        </ul>
        <p>Review taxation details in our <a href="qualified-vs-ordinary-dividends.html">Qualified vs. Ordinary Tax Guide</a>.</p>
        """,
        faqs_list=[
            {
                "q": "Why do interest rates affect REIT stock prices so heavily?",
                "a": "REITs rely continuously on debt issuance to buy commercial real estate properties. When interest rates rise, borrowing costs surge and higher bond yields compete with REIT dividend yields.",
                "a_plana": "REITs rely continuously on debt issuance to buy commercial real estate properties. When interest rates rise, borrowing costs surge and higher bond yields compete with REIT dividend yields."
            }
        ]
    ))

# 13. DIVIDEND GROWTH INVESTING (DGI)
with open("dividend-growth-investing.html", "w", encoding="utf-8") as f:
    f.write(generar_plantilla(
        titulo="Dividend Growth Investing (DGI) Strategy & Yield on Cost",
        subtitulo="How focusing on dividend growth rate (DGR) beats static high-yield chasing over multi-decade time horizons.",
        pestana_activa="dividend-growth-investing.html",
        contenido_filas="",
        con_calculadora=True,
        fecha_iso=hoy.isoformat(),
        guia_html="""
        <h2>High Yield Today vs. High Dividend Growth Tomorrow</h2>
        <p>A common pitfall among novice income investors is prioritizing nominal yield today (e.g., a stagnant 8% utility) over dividend growth (e.g., a 2.5% yield compounding payouts at 10% per year).</p>
        
        <h2>The Concept of Yield on Cost (YoC)</h2>
        <p>Yield on Cost measures current annual dividend income divided by your original purchase price. An investor who bought dividend growth champions like Microsoft or Apple a decade ago enjoys a Yield on Cost exceeding 15% to 25% on original capital today.</p>

        <div class="callout">
          <strong>The Chowder Rule:</strong> Current Dividend Yield (%) + 5-Year Dividend Growth Rate (%). A score above 12% indicates high total-return compounding potential.
        </div>
        """,
        faqs_list=[
            {
                "q": "Can Dividend Growth Investing beat the S&P 500 index?",
                "a": "Historically, companies initiating and growing dividends have outperformed the broad equal-weighted S&P 500 with significantly lower downside price volatility during bear markets.",
                "a_plana": "Historically, companies initiating and growing dividends have outperformed the broad equal-weighted S&P 500 with significantly lower downside price volatility during bear markets."
            }
        ]
    ))

# 14. SPECIAL DIVIDENDS EXPLAINED
with open("special-dividends-explained.html", "w", encoding="utf-8") as f:
    f.write(generar_plantilla(
        titulo="Special Dividends vs. Regular Dividends: Investor Guide",
        subtitulo="Understanding non-recurring one-time payouts, asset sale distributions, and why annual yield calculations distort.",
        pestana_activa="special-dividends-explained.html",
        contenido_filas="",
        con_calculadora=False,
        fecha_iso=hoy.isoformat(),
        guia_html="""
        <h2>What Is a Special Dividend?</h2>
        <p>A special dividend is a non-recurring payment made by a company to shareholders, separate from its regular quarterly or monthly dividend cycle. Special dividends frequently result from exceptional one-time profits, windfall cash balances, asset divestitures, or corporate restructuring.</p>
        
        <h2>The Yield Calculation Distortion (Trap Alert)</h2>
        <p>Many financial data aggregators annualize every declared distribution by multiplying it by 4 (quarterly) or 12 (monthly). If a company paying a $0.20 regular dividend suddenly declares a $5.00 special dividend, automated screeners may falsely project a massive 40% yield. Always verify corporate press releases before buying.</p>
        """,
        faqs_list=[
            {
                "q": "Does a stock price adjust downward on a special dividend ex-date?",
                "a": "Yes. Exactly as with regular dividends, stock exchanges adjust the opening price down by the exact special dividend amount on the morning of the ex-date.",
                "a_plana": "Yes. Exactly as with regular dividends, stock exchanges adjust the opening price down by the exact special dividend amount on the morning of the ex-date."
            }
        ]
    ))

# =========================================================
# SITEMAP.XML COMPLETO
# =========================================================
paginas_sitemap = [
    ("index.html", "1.0", "daily"),
    ("tomorrow.html", "0.9", "daily"),
    ("this-week.html", "0.9", "daily"),
    ("next-week.html", "0.8", "daily"),
    ("monthly-dividend-stocks.html", "0.9", "daily"),
    ("high-yield-dividend-stocks.html", "0.9", "daily"),
    ("dividend-aristocrats.html", "0.8", "daily"),
    ("best-dividend-etfs.html", "0.8", "weekly"),
    ("reit-bdc-dividend-guide.html", "0.8", "weekly"),
    ("dividend-growth-investing.html", "0.8", "weekly"),
    ("special-dividends-explained.html", "0.7", "weekly"),
    ("drip-calculator-guide.html", "0.8", "weekly"),
    ("payout-ratio-safety.html", "0.8", "weekly"),
    ("qualified-vs-ordinary-dividends.html", "0.8", "weekly"),
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

print("Todas las páginas generadas con Guías Editoriales profundas, Acordeones FAQs y marcado Schema FAQPage.")
