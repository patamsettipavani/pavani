CREATE DATABASE IF NOT EXISTS interview_x_ai
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE interview_x_ai;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(200) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS resumes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    filename VARCHAR(255) NOT NULL,
    filepath VARCHAR(500) NOT NULL,
    extracted_text LONGTEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS resume_analyses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    resume_id INT NOT NULL,
    job_description TEXT NOT NULL,
    ats_score FLOAT,
    grammar_score FLOAT,
    skills_match FLOAT,
    overall_score FLOAT,
    matched_skills JSON,
    missing_skills JSON,
    suggestions JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS interviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    resume_id INT,
    company VARCHAR(200),
    role VARCHAR(200),
    branch VARCHAR(200),
    difficulty VARCHAR(50),
    mode VARCHAR(50),
    status VARCHAR(50) DEFAULT 'in_progress',
    overall_score FLOAT,
    total_questions INT DEFAULT 5,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS interview_questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    interview_id INT NOT NULL,
    question_number INT NOT NULL,
    question_text TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (interview_id) REFERENCES interviews(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS interview_answers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT NOT NULL,
    interview_id INT NOT NULL,
    user_answer TEXT NOT NULL,
    score FLOAT,
    verdict VARCHAR(50),
    feedback TEXT,
    strengths TEXT,
    improvements TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (question_id) REFERENCES interview_questions(id) ON DELETE CASCADE,
    FOREIGN KEY (interview_id) REFERENCES interviews(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS interview_reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    interview_id INT NOT NULL UNIQUE,
    overall_score FLOAT,
    strengths JSON,
    weaknesses JSON,
    recommendations JSON,
    interview_dna JSON,
    resume_match JSON,
    heatmap JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (interview_id) REFERENCES interviews(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS coding_rounds (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    interview_id INT,
    branch VARCHAR(200),
    language VARCHAR(100),
    difficulty VARCHAR(50),
    question_text TEXT,
    user_code LONGTEXT,
    ai_review TEXT,
    score FLOAT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (interview_id) REFERENCES interviews(id) ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS interview_events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    interview_id INT NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    event_data JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (interview_id) REFERENCES interviews(id) ON DELETE CASCADE
) ENGINE=InnoDB;