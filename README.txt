ONLINE STUDY MATERIAL PORTAL - UPDATED

Features
--------
- Student signup/login
- Admin login and resource management
- Search resources
- Filter by subject and resource type
- 5 subjects: Java, DBMS, Python, Computer Networks, Mathematics
- 4 resource categories for every subject:
  1. Notes
  2. E-Books / References
  3. Previous Year Papers
  4. Video Lectures
- 20 verified starter resources are included in study_portal.sql.

SETUP
-----
1. Extract the ZIP.
2. Open MySQL Workbench/phpMyAdmin.
3. Import OnlineStudyMaterialPortal/study_portal.sql.
4. The SQL creates the study_portal database, tables, 5 subjects and 20 starter resources.
5. Check app.py DB_CONFIG. By default it expects:
   host=localhost
   user=root
   password=YOUR_MYSQL_PASSWORD (or empty if your MySQL root password is empty)
   database=study_portal
6. Install Python packages:
   pip install -r requirements.txt
7. Run:
   python app.py
8. Open:
   http://127.0.0.1:5000

IMPORTANT
---------
If you already imported an older version of study_portal.sql and the old resource rows are present,
use a fresh database for the demo or delete the old study_portal database before importing this SQL.
Do not delete the database if it contains important student accounts or custom admin resources.

RESOURCE SOURCES
----------------
The starter library uses public educational sources such as NPTEL, Python documentation,
W3Schools, Green Tea Press, OpenStax, RFC Editor and reference sites. Previous-year-paper
entries are clearly labelled as search resources because the exact university/semester paper
archive varies by institution. Admins can replace those links with official college/university
paper URLs from the Admin Dashboard.
