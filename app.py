import os
from datetime import datetime
import pandas as pd

from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
    jsonify,
    redirect,
    url_for,
    session
)

from src.phenotype import PhenotypePredictor
from src.recommendation import DrugRecommendation
from src.report import ReportGenerator

# =====================================================
# Flask Configuration
# =====================================================

app = Flask(__name__)
app.secret_key = "NeuroPGxAdvisor2026"

# =====================================================
# Initialize Classes
# =====================================================

predictor = PhenotypePredictor()
recommendation = DrugRecommendation()
report = ReportGenerator()

# =====================================================
# Load CSV Databases
# =====================================================

disease_df = pd.read_csv("data/disease_database.csv")
gene_df = pd.read_csv("data/gene_information.csv")
genotype_df = pd.read_csv("data/genotype_database.csv")
users_df = pd.read_csv("data/users.csv")


disease_df.fillna("", inplace=True)
gene_df.fillna("", inplace=True)
genotype_df.fillna("", inplace=True)
users_df.fillna("", inplace=True)
# =====================================================
# Save Patient History
# =====================================================

def save_patient_history(
    patient_name,
    disease,
    gene,
    genotype,
    phenotype,
    drug,
    recommendation,
    alternative,
    reason,
    evidence
):

    history_file = "data/patients.csv"

    new_record = pd.DataFrame([{
        "PatientName": patient_name,
        "Disease": disease,
        "Gene": gene,
        "Genotype": genotype,
        "Phenotype": phenotype,
        "Drug": drug,
        "Recommendation": recommendation,
        "AlternativeDrug": alternative,
        "Reason": reason,
        "EvidenceLevel": evidence,
        "DateTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])

    header = not os.path.exists(history_file) or os.path.getsize(history_file) == 0

    new_record.to_csv(
        history_file,
        mode="a",
        header=header,
        index=False
    )
# =====================================================
# Login Page
# =====================================================

@app.route("/login")
def login():

    return render_template("login.html")


# =====================================================
# Login Authentication
# =====================================================

@app.route("/login", methods=["POST"])
def login_post():

    username = request.form["username"].strip()
    password = request.form["password"].strip()

    # Search user in users.csv
    user = users_df[
        (users_df["Username"] == username) &
        (users_df["Password"] == password)
    ]

    # Invalid login
    if user.empty:

        return render_template(
            "login.html",
            error="Invalid Username or Password"
        )

    # Store user details in session
    session["user"] = user.iloc[0]["Username"]
    session["fullname"] = user.iloc[0]["FullName"]
    session["role"] = user.iloc[0]["Role"]
    session["department"] = user.iloc[0]["Department"]
    session["email"] = user.iloc[0]["Email"]
    return redirect(url_for("dashboard"))

# =====================================================
# Logout
# =====================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    print("===== DASHBOARD SESSION =====")
    print(session)
    print("=============================")

    total_diseases = len(disease_df)
    total_genes = len(gene_df)
    total_genotypes = len(genotype_df)

    drug_df = pd.read_csv("data/drug_database.csv")
    total_drugs = len(drug_df)

    return render_template(
        "dashboard.html",
        fullname=session["fullname"],
        role=session["role"],
        department=session["department"],
        email=session["email"],
        total_diseases=total_diseases,
        total_genes=total_genes,
        total_genotypes=total_genotypes,
        total_drugs=total_drugs
    )

# =====================================================
# Admin Panel
# =====================================================

@app.route("/admin")
def admin():

    # Check Login
    if "user" not in session:
        return redirect(url_for("login"))

    # Only Administrator can access Admin Panel
    if session["role"] != "System Administrator":
        return render_template(
            "403.html",
            fullname=session["fullname"],
            role=session["role"]
        )

    users_df = pd.read_csv("data/users.csv")
    disease_df = pd.read_csv("data/disease_database.csv")
    drug_df = pd.read_csv("data/drug_database.csv")
    patient_df = pd.read_csv("data/patients.csv")

    return render_template(
        "admin.html",
        fullname=session["fullname"],
        role=session["role"],
        total_users=len(users_df),
        total_patients=len(patient_df),
        total_diseases=len(disease_df),
        total_drugs=len(drug_df),
        users=users_df.to_dict(orient="records")
    )

# =====================================================
# Add User
# =====================================================

@app.route("/add_user")
def add_user():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template(
        "add_user.html",
        fullname=session["fullname"]
    )
# =====================================================
# Save User
# =====================================================

@app.route("/save_user", methods=["POST"])
def save_user():

    if "user" not in session:
        return redirect(url_for("login"))

    userid = request.form["userid"]
    username = request.form["username"]
    password = request.form["password"]
    role = request.form["role"]
    fullname = request.form["fullname"]
    department = request.form["department"]
    email = request.form["email"]

    users_file = "data/users.csv"

    new_user = pd.DataFrame([{
        "UserID": userid,
        "Username": username,
        "Password": password,
        "Role": role,
        "FullName": fullname,
        "Department": department,
        "Email": email
    }])

    users_df = pd.read_csv(users_file)

    users_df = pd.concat([users_df, new_user], ignore_index=True)

    users_df.to_csv(users_file, index=False)
    return redirect(url_for("admin"))
# =====================================================
# Edit User
# =====================================================

@app.route("/edit_user/<userid>")
def edit_user(userid):

    if "user" not in session:
        return redirect(url_for("login"))

    users_df = pd.read_csv("data/users.csv")

    user = users_df[users_df["UserID"] == userid]

    if user.empty:
        return "User not found"

    user = user.iloc[0]

    return render_template(
        "edit_user.html",
        user=user
    )
# =====================================================
# Update User
# =====================================================

@app.route("/update_user", methods=["POST"])
def update_user():

    if "user" not in session:
        return redirect(url_for("login"))

    users_file = "data/users.csv"

    users_df = pd.read_csv(users_file)

    userid = request.form["userid"]

    users_df.loc[users_df["UserID"] == userid, "Username"] = request.form["username"]
    users_df.loc[users_df["UserID"] == userid, "Password"] = request.form["password"]
    users_df.loc[users_df["UserID"] == userid, "Role"] = request.form["role"]
    users_df.loc[users_df["UserID"] == userid, "FullName"] = request.form["fullname"]
    users_df.loc[users_df["UserID"] == userid, "Department"] = request.form["department"]
    users_df.loc[users_df["UserID"] == userid, "Email"] = request.form["email"]

    users_df.to_csv(users_file, index=False)

    return redirect(url_for("admin"))
# =====================================================
# Delete User
# =====================================================

@app.route("/delete_user/<userid>")
def delete_user(userid):

    if "user" not in session:
        return redirect(url_for("login"))

    users_file = "data/users.csv"

    users_df = pd.read_csv(users_file)

    users_df = users_df[users_df["UserID"] != userid]

    users_df.to_csv(users_file, index=False)

    return redirect(url_for("admin"))
# =====================================================
# Drug Knowledge Base
# =====================================================

@app.route("/druginfo")
def druginfo():

    # User must be logged in
    if "user" not in session:
        return redirect(url_for("login"))

    # Only these roles can access Drug DB
    if session["role"] not in [
        "System Administrator",
        "Doctor",
        "Researcher"
    ]:
        return render_template("403.html")

    drug_df = pd.read_csv("data/drug_database.csv")

    drug_df.fillna("", inplace=True)

    drugs = drug_df.to_dict(orient="records")

    return render_template(
        "druginfo.html",
        fullname=session["fullname"],
        role=session["role"],
        drugs=drugs,
        total_drugs=len(drugs)
    )
# =====================================================
# Add Drug
# =====================================================

@app.route("/add_drug")
def add_drug():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template(
        "add_drug.html",
        fullname=session["fullname"]
    )
# =====================================================
# Save Drug
# =====================================================

@app.route("/save_drug", methods=["POST"])
def save_drug():

    if "user" not in session:
        return redirect(url_for("login"))

    drug_file = "data/drug_database.csv"

    new_drug = pd.DataFrame([{
        "Disease": request.form["disease"],
        "Gene": request.form["gene"],
        "Phenotype": request.form["phenotype"],
        "Drug": request.form["drug"],
        "Recommendation": request.form["recommendation"],
        "AlternativeDrug": request.form["alternative"],
        "Reason": request.form["reason"],
        "EvidenceLevel": request.form["evidence"]
    }])

    drug_df = pd.read_csv(drug_file)

    drug_df = pd.concat([drug_df, new_drug], ignore_index=True)

    drug_df.to_csv(drug_file, index=False)

    return redirect(url_for("druginfo"))
# =====================================================
# Edit Drug
# =====================================================

@app.route("/edit_drug/<int:index>")
def edit_drug(index):

    if "user" not in session:
        return redirect(url_for("login"))

    drug_df = pd.read_csv("data/drug_database.csv")

    drug = drug_df.iloc[index]

    return render_template(
        "edit_drug.html",
        drug=drug,
        index=index
    )
# =====================================================
# Update Drug
# =====================================================

@app.route("/update_drug", methods=["POST"])
def update_drug():

    if "user" not in session:
        return redirect(url_for("login"))

    drug_file = "data/drug_database.csv"

    drug_df = pd.read_csv(drug_file)

    index = int(request.form["index"])

    drug_df.loc[index, "Disease"] = request.form["disease"]
    drug_df.loc[index, "Gene"] = request.form["gene"]
    drug_df.loc[index, "Phenotype"] = request.form["phenotype"]
    drug_df.loc[index, "Drug"] = request.form["drug"]
    drug_df.loc[index, "Recommendation"] = request.form["recommendation"]
    drug_df.loc[index, "AlternativeDrug"] = request.form["alternative"]
    drug_df.loc[index, "Reason"] = request.form["reason"]
    drug_df.loc[index, "EvidenceLevel"] = request.form["evidence"]

    drug_df.to_csv(drug_file, index=False)

    return redirect(url_for("druginfo"))
# =====================================================
# Delete Drug
# =====================================================

@app.route("/delete_drug/<int:index>")
def delete_drug(index):

    if "user" not in session:
        return redirect(url_for("login"))

    drug_file = "data/drug_database.csv"

    drug_df = pd.read_csv(drug_file)

    # Delete the selected row
    drug_df = drug_df.drop(index)

    # Reset index
    drug_df.reset_index(drop=True, inplace=True)

    # Save back to CSV
    drug_df.to_csv(drug_file, index=False)

    return redirect(url_for("druginfo"))
# =====================================================
# Patient History
# =====================================================

@app.route("/history")
def history():

    if "user" not in session:
        return redirect(url_for("login"))

    history_df = pd.read_csv("data/patients.csv")

    history_df = history_df.fillna("")

    history = history_df.to_dict(orient="records")

    return render_template(
        "history.html",
        fullname=session["fullname"],
        role=session["role"],
        history=history,
        total_patients=len(history)
    )
# =====================================================
# Home Page
# =====================================================

@app.route("/")
def home():

    # Check Login
    if "user" not in session:
        return redirect(url_for("login"))

    diseases = sorted(
        disease_df["DiseaseName"]
        .dropna()
        .unique()
        .tolist()
    )

    genes = sorted(
        gene_df["Gene"]
        .dropna()
        .unique()
        .tolist()
    )

    genotypes = sorted(
        genotype_df["Genotype"]
        .dropna()
        .unique()
        .tolist()
    )
    return render_template(
    "index.html",
    username=session["user"],
    fullname=session["fullname"],
    role=session["role"],
    department=session["department"],
    email=session["email"],
    diseases=diseases,
    genes=genes,
    genotypes=genotypes
)


# =====================================================
# API : Get Diseases
# =====================================================

@app.route("/get_diseases")
def get_diseases():

    diseases = sorted(
        disease_df["DiseaseName"]
        .dropna()
        .unique()
        .tolist()
    )

    return jsonify(diseases)


# =====================================================
# API : Get Genes Based On Disease
# =====================================================

@app.route("/get_genes/<disease>")
def get_genes(disease):

    disease = disease.strip()

    row = disease_df[
        disease_df["DiseaseName"] == disease
    ]

    if row.empty:
        return jsonify([])

    related_genes = row.iloc[0]["RelatedGenes"]

    genes = []

    for gene in related_genes.split(";"):

        gene = gene.strip()

        if gene != "":
            genes.append(gene)

    return jsonify(genes)


# =====================================================
# API : Get Genotypes Based On Gene
# =====================================================

@app.route("/get_genotypes/<gene>")
def get_genotypes(gene):

    gene = gene.strip()

    rows = genotype_df[
        genotype_df["Gene"] == gene
    ]

    genotypes = sorted(
        rows["Genotype"]
        .dropna()
        .unique()
        .tolist()
    )

    return jsonify(genotypes)
# =====================================================
# Predict Recommendation
# =====================================================

@app.route("/predict", methods=["POST"])
def predict():

    if "user" not in session:
        return redirect(url_for("login"))

    patient_name = request.form.get("patient_name", "").strip()
    disease = request.form.get("disease", "").strip()
    gene = request.form.get("gene", "").strip()
    genotype = request.form.get("genotype", "").strip()

    # Predict phenotype
    phenotype = predictor.predict(gene, genotype)

    # Get drug recommendation
    result = recommendation.recommend(
        disease,
        gene,
        phenotype
    )

    # Recommendation found
    if result is not None:

        # Generate Report
        report.generate(
            patient_name,
            disease,
            gene,
            genotype,
            phenotype,
            result["Drug"],
            result["Recommendation"],
            result["AlternativeDrug"],
            result["Reason"],
            result["EvidenceLevel"]
        )

        # Save Patient History
        save_patient_history(
            patient_name,
            disease,
            gene,
            genotype,
            phenotype,
            result["Drug"],
            result["Recommendation"],
            result["AlternativeDrug"],
            result["Reason"],
            result["EvidenceLevel"]
        )

        return render_template(
            "result.html",
            patient_name=patient_name,
            disease=disease,
            gene=gene,
            genotype=genotype,
            phenotype=phenotype,
            drug=result["Drug"],
            recommendation=result["Recommendation"],
            alternative=result["AlternativeDrug"],
            reason=result["Reason"],
            evidence=result["EvidenceLevel"]
        )

    # No recommendation found
    return render_template(
        "result.html",
        patient_name=patient_name,
        disease=disease,
        gene=gene,
        genotype=genotype,
        phenotype=phenotype,
        drug="No Recommendation",
        recommendation="No Recommendation Found",
        alternative="-",
        reason="-",
        evidence="-"
    )

# =====================================================
# Download Report
# =====================================================

@app.route("/download/<patient_name>")
def download(patient_name):

    if "user" not in session:
        return redirect(url_for("login"))

    reports_folder = "reports"

    if not os.path.exists(reports_folder):
        return "Reports folder not found."

    filename = f"{patient_name}_report.txt"

    for file in os.listdir(reports_folder):

        if file.lower() == filename.lower():

            return send_from_directory(
                reports_folder,
                file,
                as_attachment=True
            )

    return "Report not found."


# =====================================================
# Run Flask
# =====================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )