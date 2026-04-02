import os
import re

template_dir = r'c:\Users\Rizwan\Documents\DBMS\Student_Management\student\templates'

# 1. Dark/Light Mode Theme Toggle code
theme_css = """
    /* Theme Toggle Overrides */
    body.light-mode .card { background-color: rgba(255, 255, 255, 0.85); color: #1a1a1a; border: 1px solid #ccc; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1); }
    body.light-mode h1 { color: #005580; text-shadow: none; }
    body.light-mode p { color: #444; text-shadow: none; }
    body.light-mode table { background-color: rgba(255, 255, 255, 0.9); color: #000; border: 1px solid #ddd; }
    body.light-mode th { background-color: rgba(0, 0, 0, 0.05); color: #000; text-shadow: none; }
    body.light-mode td { color: #000; }
    body.light-mode .modal-content { background-color: #ffffff !important; border: 1px solid #ddd; }
    body.light-mode .form-control, body.light-mode textarea { background-color: #fff; color: #000 !important; border: 1px solid #ccc; }
    body.light-mode .modal-body label { color: #111 !important; text-shadow: none; }
    body.light-mode .modal-title { color: #005580 !important; }
    body.light-mode .popup-content { background-color: rgba(255,255,255,0.9); color: #000; }
"""

theme_js = """
    function toggleTheme() {
      document.body.classList.toggle('light-mode');
      localStorage.setItem('theme', document.body.classList.contains('light-mode') ? 'light' : 'dark');
    }
    document.addEventListener("DOMContentLoaded", () => {
      if(localStorage.getItem('theme') === 'light') document.body.classList.add('light-mode');
    });
"""

theme_btn = """<button id="theme-toggle" class="btn btn-custom mb-3" style="position: fixed; top: 20px; right: 20px; z-index: 1000;" onclick="toggleTheme()">🌓 Toggle Mode</button>"""

# 2. Add Export CSV to home0.html and home2.html
csv_button = """      <a href="{% url 'export_csv' %}" class="btn btn-warning mb-3">📥 Export to CSV</a>\n"""

# 3. Chart in home0.html
chart_html = """
      <!-- Analytics Chart -->
      <div class="chart-container" style="position: relative; height:30vh; width:100%; max-width:600px; margin: 0 auto 30px auto;">
        <canvas id="courseChart"></canvas>
      </div>
      <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
      <script>
        document.addEventListener("DOMContentLoaded", function() {
          const courseDistribution = {{ course_distribution|safe }};
          const labels = courseDistribution.map(item => item.course);
          const data = courseDistribution.map(item => item.count);
          const ctx = document.getElementById('courseChart').getContext('2d');
          new Chart(ctx, {
            type: 'pie',
            data: { labels: labels, datasets: [{ data: data, backgroundColor: ['#00bfff', '#1e90ff', '#9370db', '#ff69b4', '#32cd32'], borderColor: '#fff', borderWidth: 1 }] },
            options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: document.body.classList.contains('light-mode') ? '#000' : '#fff' } } } }
          });
        });
      </script>
"""

# 4. ID Card in home.html
id_card_html = """
      <!-- ID Card Section -->
      <div id="id-card" style="margin-bottom:30px; width:100%; max-width:350px; margin-left:auto; margin-right:auto; padding:20px; border-radius:15px; background:linear-gradient(135deg, deepskyblue, dodgerblue); color:white; box-shadow: 0 4px 15px rgba(0,0,0,0.3); text-align:left;">
        <h2 style="margin-bottom:5px; text-align:center;">Student ID</h2>
        <hr style="border-top:1px solid rgba(255,255,255,0.5); margin:10px 0;">
        <p style="font-size:1.1rem; color:white; margin:5px 0;"><strong>Name:</strong> {{ student.name }}</p>
        <p style="font-size:1.1rem; color:white; margin:5px 0;"><strong>Course:</strong> {{ student.course }}</p>
        <p style="font-size:1.1rem; color:white; margin:5px 0;"><strong>Email:</strong> {{ student.email }}</p>
        <p style="font-size:1.1rem; color:white; margin:5px 0;"><strong>Age:</strong> {{ student.age }}</p>
      </div>
      <button onclick="window.print()" class="btn btn-warning mb-3" style="border-radius:25px;">🖨️ Print ID Card</button>
"""

# Loop through all files
for file in ['home0.html', 'home2.html', 'home.html', 'login.html', 'signup.html']:
    filepath = os.path.join(template_dir, file)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Inject CSS
    if '</style>' in content and 'Theme Toggle Overrides' not in content:
        content = content.replace('</style>', theme_css + '\n  </style>')

    # Inject JS
    if '<script>' in content and 'function toggleTheme' not in content:
        content = content.replace('<script>', '<script>\n' + theme_js)
    
    # Inject Theme Button
    if '<div class="center-container">' in content and 'id="theme-toggle"' not in content:
        content = content.replace('<div class="center-container">', theme_btn + '\n  <div class="center-container">')

    # Specifics
    if file in ['home0.html', 'home2.html']:
        if 'Export to CSV' not in content:
            # Place it right after Add student button
            btn_add = '<button type="button" class="btn btn-custom mb-3" data-toggle="modal" data-target="#addVehicleModal">'
            if btn_add in content:
                content = content.replace(btn_add, btn_add + '\n' + csv_button)
                
    if file == 'home0.html':
        if 'id="courseChart"' not in content:
            # Place chart before the table
            table_div = '<!-- Table Starts -->'
            if table_div in content:
                content = content.replace(table_div, chart_html + '\n      ' + table_div)

    if file == 'home.html':
        if 'id="id-card"' not in content:
            # Place ID card before the table
            table_div = '<!-- Table Starts -->'
            if table_div in content:
                content = content.replace(table_div, id_card_html + '\n      ' + table_div)


    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Processed {file}")
