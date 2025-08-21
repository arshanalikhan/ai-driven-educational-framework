# (If you prefer to split out feature engineering into its own module)
import pandas as pd

def create_composite_and_levels(df):
    """
    Given a DataFrame with reading_score, math_score, and science_score,
    compute a composite_score and performance_level.
    """
    df_copy = df.copy()
    df_copy['composite_score'] = (
        df_copy['reading_score'] +
        df_copy['math_score'] +
        df_copy['science_score']
    ) / 3
    
    df_copy['performance_level'] = pd.cut(
        df_copy['composite_score'],
        bins=[0,400,500,600,800],
        labels=['Below Basic','Basic','Proficient','Advanced']
    )
    return df_copy
