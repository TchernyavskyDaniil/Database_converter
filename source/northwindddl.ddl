CREATE SCHEMA dbo;


CREATE TABLE dbo."Employees" (
EmployeeID INTEGER,
LastName VARCHAR,
FirstName VARCHAR,
Title VARCHAR,
TitleOfCourtesy VARCHAR,
BirthDate TIMESTAMP,
HireDate TIMESTAMP,
Address VARCHAR,
City VARCHAR,
Region VARCHAR,
PostalCode VARCHAR,
Country VARCHAR,
HomePhone VARCHAR,
Extension VARCHAR,
Photo TEXT,
Notes TEXT,
ReportsTo INTEGER,
PhotoPath VARCHAR);
CREATE TABLE dbo."Categories" (
CategoryID INTEGER,
CategoryName VARCHAR,
Description TEXT,
Picture TEXT);
CREATE TABLE dbo."Customers" (
CustomerID TEXT,
CompanyName VARCHAR,
ContactName VARCHAR,
ContactTitle VARCHAR,
Address VARCHAR,
City VARCHAR,
Region VARCHAR,
PostalCode VARCHAR,
Country VARCHAR,
Phone VARCHAR,
Fax VARCHAR);
CREATE TABLE dbo."Shippers" (
ShipperID INTEGER,
CompanyName VARCHAR,
Phone VARCHAR);
CREATE TABLE dbo."Suppliers" (
SupplierID INTEGER,
CompanyName VARCHAR,
ContactName VARCHAR,
ContactTitle VARCHAR,
Address VARCHAR,
City VARCHAR,
Region VARCHAR,
PostalCode VARCHAR,
Country VARCHAR,
Phone VARCHAR,
Fax VARCHAR,
HomePage TEXT);
CREATE TABLE dbo."Orders" (
OrderID INTEGER,
CustomerID TEXT,
EmployeeID INTEGER,
OrderDate TIMESTAMP,
RequiredDate TIMESTAMP,
ShippedDate TIMESTAMP,
ShipVia INTEGER,
Freight varchar(200),
ShipName VARCHAR,
ShipAddress VARCHAR,
ShipCity VARCHAR,
ShipRegion VARCHAR,
ShipPostalCode VARCHAR,
ShipCountry VARCHAR);
CREATE TABLE dbo."Products" (
ProductID INTEGER,
ProductName VARCHAR,
SupplierID INTEGER,
CategoryID INTEGER,
QuantityPerUnit VARCHAR,
UnitPrice varchar(200),
UnitsInStock SMALLINT,
UnitsOnOrder SMALLINT,
ReorderLevel SMALLINT,
Discontinued varchar(200));
CREATE TABLE dbo."Order Details" (
OrderID INTEGER,
ProductID INTEGER,
UnitPrice varchar(200),
Quantity SMALLINT,
Discount REAL);
CREATE TABLE dbo."CustomerCustomerDemo" (
CustomerID TEXT,
CustomerTypeID TEXT);
CREATE TABLE dbo."CustomerDemographics" (
CustomerTypeID TEXT,
CustomerDesc TEXT);
CREATE TABLE dbo."Region" (
RegionID INTEGER,
RegionDescription TEXT);
CREATE TABLE dbo."Territories" (
TerritoryID VARCHAR,
TerritoryDescription TEXT,
RegionID INTEGER);
CREATE TABLE dbo."EmployeeTerritories" (
EmployeeID INTEGER,
TerritoryID VARCHAR);


CREATE UNIQUE INDEX  ON dbo."Employees" (EmployeeID);
CREATE INDEX  ON dbo."Employees" (LastName);
CREATE INDEX  ON dbo."Employees" (PostalCode);

CREATE UNIQUE INDEX  ON dbo."Categories" (CategoryID);
CREATE INDEX  ON dbo."Employees" (LastName);
CREATE INDEX  ON dbo."Employees" (PostalCode);
CREATE INDEX  ON dbo."Categories" (CategoryName);

