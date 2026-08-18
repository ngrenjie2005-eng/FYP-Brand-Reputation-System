# ============================================================
# BRANDPULSE AI
# MULTI-PROVIDER LLM SERVICE
#
# Department Managers:
# - Technical Manager         -> OpenRouter
# - Product Manager           -> Ollama Cloud
# - Customer Service Manager  -> OpenRouter
# - Marketing Manager         -> Ollama Cloud
# - Subscription Manager      -> OpenRouter
#
# Executive Manager:
# - Gemini
# ============================================================

import json
import math

import requests
import streamlit as st

from google import genai


# ============================================================
# SECRET HELPER
# ============================================================

def get_secret(
    secret_name,
    default_value=None,
):
    """
    Safely retrieve a value from
    Streamlit Secrets.
    """

    try:

        return st.secrets.get(
            secret_name,
            default_value,
        )

    except Exception:

        return default_value


# ============================================================
# MANAGER PROVIDER MAPPING
# ============================================================

MANAGER_PROVIDERS = {

    "Technical Manager":
        "openrouter",

    "Product Manager":
        "ollama",

    "Customer Service Manager":
        "openrouter",

    "Marketing Manager":
        "ollama",

    "Subscription Manager":
        "openrouter",
}


# ============================================================
# MANAGER ROLE DEFINITIONS
# ============================================================

MANAGER_ROLES = {

    # --------------------------------------------------------
    # TECHNICAL MANAGER
    # --------------------------------------------------------

    "Technical Manager": """
You are the Technical Manager for a digital
music streaming platform.

Your responsibility is to analyse the supplied
brand-reputation evidence from a technical and
software-quality perspective.

Focus primarily on:

- technical performance;
- application crashes;
- software bugs;
- playback failures;
- loading problems;
- application stability;
- reliability;
- account/login technical problems;
- technical customer complaints.

Your recommendations should help the technical
team improve reliability and reduce technical
sources of customer dissatisfaction.

Do not invent statistics.

Do not claim that an issue exists unless it is
supported by the evidence supplied to you.

When evidence is insufficient, clearly state
that the available evidence is insufficient.
""",


    # --------------------------------------------------------
    # PRODUCT MANAGER
    # --------------------------------------------------------

    "Product Manager": """
You are the Product Manager for a digital
music streaming platform.

Your responsibility is to interpret the supplied
brand-reputation evidence from a product and
customer-experience perspective.

Focus primarily on:

- product usability;
- feature quality;
- playlists;
- music library experience;
- navigation;
- user interface;
- customer experience;
- product improvement opportunities;
- recurring feature-related complaints.

Prioritise improvements according to the
evidence supplied.

Do not invent statistics, percentages,
customer counts or research findings.

Recommendations must remain grounded in
the supplied brand-reputation evidence.
""",


    # --------------------------------------------------------
    # CUSTOMER SERVICE MANAGER
    # --------------------------------------------------------

    "Customer Service Manager": """
You are the Customer Service Manager for a
digital music streaming platform.

Analyse the supplied evidence from a customer
service and customer-satisfaction perspective.

Focus primarily on:

- customer complaints;
- customer dissatisfaction;
- customer support problems;
- account difficulties;
- service recovery;
- customer communication;
- repeated customer frustrations;
- customer experience improvements.

Recommend realistic customer-service actions
and measurable KPIs.

Do not invent statistics.

Only use evidence provided by the system.
""",


    # --------------------------------------------------------
    # MARKETING MANAGER
    # --------------------------------------------------------

    "Marketing Manager": """
You are the Marketing Manager for a digital
music streaming platform.

Analyse the supplied brand-reputation evidence
from a marketing and brand-perception
perspective.

Focus primarily on:

- positive brand perception;
- negative brand perception;
- customer sentiment;
- reputation strengths;
- reputation risks;
- customer communication;
- brand messaging;
- positive customer experiences;
- opportunities to improve customer confidence.

Recommendations should be practical and
supported by the supplied evidence.

Do not invent market research, statistics,
competitor information or customer behaviour
that is not included in the evidence.
""",


    # --------------------------------------------------------
    # SUBSCRIPTION MANAGER
    # --------------------------------------------------------

    "Subscription Manager": """
You are the Subscription Manager for a digital
music streaming platform.

Analyse the supplied evidence from a
subscription, pricing and customer-value
perspective.

Focus primarily on:

- Premium subscription;
- subscription pricing;
- billing;
- advertisements;
- customer value perception;
- subscription dissatisfaction;
- potential retention concerns;
- subscription-related complaints.

Recommend evidence-based actions that could
improve customer value perception and
subscription experience.

Do not invent pricing information, customer
retention rates or statistics that are not
included in the supplied evidence.
""",
}


