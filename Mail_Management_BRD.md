# BUSINESS REQUIREMENTS DOCUMENT (BRD)

**Project Name:** Mail Management & Correspondence Tracking System

---

## 1. Project Overview

### Purpose
The purpose of this system is to digitize and manage the complete lifecycle of incoming and outgoing correspondence within the organization.

The system shall provide:
* Centralized mail registration
* Mail assignment and tracking
* Internal forwarding workflow
* Draft preparation and approval workflow
* Outgoing correspondence management
* Complete audit trail
* Notifications and tracking
* Document attachment management

---

## 2. Business Objective

**Current challenges:**
* Physical file movement
* Difficult tracking of pending mails
* Missing audit history
* No visibility of current mail owner
* Manual draft approval process
* Difficult reporting and monitoring

**The proposed system shall:**
* Digitize mail handling
* Improve accountability
* Reduce processing delays
* Maintain complete history
* Enable workflow transparency

---

## 3. Scope

### Included
**Incoming Mail Management**
* Register incoming mail
* Generate diary number
* Upload attachments
* Assign mail

**Mail Processing**
* Acknowledge mail
* Forward mail
* Create draft
* Review draft
* Approve draft
* Reply to mail
* Close mail

**Outgoing Mail**
* Create outward correspondence
* Generate dispatch number
* Send official responses

**Tracking**
* Mail history
* Assignment history
* Draft history
* Audit trail

**Notifications**
* New assignments
* Draft approvals
* Mail status changes

### Excluded (Phase-1)
* SMS integration
* Digital signatures
* OCR scanning
* Mobile application
* External ERP integration

---

## 4. User Roles

### Role 1: Central Registry
* **Responsibilities:** Receive mail, Register mail, Generate diary number, Upload attachments, Assign mail.
* **Permissions:** Register Mail, Assign Mail, View Mail History, View Reports.
* **Cannot:** Approve Draft, Reply To Mail, Close Mail.

### Role 2: D1 (Highest authority)
* **Permissions:** View Assigned Mail, Forward Mail, Create Draft, Approve Draft, Reply Directly, Close Mail, Reopen Mail.

### Role 3: D2
* **Permissions:** View Assigned Mail, Forward Mail, Create Draft, Approve Draft, Reply Directly, Close Mail.

### Role 4: D3
* **Permissions:** View Assigned Mail, Forward Mail, Create Draft, Review Draft, Reply (if allowed).

### Role 5: D4
* **Permissions:** View Assigned Mail, Forward Mail, Create Draft, Submit Draft For Approval.

### Role 6: System Administrator
* **Permissions:** Manage Users, Manage Roles, Manage Designations, Manage Departments, Manage Workflow Permissions, View Logs, View Reports.

---

## 5. Mail Lifecycle

1. **Stage 1: Mail Received** * External Organization -> Central Registry
   * *Status: REGISTERED*
2. **Stage 2: Mail Assignment** * Central Registry -> D1 / D2 / D3 / D4
   * *Status: ASSIGNED*
3. **Stage 3: Mail Processing** * Current holder may: Acknowledge, Forward, Create Draft, Reply
   * *Status: UNDER_PROCESS*
4. **Stage 4: Final Action** * Reply Sent
   * *Status: REPLIED*
5. **Stage 5: Close Mail** * *Status: CLOSED*

---

## 6. Workflow Scenarios

* **Workflow A: Acknowledgement**
  Registry -> D3 -> Acknowledged *(No further action)*
* **Workflow B: Direct Reply**
  Registry -> D2 -> Reply -> Outward Mail -> Closed
* **Workflow C: Forwarding**
  Registry -> D4 -> D3 -> D2 -> Reply -> Closed
* **Workflow D: Draft Approval**
  Registry -> D4 -> Create Draft -> D3 Review -> D2 Review -> D1 Approval -> Reply Sent -> Closed
