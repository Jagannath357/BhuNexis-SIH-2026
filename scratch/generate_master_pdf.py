import os
import subprocess

# Ensure docs directory exists
os.makedirs("D:\\HackathonProjects\\SIH_2026\\BhuNexis\\docs", exist_ok=True)

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>BhuNexis — Complete Technical Project Documentation</title>
    <style>
        @page {
            size: A4;
            margin: 12mm 15mm 15mm 15mm;
            @bottom-right {
                content: counter(page);
            }
        }
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            color: #0f172a;
            line-height: 1.45;
            font-size: 10pt;
            margin: 0;
            padding: 0;
            background-color: #ffffff;
        }
        .header {
            border-bottom: 3px solid #059669;
            padding-bottom: 10px;
            margin-bottom: 18px;
        }
        .header h1 {
            color: #065f46;
            margin: 0 0 4px 0;
            font-size: 20pt;
            font-weight: 800;
            letter-spacing: -0.5px;
        }
        .header .subtitle {
            color: #0284c7;
            font-size: 12pt;
            font-weight: 700;
            margin: 0 0 6px 0;
        }
        .header .meta {
            margin: 0;
            color: #475569;
            font-size: 9pt;
            font-weight: 600;
        }
        .badge {
            display: inline-block;
            background: #dcfce7;
            color: #166534;
            padding: 2px 7px;
            border-radius: 4px;
            font-size: 8.5pt;
            font-weight: 700;
            margin-right: 5px;
            border: 1px solid #bbf7d0;
        }
        .badge-impl {
            background: #dcfce7;
            color: #15803d;
            border: 1px solid #86efac;
        }
        .badge-prep {
            background: #e0f2fe;
            color: #0369a1;
            border: 1px solid #7dd3fc;
        }
        .badge-plan {
            background: #fef3c7;
            color: #b45309;
            border: 1px solid #fcd34d;
        }
        .section {
            margin-bottom: 20px;
        }
        h2 {
            color: #0f172a;
            border-bottom: 1.5px solid #059669;
            padding-bottom: 4px;
            font-size: 13pt;
            margin-top: 18px;
            margin-bottom: 8px;
            font-weight: 700;
        }
        h3 {
            color: #047857;
            font-size: 11pt;
            margin-top: 12px;
            margin-bottom: 6px;
            font-weight: 700;
        }
        p {
            margin-top: 0;
            margin-bottom: 6px;
        }
        ul, ol {
            margin-top: 0;
            margin-bottom: 8px;
            padding-left: 18px;
        }
        li {
            margin-bottom: 3px;
        }
        code, pre {
            font-family: 'Consolas', 'Courier New', monospace;
            background: #f1f5f9;
            border: 1px solid #e2e8f0;
            border-radius: 4px;
        }
        code {
            padding: 1px 4px;
            font-size: 9.5pt;
            color: #0f766e;
        }
        pre {
            padding: 8px 10px;
            font-size: 8.5pt;
            line-height: 1.3;
            white-space: pre-wrap;
            word-break: break-all;
            background: #0f172a;
            color: #f8fafc;
            border: none;
            border-radius: 6px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 12px;
            font-size: 9.5pt;
        }
        th, td {
            border: 1px solid #cbd5e1;
            padding: 5px 8px;
            text-align: left;
            vertical-align: top;
        }
        th {
            background-color: #f1f5f9;
            color: #0f172a;
            font-weight: 700;
        }
        tr:nth-child(even) {
            background-color: #f8fafc;
        }
        .callout {
            background-color: #f0fdf4;
            border-left: 4px solid #10b981;
            padding: 8px 12px;
            margin-bottom: 10px;
            border-radius: 0 6px 6px 0;
            font-size: 9.5pt;
        }
        .callout-warn {
            background-color: #fffbeb;
            border-left: 4px solid #f59e0b;
            padding: 8px 12px;
            margin-bottom: 10px;
            border-radius: 0 6px 6px 0;
            font-size: 9.5pt;
        }
        .footer {
            margin-top: 25px;
            border-top: 1px solid #cbd5e1;
            padding-top: 8px;
            font-size: 8.5pt;
            color: #64748b;
            text-align: center;
        }
    </style>
