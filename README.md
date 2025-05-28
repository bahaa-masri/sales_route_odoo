# 📦 Sales Route Planning and Monitoring System

## 🏢 Company Name (Optional)
**Global Distributors**

## 📖 Project Description
A system for planning and monitoring sales representatives’ visits to customers. 
It allows managers to create routes, assign salespersons, define regions and customers, and track inventory status during visits.
All data is visualized through a clear and intuitive dashboard.

## 🛠️ Installation and Setup Steps

1. Copy the module folder to the Odoo `addons` directory.
2. Update the apps list in Odoo by going to Apps → Update Apps List.
3. Install the module named **Sales Route Planning**.
4. Assign users to the appropriate groups for access rights:
   - Assign **Sales Manager** group to managers.
   - Assign **Salesperson** group to sales representatives.
5. Make sure managers are **not** assigned the group **Sales / User: Own Documents Only**, as it may restrict access.

## 👥 User Roles and Permissions

- **Sales Manager**: Can create routes, assign salespersons, define regions and customers, and access the dashboard.
- **Salesperson**: Can view and log their daily visits and see visit details.

## 📋 Available Menus

After installing the module, you will find the following menus in Odoo:

- **Dashboard**
  - **Visit Summary**
  - **Inventory Status**
  - **Route Overview**
- **Routes**
  - **All Routes**
- **Customer Visits**
  - **All Visits**
- **Sales Representatives**
  - **All Representatives**
- **Inventory Monitoring**
  - **Customer Inventory**
- **Customer Management**
  - **Customers**
- **Manage Regions**
  - **Regions**
