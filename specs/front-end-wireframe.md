Here’s the updated **prompts‑first** wireframe with:

- No user account section
- No theme toggle

Collections are still secondary and accessible from prompt creation and from a separate Collections page.

---

## 1. Main Layout

```text
+----------------------------------------------------------------------------------+
| PromptLab                                             ● API Online               |
+----------------------------------------------------------------------------------+
| [Prompts] (active)   [Collections]   [Search]                                    |
+----------------------------------------------------------------------------------+
| (Routed content area)                                                             |
+----------------------------------------------------------------------------------+
|                              © 2026 PromptLab                                   |
+----------------------------------------------------------------------------------+
```

- Top-right only shows the **API health indicator** (no user menu, no theme toggle).
- Primary nav: **Prompts** first, then **Collections**, then **Search**.

---

## 2. Home = Prompts Grid Page (`/`)

### 2.1 Prompts Home – grid with filters & create

```text
+----------------------------------------------------------------------------------+
| PromptLab                                             ● API Online               |
+----------------------------------------------------------------------------------+
| [Prompts] (active)   [Collections]   [Search]                                    |
+----------------------------------------------------------------------------------+
| Prompts                                                                        |
|----------------------------------------------------------------------------------|
| [New Prompt]        Collection: [ All Collections ▼ ]    View: [ Grid ▼ ]       |
|----------------------------------------------------------------------------------|
| [🔍 Search prompts by title or content...]        Tags: [ + Add tag ▼ ] [Clear] |
|----------------------------------------------------------------------------------|
|  [Loading spinner / error banner]                                                |
|----------------------------------------------------------------------------------|
|  (Empty state when no prompts at all)                                           |
|  ┌───────────────────────────────────────────────────────────────────────────┐  |
|  │ No prompts yet.                                                           │  |
|  │ Create your first prompt and (optionally) assign it to a collection.     │  |
|  │ [Create Prompt]                                                           │  |
|  └───────────────────────────────────────────────────────────────────────────┘  |
|----------------------------------------------------------------------------------|
|  (Grid view when prompts exist)                                                |
|----------------------------------------------------------------------------------|
|  +---------------------+   +---------------------+   +---------------------+    |
|  | Prompt Title A      |   | Prompt Title B      |   | Prompt Title C      |    |
|  | Short description…  |   | Short description…  |   | Short description…  |    |
|  | Collection: Name 1  |   | Collection: Name 2  |   | Collection: —       |    |
|  | Tags: [tag1][tag2]  |   | Tags: [tagX]        |   | Tags: [tagFoo]      |    |
|  | Updated: 2023-11-02 |   | Updated: 2023-11-03 |   | Updated: 2023-11-04 |    |
|  | [Edit] [Delete]     |   | [Edit] [Delete]     |   | [Edit] [Delete]     |    |
|  +---------------------+   +---------------------+   +---------------------+    |
|  ...                                                                            |
+----------------------------------------------------------------------------------+
```

**Key points:**

- **New Prompt** is the primary CTA on the home page.
- **Collection filter dropdown** lets you quickly narrow prompts by collection but defaults to “All Collections”.
- **Search + tags filter** refine prompts further.
- “View: Grid/List” toggle is optional; you can start with just Grid.

---

## 3. Prompt Creation Modal (with collection & inline collection creation)

### 3.1 Prompt Create / Edit Modal

```text
+--------------------------------- New Prompt -------------------------------------+
|                                                                                  |
|  Title *                                                                         |
|  [___________________________________________]                                   |
|                                                                                  |
|  Content *                                                                       |
|  [________________________________________________________________________]      |
|  [________________________________________________________________________]      |
|  [________________________________________________________________________]      |
|                                                                                  |
|  Description                                                                     |
|  [___________________________________________]                                   |
|                                                                                  |
|  Tags (comma separated)                                                          |
|  [tag1, tag2, tag3____________________________]                                  |
|   Example: onboarding, email                                                     |
|                                                                                  |
|  Collection                                                                      |
|  [ Select a collection ▼ ]   or   [ + New Collection ]                           |
|                                                                                  |
|  (When “+ New Collection” is clicked)                                           |
|  ------------------------------------------------------------------------------  |
|  New Collection Name *                                                           |
|  [___________________________________________]                                   |
|  Description                                                                     |
|  [___________________________________________]                                   |
|  [Create Collection] (creates & selects in dropdown above)                       |
|  ------------------------------------------------------------------------------  |
|                                                                                  |
|  [Cancel]                                             [Save Prompt]              |
|                                                                                  |
+----------------------------------------------------------------------------------+
```

- Users can:
  - Leave collection unselected (if you allow prompts without collections),
  - Select an existing collection,
  - Or create a new collection on the spot.
- This is where **collection creation** is easiest to discover.

---

## 4. Prompt Card (Grid Item on Home)

```text
+-----------------------------+
| Prompt Title A              |
| Short description…          |
|                             |
| Collection: Name 1          |
| Tags: [tag1] [tag2]         |
| Updated: 2023-11-02 08:00   |
|                             |
| [Edit] [Delete]             |
+-----------------------------+
```

- All core info at a glance.
- Edit/Delete are the main actions.

---

## 5. Collections Page (secondary management view)

### 5.1 Collections Index (`/collections`)

