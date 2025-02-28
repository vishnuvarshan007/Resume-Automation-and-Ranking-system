-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.4.32-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.10.0.7000
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for resume_db
CREATE DATABASE IF NOT EXISTS `resume_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `resume_db`;

-- Dumping structure for table resume_db.resumes
CREATE TABLE IF NOT EXISTS `resumes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `filename` varchar(255) NOT NULL,
  `score` int(11) NOT NULL,
  `matched_requirements` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table resume_db.resumes: ~5 rows (approximately)
INSERT INTO `resumes` (`id`, `name`, `email`, `phone`, `filename`, `score`, `matched_requirements`) VALUES
	(43, 'Emma johnson', 'emma.johnson@email.com', '9376262828', 'Emma Johnson.pdf', 8, 'Team Player, Diploma, English, JavaScript, 3+ years, Python, React, AWS'),
	(44, 'James anderson', 'james.anderson@email.com', '9784847373', 'James Anderson.pdf', 2, 'English, Python'),
	(45, 'Shusil singh', 'shusilsniper@gmail.com', '7436789027', 'Shusil Singh.pdf', 9, 'Team Player, Diploma, English, MBA, JavaScript, 3+ years, Python, React, AWS'),
	(46, 'Sophia martinez', 'sophia.martinez@email.com', '7597477338', 'Sophia Martinez.pdf', 0, ''),
	(47, 'Srikadhir', 'ssrikadir2007@gmail.com', '9856792728', 'Srikadhir.pdf', 6, 'Team Player, MBA, Bachelor’s Degree, Python, React, AWS');

-- Dumping structure for table resume_db.users
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table resume_db.users: ~0 rows (approximately)
INSERT INTO `users` (`id`, `username`, `password`) VALUES
	(1, 'testuser', 'manager');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
