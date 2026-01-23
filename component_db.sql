CREATE DATABASE  IF NOT EXISTS `component_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `component_db`;
-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: component_db
-- ------------------------------------------------------
-- Server version	8.0.44

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
-- Table structure for table `components`
--

DROP TABLE IF EXISTS `components`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `components` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `image` varchar(255) DEFAULT NULL,
  `datasheet` varchar(255) DEFAULT NULL,
  `type` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `components`
--

LOCK TABLES `components` WRITE;
/*!40000 ALTER TABLE `components` DISABLE KEYS */;
INSERT INTO `components` VALUES (1,'NE555','Timer IC used for generating precise time delays.','ne555.jpg','datasheets/ne555.pdf','Timer IC'),(2,'LM741','Operational amplifier widely used in analog circuits.','lm741.jpg','datasheets/lm741.pdf','Operational Amplifier'),(3,'LM7805','5V positive voltage regulator.','lm7805.jpg','datasheets/lm7805.pdf','Voltage Regulator'),(4,'LM7905','5V negative voltage regulator.','lm7905.jpg','datasheets/lm7905.pdf','Voltage Regulator'),(5,'LM7812','12V positive voltage regulator.','lm7812.jpg','datasheets/lm7812.pdf','Voltage Regulator'),(6,'LM7912','12V negative voltage regulator.','lm7912.jpg','datasheets/lm7912.pdf','Voltage Regulator'),(7,'LM 3V REGULATOR','3V voltage regulator for low voltage circuits.','lm3v.jpg','datasheets/lm3v.pdf','Voltage Regulator'),(8,'LM7909','9V negative voltage regulator.','lm7909.jpg','datasheets/lm7909.pdf','Voltage Regulator'),(9,'LM7809','9V positive voltage regulator.','lm7809.jpg','datasheets/lm7809.pdf','Voltage Regulator'),(10,'BC237','NPN general-purpose transistor.','bc237.jpg','datasheets/bc237.pdf','Transistor'),(11,'BC337','NPN transistor for switching and amplification.','bc337.jpg','datasheets/bc337.pdf','Transistor'),(12,'2N2219','NPN transistor used in general purpose amplification.','2n2219.jpg','datasheets/2n2219.pdf','Transistor'),(13,'2N2905','PNP transistor for amplification and switching.','2n2905.jpg','datasheets/2n2905.pdf','Transistor'),(14,'BC547','NPN transistor used in low power amplification.','bc547.jpg','datasheets/bc547.pdf','Transistor'),(15,'BC557','PNP transistor for low power amplification.','bc557.jpg','datasheets/bc557.pdf','Transistor'),(16,'TIP31','NPN power transistor for switching.','tip31.jpg','datasheets/tip31.pdf','Transistor'),(17,'TIP32','PNP power transistor for switching.','tip32.jpg','datasheets/tip32.pdf','Transistor'),(18,'TIP 3055','High power NPN transistor.','tip3055.jpg','datasheets/tip3055.pdf','Transistor'),(19,'TIP 2955','High power PNP transistor.','tip2955.jpg','datasheets/tip2955.pdf','Transistor'),(20,'BUK455','Power MOSFET transistor.','buk455.jpg','datasheets/buk455.pdf','Transistor'),(21,'MOC3041','Optocoupler for TRIAC triggering.','moc3041.jpg','datasheets/moc3041.pdf','Optocoupler'),(22,'MOC3021','Optocoupler used for isolation.','moc3021.jpg','datasheets/moc3021.pdf','Optocoupler'),(23,'BT139','TRIAC used for AC power control.','bt139.jpg','datasheets/bt139.pdf','TRIAC'),(24,'BT136','TRIAC for power switching.','bt136.jpg','datasheets/bt136.pdf','TRIAC'),(25,'35M0630','Dip Switch 3 pole.','35m0630.jpg','datasheets/35m0630.pdf','Switch'),(26,'TACT SWITCHES 5MM','Momentary push button switches.','tact_switch_5mm.jpg','','Switch'),(27,'TOGGLE DPDT','Double pole double throw toggle switch.','toggle_dpdt.jpg','','Switch'),(28,'TOGGLE SPST','Single pole single throw toggle switch.','toggle_spst.jpg','','Switch'),(29,'14M1006','2 Pin Tactile Switch.','14m1006.jpg','datasheets/14m1006.pdf','Switch'),(30,'14M8977','Mini Micro Limit Switch SPDT Lever.','14m8977.jpg','','Switch'),(31,'VOL CONTROL POTS: 1K','Variable resistor, 1 kilo-ohm.','pot_1k.jpg','datasheets/pot_1k.pdf','Potentiometer'),(32,'VOL CONTROL POTS: 5K','Variable resistor, 5 kilo-ohms.','pot_5k.jpg','datasheets/pot_5k.pdf','Potentiometer'),(33,'VOL CONTROL POTS: 10K','Variable resistor, 10 kilo-ohms.','pot_10k.jpg','datasheets/pot_10k.pdf','Potentiometer'),(34,'VOL CONTROL POTS: 100K','Variable resistor, 100 kilo-ohms.','pot_100k.jpg','datasheets/pot_100k.pdf','Potentiometer'),(35,'LED RED 5MM','Red LED indicator, 5mm size.','led_red_5mm.jpg','','LED'),(36,'LED GREEN 5MM','Green LED indicator, 5mm size.','led_green_5mm.jpg','','LED'),(37,'LED YELLOW 5MM','Yellow LED indicator, 5mm size.','led_yellow_5mm.jpg','','LED'),(38,'14M1010','PCB Tactile SWITCH.','14m1010.jpg','','Switch'),(39,'IN4148','Fast switching diode.','in4148.jpg','datasheets/in4148.pdf','Diode'),(40,'IN4007','High voltage rectifier diode.','in4007.jpg','datasheets/in4007.pdf','Diode'),(41,'RELAY 5V','5 Volt electromagnetic relay.','relay_5v.jpg','datasheets/relay_5v.pdf','Relay'),(42,'RELAY 12V','12 Volt electromagnetic relay.','relay_12v.jpg','datasheets/relay_12v.pdf','Relay');
/*!40000 ALTER TABLE `components` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `loans`
--

DROP TABLE IF EXISTS `loans`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `loans` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `item` varchar(255) DEFAULT NULL,
  `returned` tinyint DEFAULT '0',
  `loan_date` datetime DEFAULT NULL,
  `return_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `loans_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `loans`
--

LOCK TABLES `loans` WRITE;
/*!40000 ALTER TABLE `loans` DISABLE KEYS */;
INSERT INTO `loans` VALUES (1,2,'PIC Kit 4 Starter Kit',1,'2026-01-15 16:47:57','2026-01-15 16:48:50'),(2,2,'Electronic Robotic Vehicle',1,'2026-01-15 23:48:45','2026-01-15 23:49:43'),(3,2,'PIC Kit 4 Starter Kit',1,'2026-01-16 06:39:53','2026-01-16 06:40:45'),(4,2,'Electronic Robotic Vehicle',1,'2026-01-16 06:47:25','2026-01-16 06:48:15');
/*!40000 ALTER TABLE `loans` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `logs`
--

DROP TABLE IF EXISTS `logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `component_id` int DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `component_id` (`component_id`),
  CONSTRAINT `logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `logs_ibfk_2` FOREIGN KEY (`component_id`) REFERENCES `components` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs`
--

LOCK TABLES `logs` WRITE;
/*!40000 ALTER TABLE `logs` DISABLE KEYS */;
INSERT INTO `logs` VALUES (10,2,2,2,'2026-01-15 16:47:45'),(11,2,3,3,'2026-01-15 16:52:51'),(12,2,1,1,'2026-01-15 16:55:22'),(13,2,1,1,'2026-01-15 23:48:21'),(14,2,10,1,'2026-01-16 06:39:36'),(15,2,13,2,'2026-01-16 06:47:12');
/*!40000 ALTER TABLE `logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `student_number` varchar(20) NOT NULL,
  `role` varchar(20) DEFAULT 'student',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','000000000','admin'),(2,'Kiara Chetty','221008769','student');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-01-16  9:40:19