CREATE UNIQUE INDEX  ON dbo."Customers" (CustomerID);
CREATE INDEX  ON dbo."Employees" (LastName);
CREATE INDEX  ON dbo."Employees" (PostalCode);
CREATE INDEX  ON dbo."Categories" (CategoryName);
CREATE INDEX  ON dbo."Customers" (City);
CREATE INDEX  ON dbo."Customers" (CompanyName);
CREATE INDEX  ON dbo."Customers" (PostalCode);
CREATE INDEX  ON dbo."Customers" (Region);

CREATE UNIQUE INDEX  ON dbo."Shippers" (ShipperID);
CREATE INDEX  ON dbo."Employees" (LastName);
CREATE INDEX  ON dbo."Employees" (PostalCode);
CREATE INDEX  ON dbo."Categories" (CategoryName);
CREATE INDEX  ON dbo."Customers" (City);
CREATE INDEX  ON dbo."Customers" (CompanyName);
CREATE INDEX  ON dbo."Customers" (PostalCode);
CREATE INDEX  ON dbo."Customers" (Region);

CREATE UNIQUE INDEX  ON dbo."Suppliers" (SupplierID);
CREATE INDEX  ON dbo."Employees" (LastName);
CREATE INDEX  ON dbo."Employees" (PostalCode);
CREATE INDEX  ON dbo."Categories" (CategoryName);
CREATE INDEX  ON dbo."Customers" (City);
CREATE INDEX  ON dbo."Customers" (CompanyName);
CREATE INDEX  ON dbo."Customers" (PostalCode);
CREATE INDEX  ON dbo."Customers" (Region);
CREATE INDEX  ON dbo."Suppliers" (CompanyName);
CREATE INDEX  ON dbo."Suppliers" (PostalCode);

CREATE UNIQUE INDEX  ON dbo."Orders" (OrderID);
CREATE INDEX  ON dbo."Employees" (LastName);
CREATE INDEX  ON dbo."Employees" (PostalCode);
CREATE INDEX  ON dbo."Categories" (CategoryName);
CREATE INDEX  ON dbo."Customers" (City);
CREATE INDEX  ON dbo."Customers" (CompanyName);
CREATE INDEX  ON dbo."Customers" (PostalCode);
CREATE INDEX  ON dbo."Customers" (Region);
CREATE INDEX  ON dbo."Suppliers" (CompanyName);
CREATE INDEX  ON dbo."Suppliers" (PostalCode);
CREATE INDEX  ON dbo."Orders" (CustomerID);
CREATE INDEX  ON dbo."Orders" (CustomerID);
CREATE INDEX  ON dbo."Orders" (EmployeeID);
CREATE INDEX  ON dbo."Orders" (EmployeeID);
CREATE INDEX  ON dbo."Orders" (OrderDate);
CREATE INDEX  ON dbo."Orders" (ShippedDate);
CREATE INDEX  ON dbo."Orders" (ShipVia);
CREATE INDEX  ON dbo."Orders" (ShipPostalCode);

CREATE UNIQUE INDEX  ON dbo."Products" (ProductID);
CREATE INDEX  ON dbo."Employees" (LastName);
CREATE INDEX  ON dbo."Employees" (PostalCode);
CREATE INDEX  ON dbo."Categories" (CategoryName);
CREATE INDEX  ON dbo."Customers" (City);
CREATE INDEX  ON dbo."Customers" (CompanyName);
CREATE INDEX  ON dbo."Customers" (PostalCode);
CREATE INDEX  ON dbo."Customers" (Region);
CREATE INDEX  ON dbo."Suppliers" (CompanyName);
CREATE INDEX  ON dbo."Suppliers" (PostalCode);
CREATE INDEX  ON dbo."Orders" (CustomerID);
CREATE INDEX  ON dbo."Orders" (CustomerID);
CREATE INDEX  ON dbo."Orders" (EmployeeID);
CREATE INDEX  ON dbo."Orders" (EmployeeID);
CREATE INDEX  ON dbo."Orders" (OrderDate);
CREATE INDEX  ON dbo."Orders" (ShippedDate);
CREATE INDEX  ON dbo."Orders" (ShipVia);
CREATE INDEX  ON dbo."Orders" (ShipPostalCode);
CREATE INDEX  ON dbo."Products" (CategoryID);
CREATE INDEX  ON dbo."Products" (CategoryID);
CREATE INDEX  ON dbo."Products" (ProductName);
CREATE INDEX  ON dbo."Products" (SupplierID);
CREATE INDEX  ON dbo."Products" (SupplierID);

