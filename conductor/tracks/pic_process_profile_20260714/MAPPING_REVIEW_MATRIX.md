# FOI-O to PIC Mapping Review Matrix

This matrix is a certification aid for the candidate profile. `candidate` is
not approval. FOI-O remains the semantic authority; PIC records a process
projection and its loss boundaries.

| FOI-O source vocabulary | PIC event | PIC kind | PIC state effect | Human question |
| --- | --- | --- | --- | --- |
| `RequestObserved` | `foi-o/event/request.observed` | `observed_event` | initial `request.received` | Does this preserve the intended receipt observation and its source payload boundary? |
| `TransferAssessed` | `foi-o/event/transfer.assessed` | `executed_action` | `request.transfer-assessed` | Is assessment an executed process action for this projection, or should it remain an observed/derived record? |
| `TransferNotified` | `foi-o/event/request.transferred` | `executed_action` | `request.transferred` | Does this preserve notification without asserting the transfer was legally valid? |
| `DeadlineCalculated` | `foi-o/event/deadline.calculated` | `derived_state` | `request.deadline-calculated` | Is the deadline a derived calculation with no certified timeliness conclusion? |
| `ExtensionAssessed` | `foi-o/event/extension.assessed` | `executed_action` | `request.extension-assessed` | Does this preserve the distinction between assessing a ground and deciding reasonableness? |
| `ExtensionNotified` | `foi-o/event/response.extended` | `executed_action` | `request.extended` | Does this represent notice without certifying the extension period as reasonable? |
| `OverdueFlagged` | `foi-o/event/response.overdue` | `derived_state` | `request.overdue-flagged` | Is this only a deterministic signal and not a refusal or review outcome? |
| `DecisionCommunicated` | `foi-o/event/decision.communicated` | `observed_event` | no terminal state | Does this preserve communication without encoding the substantive decision? |

## Explicit non-claims

The candidate does not claim that:

- a deadline calculation proves compliance or non-compliance;
- an overdue flag is a legal refusal, Ombudsman finding, or access outcome;
- an extension ground or period is reasonable;
- a PIC state is a complete FOI-O ontology class hierarchy;
- the staged trace contains unavailable payload or deliberative evidence.
