import datetime
import html
import requests

# 1. Obtener la fecha de hoy
hoy = datetime.date.today()
fecha_str = hoy.strftime("%Y-%m-%d")
fecha_legible = hoy.strftime("%B %d, %Y")

url = f"https://api.nasdaq.com/api/calendar/dividends?date={fecha_str}"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": "https://www.nasdaq.com",
    "Referer": "https://www.nasdaq.com/"
}

print(f"Descargando datos de dividendos para: {fecha_str}")
filas_html = ""

try:
    response = requests.get(url, headers=headers, timeout=15)
    data = response.json()
    rows = data.get("data", {}).get("calendar", {}).get("rows", [])
    
    if not rows:
        filas_html = "<tr><td colspan='6' style='text-align:center; padding: 2rem;'>No ex-dividend records found for today or market is closed.</td></tr>"
    else:
        for r in rows:
            ticker = html.escape(str(r.get("symbol", "N/A")))
            name = html.escape(str(r.get("companyName", "N/A")))
            amount = html.escape(str(r.get("dividend_Rate", "N/A")))
            yield_pct = html.escape(str(r.get("annual_Yield", "N/A")))
            ex_date = html.escape(str(r.get("dividend_Ex_Date", "N/A")))
            pay_date = html.escape(str(r.get("payment_Date", "N/A")))
            
            filas_html += f"""
            <tr>
                <td><span class="badge">{ticker}</span></td>
                <td>{name}</td>
                <td class="num font-bold text-accent">{amount}</td>
                <td class="num">{yield_pct}%</td>
                <td>{ex_date}</td>
                <td>{pay_date}</td>
            </tr>
            """
except Exception as e:
    print(f"Error al descargar datos: {e}")
    filas_html = f"<tr><td colspan='6' style='text-align:center; padding: 2rem; color: #f85149;'>Error fetching live market feed. Please check back shortly.</td></tr>"

# Plantilla HTML con diseño profesional, enlaces y bloques de contenido
contenido_index = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Daily Ex-Dividend Calendar & High-Yield Stock Screener - DividendRadar</title>
  <meta name="description" content="Free daily U.S. stock market ex-dividend calendar. Track dividend yield, payment dates, and declared cash payouts across NYSE and NASDAQ securities.">
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
      margin-left: 1.5rem;
      font-size: 0.95rem;
    }}
    nav a:hover, nav a.active {{
      color: var(--primary);
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
    .badge {{
      background-color: #21262d;
      border: 1px solid var(--border);
      color: var(--primary);
      padding: 0.2rem 0.5rem;
      border-radius: 4px;
      font-weight: bold;
      font-size: 0.85rem;
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
      <a href="index.html" class="active">Calendar</a>
      <a href="guide.html">Dividend Guide</a>
      <a href="about.html">About</a>
    </nav>
  </header>

  <main>
    <div class="hero">
      <h1>Daily Ex-Dividend Calendar</h1>
      <p>Real-time corporate payout declarations, annualized yields, and cutoff schedules updated for <strong>{fecha_legible}</strong>.</p>
    </div>

    <div class="search-box">
      <input type="text" id="filtro" placeholder="Search by ticker symbol or company name..." onkeyup="filtrarTabla()">
      <span style="font-size: 0.85rem; color: var(--text-muted);">Source: Nasdaq Market Data Feed</span>
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
          {filas_html}
        </tbody>
      </table>
    </div>

    <section class="editorial">
      <h2>How to Use This Daily Calendar</h2>
      <p>The ex-dividend date determines who receives an upcoming corporate distribution. If you purchase shares on or after this cutoff date, you will not receive the current declared payout. To qualify, positions must be initiated and settled prior to market open on the designated ex-date.</p>
      
      <h2>Key Investment Takeaways</h2>
      <p>While high yields are attractive, always review payout sustainability, debt leverage, and operational cash flows before establishing long-term positions. Learn more about advanced allocation strategies in our <a href="guide.html" style="color: var(--primary);">Comprehensive Dividend Guide</a>.</p>
    </section>
  </main>

  <footer>
    <p>&copy; 2026 DividendRadar. Financial data provided for research purposes only.</p>
    <p>
      <a href="index.html">Home</a> |
      <a href="about.html">About & Methodology</a> |
      <a href="guide.html">Dividend Strategy Guide</a> |
      <a href="terms.html">Terms of Service</a> |
      <a href="privacy.html">Privacy Policy</a>
    </p>
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

with open("index.html", "w", encoding="utf-8") as f:
    f.write(contenido_index)

print("index.html generado exitosamente con nuevo diseño y enlaces de navegacion.")
