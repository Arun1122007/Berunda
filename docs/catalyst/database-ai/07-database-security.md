# 07 - Database Security

## Overview
This document outlines the security, authorization, and reliability policies for the Zoho Catalyst Data Store and Stratus implementations.

## Authentication and Data Authorization
- **Catalyst Authentication integration**: We will map the Catalyst user identity (derived from standard Catalyst Auth tokens) to the application `auth_User` record. 
- **Ownership Checks**: Every analytical result, RAG conversation, and alert will have a `UserID` reference. Catalyst ZCQL queries will explicitly filter by `UserID` to prevent horizontal privilege escalation.
- **District/Unit Scoping**: Officers will only be able to query FIR records where `DistrictID` matches their profile's `DistrictID`.
- **Admin Access**: Administrative operations (e.g. running Fairness Checks, auditing) will require the `Admin` role.
- **Direct Object Reference Prevention**: All IDs exposed to the frontend should be verified against the authenticated context before any Read/Update/Delete operation.

## Reliability and Scaling
- **Parameterized Queries**: All ZCQL operations must use parameterized SDK queries or safe ORM wrappers to prevent injection.
- **Input Validation**: Pydantic schemas will rigorously validate inputs (types, lengths, enums) before any interaction with Catalyst Data Store.
- **Secrets Management**: No API keys or credentials will be stored in frontend code. Environment variables inside the Catalyst console will manage integration credentials.
- **Soft Deletion**: `auth_User` and `src_CaseMaster` records will use an `IsActive` or `DeletedAt` flag. Hard deletes are restricted to compliance-specific scripts.
- **Audit Logging**: Any destructive action or access to restricted records will write an event to `gov_AuditLog`.
- **Sensitive Fields**: Passwords will not be stored since Catalyst Auth handles identity, but any internal application secrets will be hashed. No full sensitive prompts or plain-text PII will be printed to logs.
