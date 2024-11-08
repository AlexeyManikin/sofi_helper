DROP TABLE IF EXISTS `bills`;
CREATE TABLE `bills` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_create` DATETIME NOT NULL,
  `bills_id` int(11) NOT NULL,
  `bills_hash` varchar(32) NOT NULL,
  `operator` varchar(32) NOT NULL,
  `operator_code` varchar(32) NOT NULL,
  `paied_by` varchar(32) NOT NULL,
  `table_desc` varchar(32) NOT NULL,
  `total` FLOAT(10,2) NOT NULL,
  `total_discount` FLOAT(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY (`bills_id`),
  UNIQUE KEY (`bills_hash`),
  KEY (`operator`),
  KEY (`table_desc`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `dishes`;
CREATE TABLE `dishes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bills_id` int(11) NOT NULL,
  `name` varchar(64) NOT NULL,
  `item_count` int(11) NOT NULL,
  `price` FLOAT(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY (`name`),
  INDEX bills_id (bills_id),
    FOREIGN KEY (bills_id)
        REFERENCES bills(bills_id)
        ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `raw_data_from_message`;
CREATE TABLE `raw_data_from_message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_create` DATETIME NOT NULL,
  `writer` varchar(64) NOT NULL,
  `messages` text NOT NULL,
  `date_int` int(11) NOT NULL,
  `is_done` int(1) default 0,
  PRIMARY KEY (`id`),
  KEY (`date_create`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `cost_structure`;
CREATE TABLE `cost_structure` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_create` DATETIME NOT NULL,
  `raw_data_id` int(11) NOT NULL,
  `group_type` varchar(64) NOT NULL,
  `type` varchar(64) NOT NULL,
  `summ` float(8,2) NOT NULL,
  `date` DATETIME NOT NULL,
  `description` varchar(64) NOT NULL,
  `model` text,
  `promt` text,
  `prompt_tokens` int(11),
  `total_tokens` int(11),
  `completion_tokens` int(11),
  `elapsed_time` float(5,2),
  `raw_answer` text,
  `answer_code` int(11),
  PRIMARY KEY (`id`),
  KEY (`date_create`),
  INDEX raw_data_id (raw_data_id),
    FOREIGN KEY (raw_data_id)
        REFERENCES raw_data_from_message(id)
        ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `cost_structure_test`;
CREATE TABLE `cost_structure_test` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_create` DATETIME NOT NULL,
  `raw_data_id` int(11) NOT NULL,
  `group_type` varchar(64) NOT NULL,
  `type` varchar(64) NOT NULL,
  `summ` float(8,2) NOT NULL,
  `date` DATETIME NOT NULL,
  `description` varchar(64) NOT NULL,
  `model` text,
  `promt` text,
  `prompt_tokens` int(11),
  `total_tokens` int(11),
  `completion_tokens` int(11),
  `elapsed_time` float(5,2),
  `raw_answer` text,
  `answer_code` int(11),
  PRIMARY KEY (`id`),
  KEY (`date_create`),
  INDEX raw_data_id (raw_data_id),
    FOREIGN KEY (raw_data_id)
        REFERENCES raw_data_from_message(id)
        ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;