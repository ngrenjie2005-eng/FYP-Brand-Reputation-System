# ============================================================
# BRANDPULSE AI
# LLM SERVICE
#
# Providers:
# 1. Google Gemini
# 2. OpenRouter Free Router
# ============================================================

import json

import requests
import streamlit as st

from google import genai


# ============================================================
# PROVIDER CONSTANTS
# ============================================================

OPENROUTER_API_URL = (
    "https://openrouter.ai/"
    "api/v1/chat/completions"
)


# ============================================================
# SECRET HELPER
# ============================================================

def get_secret(
    key,
    default=None
):
    """
    Safely retrieve a Streamlit secret.
    """

    try:
        return st.secrets[key]

    except Exception:
        return default


# ============================================================
# MANAGER ROLES
# ============================================================

MANAGER_ROLES = {

    "Technical Manager": """
Focus on:

- application crashes
- software bugs
- playback failures
- performance problems
- reliability
- stability
- technical quality
- application errors

Recommendations must remain within the
technical/engineering perspective.
""",

    "Product Manager": """
Focus on:

- product features
- usability
- user experience
- navigation
- playlists
- feature requests
- product improvement priorities
- customer-facing functionality

Recommendations must remain within the
product-management perspective.
""",

    "Customer Service Manager": """
Focus on:

- customer complaints
- customer support
- service recovery
- response priorities
- customer satisfaction
- recurring customer difficulties
- communication with dissatisfied users

Recommendations must remain within the
customer-service perspective.
""",

    "Marketing Manager": """
Focus on:

- brand perception
- positive customer experiences
- reputation strengths
- reputation risks
- brand communication
- customer messaging
- positioning
- marketing opportunities

Do not invent competitor information.
""",

    "Subscription Manager": """
Focus on:

- Premium subscription
- pricing
- billing
- advertisements
- subscription satisfaction
- perceived value
- retention-related concerns
- payment complaints

Recommendations must remain within the
subscription-management perspective.
"""
}


# ============================================================
# MANAGER → LLM PROVIDER
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
# COMMON SYSTEM INSTRUCTION
# ============================================================

COMMON_SYSTEM_PROMPT = """
You are participating in an AI-assisted
brand reputation decision-support system.

The supplied findings originate from customer
reviews that were first classified using a
trained DistilBERT sentiment-classification model.

IMPORTANT RULES:

1. Use only the supplied analysis as evidence.

2. Do not invent statistics.

3. Do not invent customer reviews.

4. Do not invent issue counts.

5. Do not claim causation unless the supplied
   evidence establishes it.

6. Clearly distinguish observed findings from
   recommendations.

7. Every recommendation must be relevant to the
   department you represent.

8. Treat DistilBERT predictions as model-generated
   estimates rather than unquestionable facts.

9. If evidence is insufficient, explicitly state
   the limitation.

10. Do not invent competitor information.

11. Do not invent market information.

12. Keep recommendations practical, measurable
    and directly related to the supplied evidence.

13. Avoid repeating the same recommendation in
    several different ways.

14. Use professional business-report language.
"""


# ============================================================
# GEMINI CLIENT
# ============================================================

def create_gemini_client():
    """
    Create a Gemini API client using the
    Streamlit secret.
    """

    api_key = get_secret(
        "GEMINI_API_KEY"
    )

    if not api_key:

        raise ValueError(
            "GEMINI_API_KEY is missing from "
            "Streamlit Secrets."
        )

    client = genai.Client(
        api_key=api_key
    )

    return client


# ============================================================
# GEMINI CALL
# ============================================================