# ============================================================
# COMMON SYSTEM PROMPT
# ============================================================

COMMON_SYSTEM_PROMPT = """
You are part of BrandPulse AI, an academic
brand-reputation decision-support prototype.

The predictive sentiment classification has
already been performed by a trained DistilBERT
model.

You are NOT responsible for predicting
sentiment.

Your role is to interpret structured analytical
evidence produced by the system.

IMPORTANT RULES:

1. Use only evidence supplied in the prompt.

2. Do not invent statistics.

3. Do not invent percentages.

4. Do not invent customer counts.

5. Do not invent review quotations.

6. Do not claim access to external Spotify
   business information.

7. Clearly distinguish observations from
   recommendations.

8. If evidence is insufficient, say so.

9. Recommendations should be practical and
   department-specific.

10. Do not describe recommendations as actions
    that Spotify has already taken.

11. The Brand Reputation Score is a
    project-defined indicator. Do not describe
    it as an official Spotify metric or universal
    industry standard.

12. Issue counts represent detected issue
    mentions. One review may contain more than
    one issue.

Use clear professional English suitable for a
Final Year Project decision-support system.
"""


# ============================================================
# JSON SAFE CONVERSION
# ============================================================

def make_json_safe(
    value,
):
    """
    Convert NumPy/Pandas-like values to
    standard JSON-safe Python objects.
    """

    # --------------------------------------------------------
    # Dictionary
    # --------------------------------------------------------

    if isinstance(
        value,
        dict,
    ):

        return {
            str(key):
                make_json_safe(
                    item
                )

            for (
                key,
                item
            )
            in value.items()
        }


    # --------------------------------------------------------
    # List / Tuple
    # --------------------------------------------------------

    if isinstance(
        value,
        (
            list,
            tuple,
        ),
    ):

        return [
            make_json_safe(
                item
            )

            for item in value
        ]


    # --------------------------------------------------------
    # NumPy-like scalar
    # --------------------------------------------------------

    if hasattr(
        value,
        "item",
    ):

        try:

            return make_json_safe(
                value.item()
            )

        except Exception:

            pass


    # --------------------------------------------------------
    # NaN / Infinity
    # --------------------------------------------------------

    if isinstance(
        value,
        float,
    ):

        if (
            math.isnan(value)
            or
            math.isinf(value)
        ):

            return None


    return value


# ============================================================
# ANALYSIS SUMMARY PREPARATION
# ============================================================

def prepare_analysis_summary(
    analysis_summary,
):
    """
    Keep only the information useful to
    department managers.

    This also reduces unnecessary LLM tokens.
    """

    safe_summary = (
        make_json_safe(
            analysis_summary
        )
    )


    manager_summary = {

        "total_reviews":
            safe_summary.get(
                "total_reviews",
                0,
            ),

        "positive_reviews":
            safe_summary.get(
                "positive_reviews",
                0,
            ),

        "negative_reviews":
            safe_summary.get(
                "negative_reviews",
                0,
            ),

        "positive_percentage":
            safe_summary.get(
                "positive_percentage",
                0,
            ),

        "negative_percentage":
            safe_summary.get(
                "negative_percentage",
                0,
            ),

        "reputation_score":
            safe_summary.get(
                "reputation_score",
                0,
            ),

        "issue_counts":
            safe_summary.get(
                "issue_counts",
                {},
            ),

        "top_positive_words":
            safe_summary.get(
                "top_positive_words",
                [],
            ),

        "top_negative_words":
            safe_summary.get(
                "top_negative_words",
                [],
            ),

        "sample_negative_reviews":
            safe_summary.get(
                "sample_negative_reviews",
                [],
            ),

        "sample_positive_reviews":
            safe_summary.get(
                "sample_positive_reviews",
                [],
            ),
    }


    return manager_summary


