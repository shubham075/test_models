# Business Requirements Document (BRD)
## FlowDesk Administration Portal
**MPOnline Inward & Outward Letter Registry System**

---

| Field | Details |
|---|---|
| **Document Version** | 1.0 |
| **Prepared By** | Antigravity (AI Analysis) |
| **Date** | 05 June 2026 |
| **Project Code** | MPO-FLOWDESK-2026 |
| **Client / Owner** | MPOnline Ltd. |
| **Status** | Draft — Pending Stakeholder Review |

---

## Table of Contents
1. [Executive Summary](#1-executive-summary)
2. [Business Context & Problem Statement](#2-business-context--problem-statement)
3. [Project Scope](#3-project-scope)
4. [Stakeholders](#4-stakeholders)
5. [User Roles & Permissions](#5-user-roles--permissions)
6. [Functional Requirements](#6-functional-requirements)
7. [Business Rules](#7-business-rules)
8. [Non-Functional Requirements](#8-non-functional-requirements)
9. [System Architecture Overview](#9-system-architecture-overview)
10. [API Integration Requirements](#10-api-integration-requirements)
11. [Assumptions & Dependencies](#11-assumptions--dependencies)
12. [Out of Scope](#12-out-of-scope)
13. [Open Questions](#13-open-questions)

---

## 1. Executive Summary

**FlowDesk** is a secure, web-based digital governance platform built for **MPOnline Ltd.** to manage official departmental correspondence (letters, circulars, and notices) across their full lifecycle — from inward registration through multi-level approval workflows to outward dispatch and archival.

The system replaces manual, paper-based letter tracking with a structured, role-gated, auditable digital registry. It supports bilingual interface (English / Hindi), dual authentication methods (Mobile OTP & Password), and integrates with an ASP.NET Core Web API backend.

---

## 2. Business Context & Problem Statement

### 2.1 Current Situation
Government and semi-government departments at MPOnline Ltd. handle large volumes of official correspondence daily. Traditionally, this involved:
- Physical stamping and manual logging of inward letters
- Paper-based routing slips for multi-level approvals
- No centralized tracking of letter status or ownership
- Audit trails maintained in physical registers, prone to loss/errors

### 2.2 Business Problems
| # | Problem |
|---|---|
| P1 | No real-time visibility into the status of incoming/outgoing official letters |
| P2 | Approval routing is manual and causes processing delays |
| P3 | No immutable audit trail — compliance verification is difficult |
| P4 | Physical records are vulnerable to loss, damage, or unauthorized access |
| P5 | No centralized employee/department scope management for correspondence |
| P6 | Registry clerks and HODs have no structured handoff mechanism |

### 2.3 Proposed Solution
Deploy the **FlowDesk Portal** — a React-based SPA frontend connected to an ASP.NET Core (.NET) backend API — providing:
- Digital Inward & Outward letter registration with document upload (PDF/JPG)
- Role-based multi-level approval and forwarding workflows
- Real-time dashboard analytics with status distribution charts
- Immutable audit trail and letter tracking history
- Centralized user, department, and service management for Super Admin

---

## 3. Project Scope

### 3.1 In Scope
- **Landing Page** — Public-facing portal introduction with bilingual support
- **Authentication Module** — OTP-based and Password-based login for officers
- **Dashboard** — Role-aware analytics overview with KPI counters and donut chart
- **Inward Registry** — Registration, stamping, and receiving of incoming letters
- **Outward Dispatch** — Creation, document upload, review, approval, and dispatch of outgoing letters
- **Pending Actions Queue** — HOD/Admin action center for acknowledgment and forwarding
- **Acknowledged Registry** — Archive view of acknowledged inward letters
- **Forwarded Correspondence** — View of letters routed externally, with document viewer and timeline
- **Reports View** — Departmental statistics and registry breakdown (placeholder/phase 2 charts)
- **User Management** — Super Admin control to create and manage officer accounts
- **Department Management** — Register and view departmental scopes
- **Service Management** — Map services to departments (Services & Mapping views)
- **Settings** — Workspace security and system preferences
- **Total Actions Grid** — Master registry of all correspondence actions (API-integrated)
- **Action Track File** — Dedicated file/action tracking interface
- **Letter Detail View** — Detailed view for individual inward/outward letters by ID

### 3.2 Out of Scope
*(See Section 12)*

---

## 4. Stakeholders

| Role | Name / Group | Responsibility |
|---|---|---|
| **Business Owner** | MPOnline Ltd. Management | Final approval on scope and priorities |
| **Super Admin** | IT / System Admin Officers | Full portal management, user/dept setup |
| **Department HOD** | Head of Department Officers | Approve, acknowledge, and forward inward letters |
| **Registry Clerk** | Administrative Clerks | Register inward letters, create outward dispatch |
| **Backend Team** | .NET Core API Developers | Maintain API endpoints at `https://localhost:44331` |
| **Frontend Team** | React Developers | Implement and maintain FlowDesk SPA |
| **End Users** | All department officers | Consume the portal per their role |

---

## 5. User Roles & Permissions

The system derives roles automatically from the authenticated username:

| Role | Trigger Condition | Access Level |
|---|---|---|
| **Super Admin** | Username contains `"admin"` | Full access: all modules including User Mgmt, Dept, Services, Mapping, Settings |
| **Department HOD** | Username contains `"hod"` | Dashboard, Inwards, Outwards, Pending, Acknowledged, Forwarded, Reports |
| **Registry Clerk** | All other usernames | Dashboard, Register Inward, Register Outward, Inwards, Outwards |
| **Special (mpo000)** | Exact match `"mpo000"` | Redirected directly to Action Track File view on login |

> **Note:** Role derivation is currently username-based. A future requirement may shift this to JWT claim-based roles from the backend.

### 5.1 Role-Module Matrix

| Module | Super Admin | Department HOD | Registry Clerk |
|---|---|---|---|
| Dashboard / Overview | ✅ | ✅ | ✅ |
| Register Inward | ✅ | ✅ | ✅ |
| Register Outward | ✅ | ✅ | ✅ |
| Inward Registry View | ✅ | ✅ | ✅ |
| Outward Dispatch View | ✅ | ✅ | ✅ |
| Pending Actions | ✅ | ✅ | ❌ |
| Acknowledged Registry | ✅ | ✅ | ❌ |
| Forwarded Correspondence | ✅ | ✅ | ❌ |
| Reports | ✅ | ✅ | ❌ |
| User Management | ✅ | ❌ | ❌ |
| Department Management | ✅ | ❌ | ❌ |
| Services & Mapping | ✅ | ❌ | ❌ |
| Settings | ✅ | ❌ | ❌ |
| Total Actions Grid | ✅ | ✅ | ✅ |
| Action Track File | ✅ | ✅ | ✅ |

---

## 6. Functional Requirements

### 6.1 Authentication Module

#### FR-AUTH-01: OTP-Based Login
- Officers must be able to authenticate using a registered mobile number linked to their department registry
- System sends an OTP to the officer's registered mobile number
- OTP must be validated before access is granted

#### FR-AUTH-02: Password-Based Login
- Officers must be able to authenticate using their Username and Password credentials
- System validates credentials against the backend API

#### FR-AUTH-03: Bilingual Support
- Login page must support English and Hindi language switching
- All labels, titles, and descriptions must be translated accordingly

#### FR-AUTH-04: Session Management
- Authenticated session must be persisted in `localStorage` as `flowdesk_auth`
- JWT access token stored as `accessToken` must be decoded for `fullName` and `designation` claims
- Session must survive page refresh (hydration on app load)

#### FR-AUTH-05: New Officer Registration
- A "Register Officer Account" modal must be available on the login page
- Registration requires: Employee ID Number, Official Mobile Number
- On submission, a toast notification confirms the request is forwarded to HOD for verification

#### FR-AUTH-06: Logout
- User must be able to log out, which clears `flowdesk_auth` and `accessToken` from `localStorage`

---

### 6.2 Landing Page

#### FR-LAND-01: Public Portal Introduction
- Landing page must display: portal branding (FlowDesk logo), navigation, hero section, feature cards, how-it-works steps, and footer
- Must include "Access Portal" CTA linking to `/login`
- Must display trust indicators: Role-based workflows, Secure access, Traceable audit trail

#### FR-LAND-02: Feature Cards
Five feature cards must be displayed:
1. Inward Letter Registry
2. Outward Mail Dispatch
3. Multi-level Workflow Approvals
4. Digital File Archiving Room
5. Audit Trail Action Logs

#### FR-LAND-03: Bilingual Support
- Language toggle (English / Hindi) must be available in the header
- All text content must switch between EN and HI

---

### 6.3 Dashboard / Overview

#### FR-DASH-01: KPI Stat Cards
Dashboard must display the following real-time counters fetched from the API:
| Stat | Description |
|---|---|
| Total Actions | All registry actions |
| Inwards | Total inward letters registered |
| Pending | Letters awaiting HOD action |
| Acknowledged | Letters acknowledged by HOD |
| Forwarded | Letters forwarded to external branches |
| Outwards | Total outward dispatch letters |
| Track File | Shortcut to Action Track File (uses Total count) |

Each stat card must be clickable and navigate to the respective module.

#### FR-DASH-02: Animated Count-Up
- All KPI numbers must animate from 0 to their real value on page load

#### FR-DASH-03: Recent Letter Registry Table
- Must display up to 4 recent letters (mix of inward and outward)
- Columns: Letter Ref, Subject/Details, Type (Inward/Outward), Status
- Must link to full inwards list

#### FR-DASH-04: Letter Status Donut Chart
- Interactive SVG donut chart showing distribution of: Pending, Acknowledged, Forwarded, Outward letters
- Hovering a segment or legend item must highlight it and show its value in the center

---

### 6.4 Inward Letter Registration

#### FR-INW-REG-01: Document Upload (Letter Copy)
- Officer must upload a scanned copy of the letter before filling metadata
- Accepted formats: PDF, JPG, JPEG, PNG (max 10 MB)
- Drag-and-drop and file browser both supported
- Upload progress bar and OCR scan animation must be shown during upload
- Metadata form is locked/disabled until file upload completes

#### FR-INW-REG-02: Metadata Fields (Required)
| Field | Type | Required |
|---|---|---|
| Department Name | Dropdown (API-fetched) | Yes |
| Service Name | Dropdown (API-fetched, cascades from dept) | Yes |
| Letter Number | Text Input | Yes |
| Letter Date | Date Picker | Yes |
| Letter Received Date | Date Picker | Yes |
| Letter Subject | Textarea | Yes |

#### FR-INW-REG-03: Department & Service Cascade
- Department list must be fetched from API on page load
- Service list must dynamically reload when department changes
- Both must fall back to mock data if API is unreachable

#### FR-INW-REG-04: Form Submission
- On submit, form data posted to the API as `multipart/form-data`
- On success: toast notification + form reset
- On API failure: offline mode fallback — register to Redux local store with warning toast

---

### 6.5 Inward Registry View (Dashboard List)

#### FR-INW-LIST-01: Letter List
- Displays all inward letters with status `"Received"` or `CurrentStatus === 1`
- Columns: Ref ID, Received From, Subject Details, Registry Date, Action

#### FR-INW-LIST-02: Search & Filter
- Text search across: Ref ID, Sender, Subject, Department
- Date range filter: From Date, To Date
- Clear/reset filter button

#### FR-INW-LIST-03: Receive Action
- Each unacknowledged letter shows a **"Receive"** button
- Clicking opens a modal showing letter metadata and a required remarks textarea
- On confirm: API call to mark letter as received; row updates to "Received" badge

---

### 6.6 Outward Mail Registration

#### FR-OUT-REG-01: Outward Form Fields
| Field | Type | Required |
|---|---|---|
| Addressed To (Organization) | Text | Yes |
| Subject | Text/Textarea | Yes |
| Outward Type (Mode) | Dropdown (Speed Post, Courier, etc.) | Yes |
| Department | Dropdown | Yes |
| Service | Dropdown (cascades) | Yes |
| Letter Date | Date Picker | Yes |
| Document | File Upload | Yes |

#### FR-OUT-REG-02: Submission
- Posted to API; on success form resets
- Offline fallback dispatches to Redux store

---

### 6.7 Outward Dispatch View

#### FR-OUT-VIEW-01: List & Status Mapping
- Displays all outward letters from API with statuses:

| Status Code | Label |
|---|---|
| 10 | Prepared |
| 20 | In Approval |
| 30 | Under Review |
| 40 | Dispatched |

#### FR-OUT-VIEW-02: Action Buttons (Permission-Based)
Each row shows action buttons based on API flags (`Allow*` fields):

| Flag | Action | Description |
|---|---|---|
| `AllowEditUpload = 1` | Upload | Upload/replace document (PDF, JPG) |
| `AllowForReview = 1` | Review | Forward to a selected reviewer officer |
| `AllowChangeRequest = 1` | Request Corrections | Send correction notes back to originator |
| `AllowApprove = 1` | Approve | Approve the outward with remarks |
| `AllowSent = 1` | Send | Complete the registry (mark as Sent) |
| `AllowDispatch = 1` | Dispatch | Final dispatch confirmation |

#### FR-OUT-VIEW-03: Action Modals
- Each action opens a modal with letter details and a required remarks/input field
- "Forward for Review" additionally requires selecting a reviewer from an API-fetched employee list
- All actions post to `performOutwardAction` API with an `actionType` string

---

### 6.8 Pending Actions (HOD / Admin)

#### FR-PEND-01: Pending Queue
- Displays letters requiring HOD or Admin action
- Columns: Ref, Subject/Description, Received From, Date, Priority, Actions

#### FR-PEND-02: Acknowledge Action
- HOD clicks **"Acknowledge"**, enters mandatory remarks
- API call to `acknowledgeInward`; on success, letter removed from pending list

#### FR-PEND-03: Forward Action
- HOD clicks **"Forward"**, selects a target employee from a service-based API list, optionally adds remarks
- API call to `forwardInward`; on success, letter removed from pending list

---

### 6.9 Acknowledged Registry

#### FR-ACK-01: Acknowledged Letters List
- Lists all inward letters that have been acknowledged
- Columns: Ref, Subject, Received From, Date, Acknowledged By, Remarks

#### FR-ACK-02: Filter Support
- Search by Ref, Subject, Sender
- Date range filter

---

### 6.10 Forwarded Correspondence

#### FR-FWD-01: Forwarded List
- Lists all letters that have been forwarded externally
- Shows: Ref ID, Date, Route Target (external branch/officer), Subject

#### FR-FWD-02: Track History
- Each row has a **"Track History"** button
- Opens a modal showing a 4-step timeline: Registered → Reviewed → Forwarding Approved → Delivery Tracking

#### FR-FWD-03: Document Viewer
- If a letter has an attached file (`filePath`), a **"View"** button appears
- Opens an embedded PDF/image viewer in a full-screen modal
- Provides "Open In New Tab" and "Close Reader" controls

---

### 6.11 Reports View

#### FR-REP-01: Report Cards (Phase 1 Placeholder)
- **Registry Breakdown** — visual chart showing Inward vs. Outward percentage split
- **Resolution Clearance Rate** — overall clearance rate for the fiscal year (e.g., 94.2% FY 2026)

> *Note: Full chart implementation is a Phase 2 deliverable. Phase 1 shows placeholder layout.*

---

### 6.12 User Management (Super Admin Only)

#### FR-USR-01: Officer List
- Displays all registered system users with: Profile photo, Name, Account Code, Scope Authority, Security Level

#### FR-USR-02: Create Officer Account
- Button to open "Create Officer Account" flow
- Minimum fields: Employee ID, Name, Role, Department Scope

#### FR-USR-03: Edit Officer Profile
- Each row has an "Edit Profile" action to modify user details

---

### 6.13 Department Management (Super Admin Only)

#### FR-DEPT-01: Department List
- Displays all departments as cards showing: Code, Letter Code, Name, Active Officers count, Inward Stamped count, Description

#### FR-DEPT-02: Register Department
- Modal form with: Department Name (required), Department Code (required), Department Letter Code (required), Description (optional)
- On save, new department appears at top of the list

---

### 6.14 Services & Mapping Views (Super Admin Only)

#### FR-SVC-01: Service List
- Displays services scoped to departments

#### FR-MAP-01: Service-Department Mapping
- Allows admins to map services to their respective departments

---

### 6.15 Settings (Super Admin Only)

#### FR-SET-01: Security Policies
- Toggle options:
  - Enable strict CAPTCHA on OTP requests
  - Force alphanumeric OTP formatting (3 letters + 3 numbers)
  - Forward system events to external audit syslog

---

### 6.16 Total Actions Grid

#### FR-TOT-01: Master Registry
- Fetches all correspondence actions from the API
- Columns: Ref ID, Subject/Details, Type, Status, Date, Officer
- Search by Ref, Subject, Officer
- Filter by Type (All / Inward / Outward)
- Shows "Offline Mode" badge if API is unreachable and falls back to local Redux store

---

### 6.17 Action Track File

#### FR-ATF-01: File Tracking Interface
- Dedicated view for tracking specific file/document actions
- Accessible by all authenticated users; default landing for `mpo000` users

---

### 6.18 Letter Detail View

#### FR-DET-01: Individual Letter View
- Accessible via `/dashboard/inward/view/:id` and `/dashboard/outward/view/:id`
- Displays full letter metadata, status, and action history for a specific letter

---

### 6.19 Spotlight / Global Search

#### FR-SRCH-01: Global Search
- Keyboard-accessible spotlight search overlay
- Searches across all registered letters/actions

---

## 7. Business Rules

| ID | Rule |
|---|---|
| BR-01 | A letter copy (PDF/JPG/PNG) **must be uploaded** before inward metadata can be entered |
| BR-02 | Remarks are **mandatory** for all approval, acknowledgment, receive, and correction actions |
| BR-03 | A reviewer **must be selected** from the API employee list before forwarding an outward for review |
| BR-04 | Only PDF and JPG/JPEG files are accepted for outward document uploads |
| BR-05 | Service dropdown is disabled until a Department is selected |
| BR-06 | The "Receive" button on an inward letter is replaced with a "Received" badge once actioned |
| BR-07 | Role assignment is derived from username pattern; "admin" → Super Admin, "hod" → HOD, others → Registry Clerk |
| BR-08 | All dates are stored and displayed in `DD-Mon-YYYY` format (e.g., `05-Jun-2026`) |
| BR-09 | If the backend API is unreachable (status 0 or 408), the system must gracefully fall back to local Redux store and show a warning toast |
| BR-10 | Menu items visible in the sidebar are fetched from the API (dynamic permissions, not hardcoded) |
| BR-11 | The `mpo000` officer account is always redirected to the Action Track File view after login |

---

## 8. Non-Functional Requirements

### 8.1 Performance
| NFR | Requirement |
|---|---|
| NFR-P01 | Dashboard must load KPI counts within 3 seconds on a standard broadband connection |
| NFR-P02 | File upload must display progress feedback within 1 second of file selection |
| NFR-P03 | API calls must include timeout handling; failures should surface within 5 seconds |

### 8.2 Security
| NFR | Requirement |
|---|---|
| NFR-S01 | All API communication must use HTTPS |
| NFR-S02 | JWT tokens stored in `localStorage` must be decoded only for display — not for authorization decisions on the backend |
| NFR-S03 | Sessions must be invalidated on logout by removing all stored tokens |
| NFR-S04 | File uploads must validate file extension and MIME type before sending to server |
| NFR-S05 | Password-based login must not expose credentials in browser network logs |

### 8.3 Usability
| NFR | Requirement |
|---|---|
| NFR-U01 | Portal must support both English and Hindi (bilingual UI) |
| NFR-U02 | All interactive elements must provide clear loading, success, and error feedback (toast notifications) |
| NFR-U03 | Portal must be responsive and usable on tablet and desktop screen sizes |
| NFR-U04 | Dark mode and light mode must both be fully supported |
| NFR-U05 | Keyboard navigation must be supported for spotlight search (Escape to close) |

### 8.4 Reliability
| NFR | Requirement |
|---|---|
| NFR-R01 | System must continue to function in read/register mode when the backend API is unavailable (offline fallback to Redux store) |
| NFR-R02 | API fallback data must display a visible warning banner to the user |

### 8.5 Maintainability
| NFR | Requirement |
|---|---|
| NFR-M01 | All API service calls must be centralized in `src/services/` (not inline in components) |
| NFR-M02 | Global state (auth, registry) must be managed via Redux Toolkit slices |
| NFR-M03 | Reusable components (InputField, DatePicker, Toast, FilterBar, StatCard) must be used consistently |

---

## 9. System Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                   FlowDesk Frontend                  │
│            (React + Vite + Redux Toolkit)            │
│                                                       │
│  ┌──────────┐  ┌───────────┐  ┌──────────────────┐  │
│  │  Pages   │  │ Features  │  │   Components     │  │
│  │ (Views)  │  │ (Auth,    │  │ (Sidebar, Search,│  │
│  │          │  │  Registry)│  │  DatePicker...)  │  │
│  └────┬─────┘  └─────┬─────┘  └──────────────────┘  │
│       │              │                                │
│  ┌────▼──────────────▼──────┐                        │
│  │    Services Layer         │                        │
│  │  inwardService.js         │                        │
│  │  outwardService.js        │                        │
│  │  authService.js           │                        │
│  └────────────┬─────────────┘                        │
└───────────────┼──────────────────────────────────────┘
                │ HTTPS REST API
┌───────────────▼──────────────────────────────────────┐
│         ASP.NET Core Web API Backend                  │
│         https://localhost:44331/api/...               │
│                                                       │
│  /api/auth/*        /api/inward/*   /api/outward/*   │
└──────────────────────────────────────────────────────┘
```

### Key API Endpoints (Inferred from Services)

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/auth/send-otp` | POST | Send OTP to mobile |
| `/api/auth/verify-otp` | POST | Verify OTP and get token |
| `/api/auth/login` | POST | Password-based login |
| `/api/inward/dashboard-counts` | GET | Fetch KPI counts |
| `/api/inward/dashboard-list/{statusId}` | GET | Fetch letters by status |
| `/api/inward/register` | POST (multipart) | Register a new inward letter |
| `/api/inward/receive/{id}` | POST | Mark letter as received |
| `/api/inward/acknowledge/{id}` | POST | Acknowledge a pending letter |
| `/api/inward/forward/{id}` | POST | Forward a letter to an officer |
| `/api/inward/get-departments` | GET | Fetch department list |
| `/api/inward/get-services/{deptId}` | GET | Fetch services for a department |
| `/api/outward/upload-document` | POST (multipart) | Upload outward document |
| `/api/outward/perform-action` | POST | Perform approve/review/dispatch action |
| `/api/outward/review-emp-list/{serviceId}` | GET | Get eligible reviewer employees |

---

## 10. API Integration Requirements

### 10.1 Authentication
- All authenticated API requests must include `Authorization: Bearer {accessToken}` header
- Token is stored in `localStorage` as `accessToken` after successful login

### 10.2 Error Handling
- API responses must follow the shape: `{ success: boolean, message: string, data: any }`
- Status code `0` or `408` signals network/offline failure → trigger offline fallback
- All other failure status codes should display the API `message` in an error toast

### 10.3 File Upload
- Inward registration and outward document upload must use `multipart/form-data`
- Outward upload accepts `.pdf`, `.jpg`, `.jpeg` only
- Inward accepts `.pdf`, `.jpg`, `.jpeg`, `.png`

### 10.4 Fallback Behavior
- When API is unreachable, the system must:
  1. Display an "API Endpoint Unreachable" amber warning banner
  2. Fall back to mock/cached data where applicable
  3. Show a warning toast for any actions performed in offline mode

---

## 11. Assumptions & Dependencies

| # | Assumption / Dependency |
|---|---|
| A1 | The ASP.NET Core backend API is running at `https://localhost:44331` during development |
| A2 | The backend API returns a JWT access token containing `fullName` and `designation` claims |
| A3 | Role-based sidebar menu items are returned dynamically from the API post-login |
| A4 | All registered employees have unique `Username` values used as identifiers |
| A5 | The department/service data is maintained and served by the backend API |
| A6 | Production deployment will use a proper domain (not localhost) with SSL |
| A7 | All browser clients support ES2020+ JavaScript and modern CSS features |

---

## 12. Out of Scope

| Item | Notes |
|---|---|
| Mobile application (iOS / Android) | Web-only in this version |
| Email notification system | Not implemented in current scope |
| Full Reports & Analytics charts | Phase 1 shows placeholder; full implementation is Phase 2 |
| Physical dispatch tracking / courier integration | Not included |
| Document OCR (actual text extraction) | UI shows OCR animation but actual OCR processing is out of scope |
| Multi-tenant / multi-organization support | Single-organization (MPOnline Ltd.) only |
| Role management UI | Roles are derived from username; no UI to assign/change roles |
| Inward letter bulk import | Single letter registration only |

---

## 13. Open Questions

> These questions require answers from stakeholders or the development team before final sign-off.

| # | Question | Owner |
|---|---|---|
| OQ-01 | Will role derivation remain username-based, or should it shift to JWT claim-based roles from the backend? | Backend / Arch Team |
| OQ-02 | What is the maximum file size limit for inward letter copy uploads? (Currently shows "Max 10MB" in UI) | Business Owner |
| OQ-03 | Should the Reports view display live API data in Phase 1, or remain as a placeholder until Phase 2? | Business Owner |
| OQ-04 | Is the `mpo000` account a special system account? Should this behavior be configurable? | IT Admin |
| OQ-05 | What are the exact outward dispatch modes (Speed Post, Courier, etc.)? Should these be API-driven or hardcoded? | Business Owner |
| OQ-06 | What is the session expiry policy? Should the system auto-logout after inactivity? | Security Team |
| OQ-07 | Are there any WCAG accessibility requirements for this portal? | Business Owner |
| OQ-08 | Will the Services & Mapping views require full CRUD via API, or is read-only sufficient for Phase 1? | Backend Team |
| OQ-09 | Should audit trail in Forwarded Correspondence show real API history, or is the static 4-step timeline acceptable? | Business Owner |
| OQ-10 | What is the production base URL for the API? Is `localhost:44331` only for development? | Backend / DevOps |

---

*End of Document — FlowDesk BRD v1.0*
*© 2026 MPOnline Ltd. — Confidential and Proprietary*