def call_gemini(
    system_prompt,
    user_prompt
):
    """
    Generate text using Google's current
    Interactions API.

    Gemini 3.x should not use the older
    temperature/top_p/top_k sampling settings.
    """

    client = create_gemini_client()

    model_name = get_secret(
        "GEMINI_MODEL",
        "gemini-3.7-flash"
    )

    if not model_name:

        model_name = (
            "gemini-3.7-flash"
        )


    # --------------------------------------------------------
    # INTERACTIONS API
    # --------------------------------------------------------

    interaction = (
        client.interactions.create(

            model=model_name,

            input=user_prompt,

            system_instruction=(
                system_prompt
            ),

            # We do not need to preserve server-side
            # conversation state for independent FYP
            # management reports.
            store=False,

            # Low reasoning is enough for the
            # connection test and routine reports.
            # Change to "medium" later for the
            # Executive Manager if desired.
            generation_config={
                "thinking_level": "low"
            }
        )
    )


    response_text = (
        interaction.output_text
    )


    if not response_text:

        raise RuntimeError(
            "Gemini returned an empty response."
        )


    return {

        "provider":
            "Gemini",

        "model":
            model_name,

        "content":
            response_text,

        "interaction_id":
            getattr(
                interaction,
                "id",
                None
            )
    }


# ============================================================
# GEMINI EXECUTIVE CALL
# ============================================================

def call_gemini_executive(
    system_prompt,
    user_prompt
):
    """
    Use a higher reasoning level for the final
    Executive Manager report.
    """

    client = create_gemini_client()

    model_name = get_secret(
        "GEMINI_MODEL",
        "gemini-3.7-flash"
    )


    interaction = (
        client.interactions.create(

            model=model_name,

            input=user_prompt,

            system_instruction=(
                system_prompt
            ),

            store=False,

            generation_config={
                "thinking_level": "medium"
            }
        )
    )


    response_text = (
        interaction.output_text
    )


    if not response_text:

        raise RuntimeError(
            "Gemini returned an empty "
            "executive report."
        )


    return {

        "provider":
            "Gemini",

        "model":
            model_name,

        "content":
            response_text,

        "interaction_id":
            getattr(
                interaction,
                "id",
                None
            )
    }


# ============================================================
# OPENROUTER CALL
# ============================================================

def call_openrouter(
    system_prompt,
    user_prompt
):
    """
    Generate text through OpenRouter's
    free-model router.
    """

    api_key = get_secret(
        "OPENROUTER_API_KEY"
    )


    if not api_key:

        raise ValueError(
            "OPENROUTER_API_KEY is missing "
            "from Streamlit Secrets."
        )


    requested_model = get_secret(
        "OPENROUTER_MODEL",
        "openrouter/free"
    )


    headers = {

        "Authorization":
            f"Bearer {api_key}",

        "Content-Type":
            "application/json",
    }


    payload = {

        "model":
            requested_model,

        "messages": [

            {
                "role":
                    "system",

                "content":
                    system_prompt,
            },

            {
                "role":
                    "user",

                "content":
                    user_prompt,
            },
        ],

        # Keep the request relatively small because
        # OpenRouter free models have stricter limits.
        "max_tokens":
            1800,
    }


    response = requests.post(

        OPENROUTER_API_URL,

        headers=headers,

        json=payload,

        timeout=180,
    )


    # --------------------------------------------------------
    # HANDLE ERROR RESPONSE
    # --------------------------------------------------------

    if not response.ok:

        try:

            error_detail = (
                response.json()
            )

        except Exception:

            error_detail = (
                response.text
            )


        raise RuntimeError(
            f"OpenRouter request failed "
            f"with HTTP {response.status_code}: "
            f"{error_detail}"
        )


    response_data = (
        response.json()
    )


    # --------------------------------------------------------
    # EXTRACT RESPONSE
    # --------------------------------------------------------

    choices = response_data.get(
        "choices",
        []
    )


    if not choices:

        raise RuntimeError(
            "OpenRouter returned no response choices."
        )


    message = (
        choices[0]
        .get(
            "message",
            {}
        )
    )


    generated_content = (
        message.get(
            "content",
            ""
        )
    )


    # Some providers may return content structures
    # rather than one plain string.
    if isinstance(
        generated_content,
        list
    ):

        text_parts = []

        for part in generated_content:

            if isinstance(
                part,
                dict
            ):

                text = part.get(
                    "text"
                )

                if text:

                    text_parts.append(
                        text
                    )

            elif isinstance(
                part,
                str
            ):

                text_parts.append(
                    part
                )


        generated_content = (
            "\n".join(
                text_parts
            )
        )


    if not generated_content:

        raise RuntimeError(
            "OpenRouter returned an "
            "empty response."
        )


    # --------------------------------------------------------
    # ACTUAL FREE MODEL USED
    # --------------------------------------------------------

    actual_model = (
        response_data.get(
            "model",
            requested_model
        )
    )


    return {

        "provider":
            "OpenRouter",

        "requested_model":
            requested_model,

        "model":
            actual_model,

        "content":
            generated_content,
    }


