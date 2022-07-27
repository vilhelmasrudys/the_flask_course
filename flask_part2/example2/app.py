from flask import Flask, render_template, request
import pickle
from os.path import exists
from forms import ContactForm


app = Flask(__name__)
data_path = "data.pkl"

app.config['SECRET_KEY'] = 'SECRET_KEY'

def get_data(path: str) -> list:
    if exists(path):
        with open(path, 'rb') as handle:
            data = pickle.load(handle)
    else:
        data = []
        save_data(path, data)
    return data


def save_data(path: str, data: list) -> None:
    with open(path, 'wb') as handle:
        pickle.dump(data, handle)


@app.route('/', methods=['GET', 'POST'])
def index():
    data = get_data(data_path)
    if request.method == 'POST':
        date = request.form['date']
        autorius = request.form['autorius']
        tekstas = request.form['tekstas']
        pavadinimas = request.form['pavadinimas']
        data.append({
            'data': date,
            'autorius': autorius,
            'pavadinimas': pavadinimas,
            'tekstas': tekstas,
            'status': 'published'
        })
        save_data(data_path, data)
    return render_template('index.html', data=data)


@app.route("/")
def home():
    data = get_data(data_path)
    return render_template("index.html", data=data)


@app.route('/<string:title>')
def article(title):
    data = get_data(data_path)
    return render_template('article.html', title=title, data=data)

@app.route('/add_article')
def add_article():
    data = get_data(data_path)
    return render_template('add_article.html')

@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    form = ContactForm()
    if form.validate_on_submit():
        return render_template('contact_success.html', form=form)
    return render_template('contact_us.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)