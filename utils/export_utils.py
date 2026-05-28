# =========================================================
# utils/export_utils.py
# =========================================================

import pandas as pd
from io import BytesIO

# =========================================================
# EXPORT CSV
# =========================================================

def export_entities_csv(entities):

    df = pd.DataFrame(entities)

    return df.to_csv(
        index=False
    )

# =========================================================
# EXPORT EXCEL
# =========================================================

def export_entities_excel(entities):

    df = pd.DataFrame(entities)

    output = BytesIO()

    with pd.ExcelWriter(

        output,

        engine="openpyxl"

    ) as writer:

        df.to_excel(

            writer,

            index=False,

            sheet_name="Entities"
        )

    return output.getvalue()