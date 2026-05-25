from app.validation import validate_report, validate_review, word_count


def test_word_count():
    assert word_count("one two three") == 3
    assert word_count("  spaced   words  ") == 2


def test_validate_report_empty():
    assert validate_report("") == "Report is required."
    assert validate_report("   ") == "Report is required."


def test_validate_report_within_limit():
    assert validate_report("word " * 99) is None


def test_validate_report_over_limit():
    text = "word " * 101
    err = validate_report(text)
    assert err is not None
    assert "100 words" in err


def test_validate_review_valid(valid_review_data):
    cleaned, errors = validate_review(valid_review_data)
    assert errors == []
    assert cleaned["overall_rating"] == "very good"
    assert cleaned["food_quality"] == 4


def test_validate_review_invalid_overall(valid_review_data):
    data = {**valid_review_data, "overall_rating": "amazing"}
    cleaned, errors = validate_review(data)
    assert cleaned is None
    assert any("overall rating" in e for e in errors)


def test_validate_review_invalid_expense(valid_review_data):
    data = {**valid_review_data, "avg_expense_per_head": "-5"}
    cleaned, errors = validate_review(data)
    assert cleaned is None
    assert any("expense" in e for e in errors)


def test_validate_review_report_too_long(valid_review_data):
    data = {**valid_review_data, "report": "word " * 101}
    cleaned, errors = validate_review(data)
    assert cleaned is None
    assert any("100 words" in e for e in errors)
