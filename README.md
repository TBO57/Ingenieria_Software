# Ingenieria_Software

Proyecto de ingenieria de software

# Requerimientos para el funcionamiento del proyecto:

Paso 1 instalación de python:
Recomendamos la instalación de python 3.10.0, la cual es la versión usada en este aplicativo
https://www.python.org/downloads/

Paso 2 instalación de paquetes python:
Estos son los paquetes necesarios para ejecutar el aplicativo
pip install Flask Flask-MySQLdb

Paso 3 instalación de gestor de base de datos:
Para poder manipular los datos del aplicativo, es necesario instalar un gestor de base de datos, en nuestro caso instalaremos MySQl con el paquete XAMPP.
https://www.apachefriends.org/es/index.html

# Base de datos:

DROP DATABASE IF EXISTS db_python;
CREATE DATABASE db_python CHARACTER SET utf8mb4;
USE db_python;

CREATE TABLE Persona (
Id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
N_Documento INTEGER UNSIGNED NOT NULL ,
Tipo_Documento VARCHAR(10) NULL ,
Primer_Nombre VARCHAR(20) NULL ,
Segundo_Nombre VARCHAR(20) NULL ,
Primer_Apellido VARCHAR(20) NULL ,
Segundo_Apellido VARCHAR(20) NULL ,
Correo VARCHAR(250) NULL ,
Celular INTEGER UNSIGNED NULL ,
PRIMARY KEY(Id));

CREATE TABLE Reporte (
Id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
descripcion TEXT NULL ,
Fecha DATETIME NULL default CURRENT_TIMESTAMP,
PRIMARY KEY(Id));

CREATE TABLE Operador (
idOperador INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
Persona_Id INTEGER UNSIGNED NOT NULL ,
Usuario VARCHAR(50) NULL ,
Contrasena VARCHAR(50) NULL ,
PRIMARY KEY(idOperador),
FOREIGN KEY(Persona_Id)
REFERENCES Persona(Id)
ON DELETE NO ACTION
ON UPDATE NO ACTION);

CREATE TABLE Administrador (
idAdministrador INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
Persona_Id INTEGER UNSIGNED NOT NULL ,
Usuario VARCHAR(50) NULL ,
Contrasena VARCHAR(50) NULL ,
PRIMARY KEY(idAdministrador),
FOREIGN KEY(Persona_Id)
REFERENCES Persona(Id)
ON DELETE NO ACTION
ON UPDATE NO ACTION);

CREATE TABLE Estudiante (
idEstudiante INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
Persona_Id INTEGER UNSIGNED NOT NULL ,
PRIMARY KEY(idEstudiante),
FOREIGN KEY(Persona_Id)
REFERENCES Persona(Id)
ON DELETE NO ACTION
ON UPDATE NO ACTION);

CREATE TABLE Cuenta (
Serial INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
Estudiante_idEstudiante INTEGER UNSIGNED NOT NULL ,
N_almuerzo INTEGER UNSIGNED NULL ,
PRIMARY KEY(Serial),
FOREIGN KEY(Estudiante_idEstudiante)
REFERENCES Estudiante(idEstudiante)
ON DELETE NO ACTION
ON UPDATE NO ACTION);

CREATE TABLE Transferencia (
idTransferencia INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
Cuenta_Serial INTEGER UNSIGNED NOT NULL ,
Fecha DATETIME NULL default CURRENT_TIMESTAMP,
Valor INTEGER UNSIGNED NULL ,
PRIMARY KEY(idTransferencia),
FOREIGN KEY(Cuenta_Serial)
REFERENCES Cuenta(Serial)
ON DELETE NO ACTION
ON UPDATE NO ACTION);

INSERT INTO `persona` (`Id`, `N_Documento`, `Tipo_Documento`, `Primer_Nombre`, `Segundo_Nombre`, `Primer_Apellido`, `Segundo_Apellido`, `Correo`, `Celular`) VALUES (NULL, '1', 'id', 'admin', 'admin', 'admin', 'admin', 'admin@gmail.com', '1');
INSERT INTO `administrador` (`idAdministrador`, `Persona_Id`, `Usuario`, `Contrasena`) VALUES (NULL, '1', 'admin', 'admin');

INSERT INTO `persona` (`Id`, `N_Documento`, `Tipo_Documento`, `Primer_Nombre`, `Segundo_Nombre`, `Primer_Apellido`, `Segundo_Apellido`, `Correo`, `Celular`) VALUES (NULL, '2', 'id', 'op', 'op', 'op', 'op', 'op@gmail.com', '2');
INSERT INTO `operador` (`idOperador`, `Persona_Id`, `Usuario`, `Contrasena`) VALUES (NULL, '2', 'op', 'op');
