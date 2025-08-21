import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer

class EducationalDataProcessor:
    """
    Data preprocessing pipeline for educational datasets (PISA, TIMSS)
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.imputer = SimpleImputer(strategy='mean')
    
    def load_data(self, filepath):
        """Load educational data from CSV"""
        try:
            df = pd.read_csv(filepath)
            print(f"Data loaded successfully: {df.shape}")
            return df
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    
    def preprocess_features(self, df):
        """Clean and preprocess educational features"""
        df_processed = df.copy()
        
        # Numerical columns
        numerical_cols = df_processed.select_dtypes(include=[np.number]).columns
        df_processed[numerical_cols] = self.imputer.fit_transform(
            df_processed[numerical_cols]
        )
        
        # Categorical columns
        categorical_cols = df_processed.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
            df_processed[col] = self.label_encoders[col].fit_transform(
                df_processed[col].fillna('Unknown')
            )
        
        # Standardize numerical features
        df_processed[numerical_cols] = self.scaler.fit_transform(
            df_processed[numerical_cols]
        )
        
        return df_processed
    
    def engineer_features(self, df):
        """Create additional features for learning analytics"""
        df_engineered = df.copy()
        
        # Composite score
        if all(col in df.columns for col in ['reading_score','math_score','science_score']):
            df_engineered['composite_score'] = (
                df_engineered['reading_score'] +
                df_engineered['math_score'] +
                df_engineered['science_score']
            ) / 3
        
        # Performance level
        if 'composite_score' in df_engineered.columns:
            df_engineered['performance_level'] = pd.cut(
                df_engineered['composite_score'],
                bins=[0,400,500,600,800],
                labels=['Below Basic','Basic','Proficient','Advanced']
            )
        return df_engineered
