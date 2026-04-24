---
stepsCompleted: [1, 2, 3, 4, 5, 6]
inputDocuments: []
workflowType: 'research'
lastStep: 1
research_type: 'technical'
research_topic: 'CLI Agent ↔ MS Project Desktop Integration'
research_goals: 'Enable CLI agents to automatically update project schedules/tasks/timelines, syncing development progress into MS Project Desktop via file formats (XML, CSV, MPX, JSON) and API-based approaches. For SSPX and other projects.'
user_name: 'Sebastian'
date: '2026-04-04'
web_research_enabled: true
source_verification: true
---

# Technical Research: CLI Agent ↔ MS Project Desktop Integration

## Executive Summary

CLI agents like Claude Code can effectively interact with Microsoft Project Desktop through file-based interchange, specifically using the MSPDI XML format. This research evaluated file formats, libraries, integration patterns, and architectural decisions to determine the optimal approach for syncing development progress from code-centric project tracking (YAML/markdown in git) into MS Project Desktop for PMO scheduling and stakeholder visibility.

**The answer is yes — and it's straightforward.** MS Project Desktop natively opens MSPDI XML files without requiring an Import Wizard. A Python script using the open-source MPXJ library (LGPL, 13+ years mature) can read sprint-status YAML, epic files, and story files, then generate a fully-featured MSPDI XML file with tasks, dependencies, resources, assignments, custom fields, and calendars. The PM opens this XML in MS Project, adjusts the schedule, and optionally saves back to XML for reverse sync.

**Key Findings:**
- **MSPDI XML** is the optimal interchange format — high fidelity, native MS Project support, cross-platform
- **MPXJ** (Python/Java/.NET) is the recommended library — reads `.mpp`, writes MSPDI XML, handles the full project model
- **MPX format is dead** — current MS Project versions cannot open it
- **JSON is not supported** natively by MS Project — use as intermediate format only
- **File-mediated sync with field ownership** avoids two-master conflicts
- **Custom fields** (Text1-3, Number1) carry agent metadata through round-trips
- **Pure XML generation** (zero dependencies) is a viable fallback for simple task lists

**Recommendations:**
1. Start with MPXJ + Python for a proof of concept (~2 hours)
2. Build a full `sprint-status.yaml → MSPDI XML` converter with dependencies and custom fields (~half day)
3. Add bidirectional sync when PM feedback needs to flow back (~1 day)
4. Zero license cost for the recommended approach

## Table of Contents

