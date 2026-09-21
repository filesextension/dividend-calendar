import requests
import json
from datetime import datetime

fecha_hoy = datetime.today().strftime('%Y-%m-%d')
print(f"Buscando dividendos para la fecha: {fecha_hoy}...")

url = f"https://api.nasdaq.com/api/calendar/dividends?date={fecha_hoy}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": "https://www.nasdaq.com",
    "Referer": "https://www.nasdaq.com/"
}

response = requests.get(url, headers=headers, timeout=10)

if response.status_code == 200:
    data = response.json()
    filas = data.get("data", {}).get("calendar", {}).get("rows", [])
    if not filas:
        filas = []
    
    # Convertimos los datos a texto para incrustarlos directamente
    datos_json = json.dumps(filas)

    # Creamos el HTML completo con los datos ya integrados
    contenido_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Today's Ex-Dividend Stocks | Daily Dividend Calendar</title>
  <style>
    :root {{
      --bg: #0f172a;
      --card-bg: #1e293b;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --accent: #10b981;
      --border: #334155;
    }}
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background-color: var(--bg);
      color: var(--text);
      padding: 2rem 1rem;
    }}
    .container {{
      max-width: 1000px;
      margin: 0 auto;
    }}
    header {{
      margin-bottom: 2rem;
      text-align: center;
    }}
    h1 {{
      margin-bottom: 0.5rem;
      font-size: 2rem;
      color: #fff;
    }}
    p.subtitle {{
      color: var(--text-muted);
      margin-top: 0;
    }}
    .ad-slot {{
      background-color: var(--card-bg);
      border: 1px dashed var(--border);
      border-radius: 8px;
      padding: 1.5rem;
      text-align: center;
      color: var(--text-muted);
      font-size: 0.85rem;
      margin-bottom: 2rem;
    }}
    .search-box {{
      width: 100%;
      padding: 0.75rem 1rem;
      border-radius: 8px;
      border: 1px solid var(--border);
      background-color: var(--card-bg);
      color: var(--text);
      font-size: 1rem;
      box-sizing: border-box;
      margin-bottom: 1.5rem;
    }}
    .search-box:focus {{
      outline: 2px solid var(--accent);
    }}
    .table-container {{
      overflow-x: auto;
      background-color: var(--card-bg);
      border-radius: 8px;
      border: 1px solid var(--border);
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      text-align: left;
    }}
    th, td {{
      padding: 1rem;
      border-bottom: 1px solid var(--border);
    }}
    th {{
      background-color: #172033;
      color: var(--text-muted);
      font-weight: 600;
      font-size: 0.85rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    tr:hover {{
      background-color: #27354a;
    }}
    .ticker {{
      font-weight: 700;
      color: var(--accent);
    }}
    .yield {{
      font-weight: 600;
      color: #38bdf8;
    }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>Ex-Dividend Calendar Today</h1>
      <p class="subtitle" id="fecha-subtitulo">Companies going ex-dividend today ({fecha_hoy})</p>
    </header>

    <div class="ad-slot">
      [Espacio reservado para Google AdSense / Banner Broker Afiliado]
    </div>

    <input type="text" id="buscador" class="search-box" placeholder="Search by symbol or company name (e.g. Apple, AAPL)...">

    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Symbol</th>
            <th>Company Name</th>
            <th>Dividend Rate</th>
            <th>Annual Yield</th>
            <th>Payment Date</th>
          </tr>
        </thead>
        <tbody id="tabla-cuerpo"></tbody>
      </table>
    </div>
  </div>

  <script>
    // Los datos vienen incrustados directamente aqui
    const empresas = {datos_json};

    function mostrarTabla(lista) {{
      const cuerpo = document.getElementById('tabla-cuerpo');
      if (lista.length === 0) {{
        cuerpo.innerHTML = '<tr><td colspan="5" style="text-align:center;">No matching companies found.</td></tr>';
        return;
      }}
      cuerpo.innerHTML = lista.map(item => `
        <tr>
          <td class="ticker">${{item.symbol || '-'}}</td>
          <td>${{item.companyName || '-'}}</td>
          <td>${{item.dividend_Rate || '-'}}</td>
          <td class="yield">${{item.annual_yield || '-'}}</td>
          <td>${{item.payment_date || '-'}}</td>
        </tr>
      `).join('');
    }}

    mostrarTabla(empresas);

    document.getElementById('buscador').addEventListener('input', (e) => {{
      const termino = e.target.value.toLowerCase();
      const filtradas = empresas.filter(item => 
        (item.symbol && item.symbol.toLowerCase().includes(termino)) ||
        (item.companyName && item.companyName.toLowerCase().includes(termino))
      );
      mostrarTabla(filtradas);
    }});
  </script>
</body>
</html>"""

    # Sobrescribimos index.html con todo integrado
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(contenido_html)

    print(f"Exito: index.html generado con {len(filas)} empresas dentro.")
else:
    print(f"Error {response.status_code}")