</head>
<body>

    <!-- Title & Header -->
    <div class="header">
        <h1>BhuNexis</h1>
        <div class="subtitle">AI-Powered Land Record Digitization & Validation Platform</div>
        <p class="meta">Master Technical Project Documentation &bull; Source of Truth Reference &bull; Generated: September 19, 2026</p>
        <div style="margin-top: 8px;">
            <span class="badge">SIH 2026 Hackathon</span>
            <span class="badge">Python 3.13 + FastAPI</span>
            <span class="badge">React 18 + Vite + Leaflet</span>
            <span class="badge">PostgreSQL 15 + PostGIS</span>
            <span class="badge">MinIO S3 Storage</span>
        </div>
    </div>

    <!-- Section 1: Executive Summary -->
    <div class="section">
        <h2>1. Executive Summary & Problem Statement</h2>
        <p><strong>BhuNexis</strong> is an enterprise-grade government land records digitization and validation platform designed to solve systemic challenges in legacy land administration systems. Historical land revenue records (such as Khata, Khasra, Jamabandi, and Mutation register documents) primarily exist as unindexed scanned PDFs, physical paper archives, handwritten records, and low-resolution images containing complex tabular data.</p>
        <p><strong>Core Objective:</strong> Transform unstructured, unvalidated physical and scanned land records into structured, AI-extracted, rule-validated, spatially cross-referenced, and fully auditable digital land records backed by PostGIS spatial boundaries and human-in-the-loop review queues.</p>

        <h3>End-to-End Processing Pipeline:</h3>
        <div class="callout">
            Document Upload (PDF/Image) &rarr; MinIO Storage &rarr; Preprocessing & Page Extraction &rarr; OCR Text & Bounding Box Detection &rarr; NLP Entity Extraction & Normalization &rarr; Multi-Rule Validation Engine &rarr; GIS Spatial Cross-Reference &rarr; Human-in-the-Loop Review Queue &rarr; Final Record Verification &rarr; PostgreSQL / PostGIS Spatial Persistence &rarr; Citizen & GIS Access
        </div>
    </div>

    <!-- Section 2: Architecture -->
    <div class="section">
        <h2>2. High-Level Architecture Overview</h2>
        <p>BhuNexis follows a modern, decoupled micro-architecture separating presentation, core API orchestration, object storage, spatial data persistence, and specialized AI processing engines.</p>
        <pre>
