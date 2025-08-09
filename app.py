from flask import Flask, render_template, request, flash, session, send_file, url_for
from PIL import Image, ImageDraw, ImageFont
import random, io
from scraper import fetch_case_details
from models import init_db, insert_log

app = Flask(__name__)
app.secret_key = 'your-secret-key'
init_db()

def generate_captcha_text():
    return str(random.randint(1000, 9999))

def generate_captcha_image(text):
    img = Image.new('RGB', (120, 40), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    d.text((10, 10), text, font=font, fill=(0, 0, 0))
    return img

@app.route('/captcha_image')
def captcha_image():
    text = session.get('captcha', generate_captcha_text())
    img = generate_captcha_image(text)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')
        case_type = request.form['case_type']
        case_number = request.form['case_number']
        filing_year = request.form['filing_year']

        if action == 'regenerate':
            session['captcha'] = generate_captcha_text()
            flash("CAPTCHA regenerated.", "info")
            return render_template('index.html', result=None)

        entered_captcha = request.form['captcha']
        if 'captcha' not in session or entered_captcha != session['captcha']:
            flash("Incorrect CAPTCHA. Please try again.", "error")
            session['captcha'] = generate_captcha_text()
            return render_template('index.html', result=None)

        try:
            result = fetch_case_details(case_type, case_number, filing_year)
            insert_log(case_type, case_number, filing_year, str(result))

            if not result:
                flash("The entered case details are not related to Cuddalore District.", "error")
                session['captcha'] = generate_captcha_text()
                return render_template('index.html', result=None)

            session['captcha'] = generate_captcha_text()
            return render_template('index.html', result=result)

        except:
            flash("An error occurred while fetching data.", "error")
            session['captcha'] = generate_captcha_text()
            return render_template('index.html', result=None)

    session['captcha'] = generate_captcha_text()
    return render_template('index.html', result=None)

if __name__ == '__main__':
    app.run(debug=True)
