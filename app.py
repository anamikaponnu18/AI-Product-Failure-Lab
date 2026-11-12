
import streamlit as st
import pandas as pd

from persona_engine import generate_personas
from evaluation_engine import evaluate_persona
from analysis_engine import summarize_results


# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="AI Product Failure Lab",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 AI Product Failure Lab")

st.write(
    "Simulate diverse consumer personas to evaluate product ideas "
    "and identify potential success factors and risks."
)


# --------------------------------
# SIDEBAR
# --------------------------------

st.sidebar.header("Simulation Settings")

persona_count = st.sidebar.slider(
    "Number of Synthetic Personas",
    min_value=5,
    max_value=100,
    value=20,
    step=5
)

st.sidebar.info(
    "This application uses Python-based persona generation "
    "and rule-based evaluation. No LLM or API key is required."
)


# --------------------------------
# PRODUCT INPUT
# --------------------------------

st.header("1. Enter Product Information")

product_name = st.text_input(
    "Product Name",
    placeholder="Example: Smart Water Bottle"
)

product_description = st.text_area(
    "Product Description",
    placeholder="Describe the product, its features, price, benefits and target audience.",
    height=150
)


# --------------------------------
# SIMULATION
# --------------------------------

if st.button("Run Product Evaluation", type="primary"):

    if not product_name.strip() or not product_description.strip():
        st.warning("Please enter both product name and description.")

    else:

        product = (
            f"Product Name: {product_name}\n"
            f"Product Description: {product_description}"
        )

        st.session_state["product"] = product
        st.session_state["product_name"] = product_name

        with st.spinner("Generating synthetic consumer personas..."):

            personas = generate_personas(
                number=persona_count,
                seed=42
            )

        results = []

        progress = st.progress(0)
        status = st.empty()

        for index, persona in enumerate(personas):

            result = evaluate_persona(
                persona,
                product
            )

            results.append(result)

            progress.progress(
                (index + 1) / len(personas)
            )

            status.write(
                f"Evaluating persona {index + 1} of {len(personas)}..."
            )

        st.session_state["results"] = results

        progress.empty()
        status.success("Product evaluation completed!")


# --------------------------------
# DISPLAY RESULTS
# --------------------------------

if "results" in st.session_state:

    results = st.session_state["results"]

    st.divider()

    st.header("2. Evaluation Results")

    summary = summarize_results(results)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Average Interest Score",
        f"{summary['average_interest']:.2f}/10"
    )

    col2.metric(
        "Positive Responses",
        f"{summary['positive_pct']:.1f}%"
    )

    col3.metric(
        "High Adoption Likelihood",
        f"{summary['high_adoption_pct']:.1f}%"
    )

    # --------------------------------
    # STANCE DISTRIBUTION
    # --------------------------------

    st.subheader("Consumer Response Distribution")

    stance_data = pd.DataFrame(
        list(summary["stance_counts"].items()),
        columns=["Consumer Response", "Number of Personas"]
    )

    st.bar_chart(
        stance_data.set_index("Consumer Response")
    )

    # --------------------------------
    # ADOPTION LIKELIHOOD
    # --------------------------------

    st.subheader("Adoption Likelihood")

    adoption_data = pd.DataFrame(
        list(summary["adoption_counts"].items()),
        columns=["Adoption Likelihood", "Number of Personas"]
    )

    st.bar_chart(
        adoption_data.set_index("Adoption Likelihood")
    )

    # --------------------------------
    # OVERALL ASSESSMENT
    # --------------------------------

    st.subheader("Overall Product Assessment")

    st.write(summary["assessment"])

    st.write(
        f"**Identified Risk Level:** {summary['risk_level']}"
    )

    # --------------------------------
    # COMMON FEEDBACK
    # --------------------------------

    st.subheader("Common Positive Factors")

    for item in summary["top_positives"]:
        st.write(f"✅ {item}")

    st.subheader("Common Product Concerns")

    for item in summary["top_concerns"]:
        st.write(f"⚠️ {item}")

    st.subheader("Suggested Improvements")

    for item in summary["top_improvements"]:
        st.write(f"💡 {item}")

    # --------------------------------
    # INDIVIDUAL PERSONA RESULTS
    # --------------------------------

    st.divider()

    st.header("3. Individual Persona Evaluations")

    for index, result in enumerate(results):

        persona = result["persona"]

        with st.expander(
            f"Persona {index + 1} | "
            f"{persona.get('archetype', 'Consumer')} | "
            f"Interest: {result['interest_score']}/10"
        ):

            st.write("### Persona Profile")

            st.json(persona)

            st.write("### Evaluation")

            st.write(
                f"**Interest Score:** {result['interest_score']}/10"
            )

            st.write(
                f"**Stance:** {result['stance']}"
            )

            st.write(
                f"**Adoption Likelihood:** {result['adoption_likelihood']}"
            )

            st.write("**Reasoning:**")
            st.write(result["reasoning"])

            st.write("**Positive Factors:**")
            for item in result["positives"]:
                st.write(f"- {item}")

            st.write("**Concerns:**")
            for item in result["concerns"]:
                st.write(f"- {item}")

            st.write("**Improvements:**")
            for item in result["improvements"]:
                st.write(f"- {item}")

    # --------------------------------
    # DOWNLOAD RESULTS
    # --------------------------------

    st.divider()

    st.header("4. Download Evaluation Results")

    export_data = []

    for result in results:

        persona = result["persona"]

        export_data.append({
            "Archetype": persona.get("archetype", ""),
            "Interest Score": result["interest_score"],
            "Stance": result["stance"],
            "Adoption Likelihood": result["adoption_likelihood"],
            "Positive Factors": "; ".join(result["positives"]),
            "Concerns": "; ".join(result["concerns"]),
            "Improvements": "; ".join(result["improvements"]),
            "Reasoning": result["reasoning"]
        })

    results_df = pd.DataFrame(export_data)

    st.download_button(
        label="Download Results as CSV",
        data=results_df.to_csv(index=False).encode("utf-8"),
        file_name="product_evaluation_results.csv",
        mime="text/csv"
    )