+-----------------------------------------------------------------------------------+
|                            REACT 18 FRONTEND (Vite + Tailwind)                    |
|       [Admin /a/*]   [Officer /o/*]   [Reviewer /r/*]   [Auditor /au/*]   [Citizen /u/*] |
+-----------------------------------------------------------------------------------+
                                         |
                                (HTTP / REST + Bearer JWT)
                                         v
+-----------------------------------------------------------------------------------+
|                             FASTAPI BACKEND ROUTER (/api/v1)                      |
|   +-------------------+   +--------------------+   +--------------------------+   |
|   |  JWT Auth & RBAC  |   | Audit Event Logger |   | Document Storage Service |   |
|   +-------------------+   +--------------------+   +--------------------------+   |
+-----------------------------------------------------------------------------------+
       |                    |                    |                   |
       v                    v                    v                   v
+--------------+    +----------------+    +--------------+    +---------------------+
| PostgreSQL 15|    | PostGIS (gis)  |    | MinIO S3     |    | Prepared AI Interfaces |
| (core schema)|    | Parcel Geometry|    | Object Store |    |  - OCR JSON Interface  |
|  - Users     |    |  - Polygons    |    |  - PDF Files |    |  - NLP Normalizer   |
|  - Owners    |    |  - SRID 4326   |    |  - Pages     |    |  - Validation Engine|
|  - Parcels   |    |  - GIST Index  |    |  - Presigned |    +---------------------+
+--------------+    +----------------+    +--------------+
        </pre>
    </div>

    <!-- Section 3: Project Folder Structure -->
    <div class="section">
        <h2>3. Complete Repository Directory Structure</h2>
        <pre>
BhuNexis/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── deps.py                 # FastAPI Dependency Injection (Auth, DB, RBAC)
│   │   │   └── v1/
│   │   │       ├── api.py              # Central API Router Aggregator
│   │   │       └── endpoints/
│   │   │           ├── audit.py        # Audit Event Analytics & Logs API
│   │   │           ├── auth.py         # Login, Register, Refresh Token API
│   │   │           ├── citizen.py      # Citizen Parcel Search & Verification API
│   │   │           ├── dashboard.py    # Role Dashboards (Admin, Officer, Reviewer, Auditor, Citizen)
│   │   │           ├── documents.py    # Document Upload, Status, & File Download API
│   │   │           ├── health.py       # System Health Check API
│   │   │           ├── integrations.py # OCR/NLP External Webhook Listeners
│   │   │           ├── map.py          # GET /map/parcels PostGIS GeoJSON Spatial API
│   │   │           ├── parcels.py      # Parcel CRUD & Owner Linkage API
│   │   │           ├── profile.py      # User Profile Management API
│   │   │           ├── reviews.py      # Human Review Queue & Field Correction API
│   │   │           ├── settings.py     # System Configuration & OCR Threshold API
│   │   │           ├── users.py        # Admin User Management API
│   │   │           └── validations.py  # Rule Validation Trigger & Results API
│   │   ├── core/
│   │   │   ├── audit.py                # Audit Logging Dispatcher
│   │   │   ├── config.py               # Pydantic Settings & Environment Variables
│   │   │   ├── rbac.py                 # AppRole Enum & Permissions Matrix
│   │   │   ├── security.py             # Bcrypt Password Hashing & JWT Token Utility
│   │   │   └── storage.py              # MinIO Object Storage Manager
│   │   ├── db/
│   │   │   ├── base.py                 # SQLAlchemy DeclarativeBase
│   │   │   └── session.py              # DB Engine & Session Maker
│   │   ├── models/
│   │   │   └── all_models.py           # Unified SQLAlchemy DB Models (14 Tables)
│   │   ├── schemas/
│   │   │   ├── auth.py                 # Login & Token Pydantic Schemas
│   │   │   ├── document.py             # Document Upload & Extracted Field Schemas
│   │   │   ├── parcel.py               # Parcel & GeoJSON Feature Schemas
│   │   │   └── review.py               # Review Case & Correction Schemas
│   │   └── main.py                     # FastAPI Application Initialization & CORS
│   ├── tests/
│   │   ├── test_api.py                 # API Endpoint Integration Test Suite
│   │   └── test_health.py              # Health Check Test Suite
│   ├── pyproject.toml                  # Python Dependencies & Package Metadata
│   └── pytest.ini                      # Pytest Runner Configuration
│
├── database/                           # Prepared Schema Migration & SQL Seeds
├── docs/                               # Project Technical Documentation PDFs
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/                 # StatusBadge, AccessDenied, Navbar, Footer
│   │   │   ├── layout/                 # Sidebar & Main App Header Controls
│   │   │   └── map/
│   │   │       └── MapViewer.jsx       # Cadastral GIS Map (Leaflet + AutoFit + Plot Labels)
│   │   ├── pages/
│   │   │   ├── Home.jsx                # Platform Overview & Workflow Landing Page
│   │   │   ├── Login.jsx               # Role-Based Authentication Interface
│   │   │   ├── MapViewPage.jsx         # Fullscreen Cadastral GIS Map Page
│   │   │   ├── ProfilePage.jsx         # User Profile & Security Settings
│   │   │   ├── SignUp.jsx              # Citizen Self-Registration Page
│   │   │   ├── UploadDocumentPage.jsx  # Officer Bulk Document Upload Interface
│   │   │   ├── admin/                  # UserManagement.jsx, SystemSettings.jsx
│   │   │   ├── auditor/                # AuditLogsPage.jsx
│   │   │   ├── citizen/                # CitizenSearch.jsx
│   │   │   ├── dashboards/             # Admin, Officer, Reviewer, Auditor, Citizen Dashboards
│   │   │   └── reviewer/               # HumanReviewPage.jsx
│   │   ├── routes/
│   │   │   ├── AppRoutes.jsx           # React Router v6 Route Definitions
│   │   │   └── ProtectedRoute.jsx      # Role Guard Route Wrapper
│   │   ├── services/
│   │   │   ├── apiClient.js            # Axios Instance with JWT Interceptor
│   │   │   ├── authService.js         # Auth API Service
│   │   │   └── mapService.js          # Cadastral GIS Map API Service
│   │   ├── App.jsx                     # Application Root Component
│   │   └── main.jsx                    # Vite React Entrypoint
│   ├── package.json                    # Frontend NPM Dependencies
│   └── vite.config.js                  # Vite Server & Backend Proxy Settings
│
├── nlp/                                # Prepared NLP Entity Extraction Module Interface
├── ocr/                                # Prepared OCR Processing Pipeline Interface
└── validation/                         # Prepared Multi-Rule Validation Engine Interface
        </pre>
    </div>

    <!-- Section 4 & 5: Frontend & Page Flow -->
    <div class="section">
        <h2>4. Frontend Architecture & Page Routing Flow</h2>
        <p>The frontend is built with React 18, Vite, and TailwindCSS using a Role-Based Access Control routing model.</p>
        
        <h3>Role-Based Route Table:</h3>
        <table>
            <thead>
                <tr>
                    <th>Role</th>
                    <th>Dashboard Route</th>
                    <th>Feature Routes</th>
                    <th>Access Permissions</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><span class="badge badge-impl">ADMIN</span></td>
                    <td><code>/a/dashboard</code></td>
                    <td><code>/a/users</code>, <code>/a/settings</code>, <code>/map</code>, <code>/profile</code></td>
                    <td>Full system administrative access, user management, global settings, audit logs.</td>
                </tr>
                <tr>
                    <td><span class="badge badge-impl">OFFICER</span></td>
                    <td><code>/o/dashboard</code></td>
                    <td><code>/o/upload</code>, <code>/map</code>, <code>/profile</code></td>
                    <td>Document upload, batch ingestion, document status monitoring.</td>
                </tr>
                <tr>
                    <td><span class="badge badge-impl">REVIEWER</span></td>
                    <td><code>/r/dashboard</code></td>
                    <td><code>/r/review</code>, <code>/map</code>, <code>/profile</code></td>
                    <td>Human review queue, side-by-side OCR field correction, approve/reject land cases.</td>
                </tr>
                <tr>
                    <td><span class="badge badge-impl">AUDITOR</span></td>
                    <td><code>/au/dashboard</code></td>
                    <td><code>/au/audit</code>, <code>/map</code>, <code>/profile</code></td>
                    <td>Read-only compliance audit history, system analytics, event timeline tracking.</td>
                </tr>
                <tr>
                    <td><span class="badge badge-impl">CITIZEN</span></td>
                    <td><code>/u/dashboard</code></td>
                    <td><code>/u/search</code>, <code>/map</code>, <code>/profile</code></td>
                    <td>Read-only verified parcel search, land ownership records lookup, GIS map view.</td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- Section 6: RBAC -->
    <div class="section">
        <h2>5. Role-Based Access Control (RBAC) Specification</h2>
        <p>BhuNexis enforces RBAC at both the frontend React routing layer (via <code>ProtectedRoute.jsx</code>) and backend FastAPI dependency layer (via <code>require_roles()</code> in <code>deps.py</code>).</p>
        <table>
            <thead>
                <tr>
                    <th>Capability</th>
                    <th>ADMIN</th>
                    <th>OFFICER</th>
                    <th>REVIEWER</th>
                    <th>AUDITOR</th>
                    <th>CITIZEN</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Upload Land Documents</td><td>YES</td><td>YES</td><td>NO</td><td>NO</td><td>NO</td></tr>
                <tr><td>Human Review & Field Edit</td><td>YES</td><td>NO</td><td>YES</td><td>NO</td><td>NO</td></tr>
                <tr><td>View Audit Logs & Analytics</td><td>YES</td><td>NO</td><td>NO</td><td>YES</td><td>NO</td></tr>
                <tr><td>User Management & Settings</td><td>YES</td><td>NO</td><td>NO</td><td>NO</td><td>NO</td></tr>
                <tr><td>Search Verified Records & GIS Map</td><td>YES</td><td>YES</td><td>YES</td><td>YES</td><td>YES</td></tr>
            </tbody>
        </table>
    </div>

    <!-- Section 9-12: Backend Architecture & API Table -->
    <div class="section">
        <h2>6. Backend API Architecture & Endpoints</h2>
        <p>The backend is built using FastAPI (Python 3.13) with SQLAlchemy 2.0 ORM, PostgreSQL + PostGIS, and MinIO S3 Object Storage.</p>
        
        <h3>Implemented FastAPI Endpoint Registry:</h3>
        <table>
            <thead>
                <tr>
                    <th>Method</th>
                    <th>Endpoint</th>
                    <th>Purpose</th>
                    <th>Allowed Roles</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>POST</td><td><code>/api/v1/auth/login</code></td><td>Authenticate user & issue JWT Bearer Token</td><td>Public</td><td><span class="badge badge-impl">IMPLEMENTED</span></td></tr>
                <tr><td>POST</td><td><code>/api/v1/auth/register</code></td><td>Register citizen account</td><td>Public</td><td><span class="badge badge-impl">IMPLEMENTED</span></td></tr>
                <tr><td>GET</td><td><code>/api/v1/auth/me</code></td><td>Get current authenticated user profile</td><td>All Roles</td><td><span class="badge badge-impl">IMPLEMENTED</span></td></tr>
                <tr><td>POST</td><td><code>/api/v1/documents/upload</code></td><td>Upload document PDF/Image to MinIO & record in DB</td><td>OFFICER, ADMIN</td><td><span class="badge badge-impl">IMPLEMENTED</span></td></tr>
                <tr><td>GET</td><td><code>/api/v1/documents</code></td><td>List uploaded documents with status filters</td><td>OFFICER, ADMIN, REVIEWER</td><td><span class="badge badge-impl">IMPLEMENTED</span></td></tr>
                <tr><td>GET</td><td><code>/api/v1/map/parcels</code></td><td>Query PostGIS spatial parcels as GeoJSON FeatureCollection</td><td>All Roles</td><td><span class="badge badge-impl">IMPLEMENTED</span></td></tr>
                <tr><td>GET</td><td><code>/api/v1/reviews</code></td><td>Fetch human review queue items</td><td>REVIEWER, ADMIN</td><td><span class="badge badge-impl">IMPLEMENTED</span></td></tr>
                <tr><td>PATCH</td><td><code>/api/v1/reviews/{id}</code></td><td>Submit corrected OCR field value</td><td>REVIEWER</td><td><span class="badge badge-impl">IMPLEMENTED</span></td></tr>
                <tr><td>POST</td><td><code>/api/v1/reviews/{id}/approve</code></td><td>Approve review case & mark verified</td><td>REVIEWER</td><td><span class="badge badge-impl">IMPLEMENTED</span></td></tr>
                <tr><td>POST</td><td><code>/api/v1/reviews/{id}/reject</code></td><td>Reject review case</td><td>REVIEWER</td><td><span class="badge badge-impl">IMPLEMENTED</span></td></tr>
                <tr><td>GET</td><td><code>/api/v1/dashboard/citizen</code></td><td>Get citizen dashboard land records summary</td><td>CITIZEN, ADMIN</td><td><span class="badge badge-impl">IMPLEMENTED</span></td></tr>
                <tr><td>GET</td><td><code>/api/v1/audit/logs</code></td><td>Fetch system audit trail logs & analytics</td><td>AUDITOR, ADMIN</td><td><span class="badge badge-impl">IMPLEMENTED</span></td></tr>
                <tr><td>POST</td><td><code>/api/v1/integrations/ocr-webhook</code></td><td>Receive OCR/NLP service extraction payload</td><td>System Integration</td><td><span class="badge badge-prep">PREPARED</span></td></tr>
            </tbody>
        </table>
    </div>

    <!-- Section 16-18: Database & PostGIS -->
    <div class="section">
        <h2>7. Complete Database Schema (PostgreSQL + PostGIS)</h2>
        <p>The database <code>bhunexis</code> utilizes PostgreSQL 15 with two schemas: <code>core</code> for structured business entities and <code>gis</code> for PostGIS spatial geometries.</p>
        
        <h3>Database Table Definitions (14 Tables):</h3>
        <table>
            <thead>
                <tr>
                    <th>Table Name</th>
                    <th>Schema</th>
                    <th>Primary Columns & Foreign Keys</th>
                    <th>Description</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><code>users</code></td><td>core</td><td><code>id, email, password_hash, full_name, role</code></td><td>User credentials and RBAC authorization roles.</td></tr>
                <tr><td><code>owners</code></td><td>core</td><td><code>id, owner_uid, full_name, father_name, village, district</code></td><td>Landowner registry profiles.</td></tr>
                <tr><td><code>parcels</code></td><td>core</td><td><code>id, parcel_uid, survey_number, khasra_number, khata_number, plot_number, area, status</code></td><td>Land parcel record registry.</td></tr>
                <tr><td><code>land_rights</code></td><td>core</td><td><code>id, owner_id (FK), parcel_id (FK), ownership_type, share_percentage</code></td><td>Ownership share linkage mapping owners to parcels.</td></tr>
                <tr><td><code>parcel_geometry</code></td><td>gis</td><td><code>id, parcel_id (FK), geometry (Polygon, 4326), gis_area_sq_m</code></td><td>PostGIS spatial geometry vector polygon boundaries.</td></tr>
                <tr><td><code>documents</code></td><td>core</td><td><code>id, document_uid, title, file_path, file_type, ocr_status, uploaded_by (FK)</code></td><td>Uploaded land record metadata and MinIO storage paths.</td></tr>
                <tr><td><code>document_pages</code></td><td>core</td><td><code>id, document_id (FK), page_number, file_path</code></td><td>Individual page images extracted from PDF documents.</td></tr>
                <tr><td><code>extracted_fields</code></td><td>core</td><td><code>id, document_page_id (FK), field_name, extracted_value, confidence_score, validation_status</code></td><td>OCR & NLP extracted land attributes with confidence scores.</td></tr>
                <tr><td><code>validation_results</code></td><td>core</td><td><code>id, parcel_id (FK), document_id (FK), validation_type, status, severity, message</code></td><td>Rule validation execution outputs.</td></tr>
                <tr><td><code>review_cases</code></td><td>core</td><td><code>id, parcel_id (FK), document_id (FK), assigned_to (FK), priority, status, reviewer_comment</code></td><td>Human review queue items for low-confidence or conflicting data.</td></tr>
                <tr><td><code>audit_events</code></td><td>core</td><td><code>id, user_id (FK), action, entity_type, entity_id, old_value, new_value, created_at</code></td><td>Immutable system audit trail tracking all actions.</td></tr>
                <tr><td><code>mutations</code></td><td>core</td><td><code>id, parcel_id (FK), seller_id (FK), buyer_id (FK), status</code></td><td>Land mutation and transfer history.</td></tr>
                <tr><td><code>registrations</code></td><td>core</td><td><code>id, parcel_id (FK), deed_number, registration_date</code></td><td>Official deed registration records.</td></tr>
                <tr><td><code>evidence</code></td><td>core</td><td><code>id, review_id (FK), file_path, file_type</code></td><td>Supporting evidence attachments uploaded by reviewers.</td></tr>
            </tbody>
        </table>
    </div>

    <!-- Section 31-34: Cadastral Map GIS -->
    <div class="section">
        <h2>8. GIS & Cadastral Mapping Subsystem</h2>
        <p>The Cadastral Mapping subsystem provides visual spatial mapping of land boundaries directly linked to PostGIS database records.</p>
        <ul>
            <li><strong>PostGIS Spatial Query:</strong> Endpoint <code>GET /api/v1/map/parcels</code> executes <code>ST_AsGeoJSON(pg.geometry)::json</code> to query spatial polygons and populates GeoJSON properties with plot number, survey number, khasra number, area, and status.</li>
            <li><strong>Frontend Map Rendering (<code>MapViewer.jsx</code>):</strong>
                <ul>
                    <li><strong>Line Boundaries & Styling:</strong> Renders polygon borders with high-contrast color coding (Emerald stroke for Verified, Crimson stroke for Review Required, Amber stroke for Draft).</li>
                    <li><strong>Plot Number Badges:</strong> Displays permanent plot number badges (e.g., <code>PLT-04011</code>) centered on top of each parcel boundary polygon using Leaflet tooltips.</li>
                    <li><strong>Auto-Fit View Bounds:</strong> Includes an <code>AutoFitBounds</code> sub-component calling <code>map.fitBounds()</code> to automatically zoom and center the map on loaded PostGIS parcels.</li>
                    <li><strong>Multi-Layer Basemaps:</strong> Toggles between Standard OpenStreetMap, Esri World Imagery Satellite, and Dark GIS canvas.</li>
                </ul>
            </li>
        </ul>
    </div>

    <!-- Section 41: Implementation Status Table -->
    <div class="section">
        <h2>9. Comprehensive Component Status Matrix</h2>
        <table>
            <thead>
                <tr>
                    <th>Component</th>
                    <th>Status</th>
                    <th>Details & Implementation Notes</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><strong>Frontend React App</strong></td><td><span class="badge badge-impl">IMPLEMENTED</span></td><td>Vite, TailwindCSS, custom themes, responsive sidebar/header layouts.</td></tr>
                <tr><td><strong>Role Dashboards</strong></td><td><span class="badge badge-impl">IMPLEMENTED</span></td><td>Dashboards for Admin, Officer, Reviewer, Auditor, and Citizen.</td></tr>
                <tr><td><strong>FastAPI REST Engine</strong></td><td><span class="badge badge-impl">IMPLEMENTED</span></td><td>Async routing, request validation, error handlers, CORS middleware.</td></tr>
                <tr><td><strong>JWT Auth & RBAC</strong></td><td><span class="badge badge-impl">IMPLEMENTED</span></td><td>Bcrypt hashing, JWT Bearer tokens, frontend & backend route guards.</td></tr>
                <tr><td><strong>PostgreSQL Database</strong></td><td><span class="badge badge-impl">IMPLEMENTED</span></td><td>14 tables across <code>core</code> and <code>gis</code> schemas with relationships.</td></tr>
                <tr><td><strong>PostGIS Spatial Geometry</strong></td><td><span class="badge badge-impl">IMPLEMENTED</span></td><td>Polygon geometries, spatial queries, GIST spatial index.</td></tr>
                <tr><td><strong>Cadastral Map Viewer</strong></td><td><span class="badge badge-impl">IMPLEMENTED</span></td><td>Leaflet vector lines, plot badges, auto-fit bounds, layer switcher.</td></tr>
                <tr><td><strong>MinIO Object Storage</strong></td><td><span class="badge badge-impl">IMPLEMENTED</span></td><td>Local storage fallback & MinIO client integration for PDF uploads.</td></tr>
                <tr><td><strong>Audit Trail System</strong></td><td><span class="badge badge-impl">IMPLEMENTED</span></td><td>Audit logging helper recording user action, entity ID, and diffs.</td></tr>
                <tr><td><strong>OCR Processing Engine</strong></td><td><span class="badge badge-prep">PREPARED INTERFACE</span></td><td>Backend integration endpoints ready; PaddleOCR integration prepared.</td></tr>
                <tr><td><strong>NLP Extraction Engine</strong></td><td><span class="badge badge-prep">PREPARED INTERFACE</span></td><td>Entity normalization contracts ready; transformer models planned.</td></tr>
                <tr><td><strong>Multi-Rule Validation</strong></td><td><span class="badge badge-prep">PREPARED INTERFACE</span></td><td>Rule validation data structures ready; automated rules planned.</td></tr>
            </tbody>
        </table>
    </div>

    <!-- Section 51: Technical Glossary -->
    <div class="section">
        <h2>10. Technical Glossary</h2>
        <ul>
            <li><strong>PostGIS:</strong> Spatial database extender for PostgreSQL object-relational database, adding support for geographic objects.</li>
            <li><strong>Cadastral Map:</strong> A comprehensive map showing parcel boundaries, plot numbers, ownership details, and spatial dimensions.</li>
            <li><strong>GeoJSON:</strong> An open standard format designed for representing simple geographical features along with non-spatial attributes.</li>
            <li><strong>Khasra / Khata / Survey Number:</strong> Standard land record parcel identifiers used across Indian land revenue administration.</li>
            <li><strong>MinIO:</strong> High-performance, S3-compatible object storage server used for storing raw scanned PDF documents and page renders.</li>
            <li><strong>RBAC (Role-Based Access Control):</strong> An approach to restricting system access to authorized users based on defined roles.</li>
        </ul>
    </div>

    <!-- Section 52 & 53: AI Development Handoff Context & Strict Rules -->
    <div class="section">
        <h2>11. AI Development Handoff Context</h2>
        <div class="callout">
            <strong>Project Context Summary for Future AI Coding Assistants:</strong><br>
            BhuNexis is a full-stack land records digitization platform built using Python 3.13, FastAPI, SQLAlchemy 2.0, PostgreSQL 15 + PostGIS, MinIO, React 18, Vite, TailwindCSS, and Leaflet. The PostgreSQL database name is <code>bhunexis</code> containing 14 tables across <code>core</code> and <code>gis</code> schemas.
        </div>

        <h3>Strict Guidelines for Future AI Assistants:</h3>
        <ol>
            <li><strong>Do NOT recreate or drop the database:</strong> Use the existing <code>bhunexis</code> PostgreSQL database.</li>
            <li><strong>Preserve Schema Isolation:</strong> Maintain the <code>core</code> schema for business entities and <code>gis</code> schema for spatial geometries.</li>
            <li><strong>Preserve Database Relationships:</strong> Maintain existing primary keys, foreign keys, and model properties in <code>all_models.py</code>.</li>
            <li><strong>Security First:</strong> Keep secrets and credentials in environment variables (<code>.env</code>). Never expose MinIO credentials or DB passwords to the frontend.</li>
            <li><strong>Honest Status Reporting:</strong> Do NOT claim OCR/NLP ML models are fully integrated inside the repository when they are prepared integration interfaces.</li>
        </ol>
    </div>

    <div class="footer">
        <p>BhuNexis Technical Project Documentation &bull; Source of Truth Reference &bull; September 2026</p>
    </div>

</body>
</html>
"""

html_path = "D:\\HackathonProjects\\SIH_2026\\BhuNexis\\docs\\BhuNexis_Complete_Technical_Documentation.html"
pdf_path = "D:\\HackathonProjects\\SIH_2026\\BhuNexis\\docs\\BhuNexis_Complete_Technical_Documentation.pdf"

print("1. Writing HTML file to docs...")
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

subprocess.run(cmd, capture_output=True, text=True)

if os.path.exists(pdf_path):
    size = os.path.getsize(pdf_path)
    print(f"SUCCESS: Master PDF created successfully at: {pdf_path}")
    print(f"File Size: {size} bytes")
else:
    print("FAILED: PDF generation failed.")
