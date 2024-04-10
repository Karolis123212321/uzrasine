from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Laikinas duomenų saugojimas
vartotojai = []
uzrasai_listas = []

# Pagrindinis route
@app.route('/')
def index():
    return render_template('index.html')

# Vartotojai route
@app.route('/vartotojai', methods=['GET', 'POST'])
def vartotojai():
    if request.method == 'POST':
        # Paimame duomenis iš formos ir pridėdami prie vartotojų sąrašo
        vartotojo_vardas = request.form.get('vardas')
        vartotojai.append(vartotojo_vardas)
        return redirect(url_for('vartotojai'))
    # Jei metodas yra GET, atvaizduojame vartotojų sąrašą
    return render_template('vartotojai.html', vartotojai=vartotojai)

# Užrašai route
@app.route('/uzrasai', methods=['GET', 'POST'])
def uzrasai():
    if request.method == 'POST':
        # Paimame užrašą iš formos ir pridedame prie užrašų sąrašo
        uzrasas = request.form.get('uzrasas')
        uzrasai_listas.append(uzrasas)
        return redirect(url_for('uzrasai'))
    # Jei metodas yra GET, atvaizduojame užrašų sąrašą
    return render_template('uzrasai.html', uzrasai=uzrasai_listas)

if __name__ == "__main__":
    app.run(debug=True)