# ============================================================
# GEMINI CLIENT
# ============================================================

def create_gemini_client():
    """
    Create Google Gemini client.
    """

    api_key = get_secret(
        "GEMINI_API_KEY"
    )


    if not api_key:

        raise ValueError(
            "GEMINI_API_KEY is missing "
            "from Streamlit Secrets."
        )


    return genai.Client(
        api_key=api_key
    )


# ============================================================
# GEMINI STANDARD CALL
# ============================================================

def call_gemini(
    system_prompt,
    user_prompt,
):
    """
    Standard Gemini call.

    Department managers no longer normally
    use this function, but it is retained
    for provider flexibility.
    """

    model_name = get_secret(
        "GEMINI_MODEL",
        "gemini-3.7-flash",
    )


    client = (
        create_gemini_client()
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
                "thinking_level":
                    "low"
            },
        )
    )


    response_text = (
        interaction.output_text
    )


    if (
        response_text is None
        or
        not str(
            response_text
        ).strip()
    ):

        raise RuntimeError(
            "Gemini returned "
            "an empty response."
        )


    interaction_id = getattr(
        interaction,
        "id",
        None,
    )


    return {

        "provider":
            "Gemini",

        "model":
            model_name,

        "content":
            str(
                response_text
            ).strip(),

        "interaction_id":
            interaction_id,
    }


# ============================================================
# GEMINI EXECUTIVE CALL
# ============================================================

def call_gemini_executive(
    system_prompt,
    user_prompt,
):
    """
    Gemini is reserved primarily for the
    Executive Manager.

    Medium reasoning is used because this
    stage combines five department reports.
    """

    model_name = get_secret(
        "GEMINI_MODEL",
        "gemini-3.7-flash",
    )


    client = (
        create_gemini_client()
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
                "thinking_level":
                    "medium"
            },
        )
    )


    response_text = (
        interaction.output_text
    )


    if (
        response_text is None
        or
        not str(
            response_text
        ).strip()
    ):

        raise RuntimeError(
            "Gemini returned an empty "
            "Executive Manager response."
        )


    interaction_id = getattr(
        interaction,
        "id",
        None,
    )


    return {

        "provider":
            "Gemini",

        "model":
            model_name,

        "content":
            str(
                response_text
            ).strip(),

        "interaction_id":
            interaction_id,
    }


# ============================================================
# OPENROUTER
# ============================================================

def call_openrouter(
    system_prompt,
    user_prompt,
):
    """
    Generate a department report using
    OpenRouter's free router.
    """

    api_key = get_secret(
        "OPENROUTER_API_KEY"
    )


    requested_model = get_secret(
        "OPENROUTER_MODEL",
        "openrouter/free",
    )


    if not api_key:

        raise ValueError(
            "OPENROUTER_API_KEY is missing "
            "from Streamlit Secrets."
        )


    endpoint = (
        "https://openrouter.ai/"
        "api/v1/chat/completions"
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
    }


    response = requests.post(
        endpoint,
        headers=headers,
        json=payload,
        timeout=180,
    )


    if not response.ok:

        raise RuntimeError(
            (
                "OpenRouter request failed. "
                f"HTTP {response.status_code}: "
                f"{response.text[:1000]}"
            )
        )


    data = response.json()


    choices = data.get(
        "choices",
        [],
    )


    if not choices:

        raise RuntimeError(
            "OpenRouter returned no choices."
        )


    generated_content = (
        choices[
            0
        ]
        .get(
            "message",
            {},
        )
        .get(
            "content",
            "",
        )
    )


    if (
        generated_content is None
        or
        not str(
            generated_content
        ).strip()
    ):

        raise RuntimeError(
            "OpenRouter returned "
            "an empty response."
        )


    actual_model = data.get(
        "model",
        requested_model,
    )


    return {

        "provider":
            "OpenRouter",

        "requested_model":
            requested_model,

        "model":
            actual_model,

        "content":
            str(
                generated_content
            ).strip(),
    }


# ============================================================
# OLLAMA CLOUD
# ============================================================

