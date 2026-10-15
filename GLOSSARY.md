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
The period during which the user is talking with the system, started from the client's start control and ended by the user or by disconnection. A session can contain several tasks.
_Avoid_: Call, conversation, voice session

**Task**:
One job the user asks for, such as "add this meetup to my calendar", from request until it is done, failed, or stopped.
_Avoid_: Job, run

**Consequential action**:
Any action that changes something outside our system: sending, submitting, purchasing, posting, or creating, editing, or deleting an email or event. Reading, navigating, searching, and drafting are not consequential actions.
_Avoid_: Risky action, dangerous action, write

**Approval**:
The user's explicit consent to one consequential action with its specific details. It is used once and stops applying if any of those details change.
_Avoid_: Confirmation, permission

## Control

**Barge-in**:
The user speaking while the system is speaking. It stops the speech only; the task keeps running.
_Avoid_: Interrupt, stop

**Stop request**:
An explicit "stop working" command (spoken or by key) asking for the task's execution to end.
_Avoid_: Interrupt, cancel, pause

**Stop acknowledged**:
The system has received a stop request. It does not mean execution has ended.

**Stop confirmed**:
The system has verified that no further actions will run for the task.
_Avoid_: Cancelled, stopped (without qualification)

## Outcomes

**Verified outcome**:
A result the system checked against the real account or page state after acting, rather than taking the agent's word for it.
_Avoid_: Success, done

**Unknown outcome**:
A consequential action whose result cannot be determined, for example after a timeout. It is neither success nor failure until checked.

## Safety analysis

**Loss**:
Harm the project aims to prevent: an unwanted action, a missed or failed task, loss of the user's control or awareness, or disclosure or misuse of private information or accounts.

**Hazard**:
A property or condition of the system, together with a condition in its environment, that can lead to a loss.
