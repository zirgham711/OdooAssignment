# Real Estate Management System

## Overview
The Real Estate Management System is an Odoo module designed to manage real estate properties, their sales, and related offers. This module is developed for use within the Odoo ERP system and allows users to efficiently manage various aspects of real estate properties.

## Features
- Property Management: Create, view, and manage real estate properties with details such as title, description, postcode, availability, expected price, selling price, bedrooms, living area, facades, garage, and garden information.
- Status Tracking: Properties can have three main statuses - New, Canceled, and Sold. The status helps track the progress of the property through the sales process.
- Property Tags: Categorize properties using tags for better organization and searchability.
- Offers Management: Keep track of offers made for each property and their status (accepted or pending).
- Invoice Generation: Automatically generate invoices for sold properties, including buyer information, property details, and selling price.
- Data Validation: Implement various data validations to ensure data integrity, such as checking that expected prices and selling prices are positive, and that a sold property cannot be canceled, and vice versa.
- User-Friendly Interface: Designed with a user-friendly interface for easy navigation and efficient data entry.

## Requirements
- Odoo 16.0
- Python 3.x

## Installation
1. Clone this repository to your Odoo addons directory.
2. Restart the Odoo server.
3. Install the "Real Estate Management" module from the Odoo Apps menu.
4. Configure the module settings as needed in Odoo.

## Usage
1. Go to the "Properties" menu to create, view, and manage real estate properties.
2. Manage property tags from the "Property Tags" menu.
3. View and manage offers from the "Property Offers" menu.
4. Users can cancel or mark a property as sold from the property form view using the corresponding buttons.
5. Invoices will be generated automatically for sold properties.