def call_ollama(
    system_prompt,
    user_prompt,
):
    """
    Generate a department-manager report
    using Ollama Cloud.

    Current recommended model:
        gpt-oss:20b
    """

    api_key = get_secret(
        "OLLAMA_API_KEY"
    )


    model_name = get_secret(
        "OLLAMA_MODEL",
        "gpt-oss:20b",
    )


    if not api_key:

        raise ValueError(
            "OLLAMA_API_KEY is missing "
            "from Streamlit Secrets."
        )


    if not model_name:

        raise ValueError(
            "OLLAMA_MODEL is missing "
            "from Streamlit Secrets."
        )


    endpoint = (
        "https://ollama.com/api/chat"
    )


    headers = {

        "Authorization":
            f"Bearer {api_key}",

        "Content-Type":
            "application/json",
    }


    payload = {

        "model":
            model_name,

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

        "stream":
            False,
    }


    response = requests.post(
        endpoint,
        headers=headers,
        json=payload,
        timeout=240,
    )


    # --------------------------------------------------------
    # ERROR HANDLING
    # --------------------------------------------------------

    if not response.ok:

        error_text = (
            response.text[
                :1500
            ]
        )


        if (
            response.status_code
            == 429
        ):

            raise RuntimeError(
                (
                    "Ollama Cloud rate limit "
                    "has been reached. "
                    "Please wait and try again. "
                    f"Details: {error_text}"
                )
            )


        elif (
            response.status_code
            == 404
        ):

            raise RuntimeError(
                (
                    f"Ollama model "
                    f"'{model_name}' was not found. "
                    "Check OLLAMA_MODEL in "
                    "Streamlit Secrets. "
                    f"Details: {error_text}"
                )
            )


        elif (
            response.status_code
            == 502
        ):

            raise RuntimeError(
                (
                    "Ollama Cloud could not "
                    "currently reach the model. "
                    "Please retry later. "
                    f"Details: {error_text}"
                )
            )


        else:

            raise RuntimeError(
                (
                    "Ollama Cloud request failed. "
                    f"HTTP {response.status_code}: "
                    f"{error_text}"
                )
            )


    # --------------------------------------------------------
    # READ RESPONSE
    # --------------------------------------------------------

    data = response.json()


    message = data.get(
        "message",
        {},
    )


    generated_content = (
        message.get(
            "content",
            "",
        )
    )


    if (
        generated_content is None
        or
        not str(
            generated_content
        ).strip()
    ):

        raise RuntimeError(
            "Ollama Cloud returned "
            "an empty response."
        )


    actual_model = data.get(
        "model",
        model_name,
    )


    return {

        "provider":
            "Ollama",

        "requested_model":
            model_name,

        "model":
            actual_model,

        "content":
            str(
                generated_content
            ).strip(),
    }


# ============================================================
# PROVIDER ROUTER
# ============================================================

def call_llm(
    provider,
    system_prompt,
    user_prompt,
):
    """
    Route a request to the requested
    generative AI provider.
    """

    provider = (
        str(provider)
        .strip()
        .lower()
    )


    # --------------------------------------------------------
    # GEMINI
    # --------------------------------------------------------

    if provider == "gemini":

        return call_gemini(
            system_prompt,
            user_prompt,
        )


    # --------------------------------------------------------
    # OPENROUTER
    # --------------------------------------------------------

    if provider == "openrouter":

        return call_openrouter(
            system_prompt,
            user_prompt,
        )


    # --------------------------------------------------------
    # OLLAMA
    # --------------------------------------------------------

    if provider == "ollama":

        return call_ollama(
            system_prompt,
            user_prompt,
        )


    # --------------------------------------------------------
    # INVALID PROVIDER
    # --------------------------------------------------------

    raise ValueError(
        (
            "Unsupported LLM provider: "
            f"{provider}"
        )
    )


# ============================================================
# MANAGER USER PROMPT
# ============================================================