# ============================================================
# PROVIDER ROUTER
# ============================================================

def call_llm(
    provider,
    system_prompt,
    user_prompt
):
    """
    Route a request to Gemini or OpenRouter.
    """

    provider = (
        str(provider)
        .strip()
        .lower()
    )


    if provider == "gemini":

        return call_gemini(

            system_prompt=
                system_prompt,

            user_prompt=
                user_prompt,
        )


    if provider == "openrouter":

        return call_openrouter(

            system_prompt=
                system_prompt,

            user_prompt=
                user_prompt,
        )


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
    """
    Generate one department-specific report.
    """

    if (
        manager_name
        not in MANAGER_ROLES
    ):

        raise ValueError(
            f"Unknown manager: "
            f"{manager_name}"
        )


    provider = (
        MANAGER_PROVIDERS[
            manager_name
        ]
    )


    department_role = (
        MANAGER_ROLES[
            manager_name
        ]
    )


    system_prompt = f"""
{COMMON_SYSTEM_PROMPT}

You are acting as the:

{manager_name}

YOUR DEPARTMENT RESPONSIBILITY:

{department_role}
"""


    user_prompt = f"""
The following JSON contains the brand reputation
analysis produced from Spotify customer reviews.

ANALYSIS DATA:

{json.dumps(
    analysis_summary,
    indent=2,
    ensure_ascii=False
)}

Generate a department-specific management report.

Use exactly these sections:

# {manager_name} Report

## Department Assessment

Provide a concise overall assessment from your
department's perspective.

## Key Findings

Identify the most important findings relevant to
your department.

## Supporting Evidence

Use only statistics, issue counts, frequent terms,
and representative reviews included in the supplied
analysis.

## Recommended Improvements

Provide practical and specific improvement actions.

## Priority Actions

Organise recommendations under:

### High Priority

### Medium Priority

### Low Priority

## Suggested KPIs

Recommend measurable indicators that could be
monitored by management.

## Limitations

Explain important limitations of the supplied
evidence and model-generated analysis.
"""


    result = call_llm(

        provider=provider,

        system_prompt=system_prompt,

        user_prompt=user_prompt,
    )


    result[
        "manager"
    ] = manager_name


    return result


# ============================================================
# EXECUTIVE MANAGER REPORT
# ============================================================

def generate_executive_report(
    analysis_summary,
    department_reports
):
    """
    Consolidate all department reports.

    Gemini is used as the Executive Manager.
    """

    system_prompt = f"""
{COMMON_SYSTEM_PROMPT}

You are the Executive Manager.

You receive:

1. Overall brand reputation statistics.
2. Reports created by several department managers.

Your responsibility is to consolidate these findings
into one management-level report.

Requirements:

- Remove duplicated recommendations.
- Identify organisation-wide priorities.
- Prioritise actions based on supplied evidence.
- Clearly distinguish evidence from recommendations.
- Do not introduce new statistics.
- Do not invent customer feedback.
"""


    cleaned_reports = {}


    for (
        manager,
        report
    ) in department_reports.items():

        cleaned_reports[
            manager
        ] = {

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
                ),
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
    cleaned_reports,
    indent=2,
    ensure_ascii=False
)}

Generate the final report using exactly these sections:

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


    result = (
        call_gemini_executive(

            system_prompt=
                system_prompt,

            user_prompt=
                user_prompt,
        )
    )


    result[
        "manager"
    ] = "Executive Manager"


    return result
