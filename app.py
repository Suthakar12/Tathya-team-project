from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load the CSV file
csv_path = "PROTEIN/pro.csv"  # Make sure the CSV is in the same directory as app.py
data = pd.read_csv(csv_path)

# Home Route
@app.route('/')
def home():
    return render_template('main.html')

# Compare Route
@app.route('/compare')
def compare():
    return render_template('compare.html')

# pBLAST Route
@app.route('/blast')
def blast():
    return render_template('blast.html')

# About Route
@app.route('/about')
def about():
    return render_template('about.html')

# Search Route
@app.route('/search', methods=["POST"])
def search():
    # Get the search query from the form
    query = request.form.get("query")
    
    # Search the CSV data for the query (case-insensitive)
    results = data[data["Strain"].str.contains(query, case=False, na=False)]
    
    # Convert results to a list of dictionaries
    results_list = results.to_dict(orient="records")
    
    # Return the results as JSON
    return jsonify(results_list)

# Compare Proteins Route
@app.route('/compare_proteins', methods=["POST"])
def compare_proteins():
    # Get the two protein/strain names from the form
    protein1 = request.form.get("protein1")
    protein2 = request.form.get("protein2")
    
    # Search the CSV data for the two proteins/strains
    result1 = data[data["Strain"].str.contains(protein1, case=False, na=False)]
    result2 = data[data["Strain"].str.contains(protein2, case=False, na=False)]
    
    # Convert results to a list of dictionaries
    result1_list = result1.to_dict(orient="records")
    result2_list = result2.to_dict(orient="records")
    
    # Return the results as JSON
    return jsonify({"protein1": result1_list, "protein2": result2_list})

if __name__ == '__main__':
    app.run(debug=True)