CREATE UNIQUE INDEX  ON dbo."Order Details" (OrderID,ProductID);
CREATE INDEX  ON dbo."Employees" (LastName);
CREATE INDEX  ON dbo."Employees" (PostalCode);
CREATE INDEX  ON dbo."Categories" (CategoryName);
CREATE INDEX  ON dbo."Customers" (City);
CREATE INDEX  ON dbo."Customers" (CompanyName);
CREATE INDEX  ON dbo."Customers" (PostalCode);
CREATE INDEX  ON dbo."Customers" (Region);
CREATE INDEX  ON dbo."Suppliers" (CompanyName);
CREATE INDEX  ON dbo."Suppliers" (PostalCode);
CREATE INDEX  ON dbo."Orders" (CustomerID);
CREATE INDEX  ON dbo."Orders" (CustomerID);
CREATE INDEX  ON dbo."Orders" (EmployeeID);
CREATE INDEX  ON dbo."Orders" (EmployeeID);
CREATE INDEX  ON dbo."Orders" (OrderDate);
CREATE INDEX  ON dbo."Orders" (ShippedDate);
CREATE INDEX  ON dbo."Orders" (ShipVia);
CREATE INDEX  ON dbo."Orders" (ShipPostalCode);
CREATE INDEX  ON dbo."Products" (CategoryID);
CREATE INDEX  ON dbo."Products" (CategoryID);
CREATE INDEX  ON dbo."Products" (ProductName);
CREATE INDEX  ON dbo."Products" (SupplierID);
CREATE INDEX  ON dbo."Products" (SupplierID);
CREATE INDEX  ON dbo."Order Details" (OrderID);
CREATE INDEX  ON dbo."Order Details" (OrderID);
CREATE INDEX  ON dbo."Order Details" (ProductID);
CREATE INDEX  ON dbo."Order Details" (ProductID);

CREATE UNIQUE INDEX  ON dbo."CustomerCustomerDemo" (CustomerID,CustomerTypeID);
CREATE INDEX  ON dbo."Employees" (LastName);
CREATE INDEX  ON dbo."Employees" (PostalCode);
CREATE INDEX  ON dbo."Categories" (CategoryName);
CREATE INDEX  ON dbo."Customers" (City);
CREATE INDEX  ON dbo."Customers" (CompanyName);
CREATE INDEX  ON dbo."Customers" (PostalCode);
CREATE INDEX  ON dbo."Customers" (Region);
CREATE INDEX  ON dbo."Suppliers" (CompanyName);
CREATE INDEX  ON dbo."Suppliers" (PostalCode);
CREATE INDEX  ON dbo."Orders" (CustomerID);
CREATE INDEX  ON dbo."Orders" (CustomerID);
CREATE INDEX  ON dbo."Orders" (EmployeeID);
CREATE INDEX  ON dbo."Orders" (EmployeeID);
CREATE INDEX  ON dbo."Orders" (OrderDate);
CREATE INDEX  ON dbo."Orders" (ShippedDate);
CREATE INDEX  ON dbo."Orders" (ShipVia);
CREATE INDEX  ON dbo."Orders" (ShipPostalCode);
CREATE INDEX  ON dbo."Products" (CategoryID);
CREATE INDEX  ON dbo."Products" (CategoryID);
CREATE INDEX  ON dbo."Products" (ProductName);
CREATE INDEX  ON dbo."Products" (SupplierID);
CREATE INDEX  ON dbo."Products" (SupplierID);
CREATE INDEX  ON dbo."Order Details" (OrderID);
CREATE INDEX  ON dbo."Order Details" (OrderID);
CREATE INDEX  ON dbo."Order Details" (ProductID);
CREATE INDEX  ON dbo."Order Details" (ProductID);

