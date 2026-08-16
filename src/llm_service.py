import json

import requests
import streamlit as st

from google import genai
from google.genai import types


# ============================================================
# PROVIDER CONFIGURATION
# ============================================================

OPENROUTER_API_URL = (
    "https://openrouter.ai/"
    "api/v1/chat/completions"
)


# ============================================================
# MANAGER ROLES
# ============================================================

MANAGER_ROLES = {

    "Technical Manager": """
Focus on software reliability, application crashes,
bugs, playback failures, performance problems,
stability and technical quality.
""",

    "Product Manager": """
Focus on product features, usability, navigation,
playlists, user experience, feature requests and
product improvement priorities.
""",

    "Customer Service Manager": """
Focus on recurring customer complaints, support
quality, service recovery, customer satisfaction,
response priorities and customer communication.
""",

    "Marketing Manager": """
Focus on brand perception, positive customer
experiences, reputation risks, communication
strategies, positioning and marketing opportunities.
""",

    "Subscription Manager": """
Focus on Premium subscriptions, pricing, billing,
advertisements, perceived value, subscription
satisfaction and customer retention.
"""
}


# ============================================================
# DEFAULT PROVIDER FOR EACH MANAGER
# ============================================================

MANAGER_PROVIDERS = {

    "Technical Manager":
        "gemini",

    "Product Manager":
        "gemini",

    "Customer Service Manager":
        "gemini",

    "Marketing Manager":
        "openrouter",

    "Subscription Manager":
        "openrouter"
}


# ============================================================
# COMMON SYSTEM PROMPT
# ============================================================

COMMON_SYSTEM_PROMPT = """
You are participating in an AI-assisted brand
reputation decision-support system.

You will receive structured findings generated from
Spotify customer reviews that were first classified
by a trained DistilBERT sentiment model.

IMPORTANT RULES:

1. Use only the supplied analysis as evidence.

2. Do not invent statistics.

3. Do not invent customer reviews.

4. Do not claim that a problem causes another problem
   unless the supplied evidence establishes this.

5. Clearly separate observed findings from your
   recommendations.

6. Every recommendation should be related to the
   department you represent.

7. Treat DistilBERT predictions as model-generated
   estimates rather than unquestionable facts.

8. If the supplied evidence is insufficient, clearly
   state the limitation.

9. Do not make claims about competitors or market
   conditions unless that information is supplied.

10. Keep recommendations practical and measurable.
"""


# ============================================================
# GEMINI
# ============================================================

def call_gemini(
    system_prompt,
    user_prompt
):
    """
    Generate a response using Gemini.
    """

    api_key = st.secrets[
        "GEMINI_API_KEY"
    ]

    model_name = st.secrets.get(
        "GEMINI_MODEL",
        "gemini-2.5-flash"
    )

    client = genai.Client(
        api_key=api_key
    )

    response = (
        client.models.generate_content(

            model=model_name,

            contents=user_prompt,

            config=types.GenerateContentConfig(

                system_instruction=(
                    system_prompt
                ),

                temperature=0.2,

                max_output_tokens=2000
            )
        )
    )

    return {
        "provider": "Gemini",
        "model": model_name,
        "content": response.text
    }


# ============================================================
# OPENROUTER
# ============================================================

def call_openrouter(
    system_prompt,
    user_prompt
):
    """
    Generate a response through OpenRouter.
    """

    api_key = st.secrets[
        "OPENROUTER_API_KEY"
    ]

    requested_model = st.secrets.get(
        "OPENROUTER_MODEL",
        "openrouter/free"
    )

    headers = {

        "Authorization":
            f"Bearer {api_key}",

        "Content-Type":
            "application/json"
    }

    payload = {

        "model":
            requested_model,

        "messages": [

            {
                "role": "system",
                "content": system_prompt
            },

            {
                "role": "user",
                "content": user_prompt
            }
        ],

        "temperature":
            0.2,

        "max_tokens":
            2000
    }

    response = requests.post(

        OPENROUTER_API_URL,

        headers=headers,

        json=payload,

        timeout=120
    )

    response.raise_for_status()

    response_data = (
        response.json()
    )

    generated_content = (
        response_data[
            "choices"
        ][0][
            "message"
        ][
            "content"
        ]
    )

    # The Free Router may choose a different
    # actual model for each request.
    actual_model = (
        response_data.get(
            "model",
            requested_model
        )
    )

    return {
        "provider": "OpenRouter",
        "model": actual_model,
        "content": generated_content
    }


