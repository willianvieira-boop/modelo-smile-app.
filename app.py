<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Smile - Glenda Rodrigues Odontologia</title>
    <style>
        /* Paleta Smile */
        :root {
            --bronze: #CD7F32;
            --silver: #C0C0C0;
            --gold: #FFD700;
            --elite: #FF4500;
            --master: #8A2BE2;
            --fundo: #1A1A2E;
            --cards: #16213E;
            --texto: #FFFFFF;
        }
        body {
            font-family: Arial, sans-serif;
            background-color: var(--fundo);
            color: var(--texto);
            margin: 0;
            padding: 0;
            transition: transition: all 0.3s;
        }
        .dark-mode {
            background-color: #000000;
            color: #FFFFFF;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .card {
            background-color: var(--cards);
            padding: 20px;
            margin: 10px 0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .btn {
            background-color: var(--gold);
            color: var(--fundo);
            border: none;
            padding: 10px 20px;
            cursor: pointer;
            border-radius: 4px;
            margin: 5px;
        }
        .btn:hover {
            opacity: 0.8;
        }
        input, select {
            padding: 10px;
            margin: 5px 0;
            width: 100%;
            box-sizing: border-box;
        }
        canvas {
            max-width: 100%;
            height: auto;
        }
        .hidden {
            display: none;
        }
        .nav {
            display: flex;
            justify-content: space-around;
            background-color: var(--cards);
            padding: 10px;
            position: sticky;
            top: 0;
        }
        .nav a {
            color: var(--texto);
            text-decoration: none;
            padding: 10px;
        }
        .nav a:hover {
            background-color: var(--gold);
        }
        @media (max-width: 768px) {
            .nav {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div id="login" class="container">
        <h1>Login - Dashboard Smile</h1>
        <input type="text" id="username" placeholder="Usuário">
        <input type="password" id="password" placeholder="Senha">
        <button class="btn" onclick="login()">Entrar</button>
    </div>
    <div id="main" class="hidden">
        <nav class="nav">
            <a href="#" onclick="showScreen('dashboard')">Dashboard Executivo</a>
            <a href="#" onclick="showScreen('individual')">Painel Individual</a>
            <a href="#" onclick="showScreen('lancamento')">Lançamento</a>
            <a href="#" onclick="showScreen('metas')">Metas & Performance</a>
            <a href="#" onclick="showScreen('equipe')">Minha Equipe</a>
            <a href="#" onclick="showScreen('rotinas')">Rotinas</a>
            <a href="#" onclick="showScreen('medalhas')">Cálculo Medalhas</a>
            <a href="#" onclick="showScreen('relatorios')">Relatórios</a>
            <a href="#" onclick="showScreen('config')">Configurações</a>
            <button class="btn" onclick="toggleMode()">Dark/Light</button>
        </nav>
        <div id="dashboard" class="container screen">
            <h1>Dashboard Executivo</h1>
            <div class="card">
                <h2>KPIs</h2>
                <canvas id="kpiChart" width="400" height="200"></canvas>
            </div>
            <div class="card">
                <h2>Ranking</h2>
                <ul id="ranking"></ul>
            </div>
        </div>
        <div id="individual" class="container screen hidden">
            <h1>Painel Individual</h1>
            <select id="colaboradorSelect"></select>
            <div class="card" id="individualData"></div>
        </div>
        <div id="lancamento" class="container screen hidden">
            <h1>Lançamento de Resultados</h1>
            <form id="resultForm">
                <select id="colaborador" required>
                    <option value="Ana Clara">Ana Clara</option>
                    <option value="João Silva">João Silva</option>
                    <option value="Maria Santos">Maria Santos</option>
                    <option value="Pedro Costa">Pedro Costa</option>
                </select>
                <input type="number" id="semana" placeholder="Semana" required>
                <input type="number" id="realizado" placeholder="Realizado" required>
                <button type="submit" class="btn">Salvar</button>
            </form>
        </div>
        <div id="metas" class="container screen hidden">
            <h1>Metas & Performance</h1>
            <table id="metasTable"></table>
        </div>
        <div id="equipe" class="container screen hidden">
            <h1>Minha Equipe</h1>
            <div id="equipeCards"></div>
        </div>
        <div id="rotinas" class="container screen hidden">
            <h1>Rotinas & Comportamento</h1>
            <ul id="checklist"></ul>
        </div>
        <div id="medalhas" class="container screen hidden">
            <h1>Cálculo de Medalhas</h1>
            <div id="medalhasDisplay"></div>
        </div>
        <div id="relatorios" class="container screen hidden">
            <h1>Relatórios</h1>
            <button class="btn" onclick="exportJSON()">Exportar JSON</button>
            <button class="btn" onclick="exportCSV()">Exportar CSV</button>
        </div>
        <div id="config" class="container screen hidden">
            <h1>Configurações</h1>
            <button class="btn" onclick="backup()">Backup</button>
            <input type="file" id="restoreFile" accept=".json">
            <button class="btn" onclick="restore()">Restore</button>
            <button class="btn" onclick="clearData()">Limpar Dados</button>
        </div>
    </div>
    <script>
        // Dados iniciais
        let data = JSON.parse(localStorage.getItem('smileData')) || {
            colaboradores: {
                'Ana Clara': { meta: 25, tipo: 'comparecimentos', resultados: {1: 20, 2: 28} },
                'João Silva': { meta: 9000, tipo: 'R$', resultados: {1: 8500, 2: 9500} },
                'Maria Santos': { meta: 15000, tipo: 'R$', resultados: {1: 14000, 2: 16000} },
                'Pedro Costa': { meta: 10, tipo: 'indicações', resultados: {1: 8, 2: 12} }
            },
            periodo: 'Abril 2026'
        };
        
        function saveData() {
            localStorage.setItem('smileData', JSON.stringify(data));
        }
        
        function login() {
            // Simples login
            document.getElementById('login').classList.add('hidden');
            document.getElementById('main').classList.remove('hidden');
            loadDashboard();
        }
        
        function showScreen(screen) {
            document.querySelectorAll('.screen').forEach(s => s.classList.add('hidden'));
            document.getElementById(screen).classList.remove('hidden');
        }
        
        function toggleMode() {
            document.body.classList.toggle('dark-mode');
        }
        
        function calculateMedalhas(realizado, meta) {
            let perc = (realizado / meta) * 100;
            if (perc < 90) return 0;
            if (perc < 100) return 1;
            if (perc < 110) return 1;
            if (perc < 120) return 2;
            return 3;
        }
        
        function calculateBrasao(medalhas) {
            if (medalhas <= 3) return 'Bronze';
            if (medalhas <= 7) return 'Silver';
            if (medalhas <= 11) return 'Gold';
            if (medalhas <= 14) return 'Elite';
            return 'Master';
        }
        
        function loadDashboard() {
            // Gráfico simples com Canvas
            let canvas = document.getElementById('kpiChart');
            let ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            // Exemplo de gráfico de barras
            let colaboradores = Object.keys(data.colaboradores);
            colaboradores.forEach((col, i) => {
                let total = Object.values(data.colaboradores[col].resultados).reduce((a,b)=>a+b,0);
                let meta = data.colaboradores[col].meta * Object.keys(data.colaboradores[col].resultados).length;
                let perc = (total / meta) * 100;
                ctx.fillStyle = 'var(--gold)';
                ctx.fillRect(i*50, canvas.height - (perc*2), 40, perc*2);
            });
            
            // Ranking
            let ranking = colaboradores.sort((a,b) => {
                let aPerc = (Object.values(data.colaboradores[a].resultados).reduce((s,v)=>s+v,0) / (data.colaboradores[a].meta * Object.keys(data.colaboradores[a].resultados).length)) * 100;
                let bPerc = (Object.values(data.colaboradores[b].resultados).reduce((s,v)=>s+v,0) / (data.colaboradores[b].meta * Object.keys(data.colaboradores[b].resultados).length)) * 100;
                return bPerc - aPerc;
            });
            document.getElementById('ranking').innerHTML = ranking.map(col => `<li>${col}</li>`).join('');
        }
        
        document.getElementById('resultForm').addEventListener('submit', function(e) {
            e.preventDefault();
            let col = document.getElementById('colaborador').value;
            let semana = parseInt(document.getElementById('semana').value);
            let realizado = parseFloat(document.getElementById('realizado').value);
            data.colaboradores[col].resultados[semana] = realizado;
            saveData();
            loadDashboard();
            alert('Resultado salvo!');
        });
        
        function exportJSON() {
            let blob = new Blob([JSON.stringify(data)], {type: 'application/json'});
            let url = URL.createObjectURL(blob);
            let a = document.createElement('a');
            a.href = url;
            a.download = 'backup.json';
            a.click();
        }
        
        function exportCSV() {
            let csv = 'Colaborador,Semana,Realizado\n';
            Object.keys(data.colaboradores).forEach(col => {
                Object.keys(data.colaboradores[col].resultados).forEach(sem => {
                    csv += `${col},${sem},${data.colaboradores[col].resultados[sem]}\n`;
                });
            });
            let blob = new Blob([csv], {type: 'text/csv'});
            let url = URL.createObjectURL(blob);
            let a = document.createElement('a');
            a.href = url;
            a.download = 'relatorio.csv';
            a.click();
        }
        
        function backup() {
            exportJSON();
        }
        
        function restore() {
            let file = document.getElementById('restoreFile').files[0];
            if (file) {
                let reader = new FileReader();
                reader.onload = function(e) {
                    data = JSON.parse(e.target.result);
                    saveData();
                    loadDashboard();
                    alert('Dados restaurados!');
                };
                reader.readAsText(file);
            }
        }
        
        function clearData() {
            if (confirm('Tem certeza que deseja limpar todos os dados?')) {
                localStorage.removeItem('smileData');
                data = { colaboradores: {}, periodo: 'Abril 2026' };
                saveData();
                loadDashboard();
            }
        }
        
        // Inicializar
        loadDashboard();
    </script>
</body>
</html>
