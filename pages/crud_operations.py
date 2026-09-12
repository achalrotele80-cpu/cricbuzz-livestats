import streamlit as st

from services.database_service import (
    create_team,
    update_team,
    delete_team,
    get_table_data,
)


st.title("✏️ CRUD Operations")
st.write("Create, Read, Update and Delete team records.")
st.divider()


# ============================================================
# READ — DISPLAY TEAMS
# ============================================================

st.subheader("👀 View Teams")

columns, rows = get_table_data("teams")

if rows:
    st.dataframe(
        rows,
        column_config={
            "team_id": "Team ID",
            "team_name": "Team Name",
            "country": "Country",
            "team_type": "Team Type",
        },
        use_container_width=True,
    )
else:
    st.info("No teams available.")


st.divider()


# ============================================================
# CREATE
# ============================================================

st.subheader("➕ Create Team")

with st.form("create_team_form"):

    team_id = st.number_input(
        "Team ID",
        min_value=1,
        step=1,
    )

    team_name = st.text_input(
        "Team Name",
    )

    country = st.text_input(
        "Country",
    )

    create_button = st.form_submit_button(
        "Create Team"
    )

    if create_button:

        if not team_name:
            st.warning("Please enter a team name.")

        else:
            try:
                create_team(
                    int(team_id),
                    team_name,
                    country,
                )

                st.success(
                    f"{team_name} created successfully."
                )

                st.rerun()

            except Exception as error:
                st.error(
                    f"Unable to create team: {error}"
                )


st.divider()


# ============================================================
# UPDATE
# ============================================================

st.subheader("✏️ Update Team")

with st.form("update_team_form"):

    update_id = st.number_input(
        "Team ID to Update",
        min_value=1,
        step=1,
        key="update_id",
    )

    new_team_name = st.text_input(
        "New Team Name",
    )

    new_country = st.text_input(
        "New Country",
    )

    update_button = st.form_submit_button(
        "Update Team"
    )

    if update_button:

        if not new_team_name:
            st.warning("Please enter a team name.")

        else:
            try:
                update_team(
                    int(update_id),
                    new_team_name,
                    new_country,
                )

                st.success(
                    "Team updated successfully."
                )

                st.rerun()

            except Exception as error:
                st.error(
                    f"Unable to update team: {error}"
                )


st.divider()


# ============================================================
# DELETE
# ============================================================

st.subheader("🗑️ Delete Team")

with st.form("delete_team_form"):

    delete_id = st.number_input(
        "Team ID to Delete",
        min_value=1,
        step=1,
        key="delete_id",
    )

    delete_button = st.form_submit_button(
        "Delete Team"
    )

    if delete_button:

        try:
            delete_team(
                int(delete_id)
            )

            st.success(
                "Team deleted successfully."
            )

            st.rerun()

        except Exception as error:
            st.error(
                f"Unable to delete team: {error}"
            )