CREATE UNIQUE INDEX  ON dbo."CustomerDemographics" (CustomerTypeID);
CREATE INDEX  ON dbo."Employees" (LastName);
CREATE INDEX  ON dbo."Employees" (PostalCode);
CREATE INDEX  ON dbo."Categories" (CategoryName);
CREATE INDEX  ON dbo."Customers" (City);
CREATE INDEX  ON dbo."Customers" (CompanyName);
CREATE INDEX  ON dbo."Customers" (PostalCode);
CREATE INDEX  ON dbo."Customers" (Region);
CREATE INDEX  ON dbo."Suppliers" (CompanyName);
CREATE INDEX  ON dbo."Suppliers" (PostalCode);
CREATE INDEX  ON dbo."Orders" (CustomerID);
CREATE INDEX  ON dbo."Orders" (CustomerID);
CREATE INDEX  ON dbo."Orders" (EmployeeID);
CREATE INDEX  ON dbo."Orders" (EmployeeID);
CREATE INDEX  ON dbo."Orders" (OrderDate);
CREATE INDEX  ON dbo."Orders" (ShippedDate);
CREATE INDEX  ON dbo."Orders" (ShipVia);
CREATE INDEX  ON dbo."Orders" (ShipPostalCode);
CREATE INDEX  ON dbo."Products" (CategoryID);
CREATE INDEX  ON dbo."Products" (CategoryID);
CREATE INDEX  ON dbo."Products" (ProductName);
CREATE INDEX  ON dbo."Products" (SupplierID);
CREATE INDEX  ON dbo."Products" (SupplierID);
CREATE INDEX  ON dbo."Order Details" (OrderID);
CREATE INDEX  ON dbo."Order Details" (OrderID);
CREATE INDEX  ON dbo."Order Details" (ProductID);
CREATE INDEX  ON dbo."Order Details" (ProductID);

CREATE UNIQUE INDEX  ON dbo."Region" (RegionID);
CREATE INDEX  ON dbo."Employees" (LastName);
CREATE INDEX  ON dbo."Employees" (PostalCode);
CREATE INDEX  ON dbo."Categories" (CategoryName);
CREATE INDEX  ON dbo."Customers" (City);
CREATE INDEX  ON dbo."Customers" (CompanyName);
CREATE INDEX  ON dbo."Customers" (PostalCode);
CREATE INDEX  ON dbo."Customers" (Region);
CREATE INDEX  ON dbo."Suppliers" (CompanyName);
CREATE INDEX  ON dbo."Suppliers" (PostalCode);
CREATE INDEX  ON dbo."Orders" (CustomerID);
CREATE INDEX  ON dbo."Orders" (CustomerID);
CREATE INDEX  ON dbo."Orders" (EmployeeID);
CREATE INDEX  ON dbo."Orders" (EmployeeID);
CREATE INDEX  ON dbo."Orders" (OrderDate);
CREATE INDEX  ON dbo."Orders" (ShippedDate);
CREATE INDEX  ON dbo."Orders" (ShipVia);
CREATE INDEX  ON dbo."Orders" (ShipPostalCode);
CREATE INDEX  ON dbo."Products" (CategoryID);
CREATE INDEX  ON dbo."Products" (CategoryID);
CREATE INDEX  ON dbo."Products" (ProductName);
CREATE INDEX  ON dbo."Products" (SupplierID);
CREATE INDEX  ON dbo."Products" (SupplierID);
CREATE INDEX  ON dbo."Order Details" (OrderID);
CREATE INDEX  ON dbo."Order Details" (OrderID);
CREATE INDEX  ON dbo."Order Details" (ProductID);
CREATE INDEX  ON dbo."Order Details" (ProductID);

