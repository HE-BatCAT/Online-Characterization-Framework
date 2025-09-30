# Use This Template for Architecture Decision Records

Date: 2025-08-25

## Status

Accepted

## Context

We need a lean template for ADR.

## Decision

We will use this ADR as a template for future ADR. It is based on the decision record template by Michael
Nygard, see [Documenting architecture decisions - Michael Nygard](http://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions).

Each ADR MUST have a speaking title (such as this one) as a Markdown section header.

The first paragraph must contain the date of the last
update in the form used in this template.

It MUST have exactly four subsections.

**Status**
: What is the status, such as proposed, accepted, rejected, deprecated, superseded, etc.?

**Context**
: What is the issue that we're seeing that is motivating this decision or change?

**Decision**
: What is the change that we're proposing and/or doing? You may start with "We will..."

**Consequences**
: What becomes easier or more difficult to do because of this change?

Additional information, such as detailed discussion that led to this decision, must not be included here. It
may go in a separate document which could be linked. Find a plain ADR template under
[./templates/000X\_adr\_template.md](./templates/000X_adr_template.md).

We will put our ADR files next to this file and comply to the naming pattern

```
<4-digits>_<title-abbreviation>.md
```

The four digits are important for ordering the ADR files.


## Consequences

* You can use [adr-tools](https://github.com/npryce/adr-tools) for managing the ADR files.
* We have a simple, flexible, no-bullshit template.
