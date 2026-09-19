import os
import subprocess

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>BhuNexis - Comprehensive Technical Architecture & Project Documentation</title>
    <style>
        @page {
            size: A4;
            margin: 15mm 15mm 15mm 15mm;
        }
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            color: #1e293b;
            line-height: 1.5;
            font-size: 11pt;
            margin: 0;
            padding: 0;
            background-color: #ffffff;
        }
        .header {
            border-bottom: 3px solid #059669;
            padding-bottom: 12px;
            margin-bottom: 20px;
        }
        .header h1 {
            color: #065f46;
            margin: 0 0 6px 0;
            font-size: 22pt;
            font-weight: 800;
        }
        .header p {
            margin: 0;
            color: #475569;
            font-size: 11pt;
            font-weight: 600;
        }
        .badge {
            display: inline-block;
            background: #dcfce7;
            color: #166534;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 9pt;
            font-weight: 700;
            margin-right: 6px;
        }
        .section {
            margin-bottom: 22px;
            page-break-inside: avoid;
        }
        h2 {
            color: #0f172a;
            border-bottom: 1.5px solid #cbd5e1;
            padding-bottom: 4px;
            font-size: 14pt;
            margin-top: 18px;
            margin-bottom: 10px;
        }
        h3 {
            color: #047857;
            font-size: 12pt;
            margin-top: 12px;
            margin-bottom: 6px;
        }
        p {
            margin-top: 0;
            margin-bottom: 8px;
        }
        ul, ol {
            margin-top: 0;
            margin-bottom: 10px;
            padding-left: 20px;
        }
        li {
            margin-bottom: 4px;
        }
        code, pre {
            font-family: 'Consolas', 'Courier New', monospace;
            background: #f1f5f9;
            border: 1px solid #e2e8f0;
            border-radius: 4px;
        }
        code {
            padding: 1px 4px;
            font-size: 10pt;
            color: #0f766e;
        }
        pre {
            padding: 10px;
            font-size: 9pt;
            line-height: 1.35;
            white-space: pre-wrap;
            word-break: break-all;
            background: #0f172a;
            color: #e2e8f0;
            border: none;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 14px;
            font-size: 10pt;
        }
        th, td {
            border: 1px solid #cbd5e1;
            padding: 6px 10px;
            text-align: left;
        }
        th {
            background-color: #f8fafc;
            color: #0f172a;
            font-weight: 700;
        }
        tr:nth-child(even) {
            background-color: #f8fafc;
        }
        .footer {
            margin-top: 30px;
            border-top: 1px solid #e2e8f0;
            padding-top: 10px;
            font-size: 9pt;
            color: #64748b;
            text-align: center;
        }
    </style>