CREATE UNIQUE INDEX  ON dbo."Territories" (TerritoryID);
CREATE INDEX  ON dbo."Employees" (LastName);
CREATE INDEX  ON dbo."Employees" (PostalCode);
CREATE INDEX  ON dbo."Categories" (CategoryName);
CREATE INDEX  ON dbo."Customers" (City);
CREATE INDEX  ON dbo."Customers" (CompanyName);
CREATE INDEX  ON dbo."Customers" (PostalCode);
CREATE INDEX  ON dbo."Customers" (Region);
CREATE INDEX  ON dbo."Suppliers" (CompanyName);
CREATE INDEX  ON dbo."Suppliers" (PostalCode);
CREATE INDEX  ON dbo."Orders" (CustomerID);
CREATE INDEX  ON dbo."Orders" (CustomerID);
CREATE INDEX  ON dbo."Orders" (EmployeeID);
CREATE INDEX  ON dbo."Orders" (EmployeeID);
CREATE INDEX  ON dbo."Orders" (OrderDate);
CREATE INDEX  ON dbo."Orders" (ShippedDate);
CREATE INDEX  ON dbo."Orders" (ShipVia);
CREATE INDEX  ON dbo."Orders" (ShipPostalCode);
CREATE INDEX  ON dbo."Products" (CategoryID);
CREATE INDEX  ON dbo."Products" (CategoryID);
CREATE INDEX  ON dbo."Products" (ProductName);
CREATE INDEX  ON dbo."Products" (SupplierID);
CREATE INDEX  ON dbo."Products" (SupplierID);
CREATE INDEX  ON dbo."Order Details" (OrderID);
CREATE INDEX  ON dbo."Order Details" (OrderID);
CREATE INDEX  ON dbo."Order Details" (ProductID);
CREATE INDEX  ON dbo."Order Details" (ProductID);

CREATE UNIQUE INDEX  ON dbo."EmployeeTerritories" (EmployeeID,TerritoryID);
CREATE INDEX  ON dbo."Employees" (LastName);
CREATE INDEX  ON dbo."Employees" (PostalCode);
CREATE INDEX  ON dbo."Categories" (CategoryName);
CREATE INDEX  ON dbo."Customers" (City);
CREATE INDEX  ON dbo."Customers" (CompanyName);
CREATE INDEX  ON dbo."Customers" (PostalCode);
CREATE INDEX  ON dbo."Customers" (Region);
CREATE INDEX  ON dbo."Suppliers" (CompanyName);
CREATE INDEX  ON dbo."Suppliers" (PostalCode);
CREATE INDEX  ON dbo."Orders" (CustomerID);
CREATE INDEX  ON dbo."Orders" (CustomerID);
CREATE INDEX  ON dbo."Orders" (EmployeeID);
CREATE INDEX  ON dbo."Orders" (EmployeeID);
CREATE INDEX  ON dbo."Orders" (OrderDate);
CREATE INDEX  ON dbo."Orders" (ShippedDate);
CREATE INDEX  ON dbo."Orders" (ShipVia);
CREATE INDEX  ON dbo."Orders" (ShipPostalCode);
CREATE INDEX  ON dbo."Products" (CategoryID);
CREATE INDEX  ON dbo."Products" (CategoryID);
CREATE INDEX  ON dbo."Products" (ProductName);
CREATE INDEX  ON dbo."Products" (SupplierID);
CREATE INDEX  ON dbo."Products" (SupplierID);
CREATE INDEX  ON dbo."Order Details" (OrderID);
CREATE INDEX  ON dbo."Order Details" (OrderID);
CREATE INDEX  ON dbo."Order Details" (ProductID);
CREATE INDEX  ON dbo."Order Details" (ProductID);

