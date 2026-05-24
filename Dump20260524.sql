-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: kykyonetim
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `applications`
--

DROP TABLE IF EXISTS `applications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `applications` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tcno` varchar(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `surname` varchar(50) NOT NULL,
  `appdate` timestamp NOT NULL DEFAULT current_timestamp(),
  `status` varchar(20) DEFAULT 'Pending',
  PRIMARY KEY (`id`),
  UNIQUE KEY `tcno` (`tcno`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `applications`
--

LOCK TABLES `applications` WRITE;
/*!40000 ALTER TABLE `applications` DISABLE KEYS */;
/*!40000 ALTER TABLE `applications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `havuz_isimler`
--

DROP TABLE IF EXISTS `havuz_isimler`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `havuz_isimler` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `isim` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `havuz_isimler`
--

LOCK TABLES `havuz_isimler` WRITE;
/*!40000 ALTER TABLE `havuz_isimler` DISABLE KEYS */;
INSERT INTO `havuz_isimler` VALUES (1,'Yusuf'),(2,'Mert'),(3,'Ahmet'),(4,'Mehmet'),(5,'Mustafa'),(6,'Ali'),(7,'Ömer'),(8,'Emre'),(9,'Arda'),(10,'Burak'),(11,'Can'),(12,'Berk'),(13,'Onur'),(14,'Gökhan'),(15,'Serkan'),(16,'Murat'),(17,'Hakan'),(18,'Volkan'),(19,'Tolga'),(20,'Kerem'),(21,'Sinan'),(22,'Kaan'),(23,'Doruk'),(24,'Yiğit'),(25,'Efe'),(26,'Batu'),(27,'Furkan'),(28,'Enes'),(29,'Selim'),(30,'Tarık'),(31,'Yavuz'),(32,'Mete'),(33,'Ozan'),(34,'Umut'),(35,'Koray'),(36,'Alper'),(37,'Egemen'),(38,'Batuhan'),(39,'Emir'),(40,'Görkem'),(41,'Sarp'),(42,'Baran'),(43,'Tunahan'),(44,'Berkay'),(45,'Cihan'),(46,'Eren'),(47,'Fatih'),(48,'Halil'),(49,'İbrahim'),(50,'Semih');
/*!40000 ALTER TABLE `havuz_isimler` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `havuz_soyisimler`
--

DROP TABLE IF EXISTS `havuz_soyisimler`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `havuz_soyisimler` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `soyisim` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `havuz_soyisimler`
--

LOCK TABLES `havuz_soyisimler` WRITE;
/*!40000 ALTER TABLE `havuz_soyisimler` DISABLE KEYS */;
INSERT INTO `havuz_soyisimler` VALUES (1,'Yılmaz'),(2,'Kaya'),(3,'Demir'),(4,'Çelik'),(5,'Yıldız'),(6,'Yıldırım'),(7,'Aydın'),(8,'Arslan'),(9,'Polat'),(10,'Özdemir'),(11,'Öztürk'),(12,'Şahin'),(13,'Tekin'),(14,'Kılıç'),(15,'Koç'),(16,'Kurt'),(17,'Avcı'),(18,'Aksoy'),(19,'Doğan'),(20,'Aslan'),(21,'Çetin'),(22,'Kara'),(23,'Özkan'),(24,'Erdem'),(25,'Uzun'),(26,'Karadeniz'),(27,'Aktaş'),(28,'Yavuz'),(29,'Güneş'),(30,'Bulut'),(31,'Demirel'),(32,'Bağdat'),(33,'Yüksel'),(34,'Akın'),(35,'Şen'),(36,'Çakır'),(37,'Bakır'),(38,'Tunç'),(39,'Önal'),(40,'Güler'),(41,'Keskin'),(42,'Yaman'),(43,'Yalçın'),(44,'Sarı'),(45,'Bozkurt'),(46,'Coşkun'),(47,'Akçay'),(48,'Sönmez'),(49,'Işık'),(50,'Altun');
/*!40000 ALTER TABLE `havuz_soyisimler` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `leaves`
--

DROP TABLE IF EXISTS `leaves`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `leaves` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tcno` varchar(11) NOT NULL,
  `startdate` date NOT NULL,
  `enddate` date NOT NULL,
  `status` varchar(20) DEFAULT 'Pending',
  PRIMARY KEY (`id`),
  KEY `tcno` (`tcno`),
  CONSTRAINT `leaves_ibfk_1` FOREIGN KEY (`tcno`) REFERENCES `students` (`tcno`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `leaves`
--

LOCK TABLES `leaves` WRITE;
/*!40000 ALTER TABLE `leaves` DISABLE KEYS */;
/*!40000 ALTER TABLE `leaves` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments`
--

DROP TABLE IF EXISTS `payments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tcno` varchar(11) NOT NULL,
  `paydate` timestamp NOT NULL DEFAULT current_timestamp(),
  `period` varchar(7) NOT NULL,
  `fee` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tcno` (`tcno`),
  CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`tcno`) REFERENCES `students` (`tcno`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments`
--

LOCK TABLES `payments` WRITE;
/*!40000 ALTER TABLE `payments` DISABLE KEYS */;
/*!40000 ALTER TABLE `payments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rooms`
--

DROP TABLE IF EXISTS `rooms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rooms` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `block` varchar(50) NOT NULL,
  `roomno` int(11) NOT NULL,
  `capacity` int(11) NOT NULL DEFAULT 6,
  `occupancy` int(11) DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rooms`
--

LOCK TABLES `rooms` WRITE;
/*!40000 ALTER TABLE `rooms` DISABLE KEYS */;
INSERT INTO `rooms` VALUES (1,'A',101,6,0),(2,'A',102,6,0),(3,'A',103,6,0),(4,'A',104,6,0),(5,'A',105,6,0),(6,'A',106,6,0),(7,'A',107,6,0),(8,'A',108,6,0),(9,'A',109,6,0),(10,'A',110,6,0),(11,'A',111,6,0),(12,'A',112,6,0),(13,'A',113,6,0),(14,'A',114,6,0),(15,'A',115,6,0),(16,'A',116,6,0),(17,'A',117,6,0),(18,'A',118,6,0),(19,'A',119,6,0),(20,'A',120,6,0),(21,'A',121,6,0),(22,'A',122,6,0),(23,'A',123,6,0),(24,'A',124,6,0),(25,'A',125,6,0),(26,'A',126,6,0),(27,'A',127,6,0),(28,'A',128,6,0),(29,'A',129,6,0),(30,'A',130,6,0),(31,'A',131,6,0),(32,'A',132,6,0),(33,'B',201,6,0),(34,'B',202,6,0),(35,'B',203,6,0),(36,'B',204,6,0),(37,'B',205,6,0),(38,'B',206,6,0),(39,'B',207,6,0),(40,'B',208,6,0),(41,'B',209,6,0),(42,'B',210,6,0),(43,'B',211,6,0),(44,'B',212,6,0),(45,'B',213,6,0),(46,'B',214,6,0),(47,'B',215,6,0),(48,'B',216,6,0),(49,'B',217,6,0),(50,'B',218,6,0),(51,'B',219,6,0),(52,'B',220,6,0),(53,'B',221,6,0),(54,'B',222,6,0),(55,'B',223,6,0),(56,'B',224,6,0),(57,'B',225,6,0),(58,'B',226,6,0),(59,'B',227,6,0),(60,'B',228,6,0),(61,'B',229,6,0),(62,'B',230,6,0),(63,'B',231,6,0),(64,'B',232,6,0),(65,'C',301,6,0),(66,'C',302,6,0),(67,'C',303,6,0),(68,'C',304,6,0),(69,'C',305,6,0),(70,'C',306,6,0),(71,'C',307,6,0),(72,'C',308,6,0),(73,'C',309,6,0),(74,'C',310,6,0),(75,'C',311,6,0),(76,'C',312,6,0),(77,'C',313,6,0),(78,'C',314,6,0),(79,'C',315,6,0),(80,'C',316,6,0),(81,'C',317,6,0),(82,'C',318,6,0),(83,'C',319,6,0),(84,'C',320,6,0),(85,'C',321,6,0),(86,'C',322,6,0),(87,'C',323,6,0),(88,'C',324,6,0),(89,'C',325,6,0),(90,'C',326,6,0),(91,'C',327,6,0),(92,'C',328,6,0),(93,'C',329,6,0),(94,'C',330,6,0),(95,'C',331,6,0),(96,'C',332,6,0);
/*!40000 ALTER TABLE `rooms` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `tcno` varchar(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `surname` varchar(50) NOT NULL,
  `birthdate` date NOT NULL,
  `roomid` int(11) DEFAULT NULL,
  `allowance` int(11) DEFAULT 45,
  `is_active` tinyint(4) DEFAULT 1,
  PRIMARY KEY (`tcno`),
  KEY `students_ibfk_1` (`roomid`),
  CONSTRAINT `students_ibfk_1` FOREIGN KEY (`roomid`) REFERENCES `rooms` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-24 21:31:44