def build_manager_prompt(
    manager_name,
    analysis_summary,
):
    """
    Build one concise structured prompt
    for a department manager.
    """

    evidence = (
        prepare_analysis_summary(
            analysis_summary
        )
    )


    evidence_json = json.dumps(
        evidence,
        indent=2,
        ensure_ascii=False,
    )


    return f"""
BRANDPULSE AI
DEPARTMENT ANALYSIS REQUEST

Manager:
{manager_name}


============================================================
BRAND REPUTATION EVIDENCE
============================================================

{evidence_json}


============================================================
REQUIRED OUTPUT
============================================================

Produce a concise professional department
report using the following structure:

## 1. Department Overview

Briefly explain what the supplied evidence
means for your department.


## 2. Key Findings

Identify the most important evidence that is
relevant to your department.

Use actual supplied values where appropriate.

Do not create new statistics.


## 3. Main Reputation Risks

Identify the most important reputation risks
relevant to your department.

If the evidence does not support a particular
risk, do not include it.


## 4. Positive Signals

Identify relevant positive customer signals.

If limited positive evidence is available,
state this clearly.


## 5. Recommended Actions

Provide 3 to 5 practical department-specific
actions.

Clearly present these as recommendations,
not actions that have already happened.


## 6. Recommended KPIs

Provide 3 to 5 measurable KPIs that management
could use to monitor improvement.

Do not claim current KPI values unless those
values exist in the supplied evidence.


## 7. Priority Level

Give an overall department priority:

- High
- Medium
- Low

Briefly justify the priority using the supplied
evidence.


## 8. Limitations

State any important limitations in the available
evidence.


Keep the report focused and concise.
Do not repeat the same recommendation several
times.
"""


# ============================================================
# GENERATE MANAGER REPORT
# ============================================================

def generate_manager_report(
    manager_name,
    analysis_summary,
):
    """
    Generate one department-manager report.
    """

    # --------------------------------------------------------
    # VALIDATE MANAGER
    # --------------------------------------------------------

    if (
        manager_name
        not in MANAGER_ROLES
    ):

        raise ValueError(
            (
                "Unknown manager: "
                f"{manager_name}"
            )
        )


    # --------------------------------------------------------
    # PROVIDER
    # --------------------------------------------------------

    provider = (
        MANAGER_PROVIDERS[
            manager_name
        ]
    )


    # --------------------------------------------------------
    # SYSTEM PROMPT
    # --------------------------------------------------------

    system_prompt = (
        COMMON_SYSTEM_PROMPT
        + "\n\n"
        + MANAGER_ROLES[
            manager_name
        ]
    )


    # --------------------------------------------------------
    # USER PROMPT
    # --------------------------------------------------------

    user_prompt = (
        build_manager_prompt(
            manager_name,
            analysis_summary,
        )
    )


    # --------------------------------------------------------
    # CALL PROVIDER
    # --------------------------------------------------------

    result = (
        call_llm(
            provider=provider,
            system_prompt=(
                system_prompt
            ),
            user_prompt=(
                user_prompt
            ),
        )
    )


    # --------------------------------------------------------
    # REPORT METADATA
    # --------------------------------------------------------

    result[
        "manager"
    ] = manager_name


    result[
        "configured_provider"
    ] = provider


    return result


# ============================================================
# EXECUTIVE SYSTEM PROMPT
# ============================================================

EXECUTIVE_SYSTEM_PROMPT = """
You are the Executive Manager in BrandPulse AI,
an academic brand-reputation decision-support
prototype.

Five department managers have already analysed
the same underlying brand-reputation evidence.

Your responsibility is to consolidate their
findings into one organisation-wide executive
report.

IMPORTANT RULES:

1. Use only supplied analytical evidence and
   department reports.

2. Do not invent statistics.

3. Do not invent percentages.

4. Do not invent financial results.

5. Do not invent Spotify internal information.

6. Do not state recommendations as actions that
   have already occurred.

7. Identify agreement between departments.

8. Resolve overlapping recommendations by
   combining them where appropriate.

9. Prioritise actions according to the supplied
   evidence.

10. Clearly distinguish:
    - evidence;
    - interpretation;
    - recommendation.

11. The Brand Reputation Score is a
    project-defined indicator, not an official
    Spotify or industry-standard reputation
    measure.

12. If evidence is insufficient, explicitly
    state the limitation.

Use concise professional language suitable for
an academic Final Year Project and management
decision-support report.
"""


# ============================================================
# PREPARE EXECUTIVE DEPARTMENT REPORTS
# ============================================================