CREATE INDEX  ON dbo."Employees" (LastName);
CREATE INDEX  ON dbo."Employees" (PostalCode);
CREATE INDEX  ON dbo."Categories" (CategoryName);
CREATE INDEX  ON dbo."Customers" (City);
CREATE INDEX  ON dbo."Customers" (CompanyName);
CREATE INDEX  ON dbo."Customers" (PostalCode);
CREATE INDEX  ON dbo."Customers" (Region);
CREATE INDEX  ON dbo."Suppliers" (CompanyName);
CREATE INDEX  ON dbo."Suppliers" (PostalCode);
CREATE INDEX  ON dbo."Orders" (CustomerID);
CREATE INDEX  ON dbo."Orders" (CustomerID);
CREATE INDEX  ON dbo."Orders" (EmployeeID);
CREATE INDEX  ON dbo."Orders" (EmployeeID);
CREATE INDEX  ON dbo."Orders" (OrderDate);
CREATE INDEX  ON dbo."Orders" (ShippedDate);
CREATE INDEX  ON dbo."Orders" (ShipVia);
CREATE INDEX  ON dbo."Orders" (ShipPostalCode);
CREATE INDEX  ON dbo."Products" (CategoryID);
CREATE INDEX  ON dbo."Products" (CategoryID);
CREATE INDEX  ON dbo."Products" (ProductName);
CREATE INDEX  ON dbo."Products" (SupplierID);
CREATE INDEX  ON dbo."Products" (SupplierID);
CREATE INDEX  ON dbo."Order Details" (OrderID);
CREATE INDEX  ON dbo."Order Details" (OrderID);
CREATE INDEX  ON dbo."Order Details" (ProductID);
CREATE INDEX  ON dbo."Order Details" (ProductID);

ALTER TABLE dbo."Employees" ADD PRIMARY KEY (EmployeeID);
 ALTER TABLE dbo."Categories" ADD PRIMARY KEY (CategoryID);
 ALTER TABLE dbo."Customers" ADD PRIMARY KEY (CustomerID);
 ALTER TABLE dbo."Shippers" ADD PRIMARY KEY (ShipperID);
 ALTER TABLE dbo."Suppliers" ADD PRIMARY KEY (SupplierID);
 ALTER TABLE dbo."Orders" ADD PRIMARY KEY (OrderID);
 ALTER TABLE dbo."Products" ADD PRIMARY KEY (ProductID);
 ALTER TABLE dbo."Order Details" ADD PRIMARY KEY (OrderID,ProductID);
 ALTER TABLE dbo."CustomerCustomerDemo" ADD PRIMARY KEY (CustomerID,CustomerTypeID);
 ALTER TABLE dbo."CustomerDemographics" ADD PRIMARY KEY (CustomerTypeID);
 ALTER TABLE dbo."Region" ADD PRIMARY KEY (RegionID);
 ALTER TABLE dbo."Territories" ADD PRIMARY KEY (TerritoryID);
 ALTER TABLE dbo."EmployeeTerritories" ADD PRIMARY KEY (EmployeeID,TerritoryID);
 
ALTER TABLE dbo."Employees"  ADD FOREIGN KEY (ReportsTo) REFERENCES dbo."Employees";
ALTER TABLE dbo."Orders"  ADD FOREIGN KEY (CustomerID) REFERENCES dbo."Customers";
ALTER TABLE dbo."Orders"  ADD FOREIGN KEY (EmployeeID) REFERENCES dbo."Employees";
ALTER TABLE dbo."Orders"  ADD FOREIGN KEY (ShipVia) REFERENCES dbo."Shippers";
ALTER TABLE dbo."Products"  ADD FOREIGN KEY (SupplierID) REFERENCES dbo."Suppliers";
ALTER TABLE dbo."Products"  ADD FOREIGN KEY (CategoryID) REFERENCES dbo."Categories";
ALTER TABLE dbo."Order Details"  ADD FOREIGN KEY (OrderID) REFERENCES dbo."Orders";
ALTER TABLE dbo."Order Details"  ADD FOREIGN KEY (ProductID) REFERENCES dbo."Products";
ALTER TABLE dbo."CustomerCustomerDemo"  ADD FOREIGN KEY (CustomerID) REFERENCES dbo."Customers";
ALTER TABLE dbo."CustomerCustomerDemo"  ADD FOREIGN KEY (CustomerTypeID) REFERENCES dbo."CustomerDemographics";
ALTER TABLE dbo."Territories"  ADD FOREIGN KEY (RegionID) REFERENCES dbo."Region";
ALTER TABLE dbo."EmployeeTerritories"  ADD FOREIGN KEY (EmployeeID) REFERENCES dbo."Employees";
ALTER TABLE dbo."EmployeeTerritories"  ADD FOREIGN KEY (TerritoryID) REFERENCES dbo."Territories";

