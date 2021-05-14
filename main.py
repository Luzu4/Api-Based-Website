from flask import Flask, render_template, request, redirect, url_for, flash
import requests

# barcode_product = 4890008100309
# response = requests.get(url=f'https://world.openfoodfacts.org/api/v0/product/{barcode_product}.json').json()
# print(response['product']['nutriments']['sugars'])


app = Flask(__name__)
app.secret_key = 'Yo'

@app.route("/", methods=['GET', 'POST'])
def home():
    try:
        if len(request.args["barcode_1"]) > 0 and len(request.args["barcode_2"]) > 0:
            product_1 = requests.get(
                url=f'https://world.openfoodfacts.org/api/v0/product/{request.args["barcode_1"]}.json').json()
            product_2 = requests.get(
                url=f'https://world.openfoodfacts.org/api/v0/product/{request.args["barcode_2"]}.json').json()
            return render_template("index.html", product_1=product_1, product_2=product_2)
        elif len(request.args["barcode_1"]) > 0:
            flash('Barcode Product 2 is empty', 'error')
            product_1 = requests.get(
                url=f'https://world.openfoodfacts.org/api/v0/product/{request.args["barcode_1"]}.json').json()
            return render_template("index.html", product_1=product_1)
        elif len(request.args["barcode_2"]) > 0:
            flash('Barcode Product 1 is empty', 'error')
            product_2 = requests.get(
                url=f'https://world.openfoodfacts.org/api/v0/product/{request.args["barcode_2"]}.json').json()
            return render_template("index.html", product_1=product_2)
        else:
            flash('Enter Barcodes', 'error')
            return render_template("index.html")
    except KeyError:
        return render_template("index.html")


@app.route('/compare', methods=["POST"])
def compare_products():
    barcode_1 = request.form['product_1_barcode']
    barcode_2 = request.form['product_2_barcode']
    return redirect(url_for('home', barcode_1=barcode_1, barcode_2=barcode_2))

if __name__ == '__main__':
    app.run(debug=True)