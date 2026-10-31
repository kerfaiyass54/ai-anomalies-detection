from dataclasses import dataclass

from sklearn.model_selection import train_test_split

from ....schemas.processed_log import ProcessedLog


@dataclass(frozen=True)
class LogDataSplit:
    training: list[ProcessedLog]
    testing: list[ProcessedLog]


def split_log_data(logs: list[ProcessedLog], *, test_size: float = 0.2) -> LogDataSplit:
    """Create deterministic train and holdout sets for unsupervised log modeling."""
    training, testing = train_test_split(logs, test_size=test_size, random_state=42, shuffle=True)
    return LogDataSplit(training=list(training), testing=list(testing))
