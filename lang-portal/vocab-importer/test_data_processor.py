import pytest
from data_processor import DataProcessor

def test_filter_by_level():
    # Sample test data
    test_subjects = [
        {
            "object": "kanji",
            "data": {"level": 1, "hidden_at": None, "characters": "一"}
        },
        {
            "object": "kanji",
            "data": {"level": 3, "hidden_at": None, "characters": "見"}
        },
        {
            "object": "vocabulary",
            "data": {"level": 2, "hidden_at": None, "characters": "二つ"}
        },
        {
            "object": "kanji",
            "data": {"level": 4, "hidden_at": None, "characters": "私"}
        },
        {
            "object": "vocabulary",
            "data": {"level": 3, "hidden_at": "2024-01-01", "characters": "隠す"}
        }
    ]
    
    # Test filtering at level 3
    processor = DataProcessor(user_level=3)
    filtered = processor.filter_by_level(test_subjects)
    
    assert len(filtered) == 3, "Should only include 3 items (level ≤ 3 and not hidden)"
    assert all(s["data"]["level"] <= 3 for s in filtered), "All items should be level 3 or lower"
    assert all(s["data"]["hidden_at"] is None for s in filtered), "Should not include hidden items"
    
    # Test with lower level
    processor_level_1 = DataProcessor(user_level=1)
    filtered_level_1 = processor_level_1.filter_by_level(test_subjects)
    assert len(filtered_level_1) == 1, "Should only include 1 item at level 1"
    
    # Test with max level (60)
    processor_max = DataProcessor(user_level=60)
    filtered_max = processor_max.filter_by_level(test_subjects)
    assert len(filtered_max) == 4, "Should include all non-hidden items at max level"
    assert sorted([s["data"]["characters"] for s in filtered_max]) == ["一", "二つ", "私", "見"], \
        "Should include all non-hidden items in the correct order"
    
    # Test with empty list
    assert processor.filter_by_level([]) == [], "Should handle empty list"
