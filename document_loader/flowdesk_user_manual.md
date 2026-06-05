# FlowDesk — Complete User Manual
> **Application**: FlowDesk — Correspondence Registry & Workflow Management System  
> **Technology**: React + Vite (Frontend) | ASP.NET Core (Backend API)  
> **Session Timeout**: 95 minutes of inactivity

---

## Table of Contents
1. [System Overview](#1-system-overview)
2. [User Roles & Designations](#2-user-roles--designations)
3. [Login & Authentication](#3-login--authentication)
4. [Application Routes Reference](#4-application-routes-reference)
5. [Role-Based Route & Menu Access](#5-role-based-route--menu-access)
6. [Inward Mail — Full Workflow](#6-inward-mail--full-workflow)
7. [Outward Mail — Full Workflow](#7-outward-mail--full-workflow)
8. [Pending Actions — HOD Approval Workflow](#8-pending-actions--hod-approval-workflow)
9. [Acknowledged Communications](#9-acknowledged-communications)
10. [Forwarded Correspondence](#10-forwarded-correspondence)
11. [Track File Registry](#11-track-file-registry)
12. [Admin-Only Sections](#12-admin-only-sections)
13. [Global Features](#13-global-features)
14. [Workflow Diagrams](#14-workflow-diagrams)

---

## 1. System Overview

**FlowDesk** is a centralized digital correspondence management system for government/organizational use. It handles the entire lifecycle of both **inward mail** (mail received from outside) and **outward mail** (mail sent to outside) including:

- Digital registration of incoming and outgoing letters
- Scanned document attachment and storage
- HOD-level acknowledgment, forwarding, and reply workflows
- Outward mail approval chain (upload → review → approve → send → dispatch)
- Full audit trail and tracking history for all files
- Role-based menus dynamically loaded from the backend API

---

## 2. User Roles & Designations

FlowDesk supports **three primary roles**, determined by the JWT token returned upon login. Role detection logic (from `authSlice.js`):

| Role | Detection Logic | Example Username |
|---|---|---|
| **Super Admin** | Username contains `"admin"` | `admin`, `superadmin` |
| **Department HOD** | Username contains `"hod"` | `hod01`, `mphod` |
| **Registry Clerk** | All other users | `mpo000`, `clerk1` |

> **Note**: The actual menus/permissions are fetched dynamically from the backend API (`getDashboardTypeWithMenu`). The role detection above is the frontend fallback. The backend controls what menus each user sees.

### Role Summary

| Capability | Super Admin | Department HOD | Registry Clerk |
|---|:---:|:---:|:---:|
| View Overview Dashboard | ✅ | ✅ | ✅ |
| Register Inward Mail | ✅ | ✅ | ✅ |
| View Inward Registry | ✅ | ✅ | ✅ |
| Receive / Mark Inward | ✅ | ✅ | ✅ |
| Register Outward Mail | ✅ | ✅ | ✅ |
| View Outward Registry | ✅ | ✅ | ✅ |
| Upload Outward Document | ✅ | ✅ | ✅ |
| Forward Outward for Review | ✅ | ✅ | ✅ |
| Approve Outward | ✅ | ✅ | ✅ |
| Send / Dispatch Outward | ✅ | ✅ | ✅ |
| Pending Actions (Acknowledge / Forward / Reply) | ✅ | ✅ | ⚠️ per API |
| View Acknowledged List | ✅ | ✅ | ✅ |
| View Forwarded List | ✅ | ✅ | ✅ |
| Track File Registry | ✅ | ✅ | ✅ (default entry point for `mpo000`) |
| Reports | ✅ | ✅ | ✅ |
| User Account Management | ✅ | ❌ | ❌ |
| Department Management | ✅ | ❌ | ❌ |
| Service Catalogue Management | ✅ | ❌ | ❌ |
| Department-Service Mapping | ✅ | ❌ | ❌ |
| Workspace Settings | ✅ | ❌ | ❌ |
| Change Password | ✅ | ✅ | ✅ |

> **Special Case**: User `mpo000` is automatically redirected to the **Track File Registry** (`/dashboard/action-track-file`) and is excluded from the Overview dashboard. This is hardcoded behavior.

---

## 3. Login & Authentication

### How to Log In
1. Navigate to the application root URL (`/`) — the **Landing Page** loads.
2. Click **Login** or navigate to `/login`.
3. Enter your **username** and **password**.
4. On successful login, the system:
   - Issues a **JWT access token** stored in `localStorage` as `accessToken`
   - Stores session data in `localStorage` as `flowdesk_auth`
   - Reads your `fullName` and `designation` from the JWT token claims
   - Redirects you to `/dashboard/overview` (or `/dashboard/action-track-file` for `mpo000`)

### Session Management
- Sessions expire after **95 minutes** from login (or per the JWT `exp` claim, whichever comes first)
- The system checks expiry **every 5 seconds** in the background
- On expiry, you are automatically logged out and redirected to `/login`
- Sessions survive **browser refresh** (stored in localStorage)

### Change Password
- Available to **all roles** via the sidebar bottom section
- Click **Change Password** in the left sidebar → a modal opens
- Enter your current password, new password, and confirm new password

### Sign Out
- Click **Sign Out** in the bottom of the left sidebar
- Clears all session data and redirects to `/login`

---

## 4. Application Routes Reference

All dashboard routes are protected — unauthenticated users are redirected to `/login`.

| Route | Page / Component | Description |
|---|---|---|
| `/` | `LandingPage` | Public landing/home page |
| `/login` | `LoginPage` | Authentication page |
| `/dashboard` | `DashboardLayout` | Protected dashboard wrapper (redirects to `/dashboard/overview`) |
| `/dashboard/overview` | `Overview` | Main dashboard with stats cards, recent letters, and status chart |
| `/dashboard/inwards` | `InwardsView` | List of all received inward letters; "Receive" action |
| `/dashboard/inwards/create` | `RegisterInward` | Form to register a new inward letter |
| `/dashboard/outwards` | `OutwardsView` | List of all outward mail; Upload / Review / Approve / Send / Dispatch actions |
| `/dashboard/outwards/create` | `RegisterOutward` | Form to register a new outward letter |
| `/dashboard/pending` | `PendingView` | Pending workflow items; Acknowledge / Reply / Forward actions |
| `/dashboard/acknowledged` | `AcknowledgedView` | List of acknowledged communications; View document |
| `/dashboard/forwarded` | `ForwardedView` | List of forwarded correspondence; View / Track History |
| `/dashboard/action-track-file` | `ActionTrackFile` | Track file registry; View / Track / Forward actions |
| `/dashboard/total-actions` | `TotalActionsView` | Complete system-wide action registry grid |
| `/dashboard/inward/view/:id` | `LetterDetailView` | Detailed view of a specific inward letter |
| `/dashboard/outward/view/:id` | `LetterDetailView` | Detailed view of a specific outward letter |
| `/dashboard/reports` | `ReportsView` | Departmental reports and statistics |
| `/dashboard/users` | `UsersView` | User account management (Super Admin only) |
| `/dashboard/departments` | `DepartmentsView` | Department registry management (Super Admin only) |
| `/dashboard/services` | `ServicesView` | Service catalogue management (Super Admin only) |
| `/dashboard/mapping` | `MappingView` | Department-Service mapping management (Super Admin only) |
| `/dashboard/settings` | `SettingsView` | Workspace settings (Super Admin only) |

---

## 5. Role-Based Route & Menu Access

The sidebar menu is **dynamically loaded from the backend API**. The menu names map to routes as follows:

| API Menu Name | Route | Icon | Visible to |
|---|---|---|---|
| Dashboard | `overview` | LayoutDashboard | All roles (except `mpo000`) |
| Pending Actions | `pending` | Clock | HOD / Admin |
| Inward Letters | `inwards` | FileDown | All roles |
| Outward Letters | `outwards` | Send | All roles |
| Acknowledge | `acknowledged` | CheckCircle2 | All roles |
| Forwarded | `forwarded` | ArrowUpRight | All roles |
| Track File | `action-track-file` | GalleryHorizontalEnd | All roles |
| Register Outward | `outwards/create` | PlusCircle | All roles |
| Register Inward | `inwards/create` | PlusCircle | All roles |
| Department | `departments` | Layers | Super Admin |
| Service | `services` | Briefcase | Super Admin |
| Mapping | `mapping` | GitCompare | Super Admin |
| Settings | `settings` | Settings | Super Admin |

---

## 6. Inward Mail — Full Workflow

### 6.1 Registering an Inward Letter (Registry Clerk / HOD / Admin)

**Route**: `/dashboard/inwards/create`

This is how a new received letter is entered into the system.

**Step-by-step**:
1. Navigate to **Register Inward** from the sidebar.
2. **Upload Letter Copy** (left panel — required first):
   - Drag & drop or browse to select a scanned file (PDF, JPG, PNG — max 10MB)
   - The system simulates an OCR scan animation with a progress bar
   - Only after successful upload do the metadata fields become active
3. **Fill Letter Metadata** (right panel — unlocks after file upload):
   - **Department Name** *(required)*: Select from the dropdown (loaded from API)
   - **Service Name** *(required)*: Select a service (loaded based on selected department)
   - **Letter Number** *(required)*: e.g., `MOF/IN/2026/049`
   - **Letter Date** *(required)*: The date on the letter
   - **Letter Received Date** *(required)*: The date your office received it
   - **Letter Subject** *(required)*: Brief description of the letter content
4. Click **Save** — the form submits to the backend API.
5. On success: a confirmation toast appears and the form resets.

> **Offline Mode**: If the backend is unreachable, the letter is saved locally in Redux store with a warning toast.

---

### 6.2 Viewing the Inward Registry

**Route**: `/dashboard/inwards`

- Displays all inward letters with status `"Received"` or `CurrentStatus === 1`
- Columns: **Ref ID**, **Received From**, **Subject Details**, **Registry Date**, **Action**

**Filter & Search**:
- Search by Ref ID, sender, subject, or department name
- Filter by date range (From Date / To Date)
- Click **Clear** to reset all filters

**Action — Receive / Mark as Received**:
- Each unprocessed row shows a **Receive** button
- Click **Receive** → a modal opens showing letter reference, sender, and subject
- Enter **Registry Remarks / Notes** (required) in the textarea
- Click **Confirm Receipt** → the letter is marked as received in the system
- Already-received letters show a green ✅ badge with the remarks

---

### 6.3 What a User Can Do Upon Receiving an Inward Mail

After an inward letter is in the system, the **Pending Actions** view (`/dashboard/pending`) is the hub for further workflow steps.

Available actions (each controlled by backend `Allow` flags):

| Action | Description | Required |
|---|---|---|
| **Acknowledge** | Formally acknowledge the letter and close the workflow | Remarks (required) |
| **Reply** | Create an outward letter as a reply to this inward letter | Navigates to Register Outward with pre-filled fields |
| **Forward** | Forward the correspondence to another employee for action | Select employee + optional remarks |

> Buttons are **enabled/disabled** based on the backend response flags (`AllowAcknowledge`, `AllowReply`, `AllowForward`).

---

## 7. Outward Mail — Full Workflow

### 7.1 Registering an Outward Letter

**Route**: `/dashboard/outwards/create`

**Step-by-step**:
1. Navigate to **Register Outward** from the sidebar.
2. Fill the **Outward Registry Form**:
   - **Recipient Department** *(required)*: Select from dropdown (loaded from API)
   - **Recipient Service** *(required)*: Select after choosing department
   - **Recipient Name** *(required)*: Name of the receiving officer
   - **Recipient Address** *(required)*: Organization/office address
   - **Subject** *(required)*: Content description (max 500 characters)
   - **Remarks** *(optional)*: Initial notes or references
3. The **Outward Type** panel (right side) shows either:
   - `New Outward Mail` — fresh letter
   - `Reply to Inward` — auto-filled when navigated from Pending Actions "Reply" button
4. Click **Save Outward Mail**.
5. On success: a popup modal shows the generated **Outward Letter Number**
   - ⚠️ Important: Note this letter number — you will need it to upload the physical document.

---

### 7.2 Outward Letter Actions (in the Outward Registry)

**Route**: `/dashboard/outwards`

Each outward letter row shows action buttons based on backend `Allow` flags:

| Action Button | Backend Flag | Status Trigger | Description |
|---|---|---|---|
| 📤 **Upload** | `AllowEditUpload === 1` | Status: Prepared | Upload the physical letter document (PDF/JPG only) |
| 👁️ **Review** | `AllowForReview === 1` | Status: In Approval | Forward to a reviewer officer |
| ✏️ **Request Corrections** | `AllowChangeRequest === 1` | Status: Under Review | Send back to preparer with correction remarks |
| ✅ **Approve** | `AllowApprove === 1` | Status: Under Review | Approve the outward correspondence |
| 📨 **Send** | `AllowSent === 1` | Status: Approved | Complete the outward registry process |
| 🚚 **Dispatch** | `AllowDispatch === 1` | Status: Sent | Confirm physical dispatch of the letter |

### Outward Status Lifecycle

```
Prepared  →  In Approval  →  Under Review  →  Approved  →  Sent  →  Dispatched
  (10)          (20)            (30)             (40)
```

### Action Details

#### Upload Document
1. Click the **Upload** (📤) button
2. Select a PDF or JPG/JPEG file from your computer
3. A modal opens confirming the file and asking for **Remarks** (required)
4. Click **Confirm & Save**

#### Forward for Review
1. Click the **Review** (👁️) button
2. Modal opens with the outward letter details
3. **Select Reviewer** from the dropdown (loaded from API by service ID)
4. Enter **Remarks** (required)
5. Click **Save & Forward**

#### Request Corrections (Change Request)
1. Click the **Corrections** (✏️) button
2. Enter **Correction Instructions / Remarks** (required)
3. Click **Save Request**

#### Approve
1. Click the **Approve** (✅) button
2. Enter **Approval Remarks** (required)
3. Click **Approve & Save**

#### Send (Complete Registry)
1. Click the **Send** (📨) button
2. A confirmation dialog asks: *"Are you really want to complete the register outward process?"*
3. Click **Yes** to confirm

#### Dispatch
1. Click the **Dispatch** (🚚) button
2. A confirmation dialog asks: *"Are you sure you want to complete the dispatch process?"*
3. Click **Yes** to confirm

---

## 8. Pending Actions — HOD Approval Workflow

**Route**: `/dashboard/pending`

This is where **inward letters** that require departmental attention are listed for action.

### What Appears Here
- Letters with `Status === "Pending"` or `CurrentStatus === 2`
- Each item shows: Reference ID, Subject, Received From, Service, Department, Date
- Priority tags: **Urgent** (red) or **Normal** (amber)

### Available Actions per Item

Each pending item has up to three action buttons, controlled by API flags:

#### 1. 🟢 Acknowledge
- **When available**: `AllowAcknowledge === 1`
- **Steps**:
  1. Click **Acknowledge** (green button)
  2. Modal opens with reference ID and subject
  3. Enter **Resolution Remarks / Notes** (required) — e.g., *"Approved and filed under registry ledger"*
  4. Click **Submit**
- **Effect**: Letter moves from Pending to Acknowledged; removed from Pending list

#### 2. 🔵 Reply
- **When available**: `AllowReply === 1`
- **Steps**:
  1. Click **Reply** (blue button)
  2. Automatically navigates to `/dashboard/outwards/create`
  3. The outward form is **pre-filled** with the original sender, department, service, and subject
  4. Outward type is set to **"Reply to Inward"** with the `InwardID` linked
- **Effect**: Creates a new outward letter linked to the original inward

#### 3. ⬜ Forward
- **When available**: `AllowForward === 1`
- **Steps**:
  1. Click **Forward** (outline button)
  2. Modal opens with reference ID and subject
  3. **Select Target Employee** from the dropdown (loaded from API by service ID)
  4. Enter **Forwarding Remarks / Notes** (optional)
  5. Click **Confirm Forward**
- **Effect**: Correspondence is forwarded to the selected employee; removed from Pending list

---

## 9. Acknowledged Communications

**Route**: `/dashboard/acknowledged`

Lists all inward letters that have been **formally acknowledged**.

### Columns
| Column | Description |
|---|---|
| Letter No | Reference number of the inward letter |
| Subject | Letter subject |
| Service Name | Service category |
| Receive Date | Date received |
| View File | Button to view attached document (if available) |

### View Document
- Click **View** → a Document Viewer modal opens
- Supports **PDF** (rendered in iframe) and **Image** files
- Option to **Open In New Tab** for full-screen viewing
- Click **Close Reader** to dismiss

### Search & Filter
- Search by Letter No, Subject, or Service Name
- Filter by date range (From / To)

---

## 10. Forwarded Correspondence

**Route**: `/dashboard/forwarded`

Lists all inward letters that have been **forwarded** to another officer or branch.

### Columns / Information Shown
| Field | Description |
|---|---|
| Letter No / Ref | Reference IDs |
| Route to | The target officer or external branch |
| Subject | Letter description |
| Date | Forwarding date |

### Actions per Row

#### 📄 View Document
- Available if `filePath` exists
- Opens the Document Viewer modal (same as Acknowledged view)

#### 🕐 Track History
- Click **Track History** → a timeline modal opens
- Shows the complete journey of the letter through the system:
  1. **Inward Correspondence Registered** — digitized and entered
  2. **Review & Endorsement** — planning officer assignment
  3. **Forwarding Dispatch Approved** — HOD routing signature
  4. **External Delivery Tracking** — in transit / awaiting confirmation

---

## 11. Track File Registry

**Route**: `/dashboard/action-track-file`

> **Note**: This is the **default landing page for `mpo000`** users (Registry Clerk with special routing).

Provides real-time monitoring of workflow tracking audits for all inward/outward communication files.

### Columns
| Column | Description |
|---|---|
| File No | Unique file tracking identifier |
| Subject | File subject matter |
| Type | `Inward` or `Outward` |
| Date | Tracking timestamp |
| Status | Current workflow status |
| Actions | Context-specific action buttons |

### Action Buttons (per file, controlled by backend flags)

| Button | Flag | Description |
|---|---|---|
| 👁️ **View** | `AllowView === 1` | Opens the Document Viewer for the attached file |
| 🕐 **Track** | `AllowTrack === 1` | Opens the Tracking Audit Timeline with full history |
| ➡️ **Forward** | `AllowForward === 1` | Forward the file to another employee |

#### View Document
- Renders PDF in an iframe or image in an `<img>` tag
- Option to open in a new browser tab

#### Tracking Audit Timeline
- Each timeline event shows:
  - **Status title** (e.g., "Approved", "Under Review")
  - **Action Done By** (role/person)
  - **Remarks** from that action
  - **Date & Time** of the action
- Color-coded badges: Approved (emerald), Reviewer (amber), Default (indigo)

#### Forward File
1. Click **Forward** → modal opens
2. Employees loaded from API (by Department ID + Service ID)
3. **Select Employee** (required) from dropdown
4. Enter **Remarks** (required)
5. Click **Forward File**
6. Uses `performOutwardAction` API with `actionType: "FORWARD"`

### Search
- Search by File No, Subject, File Type, or Status
- Click **Clear Search** to reset

---

## 12. Admin-Only Sections

The following sections are visible and accessible only to **Super Admin** users.

### 12.1 User Account Manager
**Route**: `/dashboard/users`

- View all registered personnel (Super Admin, Department HOD, Registry Clerk)
- See Account Code, Scope Authority, Security Level
- Click **Edit Profile** to modify user configuration
- Click **Create Officer Account** to add a new user

### 12.2 Department Registry
**Route**: `/dashboard/departments`

- View all departments with their codes, letter codes, active officers, and stamped inwards count
- Click **Register Department Scope** to add a new department
- **Required fields**: Department Name, Department Code, Department Letter Code
- **Optional**: Description

### 12.3 Service Catalogue
**Route**: `/dashboard/services`

- View all administrative services with Code, Name, SLA (in working days), and Status
- Click **Register New Service** to add a service
  - **Required**: Service Code (auto-prefixed with `SRV-`), Service Name
  - **Optional**: SLA Days (default 7), Status (Active/Inactive)
- Click the 🗑️ (trash) icon to delete a service

### 12.4 Department-Service Mapping
**Route**: `/dashboard/mapping`

- Configure which department handles which service
- **Left panel**: Create new mapping (Select Department + Select Service)
- **Right panel**: View all active mappings
- Click 🗑️ to delete an existing mapping

### 12.5 Workspace Settings
**Route**: `/dashboard/settings`

- Security Clearance Policies:
  - Enable/disable strict CAPTCHA verification
  - Force alphanumeric OTP formatting
  - Forward system events to external audit syslog endpoints
- Click **Save Workspace Preferences** to apply

---

## 13. Global Features

### Overview Dashboard
**Route**: `/dashboard/overview`

- **Welcome banner** with pending action count
- **Stat Cards** (clickable, navigate to respective section):
  - Total Actions, Inwards, Pending, Acknowledged, Forwarded, Outwards, Track File
- **Recent Letter Registry** table (last 24 hours)
- **Letters Status Distribution** — interactive donut chart showing Pending / Acknowledged / Forwarded / Outward breakdown

### Spotlight Search
- Press **Ctrl + K** or click the search icon in the top header
- Search across the entire system from any page

### Theme Toggle
- Click the moon/sun icon in the top header to switch between **light** and **dark** mode

### Notifications Bell
- Click the bell icon in the top header
- Shows system audit clearance status message

### Breadcrumb Navigation
- Top header shows current page context (e.g., `FlowDesk → Inward Letter Registry`)

### Sidebar Collapse
- On desktop, click the **chevron button** (◀/▶) at the top of the sidebar to collapse/expand
- Collapsed mode shows only icons; expanded shows icons + labels
- On mobile, a hamburger menu (☰) opens a sliding drawer overlay

### Toast Notifications
- Appear at bottom-right of screen (success/warning/error)
- Auto-dismiss after 4 seconds
- Can be manually dismissed with the ✕ button

---

## 14. Workflow Diagrams

### Inward Mail Lifecycle

```
[External Sender] 
       ↓
[Registry Clerk registers Inward Letter]
   → /dashboard/inwards/create
       ↓
[Letter appears in Inward Registry]
   → /dashboard/inwards  (Status: Received)
       ↓
[Clerk clicks "Receive" + adds remarks]
       ↓
[Letter moves to Pending Actions]
   → /dashboard/pending
       ↓
    ┌─────────────────────────────────┐
    │                                 │
    ▼                                 ▼                          ▼
[ACKNOWLEDGE]                    [FORWARD]                  [REPLY]
(Remarks required)           (Select employee)         (Opens Outward form)
       ↓                            ↓                          ↓
[Acknowledged View]          [Forwarded View]          [Register Outward]
/dashboard/acknowledged      /dashboard/forwarded       (linked to InwardID)
```

---

### Outward Mail Lifecycle

```
[User registers Outward Letter]
   → /dashboard/outwards/create
       ↓
[Letter appears in Outward Registry]
   → /dashboard/outwards  (Status: Prepared)
       ↓
[1. Upload Document]  ← AllowEditUpload === 1
       ↓
[2. Forward for Review]  ← AllowForReview === 1
   (Select Reviewer, add Remarks)     (Status: In Approval → Under Review)
       ↓
    ┌────────────────────┐
    │                    │
    ▼                    ▼
[3. APPROVE]     [3. REQUEST CORRECTIONS]
(Remarks)        (Correction Instructions)
    ↓                    ↓
(Status: Approved)  (Returned to preparer for fix)
    ↓
[4. SEND]  ← AllowSent === 1
   (Confirmation dialog: Yes/No)
       ↓
[5. DISPATCH]  ← AllowDispatch === 1
   (Final confirmation)
       ↓
[Status: Dispatched ✅]
```

---

### Track File Forward Workflow

```
[File appears in Track File Registry]
   → /dashboard/action-track-file
       ↓
    ┌──────────────────────────────┐
    ▼                  ▼                  ▼
[VIEW]           [TRACK]           [FORWARD]
(View document)  (Timeline audit)  (Select employee + remarks)
                                          ↓
                                   [File forwarded to employee]
                                   [Registry refreshes]
```

---

## Quick Reference — Action Flags

These backend API flags control what buttons appear for each letter/file:

| Flag Name | Used In | Enables |
|---|---|---|
| `AllowAcknowledge` | Pending Actions | Acknowledge button |
| `AllowReply` | Pending Actions | Reply button |
| `AllowForward` | Pending Actions | Forward button |
| `AllowEditUpload` | Outward Registry | Upload document button |
| `AllowForReview` | Outward Registry | Forward for Review button |
| `AllowChangeRequest` | Outward Registry | Request Corrections button |
| `AllowApprove` | Outward Registry | Approve button |
| `AllowSent` | Outward Registry | Send button |
| `AllowDispatch` | Outward Registry | Dispatch button |
| `AllowView` | Track File | View document button |
| `AllowTrack` | Track File | Track timeline button |
| `AllowForward` | Track File | Forward file button |

---

*Document generated from source analysis of FlowDesk React frontend — June 2026*
