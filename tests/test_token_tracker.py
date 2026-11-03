from tools.token_tracker import estimate_tokens, load_usage, log_interaction


def test_estimates_tokens_from_words():
    assert estimate_tokens("one two three four") == 6


def test_logs_interaction_and_updates_total(tmp_path):
    log_file = tmp_path / "token_usage.json"

    first = log_interaction("Hello there", role="user", path=log_file)
    log_interaction("Hello back", role="assistant", path=log_file)

    usage = load_usage(log_file)
    assert first["tokens"] == 3
    assert usage["total_tokens"] == 6
    assert [item["role"] for item in usage["interactions"]] == ["user", "assistant"]
