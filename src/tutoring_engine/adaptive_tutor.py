from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from .skill_classifier import SkillClassifier
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

class AdaptiveTutoringEngine:
    """
    Hybrid AI tutoring system combining Random Forest and Neural Networks
    """
    def __init__(self):
        self.skill_classifier = SkillClassifier()
        self.intervention_model = None
        self.is_trained = False
    
    def prepare_training_data(self, df):
        X = df[['reading_score','math_score','science_score','socioeconomic_status']].values
        y = df['performance_level'].values
        return X, y
    
    def train_skill_classifier(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        accuracy = self.skill_classifier.train(X_train, y_train)
        y_pred = self.skill_classifier.predict(X_test)
        print(f"Skill Classifier Accuracy: {accuracy:.3f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        self.is_trained = True
        return accuracy
    
    def build_intervention_model(self, input_dim, output_dim):
        model = Sequential([
            Dense(128, activation='relu', input_dim=input_dim),
            Dropout(0.3),
            Dense(64, activation='relu'),
            Dropout(0.3),
            Dense(32, activation='relu'),
            Dense(output_dim, activation='softmax')
        ])
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        self.intervention_model = model
        return model
    
    def predict_skill_level(self, student_features):
        if not self.is_trained:
            raise ValueError("Skill classifier must be trained first.")
        return self.skill_classifier.predict([student_features])[0]
    
    def recommend_intervention(self, student_features, skill_level):
        interventions = {
            'Below Basic': ['Foundational review','One-on-one tutoring','Simulations'],
            'Basic': ['Practice exercises','Peer collaboration','Scaffolded learning'],
            'Proficient': ['Advanced problems','Project-based tasks','Cross-curricular ties'],
            'Advanced': ['Independent research','Mentoring peers','Creative projects']
        }
        return interventions.get(skill_level, ['Standard curriculum'])