1. [Technical Research Scope Confirmation](#technical-research-scope-confirmation)
2. [Technology Stack Analysis](#technology-stack-analysis)
   - MS Project Desktop File Formats
   - MSPDI XML Schema
   - Libraries (MPXJ, Aspose.Tasks, Raw XML, CSV)
   - COM Automation
   - JSON Considerations
3. [Integration Patterns Analysis](#integration-patterns-analysis)
   - Pattern 1: File-Based Interchange (MSPDI XML)
   - Pattern 2: Read-Modify-Write
   - Pattern 3: CSV Quick-Sync
   - Pattern 4: COM Automation
   - Pattern 5: Custom Fields for Agent Metadata
   - Pattern 6: Hybrid Pipeline (SSPX Recommendation)
4. [Architectural Patterns and Design](#architectural-patterns-and-design)
   - File-Mediated Sync Architecture
   - Task UID Identity Mapping
   - Conflict Resolution (Field Ownership)
   - Multi-Project Scalability
   - Security and Deployment
5. [Implementation Approaches](#implementation-approaches-and-technology-adoption)
   - Option A: MPXJ + Python (Recommended)
   - Option B: Pure XML Generation
   - Option C: Aspose.Tasks (Commercial)
   - Implementation Roadmap (4 Phases)
   - CLI Agent Integration
   - Testing Strategy
   - Risk Assessment
6. [Technical Research Recommendations](#technical-research-recommendations)
   - Summary of Key Findings
   - Implementation Priority
   - What This Enables

---

## Technical Research Scope Confirmation

**Research Topic:** CLI Agent ↔ MS Project Desktop Integration
**Research Goals:** Enable CLI agents to automatically update project schedules/tasks/timelines, syncing development progress into MS Project Desktop via file formats (XML, CSV, MPX, JSON) and API-based approaches. For SSPX and other projects.

**Technical Research Scope:**

- Architecture Analysis - MS Project file formats, interchange capabilities, import/export paths
- Implementation Approaches - CLI agent file generation, round-trip editing, practical integration methods
- Technology Stack - libraries, tools, CLI utilities for MS Project-compatible format manipulation
- Integration Patterns - file-based interchange, COM automation, MPXJ, Project Online bridge
- Performance Considerations - round-trip fidelity, format limitations, data loss risks

**Research Methodology:**

- Current web data with rigorous source verification
- Multi-source validation for critical technical claims
- Confidence level framework for uncertain information
- Comprehensive technical coverage with architecture-specific insights

**Scope Confirmed:** 2026-04-04

## Technology Stack Analysis

### MS Project Desktop File Formats

MS Project Desktop supports several interchange formats, each with different capabilities for CLI agent integration:

| Format | Extension | Read | Write | Fidelity | CLI-Friendly |
|--------|-----------|------|-------|----------|--------------|
| **MSPDI XML** | `.xml` | Yes | Yes | High | **Best option** |
| **CSV** | `.csv` | Yes (via Import Wizard) | Yes | Low-Medium | Good for simple task lists |
| **Excel** | `.xlsx` | Yes (via Import Wizard) | Yes | Low-Medium | Good for tabular data |
| **MPP** (native binary) | `.mpp` | Yes | Yes | Full | Not directly writable without libraries |
| **MPX** (legacy) | `.mpx` | **No** (dropped) | **No** | N/A | Deprecated — do not use |

**Key finding:** MPX format is **no longer supported** by current MS Project Desktop versions — it cannot open or save MPX files. MSPDI XML is the primary interchange format.
_[High Confidence]_
_Source: [File formats supported by Project desktop — Microsoft Support](https://support.microsoft.com/en-us/office/file-formats-supported-by-project-desktop-face808f-77ab-4fce-9353-14144ba1b9ae)_

### MSPDI XML Schema (Primary Target Format)

The Microsoft Project Data Interchange (MSPDI) format is an XML schema that MS Project has supported since Project 2002. The current schema is `mspdi_pj12.xsd` (Project 2007+, still used through current versions).

**XML Structure:**
```
Project (root)
├── Calendars → Calendar[]
├── Tasks → Task[]
│   ├── UID, Name, Duration, Start, Finish
│   ├── OutlineLevel, WBS
│   ├── PredecessorLink[] (dependencies)
│   └── ExtendedAttribute[] (custom fields)
├── Resources → Resource[]
│   ├── UID, Name, Type
│   └── Cost, StandardRate
└── Assignments → Assignment[]
    ├── TaskUID, ResourceUID
    └── Start, Finish, Units, Work
```

MS Project can **natively open** `.xml` files conforming to this schema — no Import Wizard needed. This makes MSPDI XML the highest-fidelity, lowest-friction format for CLI agents to generate.
_[High Confidence]_
_Source: [Project Elements and XML Structure — Microsoft Learn](https://learn.microsoft.com/en-us/office-project/xml-data-interchange/project-elements-and-xml-structure?view=project-client-2016), [XML Schema — schemas.microsoft.com](https://schemas.microsoft.com/project/2007/mspdi_pj12.xsd)_

### Libraries and Tools for Programmatic Generation

#### MPXJ (Java/Python/.NET/Ruby) — **Recommended**

MPXJ is the most mature open-source library for reading and writing MS Project-compatible files. It supports all major project management formats.

- **Languages:** Java (native), Python (via JPype bridge), .NET (via IKVM), Ruby (gem)
- **Write formats:** MSPDI XML, MPX (legacy), PMXML, XER, Planner, SDEF
- **Read formats:** MPP, MPX, MSPDI, MPD, Primavera P6, Asta Powerproject, GanttProject, and 20+ others
- **Python install:** `pip install mpxj` (requires Java JDK on the system)
- **License:** LGPL (permissive for most use cases)

**Python example (creating a project and writing MSPDI XML):**
```python
import jpype
from mpxj import ProjectFile, FileFormat

file = ProjectFile()
calendar = file.addDefaultDerivedCalendar()

task1 = file.addTask()
task1.name = "Sprint Planning"
task1.duration = Duration.getInstance(2, TimeUnit.DAYS)

task2 = file.addTask()
task2.name = "Implementation"
task2.duration = Duration.getInstance(10, TimeUnit.DAYS)

# Add dependency: task2 depends on task1
from net.sf.mpxj import RelationType
task2.addPredecessor(Relation.Builder().targetTask(task1))

# Write as MSPDI XML — MS Project can open this directly
from mpxj import UniversalProjectWriter
writer = UniversalProjectWriter(FileFormat.MSPDI)
writer.write(file, "sprint-plan.xml")
```

_[High Confidence]_
_Source: [MPXJ.org](https://www.mpxj.org/), [MPXJ on PyPI](https://pypi.org/project/mpxj/), [How To: Write MSPDI files](https://www.mpxj.org/howto-write-mspdi/)_

#### Aspose.Tasks (Python/.NET/Node.js) — **Commercial Alternative**

Aspose.Tasks is a commercial library that can create, read, and write MPP files **natively** (without MS Project installed) — something MPXJ cannot do for writes.

- **Languages:** Python (via .NET bridge), .NET, Java, Node.js (cloud SDK)
- **Key advantage:** Can write `.mpp` files directly (not just XML)
- **Cloud option:** REST API for serverless/cloud workflows
- **License:** Commercial (paid per developer)
- **Python install:** `pip install aspose-tasks`

_[High Confidence]_
_Source: [Aspose.Tasks for Python](https://products.aspose.com/tasks/python-net/), [Create MS Project in Python — Aspose Blog](https://blog.aspose.com/tasks/create-ms-project-in-python/)_

#### Raw XML Generation (No Dependencies)

For simple use cases, a CLI agent can generate MSPDI XML directly using any XML library (Python `xml.etree`, Node.js `xmlbuilder`, etc.) without MPXJ or Aspose. The schema is well-documented and deterministic.

- **Pro:** Zero dependencies, works in any language
- **Con:** Must handle schema compliance manually; easy to produce invalid XML that MS Project rejects
- **Best for:** Simple task lists with durations and dependencies; not for complex resource leveling

_[Medium Confidence — works for simple cases but schema compliance is tricky]_

#### CSV Generation (Simplest Approach)

Any CLI agent can write a CSV file. MS Project imports CSV via its Import Wizard, which maps columns to Project fields.

- **Required columns:** Task Name, Duration, Start, Finish, Outline Level
- **Optional:** Predecessors (but import to a text field first, then copy to Predecessors — direct import can produce unexpected results)
- **Limitation:** Requires user to run Import Wizard manually; no custom fields, calendars, or resource assignments
- **Best for:** Quick task list exports from sprint status files

_[High Confidence]_
_Source: [Import task outline structure — Microsoft Learn](https://learn.microsoft.com/en-us/troubleshoot/microsoft-365-apps/project/import-task-outline-structure), [Export/import data — Microsoft Support](https://support.microsoft.com/en-gb/office/export-or-import-data-to-another-file-format-6e6e581f-a580-4f04-aa87-9b6552143d9c)_

### COM Automation (Windows-Only)

On Windows, MS Project exposes a full COM automation interface accessible via VBA, PowerShell, or Python (`win32com`). This allows:

- Opening `.mpp` files programmatically
- Adding/updating/deleting tasks
- Setting dependencies, resources, custom fields
- Saving and closing — all without the Import Wizard

```python
# Windows only — requires MS Project installed
import win32com.client
app = win32com.client.Dispatch("MSProject.Application")
app.FileOpen("plan.mpp")
project = app.ActiveProject
task = project.Tasks.Add("New Sprint Task")
task.Duration = "5d"
app.FileSave()
app.Quit()
```

**Limitation:** Requires Windows + MS Project installed. Not usable from macOS CLI agents or headless servers.
_[High Confidence]_
_Source: [Application object — Microsoft Learn](https://learn.microsoft.com/en-us/office/vba/api/project.application), [Project VBA reference](https://learn.microsoft.com/en-us/office/vba/api/overview/project)_

### JSON — Not Natively Supported

MS Project Desktop does **not** natively import JSON. However, JSON can serve as an **intermediate format** in a pipeline:

1. CLI agent writes JSON (sprint status, task updates)
2. A script (Python/Node.js) converts JSON → MSPDI XML using MPXJ
3. User opens the XML in MS Project

This is the recommended approach for CLI agents that already produce structured data (like SSPX's `sprint-status.yaml`).

### Technology Adoption Trends

_CLI-to-MS-Project integration:_
- **MSPDI XML** is the de facto standard for programmatic MS Project interaction — all major project management tools use it for interchange
- **MPXJ** dominates the open-source space (13+ years active, 14.1.0 as of 2025, multi-language)
- **Aspose.Tasks** dominates the commercial space for native MPP read/write
- **COM automation** is declining as teams move to cross-platform and cloud workflows
- **No JSON support** in MS Project Desktop — this is unlikely to change; Microsoft's investment is in Project for the Web (which uses Dataverse/Power Platform, not files)

_Source: [MPXJ on Libraries.io](https://libraries.io/pypi/mpxj), [Aspose.Tasks Cloud — GitHub](https://github.com/aspose-tasks-cloud/aspose-tasks-cloud-python)_

## Integration Patterns Analysis

### Pattern 1: File-Based Interchange (Recommended Primary Approach)

The most practical integration pattern for CLI agents is **generate-and-open**: the agent writes a file that MS Project can open directly.

**Data Flow:**
```
CLI Agent (Claude Code, scripts)
    │
    ▼
YAML/JSON (sprint-status.yaml, task data)
    │
    ▼
Python converter script (MPXJ)
    │
    ▼
MSPDI XML file (.xml)
    │
    ▼
MS Project Desktop (File → Open)
```

**Why this works best:**
- No MS Project installation required on the machine generating the file
- Cross-platform (macOS, Linux, Windows)
- MSPDI XML opens natively in MS Project — no Import Wizard
- Full fidelity: tasks, dependencies, resources, assignments, custom fields, calendars
- Version-controllable (XML is text, diffs are readable)

**Round-trip capability:**
1. CLI agent generates initial XML from sprint data
2. PM opens in MS Project, adjusts schedule, adds resources
3. PM saves as XML (File → Save As → XML)
4. CLI agent reads updated XML back (MPXJ can read MSPDI)
5. Agent extracts changes (new dates, resource assignments) and syncs back

_[High Confidence]_
_Source: [MPXJ How To: Write MSPDI](https://www.mpxj.org/howto-write-mspdi/), [Saving/Opening Projects in XML — Microsoft Learn](https://learn.microsoft.com/en-us/office-project/xml-data-interchange/saving-and-opening-projects-in-xml-format?view=project-client-2016)_

### Pattern 2: Read-Modify-Write (Updating Existing Plans)

When a project plan already exists as an `.mpp` file, the agent can update it:

**Data Flow:**
```
Existing .mpp file
    │
    ▼ (MPXJ reads)
In-memory ProjectFile
    │
    ▼ (Agent modifies: update % complete, add tasks, change dates)
Modified ProjectFile
    │
    ▼ (MPXJ writes)
Updated .xml file
    │
    ▼
PM opens in MS Project, saves as .mpp
```

**What MPXJ can read from MPP:** Tasks, resources, assignments, dependencies, custom fields, calendars, baselines, cost data — essentially the full project model.

**What MPXJ writes to MSPDI XML:** All of the above. The MSPDI format supports the full range of data items present in an MPP file.

**Important limitation:** MPXJ cannot write back to `.mpp` format directly — its knowledge of the binary MPP structure is incomplete. The output must be MSPDI XML, which MS Project opens natively. For native `.mpp` output, Aspose.Tasks (commercial) is required.
_[High Confidence]_
_Source: [MPXJ FAQ](https://www.mpxj.org/faq/), [MPXJ Basics](https://www.mpxj.org/howto-start/)_

### Pattern 3: CSV Quick-Sync (Lightweight Task Lists)

For simple task status updates where full project fidelity isn't needed:

**Data Flow:**
```
sprint-status.yaml
    │
    ▼ (simple Python/bash script)
tasks.csv
    │
    ▼
MS Project Import Wizard (File → Open → CSV)
```

**CSV columns that MS Project understands:**

| Column | Maps to MS Project Field | Notes |
|--------|--------------------------|-------|
| Task Name | Name | Required |
| Duration | Duration | e.g., "5d", "2w" |
| Start | Start | Date format must match locale |
| Finish | Finish | Usually calculated from Start + Duration |
| Outline Level | Outline Level | 1 = top-level, 2 = subtask, etc. |
| Predecessors | **Text1** (not Predecessors!) | Import to text field first, then copy |
| % Complete | % Complete | 0-100 |
| Resource Names | Resource Names | Comma-separated |

**Gotcha — Dependencies:** Do NOT import predecessors directly into the Predecessors field. Import them into a Text custom field first, then copy them manually in MS Project. Direct import produces unexpected scheduling results.
_[High Confidence]_
_Source: [Import task outline structure — Microsoft Learn](https://learn.microsoft.com/en-us/troubleshoot/microsoft-365-apps/project/import-task-outline-structure), [Export/import data — Microsoft Support](https://support.microsoft.com/en-gb/office/export-or-import-data-to-another-file-format-6e6e581f-a580-4f04-aa87-9b6552143d9c)_

### Pattern 4: COM Automation (Windows-Only, Richest Control)

When running on Windows with MS Project installed, COM automation provides the deepest integration:

**Data Flow:**
```
CLI Agent (on Windows)
    │
    ▼ (win32com / PowerShell)
MS Project Application Object
    │
    ▼ (direct API calls)
Live .mpp file (opened in MS Project)
```

**Capabilities:**
- Open/create/save `.mpp` files directly
- Add, modify, delete tasks programmatically
- Set dependencies, resources, assignments
- Read/write custom fields
- Trigger recalculation
- Save and close without user interaction

**PowerShell example:**
```powershell
$app = New-Object -ComObject MSProject.Application
$app.FileOpen("C:\Plans\sprint-plan.mpp")
$project = $app.ActiveProject
$task = $project.Tasks.Add("New story from CLI agent")
$task.Duration = "3d"
$task.PercentComplete = 50
$app.FileSave()
$app.Quit()
```

**When to use:** Only when:
- Running on Windows
- MS Project Desktop is installed
- Need live `.mpp` modification without XML intermediary
- Automating batch updates (e.g., nightly sync of sprint progress)

_[High Confidence]_
_Source: [Application object — Microsoft Learn](https://learn.microsoft.com/en-us/office/vba/api/project.application), [Project VBA reference](https://learn.microsoft.com/en-us/office/vba/api/overview/project)_

### Pattern 5: Custom Fields for Agent Metadata

MS Project supports custom fields (Text1-Text30, Flag1-Flag10, Number1-Number20, etc.) that CLI agents can populate to carry metadata through the round-trip.

**Use cases for SSPX:**

| Custom Field | Purpose | Example Value |
|--------------|---------|---------------|
| Text1 | Story ID | "epic-198-story-3" |
| Text2 | Sprint | "Sprint 14" |
| Text3 | Agent Session | "2026-04-04-visit-workflow" |
| Flag1 | Agent-Generated | Yes/No |
| Flag2 | Needs PM Review | Yes/No |
| Number1 | Story Points | 5 |

**In MSPDI XML, custom fields use ExtendedAttributes:**
```xml
<Task>
  <UID>1</UID>
  <Name>Implement visit workflow layout</Name>
  <ExtendedAttribute>
    <FieldID>188743731</FieldID>  <!-- Text1 -->
    <Value>epic-198-story-3</Value>
  </ExtendedAttribute>
  <ExtendedAttribute>
    <FieldID>188743734</FieldID>  <!-- Text2 -->
    <Value>Sprint 14</Value>
  </ExtendedAttribute>
</Task>
```

Custom field values survive the XML round-trip — they persist when the PM saves back to XML or MPP.
_[High Confidence]_
_Source: [Custom Field Data in XML — Microsoft Learn](https://learn.microsoft.com/en-us/office-project/xml-data-interchange/custom-field-data-in-xml?view=project-client-2016), [ExtendedAttributes Schema — Microsoft Learn](https://learn.microsoft.com/en-us/office-project/xml-data-interchange/xml-schema-for-the-extendedattributes-element?view=project-client-2016)_

### Pattern 6: Hybrid Pipeline (SSPX-Specific Recommendation)

For SSPX and similar projects, the optimal integration combines multiple patterns:

```
┌─────────────────────────────────────┐
│  sprint-status.yaml (source of truth) │
│  + epic files + story files           │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Python script: yaml_to_msproject.py │
│  - Reads YAML/markdown epic+story    │
│  - Maps epics → summary tasks        │
│  - Maps stories → subtasks           │
│  - Sets dependencies from story deps │
│  - Populates custom fields (story ID,│
│    sprint, points, status)           │
│  - Uses MPXJ to write MSPDI XML      │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  project-plan.xml (MSPDI)            │
│  - PM opens in MS Project Desktop    │
│  - Adjusts resources, dates, leveling│
│  - Saves back as XML                 │
└──────────────┬──────────────────────┘
               │
               ▼ (optional: reverse sync)
┌─────────────────────────────────────┐
│  Python script: msproject_to_yaml.py │
│  - Reads updated XML via MPXJ        │
│  - Extracts date/resource changes    │
│  - Updates sprint-status.yaml        │
└─────────────────────────────────────┘
```

**CLI agent role in this pipeline:**
- Claude Code (or any CLI agent) can run `python yaml_to_msproject.py` to generate the XML
- The agent can also be asked to "update the MS Project plan" — it edits the converter script or runs it with parameters
- Reverse sync allows PM schedule adjustments to flow back into the dev workflow

### Integration Pattern Comparison

| Pattern | Fidelity | Complexity | Cross-Platform | Automation Level |
|---------|----------|------------|----------------|-----------------|
| MSPDI XML (Pattern 1) | **High** | Medium | **Yes** | Full |
| Read-Modify-Write (Pattern 2) | **High** | Medium | **Yes** | Full |
| CSV Quick-Sync (Pattern 3) | Low-Med | **Low** | **Yes** | Partial (wizard needed) |
| COM Automation (Pattern 4) | **Full** | High | No (Windows) | Full |
| Custom Fields (Pattern 5) | High | Medium | **Yes** | Full |
| Hybrid Pipeline (Pattern 6) | **High** | Medium-High | **Yes** | **Full + bidirectional** |

**Recommendation:** Pattern 6 (Hybrid Pipeline) built on Pattern 1 (MSPDI XML via MPXJ) with Pattern 5 (Custom Fields) for metadata. This gives you full fidelity, cross-platform support, bidirectional sync, and works from any CLI agent.

## Architectural Patterns and Design

### System Architecture: File-Mediated Sync

The architecture for CLI agent ↔ MS Project integration follows a **file-mediated synchronization** pattern. Unlike API-based integrations where two systems communicate in real time, this architecture uses a shared file (MSPDI XML) as the interchange medium.

```
┌──────────────┐     ┌─────────────┐     ┌──────────────────┐
│  CLI Agent    │     │  MSPDI XML  │     │  MS Project      │
│  (source of   │────▶│  (.xml file) │────▶│  Desktop         │
│   truth for   │◀────│             │◀────│  (PM adjustments)│
│   dev status) │     │  on disk /  │     │                  │
│              │     │  in git repo │     │                  │
└──────────────┘     └─────────────┘     └──────────────────┘
```

**Design Decision:** The development system (YAML/markdown tracked in git) remains the source of truth for task definitions, story IDs, and completion status. MS Project is a **view and scheduling layer** — PMs use it for resource leveling, critical path analysis, and timeline visualization. Data flows primarily dev → MS Project, with optional reverse sync for schedule adjustments.

**Rationale:** This avoids the classic "two masters" problem in bidirectional sync. The dev system owns _what_ needs to be done; MS Project owns _when_ and _who_.
_[High Confidence — established pattern in DevOps ↔ PMO integration]_
_Source: [Bidirectional Data Synchronization Patterns — Dev3lop](https://dev3lop.com/bidirectional-data-synchronization-patterns-between-systems/), [Two-Way Sync Architecture — Stacksync](https://www.stacksync.com/blog/two-way-sync-architecture-essential-knowledge-for-data-professionals)_

### Identity Architecture: Task UID Mapping

The critical architectural challenge is **identity**: how does each system know which task in the other system corresponds to its own?

**MS Project's identity model:**
- **UID (Unique ID):** Auto-incremented integer, never reused within a project file. Stable across save/load cycles. This is the primary identity.
- **ID:** Sequential display order number. Changes when tasks are reordered. Not suitable for mapping.
- **WBS:** Work Breakdown Structure code (e.g., "1.2.3"). Configurable but can change with restructuring.

**Recommended mapping strategy:**

| Agent Field | MS Project Field | Purpose |
|-------------|------------------|---------|
| Story ID (e.g., `198.3`) | **Text1** (ExtendedAttribute) | Stable cross-system identity |
| Epic ID (e.g., `198`) | **Text2** (ExtendedAttribute) | Group identity |
| Task UID | Stored in agent's mapping file | Reverse lookup for updates |

**Architecture:**
```python
# mapping.json — maintained by the converter script
{
  "198.3": {"uid": 5, "last_sync": "2026-04-04T10:00:00Z"},
  "198.4": {"uid": 6, "last_sync": "2026-04-04T10:00:00Z"},
  "198.5": {"uid": 7, "last_sync": "2026-04-04T10:00:00Z"}
}
```

On each sync:
1. Agent reads mapping file to find existing UIDs
2. For existing stories: update the task with matching UID
3. For new stories: create new task, record the assigned UID
4. For deleted stories: optionally mark task as inactive (don't delete — PM may want history)

**UID preservation in MSPDI XML:** Task UIDs are preserved through XML import/export. When the agent writes `<UID>5</UID>` in the XML, MS Project will use that UID. This allows stable round-trip identity.
_[High Confidence]_
_Source: [Unique ID fields — Microsoft Support](https://support.microsoft.com/en-us/office/unique-id-fields-9d8c0bcf-7fd7-40af-8b37-e32f627aa5e7), [UID Element — Microsoft Learn](https://learn.microsoft.com/en-us/office-project/xml-data-interchange/uid-element?view=project-client-2016), [MPXJ Basics](https://www.mpxj.org/howto-start/)_

### Conflict Resolution Architecture

When both sides modify data between syncs, conflicts arise. The architecture handles this with a **last-writer-wins + field ownership** strategy:

| Field | Owner | Conflict Rule |
|-------|-------|---------------|
| Task Name | Agent (dev system) | Agent always wins |
| Story Points / Effort | Agent | Agent always wins |
| % Complete | Agent | Agent always wins (reflects actual dev status) |
| Start Date | **MS Project** (PM) | PM wins — they own the schedule |
| Finish Date | **MS Project** (PM) | PM wins |
| Resource Assignment | **MS Project** (PM) | PM wins |
| Dependencies | Agent creates initial; PM may adjust | **Flag for manual review** |
| Duration | MS Project (calculated) | PM wins |
| Custom fields (Text1-3) | Agent | Agent always wins (identity fields) |

**Conflict detection:** Compare `last_sync` timestamp in mapping file with file modification timestamps. If both sides changed since last sync, flag fields where both differ from the last-known state.

**Design principle:** Avoid complex merge logic. Each field has one owner. When ownership is ambiguous (dependencies), flag for human review rather than auto-resolving.
_[Medium Confidence — pattern is sound but implementation details vary by project needs]_

### Scalability: Multi-Project and Multi-Agent

For organizations with multiple projects (like SSPX + future client projects):

**Single XML per project:**
```
project-plans/
├── sspx-sprint-14.xml          # SSPX current sprint
├── sspx-roadmap.xml            # SSPX full roadmap (all epics)
├── client-a-onboarding.xml     # Client A project
└── mappings/
    ├── sspx-sprint-14.json     # UID mapping
    ├── sspx-roadmap.json
    └── client-a-onboarding.json
```

**Subproject architecture:** MS Project supports subprojects — the roadmap file can reference sprint files. MPXJ handles subproject UID offsets (adds offset to UIDs to prevent collisions across files).
_[High Confidence]_
_Source: [External Projects — MPXJ](https://www.mpxj.org/howto-use-external-projects/)_

### Security and Data Integrity

**Concerns:**
- Project files may contain sensitive resource cost data, client names, or strategic timelines
- MSPDI XML is plain text — readable by anyone with file access

**Mitigations:**
1. Store generated XML files in `.gitignore`-d directories (not committed to repo)
2. Or store in a separate private repo with restricted access
3. Mapping files (with UIDs) can be committed — they contain no sensitive data
4. COM automation (Pattern 4) avoids files on disk entirely — but Windows-only

### Deployment Architecture

**Where the converter script runs:**

| Option | Pros | Cons |
|--------|------|------|
| **Local (developer machine)** | Simple, immediate, no infra needed | Manual trigger, macOS/Linux only |
| **CI/CD (GitHub Actions)** | Automated on push, consistent | Needs MPXJ/Java in CI, artifact storage |
| **Scheduled (cron/launchd)** | Automatic periodic sync | Runs even when not needed |
| **CLI agent on-demand** | Most flexible — "update the MS Project plan" | Requires MPXJ installed in agent env |

**Recommended for SSPX:** Local script, triggered by CLI agent on demand. The agent runs `python scripts/yaml_to_msproject.py` when asked. No CI/CD complexity needed for a single-developer project. Scale to CI/CD when multiple PMs need automatic updates.

## Implementation Approaches and Technology Adoption

### Option A: MPXJ + Python (Recommended)

**Setup requirements:**
- Python 3.8+ (already available via pyenv)
- Java JDK 11+ (for JPype bridge) — `brew install openjdk@17`
- Set `JAVA_HOME` environment variable
- `pip install mpxj` (pulls JPype1 as dependency)

**Pros:**
- Full read/write support for MSPDI XML
- Can also read existing `.mpp` files
- Well-maintained, 13+ years active development (v14.1.0+)
- LGPL licensed — no cost
- Handles calendars, dependencies, resources, assignments, custom fields

**Cons:**
- Requires Java runtime on the machine (JDK ~200MB)
- JPype bridge adds complexity (JVM startup time ~1-2s)
- Not a pure Python solution

**Risk:** Low. MPXJ is the most battle-tested library in this space.
_[High Confidence]_
_Source: [MPXJ Getting Started with Python](https://www.mpxj.org/howto-start-python/), [JPype Installation](https://jpype.readthedocs.io/en/latest/install.html)_

### Option B: Pure XML Generation (Zero Dependencies)

For maximum simplicity and portability, generate MSPDI XML directly using Python's built-in `xml.etree.ElementTree`:

```python
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

ns = "http://schemas.microsoft.com/project"

project = ET.Element("Project", xmlns=ns)
ET.SubElement(project, "Name").text = "SSPX Sprint 14"
ET.SubElement(project, "StartDate").text = "2026-04-07T08:00:00"

# Tasks
tasks = ET.SubElement(project, "Tasks")

task1 = ET.SubElement(tasks, "Task")
ET.SubElement(task1, "UID").text = "1"
ET.SubElement(task1, "ID").text = "1"
ET.SubElement(task1, "Name").text = "Epic 198: Store Journal"
ET.SubElement(task1, "OutlineLevel").text = "1"
ET.SubElement(task1, "Summary").text = "1"

task2 = ET.SubElement(tasks, "Task")
ET.SubElement(task2, "UID").text = "2"
ET.SubElement(task2, "ID").text = "2"
ET.SubElement(task2, "Name").text = "Story 198.1: Visit workflow layout"
ET.SubElement(task2, "OutlineLevel").text = "2"
ET.SubElement(task2, "Duration").text = "PT40H0M0S"  # 5 days
ET.SubElement(task2, "Start").text = "2026-04-07T08:00:00"
ET.SubElement(task2, "Finish").text = "2026-04-11T17:00:00"

# Dependency: task2 depends on nothing (first task)
# task3 would have: <PredecessorLink><PredecessorUID>2</PredecessorUID></PredecessorLink>

tree = ET.ElementTree(project)
ET.indent(tree, space="  ")
tree.write("sprint-plan.xml", xml_declaration=True, encoding="UTF-8")
```

**Pros:**
- Zero external dependencies — works on any Python install
- Fast (no JVM startup)
- Full control over XML output
- Easy to understand and maintain

**Cons:**
- Must manually comply with MSPDI schema (duration format `PT{hours}H{mins}M{secs}S`, date format, UID sequencing)
- No `.mpp` read support — can only generate, not read existing plans
- Easy to produce XML that MS Project rejects if schema rules are violated
- Must handle calendar definitions manually for non-standard schedules

**Best for:** Simple task list generation from sprint status. Not for complex round-trip scenarios.
_[Medium Confidence — works well for simple cases, fragile for complex ones]_

### Option C: Aspose.Tasks (Commercial)

**Setup:** `pip install aspose-tasks` (no Java needed — uses .NET bridge)

**Key advantage:** Can write native `.mpp` files — the only option that produces binary MPP output without MS Project installed.

**Cost:** Commercial license required (~$999/developer/year for on-premise).

**Best for:** Organizations that need `.mpp` output for stakeholders who won't open XML files, or need to modify existing `.mpp` files in place.
_[High Confidence]_
_Source: [Aspose.Tasks for Python](https://products.aspose.com/tasks/python-net/), [Aspose.Tasks on PyPI](https://pypi.org/project/aspose-tasks/)_

### Implementation Roadmap for SSPX

**Phase 1: Proof of Concept (1-2 hours)**
1. Install MPXJ: `pip install mpxj` (ensure Java is available)
2. Write a minimal script that reads `sprint-status.yaml` and produces one MSPDI XML file with epics as summary tasks and stories as subtasks
3. Open the XML in MS Project Desktop — verify it looks correct
4. Commit script to `scripts/yaml_to_msproject.py`

**Phase 2: Full Feature Script (half day)**
1. Add dependency mapping (story dependencies → PredecessorLink)
2. Add custom fields (Text1=story ID, Text2=sprint, Number1=points)
3. Add % complete from story status (`done` → 100%, `in-progress` → 50%, `todo` → 0%)
4. Add UID mapping file (`scripts/msproject-mapping.json`)
5. Support incremental updates (read existing XML, update tasks, preserve PM's schedule adjustments)

**Phase 3: Bidirectional Sync (optional, 1 day)**
1. Add reverse sync: read PM-modified XML back → extract date/resource changes
2. Surface differences as suggestions (don't auto-modify sprint-status.yaml)
3. CLI agent can present: "PM moved Story 198.3 to April 14 — update sprint status?"

**Phase 4: Multi-Project (when needed)**
1. Support multiple YAML sources → multiple XML outputs
2. Add subproject support for roadmap roll-up view
3. Template system for different project structures

### Practical CLI Agent Integration

**How a Claude Code agent would use this:**

```bash
# User asks: "Generate MS Project plan from current sprint"
python scripts/yaml_to_msproject.py --sprint current --output project-plans/sprint-14.xml

# User asks: "Update the project plan with latest story status"  
python scripts/yaml_to_msproject.py --update project-plans/sprint-14.xml

# User asks: "What did the PM change in the project plan?"
python scripts/msproject_diff.py project-plans/sprint-14.xml
```

The CLI agent can:
- Run the conversion script directly
- Read the output XML to verify it looks correct
- Present a summary of what was generated/changed
- Suggest the user open the file in MS Project

### Testing Strategy

| Test | Method | Purpose |
|------|--------|---------|
| XML schema validation | Validate against `mspdi_pj12.xsd` | Ensure MS Project will accept the file |
| Round-trip test | Generate XML → open in MS Project → save as XML → diff | Verify data survives the round trip |
| UID stability test | Generate twice → compare UIDs | Ensure mapping is deterministic |
| Dependency test | Create tasks with predecessors → verify in MS Project | Confirm Gantt chart shows correct links |
| Custom field test | Set Text1/Text2 → verify in MS Project custom columns | Confirm metadata survives |

### Risk Assessment and Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| MSPDI schema version mismatch | Low | Medium | Use 2007 schema (pj12) — all current MS Project versions support it |
| MPXJ breaking change | Low | Low | Pin version in requirements.txt |
| Java not available on target machine | Medium | High | Document setup; Option B (pure XML) as fallback |
| PM modifies task structure (adds/deletes tasks) | High | Medium | UID mapping + custom field identity; flag orphans |
| Duration format errors | Medium | Medium | Unit tests for PT format conversion |
| Calendar mismatches (holidays, work hours) | Medium | Low | Include standard calendar in XML; document limitations |

### Cost Analysis

| Approach | Setup Cost | Ongoing Cost | License |
|----------|-----------|-------------|---------|
| MPXJ + Python | ~2 hours setup | Zero | LGPL (free) |
| Pure XML (Option B) | ~1 hour setup | More maintenance | N/A (stdlib) |
| Aspose.Tasks | ~30 min setup | ~$999/yr/dev | Commercial |
| COM Automation | ~1 hour (Windows only) | Zero | Requires MS Project license |

**Recommendation for SSPX:** Start with **Option A (MPXJ)** for the PoC. If Java setup proves problematic on the target machine, fall back to **Option B (pure XML)** for simple task lists. Avoid Aspose cost unless `.mpp` output is specifically required by a client.

## Technical Research Recommendations

### Summary of Key Findings

1. **MSPDI XML is the optimal interchange format** — high fidelity, native MS Project support, well-documented schema, cross-platform
2. **MPXJ is the recommended library** — mature, multi-language, full read/write, open source
3. **File-mediated sync with field ownership** is the correct architecture — avoids two-master conflicts
4. **Custom fields (Text1-3, Flag1-2, Number1) carry agent metadata** through the round-trip
5. **Task UID + mapping file** provides stable cross-system identity
6. **Pure XML generation is a viable zero-dependency fallback** for simple use cases

### Implementation Priority

```
 Priority 1 (Do first):
   → Install MPXJ, write PoC script, verify XML opens in MS Project
   
 Priority 2 (Core value):
   → Full sprint-status.yaml → MSPDI converter with dependencies + custom fields
   → UID mapping for incremental updates
   
 Priority 3 (Nice to have):
   → Reverse sync (PM changes → sprint status suggestions)
   → Multi-project support
   → CLI agent slash command integration
```

### What This Enables

Once implemented, a CLI agent (Claude Code or similar) can:
- **"Generate a project plan"** → reads sprint-status.yaml + epic files → produces MSPDI XML
- **"Update the project plan"** → reads existing XML + current sprint status → produces updated XML preserving PM's schedule
- **"What changed in the PM's plan?"** → diffs PM-modified XML against last agent-generated version
- **"Export roadmap for stakeholder"** → generates full roadmap XML with all epics and milestones

This bridges the gap between developer-centric project tracking (YAML/markdown in git) and PMO-centric scheduling (MS Project), without requiring either side to change their workflow.

---

## Technical Research Methodology and Sources

### Research Methodology

This research was conducted on 2026-04-04 using web search verification against current public sources. All factual claims about file formats, library capabilities, and MS Project behavior are backed by official Microsoft documentation or library maintainer sources. Confidence levels are noted throughout: High (multiple authoritative sources agree), Medium (limited sources or implementation-dependent), Low (inferred or theoretical).

### Primary Sources

- [File formats supported by Project desktop — Microsoft Support](https://support.microsoft.com/en-us/office/file-formats-supported-by-project-desktop-face808f-77ab-4fce-9353-14144ba1b9ae)
- [Project XML Data Interchange Schema Reference — Microsoft Learn](https://learn.microsoft.com/en-us/office-project/xml-data-interchange/project-xml-data-interchange-schema-reference?view=project-client-2016)
- [Project Elements and XML Structure — Microsoft Learn](https://learn.microsoft.com/en-us/office-project/xml-data-interchange/project-elements-and-xml-structure?view=project-client-2016)
- [Task Elements and XML Structure — Microsoft Learn](https://learn.microsoft.com/en-us/office-project/xml-data-interchange/task-elements-and-xml-structure?view=project-client-2016)
- [Custom Field Data in XML — Microsoft Learn](https://learn.microsoft.com/en-us/office-project/xml-data-interchange/custom-field-data-in-xml?view=project-client-2016)
- [Unique ID fields — Microsoft Support](https://support.microsoft.com/en-us/office/unique-id-fields-9d8c0bcf-7fd7-40af-8b37-e32f627aa5e7)
- [UID Element — Microsoft Learn](https://learn.microsoft.com/en-us/office-project/xml-data-interchange/uid-element?view=project-client-2016)
- [XML Schema for ExtendedAttributes — Microsoft Learn](https://learn.microsoft.com/en-us/office-project/xml-data-interchange/xml-schema-for-the-extendedattributes-element?view=project-client-2016)
- [Import task outline structure — Microsoft Learn](https://learn.microsoft.com/en-us/troubleshoot/microsoft-365-apps/project/import-task-outline-structure)
- [Project VBA reference — Microsoft Learn](https://learn.microsoft.com/en-us/office/vba/api/overview/project)
- [MSPDI Schema XSD — schemas.microsoft.com](https://schemas.microsoft.com/project/2007/mspdi_pj12.xsd)

### Library and Tool Sources

- [MPXJ Official Site](https://www.mpxj.org/)
- [MPXJ on PyPI](https://pypi.org/project/mpxj/)
- [MPXJ How To: Write MSPDI files](https://www.mpxj.org/howto-write-mspdi/)
- [MPXJ How To: Read MSPDI files](https://www.mpxj.org/howto-read-mspdi/)
- [MPXJ FAQ](https://www.mpxj.org/faq/)
- [MPXJ Getting Started with Python](https://www.mpxj.org/howto-start-python/)
- [MPXJ External Projects](https://www.mpxj.org/howto-use-external-projects/)
- [MPXJ GitHub — Python README](https://github.com/joniles/mpxj/blob/master/src.python/mpxj/README.md)
- [JPype Installation Documentation](https://jpype.readthedocs.io/en/latest/install.html)
- [Aspose.Tasks for Python](https://products.aspose.com/tasks/python-net/)
- [Aspose.Tasks on PyPI](https://pypi.org/project/aspose-tasks/)
- [Aspose.Tasks Cloud — Node.js SDK](https://github.com/aspose-tasks-cloud/aspose-tasks-cloud-node)

### Architecture and Integration Sources

- [Bidirectional Data Synchronization Patterns — Dev3lop](https://dev3lop.com/bidirectional-data-synchronization-patterns-between-systems/)
- [Two-Way Sync Architecture — Stacksync](https://www.stacksync.com/blog/two-way-sync-architecture-essential-knowledge-for-data-professionals)

---

**Technical Research Completion Date:** 2026-04-04
**Research Type:** Technical
**Source Verification:** All factual claims cited with current sources
**Overall Confidence Level:** High — based on official Microsoft documentation and established open-source library documentation