* **Workflow E: Draft Rejected**
  D4 -> Draft -> D2 Rejects -> Returned -> Correction -> Resubmitted
* **Workflow F: Reopen Mail**
  Closed Mail -> Reopen -> Assign -> Process Again

---

## 7. Functional Requirements

* **FR-001:** System shall allow Central Registry to register incoming mails.
* **FR-002:** System shall generate unique diary numbers.
* **FR-003:** System shall support attachment upload.
* **FR-004:** System shall allow mail assignment.
* **FR-005:** System shall allow mail forwarding.
* **FR-006:** System shall support draft creation.
* **FR-007:** System shall support multi-level draft approval.
* **FR-008:** System shall support draft rejection and resubmission.
* **FR-009:** System shall allow official replies.
* **FR-010:** System shall generate outward correspondence records.
* **FR-011:** System shall allow mail closure.
* **FR-012:** System shall allow reopening of closed mail.
* **FR-013:** System shall maintain assignment history.
* **FR-014:** System shall maintain action history.
* **FR-015:** System shall provide notifications.
* **FR-016:** System shall provide dashboard statistics.

---

## 8. Business Rules

* **BR-001:** Only one user/designation can own a mail at a time.
* **BR-002:** Every action shall be recorded.
* **BR-003:** Diary Number must be unique.
* **BR-004:** Dispatch Number must be unique.
* **BR-005:** Deleted mails shall not be physically removed. Soft delete only.
* **BR-006:** Closed mails cannot be modified unless reopened.
* **BR-007:** Draft approval sequence shall be configurable.
* **BR-008:** Only authorized users may approve drafts.
* **BR-009:** All attachments shall be linked to parent entities.
* **BR-010:** Every mail must have an audit trail.

---

## 9. Mail Statuses

`REGISTERED` | `ASSIGNED` | `ACKNOWLEDGED` | `UNDER_PROCESS` | `FORWARDED` | `DRAFT_CREATED` | `UNDER_REVIEW` | `APPROVED` | `REPLIED` | `CLOSED` | `REOPENED` | `RETURNED_FOR_CHANGES`

---

## 10. Notification Requirements

System shall notify users when:
* Mail Assigned
* Mail Forwarded
* Draft Submitted
* Draft Approved
* Draft Rejected
* Mail Closed
* Mail Reopened

---

## 11. Reports

System shall provide:
* Pending Mails
* Closed Mails
* Department-wise Mails
* Designation-wise Mails
* Draft Approval Pending
* Mail Aging Report
* Daily Registry Report
* Monthly Correspondence Report

---

## 12. Non-Functional Requirements

* **Backend:** ASP.NET Core 8 Web API
* **Frontend:** React
* **Database:** SQL Server
* **Authentication:** JWT
* **Logging:** Serilog
* **Architecture:** Controller -> Application Layer -> Domain Layer -> Repository Layer -> EF Core -> SQL Server

---

## 13. Future Enhancements (Phase 2)

* Digital Signature
* OCR Document Reading
* SMS Notifications
* Email Notifications
* Workflow Designer
* Mobile Application
* Role-Based Dynamic Workflow
* External ERP Integration

---

## 14. Recommended Additions (Reviewer Suggestions)
*Consider adding these to the final BRD before SRS creation to cover enterprise edge cases:*

1. **Service Level Agreements (SLAs) & Escalation:** Define expected Turnaround Time (TAT) for each workflow stage and an escalation matrix if mail sits un-actioned.
2. **Global Search Engine:** Add functional requirements for complex searching (by keyword, sender, date range, diary number) across active and closed mails.
3. **Draft Version Control:** Clarify that when a draft is rejected and updated (Workflow E), the system tracks Draft v1, v2, etc., rather than hard-overwriting the text.
4. **Data Visibility Segregation:** Explicitly state if users in Department A are restricted from viewing mail assigned to Department B.
5. **Data Retention Policy:** Define how many years `CLOSED` correspondence is kept actively searchable vs. archived.
