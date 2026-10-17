# Natural Control

A voice interface that lets blind users delegate digital tasks to an AI agent while staying informed and in control. These terms are used consistently across the hazard analysis, SRS, and other deliverables.

## Tasks and actions

**User**:
The person who owns the connected accounts and gives commands by voice or keyboard. Other voices in the room are not users.
_Avoid_: Client, operator, speaker

**Setup helper**:
A person who completes the initial assisted setup (connecting accounts, granting permissions) for the user.
_Avoid_: Admin, caregiver

**Session**:
The period during which the user is talking with the system, started and ended with the client's start control or a keyboard shortcut, or ended by disconnection. A session can contain several tasks.
_Avoid_: Call, conversation, voice session

**Task**:
One job the user asks for, such as "add this meetup to my calendar", from request until completion, cancellation, or failure. A task may pause and resume.
_Avoid_: Job, run

**Consequential action**:
A write to user or account data, a submission, an external message, or a commitment such as accepting terms or granting access. Reading and navigation may proceed without approval if they have no such effect. Preparing text in memory is different from saving a draft. FR24 defines a narrow exception for rejecting non-essential cookies.
_Avoid_: Risky action, dangerous action, write

**Approval**:
The user's explicit consent to one consequential action, or to a listed batch of similar actions read back with their number and a summary, with their specific details. It is used once and stops applying if any of those details change.
_Avoid_: Confirmation, permission

## Control

**Barge-in**:
The user speaking while the system is speaking. It stops the speech only; the task keeps running.
_Avoid_: Interrupt, stop

**Stop request**:
An explicit "stop working" command (spoken or by key) asking to pause task execution and preserve its context. A separate cancellation request ends the task.
_Avoid_: Cancel (when pause is intended)

**Stop acknowledged**:
The system has received a stop request. It does not mean every earlier external operation ended.

**Stop confirmed**:
New task actions are blocked until explicit resumption. Earlier external operations may still settle. Their outcomes must be reported separately. This is a confirmed pause.
_Avoid_: Cancelled, stopped (without qualification)

## Outcomes

**Verified outcome**:
A result supported by evidence matching the intended action. Evidence may be a meaningful connector response, an account record, or a website confirmation. The agent's unsupported claim is not evidence.
_Avoid_: Success, done

**Unknown outcome**:
A consequential action whose result cannot be determined, for example after a timeout. It is neither success nor failure until checked.

## Safety analysis

**Loss**:
Harm the project aims to prevent: an unwanted action, a missed or failed task, loss of the user's control or awareness, or disclosure or misuse of private information or accounts.

**Hazard**:
A property or condition of the system, together with a condition in its environment, that can lead to a loss.
