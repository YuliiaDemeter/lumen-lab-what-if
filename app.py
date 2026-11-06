"""What if...? — інтерактивна модель LTV/CAC для дослідження сценаріїв."""
import streamlit as st
import plotly.graph_objects as go
from model import Inputs, calculate

st.set_page_config(
    page_title='What if…? — модель LTV/CAC',
    page_icon='🌱',
    layout='wide',
    initial_sidebar_state='collapsed',
)

st.markdown('''
<style>
  .stApp { background: #0e1824; color: #edf4f2; }
  .block-container { max-width: 1120px; padding-top: 2rem; padding-bottom: 4rem; }
  div[data-testid="stHeader"] { background: transparent; }
  .hero { border: 1px solid #294a50; padding: 28px 32px; border-radius: 23px;
          background: linear-gradient(125deg,#173441 0%,#18323a 48%,#253b37 100%);
          margin-bottom: 25px; box-shadow: 0 15px 45px rgba(0,0,0,.12); }
  .eyebrow { color: #a6d4c5; font-size: 0.78rem; letter-spacing: 0.16em; font-weight: 750; }
  .hero h1 { color: #fffaf0; font-size: clamp(2rem,4vw,3.6rem); margin: 7px 0; line-height: 1.12; }
  .hero p { color: #d3e6df; margin: 0; font-size: 1rem; max-width: 760px; }
  .section-label { font-size: 0.8rem; letter-spacing: 0.13em; color: #9dc7bd;
                   font-weight: 750; margin: 0.5rem 0 0.8rem; }
  .small-note { color:#a9c0bf; font-size:0.9rem; line-height:1.6; }
  .callout { background: #172b35; border:1px solid #31565b; border-radius:16px;
             padding: 16px 20px; margin-top: 10px; }
  .callout strong { color: #f6dfb4; }
  div[data-testid="stMetric"] { background:#192e38; border:1px solid #31515a;
                               border-radius:15px; padding:17px 18px; min-height:129px; }
  div[data-testid="stMetricLabel"] { color:#bcd4ce; }
  div[data-testid="stMetricValue"] { color:#fff9e8; }
  div[data-testid="stSlider"] { padding: 5px 0 14px; }
  div[data-testid="stSlider"] [role="slider"] { background:#e6b971; }
  .stButton button { background:#24443f; color:#f4f7f5; border:1px solid #729f91; }
  .stButton button:hover { background:#30594f; color:white; border-color:#b7d9ca; }
  .footer { color:#91b5ad; font-size:0.86rem; margin-top: 18px; }
  @media (max-width: 700px) { .hero { padding:22px 21px; } }
</style>
''', unsafe_allow_html=True)

st.markdown('''
<div class="hero">
  <div class="eyebrow">LUMEN LAB · ІНТЕРАКТИВНЕ ДОСЛІДЖЕННЯ</div>
  <h1>What if…? <span style="color:#ebc98e">🌱</span></h1>
  <p>Рухай бігунки. Спостерігай, як змінюються економіка клієнта,
  окупність і п’ятирічна траєкторія. Це простір для запитань, а не обіцянка майбутнього.</p>
</div>
''', unsafe_allow_html=True)

left, right = st.columns([0.92, 1.3], gap='large')
with left:
    st.markdown('<div class="section-label">01 · ЗМІНЮЙ УМОВИ</div>', unsafe_allow_html=True)
    cac = st.slider('CAC · вартість залучення одного клієнта (£)', 50, 2000, 250, 25,
                    help='Скільки коштує залучити одного нового клієнта. Витрачаємо одноразово на початку.')
    monthly_revenue = st.slider('Середня місячна виручка від клієнта (£)', 10, 500, 50, 5,
                                help='Скільки в середньому клієнт сплачує за місяць, доки активний.')
    gross_margin = st.slider('Валова маржа (%)', 10, 95, 70, 5,
                              help='Частка виручки, що залишається після прямих витрат на послугу. Не є чистою маржею.')
    churn = st.slider('Відтік клієнтів за місяць (%)', 0.5, 15.0, 4.0, 0.5,
                      help='Частка активних клієнтів, які припиняють користуватися послугою щомісяця.')
    if st.button('↺ Повернути початкові значення', use_container_width=True):
        # Streamlit оновить сторінку й підставить стандартні значення через session state.
        st.session_state.clear()
        st.rerun()
    st.markdown('''<div class="small-note">Модель для <b>умовного підписного бізнесу</b>.
        Валова маржа й відтік вважаються незмінними, новий клієнт приходить у місяці 0.
        Вибрані значення — гіпотези для перевірки.</div>''', unsafe_allow_html=True)

