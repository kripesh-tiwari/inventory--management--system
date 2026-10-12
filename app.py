
from flask import Flask, render_template, request, redirect, url_for, flash
from decimal import Decimal, InvalidOperation

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-before-deployment"


products = []
next_product_id = 1


@app.route("/")
def index():
    total_products = len(products)

    total_units = sum(
        product["quantity"] for product in products
    )

    total_value = sum(
        product["price"] * product["quantity"]
        for product in products
    )

    low_stock = sum(
        1 for product in products
        if product["quantity"] <= product["threshold"]
    )

    return render_template(
        "index.html",
        total_products=total_products,
        total_units=total_units,
        total_value=total_value,
        low_stock=low_stock,
        recent_products=products[-5:][::-1]
    )


# -------------------------
# View Products
# -------------------------

@app.route("/products")
def view_products():
    search = request.args.get("search", "").strip().lower()

    filtered_products = [
        product for product in products
        if search in product["name"].lower()
        or search in product["category"].lower()
    ]

    return render_template(
        "products.html",
        products=filtered_products,
        search=search
    )


# -------------------------
# Add Product
# -------------------------

@app.route("/products/add", methods=["GET", "POST"])
def add_product():
    global next_product_id

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        price_text = request.form.get("price", "").strip()
        quantity_text = request.form.get("quantity", "").strip()
        threshold_text = request.form.get("threshold", "5").strip()

        if not name or not category:
            flash(
                "Product name and category are required.",
                "error"
            )
            return render_template("add_product.html", product=None)

        try:
            price = Decimal(price_text)
            quantity = int(quantity_text)
            threshold = int(threshold_text)

            if not price.is_finite() or price < 0:
                raise ValueError

            if quantity < 0 or threshold < 0:
                raise ValueError

        except (ValueError, InvalidOperation):
            flash(
                "Enter a valid price, quantity and stock threshold.",
                "error"
            )
            return render_template("add_product.html", product=None)

        product = {
            "id": next_product_id,
            "name": name,
            "category": category,
            "price": price,
            "quantity": quantity,
            "threshold": threshold
        }

        products.append(product)
        next_product_id += 1

        flash("Product added successfully!", "success")

        return redirect(url_for("view_products"))

    return render_template("add_product.html", product=None)


# -------------------------
# Edit Product
# -------------------------

@app.route("/products/edit/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    product = next(
        (
            item for item in products
            if item["id"] == product_id
        ),
        None
    )

    if product is None:
        flash("Product not found.", "error")
        return redirect(url_for("view_products"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        price_text = request.form.get("price", "").strip()
        quantity_text = request.form.get("quantity", "").strip()
        threshold_text = request.form.get("threshold", "5").strip()

        if not name or not category:
            flash(
                "Product name and category are required.",
                "error"
            )
            return render_template(
                "add_product.html",
                product=product
            )

        try:
            price = Decimal(price_text)
            quantity = int(quantity_text)
            threshold = int(threshold_text)

            if not price.is_finite() or price < 0:
                raise ValueError

            if quantity < 0 or threshold < 0:
                raise ValueError

        except (ValueError, InvalidOperation):
            flash(
                "Enter a valid price, quantity and stock threshold.",
                "error"
            )
            return render_template(
                "add_product.html",
                product=product
            )

        product.update({
            "name": name,
            "category": category,
            "price": price,
            "quantity": quantity,
            "threshold": threshold
        })

        flash("Product updated successfully!", "success")

        return redirect(url_for("view_products"))

    return render_template("add_product.html", product=product)


# -------------------------
# Delete Product
# -------------------------

@app.route("/products/delete/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    global products

    original_count = len(products)

    products = [
        product for product in products
        if product["id"] != product_id
    ]

    if len(products) < original_count:
        flash("Product deleted successfully!", "success")
    else:
        flash("Product not found.", "error")

    return redirect(url_for("view_products"))




if __name__ == "__main__":
    app.run(debug=True)