def prepare_department_reports_for_executive(
    department_reports,
):
    """
    Keep only essential report information.

    This helps reduce Gemini input usage because
    Gemini is reserved for the final Executive
    Manager call.
    """

    prepared_reports = {}


    for (
        manager_name,
        report
    ) in department_reports.items():

        prepared_reports[
            manager_name
        ] = {

            "provider":
                report.get(
                    "provider",
                    "Unknown",
                ),

            "model":
                report.get(
                    "model",
                    "Unknown",
                ),

            "content":
                report.get(
                    "content",
                    "",
                ),
        }


    return make_json_safe(
        prepared_reports
    )


# ============================================================
# EXECUTIVE PROMPT
# ============================================================

def build_executive_prompt(
    analysis_summary,
    department_reports,
):
    """
    Build the final Executive Manager prompt.
    """

    evidence = (
        prepare_analysis_summary(
            analysis_summary
        )
    )


    prepared_reports = (
        prepare_department_reports_for_executive(
            department_reports
        )
    )


    evidence_json = json.dumps(
        evidence,
        indent=2,
        ensure_ascii=False,
    )


    department_json = json.dumps(
        prepared_reports,
        indent=2,
        ensure_ascii=False,
    )


    return f"""
BRANDPULSE AI
EXECUTIVE CONSOLIDATION REQUEST


============================================================
CORE BRAND REPUTATION EVIDENCE
============================================================

{evidence_json}


============================================================
DEPARTMENT MANAGER REPORTS
============================================================

{department_json}


============================================================
REQUIRED EXECUTIVE REPORT
============================================================

Generate one consolidated executive report using
the following structure:


## 1. Executive Summary

Summarise the overall reputation condition and
the most important management message.


## 2. Overall Brand Reputation

Interpret the sentiment distribution and
project-defined Brand Reputation Score.

Do not describe the score as an official
industry metric.


## 3. Main Brand Strengths

Identify the strongest positive signals supported
by the evidence.


## 4. Critical Reputation Risks

Identify the most important risks appearing in
the evidence and department reports.


## 5. Cross-Department Findings

Identify issues that affect more than one
department.


## 6. Immediate Management Priorities

Provide the most urgent actions management
should consider.


## 7. Short-Term Action Plan

Recommend actions that could reasonably be
prioritised in the near term.


## 8. Long-Term Improvement Direction

Recommend broader strategic improvements.


## 9. Recommended Executive KPIs

Provide measurable KPIs management could monitor.

Do not invent current KPI values.


## 10. Department Coordination

Explain how the relevant departments should
coordinate their recommended actions.


## 11. Overall Management Recommendation

Provide a concise final recommendation.


## 12. Limitations

State limitations of:

- sentiment predictions;
- keyword-based issue categorisation;
- available review evidence;
- LLM-generated recommendations.


Keep the executive report focused and avoid
unnecessary repetition of complete department
reports.
"""


# ============================================================
# GENERATE EXECUTIVE REPORT
# ============================================================

def generate_executive_report(
    analysis_summary,
    department_reports,
):
    """
    Generate the final Executive Manager
    report using Gemini.

    Gemini is intentionally reserved for
    this final consolidation stage.
    """

    # --------------------------------------------------------
    # VERIFY ALL MANAGERS
    # --------------------------------------------------------

    required_managers = set(
        MANAGER_ROLES.keys()
    )


    completed_managers = set(
        department_reports.keys()
    )


    missing_managers = (
        required_managers
        -
        completed_managers
    )


    if missing_managers:

        raise ValueError(
            (
                "Executive Report requires "
                "all five department reports. "
                "Missing: "
                + ", ".join(
                    sorted(
                        missing_managers
                    )
                )
            )
        )


    # --------------------------------------------------------
    # BUILD PROMPT
    # --------------------------------------------------------

    user_prompt = (
        build_executive_prompt(
            analysis_summary,
            department_reports,
        )
    )


    # --------------------------------------------------------
    # ONE GEMINI EXECUTIVE CALL
    # --------------------------------------------------------

    result = (
        call_gemini_executive(
            system_prompt=(
                EXECUTIVE_SYSTEM_PROMPT
            ),
            user_prompt=(
                user_prompt
            ),
        )
    )


    result[
        "manager"
    ] = "Executive Manager"


    return result