result = calculate(Inputs(cac, monthly_revenue, gross_margin, churn))
with right:
    st.markdown('<div class="section-label">02 · ЩО ЗМІНИЛОСЯ?</div>', unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    m1.metric('LTV / CAC', f'{result.ltv_cac:.2f} : 1')
    m2.metric('LTV · очікувана валова цінність', f'£{result.ltv:,.0f}')
    m3, m4 = st.columns(2)
    m3.metric('Окупність з урахуванням відтоку',
              f'{result.payback_month} міс.' if result.payback_month is not None else 'Не досягається')
    m4.metric('За 5 років, після CAC*', f'£{result.net_60m:,.0f}')

    if result.ltv_cac >= 3:
        st.markdown('''<div class="callout"><strong>Орієнтир 3:1 досягнуто.</strong>
        Але це не означає, що весь бізнес прибутковий: інші витрати та податки тут не враховано.</div>''',
        unsafe_allow_html=True)
    else:
        st.markdown('''<div class="callout"><strong>Нижче поширеного орієнтира 3:1.</strong>
        Це не автоматично означає збиток. Потрібно дивитися на тип бізнесу, витрати та часовий горизонт.</div>''',
        unsafe_allow_html=True)

st.markdown('<div class="section-label">03 · П’ЯТЬ РОКІВ ОДНОГО КЛІЄНТА</div>', unsafe_allow_html=True)
chart = go.Figure()
chart.add_trace(go.Scatter(
    x=list(result.months), y=list(result.cumulative_after_cac),
    mode='lines', name='Очікуваний накопичений внесок після CAC',
    line=dict(color='#77d6bf', width=4),
    fill='tozeroy', fillcolor='rgba(119,214,191,.11)',
    hovertemplate='Місяць %{x}<br>Після CAC: £%{y:,.2f}<extra></extra>',
))
chart.add_hline(y=0, line_color='#eac68c', line_dash='dot',
                annotation_text='Нульовий рівень', annotation_font_color='#eac68c')
if result.payback_month is not None and result.payback_month <= 60:
    chart.add_vline(x=result.payback_month, line_dash='dash', line_color='#c4ddcd',
                    annotation_text=f'Окупність · {result.payback_month} міс.',
                    annotation_font_color='#c4ddcd', annotation_position='top right')
chart.update_layout(
    template='plotly_dark', height=360,
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=12, r=12, t=34, b=18),
    xaxis=dict(title='Місяці від залучення клієнта', showgrid=False, dtick=6, range=[0, 60]),
    yaxis=dict(title='£ / клієнт', gridcolor='rgba(200,220,210,.12)', zeroline=False),
    font=dict(color='#d7e8e2'), showlegend=False,
)
st.plotly_chart(chart, use_container_width=True, config={'displayModeBar': False})

st.markdown('''<div class="callout">
<strong>Як читати графік.</strong> На старті ми витрачаємо CAC, тому лінія починається нижче нуля.
Потім щомісячний очікуваний валовий прибуток накопичується, але кількість активних клієнтів
зменшується через відтік. Перетин нуля — окупність витрат на залучення.
</div>''', unsafe_allow_html=True)

with st.expander('Що саме рахуємо? Формули й обмеження', expanded=False):
    st.markdown(r'''
**Для однієї умовної когорти з одного клієнта:**

- Внесок за місяць = місячна виручка × валова маржа.
- Очікуваний LTV = внесок за місяць ÷ частка місячного відтоку.
- LTV/CAC = очікуваний LTV ÷ вартість залучення.
- Очікуваний внесок за **N** місяців = сума щомісячних внесків із урахуванням відтоку.
- П’ятирічний результат на графіку = внесок за 60 місяців − CAC.

**Межі:** LTV — довгострокова теоретична оцінка; він може охоплювати більше ніж 5 років.
Модель не враховує загальні операційні витрати, податки, інфляцію, вартість капіталу,
зміну маржі, знижки, повторне залучення та невизначеність прогнозу.
Показник **3:1** — практичний орієнтир, не міжнародний норматив безпечного прибутку.

**Важливо:** `£` тут — умовна валюта для прикладу; зміна на іншу валюту
не впливає на формули, якщо всі грошові значення наведено в одній валюті.
    ''')

with st.expander('Як зберегти свій сценарій', expanded=False):
    st.write('Натисни кнопку нижче, щоб отримати CSV із поточними припущеннями та результатами. Файл залишиться у тебе.')
    import csv
    import io
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(['Показник', 'Значення'])
    for row in [
        ('CAC', cac), ('Місячна виручка', monthly_revenue),
        ('Валова маржа %', gross_margin), ('Відтік %/міс', churn),
        ('LTV', round(result.ltv, 2)), ('LTV/CAC', round(result.ltv_cac, 3)),
        ('Окупність, міс', result.payback_month or 'Недосяжна'),
        ('Внесок 60 міс після CAC до інших витрат і податків', round(result.net_60m, 2)),
    ]:
        writer.writerow(row)
    st.download_button('⬇ Завантажити сценарій (.csv)',
                       data='\ufeff' + buffer.getvalue(),
                       file_name='what_if_ltv_cac_scenario.csv',
                       mime='text/csv', use_container_width=True)

st.markdown('''<div class="footer">LUMEN LAB · What if…? · Навчальний сценарний інструмент.
Жодних особистих даних застосунок не запитує і не зберігає на сервері. 🌱</div>''',
unsafe_allow_html=True)