```text
+----------------------------------------------------------------------------------+
| PromptLab                                             ● API Online               |
+----------------------------------------------------------------------------------+
| [Prompts]   [Collections] (active)   [Search]                                   |
+----------------------------------------------------------------------------------+
| Collections                                                                   |
|----------------------------------------------------------------------------------|
| [New Collection]                                                               |
|----------------------------------------------------------------------------------|
| [Loading spinner / error banner]                                               |
|----------------------------------------------------------------------------------|
| (Empty state)                                                                  |
| No collections yet.                                                            |
| You can also create collections while creating prompts.                        |
|----------------------------------------------------------------------------------|
| (When collections exist)                                                       |
|----------------------------------------------------------------------------------|
| +--------------------------------------------------------------------------+    |
| | Collection Name 1                                       [View] [Delete] |    |
| | Short description…                                                  12   |    |
| | Prompts: 12         Created: 2023-11-01 12:00                        |   |    |
| +--------------------------------------------------------------------------+    |
| +--------------------------------------------------------------------------+    |
| | Collection Name 2                                       [View] [Delete] |    |
| | Another description…                                               3    |    |
| | Prompts: 3          Created: 2023-12-01 10:30                        |   |    |
| +--------------------------------------------------------------------------+    |
+----------------------------------------------------------------------------------+
```

- **New Collection** here is for bulk/management use.
- Main creation path still: inside **New Prompt** modal.

---

## 6. Collection Detail Page (prompts filtered by that collection)

### 6.1 Collection Detail (`/collections/:collectionId`)

```text
+----------------------------------------------------------------------------------+
| PromptLab                                             ● API Online               |
+----------------------------------------------------------------------------------+
| [Prompts]   [Collections] (active)   [Search]                                   |
+----------------------------------------------------------------------------------+
| ← Back to Collections                                                           |
|----------------------------------------------------------------------------------|
| Collection Name 1                               [Edit Collection] [Delete]       |
| Short description of this collection.                                           |
| Created: 2023-11-01 12:00   Updated: 2023-11-07 09:15                           |
|----------------------------------------------------------------------------------|
| [New Prompt]  (opens Prompt modal with this collection preselected)             |
|----------------------------------------------------------------------------------|
| [🔍 Search prompts in this collection...]   Tags: [ + Add tag ] [Clear]         |
|----------------------------------------------------------------------------------|
| (Prompts grid filtered by this collection)                                      |
|----------------------------------------------------------------------------------|
|  +---------------------+   +---------------------+   +---------------------+    |
|  | Prompt Title A      |   | Prompt Title B      |   | Prompt Title C      |    |
|  | Short description…  |   | Short description…  |   | Short description…  |    |
|  | Collection: Name 1  |   | Collection: Name 1  |   | Collection: Name 1  |    |
|  | Tags: [tag1][tag2]  |   | Tags: [tagX]        |   | Tags: [tagFoo]      |    |
|  | Updated: ...        |   | Updated: ...        |   | Updated: ...        |    |
|  | [Edit] [Delete]     |   | [Edit] [Delete]     |   | [Edit] [Delete]     |    |
|  +---------------------+   +---------------------+   +---------------------+    |
+----------------------------------------------------------------------------------+
```

- UX matches the home page Prompts grid but with a fixed `collectionId` filter.

---

## 7. Search Page (optional, but consistent)

### 7.1 Global Search (`/search`)

```text
+----------------------------------------------------------------------------------+
| PromptLab                                             ● API Online               |
+----------------------------------------------------------------------------------+
| [Prompts]   [Collections]   [Search] (active)                                   |
+----------------------------------------------------------------------------------+
| Global Search                                                                  |
|----------------------------------------------------------------------------------|
| [🔍 Search prompts across all collections...] [Search]                          |
| Tags: [ + Add tag ] [Clear]                                                    |
|----------------------------------------------------------------------------------|
| [Loading spinner / error banner]                                               |
|----------------------------------------------------------------------------------|
| Results for "welcome" (5)                                                      |
|----------------------------------------------------------------------------------|
| +--------------------------------------------------------------------------+    |
| | Prompt Title A (Collection: Collection Name 1)                          |    |
| | Short description…                                                      |    |
| | Tags: [welcome] [email]                                                 |    |
| | [Open in Prompts]                                                       |    |
| +--------------------------------------------------------------------------+    |
| ...                                                                          |
+----------------------------------------------------------------------------------+
```

- Clicking “[Open in Prompts]” can navigate to `/` with a filter set (or `/collections/:id`).

---

## 8. Confirm Dialogs

Same concept, just without any user/theming context.

### 8.1 Delete Prompt

```text
+-------------------------------- Delete Prompt? ----------------------------------+
|                                                                                  |
|  Are you sure you want to delete the prompt “Prompt Title A”?                    |
|  This action cannot be undone.                                                   |
|                                                                                  |
|  [Cancel]                                                 [Delete Prompt]        |
|                                                                                  |
+----------------------------------------------------------------------------------+
```

### 8.2 Delete Collection

```text
+-------------------------------- Delete Collection? ------------------------------+
|                                                                                  |
|  Are you sure you want to delete “Collection Name 1”?                            |
|  This may delete all prompts in this collection (depending on backend rules).    |
|                                                                                  |
|  [Cancel]                                                [Delete Collection]     |
|                                                                                  |
+----------------------------------------------------------------------------------+
```

---

If you’d like, I can now adjust the earlier JSX skeleton to match this exact prompts‑first layout (home = prompts, inline collection creation, no theme/user elements).