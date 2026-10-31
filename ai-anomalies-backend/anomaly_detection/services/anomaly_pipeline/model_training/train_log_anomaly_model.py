from sklearn.ensemble import IsolationForest
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline


def train_log_anomaly_model(training_messages: list[str]) -> Pipeline:
    """Fit an Isolation Forest over character n-gram representations of logs."""
    model = Pipeline([
        ("features", TfidfVectorizer(analyzer="char", ngram_range=(2, 5), max_features=10000)),
        ("detector", IsolationForest(n_estimators=200, contamination="auto", random_state=42)),
    ])
    model.fit(training_messages)
    return model
