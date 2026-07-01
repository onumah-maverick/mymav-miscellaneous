# mymav-miscellaneous

## Overview

This repository contains a small set of standalone scripts used for:

* CRM integration (Zoho)
* Visit scheduling logic for field operations
* OpenAI Assistants + Code Interpreter experimentation
* Lightweight SQL update operations for the Mymav application

These scripts are **non-production utilities**, primarily intended for reference, prototyping, and handover documentation.

---

# ⚠️ General Notes

* API credentials are intentionally removed
* All integrations require external environment/config setup
* Scripts are independent (no shared architecture)
* Some logic is hardcoded for testing purposes
* Not production-hardened

---

# 1. 🔌 Zoho CRM Integration (Lead Creation Script - PHP)

## Purpose

Simple PHP script that:

* Generates OAuth access token using refresh token
* Sends a test Lead record to Zoho CRM

---

## Flow

1. Uses OAuth refresh token to generate access token
2. Builds a Lead payload (test/static structure)
3. Sends POST request to Zoho CRM `/crm/v2/Leads`
4. Prints API response

---

## Configuration (Sensitive Fields Removed)

```php id="9xqk2a"
$client_id = '';
$client_secret = '';
$refresh_token = '';
$redirect_uri = 'https://flatbuffer.com/mav';
$zoho_domain = 'https://www.zohoapis.com';
```

---

## Lead Payload (Example Structure)

* First_Name
* Last_Name
* Phone
* Email
* Company
* Description
* Lead_Source

---

## Notes

* Access token is generated at runtime via refresh token
* No persistent token storage
* Hardcoded test lead used for validation only
* Zoho endpoint region may need adjustment (.eu / .in depending on org)

---

# 2. 📊 Visit Scheduling Logic (Surveyor Visit Planner)

## Purpose

Generates next visit dates for surveyors based on:

* Historical visit date
* Country-specific public holidays
* Weekday/weekend constraints
* Daily visit capacity limits per surveyor

---

## Core Logic

* Builds valid date candidates within a fixed window (May 2026)
* Excludes weekends and public holidays
* Assigns visits sequentially per surveyor
* Enforces max **4 visits per surveyor per day**
* Falls back to later dates if no slot is available

---

## Countries Supported

* Ghana
* Côte d’Ivoire
* Cameroon

---

## Output

Adds:

* `Next_Visit_Date`

---

## Notes

* Scheduling window is hardcoded (May 5–25, 2026)
* No integration with real calendar systems

---

# 3. 🤖 OpenAI Assistants + Streamlit Chat App

## Purpose

Streamlit-based chat interface for testing:

* OpenAI Assistants API
* Code Interpreter
* Vector store retrieval
* Thread-based conversation handling

---

## Key Features

* Persistent chat UI using Streamlit session state
* OpenAI thread per session
* Assistant runs triggered per user message
* Vector store search used to retrieve relevant file context
* Files attached dynamically to Code Interpreter tool

---

## Environment Variables

```env id="p0k8vz"
OPENAI_API_KEY=
assistant_id=
vector_store_id=
```

---

## Flow

1. User sends message
2. Message appended to OpenAI thread
3. Vector store searched for relevant files
4. Assistant updated with retrieved file IDs
5. Run executed and polled
6. Assistant response extracted and displayed

---

## Notes

* Assistant is updated on every request (can be optimized)
* Duplicate message insertion exists in current implementation
* No error handling implemented
* Experimental / prototype-level integration

---

# 4. 🗄️ SQL Update Script (Mymav App)

## Purpose

Simple SQL utility script used for:

* Updating records in the Mymav application
* Supporting small-scale data corrections and maintenance tasks

---

## Notes

* Not a full pipeline or ETL system
* Used for targeted updates only
* Should be reviewed before execution in production environments

---

# 📌 Repository Summary

This repository acts as a **miscellaneous toolkit** containing:

* CRM API integration (Zoho)
* Field visit scheduling logic
* OpenAI Assistants experimentation (Streamlit)
* SQL update utilities for Mymav app support

---

# 🧾 Final Notes

* Scripts are independent and not architected as a system
* Intended for reference, debugging, and handover clarity
* Sensitive credentials removed
* Some logic is hardcoded for prototyping purposes

---
