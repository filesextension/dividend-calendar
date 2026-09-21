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

CALCULADORA_HTML = """
<div class="calc-card">
  <div class="calc-header">
    <h3>🧮 Interactive Dividend Yield & Income Calculator</h3>
    <p>Estimate your passive cash flow and projected payouts before entering positions.</p>
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

def generar_plantilla(titulo, subtitulo, pestana_activa, contenido_filas, alerta="", fecha_iso="", texto_seo="", con_calculadora=True):
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
    .editorial a {{
      color: var(--primary);
      text-decoration: none;
    }}
    .editorial a:hover {{
      text-decoration: underline;
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

# 1. TODAY
datos_hoy = obtener_datos_fecha(hoy.strftime("%Y-%m-%d"))
with open("index.html", "w", encoding="utf-8") as f:
    f.write(generar_plantilla(
        titulo="Today's Ex-Dividend Stocks",
        subtitulo=f"Live list of stocks going ex-dividend today, {hoy.strftime('%B %d, %Y')}.",
        pestana_activa="index.html",
        contenido_filas=renderizar_filas(datos_hoy),
        alerta="<strong>Notice:</strong> Stocks trading ex-dividend today must have been settled prior to market open to receive distributions.",
        fecha_iso=hoy.isoformat(),
        texto_seo="<h2>Today's Market Execution</h2><p>Review current-day corporate cutoffs. Learn how compound interest impacts your income in our <a href='drip-calculator-guide.html'>DRIP Strategy Guide</a> or check distribution sustainability via our <a href='payout-ratio-safety.html'>Payout Ratio Safety Framework</a>.</p>"
    ))

# 2. TOMORROW
datos_manana = obtener_datos_fecha(manana.strftime("%Y-%m-%d"))
with open("tomorrow.html", "w", encoding="utf-8") as f:
    f.write(generar_plantilla(
        titulo="Stocks Going Ex-Dividend Tomorrow",
        subtitulo=f"Critical cutoff list for tomorrow, {manana.strftime('%B %d, %Y')}. Action required today.",
        pestana_activa="tomorrow.html",
        contenido_filas=renderizar_filas(datos_manana),
        alerta="<strong>Action Required:</strong> To receive these declared dividends, you must purchase qualifying shares before today's market close (4:00 PM EST).",
        fecha_iso=hoy.isoformat(),
        texto_seo="<h2>Immediate Trade Settlement Rules</h2><p>Under SEC T+1 settlement rules, orders must execute on the session prior to the ex-date. Be mindful of tax implications detailed in our <a href='qualified-vs-ordinary-dividends.html'>Qualified Dividend Tax Breakdown</a>.</p>"
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
        texto_seo="<h2>Weekly Strategy & Capital Allocation</h2><p>Construct a diversified capture ladder across various defensive industries. Test compound yields above using our interactive projection tool.</p>"
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
        texto_seo="<h2>Advance Research Radar</h2><p>Pre-market research prevents hasty allocations into value traps. Review dividend stability and coverage ratios before adding companies to your watchlist.</p>"
    ))

# 5. MONTHLY DIVIDENDS
datos_monthly = [r for r in todos_los_registros if str(r.get("symbol", "")).upper() in MONTHLY_PAYERS]
with open("monthly-dividend-stocks.html", "w", encoding="utf-8") as f:
    f.write(generar_plantilla(
        titulo="Monthly Dividend Stocks Calendar",
        subtitulo="High-income equities, monthly REITs, and business development companies paying dividends every 30 days.",
        pestana_activa="monthly-dividend-stocks.html",
        contenido_filas=renderizar_filas(datos_monthly),
        alerta="<strong>Passive Cash Flow:</strong> Monthly paying dividend stocks provide 12 distributions per year, accelerating dividend compounding.",
        fecha_iso=hoy.isoformat(),
        texto_seo="<h2>Compounding with Monthly Distributions</h2><p>Companies paying on a monthly schedule allow investors to reinvest dividends 12 times a year rather than 4. Learn how compounding works in our <a href='drip-calculator-guide.html'>DRIP Reinvestment Guide</a> or read our sector breakdown on <a href='reit-bdc-dividend-guide.html'>REITs & BDCs</a>.</p>"
    ))

# 6. HIGH YIELD (>6%)
datos_high_yield = [r for r in todos_los_registros if limpiar_yield(r.get("annual_Yield")) >= 6.0]
datos_high_yield.sort(key=lambda x: limpiar_yield(x.get("annual_Yield")), reverse=True)
with open("high-yield-dividend-stocks.html", "w", encoding="utf-8") as f:
    f.write(generar_plantilla(
        titulo="High Yield Dividend Stocks Screener (>6%)",
        subtitulo="Screen U.S. equities with declared annual dividend yields exceeding 6.0% going ex-dividend soon.",
        pestana_activa="high-yield-dividend-stocks.html",
        contenido_filas=renderizar_filas(datos_high_yield),
        alerta="<strong>Yield Caution:</strong> Abnormally high yields (>10%) may signal dividend sustainability risks or declining stock prices.",
        fecha_iso=hoy.isoformat(),
        texto_seo="<h2>Beware of Yield Traps</h2><p>Yields over 8% require intense scrutiny of operational cash flow. Read our breakdown on <a href='payout-ratio-safety.html'>Analyzing Dividend Payout Ratios</a> or verify whether a distribution is a one-time payout in our <a href='special-dividends-explained.html'>Special Dividends Guide</a>.</p>"
    ))

# 7. ARISTOCRATS
datos_aristocrats = [r for r in todos_los_registros if str(r.get("symbol", "")).upper() in ARISTOCRATS]
with open("dividend-aristocrats.html", "w", encoding="utf-8") as f:
    f.write(generar_plantilla(
        titulo="Dividend Aristocrats Ex-Dividend Radar",
        subtitulo="Upcoming payout schedules for elite S&P 500 companies with 25+ consecutive years of dividend increases.",
        pestana_activa="dividend-aristocrats.html",
        contenido_filas=renderizar_filas(datos_aristocrats),
        alerta="<strong>Elite Quality:</strong> Dividend Aristocrats have increased dividend distributions through recessions, market crashes, and inflationary periods.",
        fecha_iso=hoy.isoformat(),
        texto_seo="<h2>The Long-Term Aristocrat Moat</h2><p>Aristocrats offer superior dividend durability. Combine high-quality balance sheets with automated reinvestment plans for multi-decade compounding wealth. Dive deeper into <a href='dividend-growth-investing.html'>Dividend Growth Investing (DGI)</a>.</p>"
    ))

# =========================================================
# TOPICAL AUTHORITY CLUSTER: GUÍAS EDITORIALES PROFUNDAS
# =========================================================

# 8. DRIP GUIDE
with open("drip-calculator-guide.html", "w", encoding="utf-8") as f:
    f.write(generar_plantilla(
        titulo="Dividend Reinvestment Plan (DRIP) Compounding Guide",
        subtitulo="How automated dividend reinvestment accelerates wealth accumulation through exponential compound interest.",
        pestana_activa="drip-calculator-guide.html",
        contenido_filas="",
        con_calculadora=True,
        fecha_iso=hoy.isoformat(),
        texto_seo="""
        <h2>What is a DRIP (Dividend Reinvestment Plan)?</h2>
        <p>A Dividend Reinvestment Plan (DRIP) is an automated financial program allowing investors to reinvest cash dividends into additional shares or fractional shares of the underlying company, typically commission-free.</p>
        <h2>The Power of Compound Yield on Cost</h2>
        <p>Reinvesting distributions compounds capital exponentially. Each reinvested payment expands your share total, generating higher subsequent dividend payments. Check dividend growth principles in our <a href="dividend-growth-investing.html">DGI Strategy Guide</a>.</p>
        """
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
        texto_seo="""
        <h2>Understanding the Dividend Payout Ratio</h2>
        <p>The Dividend Payout Ratio measures the percentage of net earnings paid to shareholders as dividends. It acts as the primary indicator of dividend safety.</p>
        <div class="callout"><strong>Formula:</strong> Payout Ratio = (Total Annual Dividends / Net Income) &times; 100</div>
        <h2>Warning Thresholds</h2>
        <ul>
          <li><strong>0% - 60%:</strong> Healthy coverage with strong reinvestment cushion.</li>
          <li><strong>61% - 85%:</strong> Moderate safety typical for consumer staples and utilities.</li>
          <li><strong>Over 100%:</strong> High alert. Company is paying out more than it earns in GAAP net income.</li>
        </ul>
        <p>For Real Estate entities, net income is distorted by depreciation. Learn how to evaluate REITs using AFFO in our <a href="reit-bdc-dividend-guide.html">REIT & BDC Dividend Guide</a>.</p>
        """
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
        texto_seo="""
        <h2>Ordinary vs. Qualified Dividend Tax Rates</h2>
        <p>How dividends are taxed depends on IRS classification:</p>
        <ul>
          <li><strong>Ordinary Dividends:</strong> Taxed as regular income (up to 37%). Typical for REITs and short-term holdings.</li>
          <li><strong>Qualified Dividends:</strong> Taxed at favorable long-term capital gains rates (0%, 15%, or 20%).</li>
        </ul>
        <h2>The 60-Day Holding Period Rule</h2>
        <p>To qualify for lower tax brackets, shares must be held unhedged for at least 61 days during a 121-day period centered on the ex-dividend date. Short-term dividend capture traders rarely meet this requirement.</p>
        """
    ))

# 11. NUEVO: BEST DIVIDEND ETFS
with open("best-dividend-etfs.html", "w", encoding="utf-8") as f:
    f.write(generar_plantilla(
        titulo="Best Dividend ETFs for Passive Income (SCHD, VYM, JEPI)",
        subtitulo="Comparing low-cost index dividend funds, dividend growth ETFs, and high-yield covered call strategies.",
        pestana_activa="best-dividend-etfs.html",
        contenido_filas="",
        con_calculadora=True,
        fecha_iso=hoy.isoformat(),
        texto_seo="""
        <h2>Why Many Investors Prefer Dividend ETFs</h2>
        <p>Exchange-Traded Funds (ETFs) eliminate single-stock dividend cut risk through broad diversification. Instead of analyzing individual balance sheets, an ETF automatically rebalances holdings according to index rules.</p>
        
        <h2>Top Tier Dividend ETFs Compared</h2>
        <ul>
          <li><strong>Schwab U.S. Dividend Equity ETF (SCHD):</strong> The gold standard for dividend growth, screening for cash flow to total debt, return on equity, and 10 consecutive years of dividend increases.</li>
          <li><strong>Vanguard High Dividend Yield ETF (VYM):</strong> Broad market exposure tracking higher-yielding U.S. companies with an ultra-low expense ratio.</li>
          <li><strong>JPMorgan Equity Premium Income ETF (JEPI):</strong> An actively managed covered-call ETF distributing high monthly income through options premium.</li>
        </ul>

        <h2>Covered Call ETFs: Income vs. Upside Capping</h2>
        <p>High-yield synthetic option ETFs (like JEPI and JEPQ) generate double-digit yields (8% to 11%), but trade away equity capital appreciation during strong bull rallies. Combine ETF research with our <a href="monthly-dividend-stocks.html">Monthly Dividend Screener</a>.</p>
        """
    ))

# 12. NUEVO: REITS & BDCS DIVIDEND GUIDE
with open("reit-bdc-dividend-guide.html", "w", encoding="utf-8") as f:
    f.write(generar_plantilla(
        titulo="REITs & BDCs High-Yield Guide: FFO, AFFO & Debt Safety",
        subtitulo="Mastering real estate investment trusts and business development companies for maximum monthly income.",
        pestana_activa="reit-bdc-dividend-guide.html",
        contenido_filas="",
        con_calculadora=False,
        fecha_iso=hoy.isoformat(),
        texto_seo="""
        <h2>The Special Regulatory Structure of REITs & BDCs</h2>
        <p>Real Estate Investment Trusts (REITs) and Business Development Companies (BDCs) are legally mandated by Congress to pay out at least <strong>90% of their taxable income</strong> to shareholders as dividends in exchange for paying zero corporate income taxes.</p>
        
        <h2>Why Traditional P&E Ratios Fail for REITs</h2>
        <p>Real estate properties carry heavy GAAP depreciation write-offs, which artificially depress net earnings while physical properties often appreciate in value. Smart investors measure performance using:</p>
        <ul>
          <li><strong>Funds From Operations (FFO):</strong> Net income plus depreciation and amortization, minus property sales gains.</li>
          <li><strong>Adjusted Funds From Operations (AFFO):</strong> FFO minus recurring maintenance capital expenditures; the truest metric of dividend safety.</li>
        </ul>

        <h2>Tax Treatment Warning</h2>
        <p>Because REITs and BDCs pay no corporate-level tax, their distributions are classified by the IRS as ordinary income rather than qualified dividends. Review our <a href="qualified-vs-ordinary-dividends.html">Tax Guide</a> to structure your holdings tax-efficiently.</p>
        """
    ))

# 13. NUEVO: DIVIDEND GROWTH INVESTING (DGI) & YIELD ON COST
with open("dividend-growth-investing.html", "w", encoding="utf-8") as f:
    f.write(generar_plantilla(
        titulo="Dividend Growth Investing (DGI) Strategy & Yield on Cost",
        subtitulo="How focusing on dividend growth rate (DGR) beats static high-yield chasing over multi-decade time horizons.",
        pestana_activa="dividend-growth-investing.html",
        contenido_filas="",
        con_calculadora=True,
        fecha_iso=hoy.isoformat(),
        texto_seo="""
        <h2>High Yield Today vs. High Dividend Growth Tomorrow</h2>
        <p>A common pitfall among novice income investors is prioritizing nominal yield today (e.g., a stagnant 8% utility) over dividend growth (e.g., a 2.5% yield compounding payouts at 10% per year).</p>
        
        <h2>The Concept of Yield on Cost (YoC)</h2>
        <p>Yield on Cost measures the current annual dividend payment divided by your original purchase price. An investor who purchased Apple or Microsoft a decade ago may enjoy a Yield on Cost exceeding 15% or 20% on original invested capital, despite current nominal yields sitting under 1%.</p>

        <h2>The Chowder Rule for Dividend Screening</h2>
        <div class="callout">
          <strong>The Chowder Number:</strong> Current Dividend Yield (%) + 5-Year Dividend Growth Rate (%). A score of 12% or higher indicates an attractive candidate for total return.
        </div>
        <p>Track elite compounding machines on our <a href="dividend-aristocrats.html">Dividend Aristocrats Radar</a>.</p>
        """
    ))

# 14. NUEVO: SPECIAL DIVIDENDS EXPLAINED
with open("special-dividends-explained.html", "w", encoding="utf-8") as f:
    f.write(generar_plantilla(
        titulo="Special Dividends vs. Regular Dividends: Investor Guide",
        subtitulo="Understanding non-recurring one-time payouts, asset sale distributions, and why annual yield calculations distort.",
        pestana_activa="special-dividends-explained.html",
        contenido_filas="",
        con_calculadora=False,
        fecha_iso=hoy.isoformat(),
        texto_seo="""
        <h2>What Is a Special Dividend?</h2>
        <p>A special dividend is a non-recurring payment made by a company to shareholders, separate from its regular quarterly or monthly dividend cycle. Special dividends frequently result from exceptional one-time profits, windfall cash balances, asset divestitures, or corporate restructuring.</p>
        
        <h2>The Yield Calculation Distortion (Trap Alert)</h2>
        <p>Many financial data aggregators annualize every declared distribution by multiplying it by 4 (quarterly) or 12 (monthly). If a company paying a $0.20 regular dividend suddenly declares a $5.00 special dividend, automated screeners may falsely project a massive 40% yield. Always verify the filing before executing capture trades.</p>
        <p>Check verified upcoming dividend schedules on our <a href="tomorrow.html">Tomorrow Ex-Dividend Page</a>.</p>
        """
    ))

# =========================================================
# SITEMAP.XML COMPLETO (16 URLs INDEXABLES)
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

print("Ecosistema completado al 100%: 16 páginas interconectadas + Calculadora + Sitemap dinámico.")