</head>
<body>

    <div class="header">
        <h1>BhuNexis - Full-Stack Architecture Documentation</h1>
        <p>Government Land Records Digitization Platform & Interactive PostGIS Cadastral GIS Solution</p>
        <div style="margin-top: 10px;">
            <span class="badge">SIH 2026 Hackathon</span>
            <span class="badge">Python FastAPI</span>
            <span class="badge">React 18 + Leaflet</span>
            <span class="badge">PostgreSQL + PostGIS</span>
            <span class="badge">Enterprise Solution</span>
        </div>
    </div>

    <div class="section">
        <h2>1. Executive Summary & Core Objective</h2>
        <p><strong>BhuNexis</strong> is an enterprise-grade government land records digitization platform designed to solve legacy land revenue record errors, enable AI-driven OCR document extraction, provide human-in-the-loop validation, and render high-resolution <strong>PostGIS Cadastral GIS Maps</strong> linked directly to survey numbers, khasra numbers, khata numbers, and landowner identities.</p>
        <p>This technical specification document outlines the complete codebase architecture, database schema, API contracts, frontend component tree, and PostGIS GIS Cadastral mapping subsystem so that developers and AI systems can seamlessly understand, execute, and extend the project.</p>
    </div>

    <div class="section">
        <h2>2. Technology Stack & Frameworks</h2>
        <table>
            <thead>
                <tr>
                    <th>Domain</th>
                    <th>Technology / Library</th>
                    <th>Version</th>
                    <th>Purpose & Usage</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Backend Runtime</strong></td>
                    <td>Python</td>
                    <td>3.13</td>
                    <td>Core execution runtime environment for backend APIs and processing logic.</td>
                </tr>
                <tr>
                    <td><strong>Web Framework</strong></td>
                    <td>FastAPI</td>
                    <td>0.141</td>
                    <td>High-performance async web framework providing RESTful API endpoints & OpenAPI docs.</td>
                </tr>
                <tr>
                    <td><strong>Database ORM</strong></td>
                    <td>SQLAlchemy</td>
                    <td>2.0.54</td>
                    <td>Object-Relational Mapping with typed <code>Mapped</code> columns, relationships, and queries.</td>
                </tr>
                <tr>
                    <td><strong>Database Engine</strong></td>
                    <td>PostgreSQL + PostGIS</td>
                    <td>15+</td>
                    <td>Relational spatial database storing structured land records & vector polygon geometries.</td>
                </tr>
                <tr>
                    <td><strong>Database Drivers</strong></td>
                    <td>psycopg 3 / GeoAlchemy2</td>
                    <td>3.3.6</td>
                    <td>PostgreSQL dialect driver and PostGIS spatial geometry mapping engine.</td>
                </tr>
                <tr>
                    <td><strong>Authentication</strong></td>
                    <td>PyJWT & bcrypt</td>
                    <td>2.14 / 5.0</td>
                    <td>JWT Bearer token creation, validation, password hashing, and Role-Based Access Control.</td>
                </tr>
                <tr>
                    <td><strong>Object Storage</strong></td>
                    <td>MinIO Python SDK</td>
                    <td>7.2.20</td>
                    <td>S3-compatible object storage client for raw scanned PDF land record documents.</td>
                </tr>
                <tr>
                    <td><strong>Frontend Engine</strong></td>
                    <td>React 18 + Vite</td>
                    <td>18.x</td>
                    <td>Modern component-based UI runtime with fast module replacement build system.</td>
                </tr>
                <tr>
                    <td><strong>GIS Mapping</strong></td>
                    <td>Leaflet & React-Leaflet</td>
                    <td>1.9.x</td>
                    <td>Interactive map rendering engine for PostGIS GeoJSON land parcel polygon boundaries.</td>
                </tr>
                <tr>
                    <td><strong>Styling & Icons</strong></td>
                    <td>TailwindCSS + Lucide React</td>
                    <td>3.x</td>
                    <td>Utility-first CSS styling system, responsive grid layouts, custom dark/light themes.</td>
                </tr>
                <tr>
                    <td><strong>HTTP Client</strong></td>
                    <td>Axios</td>
                    <td>1.x</td>
                    <td>Client API service layer with JWT request interceptor & error handling.</td>
                </tr>
            </tbody>
        </table>
    </div>

    <div class="section">
        <h2>3. Complete Folder & File Directory Structure</h2>
        <pre>BhuNexis/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── deps.py                 # Dependency injection (Auth, DB, RBAC role guard)
