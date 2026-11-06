# What if…? 🌱 — The First LUMEN LAB Model

An interactive **LTV / CAC** model designed to explore the unit economics of a hypothetical subscription business. Sliders adjust CAC, monthly revenue, gross margin, and customer churn. The result is the LTV/CAC ratio, churn-adjusted payback period, and a 60-month projection chart.

## Target Audience

For users who simply open the link to the published model, **neither Python nor Obsidian is required**. The visitor interacts with the application directly in their browser. Data between visitors is strictly isolated (each user works with their own set of sliders in a private session). State saving between visits is implemented via CSV export, rather than through user accounts or server-side storage.

## Running Locally (For the Creator)

1. Install Python 3.10+.
2. Open a terminal in the project folder.
3. Execute:

python -m pip install -r requirements.txt
python -m streamlit run app.py

4. The application will open in your browser (usually http://localhost:8501).

To stop the application, press `Ctrl+C` in the terminal.

## Sharing with Others (No Python Required)

1. Create a GitHub repository and add the `app.py`, `model.py`, `requirements.txt`, and `.streamlit/config.toml` files.
2. Log in to [Streamlit Community Cloud](https://share.streamlit.io/) and create an app from this repository, specifying `app.py` as the main file path.
3. Upon successful deployment, the service will generate a public link that can be shared with others.

**Note:** This archive is **not hosted on the internet**. Until the app is deployed to a hosting service, others will not be able to access it via a public link. Free hosting tiers may enforce resource limits and sleep modes.

## Integration with Obsidian

Optionally, you can save the entire project folder inside your existing `LUMEN_LAB` directory (no new top-level folders are needed). Within an Obsidian card, you can document the logic, assumptions, versioning, and the link to the published model. The model and the note serve distinct roles: **Python calculates, LUMEN stores knowledge and context**.

## Important Mathematical Considerations

This is an **educational model**, not a financial forecast or tax advice.

- `Monthly Contribution = Monthly Revenue × Gross Margin`
- `LTV = Monthly Contribution / Monthly Churn (as a decimal)` — assuming constant churn, constant margin, and no discounting.
- `LTV/CAC = LTV / CAC`.
- `Cumulative Contribution over n months = Monthly Contribution × [1 − (1 − churn)^n] / churn`.
- `Plotted on chart = Cumulative Contribution − CAC`.
- Chart starting point at month 0: `−CAC`.
- `LTV` evaluates an infinite horizon; the chart displays only the first **60 months**.
- The payback period accounts for monthly customer churn, meaning it may exceed `CAC / Monthly Contribution`.
- The model **does not include** general operational expenses (OPEX), taxes, the time value of money, customer heterogeneity, or dynamic parameter changes. The post-CAC result is **not net profit**.
- The commonly cited **3:1 threshold is not a universal benchmark for a safe business** and does not account for jurisdiction-specific legislation.

### Files

- `app.py` — Streamlit web interface.
- `model.py` — Calculation logic, separated from UI.
- `requirements.txt` — Project dependencies.
- `.streamlit/config.toml` — Visual theme configuration.
- `test_model.py` — Basic automated formula checks (run via `python -m unittest test_model.py`).

**Pole-pole. One model, one step at a time.** 🌱


---
# What if…? 🌱 — перша модель LUMEN LAB

Інтерактивна модель **LTV / CAC** для дослідження економіки умовного підписного бізнесу. Бігунки змінюють CAC, місячну виручку, валову маржу та відтік клієнтів. Результат — співвідношення LTV/CAC, окупність із урахуванням відтоку та графік на 60 місяців.

## Для кого?

Для людини, яка просто відкриє посилання на опубліковану модель, **Python та Obsidian не потрібні**. Відвідувач бачить застосунок у браузері. Дані різних відвідувачів не змішуються (кожен працює з власним набором бігунків у своїй сесії). Збереження між візитами реалізовано через експорт CSV, а не через акаунти чи серверне сховище.

## Запустити локально (для авторки)

1. Установити Python 3.10+.
2. Відкрити термінал у папці проєкту.
3. Виконати:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

4. Застосунок відкриється в браузері (зазвичай `http://localhost:8501`).

Для завершення запуску — `Ctrl+C` у терміналі.

## Поділитися з іншими без установлення Python

1. Створити репозиторій у GitHub та додати файли `app.py`, `model.py`, `requirements.txt` та `.streamlit/config.toml`.
2. Увійти до [Streamlit Community Cloud](https://share.streamlit.io/) і створити застосунок із цього репозиторію, вказавши `app.py` як головний файл.
3. Після успішного розгортання сервіс видасть публічне посилання — ним можна поділитися.

**Важливо:** цей архів **не розгорнуто в інтернеті**. Доки застосунок не розміщено на хостингу, інші люди не зможуть відкрити його за публічним посиланням. На безкоштовному хостингу можуть діяти обмеження ресурсів і режим сну.

## Як пов'язати з Obsidian

За бажанням збережи всю папку проєкту в чинному `LUMEN_LAB` (не потрібно нових верхньорівневих папок). У картці Obsidian можна описати задум, припущення, версію та посилання на опубліковану модель. Модель і нотатка мають різні ролі: **Python рахує, LUMEN зберігає знання і контекст**.

## Важливі математичні уточнення

Це **навчальна модель**, не фінансовий прогноз і не податкова консультація.

- `внесок за місяць = місячна виручка × валова маржа`
- `LTV = внесок за місяць / місячний churn (у частках)` — за умови постійного відтоку, постійної маржі, без дисконтування.
- `LTV/CAC = LTV / CAC`.
- `Накопичений внесок за n місяців = внесок_на_місяць × [1 − (1 − churn)^n] / churn`.
- `На графіку = накопичений внесок − CAC`.
- Початкова точка графіка в місяці 0: `−CAC`.
- `LTV` оцінює необмежений горизонт; графік показує лише перші **60 місяців**.
- Окупність враховує втрату клієнтів щомісяця, тож може бути більшою за `CAC / внесок за місяць`.
- Модель **не включає** загальні операційні витрати, податки, вартість грошей у часі, неоднорідність клієнтів та зміни параметрів. Результат після CAC — **не чистий прибуток**.
- Поширений поріг **3:1 не є універсальною межею безпечного бізнесу** й не враховує законодавства різних країн.

### Файли

- `app.py` — вебінтерфейс Streamlit.
- `model.py` — обчислення, окремі від дизайну.
- `requirements.txt` — залежності.
- `.streamlit/config.toml` — візуальна тема.
- `test_model.py` — невеличкі автоматичні перевірки формул (працюють через `python -m unittest test_model.py`).

**Pole-pole. Одна модель, один крок.** 🌱
