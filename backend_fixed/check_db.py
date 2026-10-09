import pymysql

conn = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    password="@8008824977-bhavana",
    database="interview_x_ai",
    cursorclass=pymysql.cursors.DictCursor
)

with conn:
    with conn.cursor() as cur:
        print("=" * 60)
        print("📋 USERS TABLE:")
        print("=" * 60)
        cur.execute("SELECT id, username, email FROM users")
        users = cur.fetchall()
        if not users:
            print("  (Empty - No users)")
        for u in users:
            print(f"  ID: {u['id']} | Username: {u['username']} | Email: {u['email']}")

        print("\n" + "=" * 60)
        print("📄 RESUMES TABLE:")
        print("=" * 60)
        cur.execute("SELECT id, user_id, filename, LENGTH(extracted_text) as text_len FROM resumes")
        resumes = cur.fetchall()
        if not resumes:
            print("  (Empty - No resumes uploaded)")
        for r in resumes:
            print(f"  ID: {r['id']} | User ID: {r['user_id']} | File: {r['filename']} | Text Length: {r['text_len']}")

        print("\n" + "=" * 60)
        print("📊 ANALYSES TABLE:")
        print("=" * 60)
        cur.execute("SELECT id, resume_id, ats_score, overall_score FROM resume_analyses")
        analyses = cur.fetchall()
        if not analyses:
            print("  (Empty - No analyses yet)")
        for a in analyses:
            print(f"  ID: {a['id']} | Resume ID: {a['resume_id']} | ATS: {a['ats_score']} | Overall: {a['overall_score']}")