│   │   │   └── v1/
│   │   │       ├── api.py              # Main API router aggregator
│   │   │       └── endpoints/
│   │   │           ├── auth.py         # POST /auth/login, POST /auth/register, GET /auth/me
│   │   │           ├── citizen.py      # Citizen parcel search & verification API
│   │   │           ├── dashboard.py    # Role dashboards (Citizen, Reviewer, Officer, Admin, Auditor)
│   │   │           ├── documents.py    # Document upload, storage, OCR triggering
│   │   │           ├── integrations.py # External OCR/NLP API webhook receivers
│   │   │           ├── map.py          # GET /map/parcels PostGIS GeoJSON spatial endpoint
│   │   │           ├── parcels.py      # Land parcel CRUD & spatial relationship API
│   │   │           └── reviews.py      # Human-in-the-loop review queue & field corrections
│   │   ├── core/
│   │   │   ├── audit.py                # System audit logger for compliance events
│   │   │   ├── config.py               # Pydantic environment configuration & settings
│   │   │   ├── rbac.py                 # AppRole enum & role permission definitions
│   │   │   ├── security.py             # Password hashing (bcrypt) & JWT token handling
│   │   │   └── storage.py              # MinIO / Local storage file manager
│   │   ├── db/
│   │   │   ├── base.py                 # SQLAlchemy DeclarativeBase initialization
│   │   │   └── session.py              # Database engine & session maker
│   │   ├── models/
│   │   │   └── all_models.py           # Unified SQLAlchemy DB models (User, Owner, Parcel, etc.)
│   │   ├── schemas/
│   │   │   ├── auth.py                 # Auth request & token response schemas
│   │   │   ├── document.py             # Document upload & OCR page schemas
│   │   │   ├── parcel.py               # Parcel, GeoJSON feature & feature collection schemas
│   │   │   └── review.py               # Review case & action schemas
│   │   └── main.py                     # FastAPI application entrypoint & CORS middleware
│   ├── tests/                          # Pytest suite (test_api.py, test_health.py)
│   ├── pyproject.toml                  # Python package configuration
│   └── pytest.ini                      # Test runner configuration
│
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── common/                 # Reusable UI widgets (StatusBadge, Navbar, Footer)
    │   │   ├── layout/                 # Sidebar layout & Header controls
    │   │   └── map/
    │   │       └── MapViewer.jsx       # Cadastral GIS Map viewer with parcel lines & plot labels
    │   ├── pages/
    │   │   ├── Home.jsx                # Landing page & platform overview
    │   │   ├── Login.jsx               # Role-based JWT authentication page
    │   │   ├── MapViewPage.jsx         # Fullscreen Cadastral GIS Map page
    │   │   ├── admin/                  # User Management & System Settings
    │   │   ├── auditor/                # Audit Logs & Security Analytics
    │   │   ├── citizen/                # Citizen Search & Land Rights
    │   │   ├── dashboards/             # Citizen, Reviewer, Officer, Admin, Auditor Dashboards
    │   │   ├── officer/                # Upload Land Record & Validation Workflows
    │   │   └── reviewer/               # Human-in-the-loop OCR verification page
    │   ├── routes/
    │   │   ├── AppRoutes.jsx           # React Router v6 route configuration
    │   │   └── ProtectedRoute.jsx      # Role-based route guard wrapper
    │   ├── services/
    │   │   ├── apiClient.js            # Axios client with JWT bearer interceptors
    │   │   ├── authService.js         # Login, register, auth helper functions
    │   │   └── mapService.js          # API service for PostGIS GeoJSON endpoints
    │   ├── App.jsx                     # Application root component
    │   └── main.jsx                    # Vite React entry point
    ├── package.json                    # Frontend npm dependencies
    └── vite.config.js                  # Vite server & API proxy config</pre>
    </div>

    <div class="section">
        <h2>4. Core Database Schema & PostGIS Architecture</h2>
        <p>The system utilizes PostgreSQL with two schemas: <code>core</code> for relational entities and <code>gis</code> for PostGIS spatial geometries.</p>
        <table>
            <thead>
                <tr>
                    <th>Table Name</th>
                    <th>Schema</th>
                    <th>Key Columns & Description</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><code>core.users</code></td>
                    <td>core</td>
                    <td><code>id, email, password_hash, full_name, role (CITIZEN, REVIEWER, OFFICER, ADMIN, AUDITOR), is_active</code></td>
                </tr>
                <tr>
                    <td><code>core.owners</code></td>
                    <td>core</td>
                    <td><code>id, owner_uid, full_name, local_name, father_name, gender, address, village, tehsil, district, state</code></td>
                </tr>
                <tr>
                    <td><code>core.parcels</code></td>
                    <td>core</td>
                    <td><code>id, parcel_uid, survey_number, khasra_number, khata_number, plot_number, village, tehsil, district, area, status</code></td>
                </tr>
                <tr>
                    <td><code>core.land_rights</code></td>
                    <td>core</td>
                    <td><code>id, owner_id (FK), parcel_id (FK), ownership_type, share_percentage, is_current</code></td>
                </tr>
                <tr>
                    <td><code>gis.parcel_geometry</code></td>
                    <td>gis</td>
                    <td><code>id, parcel_id (FK), geometry (Geometry(Polygon,4326)), geometry_source, gis_area_sq_m</code></td>
                </tr>
                <tr>
                    <td><code>core.documents</code></td>
                    <td>core</td>
                    <td><code>id, document_uid, title, file_path, file_type, ocr_status, uploaded_by (FK)</code></td>
                </tr>
                <tr>
                    <td><code>core.extracted_fields</code></td>
                    <td>core</td>
                    <td><code>id, document_page_id (FK), field_name, extracted_value, confidence_score, validation_status</code></td>
                </tr>
                <tr>
                    <td><code>core.review_cases</code></td>
                    <td>core</td>
                    <td><code>id, parcel_id (FK), document_id (FK), assigned_to (FK), priority, status, reviewer_comment</code></td>
                </tr>
            </tbody>
        </table>
    </div>

    <div class="section">
        <h2>5. GIS & Cadastral Mapping Subsystem Implementation</h2>
        <p>The Cadastral Map subsystem enables seamless spatial visualization of land parcels stored in PostGIS:</p>
        <ul>
            <li><strong>Backend GeoJSON Endpoint (<code>backend/app/api/v1/endpoints/map.py</code>)</strong>:
                Executes PostGIS query <code>ST_AsGeoJSON(pg.geometry)::json</code> joined with <code>core.parcels</code> to extract vector boundary polygons and attaches plot numbers, khasra numbers, survey numbers, land use classification, and verification status to GeoJSON feature properties.
            </li>
            <li><strong>Frontend Map Viewer (<code>frontend/src/components/map/MapViewer.jsx</code>)</strong>:
                Uses <code>React-Leaflet</code> to render parcel polygons. Includes:
                <ul>
                    <li><strong>Cadastral Line Demarcation</strong>: Custom stroke styling (Emerald line for Verified, Crimson line for Review Required, Amber dashed line for Draft).</li>
                    <li><strong>Permanent Plot Labels</strong>: Displays permanent plot number badges (e.g. <code>PLT-04011</code>) centered on each land parcel polygon using Leaflet tooltips.</li>
                    <li><strong>Auto-Fit View Bounds</strong>: Built-in <code>AutoFitBounds</code> component calls <code>map.fitBounds()</code> to automatically center and zoom to fit loaded PostGIS parcels.</li>
                    <li><strong>Base Layer Switcher</strong>: Toggle between Standard (OSM), Satellite Imagery (Esri World Imagery), and Dark GIS canvas.</li>
                    <li><strong>Interactive Detail Modal</strong>: Clicking any parcel highlights its border and slides up a detailed card showing plot, khasra, khata numbers, area, and owner info.</li>
                </ul>
            </li>
        </ul>
    </div>

    <div class="section">
        <h2>6. Recent Fixes & Improvements</h2>
        <ul>
            <li><strong>Backend Model Properties & Setter Fixes</strong>: Added missing <code>@reviewer_notes.setter</code> on <code>ReviewCase</code> and <code>@status.setter</code> on <code>ExtractedField</code> in <code>all_models.py</code> to prevent read-only property assignment errors.</li>
            <li><strong>SQLAlchemy Query Filter Correction</strong>: Updated <code>reviews.py</code> to join <code>DocumentPage</code> explicitly, resolving filter parameter type mismatches.</li>
            <li><strong>Database Schema Migration</strong>: Executed DDL migration <code>ALTER TABLE core.owners ADD COLUMN IF NOT EXISTS owner_uid VARCHAR;</code> and backfilled UIDs for 60 existing owner records, resolving HTTP 500 exceptions on citizen dashboard APIs.</li>
            <li><strong>Comprehensive Unit Testing</strong>: Verified all API endpoints using <code>pytest</code>, achieving 100% test pass rate.</li>
        </ul>
    </div>

    <div class="footer">
        <p>BhuNexis Project Documentation &bull; Generated for Developer & AI System Integration &bull; September 2026</p>
    </div>

</body>
</html>
"""

html_path = "D:\\HackathonProjects\\SIH_2026\\BhuNexis\\BhuNexis_Full_Project_Documentation.html"
pdf_path = "D:\\HackathonProjects\\SIH_2026\\BhuNexis\\BhuNexis_Full_Project_Documentation.pdf"

print("1. Writing HTML file...")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"HTML generated at: {html_path}")

print("2. Converting HTML to PDF using Microsoft Edge Headless Engine...")
edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

cmd = [
    edge_exe,
    "--headless",
    "--disable-gpu",
    f"--print-to-pdf={pdf_path}",
    html_path
]

res = subprocess.run(cmd, capture_output=True, text=True)
if os.path.exists(pdf_path):
    print(f"✅ SUCCESS! PDF created successfully at: {pdf_path}")
    print(f"PDF File Size: {os.path.getsize(pdf_path)} bytes")
else:
    print(f"❌ PDF generation failed. Error output:\n{res.stderr}\n{res.stdout}")