# ============================================================
# GENERAL PROVIDER ROUTER
# ============================================================

def call_llm(
    provider,
    system_prompt,
    user_prompt
):

    provider = (
        provider.lower()
    )

    if provider == "gemini":

        return call_gemini(
            system_prompt,
            user_prompt
        )

    elif provider == "openrouter":

        return call_openrouter(
            system_prompt,
            user_prompt
        )

    else:

        raise ValueError(
            f"Unknown LLM provider: "
            f"{provider}"
        )


# ============================================================
# DEPARTMENT MANAGER REPORT
# ============================================================

def generate_manager_report(
    manager_name,
    analysis_summary
):

    if manager_name not in MANAGER_ROLES:

        raise ValueError(
            "Unknown manager role."
        )

    provider = MANAGER_PROVIDERS[
        manager_name
    ]

    department_role = (
        MANAGER_ROLES[
            manager_name
        ]
    )

    system_prompt = f"""
{COMMON_SYSTEM_PROMPT}

You are the {manager_name}.

YOUR DEPARTMENT RESPONSIBILITY:

{department_role}
"""

    user_prompt = f"""
Below is the structured brand reputation analysis.

ANALYSIS DATA:

{json.dumps(
    analysis_summary,
    indent=2,
    ensure_ascii=False
)}

Generate a department-specific report using exactly
the following structure:

# {manager_name} Report

## Department Assessment

Provide a concise assessment from your department's
perspective.

## Key Findings

Identify the most important relevant findings.

## Supporting Evidence

Use only statistics, issue counts, frequent terms
or example reviews contained in the supplied data.

## Recommended Improvements

Provide specific actions.

## Priority Actions

Categorise recommendations as:

- High Priority
- Medium Priority
- Low Priority

## Suggested KPIs

Recommend measurable indicators that management
could monitor.

## Limitations

State any limitations of the supplied evidence.
"""

    result = call_llm(

        provider=provider,

        system_prompt=system_prompt,

        user_prompt=user_prompt
    )

    result[
        "manager"
    ] = manager_name

    return result


# ============================================================
# EXECUTIVE REPORT
# ============================================================

def generate_executive_report(
    analysis_summary,
    department_reports
):
    """
    Executive Manager always uses Gemini
    in the current FYP design.
    """

    system_prompt = f"""
{COMMON_SYSTEM_PROMPT}

You are the Executive Manager.

Your responsibility is to consolidate findings from
all department managers into one management-level
brand reputation report.

Remove duplicated recommendations and prioritise
actions based on the supplied evidence.
"""

    report_texts = {

        manager: {
            "provider":
                report.get(
                    "provider"
                ),

            "model":
                report.get(
                    "model"
                ),

            "report":
                report.get(
                    "content"
                )
        }

        for manager, report
        in department_reports.items()
    }

    user_prompt = f"""
OVERALL BRAND REPUTATION ANALYSIS:

{json.dumps(
    analysis_summary,
    indent=2,
    ensure_ascii=False
)}

DEPARTMENT REPORTS:

{json.dumps(
    report_texts,
    indent=2,
    ensure_ascii=False
)}

Generate:

# Executive Brand Reputation Report

## Executive Summary

## Overall Brand Reputation

## Main Brand Strengths

## Major Reputation Risks

## Critical Issues

## Department-Level Findings

## Immediate Priorities

## Short-Term Improvement Actions

## Long-Term Improvement Actions

## Recommended KPIs

## Overall Management Recommendation

## Limitations
"""

    result = call_gemini(
        system_prompt,
        user_prompt
    )

    result[
        "manager"
    ] = "Executive Manager"

    return result
