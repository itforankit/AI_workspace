# Generative AI Principles

This directory contains examples demonstrating various principles and best practices in working with Generative AI, LLMs and Agentic AI.

## Principle Demonstrated: 
## Structured Output Parsing Using Pydantic
### pydantic/price_finder.py

This example shows how to enforce structure and reliability in LLM outputs by:
Using Pydantic models to define expected output schemas 
Validating LLM responses to ensure type safety and consistency
Handling unstructured natural language responses by converting them into typed Python objects
Providing clear failure modes when outputs don't match expectations
This is useful for scenarios where downstream systems depend on predictable, structured data from LLMs.

