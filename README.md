
# ⚽ NSFP - Soccer Community Support Platform (MVP Briefing)

**Slogan:** *"Build the Dream from the Ground Up."*  
**Prepared by:** Azaria  Morake
**Purpose:** To develop the CLI-first backend for a soccer support platform helping underfunded teams structure their information and express their needs.

---

## 🎯 Overview

Many soccer teams in disadvantaged communities suffer from a lack of resources, knowledge, and structure. This MVP is the foundation for a platform that provides teams with a centralized digital profile to help manage their information, communicate their needs, and attract support.

This briefing outlines the **core features** and validation logic necessary for the backend, designed to run via CLI during the MVP phase.

---

## ⚙️ Technical Requirements

- **Backend-First:** CLI(Bash), API-ready architecture
- **Tech Stack:** Django
- **Database:** PostgreSQL 
- **Security:** Password hashing, validation, session safety

---

## 🧩 Core Functional Modules

### 1. Team Registration & Profile Management

#### A. Registration

- **Fields:**
  - Team Name (unique)
  - Username (unique)
  - Password (strong, repeat verification)
- **Validation:**
  - Username/Team name uniqueness
  - Password policy enforcement
- **Behavior:**
  - Auto-login upon successful registration

---

#### B. Team Profile

**Subsections:**

**1. Team Profile Info:**

- Fields:
  - Profile Picture (max 2MB)
  - Location
  - Team Email (editable, unique)
  - Password (updatable)
- Validations:
  - File size checks
  - Unique emails
  - Password rules
- Behavior:
  - Highlight and return errors on invalid input
  - Save only if changes were made

---

**2. Team Management**

##### Staff Registration

- Fields:
  - Username (unique)
  - Full Name
  - Role
  - Profile Picture (2MB max)
- Validation:
  - Duplicate usernames
  - Missing roles
- Save triggers confirmation or highlights errors

##### Squad Registration

- Fields:
  - Username (unique)
  - Full Name
  - DOB (DD/MM/YYYY, within reasonable age range)
  - Citizenship (must be real country)
  - Position (from list)
  - Strong Foot (left or right only)
  - Jersey Number (unique per team)
  - Nickname (optional)
  - Team Level (auto-calculated from DOB)
  - Profile Picture (2MB max)
  - Market Value (in ZAR)
- Validation:
  - Unique usernames/jerseys
  - Age and date validation
- Save provides feedback and confirmation

---

### 2. Team Needs

- **Post:** Full-length free-text describing needs
- **Admin:** Can view, edit, delete posts
- **Validation:** Content cannot be blank
- **Behavior:**
  - Confirm post creation or return errors
  - Highlight invalid save attempts

---

### 3. Team Media

#### A. Photos

- Upload up to 10 images per team (2MB max each)
- Deletion allowed with confirmation
- Validation on image count and file size

#### B. Videos

- YouTube embed links only
- Delete allowed with confirmation

- **Behavior:** Prevent new uploads if limit is reached

---

### 4. Management Actions

#### Staff Editing

- Editable Fields:
  - Name
  - Role
  - Profile Picture
- Validation:
  - Profile pic size
- Save must return if no changes detected

#### Squad Editing

- Admin can:
  - Query by age range
  - Edit player (except DOB)
  - Delete player (with confirmation)
- All saves and deletions return feedback

#### Team Needs Editing

- Admin:
  - Views, edits, deletes posts
  - Must confirm deletions
- Save button disabled if unchanged

#### Media Editing

- Admin:
  - Deletes photos (confirmation needed)
  - Uploads new photos (up to 10 limit)
  - Deletes video links
- Error handling: too many images, wrong formats

---

## 🔐 Security

- Strong password encryption (bcrypt or PBKDF2)
- Input sanitization
- Session token safety
- HTTPS enforced in production

---

## 🧰 Deliverables

1. **CLI Tools:**
   - Commands to register, manage, and view all entities
   - Helpful flags, usage info, feedback on all actions

2. **Documentation:**
   - README with usage instructions
   - Future-proof API endpoint planning

3. **Codebase:**
   - Modular project structure
   - Git-based repository with proper commit practices

---



---

