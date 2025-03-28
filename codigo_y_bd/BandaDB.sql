CREATE DATABASE BandaDB;

USE BandaDB;

CREATE TABLE Banda (
	id INT PRIMARY KEY IDENTITY(1,1),
	nombre VARCHAR(255) NOT NULL, 
	total_seguidores INT DEFAULT 0
);

CREATE TABLE Integrante (
	id INT PRIMARY KEY IDENTITY (1,1), 
	nombre VARCHAR(255) NOT NULL, 
	instrumento VARCHAR(255),
	imagen VARCHAR(255),
	seguidores INT DEFAULT 0,
	conciertos INT DEFAULT 0, 
	ganancias FLOAT DEFAULT 0, 
	banda_id INT, 
	FOREIGN KEY (banda_id) REFERENCES Banda(id) ON DELETE SET NULL
);
CREATE TABLE Concierto(
	id	INT PRIMARY KEY IDENTITY(1,1),
	fecha DATE NOT NULL,
	ganancias FLOAT DEFAULT 0
);
CREATE TABLE Integrante_Concierto(
	id INT PRIMARY KEY IDENTITY(1,1),
	integrante_id INT NOT NULL, 
	concierto_id INT NOT NULL,
	FOREIGN KEY (integrante_id)REFERENCES Integrante(id) ON DELETE CASCADE,
	FOREIGN KEY (concierto_id)REFERENCES Concierto(id) ON DELETE CASCADE
);

INSERT INTO Banda (nombre, total_seguidores) VALUES ('RockStars', 50000);


INSERT INTO Integrante (nombre, instrumento, imagen, seguidores, conciertos, ganancias, banda_id)
VALUES ('Juan Pérez', 'Guitarra', 'juan.jpg', 10000, 50, 50000, 1);


INSERT INTO Concierto (fecha, ganancias) VALUES ('2025-06-01', 200000);


INSERT INTO Integrante_Concierto (integrante_id, concierto_id) VALUES (1, 1);