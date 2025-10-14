-- Create PowerDNS schema
CREATE TABLE IF NOT EXISTS domains (
  id                    INT AUTO_INCREMENT,
  name                  VARCHAR(255) NOT NULL,
  master                VARCHAR(128),
  last_check            INT,
  type                  VARCHAR(6) NOT NULL,
  notified_serial       INT,
  account               VARCHAR(40),
  PRIMARY KEY (id)
) Engine=InnoDB CHARACTER SET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE IF NOT EXISTS records (
  id                    BIGINT AUTO_INCREMENT,
  domain_id             INT DEFAULT 0,
  name                  VARCHAR(255),
  type                  VARCHAR(10),
  content               VARCHAR(65535),
  ttl                   INT DEFAULT 3600,
  prio                  INT DEFAULT 0,
  change_date           INT,
  disabled              TINYINT DEFAULT 0,
  ordername             VARCHAR(255),
  auth                  TINYINT DEFAULT 1,
  PRIMARY KEY (id)
) Engine=InnoDB CHARACTER SET=utf8 COLLATE=utf8_unicode_ci;

CREATE UNIQUE INDEX rec_name_type ON records (domain_id, name, type, content, disabled);

CREATE TABLE IF NOT EXISTS supermasters (
  ip                    VARCHAR(25) NOT NULL,
  nameserver            VARCHAR(255) NOT NULL,
  account               VARCHAR(40)
) Engine=InnoDB CHARACTER SET=utf8 COLLATE=utf8_unicode_ci;

-- Insert example domain
INSERT INTO domains (name, type) VALUES ('example.com', 'NATIVE');
INSERT INTO records (domain_id, name, type, content, ttl, prio) VALUES (1, 'example.com', 'SOA', 'ns1.example.com hostmaster.example.com 1 10800 3600 604800 3600', 3600, 0);
INSERT INTO records (domain_id, name, type, content, ttl, prio) VALUES (1, 'example.com', 'NS', 'ns1.example.com', 3600, 0);

-- Create PowerDNS Admin user
CREATE USER IF NOT EXISTS 'pda'@'%' IDENTIFIED BY 'pdaadmin';
GRANT ALL PRIVILEGES ON powerdns.* TO 'pda'@'%';
FLUSH PRIVILEGES;
