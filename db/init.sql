-- MySQL 컨테이너의 데이터 볼륨이 비어 있을 때 최초 한 번 실행됩니다.
-- 데이터베이스 이름은 MYSQL_DATABASE 환경변수로 전달받습니다.

SET NAMES utf8mb4;

CREATE TABLE IF NOT EXISTS accounts (
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(80) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_accounts_username (username),
    KEY ix_accounts_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS people (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    gender VARCHAR(20) NOT NULL,
    age INT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY ix_people_name (name),
    CONSTRAINT chk_people_age CHECK (age BETWEEN 0 AND 150),
    CONSTRAINT chk_people_gender CHECK (gender IN ('Male', 'Female'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO people (name, gender, age)
SELECT seed.name, seed.gender, seed.age
FROM (
    SELECT '홍길동' AS name, 'Male' AS gender, 25 AS age
    UNION ALL SELECT '김철수', 'Male', 32
    UNION ALL SELECT '이영희', 'Female', 28
    UNION ALL SELECT '박지민', 'Female', 40
) AS seed
WHERE NOT EXISTS (SELECT 1 FROM people LIMIT 1);
