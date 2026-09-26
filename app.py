from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")

DB_CONFIG = {
    "host": os.environ.get("MYSQLHOST", "localhost"),
    "port": int(os.environ.get("MYSQLPORT", "3306")),
    "user": os.environ.get("MYSQLUSER", "root"),
    "password": os.environ.get("MYSQLPASSWORD", "NewPassword123"),
    "database": os.environ.get(
        "MYSQL_DATABASE",
        os.environ.get("MYSQLDATABASE", "study_portal")
    )
}


def get_db():
    return mysql.connector.connect(**DB_CONFIG)


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login first.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get("role") != "admin":
            flash("Admin access required.", "danger")
            return redirect(url_for("dashboard"))
        return f(*args, **kwargs)
    return wrapper


@app.route("/")
def index():
    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("SELECT id, name FROM subjects ORDER BY name")
    subjects = cur.fetchall()

    cur.close()
    db.close()

    return render_template("index.html", subjects=subjects)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        confirm = request.form["confirm_password"]

        if password != confirm:
            flash("Passwords do not match.", "danger")
            return render_template("signup.html")

        if len(password) < 6:
            flash("Password must contain at least 6 characters.", "danger")
            return render_template("signup.html")

        db = get_db()
        cur = db.cursor()

        cur.execute("SELECT id FROM users WHERE email=%s", (email,))

        if cur.fetchone():
            flash("Email is already registered.", "danger")
            cur.close()
            db.close()
            return render_template("signup.html")

        hashed = generate_password_hash(password)

        cur.execute(
            """
            INSERT INTO users (name, email, password_hash, role)
            VALUES (%s,%s,%s,'student')
            """,
            (name, email, hashed)
        )

        db.commit()

        cur.close()
        db.close()

        flash("Account created successfully. Please login.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        db = get_db()
        cur = db.cursor(dictionary=True)

        cur.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        user = cur.fetchone()

        cur.close()
        db.close()

        if user and check_password_hash(
            user["password_hash"],
            password
        ):
            session["user_id"] = user["id"]
            session["name"] = user["name"]
            session["role"] = user["role"]

            if user["role"] == "admin":
                return redirect(url_for("admin"))

            return redirect(url_for("dashboard"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("index"))


@app.route("/resources/<resource_type>")
@login_required
def resource_subjects(resource_type):
    # Show the subject-selection screen for each resource category.
    allowed_types = {"notes", "ebook", "paper", "video"}
    if resource_type not in allowed_types:
        flash("Invalid resource category.", "danger")
        return redirect(url_for("dashboard"))

    selected_subject = request.args.get("subject", "")

    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("""
        SELECT s.id, s.name, COUNT(r.id) AS resource_count
        FROM subjects s
        LEFT JOIN resources r
          ON r.subject_id = s.id
         AND r.resource_type = %s
         AND r.verified = 1
        GROUP BY s.id, s.name
        ORDER BY s.name
    """, (resource_type,))

    subjects = cur.fetchall()

    resources = []
    if selected_subject.isdigit():
        cur.execute("""
            SELECT r.id, r.title, r.description, r.resource_type, r.url,
                   s.name AS subject
            FROM resources r
            JOIN subjects s ON s.id = r.subject_id
            WHERE r.subject_id = %s
              AND r.resource_type = %s
              AND r.verified = 1
            ORDER BY r.created_at DESC
        """, (int(selected_subject), resource_type))
        resources = cur.fetchall()

    cur.close()
    db.close()

    labels = {
        "notes": "Notes",
        "ebook": "E-Books",
        "paper": "Previous Year Question Papers",
        "video": "Video Lectures"
    }

    return render_template(
        "resource_subjects.html",
        subjects=subjects,
        resources=resources,
        selected_subject=selected_subject,
        resource_type=resource_type,
        resource_label=labels[resource_type]
    )


@app.route("/dashboard")
@login_required
def dashboard():
    db = get_db()
    cur = db.cursor(dictionary=True)

    q = request.args.get("q", "").strip()
    subject_id = request.args.get("subject", "")
    resource_type = request.args.get("type", "")

    query = """
        SELECT r.id,
               r.title,
               r.description,
               r.resource_type,
               r.url,
               s.name AS subject
        FROM resources r
        JOIN subjects s ON s.id = r.subject_id
        WHERE r.verified = 1
    """

    params = []

    if q:
        query += """
            AND (
                r.title LIKE %s
                OR r.description LIKE %s
                OR s.name LIKE %s
            )
        """

        like = f"%{q}%"
        params += [like, like, like]

    if subject_id.isdigit():
        query += " AND r.subject_id = %s"
        params.append(int(subject_id))

    if resource_type:
        query += " AND r.resource_type = %s"
        params.append(resource_type)

    query += " ORDER BY r.created_at DESC"

    cur.execute(query, tuple(params))
    resources = cur.fetchall()

    cur.execute(
        "SELECT id, name FROM subjects ORDER BY name"
    )
    subjects = cur.fetchall()

    cur.close()
    db.close()

    return render_template(
        "dashboard.html",
        resources=resources,
        subjects=subjects,
        q=q,
        selected_subject=subject_id,
        selected_type=resource_type
    )


@app.route("/admin")
@login_required
@admin_required
def admin():
    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("""
        SELECT r.id,
               r.title,
               r.description,
               r.resource_type,
               r.url,
               r.subject_id,
               r.verified,
               s.name AS subject
        FROM resources r
        JOIN subjects s ON s.id = r.subject_id
        ORDER BY r.created_at DESC
    """)

    resources = cur.fetchall()

    cur.execute(
        "SELECT id, name FROM subjects ORDER BY name"
    )
    subjects = cur.fetchall()

    cur.execute("SELECT COUNT(*) AS c FROM subjects")
    subject_count = cur.fetchone()["c"]

    cur.execute("SELECT COUNT(*) AS c FROM resources")
    resource_count = cur.fetchone()["c"]

    cur.execute(
        "SELECT COUNT(*) AS c FROM resources WHERE verified=1"
    )
    verified_count = cur.fetchone()["c"]

    cur.execute(
        "SELECT COUNT(*) AS c FROM resources WHERE verified=0"
    )
    pending_count = cur.fetchone()["c"]

    cur.close()
    db.close()

    return render_template(
        "admin.html",
        resources=resources,
        subjects=subjects,
        subject_count=subject_count,
        resource_count=resource_count,
        verified_count=verified_count,
        pending_count=pending_count
    )


# ---------------------------------------------------------
# ADD RESOURCE
# ---------------------------------------------------------

@app.route("/admin/resource/add", methods=["POST"])
@login_required
@admin_required
def add_resource():

    title = request.form["title"].strip()
    description = request.form["description"].strip()
    subject_id = request.form["subject_id"]
    resource_type = request.form["resource_type"]
    url = request.form["url"].strip()

    db = get_db()
    cur = db.cursor()

    cur.execute("""
        INSERT INTO resources
        (title, description, subject_id, resource_type, url, verified)
        VALUES (%s,%s,%s,%s,%s,0)
    """, (
        title,
        description,
        subject_id,
        resource_type,
        url
    ))

    db.commit()

    cur.close()
    db.close()

    flash(
        "Resource added and marked as pending verification.",
        "success"
    )

    return redirect(url_for("admin"))


# ---------------------------------------------------------
# EDIT RESOURCE - SHOW EDIT FORM
# ---------------------------------------------------------

@app.route(
    "/admin/resource/<int:resource_id>/edit",
    methods=["GET"]
)
@login_required
@admin_required
def edit_resource(resource_id):

    db = get_db()
    cur = db.cursor(dictionary=True)

    # Get selected resource
    cur.execute("""
        SELECT id,
               title,
               description,
               subject_id,
               resource_type,
               url,
               verified
        FROM resources
        WHERE id=%s
    """, (resource_id,))

    resource = cur.fetchone()

    if not resource:
        cur.close()
        db.close()

        flash("Resource not found.", "danger")
        return redirect(url_for("admin"))

    # Get all subjects
    cur.execute("""
        SELECT id, name
        FROM subjects
        ORDER BY name
    """)

    subjects = cur.fetchall()

    cur.close()
    db.close()

    return render_template(
        "edit_resource.html",
        resource=resource,
        subjects=subjects
    )


# ---------------------------------------------------------
# EDIT RESOURCE - UPDATE DATABASE
# ---------------------------------------------------------

@app.route(
    "/admin/resource/<int:resource_id>/edit",
    methods=["POST"]
)
@login_required
@admin_required
def update_resource(resource_id):

    title = request.form["title"].strip()
    description = request.form["description"].strip()
    subject_id = request.form["subject_id"]
    resource_type = request.form["resource_type"]
    url = request.form["url"].strip()

    db = get_db()
    cur = db.cursor()

    cur.execute("""
        UPDATE resources
        SET title=%s,
            description=%s,
            subject_id=%s,
            resource_type=%s,
            url=%s
        WHERE id=%s
    """, (
        title,
        description,
        subject_id,
        resource_type,
        url,
        resource_id
    ))

    db.commit()

    cur.close()
    db.close()

    flash(
        "Resource updated successfully.",
        "success"
    )

    return redirect(url_for("admin"))


# ---------------------------------------------------------
# VERIFY RESOURCE
# ---------------------------------------------------------

@app.route(
    "/admin/resource/<int:resource_id>/verify",
    methods=["POST"]
)
@login_required
@admin_required
def verify_resource(resource_id):

    db = get_db()
    cur = db.cursor()

    cur.execute(
        "UPDATE resources SET verified=1 WHERE id=%s",
        (resource_id,)
    )

    db.commit()

    cur.close()
    db.close()

    flash("Resource verified.", "success")

    return redirect(url_for("admin"))


# ---------------------------------------------------------
# DELETE RESOURCE
# ---------------------------------------------------------

@app.route(
    "/admin/resource/<int:resource_id>/delete",
    methods=["POST"]
)
@login_required
@admin_required
def delete_resource(resource_id):

    db = get_db()
    cur = db.cursor()

    cur.execute(
        "DELETE FROM resources WHERE id=%s",
        (resource_id,)
    )

    db.commit()

    cur.close()
    db.close()

    flash("Resource deleted.", "success")

    return redirect(url_for("admin"))



# -------------------- SAFE ADMIN BOOTSTRAP --------------------
# Set ADMIN_EMAIL and ADMIN_PASSWORD in the deployment environment.
# On startup, create the admin account only when no admin account exists.
# The password is stored using Werkzeug's secure password hash.

def ensure_admin_account():
    admin_email = os.environ.get("ADMIN_EMAIL")
    admin_password = os.environ.get("ADMIN_PASSWORD")

    # Stop admin setup if credentials are not configured
    if not admin_email or not admin_password:
        print("ADMIN_EMAIL/ADMIN_PASSWORD not configured; skipping admin setup.")
        return

    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        # Check whether an admin account already exists
        cursor.execute(
            "SELECT id FROM users WHERE role = 'admin' LIMIT 1"
        )

        existing_admin = cursor.fetchone()

        # Convert the password into a secure hash
        password_hash = generate_password_hash(admin_password)

        if existing_admin:
            # Update the existing admin account
            cursor.execute(
                """
                UPDATE users
                SET email = %s,
                    password_hash = %s,
                    role = 'admin'
                WHERE id = %s
                """,
                (
                    admin_email,
                    password_hash,
                    existing_admin["id"]
                )
            )

            conn.commit()
            print("Admin account updated successfully.")

        else:
            # Create a new admin account
            cursor.execute(
                """
                INSERT INTO users
                (name, email, password_hash, role)
                VALUES (%s, %s, %s, 'admin')
                """,
                (
                    "Administrator",
                    admin_email,
                    password_hash
                )
            )

            conn.commit()
            print("Admin account created successfully.")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Admin setup error: {e}")

ensure_admin_account()

if __name__ == "__main__":
    app.run(debug=True)